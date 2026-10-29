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
