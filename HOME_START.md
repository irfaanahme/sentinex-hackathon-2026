# Continue from home

Repository: https://github.com/irfaanahme/sentinex-hackathon-2026

## First time on your Mac

Open Terminal in the folder where you keep projects:

```sh
git clone https://github.com/irfaanahme/sentinex-hackathon-2026.git
cd sentinex-hackathon-2026
```

Open this folder in Codex or Claude Code. Start with this message:

> Read AGENTS.md, STATE.md, PROJECT_CONTEXT.md and HISTORY.md, then the two selected track contexts. Continue from the recorded next action and verify current organizer rules before using advance code at the finale.

No coding runtime is needed just to read the context or open the Word and PowerPoint files. Public cloning needs no GitHub login; pushing changes requires signing into your GitHub account on the Mac.

## Files to use

- `submissions/*REVIEWED_v2.pptx`: the two submitted seven-slide PPTX copies.
- `demos/`: matching silent, captioned videos.
- `apps/`: current working app code, public/synthetic CSVs, tests and hosting instructions.
- `demo-prototypes/`: earlier prototypes used in the slide videos.
- `Our Hackathon Choices.docx`: the short teammate-facing explanation.
- `Hackathon Decision Report.docx` and `DECISION_REPORT.md`: detailed rationale.
- `references/official/`: selected official requirements and both templates.
- `archive/`: additional downloads, generation sources and historical review outputs.
- `STATE.md`: current status, open questions and exact next step.
- `HISTORY.md`: the dated discussions, choices, revisions and measurements behind the current state.

The verbatim chat transcript is not transferred by Git. Its relevant discussions, decisions and uncertainties are recorded in `HISTORY.md` and the project context files. Original private chat attachments and identity documents are not published.

## Each time you switch machines

Before starting, run `git status`. If clean, use `git pull --ff-only`. If it reports local changes or diverged history, let the agent inspect and integrate them without overwriting work.

Before leaving, ask the agent: "Update STATE.md, review changed files for public sharing, commit the intended files, push, and verify the remote commit." A local save or commit alone does not upload anything. There is no automatic sync.

Keep allotment orders, student IDs, passwords, live databases, session keys and API keys outside the repository. A separate repository may be required at competition kickoff; verify organizer instructions.
