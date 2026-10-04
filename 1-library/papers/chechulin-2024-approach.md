---
id: chechulin-2024-approach
type: paper
title: "Approach to Detecting Malicious Bots in the Vkontakte Social Network and Assessing Their Parameters"
authors: [Andrey A. Chechulin, Maxim Kolomeets]
year: 2024
venue: Proceedings of Telecommunication Universities (Труды учебных заведений связи), vol. 10, no. 2, pp. 92-101
url: https://doi.org/10.31854/1813-324x-2024-10-2-92-101
doi: 10.31854/1813-324x-2024-10-2-92-101
arxiv: null
cite: "Chechulin, A. A., & Kolomeets, M. (2024). Approach to Detecting Malicious Bots in the Vkontakte Social Network and Assessing Their Parameters. Proceedings of Telecommunication Universities, 10(2), 92-101. https://doi.org/10.31854/1813-324x-2024-10-2-92-101"
topics: [swarm-detection, sybil-resistance]
added_by: shadow/sol-w4
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null  # Semantic Scholar rate-limited at access time
code: []
---

## Summary

Proposes a bot-detection approach for the Russian social network VKontakte whose distinctive element is dataset construction by "controlled purchase": the researchers buy bot services on the market, which yields ground-truth bot accounts together with their commercial parameters (price, quality tier, speed of action), and run a Turing-test style study to measure how much ordinary users trust the purchased bots. Features from interaction graphs, text and statistical distributions feed conventional machine-learning classifiers that are trained not only to detect bots but to predict their characteristics. The abstract reports that the trained model is robust to class imbalance and identifies most bot types, with only minor correlation between detection performance and the bots' main characteristics (i.e., cheap and expensive bots are caught at similar rates). Intended uses are countermeasure selection and historical analysis that characterises the specifics of an attack, not just its presence. Abstract-only read (Crossref abstract; the journal PDF link was not opened).

## Contribution

Ground truth for bot detection obtained by purchasing bots rather than by heuristic labelling, which simultaneously gives labels and a parameterisation of the bot market (price, quality, speed), enabling detectors that estimate attacker investment, not only presence.

## Key results

- Detector trained on purchased-bot datasets is robust to imbalance and catches most bot types.
- Detection quality shows only minor correlation with bot price, quality or speed.
- Turing-test component quantifies human trust in bots of different tiers (numbers not captured).

## Methods and models

Controlled purchase of bot services on VKontakte to assemble labelled datasets; user-study Turing test for trust; features from interaction graphs, message text and statistical distributions; traditional ML classifiers (specific algorithms not captured); prediction of bot parameters as auxiliary targets.

## Limitations and open questions

Abstract-only. Single platform; bot market of 2024 (likely pre-LLM or early-LLM bots); purchased bots may not represent state or in-house operations. Whether parameter prediction generalises to bots not sold on the market is open.

## Relevance to us

The controlled-purchase methodology is directly reusable for swarm-detection research: buying agent-swarm services (or standing up our own with known parameters) gives clean ground truth and a cost axis, and the finding that detection is roughly independent of bot price is a useful null to test against LLM agents, where price buys fluency. The attack-characterisation framing (estimate the operator's investment and tooling from traces) matches what the volunteer swarm-chasers are doing by hand ([[x-napleszionist-2106372439093412024]]). Related detectors: [[guo-2026-text]], [[wang-2026-botchf]]; pre-LLM bot ecology: [[li-2024-social]].
