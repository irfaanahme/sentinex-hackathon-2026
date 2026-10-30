# Offline hackathon handoff — current update 30 October 2026

## Current release on 30 October 2026

The ready-to-transfer finals source is the separate private `maskgate-finals` repository at `238aac1`. It uses real SQLite/PostgreSQL on the organizer's 129,260 synthetic records. Local demo accounts and reviewed policies are prepared; Google sign-in is removed. The full suite passed 158 tests plus 10 subtests. The exact private kit passed fresh installation, repeat setup, database restart and three-role HTTP checks with external internet blocked on the development Apple Silicon Mac. Windows/Intel compatibility and dependency checks passed, but actual execution on those machines remains to be rehearsed.

Use [STATE.md](STATE.md) for current release files and remaining work, and [MASKGATE_EXPLAINED.md](MASKGATE_EXPLAINED.md) to understand the application. The public `apps/` code and hosted links are older implementations. Finals source, organizer data, credentials and the private transfer kit remain outside this public repository. Earlier sections below are dated history and may describe steps that are now complete.

## 30 October 2026 — fully offline authentication release

The user chose local-only authentication for the offline event. Removed Google sign-in, its routes/interface/configuration and Google-specific dependencies from finals MaskGate. Existing local accounts, keys and source databases were preserved; the unused external Cloud client was not deleted. No Google setup or linking is pending.

Finals source is committed locally as `a96c422` in the separate `maskgate-finals` repository, with no remote. A fresh offline runtime install passed real three-role workflows on both databases, 54,190 evaluation assertions, 83 backend comparisons and full source equality. A fresh offline development install passed **140 tests plus 10 subtests**; the decrease retires provider-specific tests. Frontend checks and runtime/development dependency audits passed. Both Mac caches now include all 42 pinned runtime/development wheels; Intel resolved offline but actual Intel execution remains unverified.

Rebuilt the code-only `deliverables/TEAM-001130_B1.zip` and the separate private transfer kit, including updated setup instructions and checksum manifests. The kit is for the team only, not portal code upload or public sharing. Python 3.12/PostgreSQL 16 must be installed beforehand. Actual destination-Mac reboot/offline rehearsal and live workspace policy/account preparation remain pending. Saved locally; no public push.

## Latest verified portal changes — 30 October

The signed-in MaskGate application now shows **Qualified / Paid**. The 29 October payment notification confirms INR 1,003 received. The earlier unpaid status below is historical. Private payment references are intentionally omitted.

The phase documents are still the 24 October B1 dataset ZIP and Coding Guidelines v1.1. The competition's Documents tab still links the Round 1 template; its Timeline and five FAQs add no newer technical or final-deck requirements. The live Problem 11 description still requires header/sample scanning, role-based dynamic masking, two actual databases and an interactive demonstration preserving raw tables. No new final-upload control was visible in the application detail during this check.

