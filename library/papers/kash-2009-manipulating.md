---
id: kash-2009-manipulating
type: paper
title: "Manipulating Scrip Systems: Sybils and Collusion"
authors: [Ian A. Kash, Eric J. Friedman, Joseph Y. Halpern]
year: 2009
venue: Auctions, Market Mechanisms and Their Applications (AMMA 2009), LNICST vol. 14, pp. 13-24, Springer
url: https://arxiv.org/abs/0903.2278
doi: 10.1007/978-3-642-03821-1_4
arxiv: "0903.2278"
cite: "Kash, I. A., Friedman, E. J., & Halpern, J. Y. (2009). Manipulating Scrip Systems: Sybils and Collusion. In Auctions, Market Mechanisms and Their Applications (AMMA 2009), Lecture Notes of the Institute for Computer Sciences, Social Informatics and Telecommunications Engineering, vol. 14, pp. 13-24. Springer. https://doi.org/10.1007/978-3-642-03821-1_4"
topics: [sybil-resistance, collective-decision]
added_by: shadow/sol-p2
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "3 (Crossref, 2026-10-03)"
code: []
---

## Summary

Conference version of the Sybil and collusion analysis later folded into the journal paper [[kash-2012-optimizing]]. Setting: a scrip (token) system in which agents occasionally request a service, one volunteer among those with money-threshold strategies is chosen to provide it, and one unit of scrip changes hands; previous work by the authors showed threshold strategies form an epsilon-Nash equilibrium and that welfare rises with the money supply m per agent until a "crash" where nobody works. This paper drops the assumption that all agents are equally likely to be picked, which is what Sybils break, and redoes the analysis with relative entropy. Theorem 1 gives the long-run fraction of an agent's requests that are satisfied as (r - r^(k+1)) / (1 - r^(k+1)) with r = p_e/p_s (earn probability over request probability) and threshold k, so extra identities raise p_e and help the Sybil owner at the expense of everyone else's p_e. Sybils are self-reinforcing (the more others have them, the worse you do without them) but with sharply diminishing returns, so a modest creation cost usually suffices. Illustrative equilibrium calculations with n = 10,000 agents: if one fifth of agents each add one Sybil, the system crashes at m = 9.5, where without Sybils welfare was near optimal (crash between m = 10.25 and 10.5); when 20 percent of agents hold Sybils, the rest are worse off unless each Sybil owner has at least eight Sybils, in which case total welfare can rise; a discontinuity appears when about a third of agents have Sybils because they start competing with each other. Theorem 2 shows any welfare gain Sybils produce in a single-type population can be achieved by the designer instead, by adjusting m or biasing volunteer selection. Collusion (pooling money within a group) goes through three phases and is mostly Pareto-improving unless colluders serve each other off-system, which makes them act like Sybils. The paper also draws out implications for advertising (creates p_e asymmetries like Sybils) and loans (helpful, but need whitewashing defences). Read: abstract, introduction, model summary, Theorem 1 and the Sybil section, collusion section, conclusion; proofs skimmed.

## Contribution

First equilibrium (rather than assumption-level) account of what Sybils do inside a token-incentivised cooperation system: they redistribute earning opportunities, threaten monetary crashes at money levels that were previously safe, and are better handled by tuning the money supply than by trying to extract their occasional welfare benefit.

## Key results

- Theorem 1: satisfied-request fraction (r - r^(k+1)) / (1 - r^(k+1)), r = p_e/p_s.
- 20 percent of agents with one Sybil each move the crash point from m in (10.25, 10.5) to m = 9.5 (Figure 4).
- Non-Sybil agents break even only if the 20 percent Sybil owners each run at least eight Sybils (Figure 3).
- Discontinuity near one third of agents having Sybils (Figure 2).
- Theorem 2: Sybil welfare gains are replicable by designer parameters in a single-type population.
- Collusion is mostly Pareto improving; serving requests internally turns colluders into effective Sybils (Figure 5).

## Methods and models

Discrete-time scrip model with parameters alpha, beta, gamma, delta, rho, chi (default m = 4, n = 10,000, single rational type); threshold strategies; stationary distributions via relative entropy; equilibria computed numerically with the algorithm from the authors' earlier work.

## Limitations and open questions

Equilibrium calculations, not agent-based runs or deployments; single-type populations for the clean theorems; Sybil cost modelled only qualitatively. The authors explicitly leave loan design and whitewashing prevention open. The journal version [[kash-2012-optimizing]] supersedes this one with altruists and hoarders added; use that for citations unless the 2009 provenance matters.

## Relevance to us

Direct template for reasoning about Sybils in any agent economy with an internal currency or credit (compute credits, reputation points, task tokens): the damage is a shift in who gets picked to work, and the systemic risk is a crash of cooperation at parameter settings that looked safe. Pairs with [[kash-2012-optimizing]], [[douceur-2002-sybil]], and the auction-side Sybil results [[yokoo-2004-effect]], [[gafni-2023-optimal]].
