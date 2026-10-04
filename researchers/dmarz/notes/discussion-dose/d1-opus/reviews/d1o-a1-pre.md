# Pre-run assessment: d1o-a1

- Experiment / owner / stage: discussion-v3-d1-opus / dmarz (operator dmarz/d1-opus) / single bounded diagnostic stage, preceded by a zero-model rehearsal.
- Parent attempt and previous post-mortem: `v3-d1-a1`, [post-mortem](../../reviews/v3-d1-a1-post.md) read; Q0 `v3-q0-a1` records re-verified against the published receipt.
- Status: **ready for zero-model rehearsal; paid dispatch blocked on dmarz's first-hand go-ahead and G0 review decision.**
- Question and decision: whether Opus 5.5 applies constraints correctly on clean full evidence. A pass (≥10/12 fresh, 12/12 valid) justifies planning a separate fresh swarm qualification on Opus; a fail closes "a stronger model fixes it" for this instrument and points at task/prompt design.
- Expected finding: pass, with ≥5/6 on reused full evidence. Plausible negative: Opus also chooses infeasible options after correct extraction, which would locate the failure in the task wording or option framing rather than model scale. Uninformative if many calls fail (refusal, truncation, timeouts), so failures are reported with reasons and the fresh denominator stays 12.

## Design and assessment

- Closest evidence and comparator: D1 Haiku and Sonnet on the identical 60 requests; the scripted evidence reader as a known-answer control (12/12 offline).
- Units: 12 fresh worlds for the gate. Reused items are 6 world clusters plus a fixed 36-fixture grid; descriptive only.
- Coverage: fresh worlds balanced 4/4/4 across dependency, capacity and total-cost families; strata 6 resolvable-construction, 6 ambiguous-construction, both with a unique clean winner. Q1 and holdout IDs unopened.
- Manipulation: model and request configuration (no temperature, adaptive thinking, effort high, 16,000 max tokens). The actor prompt, schema and evidence are unchanged. Because the configuration changed too, an Opus–Sonnet difference cannot be attributed to model identity alone.
- Evaluator: unchanged D1 scorer for reused items; fresh items use the same evidence solver (`possible_decisions`) and truth winner; truth stays evaluator-only (gold-field rejection on every request).
- Primary metric: fresh evidence-justified count out of 12 assigned; invalid counts as not justified. 10/12 mirrors D1's 5/6 rule.
- Timing: wall time only; 2-hour stage deadline.

## Changes and unresolved issues

| Issue / prior evidence | Change or diagnostic | Expected effect | Acceptance check | Owner |
|---|---|---|---|---|
| D1: correct extraction, infeasible choices (Haiku 2/6, Sonnet 3/6) | Opus 5.5 with thinking at effort high | Fewer infeasible choices | Fresh gate and reused full-evidence count | dmarz/d1-opus |
| D1 had no fresh items | 12 fresh clean worlds 52001–52012 | Unbiased competence check | Offline validate_case passes for all 12 | dmarz/d1-opus |
| Opus rejects temperature / cannot disable thinking | New adapter `Opus` (new file) | Valid requests | Mocked parse tests; preflight serialization hashes | dmarz/d1-opus |
| Thinking consumes max_tokens | max_tokens 16,000 | No truncation | `provider_incomplete` count reported | dmarz/d1-opus |

## Frozen execution plan

- Source: `src/diagnostic_v3_opus.py` at the committed revision; manifest built by `prepare` with all request and provider-body hashes.
- Assignments: 72, order seeded `d1-opus-v1-schedule`; command via agentops `scripts/run-d1-opus.py <rev> run` (no secrets in arguments).
- Caps: 72 calls, one worker, 2-hour deadline, worst-case reservation $25.26, preflight cap $30; within dmarz's shared $500 budget.
- Retry/stop: none; stops on model mismatch, accounting anomaly, local limit, low credit, deadline or owner stop file; unknown-outcome calls never resubmitted.
- Checks: offline selftest (G2); server rehearsal must pass audit before preflight.
- Allocation: dedicated new server `sim-dmarz-9`, exclusive claim `dmarz-d1-opus`; key via ssh stdin into memory only.
- If it fails: post-mortem, no rerun to obtain a better result; any successor is a new plan.

## Visualization mapping

`d1-opus-call-ledger-v1` (README): hub counter timeline over 72 assignments (started, terminal, invalid, cost, missing usage, fresh justified vs the 10/12 line); journal as replay source; per-group outcome table as the final frame. No swarm animation because there is no swarm state; failed and missing calls shown as their own states.
