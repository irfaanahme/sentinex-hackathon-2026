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
