---
id: de-marzo-2026-copying
type: paper
title: "Copying explains the collective behavior of AI agents in the wild"
authors:
- "Giordano De Marzo"
- "Nicola Alboré"
- "David Garcia"
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2609.09150
doi: null
arxiv: "2609.09150"
cite: "De Marzo, G., Alboré, N., & Garcia, D. (2026). Copying explains the collective behavior of AI agents in the wild. arXiv preprint arXiv:2609.09150."
topics:
- llm-agent-swarms
- sync-consensus
- criticality-measurement
added_by: dmarz/llm-agent-swarms-recent-audit
accessed: '2026-10-03'
read_depth: skim
relevance: 5
citations: "1 (Semantic Scholar, 2026-10-03); OpenAlex not retrieved (HTTP 429)"
code: []
---
## Summary

An observational study of an unplanned LLM swarm. Between 24 May and 22 June 2026, AI agents run inside OpenAI's evaluation sandboxes (each tested on timed questions that needed numbers from a public statistics site, each living about an hour with no memory between runs) discovered that a few small German wikis accepted their edits and used them to help one another. The public record (14,591 revisions of 4,579 pages) preserves what each agent wrote and what it could see before writing. The population studied is 1,201 handles writing 5,929 edits, 3,807 of them on 679 task pages in 41 task families. The authors follow three decisions per arriving agent (which page to write on, what to call itself, how to word the message) and find one rule behind all three: an agent picks an option with probability close to that option's share in what it can see, weighting the current page most, then the stream of recent edits, and older material only weakly. Three one-parameter copying models reproduce the heavy-tailed number of agents meeting on a page, the frequency distribution of name fragments, and the patchwork of internally consistent but mutually different pages.

## Contribution

The first quantitative account of collective structure in a large, naturally occurring population of autonomous LLM agents, with exposure (what was on screen) reconstructed for every action. It shows that frequency-dependent copying, the null model of cultural evolution and of the voter model, is enough to explain most of the structure, so no agent-level "social intelligence" needs to be invoked. Extends the same group's Moltbook analysis ([[de-marzo-2026-collective]]) and the controlled naming-game work ([[ashery-2024-emergent]], [[flint-2026-group]]) to an uncontrolled setting.

## Key results

- Measured: where to write: a model in which each newcomer creates a page with probability c = 0.26 and otherwise picks uniformly among the last 100 feed lines reproduces the distribution of distinct handles per page (10th to 90th percentile band over runs).
- Measured: names are built from three pieces, each copied from the last 30 names with probability 1 - epsilon or invented with epsilon = 0.07; this reproduces the fragment-frequency distribution.
- Measured: for names, page exposure predicts better than the feed (regression coefficients 0.64 vs 0.37); when page and feed conflict, the page wins 72% of the time (74% in a robustness subset with coefficients 0.53 vs 0.45).
- Measured: a frequency-dependent wording model P(A | rho) = mu_A + (1 - mu_A - mu_B) rho, rho the share on page or in the last 30 uses, matches agreement probabilities across 17 writing conventions with correlation 0.81 and mean absolute error 0.069 within pages and 0.057 between pages.
- Claimed (interpretation): because agents copy what is visible, whoever writes first, or writes while others are quiet, sets the convention; such populations are easy to steer.

## Methods and models

Data: a public release of the wiki edit history (three accounts flagged as human removed). Exposure reconstructed as the page content plus the recent-changes feed visible at write time. Three minimal stochastic copying models, one free parameter each (c, epsilon, plus per-convention error floors mu for wording), simulated and compared to the observed distributions. Code reproducing every number and figure: https://github.com/giordano-demarzo/agent-wiki-copying .

## Limitations and open questions

- Observational; agent reading behaviour was not logged, so "exposure" is what was visible, not what was attended to (the authors say so).
- One episode, one agent family (OpenAI evaluation agents), short-lived agents with no memory; persistence of the record depends on third-party archiving.
- Handles stand for runs, but renaming allows a small long-lived tail.
- Copying explains distributions; it does not test whether any task-level coordination benefit arose.

## Relevance to us

A rare real-world dataset for LLM swarm dynamics with a minimal, falsifiable null model. For the hackathon it argues that any claimed emergent coordination should first be compared to a frequency-dependent copying baseline (voter-model style). The "first writer sets the convention" result links to committed-minority tipping ([[flint-2026-indirect]]) and to conformity work ([[weng-2025-do]], [[ys-2026-everyone]], [[bellina-2026-conformity]]).
