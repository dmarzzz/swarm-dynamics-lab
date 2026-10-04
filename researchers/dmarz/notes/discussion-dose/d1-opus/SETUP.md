# Experiment setup record: discussion-v3-d1-opus / d1o-a1

Status: plan, source and offline checks committed; zero-model rehearsal pending on the dedicated
server; **no model call made; paid dispatch awaits dmarz's go-ahead.** Follows
[the setup runbook](../../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md). Historical
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
| G0 Question and applicable research gates | pending (owner decision) | Exploratory model diagnostic in the dmarz discussion-dose line; Dan's direction relayed by fleet-monitor ~07:20Z 2026-10-04 ("I would like to start testing with a strong model like opus or something like that"). Relayed, not first-hand. No cross-researcher review performed. | dmarz confirms first-hand and records a review decision (waiver or review) before paid dispatch |
| G1 Plan written before implementation | pass | [README](README.md) TLDR/Question and prediction/Setup/Protocol/Metrics, committed before any server stage or model call; dmarz/d1-opus 2026-10-04 | none |
| G2 Instrument and offline checks | pass | Offline: 72/72 scripted control rows valid, fresh 12/12 evidence-justified under the scripted reader, gate correctly unpassed for a non-scientific run; mocked Opus responses: thinking+text accepted, two texts / `max_tokens` / tool block / refusal all fail closed; request body has no temperature, adaptive thinking, effort high. `src/diagnostic_v3_opus_selftest.py` | none |
| G3 Current attempt admission | pending | [pre-run](reviews/d1o-a1-pre.md); claim and rehearsal receipts recorded in DEPLOYMENT once done | rehearsal, then dmarz go-ahead, then preflight under 30 min |
| G4 Qualification before scientific escalation | pending | Fresh gate is the qualification signal; no escalation is authorized by this study | n/a until results |
| G5 Reconciliation and closeout | pending | | after the run |

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
| d1o-p1 / none | one-call interface probe, dev world 10002 / d1-opus-v1 | [d1o-a1-pre](reviews/d1o-a1-pre.md) | 1 / 0 / 0 / n/a / n/a | pending |
| d1o-a1 / v3-d1-a1 | rehearsal + paid / d1-opus-v1 | [d1o-a1-pre](reviews/d1o-a1-pre.md) | 72 / 0 / 0 / 0 / 0 | pending |

## Closeout

Pending.
