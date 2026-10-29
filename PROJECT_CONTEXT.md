# SENTINEX project context

Updated 29 October 2026. Read [STATE.md](STATE.md) first, [OFFLINE_FINALS.md](OFFLINE_FINALS.md) for the newly supplied B1 dataset and rules, and [HISTORY.md](HISTORY.md) for the path from selection through submission, demos, apps and hosting. This is the portable public handoff; never put passwords or identity documents here.

## Team, event and applications

SENTINEX (TEAM-001130): portal team owner and PPT leader Aswini Lakshya; members Aswini Lakshya and Irfaan Ahmed.

| Entry | Portal identity | Product | Application |
| --- | --- | --- | --- |
| H4 Medication Safety Second Pair of Eyes | Card 9, `ocps_id=25` | MedSafe | `APP-20261017-0266`, SUBMITTED |
| Smart Data Masking System for PII Protection | Card 11, `ocps_id=27` | MaskGate | `APP-20261017-0267`, SUBMITTED |

The signed-in InnoSmart participant portal confirmed both statuses on 18 October. It shows 105 applications across all 12 problem statements, not counts for these entries. It does not offer other teams' decks. Public search found two related code projects but no verifiable same-problem competitor PPTX: [Medi-Shield](https://github.com/TanishNain/medi-shield) and [FormGuard](https://github.com/mdmehtabalam83098-hue/Smart-Data-Masking-System-for-PII-Protection). Neither is confirmed as an InnoSmart entry.

On 29 October the live portal marked **MaskGate qualified/payable** and attached the official B1 pack and coding guidelines; MedSafe remained submitted/applied without phase documents. The organizer's new guidelines permit pre-developed code written for this hackathon and AI tools when disclosed. The old six-slide-template uncertainty is superseded for this event; see [OFFLINE_FINALS.md](OFFLINE_FINALS.md) for the exact submission structure and schedule. The portal still showed payment required for MaskGate.

## Submitted decks and demos

The uploaded copies are `submissions/SENTINEX_Problem_9_REVIEWED_v2.pptx` and `submissions/SENTINEX_Problem_11_REVIEWED_v2.pptx`. Both are seven-slide PPTX files based on the template linked under their statements. Package, font, layout and rendered-slide checks passed before submission. The two older named proposals in `submissions/` are historical.

Slide 7 links to corresponding Google Drive demos. The final MP4 files are also in `demos/`: MedSafe 54 seconds and MaskGate 52 seconds, 1440×900 H.264, with burned-in captions/highlights and no audio. Google Drive access was set to Anyone with the link / Viewer; signed-out playback was not separately checked. Preserve the uploaded decks; later repository edits will not change the organizer's copies.

## Working apps

`apps/` is the newer functional codebase, distinct from `demo-prototypes/` used in the slide videos. The hosted test workspaces share one PythonAnywhere site at `/medsafe/` and `/maskgate/`. Basic signed-in patient review and Admin data query worked on 18 October. Public/synthetic samples were imported; no real patient or customer records were uploaded.

- **MaskGate:** import CSVs into SQLite and DuckDB; scan field names/samples, require administrator review, apply server-side Admin/Support/Analyst policies, paginate/query/export masked views, deny protected filters, log activity and compare source integrity. It does not attach to an existing external database, implement arbitrary SQL rewriting or prove universal PII detection.
- **MedSafe:** import Synthea patient/medication CSVs, search patients, review records at a date, flag repeated codes and shared ingredients when current NLM RxNorm ingredient references exist, and save notes/report snapshots. Clinical interaction, renal-dose, pregnancy and allergy checks remain unavailable without validated references. A clear screen is not a safety clearance.
- **Security:** hosted mode disables public owner bootstrap, uses server sessions with revocation, request budgets, CSRF/origin checks, HTTPS cookies and restrictive browser policy. This is a test deployment with plaintext-at-rest records and a shared team workspace, not end-to-end encryption or production certification. Do not upload real sensitive data.

