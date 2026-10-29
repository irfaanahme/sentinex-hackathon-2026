# Offline hackathon handoff — 29 October 2026

Read [STATE.md](STATE.md) for the current position. This note records the organizer material visible in Irfaan's signed-in InnoSmart portal on 29 October. The organizer's ZIP and PDF were downloaded to `~/Downloads/` on this Mac for private local work; **do not add the dataset, database, SQL dumps or a copy of the pack README to Git or the final code ZIP**.

## Which entry is qualified

- **Problem 11 / B1, MaskGate (`APP-20261017-0267`)** is marked **Qualified / Payable** in My Applications and has phase documents attached.
- **Problem 9 / H4, MedSafe (`APP-20261017-0266`)** still shows **Submitted / Applied**, with no phase documents or completed evaluation round in its application details. The team-level shortlist notification should not be interpreted as qualification for both entries.
- The MaskGate detail page still showed **Payment Required**. It says payment must be completed by the application submitter, after which paid status is shared with team members. Having funds arranged is separate from payment verification.

## Organizer files and verified data

In `My Applications` → filter **Smart Data Masking System for PII Protection** → **View Details** → **Phase Documents**, the portal offers `B1_Smart_Data_Masking_PII_v1_0.zip` and `TalentAP_Participant_Coding_Guidelines_v1_1.pdf` (both added 24 October). The downloaded ZIP is `~/Downloads/phase-20261024130130-B1_Smart_Data_Masking_PII_v1_0.zip`, SHA-256 `cffbc82a5182ac1f1d4cd545bed86b661b99d87bbdd6e66691000350eef0162b`. ZIP CRC and its ready SQLite database's `PRAGMA integrity_check` passed.

The pack is **Saffron Bank**, a fictional synthetic bank. It contains the same nine related tables in CSV, SQLite, PostgreSQL and MySQL forms. The SQLite database has **129,260 rows total**, independently counted:

| Table | Rows | Important fields / challenges |
| --- | ---: | --- |
| branches | 60 | branch contact details; not every phone-like value is private customer PII |
| customers | 5,000 | abbreviated names such as `cust_nm`, `mob_no`, `pita_nm`, address and date of birth |
| kyc_records | 5,400 | PAN/Aadhaar-format fields and `kyc_meta` text/JSON |
| international_customers | 300 | US SSN-format, US address and phone |
| accounts | 8,000 | account numbers, balance, nominee and sparse `extra_info` |
| cards | 6,000 | uppercase field names, card numbers, name on card and limits |
| transactions | 100,000 | account links, amounts, narration and references |
| support_tickets | 3,000 | unstructured ticket text and notes can contain identifiers |
| loan_applications | 1,500 | income, credit score, sparse `col_7` and remarks |

The pack also has nine sample role users in `data/users.csv` (three each for Admin, Support and Analyst). They are example identities, not an authentication system. Its README says all records are synthetic; Indian mobile numbers could still be in service, so never call or message them. The pack has no CVV, PIN, OTP or password. CSV rows were independently parsed and match the advertised counts; text fields include quoted line breaks, so use a CSV parser rather than line counts. A simple digit regex also matches transaction IDs, reference numbers and public branch contacts, so **value shape alone is not a reliable PII label**. The pack provides no gold-standard labels or additional scoring rules; the published problem statement remains the task.

## Coding guidelines v1.1: the material rules

The organizer PDF explicitly allows AI coding assistants, APIs, agents and cloud services. It allows **code written for this hackathon before Day 1**, if declared in the final README. It forbids reusing application code from other hackathons/past projects and copying other teams' code. Thus the older generic six-slide template's apparent no-prebuilt-code restriction is superseded for this event by the specific coding guidelines; disclose this project's advance code honestly.

