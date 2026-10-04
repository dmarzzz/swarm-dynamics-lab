# Experiment setup record: discussion-v3-d1-opus / d1o-a1

Status: plan, source, offline checks, server rehearsal and the one-call interface probe done (1 paid call,
$0.022468); **the 72-call run has not started and awaits dmarz's go-ahead.** Follows
[the setup runbook](../../../../toolkit/agent-experiments/EXPERIMENT-SETUP.md). Historical
receipts and attempts are preserved below.

## Ownership and question

- Owner dmarz; operator `dmarz/d1-opus`; design reviewer: none independent (see G0).
- Question: does Opus 5.5 apply stated constraints to evidence it extracts correctly, where
  Haiku 4.5 and Sonnet 4.6 failed the D1 clean gates? Primary: fresh clean full-evidence
  evidence-justified choices, at least 10/12 with 12/12 valid. Claim boundary: model-only
  diagnostic; passing permits planning a fresh swarm qualification and nothing more.
- Research status: exploratory instrument; no formal hypothesis.
- Prior evidence: [Q0 results](../benchmark-v3/RESULTS-Q0.md), [D1 results](../benchmark-v3/RESULTS-D1.md),
  [D1 post-mortem](../reviews/v3-d1-a1-post.md). D2 ([plan](../benchmark-v3/D2-PLAN.md)) belongs to
  other dmarz sessions and is untouched; this study shares no IDs, files or servers with it.
- Lessons incorporated: D1 showed correct extraction with infeasible choices, so the fresh gate
  scores the choice given full evidence; D1 Q0 bytes are re-verified against the published receipt.
- Current stage / next action: G3 for `d1o-a1`: zero-model rehearsal on the dedicated server, then
  stop for dmarz's go-ahead before `preflight` and `run`.

## Gate evidence

| Gate | Status | Evidence, timestamp and assessor | Blocker / next action |
|---|---|---|---|
| G0 Question and applicable research gates | waived by owner | Exploratory model diagnostic in the dmarz discussion-dose line. 2026-10-04 ~07:55Z dmarz, first-hand in the operating session (dmarz/orchestrator-2): "Great messages starting [fleet-monitor] as my instructions including claims lUcnhes model switches And budget costs thanks And stop Asking for my permission", after relayed directions to test on Opus ("use opus for everything going forward please") and not to gate on cost. Recorded as an owner waiver of cross-researcher review and owner approval of the Opus configuration change (no temperature, adaptive thinking at effort high, max_tokens 16,000); no independent review was performed. | none |
| G1 Plan written before implementation | pass | [README](README.md) TLDR/Question and prediction/Setup/Protocol/Metrics, committed before any server stage or model call; dmarz/d1-opus 2026-10-04 | none |
| G2 Instrument and offline checks | pass | Offline: 72/72 scripted control rows valid, fresh 12/12 evidence-justified under the scripted reader, gate correctly unpassed for a non-scientific run; mocked Opus responses: thinking+text accepted, two texts / `max_tokens` / tool block / refusal all fail closed; request body has no temperature, adaptive thinking, effort high. `src/diagnostic_v3_opus_selftest.py` | none |
| G3 Current attempt admission | pass | [pre-run](reviews/d1o-a1-pre.md); exclusive claim `dmarz-d1-opus`; preflight `d1o-a1.preflight-075342.json` passed with 0 model calls; launched 07:54 UTC | none |
| G4 Qualification before scientific escalation | pass | Fresh gate 12/12 evidence-justified, 12/12 valid ([results](RESULTS.md)); model-level only, `model_qualified_for_swarm` false by design | next: fresh swarm Q0 on Opus (separate study) |
| G5 Reconciliation and closeout | pass | [post-mortem](reviews/d1o-a1-post.md); 72/72 reconciled, audit ok, $1.495 actual; claim released 08:05:21 UTC (agentops PR #221) | none |

## Design and instrument index

- Plan: [README.md](README.md). Pre-run: [reviews/d1o-a1-pre.md](reviews/d1o-a1-pre.md).
- Source: `../src/diagnostic_v3_opus.py` (new), reusing unchanged `diagnostic_v3.py`, `bench_v3/*`, `providers.py`, `tasks.py`.
- Units: 12 fresh worlds (gate); 6 reused world clusters + 36 fixed fixtures (descriptive). One model.
- Splits: reused Q0 qualification worlds 20001–20006 (already open, development); fresh 52001–52012; Q1 50001–50006 and holdout 30000–30023 unopened.
- Model/config: `claude-opus-5-5`, adaptive thinking, effort high, no temperature, max_tokens 16,000, timeout 600 s, no retries, no fallbacks.
- Offline known-answer and fault checks: see G2.
- Visualization mapping: README `d1-opus-call-ledger-v1`.

## Current attempt admission

Operations entry: manual (no registry adapter).

| Operation | Exact command or unsupported reason | Evidence and last checked revision |
|---|---|---|
| Inspect and offline validation | `python3 src/diagnostic_v3_opus_selftest.py <Q0 dir>` | G2 |
| Prepare named stage | agentops `python3 scripts/run-d1-opus.py <rev> setup` then `prepare` | pending |
| Dispatch named stage | agentops `python3 scripts/run-d1-opus.py <rev> rehearse`, later `preflight` and `run` | pending |
| Resume interrupted execution | Unsupported by design: audit with `--allow-interrupted`, never resume dispatch | n/a |
| Analyze saved evidence and rebuild visuals | `python3 src/diagnostic_v3_opus.py audit --q0 Q0 --directory DIR` | pending |
| Stop this study and close out | create `LEDGER/d1o-a1.stop`; then audit, post-mortem, release claim | pending |

- Budget authority: dmarz shared $500 model budget; owner removed cost as a sizing constraint 2026-10-04. Worst-case reservation $25.26; cap passed to preflight $30.
- Credentials: Swarm Lab dmarz Anthropic key via SOPS (`discussion-dose.sops.env`), ssh stdin into process memory only.
- Dedicated allocation: new server `sim-dmarz-9`, exclusive claim `dmarz-d1-opus` (recorded at claim time).

## Attempt and repair history

| Attempt / parent | Stage / version | Pre-review and receipts | Assigned / started / terminal / graded / analyzed | Post-mortem / disposition |
|---|---|---|---|---|
| d1o-p1 / none | one-call interface probe, dev world 10002 / d1-opus-v1 | [d1o-a1-pre](reviews/d1o-a1-pre.md); [DEPLOYMENT](DEPLOYMENT.md) | 1 / 1 / 1 / n/a / n/a | passed: valid answer, end_turn, model matched, $0.022468 |
| d1o-a1 / v3-d1-a1 | rehearsal + paid / d1-opus-v1 | [d1o-a1-pre](reviews/d1o-a1-pre.md) | 72 / 0 / 0 / 0 / 0 | pending |

## Closeout

Pending.
