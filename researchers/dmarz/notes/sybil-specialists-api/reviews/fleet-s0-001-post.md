# Post-mortem: fleet-s0-001

Experiment sybil-specialists-api / dmarz/sybil-specialists / S0 / 2026-10-04 UTC. Parent local-s0-001. Pre-run fleet-s0-001-pre.md. Disposition advance to API qualification Q0.

## What ran and what happened

Run sybil-specialists-api/62c03464 at committed revision e407c024d885c4b355d501e958d61d304db25d81, runtime digest 12ff89f2f54322f07245640708a0c243ad09ab8d933163e71869c3ce08255f6a. 216 planned → started → terminal → graded → analyzed, zero missing/invalid/duplicate observations. All 24 clean packets exact, field and missing-evidence accuracy 100%. Zero model calls/tokens/spend. Execution loop 15.53 seconds, whole hub run 37 seconds including rendering/uploads. Both remote selftest suites passed (27 tests total).

## Visualization review

Seven artifacts durably acknowledged and every local SHA256 matched hub metadata. Both PNGs and replay are 1800×1180; replay has 28 measured prefix frames. Live browser shows done 216/216, final image first and embedded GIF. Full-size playback begins at pending 0/216 and progresses through saved call prefixes. No hidden truth enters actor packets. One early read-only reconciliation ran while uploads were still completing and correctly refused missing artifacts; after done, all checks passed without rerunning observations.

## Experiment-quality assessment

The exact committed runtime reproduced local scripted behavior and qualification. Local-provenance is closed by source-pinned fleet evidence. Data quality and control checks passed; LLM competence remains untested. These repeated scripted observations are engineering validation, not independent scientific data. The existing graph-family, simulator and comparator limitations remain.

## Failure and repair ledger

No worker, evaluator or upload defect. local-provenance closed; pending public embedding closed. An unrelated project-wide Flight Deck strict check currently reports three older artifact author-schema errors and a missing deployment source on another researcher's artifact; this study adds no artifacts registry entries. It does not affect the executable instrument and is recorded for final validation.

## Next run

Q0-001: 24 fresh paid clean-packet calls with pinned Haiku4.5 and the unchanged prompt/config/runtime. USD5 aggregate reserve cap, no retries, one finite worker on the same exclusive claim. Require every structural record valid, >=95% field accuracy, >=90% exact packets, 100% missing-evidence abstention. Only a passing screen permits the predeclared 192-call exploratory pilot.
