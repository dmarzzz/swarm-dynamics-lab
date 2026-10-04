# Post-mortem: s1-001

Run `sybil-scale-opus/79bb3882`, revision `80d70b7a9ec6ad489a0e36a3acfd704d488dada2`, host sim-dmarz-13, claim `dmarz-sybil-scale-opus` (released, agentops #274). Pre-run: [s1-001-pre](s1-001-pre.md). Review: owner waiver.

## Results (measured)

- Planned / started / terminal / graded / analyzed: 2,400 / 2,400 / 2,400 / 2,400 / 2,400. Invalid 0, refusals 0, retries 0 (no 429/529).
- Tokens 21,488,624 in / 217,938 out; USD 90.313256; 2,213 s. Study total 2,465 calls, USD 93.442004.
- Primary +100.0 pp (+100 to +100); see [RESULTS.md](../RESULTS.md) for the three-cohort comparison.

## Quality and failures

No execution failures. `publish` then `verify` passed; local recomputation matched. The low mean specialist accuracy (32.8% over the grid versus Haiku 42.4% and Sonnet 47.1%) was checked before writing: the evaluator and assignments are identical to the earlier cohorts, and the difference comes from 2,243 null answers (31% of rare fields), not from scoring. It is a behaviour of this configuration (Opus 5.5, effort low, no temperature) and is confounded with the configuration change.

## Next run

None queued. The analyst's forecast that the model is not the lever for admission holds (admission is model-independent here); the open question is whether Opus abstention is an effort-level effect, which `sybil-scarcity-synth` (effort low versus high) partly addresses on a different instrument.
