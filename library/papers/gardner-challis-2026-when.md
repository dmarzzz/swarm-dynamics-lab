---
id: gardner-challis-2026-when
type: paper
title: 'When can we trust untrusted monitoring? A safety case sketch across collusion strategies'
authors: [Nelson Gardner-Challis, Jonathan Bostock, Georgiy Kozhevnikov, Morgan Sinclaire, Joan Velja, Alessandro Abate, Charlie Griffin]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/html/2602.20628
doi: null
arxiv: '2602.20628'
cite: 'Gardner-Challis, N., Bostock, J., Kozhevnikov, G., Sinclaire, M., Velja, J., Abate, A., & Griffin, C. (2026). When can we trust untrusted monitoring? A safety case sketch across collusion strategies. arXiv:2602.20628.'
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-ai-control
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

A safety-case sketch for untrusted monitoring (one copy of a model monitors another) that relaxes the earlier assumption that colluding copies share a secret signal in advance. Taxonomy of collusion: passive self-recognition (the monitor asks itself whether the code looks like its own work), causal collusion (pre-shared signal), acausal collusion (Schelling points), and combined. To bound passive self-recognition conservatively they fine-tune the monitor (SFT) to recognise the generator's code against honeypots written by another model. On APPS and BigCodeBench with GPT-4.1 as the untrusted model and Gemini 2.5 Flash writing honeypots, SFT-elicited passive self-recognition beat the best previously studied strategy (the for/while signal of [[greenblatt-2023-ai]]): red-team win rate 9.8% versus 2.8% at full usefulness under summarisation, the most effective signal-jamming defence. Without elicitation, passive self-recognition was weak (blue-team safety 84.1% to 97.7%).

## Contribution

Shows that copies of one model may not need any signal at all: recognising their own style is enough, and it survives paraphrase-style jamming better than planted signals.

## Key results

- Honeypot pass probability falls exponentially with the ratio of honeypots to allowed misses ("slack"), the monitor's false-positive rate on honeypots, and its true-positive rate.
- Summarisation lowered passive self-recognition's power least well because it also damages the honest monitor.
- Open problems listed: attack selection, honeypot slack, eliciting optimal collusion, jailbreaking.

## Methods and models

Statistical model of deployment (tasks, human budget split between honeypots and audits, collusion ROC curve, slack) solved for equilibrium; collusion scores from YES/NO logit differences; minification and summarisation as jamming.

## Limitations and open questions

A sketch, conditional on its assumptions; two coding datasets; elicitation by SFT may over- or under-state latent ability. I read the introduction, taxonomy, setup and passive-self-recognition results; not the full appendices.

## Relevance to us

- Q1 (hiding): reverses the question. A parent cannot easily hide which returning part is "real" from a corrupted copy, because copies of the same model recognise each other's outputs. Conversely, a parent can test returners with honeypots written by a different model, and this paper gives the statistical model for how many honeypots are needed.
- Q2 (thresholds): self-recognition is a correlated-fault mechanism among forks; k-of-n votes among forks of one parent are weaker than the same vote among independent models.
Related: [[jarviniemi-2025-subversion]], [[mallen-2024-subversion]], [[griffin-2024-games]], [[motwani-2024-secret]].
