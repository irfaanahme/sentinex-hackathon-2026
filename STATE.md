# Current project state

Updated: 29 October 2026, Asia/Kolkata.
Team SENTINEX (TEAM-001130); MaskGate / Problem 11 / offline B1 is the confirmed qualified entry. MedSafe remains submitted/applied, not confirmed qualified.

## Finals build completed locally

- A separate Git repository, `maskgate-finals/` beside this preparation checkout, contains the focused finals implementation. All code is under FULL_CODE; this public preparation repository does not contain the finals code.
- Uses the official 9-table, 120-field, 129,260-row bank pack with real SQLite and PostgreSQL readers. Organizer data stays ignored and outside the code ZIP.
- Working scanner, reviewed policies, server-owned roles, query/role comparison with field explanations, bounded masked CSV, four live access checks, source fingerprints, metadata audit and downloadable aggregate evidence.
- Final check: 155 Python tests and 10 subtests passed, including actual PostgreSQL permissions; Python and frontend lint/format passed; runtime/development/frontend dependency audits found no known vulnerabilities.
- Development benchmark: 98.75% precision, 100% recall (one conservative branch-date false positive); 54,190/54,190 policy-related assertions and 83/83 backend checks passed. All source rows unchanged. Team labels, not organizer ground truth or blind testing.
- A security review found prior Admin results could remain after logout; fixed by document replacement and cross-tab account-change notification. Real same-tab and cross-tab browser regressions passed. This is not a universal security guarantee.
- New seven-slide L1 PPT: outer deliverables/MaskGate_B1_FINALS.pptx, with PDF preview. Old Round 1 PPTs/videos remain historical.
- Clean-clone package: outer deliverables/TEAM-001130_B1.zip; finals commit `0e327aa`. Fresh cached-only dependency installation and checks passed in a path containing spaces, with external network denied. ZIP retains hidden .git and passed extraction/Git checks.
- Matching Apple Silicon offline recovery cache is separate in outer deliverables/MaskGate_Offline_Recovery_arm64 (48 wheels, 26.3 MB). Python 3.12/PostgreSQL 16 must already be installed; this is not a universal installer. Another-Mac rehearsal remains pending.

- Optional Google login code is saved/tested; local login stays offline. Google Cloud MaskGate project created; consent policy accepted with permission. Localhost Web client form prepared; credential creation awaits action-time confirmation. No client ID/live Google login yet. Continue Chrome, configure and test real linking/login.

## Rules and remaining actions

- Guidelines v1.1 permit same-hackathon prebuilt code and AI assistance with README disclosure. All code must be FULL_CODE; fresh-clone ZIP must KEEP hidden .git and exclude organizer data, secrets and installed dependencies. BFSI has no submission/ prediction file.
- The guidelines forbid sharing code with other teams. Finals remote publication is pending the user's private-repository choice; do not push finals source into the existing public repository.
- Confirm payment with the submitting teammate; last portal check said Payment Required. Report before 9 AM on 30 October.
- Transfer the clean finals code and obtain the official pack separately on the other Mac. Install once with internet, then preflight, tests and a full offline rehearsal.
- New L1 PPT due 5:30 PM on 30 October; final code due 6 AM on 31 October. Check any later portal/on-site instructions and regenerate the ZIP after on-site changes.

## Local security and sync

Finals is loopback-only; local files are not encrypted by the app. No live credentials or datasets belong in Git. The prepared ZIP includes source and history, not runtime accounts.
This context update and finals work are local until a private-remote decision is completed. A saved file or local commit is not remote sync.
