# Understand and demonstrate MaskGate

MaskGate is SENTINEX's qualified Problem 11 entry, called B1 in the offline round. It lets different bank employees receive different versions of the same stored information. The original records stay unchanged. This guide explains the finals application, how to demonstrate it, and the claims the team can defend. Status: 30 October 2026; finals source checkpoint `238aac1`.

The finals implementation is kept separately from this public preparation repository. The `apps/` folder and PythonAnywhere links here belong to the earlier round. They are not the current SQLite/PostgreSQL finals release. Use the private transfer kit for the finals app and [STATE.md](STATE.md) for current status.

## The problem in everyday terms

Imagine a bank employee helping someone with a card issue. The employee may need to identify the right card without seeing the complete card number, the customer's address or financial balances. Giving every employee full database access exposes information they do not need.

MaskGate puts an application-controlled access layer in front of the data. An administrator chooses and approves field classifications. The application then applies a predefined transformation for each role; the current interface is not a custom per-role rule editor. The same stored record produces different permitted responses when different accounts request it. This is **dynamic data masking**: values are transformed when the application returns a result, rather than permanently replacing the stored originals.

**PII** means personally identifiable information: details that identify or relate to a person, such as a name, phone number, address or government identifier. Financial details such as balances are protected too, even though their category differs from an identifier.

## An example to remember

The following is an invented illustration, not a row copied from the organizer data. The token is shortened for readability.

| Field | Admin receives | Support receives | Analyst receives |
|---|---|---|---|
| Card number | `4111111111111234` | `••••1234` | `hmac:card:…` |
| Name | Asha Rao | `[REDACTED]` | `[REDACTED]` |
| Credit limit | 50000 | `[REDACTED]` | `[REDACTED]` |
| Approved card status | ACTIVE | ACTIVE | ACTIVE |

The roles have different responsibilities:

- **Admin:** can inspect originals, scan fields, approve policies, manage accounts and preview all three roles.
- **Support:** can run permitted queries and export the masked results; selected identifiers show their last four characters, while names and financial values are hidden.
- **Analyst:** receives stable coded identifiers where the policy permits them, with other sensitive fields hidden. The current app does not add aggregation or a full analytics platform.

For email addresses, Support receives only the first mailbox character followed by `***@***`; the original domain is hidden.

A stable token lets someone recognize that two occurrences represent the same kind of identifier without receiving the original value. Its technical name is an **HMAC pseudonym**, made using a private key. It is not guaranteed anonymity: records remain linkable, and someone possessing the key can reproduce tokens. Tokens are consistent within the same installation and key; new laptop installations generate different keys.

## Where the data came from

The organizer supplied the fictional **Saffron Bank** dataset. We did not generate thousands of customer records ourselves or scrape a real bank. It contains **129,260 synthetic rows, nine tables and 120 fields**. A row is one record; a field is one column such as a name or card number. These are not 129,260 unique customers.

| Table | Records | What it represents |
|---|---:|---|
| customers | 5,000 | Customer identities and contact details |
| accounts | 8,000 | Accounts, balances and related details |
| cards | 6,000 | Cards and credit information |
| transactions | 100,000 | Financial activity |
| branches | 60 | Bank branch directory |
| kyc_records | 5,400 | Identity verification details |
| international_customers | 300 | International identity/contact fields |
| loan_applications | 1,500 | Applications and financial details |
| support_tickets | 3,000 | Customer support text and notes |

The same logical dataset is prepared in two actual database systems. **SQLite** stores its database in a local file. **PostgreSQL** runs as a local database server. The selector chooses which system MaskGate reads. This demonstrates the same access policy across two database engines; it is not two unrelated datasets or automatic replication between them.

## The six stages of the application

1. **Sign in.** The server verifies the local username and password, then looks up that account's role. Typing a different role into a request does not change permissions.
2. **Inspect and scan.** The scanner reads column names, data types and up to 512 nonempty values per field. It proposes a classification and explains its reasoning.
3. **Review.** An Admin checks the proposals, changes mistakes and approves the policy separately for each database. A proposal alone does not authorize restricted access.
4. **Request data.** The user chooses a table, columns, a bounded page and an allowed filter. The server checks these options before reading the source.
5. **Mask the response.** The Python application transforms the result according to the saved policy and authenticated role, before sending it to the browser. The browser does not receive the forbidden originals and merely cover them with CSS.
6. **Check and record.** Source fingerprints check whether the underlying records changed. Activity records describe operations, and an evidence view presents dated evaluation results and current workspace metadata.

The important path is:

`Browser → account and permission checks → permitted database read → masking → browser result`

The source database and the account/policy workspace are separate. MaskGate can save users, policies and audit activity without modifying customer records.

## How the scanner makes decisions

The scanner is **local rules and pattern matching**, not an AI model trained on bank records. AI helped develop the software, but the running scanner calls no AI service.

