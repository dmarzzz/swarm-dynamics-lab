---
id: lorenz-2011-how
type: paper
title: "How social influence can undermine the wisdom of crowd effect"
authors: ["Jan Lorenz", "Heiko Rauhut", "Frank Schweitzer", "Dirk Helbing"]
year: 2011
venue: "Proceedings of the National Academy of Sciences"
url: "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3107299/"
doi: "10.1073/pnas.1008636108"
arxiv: null
cite: "Lorenz, J., Rauhut, H., Schweitzer, F., & Helbing, D. (2011). How social influence can undermine the wisdom of crowd effect. Proceedings of the National Academy of Sciences, 108(22), 9020–9025. https://doi.org/10.1073/pnas.1008636108"
topics: ["collective-decision", "sync-consensus", "crowds-and-traffic", "llm-agent-swarms"]
added_by: dmarz/collective-decision-audit
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "1047 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Laboratory experiment on whether letting people see each other's estimates helps or hurts the wisdom of crowds. 144 ETH Zurich students in 12 groups of 12 answered six factual estimation questions five times each, with monetary rewards for accuracy, under three conditions: no information, the group mean of the previous round, or the full trajectories of all others' estimates. Social information made estimates converge sharply but did not reduce the collective error, pushed the truth to the edge of the estimate range, and raised individual confidence.

## Contribution

The standard empirical reference for the claim that social influence erodes the independence that crowd wisdom relies on. It names three effects (social influence, range reduction, confidence) and introduces a "wisdom-of-crowd indicator" that measures how centrally the truth sits within the sorted estimates. It is the result that [[becker-2017-network]] later qualifies by showing that network structure decides the sign of the effect.

## Key results

- Estimates were right-skewed: the arithmetic mean beat individual first estimates in only 21.3 per cent of cases, the geometric mean (mean of log estimates) in 77.1 per cent, so the authors aggregate on log scale (measured).
- Social influence effect: group diversity (mean squared deviation from the group mean, on normalised log estimates) dropped strongly under both information conditions while collective error changed only slightly; the control condition showed almost no change (24 groups per condition; Kolmogorov-Smirnov, F and t tests in SI).
- Range reduction effect: the wisdom-of-crowd indicator (0 to 6 for 12 estimates) was about one unit lower with information exchange than in the control, and the drop was larger under aggregated (mean-only) information than full information (linear regression over rounds 2 to 5).
- Confidence effect: self-reported certainty (six-point Likert) rose more between first and fifth estimates under social information, despite no accuracy gain.

## Methods and models

z-Tree lab experiment, six questions on Swiss geography and crime statistics (e.g. murders in Switzerland in 2006, true value 198), five estimation rounds per question, rewards for estimates within 10, 20 or 40 per cent of the truth. Each session posed two questions per condition with randomised order. Error decomposition by the diversity prediction theorem: collective error = mean individual error minus diversity. Raw data are in the PNAS Dataset S1 (no code repository).

## Limitations and open questions

Groups of 12 with all-to-all visibility of either the mean or everyone's answers; no network structure, so the result cannot say whether sparse or decentralised exchange would behave differently (which is what [[becker-2017-network]] tested). Only five rounds and six questions. The "undermining" is mostly about diversity and the position of the truth, not a measured increase in collective error. I skimmed the results and design; the SI statistics were not checked.

## Relevance to us

The cleanest human baseline for herding and information cascades in a collective estimation task, directly analogous to LLM-agent swarms that see each other's answers ([[de-marzo-2024-ai]], [[burton-2024-how]]). Pairs with the animal work on early-error amplification in quorum rules [[sumpter-2009-quorum]] and on cascades [[mccormick-2024-information]]. An LLM-swarm replication of the three effects with log-scale aggregation is a cheap hackathon experiment.
