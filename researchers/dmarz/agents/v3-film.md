---
agent: dmarz/v3-film
tool: claude-code
state: working  # working | idle | blocked | done
task: null
doing: explainer film for the finished v3 qualification run v3-q0-a1 (reads the run's records only; no model calls, no edits to bench_v3)
updated: 2026-10-04T03:50Z
---

## Notes

Film source is `researchers/dmarz/notes/discussion-dose/src/film_v3/` (build_data.py, build.py, film.html, record.mjs).
It reads a finished, audited run directory and refuses a partial one. The run's post-mortem stays with
dmarz/discussion-bench-v3; the film only shows what `summary.json` and `episodes.json` already report.
