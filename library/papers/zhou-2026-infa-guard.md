---
id: zhou-2026-infa-guard
type: paper
title: 'INFA-Guard: Mitigating Malicious Propagation via Infection-Aware Safeguarding in LLM-Based Multi-Agent Systems'
authors:
- Yijin Zhou
- Xiaoya Lu
- Dongrui Liu
- Junchi Yan
- Jing Shao
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2601.14667
doi: null
arxiv: '2601.14667'
cite: 'Zhou, Y., Lu, X., Liu, D., Yan, J., & Shao, J. (2026). INFA-Guard: Mitigating Malicious Propagation via Infection-Aware Safeguarding in LLM-Based Multi-Agent Systems. arXiv preprint. arXiv:2601.14667.'
topics:
- fork-merge-security
- llm-agent-swarms
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: null  # Semantic Scholar and OpenAlex rate-limited on 2026-10-03
code: []
---

## Summary

Argues that defences for LLM multi-agent systems wrongly treat agents as either benign or attacker, ignoring "infected" agents: benign agents that an attacker has persuaded and that then propagate the error themselves. INFA-Guard extends G-Safeguard's utterance-graph detector to a three-class problem (benign, attack, infected) over time, adds topology constraints (an infected agent makes an attacker likely nearby and vice versa), and remediates differently: attackers are replaced by benign agents, infected agents have their responses corrected so they recover. Evaluated on the G-Safeguard benchmark (prompt injection, InjecAgent tool attacks, PoisonRAG memory attacks). Read: abstract, introduction, motivation experiment, method overview, results and limitations.

## Contribution

Names and measures the secondary-infection problem: cutting off the original attacker is not enough because converted agents keep spreading, and the paper shows a remediation that heals rather than isolates them.

## Key results

- Motivation experiment: defending only against attack agents still let agent-level attack success rise over iterations when infected agents remained (measured, Figure 2; exact deltas lost in HTML math).
- GPT-4o-mini, round-3 agent-level attack success (lower is better): CSQA prompt injection 59.3 no defence, 31.7 G-Safeguard, 23.3 INFA-Guard; InjecAgent 67.5, 13.1, 2.1; PoisonRAG 38.3, 18.0, 6.1 (measured, Table 1).
- 20 agents: 20.9 vs 9.1 at round 3; 50 agents: 17.3 vs 9.2, with attack success falling over rounds ("self-healing") (measured, Table 2).
- Removing the replace-and-rehabilitate remediation (using pruning instead) caused the largest ablation drop (measured).

## Methods and models

GPT-4o-mini and Qwen3-235B-A22B backbones; chain, tree, star topologies; MiniLM embeddings; supervised training on synthesised, labelled dialogues. Metrics: agent-level ASR and majority-vote task accuracy (MDSR). Code at github.com/yjzscode/INFA-Guard (EMNLP 2026 per the repository page found in search; not confirmed on the arXiv page).

## Limitations and open questions

Needs labelled training data and at least one round of dialogue before it can act (stated by the authors). Same benchmark family as its baselines; no adaptive attacker.

## Relevance to us

Q3: gives a measured name to what dmarz describes as the corrupted child becoming the attacker's agent: an "infected" agent is a former benign agent that now propagates the attacker's content. The result that infected agents keep the system failing after the source is removed is the multi-agent version of "the merge carries the infection home". Q2: the remediation suggests merge-time options beyond accept or reject: replace a child judged to be an attacker, and re-ground a child judged infected before merging. Note the threshold here is a majority-vote task metric, not a provable bound. Related: [[wang-2025-g-safeguard]], [[miao-2025-blindguard]], [[papadopoulos-2026-mind]], [[ma-2026-catching]].
