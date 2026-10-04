> Live implementation update: the native relay, frozen executor, qualification and policy comparison are now implemented and executed. Current files are src/live_design.py, src/live_relay.py, src/live_worker.py, src/validation_worker.py and src/live_render.py. There are 53 passing software checks. REPORT.md and run configurations supersede the historical readiness statements below.

# RD-1 implementation and validation

The plan was committed at `5fd034c9af6613a9e8180874ab559312186b465c` before implementation. PLAN-PUBLICATION.json records an HTTP retrieval and exact-content match of its immutable public URL. That receipt is publication evidence, not hub run registration or research approval.

## Implemented

- `src/cases.py`: deterministic scenario records with a separate gold compartment, balanced action-direction controls, static scope/freshness/availability/delay/noisy-check conditions, and a three-epoch alarm trajectory. Reserved seeds require an explicit stage; the delivered examples use development seeds only.
- `src/protocol.py`: actor-field whitelist, bounded evidence checks, source-aware challenge fingerprints, withdrawal, repeat suppression, fresh-evidence reopening, explicit failure/DEFER outcomes, and paired correction/corruption accounting.
- `src/policies.py`: a transparent exact grammar reference plus strict response-tape replay. The exact policy's CHECK decision is not a learned evidence gate and proves no advantage over always-check.
- `src/jev.py`: pinned requested-model/provider wire construction and strict action, probability, confidence, usage and served-snapshot validation. No credentials or transport are present.
- `src/study.py`: private observation views, native-policy injection points, unselected natural-vote/challenge construction, exclusive attempt directories, incremental assignment/outcome records and interrupted-attempt reconciliation.
- `src/launch.py`: a fail-closed readiness diagnostic. Its flags do not perform live authorization; no function here dispatches model calls.
- `visualization/replay.html` and `build_preview.py`: saved-event fixture replay with scenario/policy selection, step/scrub/play controls, source records, optional evaluator overlay, and explicit failure states. The example is labelled scripted throughout.

## What is not implemented or established

There is no live credential relay or fleet executor for this study. The adapter can prepare requests and validate externally collected response tapes; native transport must be connected to the approved bounded executor after the live gates pass. This is an offline-validated prototype, not a claim of deployment readiness.

The alarm implementation uses a prescribed false-alarm → repeated-record → new-event trajectory (and the reversed action direction), not arbitrary event histories. The static variants are controlled grammar fixtures. Topology, learned reputation, simultaneous challengers, complex linguistic variants and a powered confirmatory sweep remain design extensions. The parameter ledger distinguishes them.

The first causal comparison uses scripted initial votes and challenges. Private-view and natural-challenge functions are implemented and checked offline, but no model-generated group has been collected. Actor confidence has not been calibrated. Provider availability, present pricing and returned snapshot have not been qualified for this study. A different study's working adapter is useful reference, not evidence of qualification here.

## Reproduce offline checks

From the repository root:

```sh
python3 -m unittest discover -s 5-experiments/studies/vishesh/dissent/tests -v
python3 5-experiments/studies/vishesh/dissent/src/cli.py requests --out /tmp/right-dissenter-requests.json
python3 5-experiments/studies/vishesh/dissent/visualization/build_preview.py --out /tmp/right-dissenter-preview.html
```

Output commands refuse to overwrite existing files. The `requests` export contains development wire probes, not a run assignment or authorization. `fixtures` exports a software fixture bundle. `replay --tape <path> --snapshot <served-id>` validates an externally supplied response tape; its claimed origin still requires executor provenance. No secret values belong in those files.

Forty-one offline tests pass. They cover both correction directions, harmful reversals, scope and temporal validity, nonexistent citations, aliases of closed evidence, budget exhaustion, unavailable/late/wrong verification, withdrawal and reopening, truth-field mutation, provider failures, invalid probabilities/model routes, private-view isolation, no-dissent retention, output overwrite prevention and interrupted-assignment denominators. These are engineering checks, not forty-one independent research trials.

The dashboard exporter and its 29 tests pass with DM-03 and DM-14 tagged to both relevant areas. DM-03's original owner score is intentionally stale; it was not silently refreshed against a changed question.

Browser inspection verified bridge correction, build scope rejection, the alarm's withdrawal/repetition/reopening sequence, evaluator-truth visibility control and an explicit failed DEFER. The preview has responsive styling; browser checks at additional small-screen widths are recorded separately if performed. No public Swarm Live playback or image fallback is claimed yet.
