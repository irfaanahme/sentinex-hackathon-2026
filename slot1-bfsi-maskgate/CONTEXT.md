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
