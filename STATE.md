# Current project state

Updated: 18 October 2026, Asia/Kolkata.
Team SENTINEX (TEAM-001130); entries: Problem 9/H4 MedSafe and Problem 11 MaskGate.
The full decision and revision trail is in [HISTORY.md](HISTORY.md).

## Completed

- Both InnoSmart applications show SUBMITTED: H4 `APP-20261017-0266`; data masking `APP-20261017-0267`.
- The submitted seven-slide PPTX copies are `submissions/*REVIEWED_v2.pptx`. Slide 7 links to silent, captioned videos in `demos/` and Google Drive.
- `apps/` contains the newer working MedSafe and MaskGate code, tests and public/synthetic samples. The earlier video prototypes are in `demo-prototypes/`.
- Hosted test workspaces: https://iamirfaanahmed.pythonanywhere.com/medsafe/ and https://iamirfaanahmed.pythonanywhere.com/maskgate/ . Both signed-in basic workflows were checked on 18 October.
- Before hosting, 16 workflow and 19 security/deployment tests passed. See `apps/tests/`. This is not proof of zero bugs or clinical/production certification.

## Current limits

- MedSafe reconciles records and optionally resolves ingredients through NLM RxNorm. Validated interaction, renal-dose, pregnancy and allergy rules are not installed.
- MaskGate uses SQLite and DuckDB on imported CSVs with administrator-reviewed policies. It does not yet connect to an existing PostgreSQL/MySQL server.
- Hosting is a shared test workspace with plaintext-at-rest database files; use public/synthetic records only. PythonAnywhere free hosting requires monthly renewal, next due 18 November 2026.
- Organizer rules on pre-built code, supplied assets and kickoff repositories remain unresolved. H4 reference packs/hidden labels have not been obtained, so official hidden-set performance is unmeasured.
- InnoSmart shows 105 applications across all 12 problems; per-problem counts and other applicants' decks are unavailable through the participant view.

## Next actions

1. Verify organizer rules before presenting prebuilt app code as a final-round entry.
2. If official assets arrive, test against them and report measured results; do not infer hidden-set performance from demos.
3. Preserve the submitted decks and video links. Treat later edits as new versions.

## Sync

Check `git status`, `git log` and `origin/main` to confirm this update was pushed. A saved file is not a sync.
