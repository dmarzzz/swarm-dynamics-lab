# Pre-run assessment: receipt-native-a1

- Experiment / owner / stage: Immune Response (`immune-response-v3`), vishesh/codex-immune, bounded development diagnostic.
- Parent: scenario-native-a2 and scenario-solo-a1; previous [assessment](../../scenario-study/ASSESSMENT.md) read in full.
- Status: **diagnostic-only**. Familiar service graph, no independent scenario review; not a confirmation stage.
- Decision: does checking explicit reviewer claims improve safe recovery enough to justify a larger independently authored benchmark? Expect some false claims or harmful actions may remain; no mismatches makes the receipt contrast uninformative about correction.

## Design and assessment

Strongest baseline: visible-contract deterministic solver; it succeeds with either receipt and either memory. Eight paired case/memory worlds reuse 24 reviewer outputs for 16 commander episodes. Analysis unit is a paired world, not each tick, boolean or reviewer. Case overlap and seed-only renaming prevent population inference. The previous 9200–9215 reserved material is unopened.

Raw and checked share exact advice, generic caution, current telemetry, catalog and six action slots. Only deterministic receipt annotation differs. A visible-probe receipt makes no optimal-action claim. Structured transcription changes both arms relative to historical A2; historical improvement cannot be attributed to checking. Commander claims are graded after response only. Both clean incident competence and healthy preservation are necessary. Primary paired healthy-tick difference is reported per case/memory; secondary outcomes separate false factual claims, rejected changes, newly failing probes and loss of healthy service. No inferential p-value on these eight familiar worlds.

Timing is six simulated tool-action ticks, plus an initial state at zero. Request latency and actual usage are recorded separately; verifier is a local comparison with no model/tool call. Checking adds prompt text, so actual token/cost differences must be reported rather than claiming exact token matching.

## Changes and unresolved issues

| Issue / evidence | Change | Acceptance / disposition | Owner |
|---|---|---|---|
| A2 narrative contradicted live probes | Both arms declare booleans; one receives checked receipts | Measure reviewer/commander errors and retain prose for audit | codex-immune |
| Independent reviewers varied across old arms | Generate each world once, fork identical proposals | Equal proposal hash across every paired episode | codex-immune |
| Old reset reintroduced stale material at tick 4 | Truly clean competence condition | All clean frame memory IDs empty | codex-immune |
| A2 passed despite failure to recover | Joint healthy/recovery readiness gate | Healthy 6/6 with zero deploys; incidents final healthy, ≥4/6, no rejected actions or loss of healthy service | codex-immune |
| Offline a1 damage definition made migrated case impossible | Separate new failing checks from loss of healthy service | Migrated reference logs one probe regression, zero loss of healthy service | codex-immune |
| Names are not scenario diversity | Explicitly retain development label | No generalization/robustness claim or scale-up | codex-immune |

## Frozen execution plan

Source and config are committed before dispatch. Runtime commit and file hashes bind runner, provider, inherited simulator, protocol, model config and renderer. Native Haiku 4.5 pinned 20251001, temperature 0, 512 output tokens, 16,000 request bytes. Seed 9300, 4 cases × 2 memories × 2 receipts; randomized world order and alternating receipt order. Command: `python evidence-study/worker.py --out /srv/swarm/immune-response/receipt-native-a1 --receipt /srv/swarm/immune-response/receipt-allocation.json` from the study environment.

Maximum 120 calls, one worker, 60-second timeout per call, no retries, ≤2.5-hour bounded execution envelope. Existing USD 8 cap and persistent `scenario-budget.sqlite` are unchanged: pre-run reserved USD 1.815067 across 240 calls; maximum additional conservative reservation USD 2.28864. Actual cost before this attempt USD 0.441259. Credential alias `swarm-lab-anthropic` is read locally, never printed. Missing/invalid responses consume slots and fail execution acceptance. Unique output directories refuse restart. If budget/config/allocation fails before execution, preserve setup diagnostics and do not create a new cap.

Dedicated vishesh-owned host `sim-immune-response`, exclusive merged claim `vishesh-immune-receipts-a1`, until 2026-10-04 09:41:16 UTC, [fleet PR 77](https://github.com/dmarzzz/swarm-labs-agentops/pull/77). Original grant `immune-scenario-native-8-20261004`. No dmarz machine borrowed. Refresh exclusivity immediately before launch. Public artifacts are associated with the existing experiment and a fresh attempt ID.

Eight unit tests pass, including all 256 pairs of four-boolean claim/observation patterns, malformed claims, adversarial but faithful harmful action, rejected store change, shared-proposal immutability, missing responses and clean-memory semantics. Scripted engineering a1 exposed the metric defect and is retained; amended engineering a2 records 16/16 outcomes with zero invalid and all joint gates passing. No paid outcome informed this repair. Historical scenario tests run separately. If native execution is valid but capability fails, analyze whether an interface defect or a valid model limit remains; no unchanged rerun to seek a pass. Scaling remains blocked.

## Visualization mapping

[README mapping v1](../README.md#visualization-mapping-v1), bound to receipt-native-a1 and seed 9300. Initial state + six measured action frames; eight panels show all case/memory pairs, overlaid raw/checked lines. Marks distinguish lost healthy service, rejected actions and false probe claims. Live/final 1800×1200 PNG, seven-frame GIF and interactive HTML with receipt details, all four probes and every decision. Missing cells explicitly unrecorded. Public dashboard supports image/GIF; local replay is the HTML fallback. Offline final PNG visually inspected; dimensions, trace-to-summary totals and replay playback checked before final reporting. Imported scripted results are feasibility evidence only.
