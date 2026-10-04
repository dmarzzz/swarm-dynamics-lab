---
id: liu-2025-can
type: paper
title: Can an Individual Manipulate the Collective Decisions of Multi-Agents?
authors:
- Fengyuan Liu
- Rui Zhao
- Shuo Chen
- Guohao Li
- Philip Torr
- Lei Han
- Jindong Gu
year: 2025
venue: arXiv preprint (cs.CL, cs.AI)
url: https://arxiv.org/abs/2509.16494
doi: null
arxiv: '2509.16494'
cite: 'Liu, F., Zhao, R., Chen, S., Li, G., Torr, P., Han, L., & Gu, J. (2025). Can an Individual Manipulate the Collective Decisions of Multi-Agents? arXiv preprint arXiv:2509.16494.'
topics:
- llm-agent-swarms
- collective-decision
added_by: vishesh/senku-1
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: '4 (Semantic Scholar, 2026-10-03)'
code: []
---

## Summary

The paper asks whether an attacker who can inspect only one agent of a multi-agent LLM system can still steer the group's final answer. It formulates the setting as a game of incomplete information and proposes M-Spoiler, which optimises an adversarial suffix against a simulation of the debate rather than against the target agent alone. The simulation adds a stubborn agent that argues against the target agent whenever the target is right and agrees whenever it is wrong, plus a critical agent that picks the most convincing of several sampled stubborn responses (a best-of-refinement tree). Gradients and losses across debate turns are weighted with exponential decay so early turns count more. Evaluation covers 9 models and 7 datasets; the paper reports attack success rates "mostly ranging from 10% to 98%", and the defences it tests do not close the gap.

## Contribution

It moves adversarial attacks on LLM agents from the single-model case to the collective-decision case under partial knowledge, showing that access to one agent is enough leverage, and that optimising against a simulated adversarial interlocutor transfers better than optimising against the single agent in isolation.

## Key results

- Measured: attack success rates "mostly ranging from 10% to 98%" across the evaluated systems.
- Measured: evaluation spans 9 models (LLaMA-2 7B/13B/70B, LLaMA-3 8B/70B, Vicuna-7B, Qwen2-7B, Mistral-7B, Guanaco-7B) and 7 datasets (AdvBench, SST-2, CoLA, RTE, QQP, Algebra, GSM).
- Measured: in Table 1 suffixes optimised on Qwen2 are transferred to two-agent systems that each contain Qwen2 plus one other model; M-Spoiler beats the single-agent baseline in the reported pairings, for example roughly 96.5% against 72.9% for the Llama3 pairing and roughly 98.6% against 95.8% for the Qwen2 pairing.
- Measured (ablation, Table 3): removing the refinement tree lowers success (about 52% for the Llama2 setting) against about 58% for two-round M-Spoiler and about 64% for the three-round variant, so the stubborn-agent simulation and extra debate rounds both carry weight.
- Measured: the scaling experiment goes "up to 101 agents (1 target agent and 100 replicated LLaMA3 agents)", and success falls as the agent count rises.
- Measured: tested defences (an introspection prompt, self-perplexity filtering) reduce but do not eliminate the effect; perplexity filtering is weaker against fluent suffixes than against token-salad ones.
- Baselines compared against: GCG, I-GCG and variants, AutoDAN.

## Methods and models

Adversarial suffix optimisation in a simulated multi-agent debate. The attacker holds white-box access to exactly one agent and no access to the rest. The simulation instantiates (i) a stubborn agent that is prompted to disagree with correct target answers and endorse incorrect ones, and (ii) a critical agent that scores N sampled stubborn replies and keeps the strongest, which is the best-of-refinement tree. Losses over debate turns are combined with an exponential decay that favours early turns. Tasks are classification and short-answer reasoning, so "success" is the group converging on the attacker's chosen wrong label or answer. Semantic Scholar records the venue for this record as EMNLP; the arXiv abstract page carried no acceptance comment when loaded, so `venue` above is left as the arXiv listing.

## Limitations and open questions

The authors state that the simplified multi-agent settings may not capture real deployments; most headline numbers come from two-agent systems, and effectiveness decays as the population grows, which is the regime a swarm actually lives in. Success is measured on tasks with a single correct answer, so it does not speak to open-ended or long-horizon group tasks. The ethics statement notes the AdvBench prompts are harmful by construction and that the method could be used for jailbreaking.

## Relevance to us

This is the closest existing work to the question of whether a preference planted in one agent propagates to a collective's choice, and it gives us three reusable pieces: the threat model (knowledge of one agent only), the simulated-opponent trick for optimising an influence signal without access to the rest of the system, and a measurement protocol (attack success rate on a group answer, swept over agent count) that a hackathon project can copy directly as a baseline. The agent-count decay is the most useful number for us: it suggests any single-agent influence result must be reported as a function of population size, not at N=2. Pairs with the persuasion-based variant in [[kraidia-2026-when]], the content-level manipulation in [[nestaas-2024-adversarial]], the injection-propagation mechanism in [[lee-2024-prompt]], the conformity and herding effects that make a group susceptible ([[cho-2025-herd]], [[weng-2025-do]], [[bellina-2026-conformity]]), and the failure vocabulary of [[cemri-2025-why]].
