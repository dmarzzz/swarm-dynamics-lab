---
id: hopkins-2025-factorio
type: paper
title: "Factorio Learning Environment"
authors: ["Jack Hopkins", "Mart Bakler", "Akbir Khan"]
year: 2025
venue: "arXiv preprint"
url: https://arxiv.org/abs/2503.09617
doi: null
arxiv: "2503.09617"
cite: "Hopkins, J., Bakler, M., & Khan, A. (2025). Factorio Learning Environment. arXiv preprint arXiv:2503.09617."
topics: [llm-agent-swarms, agent-budgets]
added_by: dmarz/factory-scan
accessed: 2026-10-03
read_depth: skim
relevance: 5
citations: "5 (Semantic Scholar, 2026-10-03)"
code: [gh-jackhopkins-factorio-learning-environment]
---

## Summary

FLE wraps the game Factorio as a text environment: an LLM agent acts by writing Python programs against a tool API in a REPL, and observes stdout/stderr from its last program. It has two settings: lab-play (the HTML v1 says 24 fixed-resource tasks to build a factory hitting a target throughput of an item, from iron ore up to utility science packs; the arXiv API abstract says eight) and open-play ("build the largest factory possible" on a procedurally generated map). The reward is a Production Score (PS) computed from Factorio's own item pricing: raw ores have seed prices (iron ore 3.1, copper ore 3.6, coal 3.0, stone 2.4, uranium 8.2) and every crafted item's value is the sum of its ingredients times a complexity multiplier that grows with ingredient count, plus a square-root energy term. PS is the value of production minus consumption, so it grows by orders of magnitude as automation deepens. Measured: Claude 3.5 Sonnet was the strongest model, completing 7 of 24 lab-play tasks and reaching a median open-play PS of 293,206 with 28 milestones, against Llama-3.3-70B at 54,998 PS. All models failed at complex automation such as electronic circuits.

## Contribution

An open-ended, non-saturating LLM-agent benchmark with real recipe chains, build costs and an endogenous price system. Earlier Factorio work (Reid et al. 2021, arXiv 2102.04871, not catalogued) used integer programming and evolutionary methods on belt layout only.

## Key results

- Measured: lab-play success falls as recipe depth rises; no model passed tasks needing more than about three factory sections.
- Measured: Claude 3.5 Sonnet invested in research and deployed electric mining drills around step 3k, lifting PS about 1.5x (200k to 300k); other models rarely researched.
- Measured: degenerate debug loops, e.g. GPT-4o repeated the same API misuse for 78 contiguous steps.
- Measured: total experiment cost $1,318 across models (Table 3).
- Stated: "all our current experiments use single-agent interaction"; multi-agent cooperative and competitive play (shared bases, competition for finite high-yield ore patches) is named as future work.

## Methods and models

Models: Claude 3.5 Sonnet, GPT-4o, GPT-4o-mini, DeepSeek-v3, Gemini-2-Flash, Llama-3.3-70B, temperature fixed. Open-play runs 5k steps (server calls). Metrics: PS and milestones (first creation of each entity type). Appendix A gives the full pricing recursion. Read: abstract, sections 1 to 6, Appendix A.

## Limitations and open questions

The authors note no human API baseline, missing late-game entities (trains, logistics robots, circuits), and that agents occasionally triggered game resets (a reward-hacking surface). PS is a single-force production value, not a market price: there is no demand curve, so it does not model competition between firms. The paper itself is single-agent; multi-agent support arrived later in the repo (see [[gh-jackhopkins-factorio-learning-environment]]).

## Relevance to us

The strongest substrate for the planned swarm factory: resource nodes, recipe chains and build costs already exist, and the item-value recursion could seed marginal costs for firms. What we would have to add is a shared market with inverse demand (as in [[lin-2024-strategic]] and [[bracale-syrnikov-2026-institutional]]) so that several agent firms sell into it. The finding that frontier agents stall at early automation means production capacity, not pricing, may bind first; a simplified recipe graph may be needed for clean collusion measurements. Related production-economy substrates: [[al-omari-2025-multi]], [[zheng-2020-ai]], [[backlund-2025-vending]].
