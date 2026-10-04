# Sources for the proposed discussion dose v3 evaluation

Inspected online on 4 October 2026 UTC. This is a focused methods review, not a completed prior-art survey or an independent benchmark replication. The transfers below are proposed adaptations to our small swarm experiment. No external framework was installed and no benchmark was run.

## HiddenBench

[Paper methods and ablations](https://arxiv.org/html/2505.11556v3), [official repository](https://github.com/Yassellee/HiddenBench_ICML); existing entry [[li-2025-systematic]]. Read depth this pass: selected methods and ablations plus repository overview.

Useful feature: compare distributed information with a full-information individual baseline, and examine judgments before and after information sharing. We will add a full-evidence competence diagnostic and separate initial private ballots from report exchange and further discussion. A task that is hard even with complete evidence cannot cleanly diagnose communication failure. We will not copy model-filtered benchmark thresholds blindly or call our new fixtures native HiddenBench results.

## Debate or Vote

[Paper](https://arxiv.org/html/2508.17536v1), [official code](https://github.com/deeplearning-wisc/debate-or-vote); existing entry [[choi-2025-debate]]. Read depth: experimental setup, baseline description, answer-extraction discussion; repository overview.

Useful feature: separate aggregation from inter-agent discussion. Its evaluation appendix also documents sensitivity to answer extraction. We will preserve private initial votes, retain a report-only arm and compare board discussion with repeated private work. Our call-matched private control is an additional design choice, not a claim that this paper already supplies it. The paper's martingale model is assumption-dependent; it is not a universal theorem about deployed LLM swarms.

## AgentDojo

[Paper design and reporting sections](https://arxiv.org/html/2406.13352v3), [official code](https://github.com/ethz-spylab/agentdojo), [documentation](https://agentdojo.spylab.ai/); existing entry [[debenedetti-2024-agentdojo]]. Read depth: task definitions, attack surfaces, metrics and evaluator discussion; repository/docs overview.

Useful feature: define legitimate-task utility and attacker objectives separately, and evaluate against explicit environment state. We will separately score correct decisions, attack-target decisions, safe abstention and downstream parent consequences. A later adapter could use small audited travel tasks; the original suite is not a fork-and-merge benchmark, and we will not inherit its full runtime for v3.

## LongMemEval

[Paper abstract](https://arxiv.org/abs/2410.10813), [official repository and data schema](https://github.com/xiaowu0162/LongMemEval). Read depth: abstract, README, oracle-retrieval variant and abstention evaluation notes.

Useful feature: explicit missing-information/abstention and knowledge-update categories, plus an evidence-only diagnostic. We will test complete, missing, conflicting and stale memory separately. We will distinguish whether evidence survived the merge from whether the parent used it correctly. Its conversational QA scoring is not automatically suitable for adversarial swarm memory; our core fixtures retain deterministic integer/action checks rather than importing its judge.

## MPBench

[Official dataset repository](https://github.com/Digital-Trust-Lab/mp-bench). Read depth: complete README and schema; underlying paper and payload dataset not audited.

Useful feature: separates insertion into memory from later retrieval and action, includes benign cases, and describes both overt instruction attacks and quieter fact/precedent poisoning. We will retain separate admission and downstream-consequence measures and benign controls. Candidate extensions need their own threat models. We are borrowing evaluation dimensions, not claiming verified dataset quality or copying uninspected payloads.

## A benchmark critique worth incorporating

[Indirect Prompt Injections: Are Firewalls All You Need, or Stronger Benchmarks?](https://arxiv.org/html/2510.05244v1). Read depth: metric definitions and Section 6 benchmark analysis; defense results not replicated.

The authors report cases where attacks remove task-critical evidence or utility checks mis-score task completion. Our proposed response is an answerability audit and exact semantic outcome checks, with unrecoverable cases labeled separately. This is a methodological lesson from the paper, not independent confirmation of every critique or an endorsement of its defense-performance claims.

## Later extensions rather than new dependencies

[LongMemEval-V2 official repository](https://github.com/xiaowu0162/LongMemEval-V2) was inspected at README/interface level. It evaluates memory over agent trajectories, including state changes and environment-specific assumptions, and keeps answer metadata outside the query interface. That suggests a future v4 workflow-transfer test. Its much larger multimodal histories and runtime are unnecessary for the first causal diagnostic.

[AgentPoison official repository](https://github.com/AI-secure/AgentPoison), existing entry [[gh-ai-secure-agentpoison]], was inspected at README level. Triggered retrieval of poisoned memory is a distinct later threat model. We will not mix it into a first experiment on honest agents sharing contaminated facts.

## Scope of the source search

Searches covered hidden-profile evaluation, debate/vote baselines, tool-result injection, memory poisoning, abstention and benchmark-validity critiques. Primary papers and author repositories support the design transfers. Community posts and search snippets were not used as evidence. Dataset licensing, individual answer keys and full external task execution remain prerequisites for copying benchmark cases; v3 uses authored fictional fixtures until those audits are complete.
