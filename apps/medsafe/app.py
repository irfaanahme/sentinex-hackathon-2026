"""Local medication reconciliation workspace with traceable source records."""
import io,json,re,sys,uuid,urllib.request,urllib.parse,ssl,time
from datetime import date,datetime,timezone,timedelta
from pathlib import Path
from flask import jsonify,request,render_template,send_from_directory,g,Response,abort
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common.core import create_app,connect,admin,csv_rows,now
ROOT=Path(__file__).resolve().parent
app=create_app('medsafe',ROOT,['Admin','Reviewer']);DB=app.config['DB']
with connect(DB) as db:
 db.executescript('''CREATE TABLE IF NOT EXISTS batches(id TEXT PRIMARY KEY,source TEXT,created TEXT,patients INTEGER,medications INTEGER);
 CREATE TABLE IF NOT EXISTS patients(id TEXT PRIMARY KEY,batch TEXT,source_id TEXT,first TEXT,last TEXT,birth TEXT,death TEXT);
 CREATE TABLE IF NOT EXISTS medicines(id INTEGER PRIMARY KEY,patient TEXT,code TEXT,name TEXT,start TEXT,stop TEXT,issue TEXT DEFAULT '');
 CREATE INDEX IF NOT EXISTS med_patient ON medicines(patient);
 CREATE TABLE IF NOT EXISTS references_cache(code TEXT PRIMARY KEY,payload TEXT,updated TEXT);
 CREATE TABLE IF NOT EXISTS reviews(id TEXT PRIMARY KEY,patient TEXT,at TEXT,author TEXT,payload TEXT,note TEXT);''')

 if 'issue' not in [r[1] for r in db.execute('PRAGMA table_info(medicines)')]:db.execute("ALTER TABLE medicines ADD COLUMN issue TEXT DEFAULT ''")

def parsed_date(value,required=False):
 if not value:
  if required:raise ValueError('A date is required.')
  return ''
 try:return date.fromisoformat(value[:10]).isoformat()
 except (ValueError,TypeError):raise ValueError('Use a valid YYYY-MM-DD date.')

def records(raw,required):
 columns,rows=csv_rows(raw)
 if not set(required)<=set(columns):raise ValueError('Required columns: '+', '.join(required))
 return [dict(zip(columns,row)) for row in rows]

def import_patients(praw,mraw,source):
 patients=records(praw,['Id','FIRST','LAST','BIRTHDATE']);meds=records(mraw,['PATIENT','CODE','DESCRIPTION','START','STOP'])
 batch=uuid.uuid4().hex;ids={};prows=[];mrows=[]
 for p in patients:
  source_id=p['Id']
  if not source_id or source_id in ids:raise ValueError('Patient IDs must be nonempty and unique.')
  ident=batch+':'+source_id;ids[source_id]=ident
  birth=parsed_date(p['BIRTHDATE'],True);death=parsed_date(p.get('DEATHDATE',''))
  if death and death<birth:raise ValueError('Death date cannot precede birth date.')
  prows.append((ident,batch,source_id,p['FIRST'],p['LAST'],birth,death))
 for m in meds:
  if m['PATIENT'] not in ids:raise ValueError('Every medication must refer to a patient in the patient CSV.')
  if not re.fullmatch(r'\d{1,12}',m['CODE']):raise ValueError('Medication CODE must be a numeric RxNorm identifier.')
  start=parsed_date(m['START'],True);stop=parsed_date(m['STOP'])
  issue='Stop date precedes start date; excluded from active review.' if stop and stop<start else ''
  if not m['DESCRIPTION'].strip():raise ValueError('Medicine descriptions cannot be empty.')
  mrows.append((ids[m['PATIENT']],m['CODE'],m['DESCRIPTION'],start,stop,issue))
 with connect(DB) as db:
  db.execute('INSERT INTO batches VALUES (?,?,?,?,?)',(batch,source,now(),len(prows),len(mrows)))
  db.executemany('INSERT INTO patients VALUES (?,?,?,?,?,?,?)',prows)
  db.executemany('INSERT INTO medicines(patient,code,name,start,stop,issue) VALUES (?,?,?,?,?,?)',mrows)
 return dict(id=batch,patients=len(prows),medications=len(mrows),flagged=sum(bool(x[-1]) for x in mrows))

def patient(ident):
 with connect(DB) as db:p=db.execute('SELECT p.*,b.source FROM patients p JOIN batches b ON b.id=p.batch WHERE p.id=?',(ident,)).fetchone()
 if not p:abort(404)
 return dict(p)

def reference(code):
 with connect(DB) as db:r=db.execute('SELECT payload,updated FROM references_cache WHERE code=?',(code,)).fetchone()
 if not r:return None
 payload=json.loads(r['payload']);payload['retrieved_at']=r['updated'];return payload

def fetch_json(url):
 # Official public terminology only. No patient identifiers or history are sent.
 ctx=ssl.create_default_context(cafile='/etc/ssl/cert.pem') if Path('/etc/ssl/cert.pem').exists() else ssl.create_default_context()
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'MedSafe-local/0.1'}),timeout=4,context=ctx) as r:return json.loads(r.read(2*1024*1024))

