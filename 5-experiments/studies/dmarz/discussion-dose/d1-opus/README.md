# D1-Opus: the D1 instrument on Claude Opus 5.5

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by dmarz/d1-opus; source `9781739c` ([registry](../../../../evidence-metadata.json), [rubric](../../../../EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **2/4** — Under adaptive thinking at effort high with no temperature, Claude Opus 5.5 makes evidence-justified choices on clean full-evidence D1-style decisions where Haiku 4.5 and Sonnet 4.6 failed. Basis: Measured: fresh gate 12/12 evidence-justified and 12/12 valid; 6/6 on the reused worlds versus Haiku 2/6 and Sonnet 3/6 on byte-identical requests; exact-source audit recomputed all 72 outcomes. Limits: model and request configuration changed together; 12 fresh clean worlds only; report packets remain Haiku-generated; all 6 inherited false memory facts were still accepted; no swarm stage.
- **sample_size_summary:** Observed: 72/72 assigned calls valid and analyzed, 0 refusals, 0 missing usage: 12 fresh clean worlds (gate units), 6 reused development world clusters (6 full-evidence, 18 report ballots), 36 fixed memory fixtures; not 72 independent samples. One model, one attempt.
<!-- experiment-evidence:end -->

Prospective plan, 2026-10-04 UTC. Owner dmarz, operator `dmarz/d1-opus`. Attempt `d1o-a1`,
hub experiment `discussion-v3-d1-opus`. Parents: [Q0](../benchmark-v3/RESULTS-Q0.md) and
[D1](../benchmark-v3/RESULTS-D1.md). Setup record: [SETUP.md](SETUP.md). Pre-run assessment:
[reviews/d1o-a1-pre.md](reviews/d1o-a1-pre.md). Status: **plan committed; no model call made.**

## TLDR

D1 gave Haiku 4.5 and Sonnet 4.6 the same 60 retained Q0 requests. Both extracted every fact
correctly from clean full evidence and then chose infeasible options (Haiku 2/6 correct, Sonnet
3/6), so neither cleared the 5/6 gates. Per dmarz's direction to start testing a strong model
where Haiku or Sonnet failed a gate, this study sends the same 60 requests once each to
`claude-opus-5-5`, plus 12 fresh clean full-evidence decisions on worlds 52001–52012 that no
model has seen. 72 calls, one worker, no retries. This is a separately labelled configuration,
not a D1 arm and not D2: Opus 5.5 rejects `temperature` and cannot disable thinking, so the
request configuration changes along with the model.

## Question and prediction

Does a stronger model apply the stated constraints to evidence it extracts correctly?

- **Fresh gate (primary):** of 12 fresh clean full-evidence decisions, at least 10 evidence-
  justified choices with all 12 responses valid. Passing makes Opus eligible for a separately
  planned fresh swarm qualification; it does not qualify Opus for the swarm and does not start one.
- **Development comparison (secondary, descriptive):** on the six reused full-evidence worlds and
  the six saved-report quorums, compare Opus with the D1 Haiku (2/6, 1/6) and Sonnet (3/6, 3/6)
  counts, paired by identical actor request. Memory-fixture outcomes are reported per state.
- **Prediction, written before any Opus call:** Opus reaches at least 5/6 on reused full
  evidence and passes the fresh gate (at least 10/12). It still accepts most locally supported
  false memory facts, because those fixtures reward source-consistent copying. The
  prediction is falsified if fresh evidence-justified choices fall below 10/12 or reused full
  evidence stays at or below Sonnet's 3/6. Either outcome is a valid result.

## Setup

- **Model:** `claude-opus-5-5`, confirmed with an authenticated Models API GET on 2026-10-04
  (metadata only, no inference): structured outputs supported, adaptive thinking only
  (`enabled` not supported), effort levels low–max. Price $4 input / $20 output per million
  tokens (Anthropic model table, checked 2026-10-04).
- **Configuration change versus D1 (declared, not hidden):** no `temperature` field (rejected
  by this model; D1 used 0); `thinking: {type: adaptive}` (cannot be disabled; D1 had none);
  `output_config.effort: high` (the model default is medium); `max_tokens` 16,000 because thinking
  counts toward it (D1 2,000); request timeout 600 s (D1 120 s). Prompt, system text, JSON
  schema, source policy, strict citation scoring and the 60 actor requests are byte-identical to
  D1. Thinking text is not requested (`display` omitted) and is not stored; only the single
  text block is scored. Server-side model fallbacks are not enabled, because model identity is
  the treatment; a refusal is recorded as a failure, and `stop_reason: refusal` is also counted
  as its own category. The visible text answer is capped at 8,000 characters (D1's 2,000-token
  visible ceiling); a longer answer is a recorded `provider_incomplete` failure.
- **Reused inputs:** the 60 Q0 actor requests selected by the committed
  [planning receipt](../benchmark-v3/next-run-planning-evidence.json): 6 clean full-evidence
  decisions, 18 clean post-report ballots and 36 fixed parent-memory fixtures. They are fetched
  from the hub's retained Q0 artifacts and rejected unless every file hash matches the
  [published Q0 audit receipt](../benchmark-v3/results/v3-q0-a1/analysis.json).
- **Fresh inputs:** worlds 52001–52012 from the frozen `finite-evidence-worlds-v3.0` generator,
  clean (no injected record), full evidence, built exactly as the v3 runner builds its single-
  agent diagnostic. 52001–52006 use the resolvable construction and 52007–52012 the ambiguous
  one; both have a unique clean winner. Families: 4 dependency, 4 capacity, 4 total cost. These
  IDs avoid the Q1 IDs 50001–50006 and the confirmation holdout 30000–30023, which stay closed.
  The fresh set contains no report-packet or swarm items: fresh reports would need a new swarm
  run, which is out of scope.
- **Units:** 12 fresh worlds are the independent units for the gate. The 60 reused requests sit
  in 6 world clusters plus a fixed fixture grid; they are not 60 independent samples.
- **Execution:** dedicated fleet server under an exclusive dmarz claim, source pinned to a
  public commit, one process, no transport or repair retries.

## Protocol

1. Commit source, this plan, SETUP and the pre-run assessment. `prepare` freezes a 72-call
   manifest (seeded order `d1-opus-v1-schedule`) with request and provider-body hashes,
   source hashes, the immutable public plan URL/hash and the worst-case reservation. Zero
   network calls.
2. On the server, `rehearse` runs the full pipeline with the scripted evidence reader and zero
   model calls, under a separate ledger prefix and hub run `discussion-v3-d1-opus/d1o-a1-rehearsal`.
   Audit and upload readback must pass.
3. Interface probe, attempt `d1o-p1`: exactly one paid call on dev world 10002 (never
   scheduled, scored or counted) checks that Opus accepts the request and returns a parsed,
   schema-valid answer. A permanent ledger marker refuses a second probe. Its cost is reported
   separately. If it fails, the 72-call run does not start and the failure is diagnosed first.
4. `preflight` (zero inference): rebuilds the manifest from committed source, re-verifies every
   serialized request, fetches the public plan bytes, checks model metadata and capabilities,
   and checks the reservation against the authorized cap. It expires after 30 minutes.
5. `run` writes a permanent attempt marker under a process lock before the first call, then
   dispatches the 72 calls once each. A returned model other than `claude-opus-5-5`, an
   accounting anomaly, a local limit, low credit, the 2-hour deadline or an owner stop file
   ends dispatch. Other provider or invalid failures are recorded and the fixed schedule
   continues. Nothing is retried or resubmitted.
6. `audit` recomputes every score and the summary from the journal under the exact source.
   Results, post-mortem and claim release follow. No D2, Q1, swarm or successor is started.

Budget: worst-case reservation $25.26 (72 × full 16,000 output tokens plus a byte bound on
input); planning estimate $4–8 actual. This sits inside dmarz's shared $500 model budget; the
owner removed cost as a sizing constraint on 2026-10-04. Actual tokens and dollars are
reported per call.

## Metrics

Per call: started, terminal, valid, dispatched, safe failure reason, HTTP class, input and
output tokens (output includes thinking), observed cost, latency, returned model.

Fresh decisions (12): evidence-justified choice (gate), truth-correct, abstain, wrong
non-abstain, constraint violation, all values extracted correctly, choice–claim consistency,
citation mismatches.

Reused development items: the D1 scores unchanged (full evidence per world, saved-report
ballots and the fixed N=3 quorum per world, memory outcomes per state), reported beside the
D1 Haiku and Sonnet results for the identical request. `model_qualified_for_swarm` is always
false here.

## Visualization mapping: d1-opus-call-ledger-v1

Bound to `discussion-v3-d1-opus/d1o-a1`. X is terminal assignment count 0–72 from service
start. Series: started, terminal, invalid, observed cost, missing usage, and fresh
evidence-justified count against the 10/12 line. The hub progress counter is the live view.
The fsynced journal is the replay source, and the final frame is the per-group outcome table.
No swarm animation: this is a single-model diagnostic with no temporal swarm state, so the
supported fallback is the counter timeline plus per-item tables. Failed and missing
observations stay visible as their own states. The scripted rehearsal has its own `-rehearsal`
run ID and is never model evidence.

## Commands

From the repository root with Python 3.12, using `src/diagnostic_v3_opus.py` in the
discussion-dose notes: `prepare --q0 Q0 --launch-owner dmarz/d1-opus --output MANIFEST`;
`rehearse --q0 Q0 --manifest MANIFEST --dispatch-ledger LEDGER --output DIR [--hub-run ...]`;
`preflight --q0 Q0 --manifest MANIFEST --max-cost-usd 30 --output PREFLIGHT`;
`run --q0 Q0 --manifest MANIFEST --preflight PREFLIGHT --dispatch-ledger LEDGER --hub-run
discussion-v3-d1-opus/d1o-a1 --output DIR`; `audit --q0 Q0 --directory DIR`. The private agentops
launcher `scripts/run-d1-opus.py` wraps these with the claim check and memory-only credentials.
