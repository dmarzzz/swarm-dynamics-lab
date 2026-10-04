---
agent: dmarz/market-split-film
tool: claude-code
state: done  # working | idle | blocked | done
task: null
doing: filed the explainer film for the finished Sonnet market-split pilot s1-002 (reads the filed records only; no model calls, no edits to market-split-api or market-split-opus)
updated: 2026-10-04T08:45Z
---

## Notes

Film source is `researchers/dmarz/notes/market-split-film/` (`_decision.md`, `build_data.py`, `build.py`, `film.html`).
It reuses the recorder and the repo QR code from `researchers/dmarz/notes/discussion-dose/src/film_v3/`. The look is
read from the brand kit at build time and is not copied into this repo.

Artifact `market-split-film` v1 covers the Sonnet pilot only. The Opus 5.5 replication (`market-split-opus`) was
mid-run when v1 was made. When its results and post-mortem are published, extend `build_data.py` to read its records
and file v2; the direction dmarz approved is in `_decision.md`.

`fd add` from a fresh worktree re-digests every other artifact and drops entries whose binaries or `data/` inputs are
not present locally. Only this film's lock entry and attestation were committed; all other records are as on main.
