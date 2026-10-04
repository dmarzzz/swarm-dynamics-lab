# Post-mortem: v3o-a3 S1 (stopped on provider spend limit)

Attempt v3o-a3, S1 only, gated on the passed v3o-a2 Q0. Server sim-dmarz-9, claim `dmarz-v3-q0-opus`, revision `d61a4183c6f8f6deee304d42b625e3ca18bf78d0`, worlds 54201–54224. Pre-run review: [v3o-a3-pre.md](v3o-a3-pre.md). Operator dmarz/orchestrator-2. Not independently reviewed (owner waiver).

## What happened (measured from the journal)

- Started 10:25:08Z; the probe passed at USD 0.005208.
- 708 call starts and 633 responses. All 633 responses came before the first failure, at call index 633.
- From call 633 to call 706, all 74 calls failed with `provider_failure` reason `provider_rate_limit`. The Anthropic organization had crossed its monthly API usage threshold: HTTP 429 `rate_limit_error`, `error_code: enforced_spend_limit_reached`, with access returning 2026-11-01 00:00 UTC. The same error was first recorded at 11:44Z in sybil-scarcity-synth.
- The runner records a failed call and continues, so every remaining assignment would also have failed. On fleet-monitor's instruction, dmarz/orchestrator-2 sent SIGTERM to the chain process at 11:50:58Z. The journal has 2,071 events and ends with a `call_start` for c000707, with no `complete` event. Whether c000707 was dispatched or billed is unknown.
- Cases: 81 of 276 assignments reached a terminal event. The rest are incomplete.
- Usage summed from the responses: 4,063,464 input and 331,359 output tokens. That is USD 22.881036 at USD 4 / USD 20 per million tokens. Failed calls report no usage.
- I set the hub run `discussion-v3-opus/v3o-a3-s1` to failed, with the reason, through swarm_report. As with a2, the chain installs no SIGTERM handler.

## Quality and interpretation

The cause is a provider stop that affects the whole organization and every Anthropic model. It is not caused by the model, the instrument or the scorer. The runner's audit applies only to completed runs: it refuses an interrupted journal ("interrupted run; assignments remain unresolved"). So no audited S1 result exists, and the 81 terminal cases are not reported as an estimate. The attempt is preserved and is not rerun on any Anthropic model while the limit holds. Records: [stopped-attempt.json](../records/v3o-a3-s1/stopped-attempt.json), manifest and chain state in the same folder. The raw journal is in git-ignored `data/`.

## Failures and causes

| ID | Failure | Cause | Repair | State |
|---|---|---|---|---|
| A3-1 | 74 calls refused (HTTP 429) | Organization monthly spend limit | None possible until 2026-11-01, or until dmarz raises the limit | open, external |
| A3-2 | Hub run stays `running` after SIGTERM | No signal handler in the chain | Set to failed by hand (same gap as in a2) | open, tooling |
| A3-3 | Runner keeps dispatching after a non-credit spend-limit error | Detector covers credit-balance text only | Treat `enforced_spend_limit_reached` as a stop category | open, tooling |

## Next run

The S1 estimate needs a new dated attempt on fresh worlds. The v3o-a2 Q0 gate is unchanged. It can run only after Anthropic access returns, or as a separately qualified configuration on another provider, which is dmarz's decision. These rows are never pooled with a later attempt. The claim on sim-dmarz-9 is released after this review.
