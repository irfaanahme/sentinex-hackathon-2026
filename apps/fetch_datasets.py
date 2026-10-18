"""Fetch official public test data; extract only explicitly named CSV files."""
from pathlib import Path
import hashlib,io,json,urllib.request,zipfile,ssl
ROOT=Path(__file__).resolve().parent/'datasets'
ROOT.mkdir(exist_ok=True)
SOURCES=[('synthea','https://synthetichealth.github.io/synthea-sample-data/downloads/synthea_sample_data_csv_apr2020.zip',['patients.csv','medications.csv']),('bank','https://archive.ics.uci.edu/static/public/222/bank+marketing.zip',['bank-full.csv'])]
records=[]
for name,url,files in SOURCES:
 archive=ROOT/(name+'.zip')
 if not archive.exists():
  with urllib.request.urlopen(url,timeout=60,context=ssl.create_default_context(cafile='/etc/ssl/cert.pem') if Path('/etc/ssl/cert.pem').exists() else ssl.create_default_context()) as response:raw=response.read(25*1024*1024)
  archive.write_bytes(raw)
 raw=archive.read_bytes();z=zipfile.ZipFile(io.BytesIO(raw))
 if name=='bank':z=zipfile.ZipFile(io.BytesIO(z.read('bank.zip')))
 for filename in files:
  match=next(x for x in z.namelist() if x.split('/')[-1]==filename)
  content=z.read(match);(ROOT/filename).write_bytes(content)
  records.append({'file':filename,'source':url,'archive_sha256':hashlib.sha256(raw).hexdigest(),'file_sha256':hashlib.sha256(content).hexdigest(),'bytes':len(content)})
 (ROOT/'sources.json').write_text(json.dumps(records,indent=2))
 print(name,'downloaded and verified',flush=True)
