# Post-mortem for sybil-scarcity-opus, chain 001

Status: scientific assessment complete for the declared exploratory scope.

- Study / owner / stage / attempt / parent / assessed at: sybil-scarcity-opus / dmarz / S0 → P0 → Q0 → S1 / chain-001 (batches s0-001, p0-001, q0-001, s1-001) / none (first attempt) / 2026-10-04 ~10:20Z.
- Assessor and scope: dmarz/orchestrator-2, the operating agent that launched the chain (dmarz researcher). Package built by dmarz/pipeline-scarcity for dmarz/pipeline; same-researcher check by dmarz/fleet-monitor. Cross-researcher review waived by dmarz; **this run is not independently reviewed**.
- Pre-run assessment and frozen inputs: [chain-001-pre.md](chain-001-pre.md); launch commit `3ebef1ce9838fca753adbb60fab9132d00e14497` (code `30e34577`), source hash `b37af99708c5f37740de3b21c7e82d5f9292584b236f0fcf30e7619e2efc58be`; model `claude-opus-5-5`, effort low, max_tokens 8,000, 2 requests in flight; READY.yaml selftests 33.
- Outputs: [RESULTS.md](../RESULTS.md); sanitized records in [records/](../records/) (per-stage summary and analysis, S1 episodes, S1 cell table, chain status with server paths redacted, verify summary). Raw results directories were copied read-only to the git-ignored `data/sybil-scarcity-opus/` on orbital-one.
- Review verdict: **complete_valid_result**.
- Execution: complete. Response validity: 1,489/1,489 valid. Qualification: passed (S0, P0, Q0). Scientific conclusion: large, precisely estimated decrease in the primary contrast (exploratory). Process compliance: pass with notes below. Artifact delivery: verified against the hub.

## Reconcile the recorded facts

