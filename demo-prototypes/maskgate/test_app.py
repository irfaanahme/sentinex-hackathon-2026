import unittest
import app


class MaskGateTests(unittest.TestCase):
    def setUp(self):
        self.client = app.app.test_client()

    def login(self, account):
        return self.client.post('/api/session', json={'account': account}, headers={'X-MaskGate-Demo': 'local'})

    def test_unauthenticated_query_rejected(self):
        response = self.client.post('/api/query', json={'backend': 'SQLite', 'query_id': 'customer_directory'})
        self.assertEqual(response.status_code, 401)

    def test_all_roles_both_backends_and_no_source_changes(self):
        for backend in app.BACKENDS:
            before = app.digest(backend)
            for account, role in app.ACCOUNTS.items():
                self.login(account)
                response = self.client.post('/api/query', json={'backend': backend, 'query_id': 'customer_directory'})
                self.assertEqual(response.status_code, 200)
                row = response.json['rows'][0]
                self.assertEqual(response.json['role'], role)
                if role == 'Admin':
                    self.assertEqual(row['card_number'], '4111111111111111')
                elif role == 'Support':
                    self.assertEqual(row['card_number'], '**** **** **** 1111')
                    self.assertEqual(row['account_balance'], '[REDACTED]')
                else:
                    self.assertEqual(row['card_number'], '[REDACTED]')
                    self.assertRegex(row['email'], '^hash:[a-f0-9]{12}$')
                    self.assertNotIn('customer.a@example.test', response.get_data(as_text=True))
            self.assertEqual(app.digest(backend), before)

    def test_forged_roles_sql_queries_and_accounts_rejected(self):
        self.login('support.demo')
        for payload in [
            {'backend': 'SQLite', 'query_id': 'customer_directory', 'role': 'Admin'},
            {'backend': 'SQLite', 'query_id': 'customer_directory', 'sql': 'SELECT * FROM customers'},
            {'backend': 'SQLite', 'query_id': 'customers WHERE 1=1'},
            {'backend': 'invalid', 'query_id': 'customer_directory'},
        ]:
            self.assertEqual(self.client.post('/api/query', json=payload).status_code, 403)
        self.assertEqual(self.login('unknown.demo').status_code, 400)

    def test_cookie_tampering_rejected(self):
        self.login('support.demo')
        cookie = self.client.get_cookie('session').value
        self.client.set_cookie('session', cookie + 'tampered')
        self.assertEqual(self.client.post('/api/query', json={'backend': 'SQLite', 'query_id': 'customer_directory'}).status_code, 401)

    def test_scanner_empty_mixed_neutral_and_known_false_positive(self):
        self.assertEqual(app.classify('reference', [None, '', '4111111111111111'])[0], 'PII_HIGH')
        self.assertEqual(app.classify('reference', [None, ''])[0], 'PUBLIC')
        self.assertEqual(app.classify('contact', ['demo@example.test'])[0], 'PII_HIGH')
        self.assertEqual(app.classify('email_opt_in', ['yes', 'no'])[0], 'PII_HIGH')
        self.assertIsNone(app.transform(None, 'email', 'PII_HIGH', 'Analyst'))

    def test_measured_evaluation(self):
        result = self.client.get('/api/evaluate').json
        self.assertEqual(result['policy'], {'passed': 144, 'total': 144})
        self.assertEqual(result['scanner']['fp'], 1)
        self.assertEqual(result['scanner']['recall'], 1.0)
        self.assertTrue(all(c['unchanged'] for c in result['source_checks']))
        self.assertEqual(len(result['latency']), 2)


if __name__ == '__main__':
    unittest.main()
