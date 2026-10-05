# 2026-10-05, dmarz/market-split-film

- dmarz passed on vishesh's accuracy notes on the films shown on the results site (reviewed 2026-10-05 00:03 UTC) and
  asked for them to be fixed, without making a batch of new films.
- Filed `theseus-film` v2 (3 min 57 s). Changes and checks: `5-experiments/studies/dmarz/theseus-film/REVISIONS.md`.
  Five narration clips were spoken again and the picture recorded again; the other 24 clips are the v1 recordings.
- Checked the hub before writing the closing: `swarm-of-theseus-s50-main` was still running at 00:23 UTC, so the film
  says the fifty-seat qualification passed and gives no outcome for the main run.
- Surprise: the review's point about the observatory was right at the step level. Observatory crews with notes were
  wrong on some cases in steps 0 to 3 and right on all of them only in steps 4 and 5, while v1 lit all six steps and
  said "every case right". `make_film.py` now checks that sentence against the steps, not the summary.
- Surprise: the influence film on the site has an audio track that is silent from start to end (23.99 s against 20.8 s
  of picture), so there is no narration to correct in it.
- The build machine's disk filled twice during the render (other jobs were writing to it); the shared recorder needs
  about 5 GB of frame files. `record_stream.mjs` pipes frames to the encoder instead.
- Not done: no telephone or immune film was made (there were none on the site, and dmarz did not want new ones yet).
  Nobody has listened to either version of the Theseus narration by ear.
- The fifty-member run closed at 00:33 UTC, ten minutes after v2's status line said it was in progress. Filed v3 with
  the same narration and a status line that names only the passed qualification, so it does not go stale again.
- Next: nothing owed on this film. If a film of the fifty-member study is wanted, it is a new film from that study's
  own reviewed results.
