# Post-mortem: q0-001

- Experiment / owner / stage / date: market-split-opus; dmarz/market-split-opus; Q0 profit qualification; 2026-10-04, 08:02-08:05 UTC.
- Pre-run assessment: [q0-001-pre](q0-001-pre.md) and [phase2-pre](phase2-pre.md); parent `i0-001`. Commit `b097331b874f2dcab2b31a830e54cdc39f9d321d`; engine `56c67cd0…c047b`; design `8d952af0…a687d`; model `claude-opus-5-5`, adaptive thinking, effort medium.
- Run ids: `market-split-opus/a658f5319ce4` (task 100) and `market-split-opus/3e1e1e294a54` (task 101), seed 31, no regulation, both arms, eight rounds.
- Disposition: advance to S1. Qualification passed; the projection is inside all three limits.

## What ran and what happened

- 2 bundles planned, started and done; 4 episodes, 4 valid; 32 calls attempted, 32 priced, 32 valid actions; no retry, no unpriced call; every stop reason `end_turn`.

| Task | Arm | Profit | Ratio to scripted one-firm reference | Registrations | Final firms |
|---|---|---|---|---|---|
| 100 | flexible | 19,503.06 | 1.000 | none | 1 |
| 100 | locked | 19,503.06 | 1.000 | none | 1 |
| 101 | flexible | 15,177.04 | 1.000 | none | 1 |
| 101 | locked | 15,177.04 | 1.000 | none | 1 |

- Gate: every episode profitable and at 100% of the reference, against the unchanged 75% floor. The model chose `maintain` in all 32 rounds and produced the lagged best response exactly ((36.5, 33.5) on task 100 and (33.5, 28) on task 101), which is the reference policy itself. Its notes say so: "No enforcement active; best-respond to recent competitor output."
- No registration in either unregulated flexible episode. The Sonnet pilot's qualification also showed none; one unregulated Haiku episode did register.
- Usage: 61,962 input and 4,275 output tokens; USD 0.333348. Per call 1,936.3 input and 133.6 output tokens (median 128.5, largest 222). Latency median 3.39 s, largest 4.47 s. Study ledger after Q0: 38 calls, USD 0.394340, all priced.
- Exact replay: the pilot's `audit_saved.py` was run on the server in the pinned runtime against this attempt. 32 of 32 saved observations and actions and all 4 traces, evaluations and validity outcomes were reproduced. Same-author audit.
- 14 of 14 run artifacts match their local files by SHA-256 against the hub; final images are 1800×1200 and replays 1080×720 with 8 frames.

## Projection for S1, as the pre-run review requires

Using the pilot's S1-to-Q0 ratios:

| Quantity | Opus Q0 | Ratio | Projected S1 | Limit |
|---|---|---|---|---|
| Input tokens per call | 1,936.3 | ×1.191 | 2,306 | |
| Output tokens per call | 133.6 | ×1.367 | 183 | |
| S1 cost, 864 calls | | | USD 11.13 | |
| Study cost | I0 0.06 + Q0 0.33 + S1 | | USD 11.52 | USD 160 |
| Largest response | 222 | ×2.771 | 615 tokens | 8,192 |
| Largest latency | 4.47 s | ×2.2 | 9.8 s | 180 s |

All three are inside their limits, so S1 was launched at once. The projected cost is below the pre-run central estimate of USD 25 because the model produces far fewer output tokens than the Sonnet pilot did (134 against 542 per call in qualification), not more as feared. The ratios come from a model that thought more in regulated markets; if Opus does the same the S1 figure will be higher than projected, with a wide margin to every limit.

## Experiment-quality assessment

- The qualification did what it is for: the model can earn the reference profit on clean unregulated markets through this interface. It reached the reference exactly, so the gate did not discriminate finely, but it is the pilot's gate and it is unchanged. Eight rounds on two markets is a screen, not a competence estimate.
- A known difference from the pilot that this stage makes concrete: the pilot's Sonnet needed a 2,048-token thinking budget to pass this floor (non-reasoning Sonnet scored 68%), and used about 540 output tokens per call. Opus at effort medium passes with about 134 output tokens per call, so it is thinking little or not at all on most calls. Whatever S1 shows is the behavior of that configuration.
- Q0 has no regulator and cannot show discovery or its absence.
- Evidence metadata unchanged in substance until S1 completes.

## Visualization review

Mapping `market-split-opus-v1`. Each run has a progress image, an 1800×1200 final image titled MODEL PILOT and a 1080×720 eight-frame replay; sizes, frame counts and hashes were checked by the verifier. I did not open a Q0 frame; the episode endpoints above come from the saved records.

## Failure and repair ledger

| ID / kind | Observed evidence | Cause | Repair | Acceptance check | Status |
|---|---|---|---|---|---|
| O2 cost and execution risk | 134 output tokens per call, largest 222; latency under 5 s | The model thinks little at this effort on this task | none needed | Projection inside all three limits | Closed for admission; S1 usage reported at closeout |

## Next run

`s1-001`: tasks 110-115, seed 41, three regulators, two arms, 24 rounds; 18 bundles, 864 calls; one finite worker of nine bundles, then the rest. Launched 08:05 UTC.