def refresh_reference(code):
 base='https://rxnav.nlm.nih.gov/REST/rxcui/'+code
 prop=fetch_json(base+'/properties.json').get('properties')
 related=fetch_json(base+'/related.json?tty=IN').get('relatedGroup',{}) if prop else {}
 ingredients=[dict(code=x['rxcui'],name=x['name']) for group in related.get('conceptGroup',[]) for x in group.get('conceptProperties',[])]
 payload=dict(code=code,name=prop.get('name') if prop else None,ingredients=ingredients,source=base+'/properties.json',ingredient_source=base+'/related.json?tty=IN',status='active' if prop else 'unresolved')
 with connect(DB) as db:db.execute('INSERT OR REPLACE INTO references_cache VALUES (?,?,?)',(code,json.dumps(payload),now()))
 return payload

def reconcile(ident,asof):
 p=patient(ident)
 if asof<p['birth']:raise ValueError('Review date is before this patient’s birth.')
 with connect(DB) as db:rows=[dict(r) for r in db.execute('SELECT * FROM medicines WHERE patient=? ORDER BY start DESC,id',(ident,))]
 active=[m for m in rows if not m['issue'] and m['start']<=asof and(not m['stop'] or m['stop']>asof)]
 groups={};unresolved=[];stale=[];ingredient_groups={}
 for m in active:
  groups.setdefault(m['code'],[]).append(m)
  ref=reference(m['code']);m['reference']=ref
  if not ref or ref['status']!='active' or not ref['ingredients']:unresolved.append(m['code'])
  elif datetime.fromisoformat(ref['retrieved_at'])<datetime.now(timezone.utc)-timedelta(days=30):stale.append(m['code'])
  else:
   for item in ref['ingredients']:ingredient_groups.setdefault(item['code'],dict(name=item['name'],meds=[]))['meds'].append(m)
 findings=[]
 for code,items in groups.items():
  if len(items)>1:findings.append(dict(kind='Repeated medication record',medicines=[m['name'] for m in items],detail='Multiple source records for the same RxNorm code overlap on the review date. Reconcile the entries; this alone does not prove duplicate dosing.',source='Imported medication start/stop dates and RxNorm code '+code))
 for code,group in ingredient_groups.items():
  if len({m['code'] for m in group['meds']})>1:findings.append(dict(kind='Shared ingredient to reconcile',medicines=sorted(set(m['name'] for m in group['meds'])),detail='These active records share '+group['name']+'. Check whether the overlap is intentional. No dose or treatment change is recommended.',source='https://rxnav.nlm.nih.gov/REST/rxcui/'+code+'/properties.json'))
 birth=date.fromisoformat(p['birth']);review_date=date.fromisoformat(asof)
 age=review_date.year-birth.year-((review_date.month,review_date.day)<(birth.month,birth.day))
 limits=['Interaction, renal-dose, allergy and pregnancy checks are not available: no validated clinical rule pack is installed.','A source record does not confirm that a patient is currently taking a medicine. Confirm the list during review.']
 if any(m['issue'] for m in rows):limits.insert(0,str(sum(bool(m['issue']) for m in rows))+' source records have invalid date order and are excluded from active review. Inspect full history.')
 if p['death'] and p['death']<=asof:limits.insert(0,'The source records this patient as deceased on or before the selected review date.')
 if unresolved:limits.append(str(len(set(unresolved)))+' active medicine codes have no complete current ingredient reference. Ingredient overlap review is incomplete.')
 if stale:limits.append(str(len(set(stale)))+' medicine references are older than 30 days. Refresh before ingredient review.')
 return dict(patient=p,as_of=asof,age=age,active=active,history_count=len(rows),findings=findings,limitations=limits,
  coverage={'record_overlap':'checked','ingredient_overlap':'incomplete' if unresolved or stale else 'checked','drug_interactions':'not available','renal_dose':'not available','allergies':'not available','pregnancy':'not available'})

@app.get('/')
def index():return render_template('index.html')
@app.get('/assets/<path:name>')
def assets(name):return send_from_directory(ROOT/'templates',name)
@app.get('/common.js')
def common_js():return send_from_directory(ROOT.parent/'common','ui.js')
@app.get('/api/patients')
def patients():
 q=request.args.get('q','')[:100];offset=max(0,int(request.args.get('offset',0)))
 with connect(DB) as db:
  total=db.execute('SELECT COUNT(*) FROM patients WHERE first LIKE ? OR last LIKE ? OR source_id LIKE ?',('%'+q+'%',)*3).fetchone()[0]
  rows=[dict(r) for r in db.execute('SELECT p.*,(SELECT COUNT(*) FROM medicines m WHERE m.patient=p.id) AS medication_count FROM patients p WHERE first LIKE ? OR last LIKE ? OR source_id LIKE ? ORDER BY last,first,id LIMIT 25 OFFSET ?',(*('%'+q+'%',)*3,offset))]
  batches=[dict(r) for r in db.execute('SELECT * FROM batches ORDER BY created DESC')]
 return jsonify(patients=rows,total=total,batches=batches,offset=offset)
