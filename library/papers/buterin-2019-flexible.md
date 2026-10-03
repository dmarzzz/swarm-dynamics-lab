---
id: buterin-2019-flexible
type: paper
title: 'A Flexible Design for Funding Public Goods'
authors:
- 'Vitalik Buterin'
- 'Zoë Hitzig'
- 'E. Glen Weyl'
year: 2019
venue: 'Management Science'
url: https://arxiv.org/pdf/1809.06421
doi: 10.1287/mnsc.2019.3337
arxiv: '1809.06421'
cite: 'Buterin, V., Hitzig, Z., & Weyl, E. G. (2019). A Flexible Design for Funding Public Goods. Management Science, 65(11), 5171-5187.'
topics:
- sybil-resistance
- collective-decision
added_by: dmarz/sybil-mechanisms
accessed: 2026-10-03
read_depth: skim
relevance: 5
citations: null
code: []
---

## Summary

The paper proposes quadratic funding (QF, called Liberal Radicalism): a project receives the square of the sum of square roots of individual contributions, with a sponsor covering the gap. Under the standard model of quasi-linear private benefit this gives first-best public goods provision. A capital-constrained variant (CQF) scales the subsidy by alpha. Section 5.2 analyses fraud (one citizen posing as many, i.e. Sybils) and collusion as the central vulnerabilities.

## Contribution

The canonical source of quadratic funding and its explicit Sybil arithmetic, which motivated later identity and cluster-matching work such as [[ethresearch-2023-collusion]].

## Key results

- Fraud example from the paper: under CQF with alpha = 0.1, one citizen posing as 20 who contributes x per identity pays 20x and her cause receives 0.1 times 20^2 x = 40x, doubling her money; the minimum profitable fraud size is 1/alpha.
- Collusion example: a 100-member cartel each paying $1000 is funded at $1,000,000; a single defector who pays nothing still receives $9801 and is $801 better off, so revenue-sharing cartels are unstable.
- The authors state that if fraud cannot be controlled QF becomes a money pump, that identity verification is the necessary first defence, and that small groups receiving large funding should be audited with penalties larger than the fraud.

## Methods and models

Mechanism design with quasi-linear utilities, standard-model welfare analysis, comparison against private contributions and one-person-one-vote. Discussion of applications: campaign finance, open-source software, news media, urban projects.

## Limitations and open questions

I skimmed the abstract, introduction and Section 5 (fraud, collusion, negative contributions). The authors call their own discussion of collusion thin. Sybil defence is delegated to identity verification and auditing outside the mechanism.

## Relevance to us

Quadratic mechanisms reward breadth of support, so they are the archetype of a mechanism that free identities break: the Sybil gain grows quadratically in the number of fake identities. Any swarm that aggregates agent preferences with square-root or per-head weighting needs identity cost or social-graph discounting. See [[ethresearch-2023-collusion]], [[yaish-2026-inequality]] and the LLM agent experiments in [[gh-brunomazorra-llms-sybils]].
