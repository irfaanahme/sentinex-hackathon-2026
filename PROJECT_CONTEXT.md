# Project context

## Purpose and working entries

Prepare a credible, practical hackathon entry that the team can build, explain and demonstrate. Irfaan values tangible outcomes and reusable skills or artifacts; prize money and opportunities are possible benefits, not guarantees.

| Entry | Official problem | Portal identity | Working name | Decision status |
| --- | --- | --- | --- | --- |
| Primary | Smart Data Masking System for PII Protection | Card 11, `ocps_id=27` | MaskGate | Working selection in the supplied conversation |
| Second | The Medication Safety Second Pair of Eyes | H4, card 9, `ocps_id=25` | Not yet named | Selected by user on 17 October; application not confirmed |

The teammate suggested H4 and R2 Returns Fraud (`ocps_id=2`). Independent review favored H4 over the earlier H2 choice because supplied reference-based checks offer a more controlled verification path than bilingual medical rewriting. H2 is now a backup; R2 is an alternative, not an active project. See `DECISION_REPORT.md`. Do not confuse card numbers with API IDs. Catalog `13` maps to competition `1` in the captured JSON.

## People and workflow

Team identity confirmed from the user's portal screenshot on 17 October: **SENTINEX**, team code **TEAM-001130**, owner **Aswini Lakshya**, members **Irfaan Ahmed** and **Aswini Lakshya**. The PPT covers use Aswini as team leader.

- Irfaan expects to contribute at least two hours per day and use Codex and Claude Code extensively. Explain technical choices rather than assuming manual coding expertise.
- The teammate introduced the event and is less comfortable with technical detail. The conversation names her Aswini Lakshya and describes her as the portal lead; confirm the actual registered roster and lead before submission.
- Suggested division: Irfaan coordinates technical design and implementation; the teammate can own problem understanding, requirements checks, presentation rehearsal and demo testing. Agree these responsibilities together.
- Devices: office Windows 10 PC and home Mac mini M2. The user accepted GitHub for syncing both project files and context; the user requested a public repository, now being published as irfaanahme/sentinex-hackathon-2026. First clone on the Mac remains to be verified.
- The user's preferred AI roles are Gemini for broad planning, Claude for architecture, and Codex for execution. Keep one shared project record and short handoffs.
- Communicate simply and briefly. The user authorized both proposal decks and public GitHub synchronization. Application implementation is not yet authorized to begin.

## Event facts checked on 17 October

The official public page states: applications close **18 October 2026**, AI screening is **20 October**, shortlists are due **21 October**, and the final event is **30–31 October at ANITS College, Visakhapatnam**. The exact application cutoff time is unspecified. Teams have 2–4 current students from AP-based colleges; each student belongs to one team. Teams may apply to 1–2 problems using the official PPT template. Applying is free; shortlisted-team fees are ₹1,000 for member institutions or ₹2,000 for non-members. The total prize pool is ₹10 lakh; individual award amounts are unconfirmed. [Official event page](https://innosmart.in/ics/2026/MegaHackathon-Oct26/)

## Rules that need clarification

Update on 17 October: the user chose the seven-slide template because it is linked under Problems 9 and 11 and authorized preparing both proposals. Two editable SENTINEX decks now exist in `submissions/`. This choice resolves our submission-format decision, not the separate event build restrictions discussed below. The user reports that applications require PPTs and allotment orders, and that they received advice to use an allotment order instead of a student ID. The advice source is unconfirmed. No upload has occurred.

The files linked to BFSI 11 and H2 use the same seven-slide PPTX. R3 links to a different six-slide template whose instructions include PDF export, CPU-only work, organizer-provided data/models, no pre-built code, and a repository created at kickoff. Its cover includes BFSI as well as Retail and Healthcare. It cannot safely be dismissed as an unrelated track rule.

Ask which template and restrictions govern each chosen entry. Also verify upload format, size limit, demo expectations and deadline time. The conversation repeatedly mentions PPT/PPTX under 5 MB; treat that as a reported constraint until the live application form or organizer confirms it. Do not invent a hybrid template or claim an exemption based on document numbering.

Planning documentation can proceed now. Keep this preparation repository distinct from any competition implementation repository required to be created at kickoff, subject to organizer clarification. Avoid starting project code on the assumption that pre-building is permitted.

## Current decisions and open choices

| Item | Current position | What resolves it |
| --- | --- | --- |
| Project selection | BFSI 11 plus H4 selected | Final names and actual application status |
| MaskGate stack | PostgreSQL and SQLite proposed; Python possible | Small architecture decision after rules clarification |
| H4 reference assets | Promised by the statement, not obtained | Organizer distribution of data, rules and evaluation assets |
| Git sync | GitHub preferred | Public remote requested by user; reviewed commit, verified push and first Mac clone |
| Submission | Two reviewed seven-slide PPTX proposals in submissions/; portal upload pending | Correct template, accurate content, reviewed export and submission receipt |
| Prototype | No application code or measurements recorded here | Authorized build at the permitted time, followed by evidence-based checks |
| Competition popularity | Per-problem counts unknown | Optional official aggregate figures; no delay to preparation |

See [sources and corrections](references/SOURCES.md) before reusing claims from earlier AI conversations.