@app.post('/api/import')
@admin
def upload():
 p=request.files.get('patients');m=request.files.get('medications')
 if not p or not m:raise ValueError('Choose patients.csv and medications.csv together.')
 result=import_patients(p.read(),m.read(),'Local Synthea-format CSV import')
 app.audit('patient_files_imported',json.dumps(result));return jsonify(result),201
@app.post('/api/sample')
@admin
def sample():
 directory=ROOT.parent/'datasets'
 if not (directory/'medications.csv').exists():return jsonify(error='Sample files are missing. Run fetch_datasets.py.'),409
 result=import_patients((directory/'patients.csv').read_bytes(),(directory/'medications.csv').read_bytes(),'MITRE Synthea April 2020 sample • synthetic patients • https://synthetichealth.github.io/downloads.html')
 app.audit('public_sample_imported',json.dumps(result));return jsonify(result),201
@app.get('/api/patients/<path:ident>/history')
def history(ident):
 p=patient(ident)
 with connect(DB) as db:rows=[dict(r) for r in db.execute('SELECT * FROM medicines WHERE patient=? ORDER BY start DESC,id',(ident,))]
 return jsonify(patient=p,medications=rows)
@app.post('/api/reconcile')
def review():
 b=request.get_json() or {};result=reconcile(b.get('patient',''),parsed_date(b.get('as_of'),True))
 app.audit('medication_review',b.get('patient',''));return jsonify(result)
@app.post('/api/references/refresh')
def refresh():
 b=request.get_json() or {};r=reconcile(b.get('patient',''),parsed_date(b.get('as_of'),True));codes=sorted(set(m['code'] for m in r['active']))
 if not app.rate_limit('references',g.user['name'],6,60):return jsonify(error='Please wait one minute before refreshing more references.'),429
 # Work in short batches; do not repeatedly fetch recent successful references.
 pending=[]
 for code in codes:
  ref=reference(code)
  if not ref or ref.get('status')!='active' or not ref.get('ingredients') or datetime.fromisoformat(ref['retrieved_at'])<datetime.now(timezone.utc)-timedelta(days=30):pending.append(code)
 updated=[];errors=[];started=time.monotonic();processed=0
 for code in pending[:3]:
  if time.monotonic()-started>16:break
  processed+=1
  try:updated.append(refresh_reference(code))
  except (OSError,ValueError,KeyError):errors.append(code)
 app.audit('reference_refresh',json.dumps({'updated':len(updated),'failed':len(errors)}))
 return jsonify(updated=len(updated),failed=errors,remaining=max(0,len(pending)-processed),cached=len(codes)-len(pending))
@app.post('/api/reviews')
def save_review():
 b=request.get_json() or {};note=b.get('note','')
 if not isinstance(note,str) or len(note)>10000:raise ValueError('Notes are limited to 10,000 characters.')
 result=reconcile(b.get('patient',''),parsed_date(b.get('as_of'),True));ident=uuid.uuid4().hex
 with connect(DB) as db:db.execute('INSERT INTO reviews VALUES (?,?,?,?,?,?)',(ident,result['patient']['id'],now(),g.user['name'],json.dumps(result),note))
 app.audit('review_saved',ident);return jsonify(id=ident),201
@app.get('/api/reviews')
def saved_reviews():
 with connect(DB) as db:rows=[dict(r) for r in db.execute('SELECT r.id,r.at,r.author,r.note,p.first,p.last FROM reviews r JOIN patients p ON r.patient=p.id ORDER BY r.at DESC LIMIT 100')]
 return jsonify(reviews=rows)
@app.get('/api/reviews/<ident>/export')
def export(ident):
 with connect(DB) as db:r=db.execute('SELECT * FROM reviews WHERE id=?',(ident,)).fetchone()
 if not r:abort(404)
 r=dict(r);result=json.loads(r.pop('payload'));p=result['patient']
 lines=['MedSafe • Medication reconciliation report',f"Patient: {p['first']} {p['last']} ({p['source_id']})",f"Review date: {result['as_of']} | Saved by: {r['author']} at {r['at']}",'Source: '+p['source'],'','ACTIVE SOURCE RECORDS']
 for m in result['active']:lines.append(f"- {m['name']} | RxNorm {m['code']} | {m['start']} to {m['stop'] or 'not recorded'}")
 lines+=['','RECONCILIATION FINDINGS']
 for f in result['findings']:lines += [f['kind']+': '+f['detail'],'Medicines: '+'; '.join(f['medicines']),'Evidence: '+f['source']]
 if not result['findings']:lines.append('No overlapping entries found under available checks. This is not a safety clearance.')
 lines+=['','COVERAGE & LIMITATIONS',*result['limitations'],'','REVIEWER NOTE',r['note']]
 app.audit('report_exported',ident)
 return Response('\n'.join(lines),mimetype='text/plain',headers={'Content-Disposition':'attachment; filename="medsafe-review.txt"'})
if __name__=='__main__':app.run(host='127.0.0.1',port=8776,threaded=False)
