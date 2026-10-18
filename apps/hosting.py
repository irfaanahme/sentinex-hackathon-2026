"""One WSGI site, two independent team workspaces. No public bootstrap."""
import importlib.util,os
from pathlib import Path
from flask import Flask, Response
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.middleware.proxy_fix import ProxyFix
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parent

def load_app(name):
    os.environ[name.upper()+'_PREFIX']='/'+name
    store=Path(os.environ['APP_DATA_ROOT']).resolve()/name
    os.environ[name.upper()+'_DATA']=str(store)
    spec=importlib.util.spec_from_file_location('hosted_'+name,ROOT/name/'app.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module.app

def create_site():
    if not os.environ.get('APP_DATA_ROOT'):raise RuntimeError('Set APP_DATA_ROOT to a private persistent directory outside the uploaded source folder.')
    os.environ['APP_MODE']='hosted'
    apps={name:load_app(name) for name in ('medsafe','maskgate')}
    portal=Flask('sentinex_portal')
    portal.config['TRUSTED_HOSTS']=[urlsplit(os.environ['APP_PUBLIC_ORIGIN']).hostname]
    @portal.get('/')
    def home():
        return Response('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>SENTINEX · Team workspaces</title><style>body{font:17px/1.6 system-ui;max-width:760px;margin:10vh auto;padding:24px;background:#f8f7f4;color:#243044}h1{font-size:42px;letter-spacing:-1px}a{display:block;padding:25px;margin:20px 0;background:white;border:1px solid #ddd;border-radius:14px;color:inherit;text-decoration:none}a:hover,a:focus{border-color:#316578}strong{font-size:24px}small{display:block;color:#65717b}</style><h1>A workspace for each problem.</h1><p>Invited team members can sign in below. This test deployment uses public and synthetic sample data.</p><a href="/medsafe/"><strong>MedSafe</strong><small>Medication records, reconciliation and review notes.</small></a><a href="/maskgate/"><strong>MaskGate</strong><small>Field policies, role-based access and masked exports.</small></a><p>Each app has separate accounts. Members share that app’s workspace. Do not upload real patient or customer information to this test deployment.</p></html>''',mimetype='text/html')
    @portal.get('/health')
    def health():return {'status':'ok'}
    @portal.after_request
    def protect(response):
        response.headers.update({'Cache-Control':'no-store','Referrer-Policy':'no-referrer','X-Frame-Options':'DENY','X-Content-Type-Options':'nosniff','Strict-Transport-Security':'max-age=31536000','Content-Security-Policy':"default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'"})
        return response
    application=DispatcherMiddleware(portal,{'/'+name:app for name,app in apps.items()})
    if os.environ.get('APP_TRUST_PROXY_PROTO')=='1':
        # Enable only behind the hosting provider's trusted HTTPS gateway.
        # Client IP and Host are deliberately not taken from forwarded headers.
        application=ProxyFix(application,x_for=0,x_proto=1,x_host=0,x_port=0,x_prefix=0)
    return application

application=create_site()
