# Post-mortem for sybil-split-opus, chain 001

Status: scientific assessment complete for the declared exploratory scope.

- Study / owner / stage / attempt / parent / assessed at: sybil-split-opus / dmarz / S0 → P0 → Q0 → S1 / chain-001 (batches s0-001, p0-001, q0-001, s1-001) / none (first attempt) / 2026-10-04 ~11:00Z.
- Assessor and scope: dmarz/orchestrator-2, the operating agent that launched the chain (dmarz researcher). Package built by dmarz/pipeline-split for dmarz/pipeline; same-researcher check by dmarz/fleet-monitor. Cross-researcher review waived by dmarz; **this run is not independently reviewed**.
- Pre-run assessment and frozen inputs: [chain-001-pre.md](chain-001-pre.md); launch commit `75d516952ab847aa90fe14cc30569a83f6b9d5e7` (code `0b8a444a`), source hash `95889beafbd40142ea68c52b4a00e2b1dbbbc10794f967cba3e00ca1767f3089`; model `claude-opus-5-5`, effort low, max_tokens 8,000, 4 requests in flight; READY.yaml selftests 55 (server setup ran 55/55 OK).
- Outputs: [RESULTS.md](../RESULTS.md); sanitized records in [records/](../records/) (per-stage summary and analysis, S1 episodes, S1 cell table, chain status with server paths redacted, verify summary). Raw results directories were copied read-only to git-ignored `~/swarm-lab-lanes/split-post-data/` on orbital-one.
- Review verdict: **complete_valid_result**.
- Execution: complete. Response validity: 2,749/2,749 valid. Qualification: passed (S0, P0, Q0). Scientific conclusion: positive primary contrast well above the useful size (exploratory); reversed under the unreliable-check stress condition. Process compliance: pass with notes below. Artifact delivery: verified against the hub.

## Reconcile the recorded facts

