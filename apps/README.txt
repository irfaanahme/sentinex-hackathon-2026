HOSTING AND SECURITY UPDATE — 18 October 2026

CURRENT STATUS: Both apps are deployed at
https://iamirfaanahmed.pythonanywhere.com/medsafe/
https://iamirfaanahmed.pythonanywhere.com/maskgate/
Owner sign-in and one basic workflow in each app were verified. See README.md
in this folder for the current portable launch instructions. The historical
notes below describe earlier local development, not the current deployment.

Both apps now include Account & privacy controls, revocable server sessions,
password changes, sign out all devices and administrator account disabling.
Public first-owner setup is disabled in hosted mode. See HOSTING.txt for the
PythonAnywhere deployment configuration and honest security limitations.
The hosted deployment is live with public/synthetic test data only.
Use requirements-lock.txt to reproduce the dependency versions tested here.

Verification: 16 workflow tests passed in 69.204s; 19 security/deployment tests
passed in 5.655s. The latter include copied-cookie replay after logout,
absolute/idle expiry, password-change/disable revocation, persistent rate
limits, cross-account reset prevention, restricted metadata and both URL paths.
Browser checks exercised login, account/privacy pages, patient pagination and
review after changes, with no captured JavaScript errors. This is not proof of
zero bugs or a production-security certification.

The historical first-release notes below describe the earlier baseline.
Where they differ, HOSTING.txt and the update above describe the current version.

SENTINEX LOCAL APPS — FIRST WORKING RELEASE
18 October 2026

The polished hackathon demos remain in maskgate-poc/ and medication-poc/.
These new apps live separately in local-apps/. Nothing has been published or pushed.

OPEN ON THIS COMPUTER
MaskGate: http://127.0.0.1:8775
MedSafe:  http://127.0.0.1:8776
Each app asks you to create its first administrator username and password.
No default user password is installed in the working apps.

START AGAIN
From the workspace folder, in separate Terminal windows:
  maskgate-poc/.venv/bin/python local-apps/run.py maskgate
  maskgate-poc/.venv/bin/python local-apps/run.py medsafe

On another computer, create a Python 3.12 virtual environment and install
local-apps/requirements.txt. Then run run.py with maskgate or medsafe.
Fetch public data with fetch_datasets.py; prepare_workspace.py preloads it
without creating accounts. Existing workspaces are preserved.

MASKGATE
- Import UTF-8 comma-, semicolon- or tab-delimited CSVs, up to 100,000 rows,
  64 columns and 20 MB. Independent persistent SQLite and DuckDB copies.
- Field scanner suggests classifications; administrator reviews policies.
- Unknown or unapproved fields stay blocked for Support and Analyst accounts.
- Public fields remain visible; personal identifiers are partially masked
  for Support or keyed-hashed for Analyst; financial values are redacted.
- Admin account creation, password sign-in, server-assigned roles, pagination,
  exact-match filters, role-aware CSV downloads and an activity log.
- Filters on protected fields are denied for restricted roles.
- Full-table source digest comparison against import, on both backends.
- Imported columns are text to preserve original formatting/leading zeros.
- This is a local imported-data workspace. Live PostgreSQL adapters, deployment,
  account recovery and a full scanner benchmark remain future work.
- Field-name/pattern suggestions are not automatic guarantees of PII coverage.
  Keep uncertain fields in Review required. No auto-public classification.

MEDSAFE
- Persistent patient + medication CSV imports in Synthea format, patient search,
  pagination, historical records and active records for a chosen review date.
- Start date inclusive, stop date exclusive, at day granularity. Missing stop
  means no recorded end date, not confirmation of current patient use.
- Five medication date anomalies in the downloaded Synthea sample are retained
  and explicitly excluded from active review, not repaired or discarded.
- Repeated RxNorm-code record detection; optional live NLM RxNorm refresh
  for ingredient identification, with source links, retrieval date and local cache.
- Only medicine codes go to NLM; patient identifiers/history are not transmitted.
- Shared-ingredient flags use cached references no older than 30 days.
- Saved reviewer notes, immutable report snapshots and text report downloads.
- Clinical interaction, renal-dose, pregnancy and allergy checks are NOT yet
  implemented in this working release. No validated clinical rule pack is
  installed. RxNorm is terminology, not a drug-interaction knowledge base.
- A result without overlapping records is not a medication-safety clearance.
- Current user interface is an administrator's local review workspace.
  Broader reviewer account management is a later increment.

STORAGE AND ACCESS
Each app stores its database and signing key in its own .runtime/ directory.
Retain the directory to preserve records, policies and hash stability.
The apps bind only to 127.0.0.1 and use separate session cookies. Passwords
are stored as salted password hashes. Requests require a local-app header,
same-origin checks and a CSRF token for authenticated mutations.
Local database files are not encrypted. Do not expose this local development
server to the Internet; hosted multi-user operation needs additional work.
QA fixtures live separately in .qa/; they are not user workspaces.

PUBLIC DATA SOURCES
UCI Bank Marketing, 45,211 records, 17 CSV columns:
https://archive.ics.uci.edu/dataset/222/bank+marketing
Citation: Moro, S., Rita, P., & Cortez, P. (2014). Bank Marketing [Dataset].
UCI Machine Learning Repository. https://doi.org/10.24432/C5K306
License: CC BY 4.0; attribution required. Unmodified bank-full.csv.
This dataset has financial/demographic fields, not direct customer identifiers.
It is used for scale and financial-field policy tests, not a PII gold standard.

MITRE Synthea April 2020 CSV sample: 1,171 synthetic patients and 42,989
medication records. These are simulated people, not identifiable real patients.
https://synthetichealth.github.io/downloads.html
Citation: Walonoski et al. Synthea: An approach, method, and software mechanism
for generating synthetic patients and the synthetic electronic health care
record. JAMIA 25(3), 2018, 230–238. https://doi.org/10.1093/jamia/ocx079
Provider permits unrestricted use of generated data and requests citation.
Exact download URLs and SHA-256 hashes are in datasets/sources.json.
Retrieved 18 October 2026. Original extracted CSV contents are unchanged.

NLM RxNorm:
https://www.lhncbc.nlm.nih.gov/RxNav/APIs/RxNormAPIs.html
https://www.lhncbc.nlm.nih.gov/RxNav/information/FAQs.html
Live properties and ingredient endpoints were exercised on four public
medicine codes during browser QA. NLM discontinued interaction features
on 2 January 2024; this app does not pretend that endpoint still exists.

VERIFICATION
Run: maskgate-poc/.venv/bin/python local-apps/tests/test_workflows.py
Test summary: tests/results.txt
Checks include cross-role denials, pending-field protection, CSV/export safety,
source integrity, persistent state, invalid imports, dated medication review,
report saving, unavailable network behavior and real public-dataset imports.
Browser QA separately exercised sample loading, policy changes, two-engine
role views, integrity results, patient selection, live reference refresh,
saving a review and downloading its report.

NEXT DEVELOPMENT PRIORITIES
1. Curated, licensed clinical interaction/risk reference with provenance and
   independently labelled validation cases; only then add clinical safety rules.
2. MedSafe name/brand lookup with explicit disambiguation; richer patient
   context imports, review outcomes and reviewer account UI.
3. MaskGate scanner benchmark with independent field labels, policy versioning,
   column selection and an adapter for an existing local database.
4. Account recovery, backups and deployment hardening before online use.

Public data is for development and testing. Organizer-supplied assets and
competition restrictions still need to be checked for the final event.
