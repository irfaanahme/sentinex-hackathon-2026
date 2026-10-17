# Preparation archive

This directory preserves the useful working material from the office PC's `tmp/` folder. The current submission-ready files are in **`../submissions/`**. Earlier drafts, roundtrips and renderings here are historical checks, not alternative submissions.

- `inspection/`: downloaded public official statements and templates for all 12 problems, extracted text, source URLs, hashes and the download/inspection script.
- `ppt-build/`: proposal generation source, team identity input, earlier candidates, inspection output, validation receipts and rendered slides.
- `ppt-template/` and `roundtrip-render/`: visual template/roundtrip checks.
- `report-render/`: Word-report render checks and PDFs.
- `build_report_docx.py` and `build_simple_report.py`: report generation scripts.

## Reuse on another computer

Existing DOCX/PPTX/PDF/PNG files can be opened without the generation runtime. Run scripts from the repository root. The Python report scripts require `python-docx`; the inspection script requires `pypdf` and network access and re-downloads the public originals. The JavaScript scripts require Codex's `@oai/artifact-tool` package and presentation tooling, which are not bundled in this repository. In `build.mjs`, set `CODEX_PRESENTATIONS_SKILL` to the local presentations skill folder and optionally `CODEX_PYTHON` to its Python executable (default `python3`). Make the artifact-tool package available to Node's package resolver. Create `tmp/ppt-build/` before running these scripts; their intermediate output still goes there. The finalizer may refuse to replace existing submission files, so review its output paths before regeneration.

The copied scripts are preparation utilities, not hackathon application code. They have not been rerun or tested on macOS. Do not interpret archived validation receipts as fresh checks on another machine.

## Archive adjustments and scope

Original files under `tmp/` were left untouched. Download-manifest paths now point to the archived files. Absolute workspace prefixes were normalized, and runtime paths in historical validation receipts were replaced with `${CODEX_NODE_MODULES}` and `${CODEX_NODE_EXECUTABLE}` placeholders. These receipt strings describe prior execution and are not automatic environment-variable expansion. The build script uses explicit runtime environment variables. Other archived binary content is copied unchanged.

Dependency junctions (`node_modules`), caches and bytecode were excluded. A text/OOXML scan found no JWT, GitHub-token, private-key or AWS access-key patterns; the only extracted email was the public organizer address. No student identification or allotment-order documents were present in this archived material. Raw private conversations and browser authentication data are not included.
