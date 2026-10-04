# SOC-07 v2: private first judgments on a harder three-option task

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by dmarz/orbital-orchestrator; source `9781739c` ([registry](../../../../experiments/evidence-metadata.json), [rubric](../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **0/4** — Untested: on a task where first answers disagree, keeping first judgments private changes team decision accuracy relative to publishing them. Basis: Prepared successor design only; no v2 run exists. Built because v1 replay on Opus 5.5 reached team success 1.00 in both arms. Five agents, repeats and calls are not independent observations.
- **sample_size_summary:** Observed: none. Planned: 12 qualification worlds; 24-world replay and 24-world live pilots, 2 repeats each; 192 replay and 240 live episodes; 4,765 calls.
<!-- experiment-evidence:end -->

Owner: dmarz. Operator: dmarz/orbital-orchestrator. Hub experiment: `soc07-private-judgments-v2`. Status: **prepared, not launched**. Exploratory development study; cross-researcher review waived by dmarz ([launch/review-waiver.md](launch/review-waiver.md)). Predecessor: [soc07-private-judgments](../soc07-private-judgments/README.md) (design v1). Setup record: [SETUP.md](SETUP.md). Pre-run assessment for the whole chain: [reviews/chain-001-pre.md](reviews/chain-001-pre.md). Preregistered comparison and stop rules: [preregistration.md](preregistration.md).

## TLDR

Five agents choose one of three fictional suppliers from eleven dated records, some of which are superseded estimates or audits that a later audit revises. In the two minority regimes, one agent (informed minority) or four agents (correctable minority) hold the audits; the rest hold only estimates, which point to a different supplier. Each agent gives a first answer alone. The team then discusses once with the first answers kept private (PRIVATE) or published (PUBLIC), plus three diagnostic arms, and votes. Primary contrast: PRIVATE minus PUBLIC team success. v2 exists because v1 hit a ceiling on Claude Opus 5.5 (team success 1.00 in both arms at the replay stage), so the comparison carried no information. Model: Claude Opus 5.5, adaptive reasoning at effort medium, unchanged from v1 manifest m3.

## Why v2

v1 S1-R (`soc07-private-judgments/807dfab8`, 2026-10-04, Opus 5.5 manifest m3) completed 192 of 192 episodes with 672 of 672 valid calls and team success 1.00 in PRIVATE and 1.00 in PUBLIC: difference 0.000 (measured). With every team correct in both arms the comparison cannot move, so S1-L on the same task was expected to return a null by construction. That is a statement about task difficulty for this model, not evidence that disclosure does not matter (results analyst, relayed by dmarz/fleet-monitor). v1's S1-L runs to completion as launched; its results are not pooled with v2.

v2 changes the task, not the model:

| v1 | v2 |
| --- | --- |
| Two options (A, B) | Three options (A, B, C); labels rotate across repeats |
| Five records: four estimates and one audit | Eleven records: nine estimates (each option's cost and delivery, plus one earlier estimate per option that a later estimate supersedes) and two audits |
| One audit | Two audits. Pattern `conflict`: the second audit revises the same value as the first, so the first audit, read alone, points to a wrong option. Pattern `independent`: the audits touch different values and only one of them changes the answer |
| Cost margins 1-3, 4-10, 11-20 | Cost margins between the winner and the next-cheapest on-time option 1-2, 3-5, 6-9 |
| No boundary cases by design | Every third world of a regime is a deadline-boundary world: the winner's latest delivery equals the deadline |
| No runtime check that first answers disagree | Manipulation check: share of minority-regime live episodes whose first answers are not unanimous; below 50% the comparison is declared uninformative and S1-L fails its `informative` gate |
| Stages S0, S1-Q, S1-R, S1-L | S0, **P0 one-call interface probe**, S1-Q, S1-R, S1-L, chained under software gates |

Seeds are new (development root 731071, holdout 731072, bootstrap 731073), so no v1 world is reused. The study has its own ledger and its own USD 150 cap.

## Question and prediction

Question: when agents hold conflicting evidence, does keeping first answers private until after one discussion round change the correctness of the team's final vote, compared with publishing them first?

Prediction (exploratory, not a registered hypothesis): on a task hard enough that first answers disagree, PRIVATE is at least as good as PUBLIC in the correctable-minority regime and better in the informed-minority regime, where publishing four wrong first answers can pull the informed agent and the discussion toward the majority. A valid null is a result. An adverse result (PUBLIC better) is a result. The study is uninformative if first answers rarely disagree in the minority regimes (manipulation check below threshold), if both arms sit at ceiling again, or if validity gates fail.

## Setup

- Model: `claude-opus-5-5`, adaptive reasoning, `output_config.effort` medium, 4,096-token reasoning allowance added to each phase's visible cap (256 / 256 / 64 / 64, qualification 128), no temperature (the model rejects it). USD 4 / 20 per million input / output tokens. Settings in `execution.json` `launch_manifest` (version m3, copied from v1).
- Task generator: `src/generate.py`. A world's truth is keyed by stage and world index only. Rejection sampling enforces regime, kind (cost-decided or feasibility-decided), cost-gap bin, audit pattern, boundary flag, decisiveness, and a unique answer under both the estimates alone and the full records. An independent solver (`src/score.py` `solve`) re-derives every answer key.
- Regimes: clean (every agent holds all eleven records), informed minority (one agent holds all eleven, four hold the nine estimates), correctable minority (four hold all eleven, one holds the nine estimates). In both minority regimes the estimates-only answer differs from the correct answer in every world.
- Arms: PRIVATE, PUBLIC, NEVER (keep the first answer), PREPARE (inventory instead of a first answer), VOTE (no discussion). Shared first pass for PRIVATE, PUBLIC, NEVER and VOTE.
- Sizes (unchanged from v1): S1-Q 12 worlds, 1 call each; S1-R 24 worlds x 2 repeats, one focal model agent with four scripted peers, 672 calls; S1-L 24 worlds x 2 repeats x 5 arms x 5 agents, 4,080 calls.

## Protocol

One chained launch on a fresh dedicated server (operator runbook in [SETUP.md](SETUP.md)):

1. S0: scripted fixtures, zero model calls; 60 worlds, four scripted policies, fault injections. Must pass every check.
2. P0: one qualification call on S0 fixture world 0 (not an S1 world) at the frozen settings. Passes only if the response parses, ends `end_turn` and equals the key.
3. S1-Q: 12 single-solver calls on fresh worlds; gate at least 10 correct and 11 valid.
4. S1-R: controlled replay; gates as v1 (parse-valid at least 95%, truncation at most 5% per phase, budget and timeout failures under 5%, zero leaks, clean-regime competence at least 13 of 16 in PRIVATE and PUBLIC).
5. S1-L: live teams; v1 gates plus `informative` (manipulation check at least 50%).

Each stage is one hub run and starts only if the previous stage ended `done` with `gate_passed = 1` at the same runtime fingerprint (`src/coordinator.py`). A failed gate stops the chain. Nothing is retried except HTTP 429 and 529 (two retries, as v1).

## Metrics

- Primary: PRIVATE minus PUBLIC public-team success over all assigned S1-L episodes, equal weight per regime, world-cluster bootstrap (as v1).
- Manipulation check (reported for S1-R and S1-L; gate for S1-L): share of minority-regime PUBLIC episodes whose valid first answers are not unanimous.
- Ceiling report: team success rate per arm and regime, and an `at_ceiling` flag when PRIVATE and PUBLIC are 1.00 in every regime.
- Secondary (as v1): useful and harmful revisions, designated-minority correction, stale citations (now: citing any superseded record without the record that superseded it), token ratio.
- Every run reports `model_calls`, `input_tokens`, `output_tokens` and `cost_usd` to the hub.

## Cost estimate

Measured basis: v1 S1-R on Opus 5.5 cost USD 5.24 for 672 calls (USD 0.0078 per call; 1.03 million input and 56,000 output tokens, about 1,530 input and 83 output tokens per call). v2 requests are 1.13 to 1.25 times v1's size by bytes (measured on rendered contexts). Assuming reasoning output doubles to roughly 170 tokens per call on the harder task (an assumption, not a measurement):

| Stage | Calls | Estimate |
| --- | --- | --- |
| P0 | 1 | about USD 0.01 |
| S1-Q | 12 | about USD 0.1 |
| S1-R | 672 | about USD 8 |
| S1-L | 4,080 | about USD 47 |
| Total | 4,765 | about USD 55; USD 45 to 80 if reasoning output is two to four times v1's |

The USD 150 study cap is a runaway guard (cost is not a gate per dmarz). Call caps per stage are hard.
