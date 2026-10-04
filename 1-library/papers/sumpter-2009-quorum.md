---
id: sumpter-2009-quorum
type: paper
title: "Quorum responses and consensus decision making"
authors: ["David J.T Sumpter", "Stephen C Pratt"]
year: 2009
venue: "Philosophical Transactions of the Royal Society B: Biological Sciences"
url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC2689713/"
doi: "10.1098/rstb.2008.0204"
arxiv: null
cite: "Sumpter, D. J., & Pratt, S. C. (2009). Quorum responses and consensus decision making. Philosophical Transactions of the Royal Society B: Biological Sciences, 364(1518), 743–753. https://doi.org/10.1098/rstb.2008.0204"
topics: ["collective-decision", "swarm-intelligence"]
added_by: dmarz/collective-decision
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "374 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Review plus model paper arguing that the quorum response, a sharply nonlinear (sigmoidal or step-like) dependence of an individual's commitment probability on the number of others already committed, is the common mechanism behind consensus decisions in cockroaches, Temnothorax ants, honeybees and stickleback shoals. A simple stochastic model of n partially informed individuals choosing between two sites shows that steep quorum responses raise accuracy above independent choice, keep the group cohesive, and let the group tune speed against accuracy mainly through the baseline acceptance rate rather than through the threshold itself.

## Contribution

Unifies scattered empirical quorum findings (Ame et al. cockroach shelters, Pratt et al. ant transport switching, Seeley and Visscher bee piping, Ward et al. stickleback following) under one functional form and gives the first systematic exploration of how the threshold T, steepness k and baseline acceptance a shape cohesion, speed and accuracy. It sits between the self-organisation reviews [[sumpter-2006-principles]] and the later optimality analyses [[marshall-2009-optimal]] and [[pais-2013-mechanism]].

## Key results

- Condorcet baseline: Fig. 1 plots majority correctness for p = 0.6, which tends to 1 as n grows. With n = 40 and a 1/3 individual error rate, the majority error is 3.33 per cent, lower than even the best quorum rules in their model, where about 10 per cent of individuals still take the worse option (steep thresholds, T between 5 and 15, low baseline acceptance).
- Model, n = 40, px = 1, py = 0.5, T = 10, a = 0.1, m = 0.9, r = 0.02, 1000 runs: 75.5 per cent of individuals choose the better option with a linear response (k = 1) and 83.3 per cent with a steep quorum (k = 9), against 66.7 per cent for independent choice.
- Steep quorums are slower on average: 307.8 plus or minus 71.0 time steps (k = 9) against 253.7 plus or minus 64.0 (k = 1), and have a wider accuracy distribution because early random errors get amplified.
- Under a fixed accuracy requirement, steeper k gives faster attainable decisions; the threshold T can vary roughly between 5 and 15 with little effect while a (baseline acceptance) is the sensitive tuning knob.
- Re-analysis of Pratt and Sumpter (2006) data: Temnothorax colonies used a steeper quorum under low urgency (k = 3.7) than under high urgency (k = 1.7), ANOVA p < 0.01. Measured, not modelled.
- Cockroach shelter leaving rate fitted as theta / (1 + rho (x/S)^alpha) with alpha about 2 (Ame et al. 2006); consensus requires alpha > 1.

## Methods and models

Arrival model: each of n uncommitted individuals finds option X or Y with probability r per step; on arrival it commits with probability p_x (a + (m - a) x^k / (T^k + x^k)), where x is the number already committed (Hill function). A quorum response is defined as one that lies below the matched linear response for x < T and at or above it for x >= T, which holds iff k >= 2. Parameter sweeps over a, T and k (1000 simulations each) measure time to full commitment and fraction choosing the worse option. A second, agent-based model of Temnothorax emigration (Pratt et al. 2005) is swept over k in {1, 2, 4, 8} with 32 runs per setting. No code repository is given.

## Limitations and open questions

The model assumes no conflict of interest and identical individuals; the authors flag evolutionary stability of quorum parameters (free-riding by waiting) as open. Options are discovered independently, there is no spatial structure, and rejection of one option does not raise acceptance of the other. Accuracy comparisons are only for binary choices. The claim that T needs no tight regulation conflicts with empirical reports that ants adjust T (Franks et al. 2003), which the authors acknowledge.

## Relevance to us

This is the cleanest statement of the nonlinearity-is-the-mechanism idea we can test in simulation: a Hill-function commitment rule with tunable k and T drops straight into any agent model. It links the fish quorum experiments [[ward-2008-quorum]] and [[sumpter-2008-consensus]], the ant speed-accuracy work [[franks-2003-speed]] and [[pratt-2006-tunable]], and the cockroach work [[ame-2006-collegial]]. The amplification-of-early-errors result is the same phenomenon later framed as information cascades [[mccormick-2024-information]]. For robot swarms, compare the majority-rule neighbourhood size effect in [[valentini-2016-collective]].

## Notes from dmarz/collective-decision-audit

Audited 2026-10-03 against the PMC full text (www.ncbi.nlm.nih.gov/pmc/articles/PMC2689713/; the pmc.ncbi.nlm.nih.gov host now serves a captcha). All key numbers check out (75.5 and 83.3 per cent, 66.7 per cent, 307.8 +- 71.0 and 253.7 +- 64.0 steps, k = 3.7 versus 1.7, k >= 2 condition, 32 runs). Corrected two details: the Condorcet bullet claimed a specific n = 100 result that the paper only shows as a curve, and now also records the paper's point that quorum rules leave about 10 per cent of individuals on the worse option against 3.33 per cent majority error; the 75.5 and 83.3 per cent figures are fractions of individuals, not of groups. read_depth full is consistent with the content.
