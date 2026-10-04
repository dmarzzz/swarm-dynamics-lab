---
id: lin-2026-you
type: paper
title: "You Can't Fool Us: Understanding the Resilience of LLM-driven Agent Communities to Misinformation"
authors: [Chichen Lin, Yijie Jin, Kangbo Hu, Weijian Fan, Han Xiao, Yongbin Wang, Zhihui Ying, Zhanzhan Zhao]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/html/2605.17353
doi: null
arxiv: '2605.17353'
cite: "Lin, C., Jin, Y., Hu, K., Fan, W., Xiao, H., Wang, Y., Ying, Z., & Zhao, Z. (2026). You Can't Fool Us: Understanding the Resilience of LLM-driven Agent Communities to Misinformation. arXiv preprint arXiv:2605.17353."
topics: [llm-agent-swarms]
added_by: dmarz/honeypot-vigilance
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: null
code: []
---

## Summary

CoSim builds 16 synthetic communities of N = 200 LLM agents on a small-world network (mean degree 6, rewiring 0.1), crossing four distributions of Actively Open-minded Thinking with four of political ideology, and shocks them with credible but refuted claims drawn from 5,194 Chinese fact-check records (105 selected). Over 10 rounds, 10% of agents are exposed each round; trust trajectories give a robustness score (area under the trust curve) and a recovery score (fall from peak). Higher open-mindedness improves both; polarised communities keep more residual support. Among interventions, accuracy prompts mostly add early caution, while persuasion and fact checking drive post-peak correction.

## Contribution

Treats resilience as two stages, uptake and post-peak recovery, and shows they respond to different interventions. That split is the shape V4 needs for "does a false belief outlive correction".

## Key results

- Pre-peak query rate rises from 25.31% (lowest AOT row) to 41.93% (highest), max cell 46.17% (measured).
- Best communities score about 58/23 on robustness/recovery (e.g. G10 58.03/23.26) (measured).
- Accuracy prompt cuts pre-peak support by 3.90 points and raises pre-peak querying by 5.43 points but helps less after the peak; persuasion and fact checking better convert support into denial; source warnings have the weakest effect (measured).

## Methods and models

Persona prompts from sampled trait scores; agents see peer posts, update a trust score, and pick stances (support, query, deny, etc.); several LLM backbones. Skimmed the method, RQ results and limitations.

## Limitations and open questions

Misinformation is true-or-false news, not a threat warning; Chinese claims and an expert-coded ideology map limit generality. Recovery is relative to the community's own peak, not compared with how long a true claim persists.

## Relevance to us

V4: provides recovery and residual-support metrics that can be reused for a false honeypot alarm, and warns that "early caution" interventions (like a generic warning) do not drive later correction. Pair with [[yan-2026-when]] (false testimony persists after the deceiver leaves) and [[becker-2026-misinformation]].
