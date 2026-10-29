# Current project state

Updated: 30 October 2026, Asia/Kolkata.
SENTINEX TEAM-001130: MaskGate / Problem 11 / offline B1 is Qualified / Paid, verified in the signed-in portal. MedSafe is not confirmed qualified.

## Verified finals build

- Focused finals source is the separate local `maskgate-finals/` Git repository, commit `9cedf27`; no remote configured or public push. All submitted code is under FULL_CODE.
- Official synthetic bank: 9 tables, 120 fields, 129,260 rows; real SQLite and PostgreSQL. Organizer data is excluded from the source ZIP.
- Scanner, reviewed policies, server-owned roles, masked queries/CSV, role comparison, field explanations, four live protection checks, source fingerprints, audit and downloadable evidence work.
- 30 October: 158 Python tests + 10 subtests passed, including actual PostgreSQL tests. Frontend checks passed. Python runtime/development and frontend dependency audits reported no known vulnerabilities.
- Fresh clone in a path with spaces: new Python environment from cached wheels, NEW private PostgreSQL cluster and official import, preflight, tests and evaluation all passed with external network denied. Launcher restarted the stopped database and served the app. Original workspace was restored.
- Evaluation: 54,190/54,190 assertions, 83/83 backend comparisons, all source rows unchanged; scanner precision 98.75%, recall 100% against team-authored development labels, with one conservative branch-date false positive. Not an organizer/blind benchmark.
- Source ZIP: outer `deliverables/TEAM-001130_B1.zip`, 81 files, 306,574 bytes; SHA-256 `9eda3ad3d8ad82f5b20e0324d79b649303dc66fe91a0fac0d72feef69104b976`. Extraction, Git fsck/clean status, exact HEAD, no remotes, executable launcher, exclusions and current-credential scan over all 105 history blobs passed.
- Separate PRIVATE transfer kit: outer `deliverables/MaskGate_Private_Mac_Transfer_2026-10-30.zip`, containing source ZIP, official pack, arm64 Python wheels and START_HERE. Do NOT upload the kit as code. Python 3.12/PostgreSQL 16 are prerequisites; Intel needs matching wheels.
- Local app is running at http://127.0.0.1:8785/. Existing account/key files were preserved. Live workspace has one Admin, no Support/Analyst accounts, no saved policies or integrity baselines; prepare these after user sign-in. App files are not encrypted at rest; it is loopback-only, not a production bank perimeter.
- Optional Google client is configured and provider button/chooser verified. No completed live linking/login round trip is confirmed. User was asked to finish My account → Link Google account personally; local login works offline.
- Seven-slide `deliverables/MaskGate_B1_FINALS.pptx` remains the dated 29 October build snapshot. Old Round 1 videos/PPTs are historical; a new finals video has not been recorded.

## New organizer requirements

- Read all notifications, application phase documents, competition Overview/Documents/Timeline/FAQs/B1 description, public event page and all 13 Quest Map sections. Same v1.1 guidelines/B1 pack; general Documents still has Round 1 template. No new final-upload control visible.
- Tentative Quest Map: functional 25 points (30 Oct 18–21), BFSI code analysis 25 (31 Oct 06–09), three-minute sales/product video 25 (record 09:30–11:30 after briefing), final jury Q&A 25 (~four minutes/team, 14–15).
- Code freeze 31 Oct 06:00: one ZIP, no code changes afterward. Keep earlier 30 Oct 17:30 PPT deadline until orientation clarifies; the new plan did not explicitly cancel it.
- Paid confirmation received; latest notification says arrive 09:00–09:30, Quest Map registration 08:00–09:30. Earlier arrival before 09:00 remains compatible. No travel/accommodation booking confirmed.
- Guidelines permit same-hackathon advance code and AI assistance with disclosure. Retain .git, exclude data/secrets/dependencies. BFSI has no prediction file. Do not share finals code with other teams.

## Remaining gates / exact next step

1. Confirm whether the actual destination Mac is Apple Silicon or Intel and available. Transfer privately, install prerequisites while online, then reboot and rehearse offline on THAT Mac. The current Mac rehearsal does not prove the other device works.
2. User signs in to prepare live reviewed policies, integrity baselines and real Support/Analyst accounts. Complete optional personal Google account linking and a real sign-out/sign-in check, or explicitly defer it for the offline event.
3. At orientation confirm PPT format/upload URL, schedule and final code/video submission instructions. Rebuild source ZIP after permitted code changes; freeze by the organizer deadline.

Context and code are saved locally, not remotely synced. The public preparation repository intentionally excludes finals source and the private transfer kit. See OFFLINE_FINALS.md and references/SOURCES.md for dated official evidence.
