---
agent: dmarz/market-split-film
tool: claude-code
state: done  # working | idle | blocked | done
task: null
doing: filed v2 of the market-split film, a narrated version (wall of all 36 runs, zoom into market 36, the agent's message and reply, then the result); no model calls
updated: 2026-10-04T09:25Z
---

## Notes

Film source is `researchers/dmarz/notes/market-split-film/`: v1 (silent) is `build_data.py`, `build.py`, `film.html`; v2 (narrated) is
`narrated/` (`script.json`, `vo.py`, `build_data.py`, `build.py`, `film.html`), which imports v1's checks. `_decision.md` has both directions.
It reuses the recorder and the repo QR code from `researchers/dmarz/notes/discussion-dose/src/film_v3/`. The look is
read from the brand kit at build time and is not copied into this repo.

Artifact `market-split-film` v1 and v2 cover the Sonnet pilot only. The Opus 5.5 replication (`market-split-opus`) was
mid-run when v1 was made. When its results and post-mortem are published, extend `build_data.py` to read its records
and file a new version; the directions dmarz approved are in `_decision.md`.

`fd add` from a fresh worktree re-digests every other artifact and drops entries whose binaries or `data/` inputs are
not present locally. Only this film's lock entry and attestation were committed; all other records are as on main.

The narration voice is synthetic (Kokoro `af_heart` through mlx-audio). `vo.py` needs an environment with mlx-audio,
misaki[en] and the spaCy model en_core_web_sm; the timeline is derived from the clip lengths, so recorded clips named
`<key>.wav` can replace the synthetic ones without touching the page.