The public data in `apps/datasets/` are UCI Bank Marketing (45,211 records, CC BY 4.0) and MITRE Synthea April 2020 synthetic patients (1,171) and medications (42,989). Source URLs, attribution and SHA-256 hashes are recorded in `apps/datasets/sources.json` and `apps/README.txt`. The bank set has no direct customer identifiers and is not a PII scanner gold standard. Synthea includes five source medication rows whose stop predates start; they are retained and excluded from active review.

Local verification before deployment: 16 workflow tests and 19 security/deployment tests passed; an exact dependency audit reported no known vulnerabilities at the time. Hosted public endpoints and asset paths loaded, unauthenticated data endpoints returned 401, and signed-in MedSafe review and MaskGate Admin query worked. These checks do not establish zero bugs, safety effectiveness or Apple-equivalent privacy. Test summaries are in `apps/tests/`.

PythonAnywhere Beginner free hosting has one web worker, limited storage/CPU and monthly web-app expiry; the current renewal date is 18 November 2026. See `apps/HOSTING.txt` and [apps/README.md](apps/README.md) for operation. Use only public/synthetic samples.

## Next technical work

Obtain the official H4 medicine/interaction reference, 5,000 patients and hidden-label evaluation harness if distributed. Implement clinical rules only with validated provenance; report serious-issue recall, alert burden, name matching and 300 near-misses honestly. For MaskGate, independently label a scanner benchmark, version policies and add a connector to an existing database if final rules permit. Verify organizer restrictions before treating advance code as a final-round entry.

Keep `sources/` in the surrounding ChatGPT project read-only. Keep credentials, allotment orders, ID scans, live databases, session keys and dependency caches outside this public repository. Fetch and integrate remote work before editing from another computer; commit and push deliberately.

## Focused offline B1 build — 29 October 2026

The user narrowed the task to the supplied B1 dataset, exact coding guidelines and a strong, explainable competition demonstration. They confirmed the event machine will be another Mac. A separate local `maskgate-finals/` repository now implements real SQLite and PostgreSQL access to all nine source tables. It includes reviewed role policies, keyed pseudonyms, whole-cell text/JSON protection, read-only source verification and actual measured evidence. It is a new finals build; the older CSV-import SQLite/DuckDB app remains historical.

Final checks passed: 130 Python tests and 10 subtests, frontend lint/format, three dependency audits, 54,190 policy-related assertions and 83 cross-backend comparisons. Scanner development score is 98.75% precision / 100% recall against team-authored labels; branch opening date is one conservative false positive. Initial recall was lower for personal dates; the generic date rule was improved and measured on the same development labels, not a hidden set. All 129,260 rows were unchanged on both backends.

A source security review found rendered Admin query data could survive logout. The browser now discards the document at account transitions and notifies other tabs. Real same-tab Admin-to-Support and cross-tab logout checks passed. Delayed-response/forced-expiry browser races and production concurrency were not simulated. Local files remain unencrypted by the app.

The new L1 deck is in the outer deliverables directory as `MaskGate_B1_FINALS.pptx`; the finals code contains portable Mac setup and a five-minute judge explanation. The other Mac has not been tested yet. The code ZIP must retain .git (explicit organizer checklist) and exclude data/DBs/secrets/dependencies. No finals code has been pushed to the public preparation repository: the user's private-repository preference is pending because rules prohibit sharing code with other teams.

Final local checkpoint: finals commit `bfbca4b`, clean working tree. `deliverables/TEAM-001130_B1.zip` was made from a fresh clone, retains .git, contains 72 files (~245 KB) and passed archive integrity/exclusion checks. SHA-256: `d2c1312a676cb9af7840c1ff4d4efe71352b985c91d55c91006020a8239df440`. A new Python environment plus a clean frontend dependency install passed all checks in a temporary clone with spaces in its path. User app starts at localhost:8785 with first-owner setup; the separately tested QA workspace used port8786. No finals remote has been configured or pushed while private-repository choice is pending.

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
