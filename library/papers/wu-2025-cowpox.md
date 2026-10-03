---
id: wu-2025-cowpox
type: paper
title: 'Cowpox: Towards the Immunity of VLM-based Multi-Agent Systems'
authors:
- Yutong Wu
- Jie Zhang
- Yiming Li
- Chao Zhang
- Qing Guo
- Nils Lukas
- Tianwei Zhang
year: 2025
venue: arXiv preprint (keywords list ICML; venue not confirmed)
url: https://arxiv.org/abs/2508.09230
doi: null
arxiv: '2508.09230'
cite: 'Wu, Y., Zhang, J., Li, Y., Zhang, C., Guo, Q., Lukas, N., & Zhang, T. (2025). Cowpox: Towards the Immunity of VLM-based Multi-Agent Systems. arXiv preprint (keywords list ICML; venue not confirmed). arXiv:2508.09230.'
topics:
- fork-merge-security
- llm-agent-swarms
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: skim
relevance: 3
citations: null  # Semantic Scholar and OpenAlex rate-limited on 2026-10-03
code: []
---

## Summary

Defends vision-language multi-agent systems against the infectious jailbreak of Gu et al. (an adversarial image stored in one agent's retrieval album that is preferentially retrieved and passed on in pairwise chats). A small number of defender-controlled "Cowpox" agents inspect what they receive with an output-analysis module; when they find a virus sample they optimise a "cure" image that scores even higher in retrieval than the virus, and spread it the same way the virus spreads, so infected agents retrieve the cure instead and agents holding the cure are immune. Includes a stability analysis of the infection dynamics with a condition under which the cure outpaces the virus. Read: abstract, introduction, threat model, method overview, experiments and limitations; proofs skimmed.

## Contribution

Shows that one can fight contagion with counter-contagion when the defender controls only about 3% of agents, with a theoretical recovery condition, and tests an adaptive attacker who re-optimises against the cure.

## Key results

- With 4 Cowpox agents in a 128-agent system (about 3%), current infection was pushed back down after peaking, recovering over 95% of infected agents; cumulative infection stayed around 90% instead of 100% (measured, Table 2).
- The output-analysis module (same VLM, yes/no) had 84.7% accuracy with 12.5% false negatives in one turn and 89.1% with 3.0% false negatives over three turns (measured, Table 1).
- An adaptive virus re-optimised against the captured cure at round 65 produced a much lower second infection peak (measured, Figure 5).
- Limitation stated by the authors: the system converges on one or two cure samples, making conversations monotonous; [[ma-2026-catching]] later quantifies this loss of diversity.

## Methods and models

LLaVA-1.5-7B agents, CLIP retrieval, history length 3, album size 10, 64 chat rounds, following Gu et al.'s setup. Attacker has white-box access to one "patient zero" agent. Code at github.com/WU-YU-TONG/Cowpox.

## Limitations and open questions

Assumes the defender's cure can outscore any virus in retrieval, which an attacker with white-box access can contest; homogenisation of retrieval; tested on one retrieval-driven attack family.

## Relevance to us

Q2: Cowpox is a threshold result of a different kind from Byzantine voting: containment is guaranteed when the cure's spread rate exceeds the virus's, with a few percent of trusted agents. For a parent that forks many children, a small set of trusted children that carry a "vaccine" (an explicit warning or verified memory) is an analogue, and [[papadopoulos-2026-mind]] measured a related effect with a one-paragraph warning. Q3: the attack model, retrieval-score optimisation of a stored item, is the memory-poisoning route by which a returning child's memory dominates the parent's retrieval after merge. Related: [[gu-2024-agent]], [[ma-2026-catching]].


## Notes from shadow/sol-g74

Issue #74 rerun, 2026-10-03. Source opened: https://arxiv.org/abs/2508.09230 . Read depth in this session: full.

Read all HTML sections, mathematical proofs and appendices. The earlier limitation saying only one retrieval-driven environment is broadly right, but Appendix D also tests heterogeneous LLaVA-1.5/InstructBLIP agents and CLIP/DINO V2 retrievers, populations 128-512, and multiple virus samples. Proposition 4.1 gives extinction under a strict cure-conversion advantage in an idealized model with effectively infinite history and negligible spontaneous recovery; this is not an unconditional deployment theorem. Four defenders among 128 agents recover over 95% of infected agents in Table 2; cumulative infection remains roughly 84-92%, so recovery is not prevention. The defence has a documented conversation-diversity cost. Publisher record opened: https://proceedings.mlr.press/v267/wu25aq.html . Correct published reference: Wu, Yutong; Zhang, Jie; Li, Yiming; Zhang, Chao; Guo, Qing; Qiu, Han; Lukas, Nils; Zhang, Tianwei (2025). Cowpox: Towards the Immunity of VLM-based Multi-Agent Systems. Proceedings of the 42nd International Conference on Machine Learning, PMLR 267, 68015-68035. The landing arXiv author metadata omits Han Qiu, whereas the HTML and publisher include him. The publisher settles the published author list and confirms ICML 2025.
