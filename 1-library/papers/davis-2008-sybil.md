---
id: davis-2008-sybil
type: paper
title: "Sybil attacks as a mitigation strategy against the Storm botnet"
authors: [Carlton R. Davis, José M. Fernandez, Stephen Neville, John McHugh]
year: 2008
venue: 2008 3rd International Conference on Malicious and Unwanted Software (MALWARE), Alexandria, VA, pp. 32-40
url: https://www.cs.mcgill.ca/~carlton/papers/Malware08.pdf
doi: 10.1109/malware.2008.4690855
arxiv: null
cite: "Davis, C. R., Fernandez, J. M., Neville, S., & McHugh, J. (2008). Sybil attacks as a mitigation strategy against the Storm botnet. In 2008 3rd International Conference on Malicious and Unwanted Software (MALWARE), pp. 32-40. IEEE. https://doi.org/10.1109/MALWARE.2008.4690855"
topics: [sybil-resistance, swarm-detection]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "35 (Crossref, 2026-10-03)"
code: []
---

## Summary

Turns the Sybil attack around: the defender floods a P2P botnet's command-and-control overlay (Storm, built on Overnet/Kademlia with XOR-encrypted messages) with fake nodes in order to insert them into bots' peer lists and starve the bots of real peers, as an alternative to index poisoning (which needs Sybils that stay online to answer FIND_VALUE lookups). A discrete-time simulation of a 20,000-node botnet with 1% per-step attrition and growth (200 nodes/step, net 2% churn), Kademlia k-buckets, peer-list sizes l in {100, 200, 300} and refresh intervals delta-t in {10, 20} steps, injects Sybils at rates SBR of 0.5, 1 and 2 times the bot growth rate (3,000, 6,000, 12,000 Sybils over a run) and measures how reachability inside the non-Sybil subgraph degrades (fraction of bots whose radius-r neighbourhood still covers 10% of the botnet). Mean Sybil insertion into peer lists is 10.5%, 18.7% and 30.9% at the three rates (up to 24.8% on 26,000-node runs); radius-1 reachability drops 16%, 16% and 27-37% respectively but all reachability measures past radius 1 stay at 100%. Conclusion: uninformed Sybil injection, even approaching half the nodes, produces at most about a one-third hit on local reachability and no global disruption, because the binding constraint is whether a Sybil lands on the first responding path to the node holding the answer; informed attacks that target those paths would need near-global knowledge of response times and could be countered by voting; practical takedown would need QoS-level cooperation with ISPs. Read: abstract, introduction, Storm/Overnet background, simulation model and parameters, results (Figs and insertion-rate numbers), discussion and conclusions; related-work section skimmed.

## Contribution

One of the first quantitative studies of Sybil attacks as a defensive tool, and an early negative result: random Kademlia overlays are fairly robust to uninformed Sybil flooding as long as Sybils remain a minority.

## Key results

- Sybil peer-list insertion ratio: 10.53% / 18.67% / 30.94% at SBR = 0.5, 1, 2 x bot growth rate (20,000 bots).
- Radius-1 reachability decrease: ~16% at SBR <= BGR, 27-37% at SBR = 2 BGR; reachability at radius >= 2 unaffected (100%).
- Potency depends on Sybils sitting on first-responding lookup paths, not on raw count.

## Methods and models

Custom simulator of Overnet-style botnet overlay (random graph with Kademlia bucket maintenance), attrition/growth/Sybil-injection rates, reachability metrics on the Sybil-removed subgraph. No live botnet experiments.

## Limitations and open questions

Simulation only, idealised random overlay, no latency model (which the authors note is what an informed attack would exploit); Storm itself was taken down by other means shortly after. The reverse framing (defensive Sybils) raises legal and collateral questions the paper does not address.

## Relevance to us

Useful on two fronts. For sybil-resistance it gives a measured example of how much identity flooding a Kademlia-style network tolerates (contrast the targeted eight-Sybil eclipse in [[steiner-2007-exploiting]]: volume without placement does little). For swarm-detection it is a precedent for "infiltrate the swarm with your own agents to map or degrade it", which is a live option against LLM agent swarms whose coordination runs over open channels. Related: [[douceur-2002-sybil]], [[urdaneta-2011-survey]], [[heilman-2015-eclipse]].
