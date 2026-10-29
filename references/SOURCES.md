# Sources and corrections

Evidence snapshot: 17 October 2026. Official requirements take priority over assistant interpretations. Written organizer clarification should be added here with its date and scope when received.

## Source register

| Source | What it supports | Limit |
| --- | --- | --- |
| [Official event page](https://innosmart.in/ics/2026/MegaHackathon-Oct26/) | Deadline, timeline, eligibility, fees, prize pool, AI screening and official-template requirement; rechecked on 17 October | No private grading prompt, exact cutoff time or prize breakdown |
| [Authenticated portal](https://app.innosmart.in/rp/competitions/13) | Prior read-only inspection of cards and document links | Portal content can change; registration/submission state is not confirmed here |
| [Official document manifest](official/manifest.json) | URLs and SHA-256 hashes for the two chosen statements and conflicting templates | Hashes establish file identity, not rule precedence |
| [BFSI 11 statement](official/BFSI11-statement.txt) | Required scanner, masking, two backends and demo | Extracted text; retain original PDF for exact layout |
| [H2 statement](official/H2-statement.txt) | Required care-plan outputs, faithfulness and promised assets | Descriptions of supplied assets are not the assets themselves |
| [Shared seven-slide template](official/shared-template.txt) and [six-slide R3 template](official/R3-template.txt) | Concrete template differences and restrictive declaration | Applicability conflict unresolved |
| Supplied Gemini conversation | User preferences and history of candidate designs | Export lacks reliable role labels in places; assistant claims and suggested follow-ups are not authoritative decisions |
| Supplied authenticated problem-list JSON | 12 records, IDs, document references and eligibility configuration | Not a competition-detail response and not an applicant registry |

Original conversation: user-supplied Gemini chat export (private attachment; decisions summarized in project context).

Original JSON: user-supplied authenticated competition problem-list response (private attachment; findings summarized below).

Full original downloads and earlier inspection outputs are preserved in `archive/inspection/`. Selected official files are copied under `references/official/` for portable context. The long chat and authenticated response are not copied into the shared repository.

## Findings to preserve

- The captured problem-list response contains no per-problem application, submission, team or view counts. Missing fields mean unknown, not zero.
- `applicant_types` describes eligibility, not the people who applied. Its `weightage: 1.0` fields are eligibility configuration, not a judging rubric.
- A prior portal snapshot displayed 105 total applications. That is a dated aggregate, not unique teams or a per-problem distribution.
- All 12 statement PDFs differ. Eleven PPTX downloads have identical content; R3 has a distinct six-slide template. There were 24 linked documents, matching one PDF and one PPTX per problem.
- The inspected response has no problem-level `created_at` or `updated_at`; document timestamps and uploader account IDs do not establish problem author or sponsor.

## Claims not established by the evidence

- Exact grader model, prompt, parser, weights, video capability or a guaranteed score from wording.
- Fewer competitors in BFSI 11, rival skill levels, win probabilities or guaranteed shortlisting.
- Different sponsor ownership or exemption from shared rules inferred from larger problem IDs.
- BFSI 11 being judged exclusively by humans. Its statement gives functional deliverables without a numeric metric; the public Round 1 announcement still says AI screening.
- A verified MaskGate prototype, execution transcript, sub-5 ms latency, 99% precision or zero leakage. These appeared in draft suggestions without measured evidence.
- Guaranteed internships, contracts, college attendance exemption, IP rights, market-size claims or regulatory compliance.

Prepare persuasive submissions by clearly connecting requirements, design and actual evidence. Do not describe invented results as tests or try to instruct the evaluator through hidden content. Any demo simulation or mockup must be labeled honestly.


## 30 October 2026 portal recheck

- [Signed-in application detail](https://app.innosmart.in/rp/applications): MaskGate Qualified / Paid; same B1 dataset and v1.1 guidelines added 24 October. No new final-upload control visible during review. Payment transaction identifiers were not copied.
- [Notifications](https://app.innosmart.in/rp/notifications): 29 October update, paid confirmation and earlier PPT/code deadlines read. Treat generic dashboard progress as weaker than the specific application status.
- [Participant Quest Map](https://innosmart.in/ics/2026/MegaHackathon-Oct26/ParticipantsQuestMap/): all 13 sections expanded. Saved rendered text in [the dated snapshot](official/ParticipantsQuestMap-2026-10-30.txt). Tentative four-stage 25-point route, 06:00 code freeze, new three-minute video round and four-minute final Q&A. No exact code-analysis rubric supplied.
- [Competition details](https://app.innosmart.in/rp/competitions/13): read Overview, Documents, Timeline, FAQs and current B1 description. General Documents still contains only the Round 1 template. 573 is the total across 12 problems, not the MaskGate competitor count.
- [Public event page](https://innosmart.in/ics/2026/MegaHackathon-Oct26/): read current event details; accommodation contact availability does not confirm a reservation.

The current state and newer schedule are summarized at the top of OFFLINE_FINALS.md; earlier sections remain dated history.
