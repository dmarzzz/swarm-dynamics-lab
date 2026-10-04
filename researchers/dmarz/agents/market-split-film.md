---
agent: dmarz/market-split-film
tool: claude-code
state: done  # working | idle | blocked | done
task: null
doing: filed a narrated film of vishesh's Swarm of Theseus pilot S1-a1 as artifact theseus-film v1 (reads his committed results and evidence archive only; no model calls), after the two market-split films
updated: 2026-10-04T10:35Z
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

Second film: `researchers/dmarz/notes/theseus-film/` (`_decision.md`, `script.json`, `film_data.py`, `make_film.py`, `film.html`). It
reuses the market-split film's narration and mix tools (`narrated/vo.py --script`, `narrated/build.py`) and the same recorder.
The study belongs to vishesh; a note about the film is in his inbox. If his v2 turnover run ever completes, the closing
lines C3 and C4 of `script.json` are the ones to revise.