The 29 October update directs participants to the [Participant Quest Map](https://innosmart.in/ics/2026/MegaHackathon-Oct26/ParticipantsQuestMap/). The expanded page was saved in `references/official/ParticipantsQuestMap-2026-10-30.txt`. It explicitly calls its schedule **tentative**:

| Time | Latest plan |
|---|---|
| 30 Oct 08:00–09:30 | Registration. Latest notification asks arrival 09:00–09:30; arriving before 09:00 also meets the earlier shortlist notice. |
| 09:30–10:15; 10:30 | Orientation, then hackathon starts. Confirm upload URLs/formats and the retained 17:30 PPT deadline. |
| 18:00–21:00 | Stage 1 functional evaluation, 25 points: completeness, each member's actual contribution and readiness/confidence. |
| 31 Oct 06:00 | Code freeze: one ZIP, no code changes afterward. |
| 06:00–09:00 | Stage 2 automated code analysis, 25 points. BFSI receives all 25 here; the other domains split model evaluation/code analysis. No B1 prediction file. |
| Around 09:00 | Approximately 40 teams shortlisted on the first 50 points. |
| 09:00–09:30; 09:30–11:30 | Briefing, then shortlisted teams record a three-minute sales-and-product video. |
| 11:30–13:30 | Stage 3 video judging, 25 points; top 15 ranked on 75 points. |
| 13:45–14:00; 14:00–15:00 | Briefing, then Stage 4 jury questions only, about four minutes per team, 25 points. |
| 15:00–16:00 | Prizes and wrap-up. |

The Quest Map does **not explicitly cancel** the earlier 30 October 17:30 PPT deadline. Keep that deadline until orientation clarifies it. The exact code-analysis rubric and grader internals are not published. A rehearsal script is now in the finals judge guide; a required final-stage video has not been recorded or submitted. Do not reuse the old Round 1 clip as evidence of the finals build.

The update also confirms teams of two to four, participation certificates on 31 October evening, and team-leader contact with the secretariat for missing/replacement members. Bus support mentioned is for KIET/KITS; no transport booking or accommodation is confirmed for this team.

## Historical handoff — 29 October 2026

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

## Historical comparison of the earlier app before the finals build

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

Google setup continuation: user explicitly approved the API Services User Data Policy; agreement accepted and Google confirmed OAuth configuration created. The Web client form is now prepared as MaskGate Local with origins http://localhost, http://localhost:8785, http://127.0.0.1 and http://127.0.0.1:8785, no redirect URI. Paused immediately before Create for action-time confirmation of credential creation. No client credentials have been created; local app configuration remains unchanged.

Google client created with explicit approval: MaskGate Local, project pure-object-513112-b4, public client ID 857061841969-26l42sv2o1n10fmkcd7a442uv036bpvu.apps.googleusercontent.com. Registered the four prepared localhost/127.0.0.1 origins. No billing activated, client secret not copied/stored. Ignored local configuration updated and app restarted on port 8785. Chrome loaded the real Google SDK button without warnings/errors and opened Google's MaskGate account chooser successfully. User must complete password-confirmed My account → Link Google account; successful linked login remains unverified. Fresh Chrome handoff is open at localhost:8785/#account.

Current finals evidence commit ebd4794; clean-clone ZIP rebuilt and extraction/Git/executable checks passed: 79 files, 292112 bytes, SHA-256 6e18af3abbb651bfffcfd74747335a1c271095d4a81e7a96569a6f13b720ffa0. Code unchanged from the 155-test implementation checkpoint. Severe disk pressure blocked first packaging; under prior cleanup authorization, removed only regenerable npm/pip download caches (~624 MB). Preserved offline wheel cache, programs and personal files; about 745 MiB free immediately afterward. Local-only context/source commits; no push.

## Readiness and organizer recheck — 30 October 2026

The signed-in MaskGate application is now Qualified / Paid. Read all 13 notifications, phase documents, competition overview/documents/timeline/FAQs/current B1 text, public event page and all 13 expanded Participant Quest Map sections. Same official B1 pack and Coding Guidelines v1.1; no new final-upload control was visible. The new tentative plan has four 25-point stages: functional, BFSI code analysis, a three-minute sales/product video, then four-minute jury Q&A. Code freezes at 06:00 on 31 October. Retain the earlier 17:30 PPT deadline until organizers clarify. See OFFLINE_FINALS.md and the saved Quest Map text for exact schedule and source limits. Payment identifiers were not copied.

After reboot, the private PostgreSQL server was stopped; restarted successfully. Fixed setup retry so optional Google/client-port settings and comments survive; fixed the check runner to redact configured credentials from failure output. Regression checks pass: 158 Python tests + 10 subtests, frontend checks and fresh dependency audits with no known vulnerabilities reported. Commit 84d2172 contains these code fixes; release 9cedf27 adds dated installation/evaluation evidence and a requirement-to-evidence map plus the new video/Q&A rehearsal.

A clean source clone in a folder with spaces created a fresh cache-only Python environment and a NEW private PostgreSQL cluster, imported the official organizer data, passed preflight/tests/evaluation with external network denied, and restarted its database through the launcher. An external TCP probe confirmed the restriction. All 54,190 assertions and 83 backend comparisons passed; source equality covered all 129,260 rows on each backend. Scanner precision 98.75%, recall 100% on the same development labels. Existing Python/PostgreSQL binaries were reused: this is not proof of destination-Mac installation, Intel compatibility or a complete macOS reboot. Original workspace/accounts/keys/configuration were preserved and its app is running at localhost:8785.

Latest source-only ZIP is outer deliverables/TEAM-001130_B1.zip (81 files, 306574 bytes), commit 9cedf27, SHA-256 9eda3ad3d8ad82f5b20e0324d79b649303dc66fe91a0fac0d72feef69104b976. Extraction, Git fsck, clean exact commit, launcher permissions and exclusions passed; all 105 reachable history blobs were checked for current private credentials without printing them. Yesterday's ZIP is preserved under deliverables/previous-releases. Separate private transfer kit contains this source ZIP, the official organizer pack and matching arm64 wheels plus START_HERE; never submit or publish the whole transfer kit. Python 3.12/PostgreSQL 16 must be installed separately before offline use.

Remaining: actual other-Mac architecture/availability and reboot/offline rehearsal; optional live Google linking/login (user asked to complete personal account prompts); orientation-specific portal/format changes. The 29 October PPT is still a dated verified-build snapshot. No final-stage video recorded/submitted, no final upload, no finals public push. A saved file/local commit is not remote sync.

Read-only live-workspace readiness check: one active Admin account, zero linked Google accounts, and no saved policy/baseline documents. Existing real-account/browser verification used isolated QA workspaces; do not present those as proof the user’s current workspace is already configured. User sign-in and live demo account/policy/baseline preparation remain necessary before the event walkthrough.

## Additional Mac portability check — 30 October 2026

The pinned cryptography 50.0.2 distribution has macOS arm64 wheels but no Intel wheel, verified from https://pypi.org/pypi/cryptography/50.0.2/json. A full binary-only Intel dependency download failed at that package. The earlier advice to simply install the full pinned set online on Intel was incomplete: an Intel Google-enabled build needs separate compiler/dependency preparation and verification.

Finals commit 3a3d824 splits the existing local banking pins into requirements-local.txt, included by the unchanged-version full Google requirements. All banking workflows remain available with local login and the Google client ID unset. A fresh minimal environment with Google, cryptography and requests absent passed real owner/Support/Analyst account flows, preapproval blocking, scan/review, role masks, denied requests, source integrity and logout against both actual sources; the evaluator passed all 54,190 assertions and 83 backend comparisons with external network denied. Upgrading that environment from the arm64 cache to full development/Google dependencies then passed all 158 tests + 10 subtests. No dependency version was downgraded.

Downloaded a separate 10-wheel Intel local-runtime cache. Its pinned requirements resolve entirely offline for CPython 3.12/macOS 14 x86_64. This is resolver/archive verification, NOT execution on Intel hardware. It excludes Google login and development tools. Full arm64 cache and matching requirements/manifests were refreshed. The private transfer kit now includes both caches, corrected architecture-specific instructions, the code ZIP and dated PPT/PDF. Actual other-Mac setup, reboot/offline rehearsal and live workspace sign-in/configuration still remain.

Current source-only ZIP: TEAM-001130_B1.zip, commit 3a3d824, 83 files, 312137 bytes, SHA-256 92b3313b32d511db28c368820f1125e610ef53aeec0aebf07bad56d16c4d3d70. Extraction, hidden Git/history, clean exact HEAD, executable launcher, exclusions and credential scan over all 111 history blobs passed. Prior 9cedf27 ZIP was preserved under previous-releases. No source or private transfer material was published.
