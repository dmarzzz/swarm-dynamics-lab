---
id: yan-2026-when
type: paper
title: 'When Truth Is Distributed: Misinformation Derails Collective Fact Recovery in LLM-Based Multi-Agent Systems'
authors:
- Chenfei Yan
- Zeyang Yue
- Feifei Zhao
- Erliang Lin
- Lu Jia
- Haibo Tong
- Mingyang Lyu
- Chengyi Sun
- Yi Zeng
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2608.03421
doi: null
arxiv: '2608.03421'
cite: 'Yan, C., Yue, Z., Zhao, F., Lin, E., Jia, L., Tong, H., Lyu, M., Sun, C., & Zeng, Y. (2026). When Truth Is Distributed: Misinformation Derails Collective Fact Recovery in LLM-Based Multi-Agent Systems. arXiv preprint. arXiv:2608.03421.'
topics:
- fork-merge-security
- llm-agent-swarms
- collective-decision
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: skim
relevance: 5
citations: null  # Semantic Scholar and OpenAlex rate-limited on 2026-10-03
code: []
---

## Summary

Introduces ForesightSafety-TIDE, a controlled test of distributed fact recovery in LLM multi-agent systems. In each of 120 stories, five agents each see a different time window of an object's movements, and only their pooled observations determine the object's true endpoint; exactly two agents (the key role and a second key role) directly observed the endpoint. Each story is run twice, once with all agents honest and once with the key role deceiving (fabricating a later move, overstating its observation window, or re-dating a stale report), followed by testimony, private votes and three public discussion rounds. Process tracing follows which agent's evidence each statement cites and adopts, and "exit" ablations remove the deceiver mid-discussion. Read: abstract, introduction, framework and procedure, setup, the propagation analysis and the conclusion; several numbers were in stripped math markup, so figures below come from the arXiv abstract unless noted.

## Contribution

Isolates the effect of one lying holder of exclusive evidence, with paired honest and deceptive runs, and measures the mechanism: false evidence is adopted more readily, spreads further, and outlives its source.

## Key results

- Aggregate truth recovery fell from 72.50% (honest) to 14.17% (one deceiver), with significant declines for every one of the three systems (GPT-5.5, DeepSeek-v4-pro, Grok-4.5) (measured, per abstract).
- The honest second key role's testimony was referenced as often as the deceiver's, but adoption of the deceiver's testimony rose while adoption of the honest one fell; access to the truth was not the bottleneck, integration was (measured).
- Agents holding only the true evidence acquired the false evidence much more often than the reverse; among agents holding both, a minority voted for the truth; false evidence formed deeper relay chains than true evidence (measured, exact rates not transcribed).
- False testimony persisted through honest agents after the deceiver exited (measured, exit ablation).
- Observers without first-hand evidence reduced consensus on the decoy but did not raise truth recovery; they shifted the group to uncertainty (measured).

## Methods and models

Five-agent homogeneous systems per model; checkpoints T0, T1, R1-R3; deception types Event, Coverage, Source (40 stories each); private and public communication variants; evidence-root lineage tracing.

## Limitations and open questions

Synthetic object-movement stories; one deceiver; homogeneous models; the deceiver knows the ground truth, which is the worst case.

## Relevance to us

Q3 and Q2: this is the closest measured setting to dmarz's China example. Each part holds evidence nobody else has; when the one part that saw a domain lies about it, an honest majority could not recover the truth (14% recovery), even with a second honest witness present, and the falsehood kept circulating after the liar left. So a k-of-n vote does not protect facts that only one or two parts can attest; the threshold applies per fact, to the number of independent first-hand witnesses, not to the number of parts. The authors' design advice (separate first-hand evidence from relays, check provenance and source independence) is the merge-time rule this implies. Q1: the deceiver was more effective by being the evidence holder, which is what an attacker gains by identifying which part went to which domain. Related: [[becker-2026-misinformation]], [[zhang-2021-corruption-robust]] (the RL analogue: corruption concentrated on the least-covered region), [[papadopoulos-2026-mind]].