The final code deliverable is one ZIP named `teamID_psID.zip` made from a clean Git clone, with the team's own `README.md` and all code inside `FULL_CODE/`. BFSI has **no `submission/` prediction file**. Include `.env.example`, schema/migrations, dependency lockfile, meaningful tests, setup/test commands, architecture, AI/prebuilt-code disclosure and limitations. Exclude the organizer pack, database files/SQL dumps, real `.env`, secrets, caches, virtual environments and build output. Run a formatter/linter and dependency audit. The organizers will announce the upload time/flow.

## What the current MaskGate app can and cannot yet show

The existing [`apps/maskgate/`](apps/maskgate/) imports a single CSV at a time into its own SQLite and DuckDB copies, proposes column tags, requires admin approval and masks returned rows for server-side roles. It can theoretically ingest the organizer's CSVs one by one (the largest is 100,000 rows / 16 MB, at its current limits), but this has **not been load-tested** and would duplicate data on the free host. It **does not yet connect to the supplied SQLite database as a target**, preserve the nine-table relationships, or support PostgreSQL/MySQL. Its current scanner depends heavily on generic field names and simple value patterns; it will miss abbreviations (`cust_nm`, `mob_no`, `pan_no`, `col_7`), nested/free-text identifiers and some finance fields unless policies are reviewed. It should not be presented as already satisfying the full official B1 challenge.

The shortest defensible build path is to make the shipped SQLite database the read-only source; add a second genuine backend from the pack (PostgreSQL or MySQL), with matching table/schema scans and a narrow, server-enforced query/view mechanism. Test real role outputs, denial cases, original-table equality and latency on the organizer data. Keep the existing UI where useful, but only claim features demonstrated on this pack. Prepare the L1 solution PPT from the working result, then package a fresh-clone `FULL_CODE/` ZIP under the organizer rules.

## Schedule from the shortlist notification

Report at ANITS before **9:00 AM on 30 October**. Submit a new **solution PPT by 5:30 PM**; L1 jury presentations run **6:00–9:00 PM**. Incorporate feedback and submit final working code by **6:00 AM on 31 October**. L1 shortlist is announced by **9:00 AM**; L2 evaluation is **12:00–2:00 PM**, final presentations **2:00–3:00 PM**, and prize ceremony **3:00–4:00 PM**. The notification does not promise food, accommodation, an offline-only environment or a particular slide template for the new solution PPT; check the portal/on-site instructions rather than relying on assumptions.

## Focused offline B1 build — 29 October 2026

The user narrowed the task to the supplied B1 dataset, exact coding guidelines and a strong, explainable competition demonstration. They confirmed the event machine will be another Mac. A separate local `maskgate-finals/` repository now implements real SQLite and PostgreSQL access to all nine source tables. It includes reviewed role policies, keyed pseudonyms, whole-cell text/JSON protection, read-only source verification and actual measured evidence. It is a new finals build; the older CSV-import SQLite/DuckDB app remains historical.

Final checks passed: 130 Python tests and 10 subtests, frontend lint/format, three dependency audits, 54,190 policy-related assertions and 83 cross-backend comparisons. Scanner development score is 98.75% precision / 100% recall against team-authored labels; branch opening date is one conservative false positive. Initial recall was lower for personal dates; the generic date rule was improved and measured on the same development labels, not a hidden set. All 129,260 rows were unchanged on both backends.

A source security review found rendered Admin query data could survive logout. The browser now discards the document at account transitions and notifies other tabs. Real same-tab Admin-to-Support and cross-tab logout checks passed. Delayed-response/forced-expiry browser races and production concurrency were not simulated. Local files remain unencrypted by the app.

The new L1 deck is in the outer deliverables directory as `MaskGate_B1_FINALS.pptx`; the finals code contains portable Mac setup and a five-minute judge explanation. The other Mac has not been tested yet. The code ZIP must retain .git (explicit organizer checklist) and exclude data/DBs/secrets/dependencies. No finals code has been pushed to the public preparation repository: the user's private-repository preference is pending because rules prohibit sharing code with other teams.

## Judge-facing improvements and offline verification — 29 October 2026

