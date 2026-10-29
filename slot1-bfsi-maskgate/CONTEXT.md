# MaskGate context

Working name: MaskGate. Official title: **Smart Data Masking System for PII Protection**, portal card 11, `ocps_id=27`, catalog `13`. The source PDF itself says “Problem Statement 1”; use the full title and portal identity to avoid ambiguity.

Plain explanation: show sensitive database values differently depending on the user's authorized role, while preserving the original records.

## Official deliverables

| Requirement | Evidence to demonstrate |
| --- | --- |
| Scan column names and sample values automatically | Detect and tag sensitive fields, including examples such as `PII_HIGH` and `FINANCIAL_CONFIDENTIAL` |
| Support at least two database backends | Run the same policy examples against two real backends |
| Apply dynamic role-based masking | Admin full view, Support partial masking, Analyst redaction or hashes, according to a documented policy |
| Preserve underlying data | Before/after checks show raw source values remain unchanged |
| Provide an interactive demonstration | CLI, API/Postman or a small dashboard lets evaluators compare role-specific results |

Regex/rules and query interception or view logic are explicitly allowed. An LLM, arbitrary SQL support, a production authentication platform and a polished web frontend are not stated requirements. See [official statement](../references/official/BFSI11-statement.txt).

## Proposed minimal scope

Use PostgreSQL and SQLite, a small synthetic customer dataset, an automatic scanner, one policy configuration and a simple demo. Python is a candidate; framework and UI choices remain open.

Before implementation, decide whether supported queries are fixed templates, restricted selections or a wider SQL subset. Enforce roles on the server; a role selector is a controlled demo mechanism, not proof that users cannot grant themselves privileges. Unsupported query forms should be rejected explicitly. Client-side blurring alone does not meet the masking requirement.

## Verification plan

- Label expected sensitive and non-sensitive columns, including misleading names and empty or mixed samples. Report detection precision and recall on that defined test set.
- Compare actual values against expected results for each role, field and backend.
- Test direct endpoint requests, unauthorized role changes and unsupported query forms within the chosen scope.
- If aliases, joins, functions or filters are supported, test their effects on disclosure. Output masking alone does not establish protection against all inference through queries.
- Check database values before and after masking and keep sensitive values out of logs.
- Measure latency with a stated dataset, query set, machine and baseline. No accuracy or latency target is a measured result yet.

## Deferred choices

Arbitrary SQL lineage, audit hash chains, streaming, a third backend and enterprise compliance claims are outside the proposed minimum. Do not claim production readiness, universal SQL safety, zero leakage or regulatory certification from a hackathon demo.

## Current working implementation — 18 October 2026

The submitted deck is `../submissions/SENTINEX_Problem_11_REVIEWED_v2.pptx`.
The working code is in `../apps/maskgate/`, with SQLite and DuckDB as the two
real backends. It supports administrator-reviewed field policies, server-side
roles, masked query/export, denied protected filters and source-integrity
verification on imported CSVs. UCI Bank Marketing and MITRE Synthea are public
or synthetic samples, not an independently labelled scanner benchmark.
The hosted test app is at
https://iamirfaanahmed.pythonanywhere.com/maskgate/ .
PostgreSQL and arbitrary SQL interception remain proposed, not implemented.
The earlier scope above records planning history; see [STATE.md](../STATE.md)
for the current handoff. Applicable final-event build restrictions remain
unresolved.

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
