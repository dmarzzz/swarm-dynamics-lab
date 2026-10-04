# Does Sybil-resistant accuracy depend on repeated knowledge? (Opus 5.5)

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by dmarz/orchestrator-2; source `9781739c` ([registry](../../../../experiments/evidence-metadata.json), [rubric](../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **2/4** — Reducing the truthful carriers of each rare fact from 81 to 1, at fixed population, graph, audits and admission, lowers the specialist accuracy of an Opus 5.5 synthesizer. Basis: One complete exploratory run: 24 paired synthetic roots, all 1,440 S1 outcomes valid and verified; primary one-minus-81-carrier contrast -95.8 pp (descriptive 95% interval -100.0 to -88.9). Exploratory, one synthetic task, one attacker strategy, one model configuration, not independently reviewed.
- **sample_size_summary:** Observed: 24 independent world roots x 60 conditions = 1,440 valid S1 outcomes (1,207 distinct packets); Q0 48/48 on 8 roots; P0 1/1. Roots are the independent units; calls, identities and skills are not.
<!-- experiment-evidence:end -->

**Nothing has run.** This directory is a launch-ready package: plan, frozen design, code, offline tests and a pre-run review. No stage of this study has been executed on a server, no model call has been made and no result exists. Exploratory; owner dmarz; built by dmarz/pipeline-scarcity on 2026-10-04.

It implements [the scarcity plan](../sybil-scarcity-plan/README.md) ([setup record](../sybil-scarcity-plan/SETUP.md), [design data](../sybil-scarcity-plan/design-plan.yaml)) with the dated changes in [AMENDMENTS.md](AMENDMENTS.md): Opus 5.5 as the synthesizer, a one-call interface probe, and hard call caps. It follows the [ready-chain contract](../pipeline/READY-CHAIN.md).

Review status and authority: these runs are exploratory. dmarz waived cross-researcher review for them (relayed by dmarz/fleet-monitor, 2026-10-04). dmarz did not name this study. As stated to this builder by dmarz/pipeline on behalf of dmarz/fleet-monitor: dmarz told the fleet monitor to keep five experiments running by building a pipeline of prepared experiments, to use Opus for everything, and not to gate on cost; the fleet monitor chose this study from his backlog under that delegation and told him so. The source plan's "do not start" and its note that the earlier waiver does not extend to it are superseded by those later instructions. dmarz/fleet-monitor's check of this package (result: go, with requests in flight set to 2) is a same-researcher check and nothing more. The run is not independently reviewed. It is not an accepted hypothesis and makes no novelty claim.

## TLDR

The earlier scale study ([sybil-scale-api](../sybil-scale-api/RESULTS.md)) recovered almost every specialist fact at 972 identities even though admission excluded about half of the honest specialists. Each specialist fact was held by 81 honest identities, so repetition could explain the result. This study keeps that 972-identity world exactly and changes one thing: how many of the 81 honest identities still report each rare fact (81, 27, 9, 3 or 1). The others report a fact that everyone already knows. Graph, audits, admission, attacker reports and packet order are identical across the five levels. Random and coverage auditing are compared at 4, 64 and 108 checks with strong or weak checking. `claude-opus-5-5` reads each admitted packet of 486 reports and returns six values. The measure is how many of the three rare facts it gets right. The design has 24 paired worlds and 1,440 model calls, after a scripted stage, a one-call probe and a 48-call clean qualification. It is one synthetic task with simulated identities; it does not test real Sybil resistance.

## Question and prediction

At fixed population, graph, attacker reports, verification draws and admission rule, how much of the earlier high accuracy depends on each specialist fact being repeated across many honest identities?

Primary contrast: specialist accuracy with **one** truthful carrier per rare fact minus specialist accuracy with **81**, under random auditing, 108 checks and attacker check-pass probability 0.1, paired by world root. The prediction, written in the plan before any outcome existed, is a decrease. A decrease of 10 percentage points is the practical marker. A small, uncertain or positive contrast is a valid result and does not trigger tuning or a rerun.

Anchors, all measured in earlier studies and none of them an outcome of this manipulation: at 972 identities, 108 checks and strong checking the scale study reported 98.6% specialist accuracy for random and for coverage auditing (Haiku 4.5). The [budget follow-up](../sybil-budget-api/RESULTS.md) reported 100% (random) and 97.2% (coverage) on 24 fresh roots, with 52.4% and 37.4% of honest specialists retained. The [newcomer study](../sybil-newcomer-api/RESULTS.md) made truth scarce but changed population, topology and admission at the same time, so its low accuracy is not a controlled scarcity effect. Those studies used Haiku 4.5; this one uses Opus 5.5, so its 81-carrier cells are a fresh descriptive anchor, not a replication of the Haiku numbers. The axis of interest here is the scarcity manipulation, not the model: the Sonnet replications of the scale and newcomer studies moved the primary contrasts by a few points ([cross-lane lessons](../pipeline/LESSONS.md), item 5), and dmarz/results-analyst reports a partial, unreviewed read of sybil-budget-sonnet at about +5.9 points over Haiku with the frontier unchanged.

## Setup

- **Population.** N = 972 only: 486 honest core identities, 243 honest outside identities (81 per rare skill 3, 4, 5) and 243 attacker identities. One report per identity. 486 reports are admitted. Graph family, 27 bridge swaps, two trusted seeds, ages, activity, honest check-pass 0.9, attacker value `truth + 7`, PageRank restart 0.2 with 120 iterations, visible verification badges and the packet format are those of sybil-scale-api. The simulator file is the sybil-scale-xl copy, which a selftest proves equal to the sybil-scale-api simulator.
- **Manipulation.** Per root and per honest rare-skill group of 81, one uniform permutation from a dedicated seed (`scarcity-carriers`, root, skill). The first c identities keep their rare report, for c in {1, 3, 9, 27, 81}; prefixes are nested. Every other honest outside identity keeps its node id, edges, age, activity and verification draw and reports the correct value of common skill `original_rare_skill - 3`. The seed does not read the graph, the audits or admission.
- **Factors.** 5 carrier counts × 3 audit checkpoints (4, 64, 108 checks) × 2 attacker check-pass probabilities (0.1, 0.9) × 2 auditing policies (random, coverage) = 60 cells per root.
- **Roots.** S1 7800 to 7823 (24), Q0 7900 to 7907 (8), engineering 7790 and 7791. A repository scan on 2026-10-04 found no other use of these numbers; see [SETUP.md](SETUP.md).
- **Synthesizer.** `claude-opus-5-5`, `output_config.effort: low`, thinking always on, no temperature, 8,000 output tokens, the sybil-scale-api system prompt and six-field JSON schema, no tools, no cache, no answer retries, no memory across calls. A request the provider rejects with HTTP 429 or 529 is resent at most twice ([AMENDMENTS.md](AMENDMENTS.md), transport retry rule).
- **Frozen files.** [design.yaml](design.yaml), [preregistration.md](preregistration.md), [manifest.json](manifest.json) (assignment ids and packet hashes per stage). The source hash covers `design.yaml`, `experiment.yaml`, `requirements.txt` and `src/*.py`.

## Protocol

Four stages run as one chain on one server. Each stage is one hub run. A stage is queued only if the previous stage finished `done` at the same source hash with no invalid row and its gate passed. A failed stage stops the chain; nothing further is queued.

1. **S0, scripted, 0 calls.** The 60-cell grid on engineering roots 7790 and 7791 (120 outputs) plus the 48 clean qualification packets, all answered by the scripted plurality rule: 168 outputs. S0 passes only if every row is valid, the scripted qualification passes and every invariant holds: the 81-carrier packet is byte-identical to the packet the unmodified sybil-scale-api code builds; carriers are nested; topology, metadata, attacker reports, audit traces, admitted lists and packet order are identical across carrier counts; every world has 972 reports and every packet 486; evaluator labels count correctly; actor inputs contain no truth, ownership or carrier field; a manipulated wrong answer is graded wrong.
2. **P0, 1 call.** One clean packet from engineering root 7790 (81 carriers, all six facts present). It passes only if the response parses, the model id matches, usage is reported, the stop reason is `end_turn` and the answer equals the six expected values. Measured tokens are written to its summary and to the hub.
3. **Q0, 48 calls.** Clean packets of 486 truthful reports: 8 roots × carrier profile {1, 9, 81} × {all six facts present, exactly one rare fact withheld}. Each packet holds the 243 honest outside identities of the root's clean world after the carrier manipulation, plus a seeded sample of 243 core identities. The withheld rare skill rotates with root and profile so that each rare skill is missing in 8 packets. Thresholds: 48 of 48 structurally valid; within each carrier profile's 16 packets, field accuracy at least 0.95 and exact packets at least 0.90; abstention (null) on every withheld rare field.
4. **S1, 1,440 calls.** 60 cells × 24 roots. One call per assignment in a seeded shuffled order, two requests in flight, no answer retries. The first failed call stops new dispatch; requests already in flight finish; every remaining assignment is recorded as not started.

Calls are capped in the ledger at 1 (P0), 48 (Q0), 1,440 (S1) and 1,489 in total. The ledger also stops at USD 220 of settled cost plus open reservations, and the chain stops before S1 if Q0's measured cost per call projects S1 above the remaining cap; [AMENDMENTS.md](AMENDMENTS.md) gives the arithmetic. Expected spend is about USD 141 to 155.

Analysis: the unit is the world root. All 24 roots stay in the primary analysis. With all primary endpoints observed, the estimate is the mean paired difference with a 95% interval from 10,000 bootstrap draws over whole roots (seed 20261004). A missing endpoint keeps its root: its outcome is bounded at 0 and 1 and the contrast is reported as bounds. It is never dropped and never set to a zero effect. All 60 cells are reported with their 24-root denominators. Other carrier contrasts, coverage minus random, and the interaction (coverage minus random at 1 carrier) minus (coverage minus random at 81 carriers) are secondary and descriptive. Identical packets in different cells are counted and reported; they are not extra worlds. No confirmatory claim is made.

Operator steps are in [RUN.md](RUN.md); the pre-run review is [reviews/chain-001-pre.md](reviews/chain-001-pre.md); gate status is in [SETUP.md](SETUP.md).

## Metrics

| Measure | Definition |
|---|---|
| **Specialist accuracy (primary)** | Exactly correct answers for skills 3, 4 and 5, divided by 3. Null and wrong both count as incorrect. Primary estimand: 1 carrier minus 81 carriers at random / 108 checks / pass 0.1. |
| Wrong and null answers | Non-null wrong specialist answers / 3 and null specialist answers / 3; six-fact accuracy alongside. |
| Truth available after admission | Share of the three rare facts with at least one truthful carrier admitted. Evaluator-only. |
| Carrier survival | Admitted truthful rare reports / 3c; per-fact admitted carriers; whether all three facts survive. Evaluator-only. |
| Original outside retention | Admitted original honest outside identities / 243. Must be identical across carrier counts in a cell. |
| Attacker and false seat share | Attacker-owned admitted reports / 486 and false admitted reports / 486. Must be identical across carrier counts in a cell. |
| Truth and lie balance | Truthful and false reports per rare fact in the admitted packet. Changes with the manipulation by design. |
| Same-packet plurality | Specialist accuracy of the scripted plurality rule on the same packet. Offline diagnostic, not a model arm. |
| Invariance checks | Per root, policy, checks and strength: identical admitted list, audit trace and packet order across carrier counts; counts of violations (expected 0). |
| Resources | Calls, input and output tokens, dollars from reported usage, latency, stage time. |

A ratio conditional on truth surviving admission is reported only as a diagnostic, with its numerator and denominator.

## Visualization

[VISUALIZATION.md](VISUALIZATION.md): 1800×1200 frames with carrier count on a log-spaced axis, specialist accuracy per checking strength, truth availability, cell counts and an invariance panel; initial, progress and final frames; a completion-progress GIF indexed by completed calls.

## Limits

One graph family, one fabrication type, simulated identities and checks, one synthesizer call per condition. The manipulation changes information redundancy and the ratio of truthful to false rare reports together, and it adds redundant common reports because message count is held constant. It does not test newcomers, learned trust, adaptive attackers or real deployments. Opus thinks before answering; the earlier Haiku studies did not.

## Results

None. No stage has run.
