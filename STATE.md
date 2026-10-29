# Current project state

Updated: 29 October 2026, Asia/Kolkata.
Team SENTINEX (TEAM-001130); **MaskGate / Problem 11 is the confirmed qualified offline entry**. See [OFFLINE_FINALS.md](OFFLINE_FINALS.md) for the organizer dataset, coding rules, schedule and readiness gaps.
The full decision and revision trail is in [HISTORY.md](HISTORY.md).

## Completed

- Both entries were submitted. MaskGate `APP-20261017-0267` now shows **Qualified / Payable**; MedSafe `APP-20261017-0266` still shows **Submitted / Applied** in the portal.
- The official B1 Saffron Bank ZIP and participant coding guidelines v1.1 were downloaded privately on 29 October. The ZIP's nine-table SQLite database passed integrity checks and contains 129,260 synthetic rows. The pack also supplies PostgreSQL, MySQL and CSV forms; do not commit the pack/data.
- The submitted seven-slide PPTX copies are `submissions/*REVIEWED_v2.pptx`. Slide 7 links to silent, captioned videos in `demos/` and Google Drive.
- `apps/` contains the newer working MedSafe and MaskGate code, tests and public/synthetic samples. The earlier video prototypes are in `demo-prototypes/`.
- Hosted test workspaces: https://iamirfaanahmed.pythonanywhere.com/medsafe/ and https://iamirfaanahmed.pythonanywhere.com/maskgate/ . Both signed-in basic workflows were checked on 18 October.
- Before hosting, 16 workflow and 19 security/deployment tests passed. See `apps/tests/`. This is not proof of zero bugs or clinical/production certification.

## Current limits

- MedSafe reconciles records and optionally resolves ingredients through NLM RxNorm. Validated interaction, renal-dose, pregnancy and allergy rules are not installed.
- MaskGate uses SQLite and DuckDB on imported CSVs with administrator-reviewed policies. It does not yet connect to an existing PostgreSQL/MySQL server.
- Hosting is a shared test workspace with plaintext-at-rest database files; use public/synthetic records only. PythonAnywhere free hosting requires monthly renewal, next due 18 November 2026.
- Coding guidelines v1.1 allow AI tools and code written for this hackathon before Day 1, with explicit disclosure; they require a fresh-clone `FULL_CODE/` ZIP and exclude organizer data/DB dumps. The existing MaskGate app does not yet connect to the supplied database or preserve its related tables; do not claim full B1 compliance.
- H4 reference packs/hidden labels have not been obtained, so official hidden-set performance is unmeasured.
- InnoSmart shows 105 applications across all 12 problems; per-problem counts and other applicants' decks are unavailable through the participant view.

## Next actions

1. Confirm the MaskGate payment status with the submitting teammate; portal still says Payment Required. Report before 9:00 AM on 30 October.
2. Build/test MaskGate against the official B1 database with two actual backends and a role-policy matrix; keep originals intact. Use the organizer data only locally.
3. Prepare a **new** L1 solution PPT by 5:30 PM on 30 October and a compliant final code ZIP by 6:00 AM on 31 October. Preserve the Round 1 decks as history.

## Sync

Check `git status`, `git log` and `origin/main` to confirm this update was pushed. A saved file is not a sync.
