# SENTINEX — Talent AP Mega Hackathon 2026

**Current focus: MaskGate, Problem 11 / offline B1.** The entry was confirmed **Qualified / Paid** in the participant portal on 30 October 2026. MedSafe's offline qualification is not confirmed.

Start with **[Understand and demonstrate MaskGate](MASKGATE_EXPLAINED.md)** for the problem, a simple example, the app's screens, architecture, measurements and a five-minute walkthrough. Read **[STATE.md](STATE.md)** for the latest release and next actions.

The finals application uses the organizer's synthetic Saffron Bank dataset: **129,260 rows, nine tables, 120 fields, real SQLite and PostgreSQL**. It scans fields, supports administrator-reviewed policies, enforces Admin/Support/Analyst access and masks results while preserving the originals. It runs locally with offline sign-in. The 30 October release passed 158 tests plus 10 subtests and an offline rehearsal of the exact transfer ZIP on the development Apple Silicon Mac. Windows and Intel Mac execution still need checking on those machines.

**This public repository contains preparation history, the current explanation and earlier implementations. The private finals source (`238aac1`), organizer dataset and transfer kit are not published here.** The event's code-sharing restrictions are the reason for keeping the finals implementation separate. Cloning this public repository does not install the current finals app; teammates should use the private Mac/Windows transfer kit and its Setup, View logins and Start launchers.

## Earlier Round 1 work

| Problem | Product | Submitted deck | Earlier hosted test app |
| --- | --- | --- | --- |
| 9 / H4 — Medication Safety Second Pair of Eyes | MedSafe | [PPTX](submissions/SENTINEX_Problem_9_REVIEWED_v2.pptx) | [Earlier app](https://iamirfaanahmed.pythonanywhere.com/medsafe/) |
| 11 — Smart Data Masking System for PII Protection | MaskGate | [PPTX](submissions/SENTINEX_Problem_11_REVIEWED_v2.pptx) | [Earlier app](https://iamirfaanahmed.pythonanywhere.com/maskgate/) |

Both Round 1 applications were submitted in October. Those decks link to [silent, captioned videos](demos/) of the earlier [prototypes](demo-prototypes/). The public [apps/](apps/) implementation and hosted MaskGate link predate the finals SQLite/PostgreSQL build. Hosted availability has not been rechecked in this documentation update. MedSafe is not a clinically validated decision system.

## Project records

- [Beginner explanation and rehearsal](MASKGATE_EXPLAINED.md)
- [Current status and release](STATE.md)
- [Offline event requirements and dated organizer updates](OFFLINE_FINALS.md)
- [Project context](PROJECT_CONTEXT.md) and [discussion and decision history](HISTORY.md)
- [Continue on another computer](HOME_START.md)
- [Official references](references/official/) and [source notes](references/SOURCES.md)

Older proposals and working archives remain in `archive/`. Dated historical notes can describe superseded states; use STATE.md first. Passwords, live databases, keys, private IDs and dependency caches remain outside this public repository. AI assistance and work prepared for this same hackathon are disclosed; measurements are development evidence, not promised judging scores or universal security guarantees.
