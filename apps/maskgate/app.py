"""MaskGate local workspace: imported tables, reviewed policies and enforced roles."""
import csv, hashlib, hmac, io, json, re, sys, time, uuid
from pathlib import Path
from contextlib import contextmanager
import sqlite3, duckdb
from flask import jsonify, request, render_template, g, Response, send_from_directory, abort
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common.core import create_app, connect, admin, csv_rows, safe_csv, now
ROOT=Path(__file__).resolve().parent
app=create_app('maskgate',ROOT,['Admin','Support','Analyst'])
DATA=app.config['DATA'];DB=app.config['DB'];ENGINES=('SQLite','DuckDB')
TAGS=['REVIEW','PII_HIGH','FINANCIAL_CONFIDENTIAL','PUBLIC']
with connect(DB) as db:
 db.execute('CREATE TABLE IF NOT EXISTS datasets (id TEXT PRIMARY KEY, name TEXT, columns_json TEXT, policy_json TEXT, rows INTEGER, digest TEXT, created TEXT, source TEXT)')

def suggestion(name,values):
 n=re.sub(r'[^a-z0-9]+','_',name.lower()).strip('_')
 words=set(n.split('_'))
 if words & {'balance','income','salary','cost','coverage','expenses','loan','housing','default'}:return 'FINANCIAL_CONFIDENTIAL','Financial field name'
 if words & {'email','phone','ssn','passport','address','birthdate','first','last','maiden','name','latitude','longitude'} or n in ('id','patient','drivers','zip','card_number'):
  return 'PII_HIGH','Identifier or personal field name'
 for v in values:
  if re.search(r'[^\s@]+@[^\s@]+\.[^\s@]+',v) or re.fullmatch(r'\d{3}-\d{2}-\d{4}',v) or re.fullmatch(r'\+?[\d ()-]{10,19}',v):return 'PII_HIGH','Identifier pattern in sampled values'
 return 'REVIEW','No confident classification. Review before allowing access.'

@contextmanager
def source_conn(dataset_id,engine,write=False):
 if engine not in ENGINES:raise ValueError('Choose SQLite or DuckDB.')
 if not re.fullmatch('[a-f0-9]{32}',dataset_id):abort(404)
 path=DATA/(dataset_id+('.sqlite' if engine=='SQLite' else '.duckdb'))
 c=(sqlite3.connect(str(path) if write else f'file:{path}?mode=ro',uri=not write) if engine=='SQLite' else duckdb.connect(str(path),read_only=not write))
 try:yield c
 finally:c.close()

def logical_hash(rows):
 h=hashlib.sha256()
 for row in rows:h.update(json.dumps(list(row),ensure_ascii=False,separators=(',',':')).encode()+b'\n')
 return h.hexdigest()

def dataset(ident):
 with connect(DB) as db:r=db.execute('SELECT * FROM datasets WHERE id=?',(ident,)).fetchone()
 if not r:abort(404)
 d=dict(r);d['columns']=json.loads(d.pop('columns_json'));d['policy']=json.loads(d.pop('policy_json'));return d

def import_data(raw,name,source):
 cols,rows=csv_rows(raw);ident=uuid.uuid4().hex
 policy=[dict(field=c,tag=suggestion(c,[r[i] for r in rows[:2000]])[0],reason=suggestion(c,[r[i] for r in rows[:2000]])[1],approved=False) for i,c in enumerate(cols)]
 try:
  for engine in ENGINES:
   with source_conn(ident,engine,True) as db:
    db.execute('CREATE TABLE records (row_id INTEGER PRIMARY KEY,'+','.join(f'f{i} TEXT' for i in range(len(cols)))+')')
    db.execute('BEGIN TRANSACTION')
    placeholder='('+','.join('?' for _ in range(len(cols)+1))+')'
    if engine=='SQLite':db.executemany('INSERT INTO records VALUES '+placeholder,((i,*row) for i,row in enumerate(rows)))
    else:
     for start in range(0,len(rows),500):
      batch=rows[start:start+500]
      values=[v for i,row in enumerate(batch,start) for v in (i,*row)]
      db.execute('INSERT INTO records VALUES '+','.join([placeholder]*len(batch)),values)
    db.commit()
  with connect(DB) as db:db.execute('INSERT INTO datasets VALUES (?,?,?,?,?,?,?,?)',(ident,name[:100],json.dumps(cols),json.dumps(policy),len(rows),logical_hash(rows),now(),source[:500]))
 except Exception:
  for suffix in ('.sqlite','.duckdb'): (DATA/(ident+suffix)).unlink(missing_ok=True)
  raise
 return ident

def protect(value,policy,role):
 if role=='Admin':return value
 if not policy['approved'] or policy['tag']=='REVIEW':return '[PENDING REVIEW]'
 if policy['tag']=='PUBLIC':return value
 if value=='':return ''
 if policy['tag']=='FINANCIAL_CONFIDENTIAL':return '[REDACTED]'
 if role=='Analyst':return 'hash:'+hmac.new(app.secret_key,str(value).encode(),hashlib.sha256).hexdigest()[:20]
 # Avoid leaking a full short identifier or domain.
 return str(value)[:1]+'•••' if len(str(value))>1 else '•••'

