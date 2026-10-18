"""Local, synthetic-data MaskGate proof of concept. No arbitrary SQL endpoint."""
from pathlib import Path
from contextlib import contextmanager
import hashlib
import hmac
import json
import re
import secrets
import sqlite3
import statistics
import time

import duckdb
from flask import Flask, jsonify, render_template, request, session

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "private-build" / "data"
DATA.mkdir(parents=True, exist_ok=True)
BACKENDS = ("SQLite", "DuckDB")
COLUMNS = ("customer_id", "full_name", "email", "phone", "card_number", "account_balance", "city", "tier")
ROWS = [
    ("C001", "Demo Customer A", "customer.a@example.test", "+1-202-555-0101", "4111111111111111", 18420.50, "Visakhapatnam", "Gold"),
    ("C002", "Demo Customer B", "customer.b@example.test", "+1-202-555-0102", "5555555555554444", 7260.00, "Vijayawada", "Silver"),
    ("C003", "Demo Customer C", "customer.c@example.test", "+1-202-555-0103", "4000000000000002", 35910.25, "Guntur", "Gold"),
]
QUERY = "SELECT " + ", ".join(COLUMNS) + " FROM customers ORDER BY customer_id"
ACCOUNTS = {"admin.demo": "Admin", "support.demo": "Support", "analyst.demo": "Analyst"}
HASH_KEY = secrets.token_bytes(32)
app = Flask(__name__)
app.secret_key = secrets.token_bytes(32)
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Strict", MAX_CONTENT_LENGTH=4096)


@contextmanager
def connect(backend):
    if backend not in BACKENDS:
        raise ValueError("Unknown backend")
    connection = (sqlite3.connect(DATA / "customers.sqlite") if backend == "SQLite"
                  else duckdb.connect(str(DATA / "customers.duckdb")))
    try:
        yield connection
    finally:
        connection.close()


def initialize():
    for backend in BACKENDS:
        with connect(backend) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS customers (customer_id TEXT PRIMARY KEY, full_name TEXT, email TEXT, phone TEXT, card_number TEXT, account_balance DOUBLE, city TEXT, tier TEXT)")
            if conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0] == 0:
                conn.executemany("INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?, ?)", ROWS)
            conn.commit()


def fetch(backend):
    with connect(backend) as conn:
        return [dict(zip(COLUMNS, row)) for row in conn.execute(QUERY).fetchall()]


def classify(name, samples):
    """Small deterministic scanner: schema hints plus nonempty sample patterns."""
    name = name.lower()
    nonempty = [str(value) for value in samples if value is not None and str(value).strip()]
    if any(word in name for word in ("balance", "salary", "income")):
        return "FINANCIAL_CONFIDENTIAL", "Financial column name"
    if any(word in name for word in ("email", "phone", "card_number", "full_name", "ssn")):
        return "PII_HIGH", "Sensitive column name"
    patterns = [r"[^\s@]+@[^\s@]+\.[^\s@]+", r"\d{13,19}", r"\+\d[\d ()-]{9,18}"]
    if any(re.fullmatch(pattern, value) for pattern in patterns for value in nonempty):
        return "PII_HIGH", "Sensitive pattern in row sample"
    return "PUBLIC", "No sensitive rule matched"


def scan(backend):
    rows = fetch(backend)
    return [{"field": col, "tag": classify(col, [r[col] for r in rows])[0],
             "reason": classify(col, [r[col] for r in rows])[1]} for col in COLUMNS]


def transform(value, field, tag, role):
    if value is None or tag == "PUBLIC" or role == "Admin":
        return value
    if role == "Analyst":
        if field == "email":
            return "hash:" + hmac.new(HASH_KEY, str(value).encode(), "sha256").hexdigest()[:12]
        return "[REDACTED]"
    text = str(value)
    if tag == "FINANCIAL_CONFIDENTIAL":
        return "[REDACTED]"
    if field == "email":
        return text[:1] + "***@" + text.split("@", 1)[1]
    if field in ("card_number", "phone"):
        return "**** **** **** " + text[-4:]
    return text[:1] + "***"


def masked(backend, role):
    rows = fetch(backend)
    tags = {item["field"]: item["tag"] for item in scan(backend)}
    return [{col: transform(row[col], col, tags[col], role) for col in COLUMNS} for row in rows]


def digest(backend):
    return hashlib.sha256(json.dumps(fetch(backend), sort_keys=True).encode()).hexdigest()


initialize()
BASELINES = {backend: digest(backend) for backend in BACKENDS}