It recognizes meaningful headers, including abbreviations such as `cust_nm` and `mob_no`, and looks for patterns in sampled values. This also helps with unclear column names such as `col_7`. A suspicious value can cause the whole column to be protected. Unknown evidence requires review rather than automatically becoming public.

The classifications are `PII_HIGH`, `FINANCIAL_CONFIDENTIAL`, `PUBLIC` and `REVIEW`. Once approved, a PUBLIC field is returned unchanged to all three application roles. The PUBLIC tag and approval are separate decisions; neither authorizes publishing the whole dataset online. Restricted roles receive `[BLOCKED]` for unapproved or REVIEW fields. Admin can still inspect originals to make the review decision.

The displayed Rule strength is a heuristic indication of the rule evidence, not a calibrated probability or the measured scanner accuracy. Admin approval is a trust boundary: incorrectly approving a sensitive field as PUBLIC would expose it to restricted users.

Context matters. A bank's branch-directory phone can be a public business contact, while a customer's phone is personal information. The scanner also conservatively flags a branch opening date as sensitive; the team's reviewed policy changes that field to PUBLIC. This is a useful example of why human review remains necessary.

Support notes and JSON are hidden as entire cells for restricted roles. Removing one recognizable number would not prove that the remaining text contains no names or unexpected identifiers. The application accepts reduced usefulness in exchange for a clear protection rule.

The transfer setup loads the team's explicitly reviewed policy for the supplied dataset so a fresh installation is ready to demonstrate. This is a disclosed setup convenience. It is separate from automatic scanner performance and does not mean the scanner approves itself.

## What the screens are for

| Screen | Your purpose when demonstrating it |
|---|---|
| Overview | Establish the actual dataset, selected engine and current policy version. |
| Inspect data | Show the catalogue, proposed classifications and reasons. |
| Policy review | Show the Admin's decision and explain a correction. |
| Query workspace | Run the same permitted request, compare role outputs as Admin, and show field explanations. |
| Protection checks | Show one valid read succeeding and three forbidden requests being rejected. |
| Source integrity | Compare the current complete source with its recorded baseline. |
| Evidence | Explain measured results and their scope; downloading evidence does not rerun every test. |
| Activity | Inspect metadata about actions, rather than a log containing copies of customer records. |

The role comparison is an **Admin-only preview**. To prove actual authorization, log out and sign in as the real Support or Analyst account. Two ordinary browser tabs share the same session, so they are not independent role logins.

## Languages and code map

| Technology | What it does here |
|---|---|
| Python 3.12 | Server logic, scanner, masking, authentication, database access, setup and tests |
| Flask | Python framework that receives browser requests and returns pages/data |
| HTML | Page structure and controls |
| CSS | Layout, colours and typography |
| JavaScript | Browser interactions, requests and displaying results |
| SQL | Database schema and controlled reads in SQLite/PostgreSQL |
| Mac and Windows launchers | Start the matching local setup and application |

Node.js is needed for frontend maintenance checks, not to run the prepared app. Google login was removed so authentication can work offline. After setup, the interface assets and both database engines run locally.

In the private finals checkout, look inside `FULL_CODE/`:

| File or folder | One sentence you should be able to explain |
|---|---|
| `main.py` | Starts the local application. |
| `maskgate/web.py` | Connects browser API requests to the appropriate operations. |
| `maskgate/auth.py` | Checks identity, sessions and server-owned permissions. |
| `maskgate/scanner.py` | Proposes field classifications using headers, types and samples. |
| `maskgate/service.py` | Coordinates the request, saved policy, database read and masking. |
| `maskgate/masking.py` | Decides and applies the permitted transformation to each value. |
| `maskgate/adapters.py` | Reads SQLite/PostgreSQL safely and calculates source fingerprints. |
| `maskgate/store.py` | Saves local users, policies, sessions and audit information separately. |
| `templates/` and `static/` | Implement the browser interface. |
| `scripts/evaluate.py` and `tests/` | Produce measurements and check expected/forbidden behavior. |

These paths describe the private finals code. They are not links into the older public `apps/` implementation.

## What protects the data

The app reads source SQLite in read-only mode. PostgreSQL uses a SELECT-only application account and read-only transactions. The request interface accepts known tables/columns and bounded options, with parameterized filter values. Protected-field filtering is refused because repeated guesses can reveal information even when the displayed column is masked.

Passwords are stored as password hashes in the account database. Sessions can be revoked; the role is resolved from the server-side account. State-changing requests have cross-site request protections and request limits. Logout clears displayed results so the next account does not inherit the earlier account's view.

The separately generated demonstration password file is intentionally readable by the laptop owner for rehearsal. It stays in ignored private runtime files and is absent from the transfer/source ZIPs. It is not a claim that every local file is encrypted.

A **source fingerprint** is a digest computed from the ordered source contents. Recording a baseline, running operations, then obtaining the same digest is evidence that those contents stayed unchanged during that check. Merely creating the first baseline is not proof of a before-and-after comparison.

