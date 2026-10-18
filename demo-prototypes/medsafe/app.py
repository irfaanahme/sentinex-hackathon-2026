"""Medication Safety workflow prototype using fictional exercise medicines only."""
from difflib import SequenceMatcher
from itertools import combinations
from pathlib import Path
import json
import re

from flask import Flask, jsonify, render_template, request

ROOT = Path(__file__).resolve().parent
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 8192
DISCLAIMER = 'A clinician decides. This prototype uses fictional medicines and illustrative rules, not clinical guidance.'
REFERENCE = [
    {'id': 'A', 'generic': 'Demo Alpha', 'brands': ['AlphaTab', 'AlphaPlus'], 'class': 'Exercise class 1', 'renal_threshold': 40},
    {'id': 'B', 'generic': 'Demo Beta', 'brands': ['BetaTab'], 'class': 'Exercise class 2'},
    {'id': 'C', 'generic': 'Demo Gamma', 'brands': ['GammaTab'], 'class': 'Exercise class 3', 'pregnancy_restricted': True},
    {'id': 'D', 'generic': 'Demo Delta', 'brands': ['DeltaTab'], 'class': 'Exercise class 1'},
]
INTERACTIONS = {frozenset(('A', 'B')): {'id': 'INT-01', 'severity': 'HIGH', 'action': 'Prescriber to review this combination against the authoritative exercise reference.'}}
PATIENTS = {
    'review': {'id': 'SYN-001', 'age': 72, 'egfr': 28, 'pregnant': False, 'medications': ['Alphatb', 'BetaTab', 'AlphaPlus']},
    'pregnancy': {'id': 'SYN-002', 'age': 29, 'egfr': 90, 'pregnant': True, 'medications': ['GammaTab']},
    'incomplete': {'id': 'SYN-003', 'age': 65, 'egfr': None, 'pregnant': None, 'medications': ['AlphaTab', 'UnknownDrug']},
    'no_issue': {'id': 'SYN-004', 'age': 43, 'egfr': 95, 'pregnant': False, 'medications': ['BetaTab']},
}


def normalize(text):
    return re.sub(r'[^a-z0-9]', '', text.lower())


def resolve(text):
    needle = normalize(text)
    ranked = []
    for drug in REFERENCE:
        aliases = [drug['generic']] + drug['brands']
        score = max(SequenceMatcher(None, needle, normalize(alias)).ratio() for alias in aliases)
        ranked.append((score, drug))
    ranked.sort(key=lambda item: item[0], reverse=True)
    best, runner = ranked[0], ranked[1]
    accepted = best[0] == 1 or (best[0] >= .80 and best[0] - runner[0] >= .12)
    return {'input': text, 'drug_id': best[1]['id'] if accepted else None,
            'generic': best[1]['generic'] if accepted else 'Unresolved',
            'method': ('exact alias' if best[0] == 1 else 'fuzzy match') if accepted else 'needs review',
            'confidence': round(best[0], 3) if accepted else None}


def check_patient(patient):
    matches = [resolve(name) for name in patient['medications']]
    resolved = {m['drug_id'] for m in matches if m['drug_id']}
    drugs = {d['id']: d for d in REFERENCE}
    alerts, limitations = [], []

    def alert(rule_id, issue, severity, ids, action):
        matching = [m['confidence'] for m in matches if m['drug_id'] in ids and m['confidence'] is not None]
        alerts.append({'rule_id': rule_id, 'issue': issue, 'severity': severity,
                       'drugs': [drugs[i]['generic'] for i in sorted(ids)], 'action': action,
                       'confidence': min(matching) if matching else None,
                       'limitations': 'Match confidence is a string-similarity score, not clinical certainty. Illustrative reference only.'})

    for pair, rule in INTERACTIONS.items():
        if pair <= resolved:
            alert(rule['id'], 'Interaction', rule['severity'], pair, rule['action'])
    for drug_id in sorted(resolved):
        drug = drugs[drug_id]
        if sum(m['drug_id'] == drug_id for m in matches) > 1:
            alert('DUP-' + drug_id, 'Duplicate therapy', 'MODERATE', {drug_id}, 'Reconcile repeated entries before the prescriber makes a decision.')
        if 'renal_threshold' in drug:
            if patient.get('egfr') is None:
                limitations.append('Kidney-function context missing. Renal check incomplete for ' + drug['generic'] + '.')
            elif patient['egfr'] < drug['renal_threshold']:
                alert('REN-' + drug_id, 'Renal dose review', 'HIGH', {drug_id}, 'Prescriber to review dosing against the authoritative renal reference. This demo does not recommend a dose.')
        if drug.get('pregnancy_restricted'):
            if patient.get('pregnant') is None:
                limitations.append('Pregnancy status missing. Contraindication check incomplete.')
            elif patient['pregnant']:
                alert('CON-' + drug_id, 'Contraindication', 'HIGH', {drug_id}, 'Prescriber to review the flagged pregnancy restriction in the authoritative exercise reference.')
    for a, b in combinations(sorted(resolved), 2):
        if drugs[a]['class'] == drugs[b]['class']:
            alert('CLASS-' + a + b, 'Duplicate therapy', 'MODERATE', {a, b}, 'Prescriber to reconcile the two entries in the same exercise medicine class.')
    unknown = [m['input'] for m in matches if not m['drug_id']]
    if unknown:
        limitations.append('Unresolved medicine names: ' + ', '.join(unknown) + '. Checks involving these entries remain incomplete.')
    limitations.append('Medication list may be incomplete. No allergy history is available in this example.')
    alerts.sort(key=lambda a: (0 if a['severity'] == 'HIGH' else 1, a['rule_id']))
    return {'patient': patient, 'matches': matches, 'alerts': alerts, 'limitations': limitations,
            'message': 'Prioritized issues for clinician review' if alerts else 'No issue found in the supplied list under these demo rules. This does not establish safety.',
            'disclaimer': DISCLAIMER, 'reference': '4 fictional medicines and 1 illustrative interaction pair. Not organizer-provided assets.'}


