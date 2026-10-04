# Frozen-history reading-rule diagnostic

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by shadow/sol-cm2; source `d648e0f7` ([registry](../../../../../experiments/evidence-metadata.json), [rubric](../../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **2/4** — Reversing these indexed raw histories changed majority-name probability by far less than the prespecified 0.10 practical threshold. Basis: All 24 paired synthetic histories and 12 unanimous controls are complete; mean absolute effect 0.000183, 95% history-bootstrap interval [0.000002,0.000532]. Explicit last-event metadata, mixed upstream providers and no independent replication limit generalization.
- **sample_size_summary:** Observed: 24 synthetic history units; 144/144 scientific calls valid across six paired presentations. R2 controls: 12/12 valid and correct on two separate histories. All attempts: 157 calls, 156 valid, one old HTTP403; 155 v1 assignments unstarted. Calls are not independent histories.
<!-- experiment-evidence:end -->

**Latest result, R2 (2026-10-04): complete.** [FINDING.md](FINDING.md) reports all 24 paired synthetic histories and 144/144 valid scientific calls. Reversing raw indexed histories had mean absolute probability effect 0.000183, far below the prespecified 0.10 threshold. All 72 raw choices followed the true last event, explicitly disclosed in each prompt. This does not establish a mechanism for prior swarm recovery.

R2 used the unchanged frozen requests after a prospective [access-restoration amendment](AMENDMENT-R2.md). Cumulative: 157 attempts, 156 valid including qualification, one historical HTTP403; USD0.01704420 reported cost plus USD0.05 unknown-cost allowance, USD7.85 retained reservations under USD8. [Root accounting](accounting.json), [all attempt assignments](all-attempts.csv), [R2 post-mortem](POSTMORTEM-R2.md).

## Historical v1 closeout (superseded operational status, retained evidence)

The following describes only v1. Its blocked result is preserved; R2 did not rewrite or silently retry it.

**Status: access-blocked, no scientific result.** On 2026-10-04 at 15:50:40Z the first OpenRouter qualification request for `openai/gpt-4o-mini` returned HTTP 403. The runner stopped immediately as preregistered. No valid model response was obtained; the reason for the provider's denial is not established by the saved status code. No Anthropic pool was used.

## Question and fixed design

Does a coordination model change its choice when identical histories are shown chronologically, reversed or shuffled, as raw events versus a lossless count-and-position summary? True chronology is indexed, and true last-event metadata is present in all six conditions. Position lists make the summary reconstruct the whole history, not just the counts. This is not a pure count-only ablation.

The [prospective plan](PLAN.md) and [frozen prompts](input.json) were committed and public before the request. Scientific units would be **24 synthetic histories**, lengths 16/64/256, balanced majority name and last-event conflict, two seeded permutations per stratum. Six calls per history are paired observations, not six independent samples. This is an instrument diagnostic, not a natural-history replay or a swarm-recovery replication.

## Complete accounting

| Stage | Frozen assignments | Started | Terminal | Valid | Unstarted |
|---|---:|---:|---:|---:|---:|
| S0 qualification, 2 unanimous histories | 12 | 1 | 1 HTTP 403 | 0 | 11 |
| S1 comparison, 24 histories | 144 | 0 | 0 | 0 | 144 |
| Total | 156 | 1 | 1 | 0 | 155 |

S0 criteria were 12/12 valid receipts and at least 11 unanimous-name choices. Access failed before capability could be assessed. S1 was never admitted. No first-token probabilities, effects, confidence intervals or recovery findings exist for this diagnostic. The primary all-assignment bound remains the uninformative [0,1].

- Budget authority: USD 12 total, OpenRouter only. USD 0.05 reserved durably before the one attempted request and retained after the error. **Actual cost unknown**, not asserted to be zero. The sum of known reported costs is zero because there were no cost receipts.
- Full original [journal](results/journal.jsonl), [admission/public-plan receipt](results/admission-S0-155040161364.json), [summary](results/summary.json), [all-assignment table](results/scored.csv).
- [Missingness figure](results/paired-history.svg) shows crosses for every unstarted scientific cell; it is not a plot of model behavior.
- [Post-mortem](POSTMORTEM.md), [setup/handoff](SETUP.md), [S0 pre-assessment](S0-PRE.md).

## Reproduction and next action

Offline only, from this directory:

```sh
python3 test_reading_rule.py   # 8 instrument and guard tests
python3 analyze.py            # regenerate aggregates and missingness plot from saved journal
```

Frozen instrument revision: `cf36e30fd72c53147afa37f6418b94f6870e0fb2`. No retry is warranted merely to obtain a result. V1 ends blocked. If the owner resolves OpenRouter access, prepare a separately declared qualification attempt with refreshed public admission, unchanged independent-unit rules and the existing USD 0.05 exposure carried forward. Do not switch to the Anthropic pool or reset the cap. No further calls were made in this session.
