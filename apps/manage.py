"""Private console account setup/recovery. Never accepts passwords as arguments."""
import argparse,getpass,importlib.util,os,re
from pathlib import Path
from werkzeug.security import generate_password_hash
from common.core import connect
ROOT=Path(__file__).resolve().parent

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['init','reset-password'])
    parser.add_argument('app',choices=['medsafe','maskgate','both'])
    args=parser.parse_args()
    username=input('Account username: ').strip()
    if not re.fullmatch(r'[a-zA-Z0-9_.-]{3,40}',username):raise SystemExit('Invalid username.')
    password=getpass.getpass('Password (12–256 characters): ')
    if not 12<=len(password)<=256:raise SystemExit('Use 12–256 characters.')
    if getpass.getpass('Repeat password: ')!=password:raise SystemExit('Passwords do not match.')
    hashed=generate_password_hash(password)
    for name in ('medsafe','maskgate') if args.app=='both' else (args.app,):
        if os.environ.get('APP_DATA_ROOT'):os.environ[name.upper()+'_DATA']=str(Path(os.environ['APP_DATA_ROOT'])/name)
        spec=importlib.util.spec_from_file_location('manage_'+name,ROOT/name/'app.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        with connect(module.DB) as db:
            db.execute('BEGIN IMMEDIATE')
            if args.action=='init':
                if db.execute('SELECT COUNT(*) FROM users').fetchone()[0]:raise SystemExit(name+' already has an owner; no changes made to it.')
                db.execute('INSERT INTO users(name,password,role) VALUES (?,?,?)',(username,hashed,'Admin'))
            else:
                if not db.execute('UPDATE users SET password=? WHERE name=?',(hashed,username)).rowcount:raise SystemExit(name+': account not found.')
                db.execute('DELETE FROM sessions WHERE user=?',(username,))
        print(name+': account saved; password not displayed.')

if __name__=='__main__':main()
