# Pre-run assessment: fleet-s0-001

Experiment sybil-scale-opus, owner dmarz (operator dmarz/scale-opus), stage fleet S0 (scripted, zero model calls). Parent: [local-s0-001-post](local-s0-001-post.md).

- Design: 264 scripted assignments on engineering worlds 4900–4901, all four sizes and arms; checks graph generation, packets, evaluator, analysis, rendering and hub upload on the dedicated host at the pinned revision.
- Gate: 264/264 valid, qualification flag passed, artifacts publish then verify. Failure blocks Q0.
- Execution: host sim-dmarz-12, exclusive claim dmarz-sybil-scale-opus, one worker, revision pinned by the launcher. No credentials used.
- Visualization: [VISUALIZATION.md](../VISUALIZATION.md) v1 bound to this run id; images labelled SCRIPTED.


## Amendment 2026-10-04 ~08:25Z: transport retry (before any fleet or paid run)

At the results analyst's recommendation (pipeline LESSONS.md item 8, SOC-07's rule), `design.yaml` `retries` changes from 0 to 2 and `src/provider.py` retries only after HTTP 429 or 529 (the provider did not run the model), at most two extra attempts, all inside the one 120-second request timeout, with 2 s and 4 s waits. Every attempt is a separate ledger reservation counted against `max_attempted_calls` (2,600; planned calls are 64 Q0 + 1 probe + 2,400 S1, so up to 135 retry attempts fit before the cap halts dispatch) and the USD 600 reservation cap. Any other HTTP status, transport error or model answer (including refusal or invalid output) is never retried; the first such failure still stops dispatch. Selftest `test_transport_retry_429_529_only` covers 429→success, 529×3→failure, 500 not retried and answers not retried (11/11 pass). Runtime source hash changes to `323f8b7b2089fd6d0355297b58264ad2011784ac31f17df5ef88e9745d0b494f`; local S0 re-run as local-s0-002. No scientific input, world, prompt, schema or evaluator changes.
