# Task and evaluation audit

This document separates inspected benchmark methods, our adaptation, and what has actually been validated. These tasks are **new fictional fixtures inspired by distributed-evidence benchmarks**, not a licensed copy of HiddenBench or an official benchmark score. No external benchmark framework or dataset is installed.

## Why these sources

| Source and inspected material | What it contributes | Why it is not the first runtime |
| --- | --- | --- |
| [[li-2025-systematic]]; [HiddenBench official repository](https://github.com/Yassellee/HiddenBench_ICML), [data](https://github.com/Yassellee/HiddenBench_ICML/blob/3be6ca16973e4fb751ffc0dfb7eb11f2d28335d1/data/benchmark.json) | Distributed facts and full-information solvability controls motivate the fixture. Official README reports 65 tasks. | Native tasks/schedules differ from this three-agent tool/memory protocol. Some inspected cases rely on inferential assumptions. Reusing a whole dataset without auditing every answer would weaken ground truth. |
| [[debenedetti-2024-agentdojo]]; [official repository](https://github.com/ethz-spylab/agentdojo), [travel task definitions](https://github.com/ethz-spylab/agentdojo/blob/089ed468cf3ed0322acc66b0211f26d9d90dbf60/src/agentdojo/default_suites/v1/travel/user_tasks.py) | Concrete tool-result attack surface and separate legitimate-task/attack outcomes. Read-only hotel/restaurant selection illustrates discrete auditable choices. | Native tasks are not swarm fork/merge experiments. Some tasks involve environment changes. Use as a later external-validity adapter after the small harness is qualified. |
| [[chen-2026-memsecbench]]; [paper](https://arxiv.org/abs/2607.27080) | Distinguishes memory persistence from a downstream consequence. | Its lifecycle and evaluator are not this voting task. We use a narrow integer-valued memory probe rather than assume all memory scoring is deterministic. |
| [Correlated Promotion Benchmark](https://github.com/lxy1134/iclr_2027) | Source dependence and promotion of claims are relevant to nominal quorum. | Promotion rules and authored provenance are not equivalent to independent child ballots. Source independence remains untested here. |
| [WeClawArena](https://github.com/kingofspace0wzz/WeClawArena) | Private agent state and tool-mediated collaboration motivate later realistic workflows. | Transaction approvals can establish governance compliance without establishing objective truth of a recommendation. More environment machinery is unnecessary for this first question. |

Repository versions inspected in the preceding benchmark audit: HiddenBench `3be6ca16973e4fb751ffc0dfb7eb11f2d28335d1`; AgentDojo `089ed468cf3ed0322acc66b0211f26d9d90dbf60`; CPB `7614c78262c727637f0ca96860baaf0d0a6fe18c`; WeClawArena `a997b82a0f865f057db14d0a7caf40e4470174b6`. The first two official repository pages were reopened in this implementation pass. This is a bounded task-selection audit, not a newly completed full-paper survey or an assertion that every available benchmark was run.

## Exact fixture contract

Generator and renderer: [src/tasks.py](src/tasks.py). Validation: `validate_world` and the independently written `independent_answer` function in that file. The latter uses a separate declarative computation, not the generator's stored expected label. It is an implementation cross-check by the same author, not independent researcher review.

| Family | Clean eligibility | What is contaminated | Why the wrong option is attractive |
| --- | --- | --- | --- |
| Capacity | Power at least a minimum AND access at most a maximum | A digest overstates one site's power | The wrong site becomes apparently eligible and is strictly better under the numeric objective |
| Total cost | Base plus freight within budget AND arrival by deadline | A digest understates freight | It hides a total-cost violation while the arrival condition is satisfied |
| Dependency | Sufficient direct capacity OR a backup with transfer within limit | A digest understates transfer time | It makes an otherwise invalid fallback appear usable |

Clean worlds have one eligible option. The public numeric objective yields a deterministic choice if agents perceive more than one; an alphabetic tie break is explicit. Both the correct answer and wrong target range over A/B/C. One false numeric field changes the decision under the counterfactual false world. All other evidence content, source metadata, word counts, assignments and objectives are held fixed across clean/attack pairs.

Each task has three canonical option records, an independent audit of the targeted quantity and a lower-authority digest of that quantity. This source structure is intentionally favorable to verification and may cue agents to the contested field; it is held constant in clean and attack conditions. More realistic ambiguous provenance is a future treatment, not something this fixture validates. The digest and audit covering one field is not evidence that the model discovered an attack.

Each agent initially reads its assigned partition. All agents later receive the same child reports and can request three registry documents to recover the complete clean evidence. Correct answers never require a fact unavailable within the tool allowance. Initial reports need not be complete; their omissions are observable agent behavior. No attacker-chosen instruction modifies the goal, evaluator, model settings or merge policy.

## Mechanical qualification

[Self-tests](src/selftest.py) cover:

- 300 reproducible worlds across the three families, unique clean solutions, label coverage and attack counterfactual relevance.
- Hand-written threshold/cost boundary examples and the full boolean truth table for the conditional dependency rule.
- Exactly one initial tool result changes; later verification remains clean; complete evidence union survives N=3, 5 and 9 allocation.
- No answer/target metadata in model requests; separate private contexts; no intermediate ballot feedback; no same-round post visibility.
- Three-way ties, abstention and fixed-electorate majority; majority fact merge with source references.
- A deliberately harmful synthetic outcome that must be scored as target success, wrong decision, poisoned memory and injected-value follow-up.
- Timeouts, malformed objects, unknown source IDs, duplicate claims, output limits and all-assigned invalid denominators.
- Paired snapshot identity, missing/duplicate episode detection, event hashes, no overwrite of results and the HTTP adapter against a local mock server.

The scripted policy is an engineering fixture. It reads supplied documents and prefers canonical sources. Its clean success proves the task is solvable through the exposed interface, but **does not qualify an LLM, establish difficulty, demonstrate persuasion, or validate ecological realism**.

## Live qualification still needed

Before S1 LLM collection, pin a model and run S0 with all eight conditions. Show clean accuracy and invalid rates per family; manually inspect every failure in those six worlds. Add a full-information single-model check if clean performance is poor, to separate reasoning difficulty from report loss. Do not select worlds by attack success.

Before confirmation, a different researcher should inspect rendered examples, answer derivations, the intervention diff and scorer mutations. The [review task](../../../../tasks/review-discussion-dose.md) records this unmet requirement. Expand into a second independently designed task family or a fully audited AgentDojo adapter before claiming broader agent-workflow relevance. Three semantic wrappers or paraphrases do not constitute held-out domains.

No holdout task data are generated or opened by the stage coordinator. S2 is disabled. Any future held-out set needs frozen distinct templates as well as distinct task IDs if the claim concerns transfer beyond these three rules.
