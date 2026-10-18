import importlib.util,io,json,os,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
TEMP=tempfile.TemporaryDirectory()
os.environ['MASKGATE_DATA']=str(Path(TEMP.name)/'maskgate');os.environ['MEDSAFE_DATA']=str(Path(TEMP.name)/'medsafe')
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);mod.app.config.update(TESTING=True);return mod
mask=module('maskgate_test',ROOT/'maskgate/app.py');med=module('medsafe_test',ROOT/'medsafe/app.py')
from common.core import connect

def init(client):
 r=client.post('/api/setup',json={'name':'administrator','password':'Long local test password 2026'},headers={'X-Local-App':'1'})
 assert r.status_code==200,r.json
 return {'X-Local-App':'1','X-CSRF-Token':client.get('/api/status').json['csrf']}

class MaskTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=mask.app.test_client();cls.h=init(cls.c)
  raw=b'name,email,balance,town,unclassified\nAda,ada@example.test,250,Port,secret\nBea,bea@example.test,900,Hill,hidden\n'
  r=cls.c.post('/api/datasets',data={'file':(io.BytesIO(raw),'example.csv')},headers=cls.h);assert r.status_code==201,r.json
  cls.d=r.json['dataset'];cls.id=cls.d['id']
 def test_01_unapproved_closed_both_engines(self):
  for engine in mask.ENGINES:
   r=self.c.get(f'/api/datasets/{self.id}/rows?engine={engine}&preview=Support')
   self.assertTrue(all(x=='[PENDING REVIEW]' for row in r.json['rows'] for x in row))
 def test_02_policy_role_query_export_integrity(self):
  tags=['PII_HIGH','PII_HIGH','FINANCIAL_CONFIDENTIAL','PUBLIC','REVIEW']
  fields=[dict(field=f,tag=t) for f,t in zip(self.d['columns'],tags)]
  self.assertEqual(self.c.put(f'/api/datasets/{self.id}/policy',json={'fields':fields},headers=self.h).status_code,200)
  for engine in mask.ENGINES:
   r=self.c.get(f'/api/datasets/{self.id}/rows?engine={engine}&preview=Support').json
   self.assertEqual(r['rows'][0],['A•••','a•••','[REDACTED]','Port','[PENDING REVIEW]'])
   self.assertNotIn('ada@example.test',self.c.get(f'/api/datasets/{self.id}/export?engine={engine}&preview=Analyst').text)
  self.assertTrue(all(x['unchanged'] for x in self.c.get(f'/api/datasets/{self.id}/verify').json['results']))
 def test_03_session_authority(self):
  r=self.c.post('/api/users',json={'name':'support','password':'Support password long 2026','role':'Support'},headers=self.h);self.assertEqual(r.status_code,201)
  client=mask.app.test_client();self.assertEqual(client.get('/api/datasets').status_code,401)
  client.post('/api/login',json={'name':'support','password':'Support password long 2026'},headers={'X-Local-App':'1'})
  h={'X-Local-App':'1','X-CSRF-Token':client.get('/api/status').json['csrf']}
  self.assertEqual(client.get(f'/api/datasets/{self.id}/rows?preview=Admin').status_code,403)
  self.assertEqual(client.get(f'/api/datasets/{self.id}/rows?field=email&value=ada@example.test').status_code,403)
  self.assertEqual(client.put(f'/api/datasets/{self.id}/policy',json={'fields':[]},headers=h).status_code,403)
  self.assertEqual(client.post('/api/samples/bank',headers=h).status_code,403)
 def test_04_csv_validation_and_csrf(self):
  for raw in [b'a,a\n1,2\n',b'a,b\n1,2,3\n',b'']:
   self.assertEqual(self.c.post('/api/datasets',data={'file':(io.BytesIO(raw),'bad.csv')},headers=self.h).status_code,400)
  self.assertEqual(self.c.post('/api/samples/bank').status_code,403)
  self.assertEqual(self.c.post('/api/samples/bank',headers={**self.h,'Origin':'https://untrusted.test'}).status_code,403)
  self.assertEqual(self.c.get(f'/api/datasets/{self.id}/rows?sql=DELETE').status_code,400)
 def test_05_persistent_state(self):
  reopened=module('maskgate_reopened',ROOT/'maskgate/app.py')
  self.assertEqual(reopened.app.secret_key,mask.app.secret_key)
  with connect(reopened.DB) as db:self.assertEqual(db.execute('SELECT rows FROM datasets WHERE id=?',(self.id,)).fetchone()[0],2)
 def test_06_formula_export(self):
  r=self.c.post('/api/datasets',data={'file':(io.BytesIO(b'value\n=1+1\n'),'formula.csv')},headers=self.h)
  ident=r.json['dataset']['id'];self.assertIn("'=1+1",self.c.get(f'/api/datasets/{ident}/export').text)
 def test_07_public_dataset_scale(self):
  r=self.c.post('/api/samples/bank',headers=self.h);self.assertEqual(r.status_code,201,r.json)
  d=r.json['dataset'];self.assertEqual(d['rows'],45211)
  result=self.c.get(f"/api/datasets/{d['id']}/verify").json
  self.assertTrue(all(x['unchanged'] and x['rows']==45211 for x in result['results']))

class MedTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=med.app.test_client();cls.h=init(cls.c)
  p=b'Id,FIRST,LAST,BIRTHDATE\np1,Test,Person,1980-01-01\n'
  m=b'PATIENT,CODE,DESCRIPTION,START,STOP\np1,123,Medicine A,2020-01-01,\np1,123,Medicine A,2020-02-01,\np1,456,Medicine B,2020-01-01,2020-03-01\n'
  r=cls.c.post('/api/import',data={'patients':(io.BytesIO(p),'patients.csv'),'medications':(io.BytesIO(m),'medications.csv')},headers=cls.h);assert r.status_code==201,r.json
  cls.ident=cls.c.get('/api/patients').json['patients'][0]['id']
 def review(self,day='2020-04-01'):
  return self.c.post('/api/reconcile',json={'patient':self.ident,'as_of':day},headers=self.h)
 def test_01_dated_overlap_and_explicit_coverage(self):
  r=self.review().json;self.assertEqual(len(r['active']),2);self.assertEqual(len(r['findings']),1)
  self.assertEqual(r['coverage']['drug_interactions'],'not available')
  self.assertEqual(r['coverage']['ingredient_overlap'],'incomplete')
  self.assertEqual(len(self.review('2020-01-10').json['active']),2)
  self.assertEqual(self.review('1900-01-01').status_code,400)
 def test_02_saved_report(self):
  r=self.c.post('/api/reviews',json={'patient':self.ident,'as_of':'2020-04-01','note':'Confirm overlapping entries with source.'},headers=self.h)
  self.assertEqual(r.status_code,201)
  report=self.c.get('/api/reviews/'+r.json['id']+'/export').text
  self.assertIn('Confirm overlapping entries with source.',report);self.assertIn('not available',self.review().json['coverage']['drug_interactions'])
  self.assertIn('no validated clinical rule pack',report)
 def test_03_network_failure_visible(self):
  with patch.object(med,'fetch_json',side_effect=OSError('offline')):
   r=self.c.post('/api/references/refresh',json={'patient':self.ident,'as_of':'2020-04-01'},headers=self.h)
  self.assertEqual(r.json['failed'],['123']);self.assertEqual(r.json['updated'],0)
 def test_04_unknown_patient_rejected_atomically(self):
  p=b'Id,FIRST,LAST,BIRTHDATE\np2,Other,Person,1990-01-01\n';m=b'PATIENT,CODE,DESCRIPTION,START,STOP\nunknown,123,X,2020-01-01,\n'
  before=self.c.get('/api/patients').json['total']
  r=self.c.post('/api/import',data={'patients':(io.BytesIO(p),'patients.csv'),'medications':(io.BytesIO(m),'meds.csv')},headers=self.h)
  self.assertEqual(r.status_code,400);self.assertEqual(self.c.get('/api/patients').json['total'],before)
 def test_05_synthea_import(self):
  r=self.c.post('/api/sample',headers=self.h);self.assertEqual(r.status_code,201,r.json)
  self.assertEqual(r.json['flagged'],5);self.assertGreaterEqual(r.json['patients'],1000);self.assertGreater(r.json['medications'],20000)
  self.assertEqual(len(self.c.get('/api/patients?offset=25').json['patients']),25)
 def test_06a_reference_ingredient_overlap_and_staleness(self):
  from datetime import datetime,timezone,timedelta
  with connect(med.DB) as db:
   for code in ('123','456'):
    payload={'code':code,'name':'Test reference','status':'active','ingredients':[{'code':'42','name':'Test ingredient'}],'source':'https://rxnav.nlm.nih.gov/'}
    db.execute('INSERT OR REPLACE INTO references_cache VALUES (?,?,?)',(code,json.dumps(payload),datetime.now(timezone.utc).isoformat()))
  result=self.review('2020-02-10').json
  self.assertTrue(any(f['kind']=='Shared ingredient to reconcile' for f in result['findings']))
  with connect(med.DB) as db:db.execute('UPDATE references_cache SET updated=?',((datetime.now(timezone.utc)-timedelta(days=31)).isoformat(),))
  result=self.review('2020-02-10').json
  self.assertEqual(result['coverage']['ingredient_overlap'],'incomplete')
  self.assertFalse(any(f['kind']=='Shared ingredient to reconcile' for f in result['findings']))
 def test_06b_invalid_date_preserved_and_excluded(self):
  p=b'Id,FIRST,LAST,BIRTHDATE\npbad,Test,Bad,1980-01-01\n'
  m=b'PATIENT,CODE,DESCRIPTION,START,STOP\npbad,123,Medicine,2020-03-01,2020-02-01\n'
  result=med.import_patients(p,m,'test fixture');ident=result['id']+':pbad'
  with med.app.test_request_context():result=med.reconcile(ident,'2020-04-01')
  self.assertEqual(result['history_count'],1);self.assertEqual(result['active'],[])
  self.assertTrue(any('invalid date order' in x for x in result['limitations']))
 def test_06c_json_shape_validation(self):
  self.assertEqual(self.c.post('/api/reconcile',json=['bad'],headers=self.h).status_code,400)
 def test_06_protected_history(self):
  self.assertEqual(med.app.test_client().get('/api/patients').status_code,401)
  self.assertEqual(self.c.post('/api/reconcile',json={'patient':self.ident,'as_of':'2020-04-01'}).status_code,403)

if __name__=='__main__':unittest.main(verbosity=2)
