# Working MedSafe and MaskGate apps

These are the newer functional apps, separate from `../demo-prototypes/` shown in the submitted slide videos. They are currently hosted for team testing at [MedSafe](https://iamirfaanahmed.pythonanywhere.com/medsafe/) and [MaskGate](https://iamirfaanahmed.pythonanywhere.com/maskgate/). The hosted pages require an owner-created account. No credentials, live database files or session keys are in this repository.

## Run locally

Use Python 3.12 or newer. From the repository root:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r apps/requirements-lock.txt
.venv/bin/python apps/prepare_workspace.py
.venv/bin/python apps/run.py maskgate
```

In another terminal run `.venv/bin/python apps/run.py medsafe`. Open MaskGate at `http://127.0.0.1:8775/` and MedSafe at `http://127.0.0.1:8776/`. Each local workspace asks you to create its first administrator account. The generated databases and signing keys are kept in ignored `.runtime/` folders. On Windows, activate the virtual environment and use its `Scripts/python.exe` in place of `.venv/bin/python`.

`apps/datasets/` contains public UCI Bank Marketing and MITRE Synthea synthetic CSV samples. `sources.json` records download URLs and hashes. The bank data are CC BY 4.0 and require attribution. Synthea data are simulated people; use only public/synthetic records in the hosted test workspace. `fetch_datasets.py` can re-download the samples and verify their hashes.

## What is working

MaskGate imports CSVs into SQLite and DuckDB, suggests field tags, requires administrator policy review, applies server-side Admin/Support/Analyst masking, blocks protected filters and provides role-aware exports, activity and source-integrity checks. MedSafe imports Synthea patient and medication records, supports dated review, repeated-code checks, optional NLM RxNorm ingredient lookup, reviewer notes and report snapshots.

MedSafe does not have a validated drug-interaction, renal-dose, pregnancy or allergy rule pack. MaskGate does not connect to existing external databases or support arbitrary SQL. This is a test deployment, not a clinical device or production data platform. Further detail is in [README.txt](README.txt) and [HOSTING.txt](HOSTING.txt).

## Verify

```sh
.venv/bin/python apps/tests/test_workflows.py
.venv/bin/python apps/tests/test_security.py
```

Before hosting, 16 workflow tests and 19 security/deployment tests passed. The results are in `tests/`. These tests are useful regression checks, not a claim that the apps are bug-free. Hosted basic signed-in flows were checked on 18 October 2026.