| Quantity | Assigned or planned | Observed | Missing, partial or uncertain | Evidence |
|---|---|---|---|---|
| Independent roots and paired arms | S1: 24 ring (8233–8256) + 24 community (8351–8374) × 56 conditions; Q0: 6 shapes × 10 roots; P0: engineering root 4919; S0: 32 engineering roots | all 48 roots complete in every S1 cell; Q0 60/60; P0 1/1; S0 1,853/1,853 | none | records/s1-analysis.json `denominators` |
| Started / terminal / graded / analyzed | S0 1,853; P0 1; Q0 60; S1 2,688 | equal to planned at every stage | 0 invalid, 0 failed, 0 not started | records/*-summary.json |
| Model calls and transport attempts | 2,749 calls (cap 2,749) | 2,749 calls; 2,749 transport attempts (0 retries; no 429/529) | none | records/chain-status.json `ledger` |
| Tokens (input / output) | — | P0 4,455 / 38; Q0 250,964 / 2,644; S1 10,108,086 / 193,913; total 10,363,505 / 196,595 (thinking tokens billed as output, included) | none | per-stage summaries |
| Actual spend / reservations / authority | expected USD 45–60; cap USD 190 | P0 USD 0.018580; Q0 USD 1.056736; S1 USD 44.310604; total **USD 45.38592**; reservations 482.82 cumulative, all settled, 0 open | none | ledger via `status` |
| Wall time, concurrency, machine | 50–80 min expected; 4 in flight; one exclusive server | chain started 10:11:59Z; P0 10:13:43–10:13:47Z; Q0 10:13:48–10:14:46Z; S1 2,126 s (~35 min), ended ~10:51Z; sim-dmarz-13 under claim `dmarz-sybil-split-opus` (agentops #253), released 10:51:57Z | none | records/chain-status.json |

- Reconciliation differences, duplicates and exclusions: none. 1,901 distinct packets among 2,688 S1 assignments; 767 packets recur across cells (1,554 calls), as the preregistration anticipated; they are not treated as extra roots.
- Cost estimate versus actual: USD 45.39 against a USD 45–60 estimate.
- Readback: `verify` (exit 0) passed every check for every stage (manifest match, packet hashes, regrading, summary and analysis recomputation, hub metrics/status/artifact match).
- Corrections to generated facts: none.

## Interpret the result

- **Primary contrast** (informative checks, 12 checks; degree 27−1 minus coverage 27−1, rare-skill wrong answers): **+41.0 percentage points**, descriptive 95% bootstrap interval +27.8 to +54.9 (10,000 root draws within family, seed 20261004). Ring +50.0, community +31.9. Components: degree +48.6 (7.6% → 56.2%), coverage +7.6 (0.0% → 7.6%). Prediction (positive, 10-point useful size): observed, about four times the useful size.
- Secondary: at 4 checks +50.7; on accuracy −20.8; same-packet plurality +44.4 (the model's primary matches the scripted rule); the same difference-in-differences with `random` in place of `coverage` +45.8; random minus coverage −4.9 (interval includes 0).
- **Stress condition:** with unreliable checks (attacker pass 0.9) the primary is −52.8 (−70.2 to −34.0). A single attacker hub passes its checks and dominates; splitting dilutes it under `degree` and enlarges it under `coverage`. The direction was anticipated by the scripted calibration (−0.16) but the magnitude, especially in the community family (−86.1), is larger.
- Model behaviour: Opus abstains much more than plurality where fabricated rows are the only rare-skill evidence (model minus plurality on wrong answers −30.6 points on average), which is why `no_verification` wrong answers stay near 41–57% instead of higher.
- Supported claim, deviations and limits: see RESULTS.md. No deviation from the frozen plan; no held-out exposure.

## Assess experiment quality

| Dimension | Status | Finding and evidence | Next action / acceptance check |
|---|---|---|---|
| question | pass | One manipulated factor (identity count at fixed attacker rows, edges and checks); honest world identical across k within a root (S0 invariants, 0 violations) | — |
| scenarios | gap | One population size, one fabrication type, one attachment rule; attacker-internal links free and k-dependent | Successor with no-internal-link and degree-matched attacker variants, and a faithful published-defense comparator before any comparative claim |
| controls | pass | `random` at equal checks; no-check baseline; same-packet plurality and identity plurality per cell | — |
| capability | pass | Q0 60/60, all six shapes including multirow fixtures at 100% field accuracy and exact packets, all 40 withheld fields null | — |
| measurement | pass | Evaluator-only truth; grades recomputed by verify | — |
| sample_size | pass (descriptive) | 24 roots per family; primary interval width 27 points against a 41-point effect | Secondary cells near zero remain imprecise |
| agent_context | pass | Single-call synthesizer; prompt does not mention manipulation, truth or ownership | — |
| data_integrity | pass | verify all checks; committed records contain no server paths (redacted to `<study-base>`) or credentials | — |
| resources | pass | USD 45.39 of a 190 cap; 0 retries; ~40 min chain | — |
| reproducibility | pass | Pinned commit and source hash; per-stage records committed; raw records retained on orbital-one | — |
| visualization | gap | Hub artifacts (initial/progress/final frames, 33-frame replay) verified by checksum; browser playback on the public site not checked | Open the S1 run page and play the replay |

## Resolve issues and prior suggestions

| Issue | Decision | Evidence | Repair | Acceptance | Owner / status |
|---|---|---|---|---|---|
| Launch held until the workspace Opus load fell | Accepted | fleet-monitor timing request: sybil-scale-xl's main stage was expected to exceed the 5M input-token/min limit; chain started 10:11:59Z after scale-xl's main stage stopped | — | 0 retries, 0 failures | closed |
| Account credit ran out ~10:07–10:11Z (affected another lane) | Not affected | Split's paid calls started 10:13:43Z, after credit returned; 0 failures | Credit errors are not covered by the retry rule; a credit stop would end the stage | — | noted for dmarz/pipeline |
| `run-ready-chain.py --source` default | Noted on #248 | Operator passed `--source dmarz/orchestrator-2` | Default from the claim's `by` field | — | dmarz/pipeline, open |

## Next run

The result supports building the comparator the source plan requires before any comparative claim: a faithful published Sybil-defense admission rule (for example a SybilGuard/SybilLimit-style random-route check) in the same fixed-resource grid, plus the no-internal-link attacker variant as a second treatment. The unreliable-check reversal deserves its own question (when does concentration help an attacker that passes checks?). Any successor is a new study with fresh roots and its own pre-run review; this attempt is closed.