def query_args(d):
 allowed={'engine','offset','limit','field','value','preview'}
 if set(request.args)-allowed:raise ValueError('Unsupported query option. Raw SQL and supplied roles are not accepted.')
 engine=request.args.get('engine','SQLite');role=g.user['role']
 preview=request.args.get('preview')
 if preview:
  if role!='Admin':abort(403,description='Only administrators may preview another role.')
  if preview not in ('Support','Analyst','Admin'):raise ValueError('Invalid preview role.')
  role=preview
 try:offset=int(request.args.get('offset',0));limit=int(request.args.get('limit',50))
 except ValueError:raise ValueError('Invalid page number.')
 if offset<0 or offset>d['rows'] or not 1<=limit<=100:raise ValueError('Page size must be 1–100.')
 where='';args=[]
 field=request.args.get('field','');value=request.args.get('value','')
 if field:
  if field not in d['columns']:raise ValueError('Unknown filter field.')
  i=d['columns'].index(field);p=d['policy'][i]
  if role!='Admin' and not(p['approved'] and p['tag']=='PUBLIC'):abort(403,description='Filtering protected fields is blocked to prevent inference.')
  if len(value)>4000:raise ValueError('Filter is too long.')
  where=f' WHERE f{i} = ?';args=[value]
 return engine,role,offset,limit,where,args

def read_rows(d,engine,where,args,offset=0,limit=None):
 fields=','.join(f'f{i}' for i in range(len(d['columns'])))
 with source_conn(d['id'],engine) as db:
  total=db.execute('SELECT COUNT(*) FROM records'+where,args).fetchone()[0]
  sql='SELECT '+fields+' FROM records'+where+' ORDER BY row_id'
  values=list(args)
  if limit is not None:sql+=' LIMIT ? OFFSET ?';values += [limit,offset]
  rows=db.execute(sql,values).fetchall()
 return total,rows

@app.get('/')
def index():return render_template('index.html')
@app.get('/assets/<path:name>')
def assets(name):return send_from_directory(ROOT/'templates',name)
@app.get('/common.js')
def common_js():return send_from_directory(ROOT.parent/'common','ui.js')
@app.get('/api/datasets')
def datasets():
 with connect(DB) as db:ids=[r[0] for r in db.execute('SELECT id FROM datasets ORDER BY created DESC')]
 items=[dataset(x) for x in ids]
 if g.user['role']!='Admin':
  allowed={'id','name','columns','policy','rows','created','source'}
  items=[{k:v for k,v in d.items() if k in allowed} for d in items]
 return jsonify(datasets=items)
@app.post('/api/datasets')
@admin
def upload():
 file=request.files.get('file')
 if not file:raise ValueError('Choose a CSV file.')
 ident=import_data(file.read(),file.filename or 'Imported CSV','Local CSV upload')
 app.audit('dataset_imported',ident);return jsonify(dataset=dataset(ident)),201
@app.post('/api/samples/<name>')
@admin
def sample(name):
 samples={'bank':('bank-full.csv','UCI Bank Marketing • Moro, Rita & Cortez (2014) • CC BY 4.0'), 'synthea':('patients.csv','MITRE Synthea • synthetic patient demographics • April 2020 sample')}
 if name not in samples:abort(404)
 file,source=samples[name];path=ROOT.parent/'datasets'/file
 if not path.exists():return jsonify(error='Sample is not downloaded. Run fetch_datasets.py.'),409
 ident=import_data(path.read_bytes(),file,source);app.audit('sample_imported',ident);return jsonify(dataset=dataset(ident)),201
@app.put('/api/datasets/<ident>/policy')
@admin
def policy(ident):
 d=dataset(ident);body=request.get_json() or {};items=body.get('fields')
 if not isinstance(items,list) or len(items)!=len(d['columns']):raise ValueError('Submit one policy for every column.')
 updated=[]
 for i,p in enumerate(items):
  if not isinstance(p,dict) or p.get('field')!=d['columns'][i] or p.get('tag') not in TAGS:raise ValueError('Invalid field policy.')
  updated.append(dict(field=p['field'],tag=p['tag'],approved=p['tag']!='REVIEW',reason='Reviewed by '+g.user['name']))
 with connect(DB) as db:db.execute('UPDATE datasets SET policy_json=? WHERE id=?',(json.dumps(updated),ident))
 app.audit('policy_saved',ident);return jsonify(dataset=dataset(ident))
@app.get('/api/datasets/<ident>/rows')
def rows(ident):
 d=dataset(ident);engine,role,offset,limit,where,args=query_args(d);start=time.perf_counter()
 total,raw=read_rows(d,engine,where,args,offset,limit)
 out=[[protect(v,p,role) for v,p in zip(row,d['policy'])] for row in raw]
 app.audit('query',json.dumps({'dataset':ident,'engine':engine,'role':role,'rows':len(out)}))
 return jsonify(columns=d['columns'],rows=out,total=total,offset=offset,role=role,engine=engine,elapsed_ms=round((time.perf_counter()-start)*1000,2))
@app.get('/api/datasets/<ident>/export')
def export(ident):
 d=dataset(ident);engine,role,_,_,where,args=query_args(d);_,raw=read_rows(d,engine,where,args)
 out=io.StringIO();writer=csv.writer(out);writer.writerow([safe_csv(x) for x in d['columns']])
 writer.writerows([[safe_csv(protect(v,p,role)) for v,p in zip(row,d['policy'])] for row in raw])
 app.audit('csv_export',json.dumps({'dataset':ident,'role':role,'rows':len(raw)}))
 return Response(out.getvalue(),mimetype='text/csv',headers={'Content-Disposition':'attachment; filename="maskgate-export.csv"'})
@app.get('/api/datasets/<ident>/verify')
@admin
def verify(ident):
 d=dataset(ident);results=[]
 for engine in ENGINES:
  start=time.perf_counter();_,raw=read_rows(d,engine,'',[]);digest=logical_hash(raw)
  results.append(dict(engine=engine,rows=len(raw),unchanged=digest==d['digest'],sha256=digest,read_ms=round((time.perf_counter()-start)*1000,2)))
 app.audit('integrity_check',ident);return jsonify(results=results,import_sha256=d['digest'])
if __name__=='__main__':app.run(host='127.0.0.1',port=8775,threaded=False)
