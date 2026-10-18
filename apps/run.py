"""Launch one local app. Defaults to persistent user workspace; --qa isolates test data."""
import argparse,importlib.util,os
from pathlib import Path
root=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('app',choices=['maskgate','medsafe']);parser.add_argument('--qa',action='store_true');args=parser.parse_args()
port={'maskgate':8775,'medsafe':8776}[args.app]
if args.qa:
 os.environ[args.app.upper()+'_DATA']=str(root/'.qa'/args.app);port+=100
spec=importlib.util.spec_from_file_location('local_app',root/args.app/'app.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
print(f'Local {args.app}: http://127.0.0.1:{port}',flush=True)
m.app.run(host='127.0.0.1',port=port,threaded=False,debug=False)
