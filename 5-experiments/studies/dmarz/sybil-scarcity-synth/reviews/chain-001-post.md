# Post-run review: chain-001 (sybil-scarcity-synth)

Ready request: agentops #268. Operator dmarz/orchestrator-2. Server sim-test-01, exclusive claim `dmarz-sybil-scarcity-synth`. Revision `34c11486ca6c49d0c14d60fc5e20c4aca0317f32`, source hash `b75d7b372e7e9780d79ab7b358f175752225f881e1dba87b8d6024f0a8129725`. Pre-run review: [chain-001-pre.md](chain-001-pre.md). The package had a same-researcher check under dmarz's waiver of cross-researcher review; it was not independently reviewed.

**Outcome: provider stop in S1, not a scientific or qualification result.** S0, P0 and Q0 passed on `claude-opus-5-5`. S1 stopped at 304 of 960 dispatched calls, because the Anthropic organization reached its monthly API usage threshold. The pre-registered ladder step to `claude-opus-5` was refused by the same limit at its probe. No primary or secondary contrast can be estimated: no root has all of its cells complete.

## What ran (measured)

| Stage | Run | Model | Planned | Valid | Failed | Not started | Calls | Input tokens | Output tokens | Cost USD |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| S0 | `e1ada5ff` | scripted | 128 | 128 | 0 | 0 | 0 | 0 | 0 | 0 |
| P0 | `03aad727` | claude-opus-5-5 | 1 | 1 | 0 | 0 | 1 | 23,536 | 38 | 0.094904 |
| Q0 | `3e594c13` | claude-opus-5-5 | 48 | 48 | 0 | 0 | 48 | 1,133,304 | 4,634 | 4.625896 |
| S1 | `d955e1b4` | claude-opus-5-5 | 960 | 292 | 12 | 656 | 304 | 6,848,903 | 46,808 | 28.331772 |
| P0 (ladder) | `7c26a1c6` | claude-opus-5 | 1 | 0 | 1 | 0 | 1 | 0 | 0 | 0 |

Opus 5.5 ledger: 353 calls, 377 transport attempts, 341 calls with reported usage, actual USD 33.052572 (8,005,743 input / 51,480 output tokens). The 12 failed S1 calls reported no usage and carry no charge in the ledger. The Opus 5 attempt has its own ledger: 1 call, 3 transport attempts, USD 0.

Row reconciliation for S1: 960 assigned = 292 valid + 12 failed + 656 not started. 304 started, 304 terminal, 292 graded and analyzed. S1 ran 11:31:50Z to 11:44:48Z.

`verify` passed for both model attempts (exit 0, ok): hub metrics, status and artifacts match; grades, analysis, summary and packet hashes were recomputed; no unit was counted twice. Records: [verify.json](../records/verify.json), [opus5-verify.json](../records/opus5-verify.json), [status.json](../records/status.json) (server paths redacted).

## Qualification (Q0, measured)

All four configurations passed with no miss: 12 of 12 valid, 72 of 72 fields correct, 12 of 12 exact packets, and null on all 6 withheld rare fields, for each of base/low, rule/low, base/high and rule/high. [q0-summary.json](../records/q0-summary.json).

## The provider stop

From 11:44Z, S1 calls returned HTTP 429 with this kept error body:

> `{"type":"error","error":{"type":"rate_limit_error","message":"You have reached your API usage limits: your organization has crossed its monthly API usage threshold, set based on your organization's API tier. You will regain access on 2026-11-01 at 00:00 UTC.","details":{"error_code":"enforced_spend_limit_reached"}}}`

The 429 retry rule retried each call twice. After 12 failed calls the stage stopped with `failed_calls_exceed_limit:12`, as designed. This is an organization-level spend limit, not a per-model rate limit. The ladder's one Opus 5 probe was refused in the same way, at USD 0.

That probe was sent before fleet-monitor's message arrived, which declared the ladder void and stopped all Anthropic launches. No further Anthropic calls were made.

## Partial S1 (descriptive only; incomplete)

These rows are an unplanned partial sample: 292 of 960 assignments, with between 3 and 14 valid roots per cell out of 24. Which rows completed was set by dispatch order and the time of the stop, not by design. The planned estimand and its intervals are not defined: `complete_roots` is 0 for the primary. The analysis file reports all-assigned bounds, which are very wide. The table below gives valid-row means of rare-fact accuracy at the single-carrier and 27-carrier levels; it is not a result.

| Carriers | Arm | base/low | base/high | rule/low | rule/high |
|---:|---|---:|---:|---:|---:|
| 1 | random | 0.00 (n=8) | 0.14 (7) | 0.00 (5) | 0.07 (5) |
| 1 | coverage | 0.07 (5) | 0.11 (6) | 0.06 (6) | 0.07 (5) |
| 27 | random | 0.85 (9) | 0.97 (10) | 0.67 (4) | 0.78 (6) |
| 27 | coverage | 0.91 (11) | 1.00 (6) | 0.44 (9) | 0.47 (5) |

What these few rows show: at one carrier, no configuration resisted the repeated fabrication (fabricated share 0.73 to 1.00). At 27 carriers, the rule prompt scored below the base prompt. At 81 carriers, every configuration scored 1.00. With these sample sizes and the non-random truncation, none of this supports a claim. Full per-cell output: [s1-partial-analysis.json](../records/s1-partial-analysis.json).

## Quality and failures

- Execution, scoring, ledger and verification all behaved as designed, including the failed-call limit and the separate Opus 5 batches and ledger.
- The credit-balance detector did not catch this error: the message says "usage limits", not "credit balance". The operator rule on #268 anticipated that case.
- The only failure is the provider stop. Its cause is outside the study.

## Next run

None while the organization limit holds. Access returns 2026-11-01 00:00Z, unless dmarz raises the limit or tier. A rerun would be a new dated attempt with fresh roots. These partial Opus 5.5 rows must not be pooled with it, and no gate changes. Whether to move the study to another provider is dmarz's decision, through dmarz/fleet-monitor. The claim on sim-test-01 is released after this review. Raw records are copied to git-ignored `data/sybil-scarcity-synth/`.
