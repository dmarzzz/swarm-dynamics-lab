# Post-mortem for discussion-v3-d1-opus / d1o-a1

Status: scientific assessment completed by the owning agent (dmarz/d1-opus close-out, 2026-10-04 ~08:10 UTC).
This is the owner's review, not an independent review. Cross-researcher review was waived by the owner
(SETUP.md G0).

- Study / owner / stage / attempt / parent: discussion-v3-d1-opus / dmarz / model diagnostic / `d1o-a1` /
  D1 `v3-d1-a1` (Haiku 4.5 and Sonnet 4.6).
- Pre-run assessment: [d1o-a1-pre](d1o-a1-pre.md). Source `573c4103bb411fec1b37f2288ef859737aafe839`, frozen
  manifest sha256 `29f0c9ce20012f3ec4fd3c6f1c55b35341608cc337097d7db7f61e927115a921`, model `claude-opus-5-5`,
  adaptive thinking at effort high, no temperature, `max_tokens` 16,000.
- Review verdict: **advance** (to a fresh swarm qualification on Opus).
- Execution: complete. Response validity: 72/72. Qualification (fresh gate): passed, 12/12. Scientific
  conclusion: model-level only (see RESULTS.md). Process compliance: plan, pre-run review and waiver on main
  before launch; exclusive claim; pinned source. Artifact delivery: hub run, audit and records retained.

## Reconcile the recorded facts

| Quantity | Assigned or planned | Observed | Missing, partial or uncertain | Evidence |
|---|---|---|---|---|
| Independent worlds | 6 reused + 12 fresh | 18 | none | summary.json groups |
| Started / terminal / graded / analyzed calls | 72 | 72 / 72 / 72 / 72 | 0 | audit.json: 72 requests verified, 72 outcomes recomputed |
| Model calls incl. retries | 72 (no retries) + 1 probe | 72 + 1 | 0 retries, 0 refusals | summary.json, d1o-p1 |
| Tokens | n/a | 259,135 in / 21,803 out (thinking billed as output) | 0 calls missing usage | summary.json |
| Spend | expected $1–3, worst case $25.26, cap $30 | $1.4726 batch + $0.022468 probe = $1.495 | none | hub metrics `cost_usd` |
| Wall time / machine | one worker | ~6 min (07:54–08:00 UTC), median latency 4.8 s, max 15.3 s | n/a | summary latencies |

No duplicates, exclusions or unstarted assignments. The holdout was not opened.

## Interpret the result

- Primary (fresh gate): 12/12 clean full-evidence decisions evidence-justified, 12/12 valid; the threshold was
  10/12 and 12/12. Independent n = 12 fresh worlds.
- Development comparison on identical requests: full-evidence 6/6 (Haiku 2/6, Sonnet 3/6); report quorums 4/6
  (1/6, 3/6); correct report ballots 10/18 with 8 unnecessary abstentions; memory fixtures 33/36
  policy-justified (23/36, 31/36), 0 unsupported answers, and 6/6 inherited false facts accepted.
- Supported: Opus 5.5 under this configuration does not show the extraction-to-decision failure seen in D1.
  Not supported: any swarm, discussion or memory-safety claim; the inherited-false-fact failure persists.
- Cause attribution: model, reasoning allowance and sampling changed together; no discriminating check
  separates them.

## Assess experiment quality

| Dimension | Status | Finding and evidence | Next action / acceptance check |
|---|---|---|---|
| question | pass | Does a stronger model pass the D1 clean-decision gate on fresh worlds? Answered. | n/a |
| scenarios | gap | Fresh worlds are clean full-evidence only; reused worlds are development examples | Fresh swarm Q0 with attacked arms |
| controls | pass | Haiku and Sonnet D1 answers on byte-identical requests; scripted-reader rehearsal | n/a |
| capability | pass | 18/18 full-evidence decisions correct | n/a |
| measurement | pass | Same scorer as D1; audit recomputed all outcomes | n/a |
| sample_size | gap | 12 fresh worlds supports a gate, not an effect estimate | Larger fresh set in the swarm stage |
| agent_context | pass | Byte-identical prompts and inputs; thinking blocks filtered and not stored as answers | n/a |
| data_integrity | pass | 72/72 requests verified against the frozen manifest; complete journal | n/a |
| resources | pass | $1.495 actual vs $30 cap; one dedicated box, exclusive claim | n/a |
| reproducibility | gap | No temperature control is possible on this model; reruns may differ | Report run-to-run variation if repeated |
| visualization | pass | Mapping `d1-opus-call-ledger-v1`: hub counter timeline and per-group final table; no swarm state to animate | n/a |

## Failures and causes

No execution failures in `d1o-a1`. Earlier, the first zero-model rehearsal launch stopped before execution
because the CLI child lacked the `swarm_report` import path; the launcher was repaired and the rehearsal rerun
(DEPLOYMENT.md). Both attempts are preserved.

## Next run

Fresh v3 swarm qualification on Opus (`dmarz/v3-q0-opus`, sim-dmarz-9): same shape as `v3-q0-a1` on fresh world
ids (not 20001–20006, 50001–50006, 52001–52012 or 30000–30023), the D1-Opus request path ported into `bench_v3`
(the pinned runner still sends temperature 0 and a 2,000-token cap), F1/F2 scoring fixes (swarm-lab 6563e28)
pinned, a new launch manifest and pre-run review on main, and a claim scoped to that run. Claim
`dmarz-d1-opus` was released at 08:05:21 UTC (agentops PR #221) so the box can be reused.