This release does not encrypt the databases or secret files at rest. Someone controlling the laptop's operating-system account can reach files outside the app. Masking is enforced by the Python application. It does not automatically protect an independent connection made directly to the original database. Restricting direct database/file access is a deployment responsibility. The app is bound to the local computer, not deployed as an internet-facing bank service. It has no universal security, legal-compliance or production-load certification.

## What the numbers mean

| Evidence from the development release | Meaning |
|---|---|
| 158 tests plus 10 subtests passed | Program checks passed, including actual PostgreSQL integration; not a promise that no bugs exist. |
| 54,190 assertions passed | Many individual expected-value, denial and integrity checks passed; not 54,190 distinct user workflows. |
| 83 backend comparisons passed | The evaluator checked outputs across the two real engines. |
| 98.75% scanner precision | Of 80 sensitive flags, 79 matched the team's development labels and one was a conservative extra flag. |
| 100% scanner recall | It found all 79 sensitive fields in those labels; not proof it finds all sensitive information in any future dataset. |
| Source equality passed | All 129,260 rows in each backend were covered by before/after logical fingerprints. |

Full-source integrity checks cover every row; role-output evaluation samples pages at the beginning, middle and end of each table.

The labels are team-authored development labels. Rules were improved using this dataset; these are not hidden organizer test results or an independent blind benchmark. The scanner can miss a rare pattern outside its bounded sample. HMAC tokens remain linkable, and PUBLIC fields can permit inference when combined.

The exact transfer ZIP passed fresh setup, repeat setup, database restart, app startup and three-role HTTP checks on the development Apple Silicon Mac with external network access blocked. Windows/Intel dependencies were checked and packaged, but those operating-system/hardware combinations still need their own run. A full destination-laptop restart/offline rehearsal remains the team's next practical check.

## A five minute demonstration

1. **Overview:** “This is the organizer's synthetic bank: nine tables and 129,260 records.”
2. **Inspect and Policy review:** Explain a customer identifier, the unclear `col_7` field and the reviewed branch-date false positive.
3. **Cards query:** As Admin, compare `CARD_NO`, `NAME_ON_CARD`, `CREDIT_LIMIT` and a public status across the three role previews. Expand the explanations.
4. **Real Support login:** Log out, sign in as Support and run the request. Show the protection checks: a valid read succeeds; raw SQL, supplied Admin role and protected-field guessing are refused.
5. **Second engine and integrity:** Repeat relevant results on PostgreSQL, then use Admin to verify source equality and explain Evidence.

The query interface is a controlled query builder. Do not call it a general SQL editor or an arbitrary-SQL AST parser. The ordinary Analyst view offers pseudonymized identifiers, not a full statistics dashboard.

A suitable opening is: “Bank staff need useful data without receiving every personal detail. MaskGate scans sensitive fields, lets an administrator review the policy, and returns role-appropriate results across SQLite and PostgreSQL while preserving the original records.”

## How to become comfortable explaining it

Start with actions rather than memorizing source files. Sign in as each role and predict what the same card query should return before running it. Explain why a name is hidden, why a card's last four digits can remain, and why Analyst tokens differ from anonymity. Then run a rejected request and explain who made the permission decision.

Next, trace one request through `web.py`, `auth.py`, `service.py`, `adapters.py` and `masking.py`. You do not need every line memorized. You should be able to say what each layer receives, decides and returns. Finally, explain one scanner mistake and the limits of the test results without hiding them.

AI assistance and same-hackathon advance work are disclosed in the finals README. Describe actual contributions accurately: what you specified, inspected, tested, changed and demonstrated. Do not say you independently wrote a module unless you did. Understanding the design and verifying behavior is work you can begin doing now; a presentation assignment alone is not evidence of authorship.

## Files and remaining event work

- **Public GitHub repository:** preparation history, older submissions/apps and this current explanation. It is not the full finals runtime backup.
- **Private transfer kit:** code ZIP, authorized organizer pack, offline dependencies, prerequisites and Setup/Start/View logins shortcuts for teammates. Extract it and follow the matching Mac/Windows setup.
- **Code submission ZIP:** clean finals source and required Git history; excludes data, passwords, runtime files and dependencies. This is the source deliverable, not the large transfer kit.
- **Finals PPT/PDF:** currently the dated 29 October snapshot; refresh screenshots/details where permitted before submission. Earlier Round 1 videos show the earlier prototype.

The current app opens at `http://127.0.0.1:8785/` on the computer running it. Sending that address to a friend does not share your computer's server; they run their own transferred copy. Mac setup requires Python 3.12/PostgreSQL 16 beforehand. Windows prerequisites are included; its Microsoft runtime installer may need administrator approval. Each new installation generates private demo credentials, accessible through View logins.

Read [OFFLINE_FINALS.md](OFFLINE_FINALS.md) for the dated organizer instructions and tentative schedule. Reconfirm requirements at orientation; distinguish today's personal 06:00 preparation target from the organizer's **31 October 06:00 code freeze**. The destination-device rehearsal, refreshed presentation material and required final-stage recording/submission are separate from completing the application package.