def evaluate():
    # Separate labeled examples include neutral headers, empty and mixed samples.
    examples = [
        ("contact", ["demo@example.test"], "PII_HIGH"),
        ("reference", [None, "", "4111111111111111"], "PII_HIGH"),
        ("callback", ["+1-202-555-0101"], "PII_HIGH"),
        ("full_name", ["Demo Customer"], "PII_HIGH"),
        ("account_balance", [10.0], "FINANCIAL_CONFIDENTIAL"),
        ("salary", [None], "FINANCIAL_CONFIDENTIAL"),
        ("phone", [None], "PII_HIGH"),
        ("email", [None, ""], "PII_HIGH"),
        ("customer_id", ["C001"], "PUBLIC"),
        ("city", ["Guntur"], "PUBLIC"),
        ("tier", ["Gold"], "PUBLIC"),
        ("email_opt_in", ["yes", "no"], "PUBLIC"),
        ("notes", ["call tomorrow"], "PUBLIC"),
        ("reference", [None, ""], "PUBLIC"),
    ]
    predictions = [classify(name, values)[0] for name, values, _ in examples]
    tp = sum(pred != "PUBLIC" and expected != "PUBLIC" for pred, (_, _, expected) in zip(predictions, examples))
    fp = sum(pred != "PUBLIC" and expected == "PUBLIC" for pred, (_, _, expected) in zip(predictions, examples))
    fn = sum(pred == "PUBLIC" and expected != "PUBLIC" for pred, (_, _, expected) in zip(predictions, examples))
    # Independent expected policy properties for each row, role, column and backend.
    passed = total = 0
    checks = []
    timings = []
    for backend in BACKENDS:
        original = fetch(backend)
        for role in ACCOUNTS.values():
            result = masked(backend, role)
            for source, output in zip(original, result):
                for col in COLUMNS:
                    if role == "Admin" or col in ("customer_id", "city", "tier"):
                        ok = output[col] == source[col]
                    elif role == "Support":
                        expected = {"full_name": "D***", "email": "c***@example.test", "account_balance": "[REDACTED]"}
                        ok = output[col] == expected[col] if col in expected else (str(source[col])[-4:] in output[col] and output[col] != source[col])
                    else:
                        ok = (bool(re.fullmatch(r"hash:[a-f0-9]{12}", output[col])) and output[col] != source[col]) if col == "email" else output[col] == "[REDACTED]"
                    passed += int(ok)
                    total += 1
        unchanged = digest(backend) == BASELINES[backend]
        checks.append({"backend": backend, "unchanged": unchanged, "sha256": digest(backend)})
        # Warm connections, alternate paths, exclude open/close, report median over 50 calls.
        tags = {item["field"]: item["tag"] for item in scan(backend)}
        raw_times, masked_times = [], []
        with connect(backend) as conn:
            for i in range(55):
                for protect in ([False, True] if i % 2 else [True, False]):
                    start = time.perf_counter_ns()
                    rows = [dict(zip(COLUMNS, row)) for row in conn.execute(QUERY).fetchall()]
                    if protect:
                        rows = [{c: transform(r[c], c, tags[c], "Support") for c in COLUMNS} for r in rows]
                    elapsed = (time.perf_counter_ns() - start) / 1e6
                    if i >= 5:
                        (masked_times if protect else raw_times).append(elapsed)
        timings.append({"backend": backend, "baseline_ms": round(statistics.median(raw_times), 3), "masked_ms": round(statistics.median(masked_times), 3)})
    return {"scanner": {"precision": round(tp / (tp + fp), 3), "recall": round(tp / (tp + fn), 3),
                        "examples": len(examples), "tp": tp, "fp": fp, "fn": fn},
            "policy": {"passed": passed, "total": total}, "source_checks": checks, "latency": timings,
            "limits": "Tiny synthetic fixture. Scanner includes a known false positive. Demo identities have no passwords. Fixed SELECT only. PostgreSQL and production authentication remain future work."}


@app.after_request
def headers(response):
    response.headers["Cache-Control"] = "no-store"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/session")
def login():
    if request.headers.get("X-MaskGate-Demo") != "local":
        return jsonify(error="Demo header required"), 403
    body = request.get_json(silent=True) or {}
    if set(body) != {"account"} or body["account"] not in ACCOUNTS:
        return jsonify(error="Choose a configured demo account"), 400
    session.clear()
    session["account"] = body["account"]
    return jsonify(account=body["account"], role=ACCOUNTS[body["account"]])


@app.post("/api/query")
def query():
    account = session.get("account")
    if account not in ACCOUNTS:
        return jsonify(error="Choose a demo identity first"), 401
    body = request.get_json(silent=True) or {}
    if set(body) != {"backend", "query_id"}:
        return jsonify(error="Request rejected: raw SQL and client-supplied roles are forbidden."), 403
    if body["backend"] not in BACKENDS or body["query_id"] != "customer_directory":
        return jsonify(error="Only the approved customer_directory query is allowed."), 403
    role = ACCOUNTS[account]
    return jsonify(backend=body["backend"], role=role, columns=COLUMNS, rows=masked(body["backend"], role), query=QUERY)


@app.get("/api/scan")
def scan_api():
    backend = request.args.get("backend", "SQLite")
    if backend not in BACKENDS:
        return jsonify(error="Unknown backend"), 400
    return jsonify(backend=backend, fields=scan(backend), row_count=len(ROWS))


@app.get("/api/evaluate")
def evaluation_api():
    return jsonify(evaluate())


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8765, debug=False, threaded=False)