User asked for judge-appreciated improvements, then made extreme offline portability a release requirement. They want the finished product verified before discussing teammate access. Their pasted logistics plan is context, not verified transit/timing evidence. The app is localhost:8785 (not 8501) and uses a restricted query builder, not an arbitrary-SQL AST parser. Keep the README AI/prebuilt disclosure and explain the real architecture.

Finals commit `383f664` adds server-owned field explanations in query and role-comparison results; four live checks (allowed read, raw SQL, supplied-role spoofing, protected-field filtering); and an Admin-only aggregate evidence JSON download. The UI waits for backend loading before accepting queries. Preflight imports and relative runtime paths were fixed for arbitrary launch directories. The existing user account/policy store was preserved.

Verified: 136 Python tests plus 10 subtests, real PostgreSQL included; frontend checks; updated dev dependency audit with no known vulnerabilities; all 54,190 evaluation assertions and 83 cross-backend comparisons, full source equality. Evaluation and final QA server ran under an external-network-denying process sandbox, with localhost allowed; an external TCP probe confirmed the restriction. A separate folder with spaces rebuilt its fresh Python environment from cached wheels only and passed preflight from `/` and the full suite. This reused the already-installed PostgreSQL server; it is not a second-laptop installation test. Real browser checks passed four requests on both backends, per-role explanations and a downloaded/parsed evidence JSON.

Current clean code ZIP: outer `deliverables/TEAM-001130_B1.zip`, 74 files, 262,773 bytes, SHA-256 `9b93a91d3d2f7bac1c07938d3cc22fb899a08bbd2712d43a99cabb26791d8084`. Unpacked archive passed Git fsck, clean checkout and executable-launcher checks; hidden .git retained, data/secrets/dependencies excluded. The PPT retains its earlier dated benchmark snapshot; current report timings differ by run.

Separate local recovery folder: `deliverables/MaskGate_Offline_Recovery_arm64/`, 42 Python runtime/development wheels, about 21.6 MB, requirements, platform notes and SHA256SUMS. Requires already installed Python 3.12 and PostgreSQL 16; contains no official dataset, accounts or keys. It is not a universal/Intel installer and must not go in the code submission. Destination Mac setup, restart and offline rehearsal remain pending. Technical build is verified on this Mac, not universally guaranteed. No finals remote or public push; private-repository choice remains pending.

## Optional Google sign-in — 29 October 2026

User requested Google login and confirmed no Web client ID exists yet. Finals commit `0e327aa` adds optional Google Identity Services login, explicit password-confirmed linking to existing local accounts, unlink/session revocation, and a separate provider sign-in document. Local accounts remain the role authority; unknown Google identities cannot create accounts. Only a keyed hash of the Google subject is persisted, not email/profile/token data. Local login remains fully offline; Google login requires internet and optional ignored `.env` configuration.

Verified 155 tests plus 10 subtests, including real Google token-verifier checks with test signatures and substituted certificate transport; frontend checks and refreshed runtime/development audits passed. The updated 48-wheel Apple Silicon recovery cache (about 26.3 MB) installed into a fresh environment in a path with spaces and passed all tests with external network denied. Live Google account login is not yet verified. Existing user accounts and source data were preserved.

Updated clean-clone `deliverables/TEAM-001130_B1.zip`: 79 files, 291,380 bytes, SHA-256 `488aa786025f0cfe44b29273ad14cea2da04079666b546914260a4ce83d35d25`. Extraction, Git fsck, clean checkout, launcher permissions and exclusion checks passed. Source/ZIP/context are local only, not pushed.

Google Cloud is now accessible after the user's MFA step. Created a dedicated MaskGate project (`pure-object-513112-b4`) to avoid changing existing apps. Consent configuration is prepared in Chrome, external/testing audience; paused at the Google API Services User Data Policy agreement pending explicit user confirmation. No OAuth client exists yet and the main app has no Google client ID. Next: finish approved consent setup, create a localhost Web client, configure ignored `.env`, restart and verify a real Google linking/login round-trip. Never treat unconfigured or mocked-provider tests as proof of live Google login.
