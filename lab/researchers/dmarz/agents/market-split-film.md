---
agent: dmarz/market-split-film
tool: claude-code
state: working  # working | idle | blocked | done
task: null
doing: theseus-film v2 filed after vishesh's accuracy review of 2026-10-05; updating the results site copies next
updated: 2026-10-05T00:55Z
---

## Notes

Film source is `5-experiments/studies/dmarz/market-split-film/`: v1 (silent) is `build_data.py`, `build.py`, `film.html`; v2 (narrated) is
`narrated/` (`script.json`, `vo.py`, `build_data.py`, `build.py`, `film.html`), which imports v1's checks. `_decision.md` has both directions.
It reuses the recorder and the repo QR code from `5-experiments/studies/dmarz/discussion-dose/src/film_v3/`. The look is
read from the brand kit at build time and is not copied into this repo.

Artifact `market-split-film` v1 and v2 cover the Sonnet pilot only. The Opus 5.5 replication (`market-split-opus`) was
mid-run when v1 was made. When its results and post-mortem are published, extend `build_data.py` to read its records
and file a new version; the directions dmarz approved are in `_decision.md`.

`fd add` from a fresh worktree re-digests every other artifact and drops entries whose binaries or `data/` inputs are
not present locally. Only this film's lock entry and attestation were committed; all other records are as on main.

The narration voice is synthetic (Kokoro `af_heart` through mlx-audio). `vo.py` needs an environment with mlx-audio,
misaki[en] and the spaCy model en_core_web_sm; the timeline is derived from the clip lengths, so recorded clips named
`<key>.wav` can replace the synthetic ones without touching the page.

Second film: `5-experiments/studies/dmarz/theseus-film/` (`_decision.md`, `script.json`, `film_data.py`, `make_film.py`, `film.html`). It
reuses the market-split film's narration and mix tools (`narrated/vo.py --script`, `narrated/build.py`) and the same recorder.
The study belongs to vishesh; a note about the film is in his inbox. If his v2 turnover run ever completes, the closing
lines C3 and C4 of `script.json` are the ones to revise.

Close-out, 2026-10-04. The film binaries are git-ignored. Copies with checksums matching the lock are in the swarm-lab
checkout on orbital-one (`artifacts/market-split-film/`, `artifacts/theseus-film/`) and in this lane's worktree on
halcyon. The built pages, narration clips and reduced data (git-ignored `data/`) are backed up on orbital-one under
`~/backups/swarm-lab-films/2026-10-04/` with a MANIFEST.txt. Open items are on dmarz's backlog under the tag
`swarm-lab`: review of the two narrated films (nobody has listened to them), and a market-split version with the Opus
replication once that study publishes results.

Revision, 2026-10-05. vishesh reviewed the films on the results site and sent notes. `theseus-film` v2 answers them:
a scope line on screen throughout, the observatory and mentoring sentences limited to steps 4 and 5, and a dated
closing that no longer says the follow-up has not run. What changed, what was checked and what was not is in
`5-experiments/studies/dmarz/theseus-film/REVISIONS.md`. `record_stream.mjs` there records without writing frames to
disk. The closing status line is dated 2026-10-05 00:23 UTC; when `swarm-of-theseus-s50-main` finishes, edit `STATUS`
and `REVISED` in `make_film.py` and file v3.
