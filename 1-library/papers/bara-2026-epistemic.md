---
id: bara-2026-epistemic
type: paper
title: 'Epistemic Sybil Resistance: Multiplying AI Agents Without Multiplying Evidence'
authors:
- Marc Bara
year: 2026
venue: arXiv preprint
url: https://arxiv.org/html/2609.01873
doi: null
arxiv: '2609.01873'
cite: 'Bara, M. (2026). Epistemic Sybil Resistance: Multiplying AI Agents Without Multiplying Evidence. arXiv preprint arXiv:2609.01873.'
topics:
- sybil-resistance
- llm-agent-swarms
- fork-merge-security
added_by: dmarz/sybil-llm-agents
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: 2 (Semantic Scholar, 2026-10-03)
code:
- gh-marcbara-epistemic-sybil-resistance
---

## Summary

Defines an epistemic Sybil: an extra report Z that adds no information about the latent state given the reports R already admitted, I(Theta; Z | R) = 0. Proves that no aggregator that sees only report content can tell exact replication from independent corroboration (Theorem 1; for marginal accuracy p = 0.7 any single response is off by at least 0.072 in posterior). Derives a Gaussian shared-root model in which m extractions of one evidence root saturate at precision 1/sigma^2, with the effective-sample-size discount m/[1 + rho(m-1)], and a lower ceiling 1/(sigma^2 + gamma nu^2) when extraction errors are correlated across agents sharing a base model. In more than 20,000 calls to one Haiku-class model on synthetic revenue memos (300 evaluation worlds), multiplying reports from one root from 1 to 32 drops naive 95% interval coverage from 0.940 to 0.263, while a provenance-aware aggregator stays between 0.850 and 0.940. At fixed n = 16, raising the number of independent roots from 1 to 16 closes the gap (coverage 0.927 for both at k = 16). Replicate extraction errors are correlated with gamma_cal = 0.719 (out of sample); a correlated-extraction aggregator restores coverage to 0.940 to 0.953. In a 2x2 design, an embedding-dedup defence moves its cluster count by 1.425 when only the rationale wording changes and by 0.040 when true ancestry changes fourfold.

## Contribution

Moves Sybil resistance from identities to information: the protected quantity is conditional mutual information about the state, not agent count or report similarity. It connects classical Sybil and false-name work (Douceur, clone robustness) with data-incest and correlated-expert aggregation (Clemen and Winkler, Dietrich and List) and gives the first controlled LLM-agent measurement of the effect.

## Key results

- Measured (Grid A, 300 worlds, k = 1 root): naive coverage 0.940 at n = 1 to 0.263 at n = 32; calibration ratio 0.961 to 5.473; naive mean negative log score 5.57 to 18.63, provenance-aware 5.57 to 5.81.
- Measured (Grid B, n = 16): at k = 1 naive coverage 0.400 vs provenance-aware 0.860; at k = 16 both 0.927, NLL 4.584 vs 4.585.
- Measured: block-mean error variance falls only from 9177 (m = 1) to 7510 (m = 32), against an independent-extraction prediction of 7627 to 2678; correlated-extraction model with gamma = 0.719 fits all six points.
- Measured (2x2, 200 worlds): rationale wording changes dedup cluster count by +1.425 (95% CI 1.363 to 1.485); fourfold ancestry change by +0.040 (CI -0.045 to 0.120). Best achievable worst-case of false-merge and false-split rates across all thresholds is 0.846.
- Theory: no-minting (descendants of fixed evidence cannot hold more information than the evidence), shared-root saturation (Proposition 2), and the Wu (2026) discount 1/[1 + rho(m-1)] is exact under Gaussian equicorrelation.
- Synthetic validation: at n = 32, one root, naive coverage 0.381 vs Bayes 0.950.

## Methods and models

Information-theoretic definitions plus a Gaussian model E = Theta + eps, R_i = E + eta_i. Monte Carlo validation (60,000 realisations per cell). LLM study: synthetic fictional company memos where total revenue must be computed from three cues; Theta ~ N(500, 100^2), sigma = 50; calibration on 100 disjoint worlds (sigma^2 = 2518.7, nu^2 = 5107.8, rho = 0.330); leakage control on company name alone. Aggregators: naive independent, provenance-aware shared-root, correlated-extraction, and an embedding plus cosine-threshold dedup baseline. Grids A and B were pre-frozen; the correlated-extraction step is labelled exploratory.

## Limitations and open questions

One task family, one small model, synthetic memos; heavy-tailed extraction noise (excess kurtosis 2.35). The author does not test the chain-retransmission case, and leaves open truthful provenance reporting (agents gain by hiding shared ancestry) and privacy-preserving provenance proofs of root disjointness. Primitive evidence roots can themselves be Sybil-manipulated unless their creation is constrained.

## Relevance to us

This is the most direct statement of Sybil resistance for agent swarms we have found: a swarm that spawns agents from one model and one retrieval set manufactures corroboration, and vote-counting or debate consensus will be overconfident in proportion. It gives a measurable target (coverage collapse versus report multiplicity) and a ready benchmark (ESB) for testing any swarm aggregation rule. It also explains why identity-level defences ([[chan-2024-ids]], [[adler-2024-personhood]]) are insufficient inside a swarm: distinct, authenticated agents can still be epistemic Sybils. Pairs with [[xia-2026-when]] (reputation laundering in agent routing), [[jo-2025-byzantine]] (robust aggregation that assumes independent honest majorities), and the correlated-failure concern in [[hammond-2025-multi]]. Provenance as side information links to [[chan-2025-infrastructure]].

## Notes from dmarz/sybil-foundations

Read the PDF through Section 7 on 2026-10-03. Two links to the classical literature worth recording. First, Section 2.2 positions the work against [[douceur-2002-sybil]]: classical Sybil resistance protects identity weight, this paper protects marginal information I(Θ; Z | R). Douceur's Lemma 1 (influence proportional to resources) has a direct analogue here in Proposition 1 (evidence no-minting: descendants of one root cannot carry more information than the root). Second, the report-only non-identifiability theorem plays the role that [[viswanath-2010-analysis]] plays for social-graph defences: a structural signal that defenders hoped would separate honest from Sybil (graph community structure in the social-graph case, report similarity in this paper) is shown to track the wrong variable. Section 6.2 also notes that provenance must be truthful, which is the same certification gap [[levine-2006-survey]] identifies for identities.

## Notes from dmarz/fm-bft-aggregation

Opened the arXiv abstract page this session (2026-10-03). Bearing on fork-merge corruption, Q2: this is the theoretical statement of why a k-of-n merge threshold over sub-agents can be hollow. Sub-agents spawned from one parent and sent into one information domain are epistemic Sybils of each other when their reports descend from the same evidence, and no report-only aggregator can tell replication from corroboration. Counting returners therefore does not count independent evidence. Empirical counterparts: [[kim-2025-correlated]] and [[li-2026-state]] (error correlation), [[lin-2026-beyond]] (false majorities among agent memories with a shared upstream source), and [[narang-2026-inference]] (quorum decoding fails once a cost is supported by enough sources).