def evaluate():
    match_cases = [('AlphaTab', 'A'), ('Alphatb', 'A'), ('AlphaPlus', 'A'), ('BetaTba', 'B'),
                   ('GamaTab', 'C'), ('Demo Delta', 'D'), ('UnknownDrug', None), ('Demo', None)]
    match_pass = sum(resolve(text)['drug_id'] == expected for text, expected in match_cases)
    # Labels are written independently for tiny illustrative patient cases.
    expected = {'review': {'INT-01', 'REN-A', 'DUP-A'}, 'pregnancy': {'CON-C'}, 'no_issue': set(),
                'incomplete': set()}
    tp = fn = extras = 0
    cases = []
    for name, labels in expected.items():
        result = check_patient(PATIENTS[name])
        predicted = {a['rule_id'] for a in result['alerts']}
        serious_expected = labels - {'DUP-A'}
        serious_predicted = {a['rule_id'] for a in result['alerts'] if a['severity'] == 'HIGH'}
        tp += len(serious_expected & serious_predicted)
        fn += len(serious_expected - serious_predicted)
        extras += len(predicted - labels)
        cases.append({'case': name, 'expected': sorted(labels), 'observed': sorted(predicted), 'pass': labels == predicted})
    return {'matching': {'passed': match_pass, 'total': len(match_cases)},
            'serious': {'found': tp, 'total': tp + fn}, 'extra_alerts': extras,
            'cases': cases, 'official_near_miss_recall': None,
            'limitations': 'Tiny handcrafted demo fixtures only. Official 300-case near-miss recall is not measured. Organizer reference and evaluate.py have not been supplied.'}


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/api/reference')
def reference():
    return jsonify(medicines=REFERENCE, disclaimer=DISCLAIMER)


@app.post('/api/check')
def check():
    body = request.get_json(silent=True) or {}
    if 'case' in body:
        if body['case'] not in PATIENTS:
            return jsonify(error='Unknown synthetic example'), 400
        patient = PATIENTS[body['case']]
    else:
        patient = body.get('patient')
        if not isinstance(patient, dict) or not isinstance(patient.get('medications'), list) or not 1 <= len(patient['medications']) <= 20:
            return jsonify(error='Provide 1 to 20 medicine names'), 400
        if any(not isinstance(name, str) or not 1 <= len(name) <= 80 for name in patient['medications']):
            return jsonify(error='Invalid medicine name'), 400
        egfr = patient.get('egfr')
        if egfr is not None and (type(egfr) not in (int, float) or not 0 <= egfr <= 200):
            return jsonify(error='Invalid eGFR'), 400
        if patient.get('pregnant') is not None and type(patient.get('pregnant')) is not bool:
            return jsonify(error='Invalid pregnancy status'), 400
    return jsonify(check_patient(patient))


@app.get('/api/evaluate')
def evaluation():
    return jsonify(evaluate())


@app.after_request
def headers(response):
    response.headers['Cache-Control'] = 'no-store'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8766, debug=False, threaded=False)
