# CareSetu context

Status: backup only. On 17 October 2026 the user selected Problems 9 and 11 for the decision report; H4 replaces H2 as the planned second entry. The material below is retained for reference, not active implementation.

Working name: CareSetu. Official problem: **H2 — Discharge Summary to Patient-Understandable Care Plan**, portal card 7, `ocps_id=7`, catalog `13`.

Plain explanation: turn a supplied discharge summary into readable home-care instructions without changing or inventing medical instructions.

## Official deliverables

- Structured care plan covering medicines, warning signs, diet/activity guidance and follow-up appointments, preserving what the source actually says.
- English plus one Indian language, with the same faithfulness requirements for both.
- Reported readability score, aiming roughly at Class 8 reading level.
- A one-page fridge sheet.

The statement promises 2,000 synthetic summaries, a glossary, a drug reference, 50 reference rewrites and an evaluation harness. Those assets have not been obtained in this workspace. Dropped medications, changed doses and invented instructions receive hard penalties; fluency is secondary to faithfulness. Audio and a seven-day timetable are stretch features. See [official statement](../references/official/H2-statement.txt).

## Proposed minimal scope

Start with text summaries, extract the source facts into a structured representation, simplify only the explanation, and compare the final output against the source. English plus Telugu is proposed, subject to the team's ability to review both. Do not add a warning, dose or recommendation simply because it seems medically plausible.

Choose the model, runtime and translation method after clarifying allowed models and CPU constraints. Avoid expanding into diagnosis, prescribing, patient records integration or scanned-document OCR unless explicitly required later.

## Verification plan

- Preserve medicine, dose, frequency, duration and dates, including multiple medications and unusual formatting.
- Check omissions and additions separately in each language and in the fridge sheet.
- Flag ambiguous or unparseable instructions instead of silently guessing.
- Report readable-output quality separately from factual preservation; a readability score does not establish safety.
- Run the organizer harness when supplied and retain actual results. Human review must cover translated critical instructions.

The exact dataset, evaluation code, model access, template and build timing are unresolved. Do not call this a clinically validated product or promise a shortlist result.
