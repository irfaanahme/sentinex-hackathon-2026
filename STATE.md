# Current project state

Updated: 30 October 2026, Asia/Kolkata.
SENTINEX TEAM-001130: MaskGate / Problem 11 / offline B1 is Qualified / Paid. MedSafe is not confirmed qualified.

Start with [MASKGATE_EXPLAINED.md](MASKGATE_EXPLAINED.md) to understand and rehearse the project.

## Current finished transfer release

- Finals source: separate local `maskgate-finals/` Git repository, commit `238aac1`; clean checkout, no remote/public push. All submitted code is under FULL_CODE.
- Official synthetic bank: 9 tables, 120 fields, 129,260 rows on real SQLite and PostgreSQL. No organizer data in the source ZIP.
- Working scanner/review, server-owned roles, masked queries/CSV, role comparison, explanations, denied requests, fingerprints, audit and evidence.
- Current full checks: 158 tests + 10 subtests, actual PostgreSQL integration, lint/format pass. Browser Support and Analyst sign-ins/results verified; all three demo accounts pass actual HTTP login/query/role/logout checks on both backends.
- Evaluation: 54,190/54,190 assertions, 83/83 backend comparisons, source rows unchanged; scanner precision 98.75%, recall 100% against team-authored development labels (not organizer/blind grading).
- Setup creates private per-installation demo_admin/Admin, demo_support/Support, demo_analyst/Analyst accounts and explicitly team-reviewed demo policies. Existing owner/passwords/policies/keys/baselines preserved. Credentials stay in ignored .runtime/demo-credentials.json; use View logins launcher.
- Code ZIP: outer `deliverables/TEAM-001130_B1.zip`, 99 files, 372,387 bytes; SHA-256 dc90691a54e7805e2f4cfc7b6105ea6f1e7d580802b335b32dea178238aa43cb. Extraction, exact HEAD, Git fsck, exclusions and actual-credential history scan passed.
- PRIVATE all-platform kit: outer `deliverables/MaskGate_Private_Transfer_2026-10-30.zip`, 495,805,771 bytes. Includes source, organizer pack, Mac arm64/Intel + Windows x64 caches, Windows prerequisites, Setup/Start/View logins shortcuts and dated slides. Do NOT upload this kit as source or public Git.
- Cache closure/hashes passed: 42 wheels per Mac architecture and 44 Windows wheels. All 44 Windows Python packages advisory-audited with none skipped/no known vulnerabilities; not a runtime-binary audit.
- Windows bundled Python 3.12.10/PostgreSQL 16.15; VC++ installer may require admin approval. Mac Python 3.12/PostgreSQL 16 must be installed before going offline. Windows and Intel Mac hardware execution remain unverified.
- Fresh Apple Silicon setup and repeat passed with external network denied; new private PostgreSQL cluster/data/accounts. Exact final packaged-ZIP extraction/setup/repeat/start/three-role HTTP rehearsal also passed; source remained clean. Result: outer `deliverables/MaskGate_Final_Kit_Rehearsal.json`.
- Live app: http://127.0.0.1:8785/. Local-only accounts, no Google login. App does not encrypt files at rest and is not a production bank perimeter.
- Existing seven-slide finals PPT/PDF remain a dated 29 October snapshot. Old Round 1 decks/videos are historical; finals video not recorded yet.

## Organizer requirements

- Portal notifications, phase docs, event pages and all 13 Quest Map sections reviewed. Same v1.1 guidelines/B1 pack; no new final-upload control visible at last check.
- Tentative scoring: functional 25 (30 Oct 18–21), BFSI code 25 (31 Oct 06–09), three-minute sales/product video 25 (record 09:30–11:30), jury Q&A 25 (~four minutes/team,14–15).
- Code freeze 31 Oct 06:00: one clean ZIP retaining .git; no data/secrets/dependencies. No BFSI prediction file. No code changes afterward.
- Keep 30 Oct 17:30 PPT deadline until orientation clarifies. Confirm portal, format and schedule on arrival. Registration before09:00 remains compatible with latest arrival information.
- Same-hackathon advance code and disclosed AI assistance permitted. Do not share finals source with other teams.

## Next on each teammate laptop

1. Copy/extract the private kit; run matching Setup, View logins and Start launchers. User's other Mac is available/Apple Silicon; friends use Intel Windows PCs. Do not copy live environments/accounts/databases.
2. Restart THAT laptop, disconnect internet, demonstrate both backends and real roles, rejected requests and source equality. Current-Mac tests do not prove destination execution.
3. Refresh permitted screenshots/slides, confirm organizer requirements at orientation, rebuild source ZIP after on-site changes and obey code freeze.

This public update contains current context and the beginner guide; finals source and the private kit stay separate and private. See OFFLINE_FINALS.md and references/SOURCES.md for official evidence.