| Quantity | Assigned or planned | Observed | Missing, partial or uncertain | Evidence |
|---|---|---|---|---|
| Independent world roots and paired arms | S1: 24 roots (7800–7823) × 60 conditions; Q0: 8 roots × 6; P0: engineering root 7790 | 24 roots complete in every S1 cell; Q0 48/48; P0 1/1 | none | records/s1-analysis.json (`complete_roots` 24 in all cells) |
| Started / terminal / graded / analyzed | S0 168; P0 1; Q0 48; S1 1,440 | 168/168/168/168; 1/1/1/1; 48/48/48/48; 1,440/1,440/1,440/1,440 | 0 invalid, 0 failed, 0 not started | records/*-summary.json |
| Model calls and transport attempts | 1,489 calls (cap 1,489); attempt cap 1,640 | 1,489 calls; 1,489 transport attempts (0 retries) | none | records/s1-summary.json `study_accounting` |
| Tokens (input / output) | — | P0 23,537 / 38; Q0 1,129,722 / 1,824; S1 33,751,860 / 74,360; total 34,905,119 / 76,222 (thinking tokens are billed as output and included) | none | per-stage summaries |
| Actual spend / reservations / authority | expected USD 141–155; cap USD 220 settled + open | P0 USD 0.094908; Q0 USD 4.555368; S1 USD 136.494640; total **USD 141.144916**; cumulative reservations 381.03 all settled, 0 open | none | ledger via `status` |
| Wall time, concurrency, machine | 45–80 min expected; 2 in flight; one exclusive server | chain 09:17:37Z → 09:59:31Z (≈42 min): S0 36.5 s, P0 3.3 s, Q0 65.4 s, S1 2,339.7 s (mean latency 2.8 s); sim-dmarz-2 under claim `dmarz-sybil-scarcity-opus` (agentops #249) | none | records/chain-status.json |

- Reconciliation differences, duplicates and exclusions: none. 1,207 distinct packets among 1,440 S1 assignments; identical packets in different cells are recorded by hash and are not treated as extra worlds (preregistration item 4).
- Cost estimate versus actual: USD 141.14 actual against a USD 141–155 estimate; no open exposure.
- Readback: `verify` (exit 0) passed every check for every stage: manifest match, packet hashes, regrading, summary and analysis recomputation, hub metrics/status/artifact match.
- Corrections to generated facts: none.

## Interpret the result

- **Primary contrast** (random, 108 checks, attacker pass 0.1, one minus eighty-one carriers): **−95.8 percentage points**, descriptive 95% bootstrap interval −100.0 to −88.9 over 24 roots (10,000 root-level draws, seed 20261004); 22 of 24 roots at −100. Prediction (decrease, 10-point practical marker): observed, at about ten times the marker.
- Graded contrasts in the same cell: 3 − 81 −86.1 (−95.8 to −75.0); 9 − 81 −45.8 (−61.1 to −30.6); 27 − 81 −4.2 (−8.3 to 0.0).
- Anchor: at 81 carriers (byte-identical to the sybil-scale-api packet) Opus scored 100% in the primary cell, consistent with the earlier 98.6% Haiku result.
- Diagnostics (evaluator-only): at one carrier a truthful report was admitted for 46/72 rare facts, but Opus answered only 3 of those 46 correctly, gave the attacker's value 94% of the time and abstained 1%. Same-packet scripted plurality scored 3%. Admitted packets held about 0.6 truthful and 5.7 fabricated reports per rare fact; accuracy rises as truthful reports approach and pass the fabricated count (54% at 9 carriers, 96% at 27). Reading, not a verified mechanism: the synthesizer weighs agreeing reports roughly by count, so the earlier high accuracy depended on repetition.
- Secondary: with weak checks (attacker pass 0.9) random auditing at 64 or 108 checks scores 0% below 81 carriers and 27.8% at 81; coverage with 4 checks scores 0% everywhere. Policy-by-rarity interactions are listed in RESULTS.md; most are driven by coverage's poor 81-carrier performance at low budgets.
- Supported claim (exploratory, this synthetic task and configuration): reducing truthful carriers of a rare fact from 81 to 1, with population, graph, audits, admission and attacker reports held fixed, reduces Opus 5.5 specialist accuracy from 100% to about 4%. Not supported: any claim about real Sybil defenses, other attacker strategies, other graph families, or other models.
- Deviations: none from the frozen plan. No held-out exposure.

## Assess experiment quality

| Dimension | Status | Finding and evidence | Next action / acceptance check |
|---|---|---|---|
| question | pass | One manipulated factor (carriers) with everything else frozen; invariance 288 matched cells, 0 violations | — |
| scenarios | gap | One graph family, one fabrication strategy, simulated checks | A successor varying attacker strategy (e.g. spread fabrications) or graph family; acceptance = its own frozen plan |
| controls | pass | 81-carrier cell is the unmodified parent packet; same-packet scripted plurality reported per cell; random vs coverage at equal checks | — |
| capability | pass | Q0 48/48, every profile including 1 carrier at 100% field accuracy and 24/24 withheld-field abstention on clean packets | — |
| measurement | pass | Evaluator-only truth; grades recomputed by verify | — |
| sample_size | pass (descriptive) | 24 paired roots; primary interval width 11 points against a 96-point effect | Secondary cells with smaller effects remain imprecise; no confirmatory claim |
| agent_context | pass | Actor inputs leak-free (S0 invariant `actor_inputs_leak_free`); single-call synthesizer, no memory | — |
| data_integrity | pass | verify all checks; no secrets or endpoints in committed records (server paths in chain-status redacted to `<study-base>`) | — |
| resources | pass | USD 141.14 of a 220 cap; 0 retries; ~42 min | — |
| reproducibility | pass | Pinned commit and source hash; per-stage records committed; raw records retained on orbital-one `data/` | — |
| visualization | gap | Hub artifacts (initial/progress/final frames, 33-frame replay) verified by checksum; browser playback on the public site not checked | Open the S1 run page and play the replay; acceptance = frames match records/s1-cells.csv |

## Resolve issues and prior suggestions

| Issue | Decision | Evidence | Repair | Acceptance | Owner / status |
|---|---|---|---|---|---|
| Chain log ends with a `Terminated` traceback | Accepted as benign | Raised by `src/chain.py` line 309 `terminate()` inside a multiprocessing pool worker when the preparation pool is shut down; the chain kept dispatching and finished all stages; `status` showed `chain_active: true` throughout | Suggest the chain suppress the pool-shutdown traceback so `status` log tails do not look like a crash | A future chain log ends with the completion line | dmarz/pipeline, open (cosmetic) |
| `run-ready-chain.py --source` defaults to dmarz/orbital-orchestrator | Noted on #248 | Operator passed `--source dmarz/orchestrator-2` | Default from the claim's `by` field | Hub source equals claimant without the flag | dmarz/pipeline, open |
| `setup` wall time 5m22s vs 2–3 min estimate | Noted | launch transcript | Update the runbook estimate | — | dmarz/pipeline, open |
| Retry exposure (analyst LESSONS item 8) | Mitigated by design | 2 retries for 429/529; 0 used | — | — | closed |

## Closeout and handoff

- Scientific assessment: this file and RESULTS.md, dmarz/orchestrator-2, 2026-10-04.
- Evidence metadata: registry row updated to score 2 for this scoped cohort.
- Remaining gaps: scenario breadth (attacker strategy, graph family), browser replay check.
- Next decision: the result is complete and valid; no repair or rerun. A successor, if wanted, should test whether a synthesizer instructed or structured to discount repeated identical claims (or a provenance-aware merge) recovers rare truth at low carrier counts, holding this world fixed. That needs its own plan and pre-run review (dmarz/pipeline).
- Workers: chain process exited (`chain_active: false`); uploads verified; claim `dmarz-sybil-scarcity-opus` released (status done on agentops main). Server not destroyed.
