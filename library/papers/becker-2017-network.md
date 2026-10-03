---
id: becker-2017-network
type: paper
title: "Network dynamics of social influence in the wisdom of crowds"
authors: ["Joshua Becker", "Devon Brackbill", "Damon Centola"]
year: 2017
venue: "Proceedings of the National Academy of Sciences"
url: "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5495222/"
doi: "10.1073/pnas.1615978114"
arxiv: null
cite: "Becker, J., Brackbill, D., & Centola, D. (2017). Network dynamics of social influence in the wisdom of crowds. Proceedings of the National Academy of Sciences, 114(26), E5070–E5076. https://doi.org/10.1073/pnas.1615978114"
topics: ["collective-decision", "sync-consensus", "crowds-and-traffic", "llm-agent-swarms"]
added_by: dmarz/collective-decision-audit
accessed: 2026-10-03
read_depth: skim
relevance: 5
citations: "415 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Online experiment with 1,360 participants showing that social influence can improve rather than undermine crowd accuracy, depending on network structure. Groups of 40 estimated quantities from images over three rounds, seeing the average of their network neighbours' answers. In decentralised networks (everyone has the same degree) both the median and the mean became more accurate; in centralised networks the outcome followed the central node, improving when it was right and worsening when it was wrong.

## Contribution

Reverses the conclusion of [[lorenz-2011-how]] by adding network structure and a DeGroot-model explanation: in an equal-degree network the mean is preserved under averaging, and if accurate people revise less (higher self-weight), the mean moves toward the truth. It gives a mechanistic link between individual revision rules, network centralisation and collective accuracy.

## Key results

- Decentralised networks (13 trials): average individual error fell by 23 per cent from round 1 to round 3 (Wilcoxon, P < 0.001); group-median error fell from 0.76 to 0.67 SD (12 per cent, P < 0.001); group-mean error fell from 0.69 to 0.62 SD (10 per cent, P < 0.01).
- Centralised networks: mean and median became less accurate when the central node's estimate lay away from the truth (n = 13, P < 0.01) and more accurate when it lay toward the truth (n = 12, P < 0.01).
- Diversity (SD of estimates) fell significantly after each revision in both network types (P < 0.001), without hurting accuracy in decentralised networks.
- Revision magnitude correlated with initial error (rho = 0.41, 95 per cent CI 0.39 to 0.43, n = 4,340 estimates by 1,040 subjects), the non-i.i.d. self-weighting that lets the mean improve.

## Methods and models

DeGroot update R_{t+1,i} = alpha_i R_{t,i} + (1 - alpha_i) mean_{j in N_i} R_{t,j}. Decentralised (equal-degree) versus centralised (one hub) networks of 40 subjects, plus a no-influence control; three rounds; monetary prize for final-estimate accuracy. Theoretical predictions in the SI. No code repository noted in the text I read.

## Limitations and open questions

Continuous estimation tasks only, three rounds, and one type of centralisation (a single hub). The improvement of the mean depends on accurate people revising less, an empirical regularity that may not hold for adversarial or overconfident populations. Effect sizes are modest (10 to 12 per cent). Later work by the same group and others debates how general the result is; I did not follow that thread here.

## Relevance to us

Directly testable in LLM-agent swarms: does an equal-degree communication graph improve a crowd of model estimates while a hub-and-spoke graph inherits the hub's error? It connects to network-structure effects in animal decision models ([[kao-2014-decision]], [[sueur-2012-from]]) and to the DeGroot and opinion-dynamics line in `sync-consensus` ([[bizyaeva-2023-nonlinear]], [[leonard-2024-fast]]). Compare [[de-marzo-2024-ai]].
