"""Preload public datasets without creating user accounts or changing existing policies."""
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parent
for name in ('maskgate','medsafe'):
 spec=importlib.util.spec_from_file_location('prepare_'+name,ROOT/name/'app.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 with m.connect(m.DB) as db:count=db.execute('SELECT COUNT(*) FROM '+('datasets' if name=='maskgate' else 'batches')).fetchone()[0]
 if count:print(name,'existing data retained',flush=True);continue
 if name=='maskgate':
  for f,source in [('bank-full.csv','UCI Bank Marketing • Moro, Rita & Cortez (2014) • CC BY 4.0'),('patients.csv','MITRE Synthea • synthetic patient demographics • April 2020 sample')]:
   m.import_data((ROOT/'datasets'/f).read_bytes(),f,source);print(name,f,'loaded',flush=True)
 else:
  print(name,m.import_patients((ROOT/'datasets/patients.csv').read_bytes(),(ROOT/'datasets/medications.csv').read_bytes(),'MITRE Synthea April 2020 sample • synthetic patients • https://synthetichealth.github.io/downloads.html'),flush=True)
