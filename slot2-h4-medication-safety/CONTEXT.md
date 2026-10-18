# Medication Safety context

Selected second entry as of 17 October 2026: **H4 — The Medication Safety Second Pair of Eyes**, portal card 9, `ocps_id=25`, catalog `13`. This replaces H2 as the planned second entry. No application submission is confirmed.

## Required outcome

Given a medication list and basic clinical context, return prioritized safety alerts with issue type, severity, drugs involved, suggested action, confidence and limitations. A clinician decides; absence of detected issues must not be described as proof of safety.

The official statement promises a roughly 500-medicine reference, roughly 2,000 interaction pairs, 5,000 synthetic patient records and hidden labels including 300 seeded near-misses. Assets have not yet been obtained here.

Evaluation includes serious-issue recall, penalties for excessive low-severity alerts, brand/generic matching accuracy and recall on seeded near-misses. See [official statement](../references/official/H4.pdf).

## Proposed approach

Normalize and resolve medicine names first, apply supplied reference rules, then prioritize and explain alerts. Handle interactions, duplicate therapy, renal-dose issues and contraindications within the supplied exercise references. Flag ambiguous matches rather than silently selecting a drug. Keep suggested actions supported by the reference.

Begin with structured/text inputs and one complete patient-to-alert workflow. Do not add handwriting OCR, a live hospital integration or autonomous prescribing. No model or framework is finalized.

## Checks before claiming success

- Measure matching accuracy separately from safety-rule performance.
- Test misspellings, ambiguous names, missing context, duplicate entries and non-issue examples.
- Measure serious-issue detection and unnecessary alerts together.
- Run the supplied harness when available; do not invent results for hidden labels.
- Make limitations understandable to the teammate and evaluator.

## Current working implementation — 18 October 2026

The submitted deck is `../submissions/SENTINEX_Problem_9_REVIEWED_v2.pptx`.
The working code is in `../apps/medsafe/` and the hosted test app is at
https://iamirfaanahmed.pythonanywhere.com/medsafe/ . It imports Synthea
synthetic patient/medication records, reviews active records at a chosen date,
detects repeated codes, optionally refreshes NLM RxNorm ingredient references,
and saves human review notes. Validated interaction, renal, pregnancy and
allergy checks are unavailable because the organizer's reference pack has not
been obtained. Official 300-case near-miss recall is unmeasured. The earlier
approach above is planning history; see [STATE.md](../STATE.md) for current
status. Applicable final-event build restrictions remain unresolved.
