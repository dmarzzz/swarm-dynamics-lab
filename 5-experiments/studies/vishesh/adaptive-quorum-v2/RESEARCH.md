# Research rationale and boundaries

Sources reopened 2026-10-03. This is a focused methods review, not a gate-passed survey or a claim of exhaustive novelty. Read depths below refer to this pass. Existing library metadata is not fresh reading.

| Primary source | Read this pass | Design consequence | Boundary |
|---|---|---|---|
| [[pratt-2006-tunable]], [primary article](https://pmc.ncbi.nlm.nih.gov/articles/PMC1635101/) | Results and methods skim | Vary evidence arrival independently of commitment threshold; record deadline tradeoffs | Search and acceptance changes strongly affect speed/accuracy in the studied ants. Lowering our software threshold is an analogy, not a biological mechanism test. |
| [[choi-2025-debate]], [paper](https://arxiv.org/html/2508.17536v1) | Abstract, setup, formalization and limitations skim | Include ordinary majority and a centralized deadline solver; do not equate extra discussion with improvement | Findings concern tested tasks/models/protocols; the martingale argument depends on its update assumptions and is not a universal impossibility result. |
| [StableToolBench](https://arxiv.org/html/2403.07714v3) | Abstract and virtual-server methodology skim | Freeze local API behavior and evidence fixtures; execute deterministic mock responses with independent scoring | This study does not run StableToolBench or inherit its realism/performance claims. Its cached/simulated API approach motivates reproducibility, not equivalence to live services. |

## Connection to the original sixteen briefs

- [Quorum](../project-briefs/quorum.md): stopping with an explicit false-commit/abstention tradeoff.
- [Collective sensing](../project-briefs/collective-sensing.md): factual evidence distributed across agents; an information-matched central control.
- [Coordination](../project-briefs/coordination.md): acquiring and sharing complementary evidence under a deadline.
- [Diversity](../project-briefs/diversity.md): distinct evidence versus merely adding copies of the same model.
- [Dissent](../project-briefs/dissent.md): a contradictory benchmark can change a leader; no benefit is attributed to dissent without new evidence.
- [Institutions](../project-briefs/institutions.md): fixed admission criteria versus pressure to commit.

## What is genuinely tested

The primary comparison isolates two stopping policies on the same model ballot tape. It tests whether reducing a provenance floor changes decisions usefully under a specified evidence schedule. The verification contrasts test allocation of a small testing budget. Neither is evidence of autonomous self-organization. Explicit roles describe evidence access, not independently trained experts.

The main novelty claim remains modest: integration of typed local decision agents, controllable evidence arrival, provider eligibility, a mock test tool, and paired stopping policies. Before promotion, search stopping/optimal-stopping, sequential testing, value-of-information and best-arm identification literature more deeply; obtain independent review and compare the closest implementation. A new visualization is not scientific novelty.

## Skeptical design changes

1. No central early-stop straw man: the central deadline arm sees all available evidence and can use the whole deadline.
2. No root-count guarantee: roots identify supplied document ancestry; copied or stale evidence is not independent truth.
3. No model-count/evidence-count confound: five and nine agents divide the same document schedule.
4. No purchased accuracy: verification controls share the same two-probe ceiling; actual tokens and time are reported.
5. No engineered positive result: early correct, early wrong, stalled and no-solution cases are included. Adaptive can lose.
6. No oracle decision gate: hidden fixture truth is used only to construct the environment and score final decisions. Mock tools reveal only their measured test output.
7. No benchmark inflation: synthetic extraction and toy privacy policies remain a limitation; no production procurement recommendation is claimed.
