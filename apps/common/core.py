"""Shared accounts, revocable sessions and local/hosted request protections."""
import csv, io, json, os, re, secrets, sqlite3, time, hashlib, hmac
from datetime import timedelta, datetime, timezone
from pathlib import Path
from functools import wraps
from urllib.parse import urlsplit
from flask import Flask, jsonify, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import HTTPException


def now(): return datetime.now(timezone.utc).isoformat()

def connect(path):
    conn = sqlite3.connect(path, timeout=15)
    conn.row_factory = sqlite3.Row
    return conn

def token_hash(value): return hashlib.sha256(value.encode()).hexdigest()

def create_app(name, root, roles):
    app = Flask(name, template_folder=str(root/'templates'))
    data = Path(os.environ.get(name.upper()+'_DATA', root/'.runtime')).resolve()
    data.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(data, 0o700)
    keyfile = data/'secret.key'
    try:
        fd = os.open(keyfile, os.O_CREAT|os.O_EXCL|os.O_WRONLY, 0o600)
        with os.fdopen(fd, 'wb') as f: f.write(secrets.token_bytes(32))
    except FileExistsError: pass
    os.chmod(keyfile,0o600)
    app.secret_key = keyfile.read_bytes()
    if len(app.secret_key)<32: raise RuntimeError('Signing key is too short.')
    hosted=os.environ.get('APP_MODE','local')=='hosted'
    origin=os.environ.get('APP_PUBLIC_ORIGIN','').rstrip('/')
    parsed=urlsplit(origin)
    if hosted and (parsed.scheme!='https' or not parsed.hostname or parsed.path or parsed.query or parsed.fragment or parsed.username or parsed.password):
        raise RuntimeError('Hosted mode requires APP_PUBLIC_ORIGIN=https://your-exact-hostname')
    prefix=os.environ.get(name.upper()+'_PREFIX','')
    if prefix and not re.fullmatch(r'/[a-z][a-z0-9-]*',prefix):raise RuntimeError('Invalid application path prefix.')
    app.config.update(DATA=data, DB=data/'workspace.sqlite', HOSTED=hosted, PUBLIC_ORIGIN=origin, APP_PREFIX=prefix,
        MAX_CONTENT_LENGTH=20*1024*1024, MAX_FORM_MEMORY_SIZE=256*1024, MAX_FORM_PARTS=12,
        SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Strict', SESSION_COOKIE_SECURE=hosted,
        SESSION_COOKIE_NAME=name+'_session', SESSION_COOKIE_PATH=prefix+'/' if prefix else '/',
        SESSION_REFRESH_EACH_REQUEST=False, PERMANENT_SESSION_LIFETIME=timedelta(hours=8),
        SESSION_IDLE_SECONDS=1800, SESSION_ABSOLUTE_SECONDS=28800,
        TRUSTED_HOSTS=[parsed.hostname] if hosted else ['127.0.0.1','localhost'])
    with connect(app.config['DB']) as db:
        db.executescript('''CREATE TABLE IF NOT EXISTS users (name TEXT PRIMARY KEY, password TEXT NOT NULL, role TEXT NOT NULL, disabled INTEGER NOT NULL DEFAULT 0);
        CREATE TABLE IF NOT EXISTS audit (id INTEGER PRIMARY KEY, at TEXT, actor TEXT, action TEXT, detail TEXT);
        CREATE TABLE IF NOT EXISTS sessions (id TEXT PRIMARY KEY, user TEXT NOT NULL, created REAL NOT NULL, seen REAL NOT NULL, expires REAL NOT NULL);
        CREATE INDEX IF NOT EXISTS session_user ON sessions(user);
        CREATE TABLE IF NOT EXISTS attempts (bucket TEXT NOT NULL, at REAL NOT NULL);
        CREATE INDEX IF NOT EXISTS attempt_bucket ON attempts(bucket,at);''')
        if 'disabled' not in [r[1] for r in db.execute('PRAGMA table_info(users)')]:db.execute('ALTER TABLE users ADD COLUMN disabled INTEGER NOT NULL DEFAULT 0')
    os.chmod(app.config['DB'],0o600)
    dummy_hash=generate_password_hash(secrets.token_urlsafe(32))

    def audit(action, detail=''):
        with connect(app.config['DB']) as db:
            db.execute('INSERT INTO audit(at,actor,action,detail) VALUES (?,?,?,?)', (now(),(getattr(g,'user',None) or {}).get('name','setup'),action,str(detail)[:500]))
            db.execute('DELETE FROM audit WHERE id <= (SELECT COALESCE(MAX(id),0)-10000 FROM audit) OR at < ?',((datetime.now(timezone.utc)-timedelta(days=30)).isoformat(),))
    app.audit = audit

    def rate_limit(scope, identity, maximum=10, window=300):
        """Reserve attempts atomically, including successes; never clear another account."""
        stamp=time.time()
        labels=[(scope+':account:'+str(identity)[:80],maximum),(scope+':ip:'+(request.remote_addr or 'local'),100)]
        buckets=[(hmac.new(app.secret_key,label.encode(),hashlib.sha256).hexdigest(),limit) for label,limit in labels]
        with connect(app.config['DB']) as db:
            db.execute('BEGIN IMMEDIATE')
            db.execute('DELETE FROM attempts WHERE at < ?',(stamp-3600,))
            for bucket,limit in buckets:
                if db.execute('SELECT COUNT(*) FROM attempts WHERE bucket=? AND at>?',(bucket,stamp-window)).fetchone()[0]>=limit:
                    return False
            db.executemany('INSERT INTO attempts VALUES (?,?)',[(bucket,stamp) for bucket,_ in buckets])
        return True
    app.rate_limit=rate_limit

    def revoke_current():
        sid=session.get('sid')
        if isinstance(sid,str):
            with connect(app.config['DB']) as db:db.execute('DELETE FROM sessions WHERE id=?',(token_hash(sid),))
        session.clear()

    def issue_session(user, expected_password=None):
        revoke_current();stamp=time.time();sid=secrets.token_urlsafe(32)
        with connect(app.config['DB']) as db:
            db.execute('BEGIN IMMEDIATE')
            current=db.execute('SELECT password,disabled FROM users WHERE name=?',(user['name'],)).fetchone()
            if not current or current['disabled'] or (expected_password is not None and current['password']!=expected_password):
                raise ValueError('Account access changed. Please sign in again.')
            db.execute('DELETE FROM sessions WHERE expires<? OR seen<?',(stamp,stamp-app.config['SESSION_IDLE_SECONDS']))
            db.execute('INSERT INTO sessions VALUES (?,?,?,?,?)',(token_hash(sid),user['name'],stamp,stamp,stamp+app.config['SESSION_ABSOLUTE_SECONDS']))
            # Keep a bounded set of current devices for each account.
            db.execute('DELETE FROM sessions WHERE user=? AND id NOT IN (SELECT id FROM sessions WHERE user=? ORDER BY created DESC LIMIT 10)',(user['name'],user['name']))
        session.update(sid=sid,csrf=secrets.token_urlsafe(32));session.permanent=True
        g.user={'name':user['name'],'role':user['role']}

    @app.before_request
    def protect():
        if hosted and not request.is_secure:
            return jsonify(error='Use the HTTPS address for this workspace.'),400
        g.user=None
        g.session_expires=None
        sid=session.get('sid')
        if isinstance(sid,str) and len(sid)<=128:
            stamp=time.time()
            with connect(app.config['DB']) as db:
                user=db.execute('SELECT u.name,u.role,s.expires FROM sessions s JOIN users u ON s.user=u.name WHERE s.id=? AND s.expires>? AND s.seen>? AND u.disabled=0',(token_hash(sid),stamp,stamp-app.config['SESSION_IDLE_SECONDS'])).fetchone()
                if user:
                    g.user={'name':user['name'],'role':user['role']};g.session_expires=user['expires'];db.execute('UPDATE sessions SET seen=? WHERE id=?',(stamp,token_hash(sid)))
                else:session.clear()
        if request.is_json and request.method not in ('GET','HEAD','OPTIONS') and not isinstance(request.get_json(silent=True),dict):
            return jsonify(error='Request body must be a JSON object.'),400
        public=('/api/status','/api/setup','/api/login')
        if request.path.startswith('/api/') and request.path not in public and not g.user:
            return jsonify(error='Your session ended. Sign in again.'),401
        if request.method not in ('GET','HEAD','OPTIONS'):
            if request.headers.get('X-Local-App') != '1': return jsonify(error='Use the application to make changes.'),403
            expected_origin=origin if hosted else request.host_url.rstrip('/')
            request_origin=request.headers.get('Origin')
            if request_origin and request_origin != expected_origin:return jsonify(error='Cross-origin request rejected.'),403
            if request.headers.get('Sec-Fetch-Site')=='cross-site':return jsonify(error='Cross-site request rejected.'),403
            if request.path not in ('/api/setup','/api/login') and not secrets.compare_digest(request.headers.get('X-CSRF-Token',''),session.get('csrf','missing')):
                return jsonify(error='Session changed. Refresh this page before trying again.'),403

    @app.context_processor
    def browser_config():return dict(app_prefix=prefix,hosted=hosted)

    @app.after_request
    def headers(r):
        r.headers.update({'Cache-Control':'no-store','X-Content-Type-Options':'nosniff','X-Frame-Options':'DENY',
            'Referrer-Policy':'no-referrer','Permissions-Policy':'camera=(), microphone=(), geolocation=(), payment=()',
            'Cross-Origin-Resource-Policy':'same-origin',
            'Content-Security-Policy':"default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; object-src 'none'; form-action 'self'"})
        if hosted:r.headers['Strict-Transport-Security']='max-age=31536000'
        return r

    @app.errorhandler(ValueError)
    def bad_request(e):return jsonify(error=str(e)),400
    @app.errorhandler(HTTPException)
    def http_error(e):return jsonify(error=e.description),e.code
    @app.errorhandler(Exception)
    def unexpected(e):
        # Avoid recording request bodies, patient details, database values or credentials.
        app.logger.error('Request failed: %s',type(e).__name__)
        return jsonify(error='We could not complete that request. Your saved data is unchanged unless a save was already confirmed. Please refresh and check before retrying.'),500

    @app.get('/api/status')
    def status():
        with connect(app.config['DB']) as db:count=db.execute('SELECT COUNT(*) FROM users').fetchone()[0]
        session.setdefault('csrf',secrets.token_urlsafe(32))
        return jsonify(setup_required=count==0 and not hosted,setup_locked=count==0 and hosted,user=g.user,csrf=session['csrf'],roles=roles,hosted=hosted,session_expires=g.session_expires,idle_seconds=app.config['SESSION_IDLE_SECONDS'])

    def credentials(body):
        username=body.get('name','');password=body.get('password','')
        if not isinstance(username,str) or not re.fullmatch(r'[a-zA-Z0-9_.-]{3,40}',username):raise ValueError('Username: 3–40 letters, numbers, dots, underscores or hyphens.')
        if not isinstance(password,str) or not 12<=len(password)<=256:raise ValueError('Use a password of 12–256 characters.')
        return username,password

    @app.post('/api/setup')
    def setup():
        if hosted:return jsonify(error='Online setup is disabled. The site owner must create the first account from the hosting console.'),403
        username,password=credentials(request.get_json() or {})
        with connect(app.config['DB']) as db:
            db.execute('BEGIN IMMEDIATE')
            if db.execute('SELECT COUNT(*) FROM users').fetchone()[0]:return jsonify(error='Workspace is already set up.'),409
            db.execute('INSERT INTO users(name,password,role) VALUES (?,?,?)',(username,generate_password_hash(password),roles[0]))
        issue_session({'name':username,'role':roles[0]});audit('workspace_created');return jsonify(ok=True)

    @app.post('/api/login')
    def login():
        b=request.get_json() or {};username=b.get('name','');password=b.get('password','')
        if not isinstance(username,str) or not isinstance(password,str):raise ValueError('Enter a username and password.')
        if not re.fullmatch(r'[a-zA-Z0-9_.-]{3,40}',username):return jsonify(error='Incorrect username or password.'),401
        if not rate_limit('login',username):return jsonify(error='Too many sign-in attempts. Wait five minutes before trying again.'),429,{'Retry-After':'300'}
        with connect(app.config['DB']) as db:user=db.execute('SELECT * FROM users WHERE name=?',(username,)).fetchone()
        valid=check_password_hash(user['password'] if user else dummy_hash,password[:257])
        if not valid or not user or user['disabled'] or len(password)>256:return jsonify(error='Incorrect username or password.'),401
        issue_session(dict(user),expected_password=user['password']);audit('signed_in');return jsonify(ok=True)

    @app.post('/api/logout')
    def logout():audit('signed_out');revoke_current();return jsonify(ok=True)

    @app.post('/api/account/sign-out-all')
    def sign_out_all():
        audit('all_sessions_revoked')
        with connect(app.config['DB']) as db:db.execute('DELETE FROM sessions WHERE user=?',(g.user['name'],))
        session.clear();return jsonify(ok=True)

    def reauthenticate(body):
        if not rate_limit('reauth',g.user['name']):return False
        with connect(app.config['DB']) as db:user=db.execute('SELECT password FROM users WHERE name=?',(g.user['name'],)).fetchone()
        value=body.get('current_password','')
        return user['password'] if isinstance(value,str) and len(value)<=256 and check_password_hash(user['password'],value) else None

    @app.post('/api/account/password')
    def password_change():
        body=request.get_json() or {}
        verified_hash=reauthenticate(body)
        if not verified_hash:return jsonify(error='Current password was not accepted, or too many attempts. Please try again later.'),403
        username,password=credentials({'name':g.user['name'],'password':body.get('new_password')})
        new_hash=generate_password_hash(password)
        with connect(app.config['DB']) as db:
            db.execute('BEGIN IMMEDIATE')
            if not db.execute('UPDATE users SET password=? WHERE name=? AND password=?',(new_hash,username,verified_hash)).rowcount:
                raise ValueError('Your password changed in another session. Sign in again before retrying.')
            db.execute('DELETE FROM sessions WHERE user=?',(username,))
        audit('password_changed');session.clear();return jsonify(ok=True)

    @app.get('/api/account/security')
    def security_status():
        with connect(app.config['DB']) as db:count=db.execute('SELECT COUNT(*) FROM sessions WHERE user=? AND expires>? AND seen>?',(g.user['name'],time.time(),time.time()-app.config['SESSION_IDLE_SECONDS'])).fetchone()[0]
        return jsonify(active_sessions=count,idle_minutes=app.config['SESSION_IDLE_SECONDS']//60,absolute_hours=app.config['SESSION_ABSOLUTE_SECONDS']//3600,hosted=hosted,shared_workspace=True)

    @app.get('/api/users')
    def users():
        if g.user['role']!=roles[0]:return jsonify(error='Administrator access required.'),403
        with connect(app.config['DB']) as db:return jsonify(users=[dict(x) for x in db.execute('SELECT name,role,disabled FROM users ORDER BY name')])

    @app.post('/api/users')
    def add_user():
        if g.user['role']!=roles[0]:return jsonify(error='Administrator access required.'),403
        b=request.get_json() or {};username,password=credentials(b)
        if b.get('role') not in roles:raise ValueError('Choose a valid role.')
        try:
            with connect(app.config['DB']) as db:
                db.execute('BEGIN IMMEDIATE')
                if db.execute('SELECT COUNT(*) FROM users').fetchone()[0]>=50:raise ValueError('This test workspace supports up to 50 accounts.')
                db.execute('INSERT INTO users(name,password,role) VALUES (?,?,?)',(username,generate_password_hash(password),b['role']))
        except sqlite3.IntegrityError:return jsonify(error='Username already exists.'),409
        audit('user_created',username+': '+b['role']);return jsonify(ok=True),201

    @app.post('/api/users/<username>/status')
    def user_status(username):
        if g.user['role']!=roles[0]:return jsonify(error='Administrator access required.'),403
        if username==g.user['name']:raise ValueError('You cannot disable your own account.')
        body=request.get_json() or {};disabled=body.get('disabled')
        if type(disabled) is not bool:raise ValueError('Choose enabled or disabled.')
        with connect(app.config['DB']) as db:
            if not db.execute('UPDATE users SET disabled=? WHERE name=?',(int(disabled),username)).rowcount:return jsonify(error='Account not found.'),404
            if disabled:db.execute('DELETE FROM sessions WHERE user=?',(username,))
        audit('user_disabled' if disabled else 'user_enabled',username);return jsonify(ok=True)

    @app.get('/api/audit')
    def logs():
        if g.user['role']!=roles[0]:return jsonify(error='Administrator access required.'),403
        with connect(app.config['DB']) as db:return jsonify(events=[dict(x) for x in db.execute('SELECT * FROM audit ORDER BY id DESC LIMIT 100')])
    return app


def admin(fn):
    @wraps(fn)
    def wrapped(*args,**kwargs):
        if g.user['role']!='Admin':return jsonify(error='Administrator access required.'),403
        return fn(*args,**kwargs)
    return wrapped


def csv_rows(raw):
    try:text=raw.decode('utf-8-sig')
    except UnicodeDecodeError:raise ValueError('Upload a UTF-8 CSV file.')
    if '\x00' in text:raise ValueError('Binary data is not a CSV file.')
    try:delimiter=csv.Sniffer().sniff(text[:8192],delimiters=',;\t').delimiter
    except csv.Error:delimiter=','
    reader=csv.reader(io.StringIO(text),delimiter=delimiter)
    try:
        columns=next(reader)
        if not 1<=len(columns)<=64 or any(not c.strip() or len(c)>100 for c in columns):raise ValueError('Use 1–64 named columns, each at most 100 characters.')
        if len(set(c.casefold() for c in columns))!=len(columns):raise ValueError('Column names must be unique.')
        rows=[]
        for row in reader:
            if not row:continue
            if len(row)!=len(columns):raise ValueError('Every CSV row must have the same number of columns.')
            if any(len(v)>4000 for v in row):raise ValueError('CSV cells are limited to 4,000 characters.')
            rows.append(row)
            if len(rows)>100000:raise ValueError('Import up to 100,000 rows at a time.')
    except (StopIteration,csv.Error):raise ValueError('CSV is empty or malformed.')
    if not rows:raise ValueError('CSV needs at least one data row.')
    return columns,rows


def safe_csv(value):
    value=str(value if value is not None else '')
    return "'"+value if value.lstrip().startswith(('=','+','-','@','\t','\r')) else value
