# Verification budget and verifier reliability

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by dmarz/sybil-specialists; source `1226b626` ([registry](../../../../experiments/evidence-metadata.json), [rubric](../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **2/4** — In the repeated-fact synthetic environment, the strong-check accuracy benefit replicated; random checking reached the N972 joint mean target at 64 tested checks and coverage at 108. No weaker tested checking strength met that joint target. Basis: Same-owner audit of twenty-four paired roots, competent clean controls and fully accounted outcomes supports this narrow grid result. One task family, one model, scripted identities/checks, repeated facts and unadjusted intervals limit generalization; independent review was waived and the historical immutable public-plan receipt gap is retained.
- **sample_size_summary:** Observed: 24 paired roots from one synthetic task family; 2,880/2,880 S1 outcomes analyzed, zero missing; 120 conditions at 324/972 simulated identities, one synthesizer. Q0 separately: 16/16 clean calls on four roots.
<!-- experiment-evidence:end -->

Exploratory follow-up to [sybil-scale-api](../sybil-scale-api/RESULTS.md), owned by dmarz. This is a bounded synthetic study with model synthesis, not hundreds of autonomous model agents and not an accepted formal hypothesis. The owner explicitly authorized shipping both follow-ups in parallel and waived independent review on 2026-10-04. Own planning, qualification, reconciliation and post-run assessments remain required; S2 stays disabled.

**Current status, 2026-10-04:** S1 completed all 2,880 outcomes in 120 cells on 24 paired world clusters, with zero invalid or missing outcomes. See [results and analysis](RESULTS.md), [S1 post-mortem](reviews/s1-001-post.md), [verification receipt](verification-summary.json) and [deployment closeout](DEPLOYMENT.md). Main S1 cost $39.349188; Q0 plus S1 cost $39.672176. The dated allocation and readiness entries below preserve what was planned at those earlier snapshots.

## Question

How many identity checks are needed to preserve specialist information while keeping attacker admission low, and when do unreliable checks make more verification ineffective or harmful?

The preceding experiment reached 98.6% specialist accuracy with 108 strong checks at 972 identities, while four coverage checks reached 47.2%. Equal-budget random checking also reached 98.6%; coverage had no established unique advantage. High accuracy coexisted with rejection of 62.8% of honest specialists. These observations motivate mapping budgets between the endpoints, varying check reliability and retaining the exclusion measure.

## Setup

The previous graph generator, initial trust, task, fabrication, check policy, model prompt and admission logic are preserved. Half the identities are honest core, a quarter honest outside specialists, and a quarter controlled by one attacker. Two core identities start trusted. Half the population is admitted using seeded PageRank after checks. Honest identities pass a simulated check with probability 90%; attackers pass with the assigned probability. Core identities know three facts, honest outside specialists know three other repeated facts, and attacker claims add seven to the true value. The model is `claude-haiku-4-5-20251001`, temperature zero, one structured synthesis per admitted packet, maximum 500 output tokens, no retries or tools. Truth and principal ownership never enter the model packet or checking-policy inputs.

Python 3.12 and pinned dependencies in `requirements.txt` match the prior deployed runtime. Operator deployment record supplies the source revision, host name, exclusive claim and output location. Credentials enter by alias through the private launcher only.

**Historical allocation correction, 2026-10-04, before S1:** the owner now requires one active experiment per host. Both Q0 stages are complete and their workers stopped. The planned S1 allocation keeps this budget study alone on `sim-dmarz-4`, with `dmarz-sybil-followups` narrowed to this experiment. The newcomer study will move to dedicated `sim-dmarz-sybil-newcomer`. These are planned deployment actions, not a claim that S1 has started. The two studies can still run in parallel on separate hosts. A $50/$10 budget partition preserves the combined $60 allowance using identical settled ledger checkpoints and persistent peer-allocation holds; details are in [RUN.md](RUN.md) and [DEPLOYMENT.md](DEPLOYMENT.md). Scientific conditions and the frozen runtime are unchanged; the newcomer host receives setup selftests, with no new API qualification required solely for relocation.

## Protocol

The full grid is 2 population sizes (324, 972) × 6 checking budgets (4, 8, 16, 32, 64, 108) × 5 attacker check-pass probabilities (10%, 30%, 50%, 70%, 90%) × 2 policies (random, topology coverage). Verification badges remain visible. There are 120 cells and 24 fresh paired worlds per cell: 2,880 scientific model calls.

The 24 worlds 7000–7023 are disjoint from the preceding study. Every cell reuses their deterministic truth, identity permutation and verification draws. Budgets are checkpoints along each policy's same check sequence, rather than independently resampled sequences. No assumption of monotonicity is made about checks, reliability or outcomes. Some packets can be identical across reliability labels when the underlying Bernoulli outcomes match; these are declared repeated invocations within the same world, not new independent units. Each assigned cell receives one call; repeated episode IDs are forbidden.

The ordered stages are: offline selftests; S0 scripted run of the complete grid on engineering worlds 6800–6801 plus clean controls; Q0 clean API competence on four separate worlds 6900–6903; S1 grid after exact-runtime S0/Q0 success. Q0 has no attackers and includes all reports and common-facts-only packets at both sizes (16 calls). Missing specialist facts require `null`; no check success is treated as truth. All assigned outputs, including failures and not-started rows, persist. A failed call halts new dispatch after already-running calls terminate. Paid stages never automatically replay. Holdout 10000–19999 remains closed and no S2 is implemented.

`design.yaml` and `preregistration.md` freeze the protocol. `reviews/` records own assessments, not independent approvals. `src/worker.py --hub` consumes one finite queued stage; the coordinator enforces exact runtime prerequisite qualification. See `RUN.md` for reproduction and `VISUALIZATION.md` for the UI mapping.

## Metrics

The primary endpoint replication compares 108 versus four coverage checks at N=972 and 10% attacker check-pass probability on fresh worlds. Specialist accuracy is the fraction of three specialist facts correctly recovered in the final model answer; wrong answers and abstentions score zero. Attacker seat share is attacker identities divided by admitted identities. Honest specialist retention is admitted honest specialists divided by all honest specialists. Also report six-fact accuracy, attacker admission rate, actual checks, token usage, actual model cost and simple-plurality accuracy on identical packets.

A predeclared engineering target is mean specialist accuracy ≥90% and mean attacker seat share ≤5%. For every size, policy and reliability, report all tested budgets attaining that target and the smallest such tested budget, if any. Do not interpolate a minimum, conceal a later failing budget or treat this as a safety guarantee. Descriptive uncertainty includes paired-world bootstrap intervals and a more stringent interval-envelope target (accuracy lower bound ≥90%, seat-share upper bound ≤5%); neither is a simultaneous guarantee. All 24 worlds remain the statistical clusters, not identities, facts, calls or replay frames. Equal-budget coverage-minus-random contrasts and the full grid are exploratory with no multiple-comparison significance claims.

## Interpretation limits

This maps an engineering frontier inside the existing fixture. It does not establish real-world Sybil resistance, an optimal policy, learned verification, autonomous-agent performance or population-independent thresholds. Independent check outcomes, the simple +7 fabrication, repeated specialist facts, two fixed trust seeds and this graph family are retained intentionally for continuity. Weak checks may admit more attackers; that is a valid adverse scientific result. The separately launched newcomer study addresses scarce information, evolving reputation and controlled identity splitting.

## Results

The fresh-world primary result reproduced: at 972 identities and 10% attacker pass probability, 108 versus four coverage checks increased specialist accuracy by 56.9 percentage points (descriptive paired 95% interval +43.1 to +70.8). Seven of 120 cells met the joint mean target, all at 10% attacker pass. The frontier was nonmonotone: 324-identity coverage passed at 32 checks, then failed at 64 and 108 because attacker seat share rose.

At 972 identities and 64 strong checks, random checking achieved 100% accuracy, 4.82% attacker seats and 52.9% specialist retention; coverage achieved 86.1%, 0.63% and 5.9%, respectively. Random's seat-share interval crossed the 5% target. Accuracy therefore cannot substitute for attacker exclusion, specialist inclusion or a safety guarantee. See [the complete analysis](RESULTS.md), [all 120 cells](results-cells.csv), [paired statistics](results-summary.json), [raw synthetic outcomes](records/s1-001-episodes.jsonl.gz) and [post-mortem](reviews/s1-001-post.md).

The public [final heatmap](https://swarm-live.pages.dev/api/a/sybil-budget-api/46ebda03/final_frame.png), [retention view](https://swarm-live.pages.dev/api/a/sybil-budget-api/46ebda03/retention.png) and [recorded completion replay](https://swarm-live.pages.dev/api/a/sybil-budget-api/46ebda03/replay.gif) are available. The replay depicts real collection progress only.

The later setup audit records a historical immutable-public-plan receipt failure; it does not relabel the run as formally preregistered or independently reviewed. Formal S2 and the reserved holdout remain closed. Any successor remains a plan until separately admitted; this completion authorizes no further run.
