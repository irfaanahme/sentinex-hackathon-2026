import unittest
import app


class MedicationTests(unittest.TestCase):
    def test_brand_and_typo_resolution(self):
        for text, expected in [('Alphatb', 'A'), ('BetaTba', 'B'), ('GamaTab', 'C'), ('AlphaPlus', 'A')]:
            self.assertEqual(app.resolve(text)['drug_id'], expected)

    def test_ambiguous_and_unknown_stay_unresolved(self):
        self.assertIsNone(app.resolve('UnknownDrug')['drug_id'])
        self.assertIsNone(app.resolve('Demo')['drug_id'])

    def test_all_four_issue_types_and_priority(self):
        review = app.check_patient(app.PATIENTS['review'])
        self.assertEqual({a['rule_id'] for a in review['alerts']}, {'INT-01', 'REN-A', 'DUP-A'})
        self.assertEqual(review['alerts'][-1]['severity'], 'MODERATE')
        self.assertTrue(all(a['limitations'] and a['confidence'] and a['action'] for a in review['alerts']))
        pregnancy = app.check_patient(app.PATIENTS['pregnancy'])
        self.assertEqual(pregnancy['alerts'][0]['issue'], 'Contraindication')

    def test_same_class_duplicates(self):
        result = app.check_patient({'medications': ['AlphaTab', 'DeltaTab'], 'egfr': 90, 'pregnant': False})
        self.assertIn('CLASS-AD', {a['rule_id'] for a in result['alerts']})

    def test_incomplete_inputs_never_claim_safe(self):
        result = app.check_patient(app.PATIENTS['incomplete'])
        self.assertIn('does not establish safety', result['message'])
        self.assertTrue(any('Kidney-function' in note for note in result['limitations']))
        self.assertTrue(any('Unresolved' in note for note in result['limitations']))

    def test_no_issue_does_not_create_alerts(self):
        self.assertEqual(app.check_patient(app.PATIENTS['no_issue'])['alerts'], [])

    def test_api_validation(self):
        client = app.app.test_client()
        self.assertEqual(client.post('/api/check', json={'case': 'invalid'}).status_code, 400)
        self.assertEqual(client.post('/api/check', json={'patient': {'medications': ['AlphaTab'], 'egfr': -1}}).status_code, 400)
        self.assertEqual(client.post('/api/check', json={'case': 'review'}).status_code, 200)

    def test_demo_evaluation_no_official_claim(self):
        result = app.evaluate()
        self.assertEqual(result['matching'], {'passed': 8, 'total': 8})
        self.assertEqual(result['serious'], {'found': 3, 'total': 3})
        self.assertEqual(result['extra_alerts'], 0)
        self.assertIsNone(result['official_near_miss_recall'])


if __name__ == '__main__':
    unittest.main()
