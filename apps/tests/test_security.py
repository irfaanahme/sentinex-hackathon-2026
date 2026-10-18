"""Regression tests for the pre-hosting findings and deployment boundary."""
import importlib.util,io,os,sys,tempfile,time,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from common.core import create_app,connect
from werkzeug.security import generate_password_hash
from werkzeug.test import Client
from werkzeug.wrappers import Response
PASSWORD='Separate testing password 2026'

def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

class SecurityTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
  self.env=patch.dict(os.environ,{'TEST_DATA':str(self.root/'state'),'APP_MODE':'local','TEST_PREFIX':''});self.env.start()
  self.app=create_app('test',self.root,['Admin','Support']);self.app.config['TESTING']=True
  @self.app.get('/api/protected')
  def protected():return {'ok':True}
  self.c=self.app.test_client()
  self.assertEqual(self.c.post('/api/setup',json={'name':'owner','password':PASSWORD},headers={'X-Local-App':'1'}).status_code,200)
  self.h=self.headers(self.c)
 def tearDown(self):self.env.stop();self.temp.cleanup()
 def headers(self,c):return {'X-Local-App':'1','X-CSRF-Token':c.get('/api/status').json['csrf']}
 def login(self,c,name='owner',password=PASSWORD):return c.post('/api/login',json={'name':name,'password':password},headers={'X-Local-App':'1'})
 def new_user(self,name='member'):
  self.assertEqual(self.c.post('/api/users',json={'name':name,'password':PASSWORD,'role':'Support'},headers=self.h).status_code,201)
 def test_logout_rejects_copied_cookie(self):
  copied=self.c.get_cookie('test_session').value
  self.assertEqual(self.c.post('/api/logout',headers=self.h).status_code,200)
  other=self.app.test_client();other.set_cookie('test_session',copied)
  self.assertEqual(other.get('/api/protected').status_code,401)
 def test_all_devices_revoked(self):
  other=self.app.test_client();self.login(other)
  self.c.post('/api/account/sign-out-all',headers=self.h)
  self.assertEqual(other.get('/api/protected').status_code,401)
  self.assertEqual(self.c.get('/api/protected').status_code,401)
 def test_password_change_revokes_other_sessions(self):
  other=self.app.test_client();self.login(other)
  r=self.c.post('/api/account/password',json={'current_password':PASSWORD,'new_password':'A different strong password 2026'},headers=self.h)
  self.assertEqual(r.status_code,200);self.assertEqual(other.get('/api/protected').status_code,401)
  self.assertEqual(self.login(other).status_code,401)
  self.assertEqual(self.login(other,password='A different strong password 2026').status_code,200)
 def test_wrong_password_cannot_change_password(self):
  self.assertEqual(self.c.post('/api/account/password',json={'current_password':'incorrect','new_password':'Some strong new password'},headers=self.h).status_code,403)
 def test_disabled_user_cannot_replay_or_login(self):
  self.new_user();other=self.app.test_client();self.login(other,'member')
  self.assertEqual(self.c.post('/api/users/member/status',json={'disabled':True},headers=self.h).status_code,200)
  self.assertEqual(other.get('/api/protected').status_code,401);self.assertEqual(self.login(other,'member').status_code,401)
 def test_user_cannot_disable_owner(self):
  self.new_user();other=self.app.test_client();self.login(other,'member')
  self.assertEqual(other.post('/api/users/owner/status',json={'disabled':True},headers=self.headers(other)).status_code,403)
  self.assertEqual(self.c.post('/api/users/owner/status',json={'disabled':True},headers=self.h).status_code,400)
 def test_other_login_cannot_clear_target_rate_limit(self):
  self.new_user();other=self.app.test_client()
  for _ in range(9):self.assertEqual(self.login(other,password='wrong').status_code,401)
  self.assertEqual(self.login(other,'member').status_code,200)
  self.assertEqual(self.login(other,password='wrong').status_code,401)
  self.assertEqual(self.login(other,password='wrong').status_code,429)
 def test_rate_limit_persists_after_app_restart(self):
  other=self.app.test_client()
  for _ in range(10):self.login(other,password='wrong')
  reopened=create_app('test',self.root,['Admin','Support'])
  self.assertEqual(self.login(reopened.test_client(),password='wrong').status_code,429)
 def test_absolute_session_expiry(self):
  with connect(self.app.config['DB']) as db:db.execute('UPDATE sessions SET expires=?',(time.time()-1,))
  self.assertEqual(self.c.get('/api/protected').status_code,401)
 def test_idle_session_expiry(self):
  with connect(self.app.config['DB']) as db:db.execute('UPDATE sessions SET seen=?',(time.time()-1900,))
  self.assertEqual(self.c.get('/api/protected').status_code,401)
 def test_csrf_and_origin(self):
  self.assertEqual(self.c.post('/api/account/sign-out-all',headers={'X-Local-App':'1'}).status_code,403)
  self.assertEqual(self.c.post('/api/account/sign-out-all',headers={**self.h,'Origin':'https://evil.test'}).status_code,403)
  self.assertEqual(self.c.post('/api/account/sign-out-all',headers={**self.h,'Sec-Fetch-Site':'cross-site'}).status_code,403)
 def test_no_cookie_identity_without_session_record(self):
  other=self.app.test_client()
  with other.session_transaction() as s:s['user']='owner';s['csrf']='old'
  self.assertEqual(other.get('/api/protected').status_code,401)
 def test_overlong_username_cannot_alias_real_account(self):
  username='a'*40
  self.new_user(username)
  other=self.app.test_client()
  self.assertEqual(self.login(other,username+'suffix').status_code,401)
  self.assertEqual(other.get('/api/protected').status_code,401)
  self.assertEqual(self.login(other,username).status_code,200)
 def test_password_rotation_during_login_cannot_issue_old_session(self):
  import common.core as core
  original=core.check_password_hash
  other=self.app.test_client()
  def rotate_after_check(hashed,password):
   valid=original(hashed,password)
   with connect(self.app.config['DB']) as db:
    db.execute('UPDATE users SET password=? WHERE name=?',(generate_password_hash('Rotated concurrently long password'),'owner'))
    db.execute('DELETE FROM sessions WHERE user=?',('owner',))
   return valid
  with patch.object(core,'check_password_hash',side_effect=rotate_after_check):
   self.assertEqual(self.login(other).status_code,400)
  self.assertEqual(other.get('/api/protected').status_code,401)
 def test_concurrent_password_change_does_not_overwrite_newer_password(self):
  import common.core as core
  original=core.check_password_hash
  replacement=generate_password_hash('Already rotated separate password')
  def rotate_after_check(hashed,password):
   valid=original(hashed,password)
   with connect(self.app.config['DB']) as db:db.execute('UPDATE users SET password=? WHERE name=?',(replacement,'owner'))
   return valid
  with patch.object(core,'check_password_hash',side_effect=rotate_after_check):
   r=self.c.post('/api/account/password',json={'current_password':PASSWORD,'new_password':'A late overwritten password 2026'},headers=self.h)
  self.assertEqual(r.status_code,400)
  with connect(self.app.config['DB']) as db:self.assertEqual(db.execute('SELECT password FROM users WHERE name=?',('owner',)).fetchone()[0],replacement)
 def test_hosted_bootstrap_tls_and_headers(self):
  with patch.dict(os.environ,{'APP_MODE':'hosted','APP_PUBLIC_ORIGIN':'https://team.example','TEST_DATA':str(self.root/'hosted')}):
   app=create_app('test',self.root,['Admin','Support']);c=app.test_client()
   self.assertEqual(c.post('/api/setup',base_url='https://team.example',headers={'X-Local-App':'1'},json={'name':'intruder','password':PASSWORD}).status_code,403)
   self.assertTrue(c.get('/api/status',base_url='https://team.example').json['setup_locked'])
   self.assertEqual(c.get('/api/status',base_url='http://team.example').status_code,400)
   self.assertEqual(c.get('/api/status',base_url='https://evil.example').status_code,400)
   r=app.test_client().get('/api/status',base_url='https://team.example')
   self.assertIn('Secure',r.headers['Set-Cookie']);self.assertIn('HttpOnly',r.headers['Set-Cookie']);self.assertEqual(r.headers['Referrer-Policy'],'no-referrer');self.assertIn("object-src 'none'",r.headers['Content-Security-Policy'])
 def test_hosted_requires_exact_origin(self):
  for origin in ('http://team.example','https://team.example/path','https://user:pass@team.example'):
   with patch.dict(os.environ,{'APP_MODE':'hosted','APP_PUBLIC_ORIGIN':origin}):
    with self.assertRaises(RuntimeError):create_app('test',self.root,['Admin'])

class AppBoundaryTests(unittest.TestCase):
 def test_digest_is_not_disclosed_to_restricted_users(self):
  with tempfile.TemporaryDirectory() as tmp,patch.dict(os.environ,{'APP_MODE':'local','MASKGATE_DATA':tmp,'MASKGATE_PREFIX':''}):
   m=load('mask_security',ROOT/'maskgate/app.py');c=m.app.test_client()
   c.post('/api/setup',json={'name':'owner','password':PASSWORD},headers={'X-Local-App':'1'})
   h={'X-Local-App':'1','X-CSRF-Token':c.get('/api/status').json['csrf']}
   c.post('/api/datasets',headers=h,data={'file':(io.BytesIO(b'id,balance\nknown,42\n'),'small.csv')})
   self.assertIn('digest',c.get('/api/datasets').json['datasets'][0])
   c.post('/api/users',headers=h,json={'name':'restricted','password':PASSWORD,'role':'Analyst'})
   other=m.app.test_client();other.post('/api/login',json={'name':'restricted','password':PASSWORD},headers={'X-Local-App':'1'})
   d=other.get('/api/datasets').json['datasets'][0];self.assertNotIn('digest',d)
   self.assertEqual(other.get('/api/datasets/'+d['id']+'/verify').status_code,403)
 def test_both_apps_work_under_hosted_prefixes(self):
  with tempfile.TemporaryDirectory() as tmp,patch.dict(os.environ,{'APP_MODE':'hosted','APP_PUBLIC_ORIGIN':'https://team.example','APP_DATA_ROOT':tmp,'APP_TRUST_PROXY_PROTO':'0'}):
   site=load('hosting_test',ROOT/'hosting.py');client=Client(site.application,Response)
   self.assertEqual(client.get('/',base_url='https://team.example').status_code,200)
   for app in ('maskgate','medsafe'):
    r=client.get('/'+app+'/',base_url='https://team.example');self.assertEqual(r.status_code,200)
    self.assertIn('content="/'+app+'"',r.text);self.assertIn('href="/'+app+'/assets/',r.text)
    with client.get('/'+app+'/assets/app.js',base_url='https://team.example') as asset:self.assertEqual(asset.status_code,200)
    with client.get('/'+app+'/common.js',base_url='https://team.example') as asset:self.assertEqual(asset.status_code,200)
    self.assertTrue(client.get('/'+app+'/api/status',base_url='https://team.example').json['setup_locked'])
    self.assertEqual(client.get('/'+app+'/assets/../../.runtime/secret.key',base_url='https://team.example').status_code,404)
    with connect(Path(tmp)/app/'workspace.sqlite') as db:db.execute('INSERT INTO users(name,password,role) VALUES (?,?,?)',('owner',generate_password_hash(PASSWORD),'Admin'))
    r=client.post('/'+app+'/api/login',base_url='https://team.example',json={'name':'owner','password':PASSWORD},headers={'X-Local-App':'1','Origin':'https://team.example'})
    self.assertEqual(r.status_code,200);self.assertIn('Path=/'+app+'/',r.headers['Set-Cookie'])
    self.assertEqual(client.get('/'+app+'/api/status',base_url='https://team.example').json['user']['name'],'owner')

if __name__=='__main__':unittest.main(verbosity=2)
