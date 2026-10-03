---
id: singh-2006-eclipse
type: paper
title: "Eclipse Attacks on Overlay Networks: Threats and Defenses"
authors: ["Atul Singh", "Tsuen-Wan \"Johnny\" Ngan", "Peter Druschel", "Dan S. Wallach"]
year: 2006
venue: "Proceedings IEEE INFOCOM 2006, 25th IEEE International Conference on Computer Communications"
url: https://www.cs.rice.edu/~dwallach/pub/eclipse-infocom06.pdf
doi: "10.1109/INFOCOM.2006.231"
arxiv: null
cite: "Singh, A., Ngan, T.-W. J., Druschel, P., & Wallach, D. S. (2006). Eclipse Attacks on Overlay Networks: Threats and Defenses. In Proceedings IEEE INFOCOM 2006, 25th IEEE International Conference on Computer Communications, Barcelona, Spain."
topics: [sybil-resistance, sync-consensus]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: skim
relevance: 5
citations: "387 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

The paper studies eclipse attacks, where colluding overlay nodes arrange for correct nodes to peer only with the coalition, and shows they work even when Sybil attacks are prevented by certified identities, because malicious nodes can advertise neighbour sets made only of other malicious nodes. The defence observes that an eclipsing node must have higher than average in-degree, so correct nodes bound in-degree and out-degree of their neighbours and enforce the bound by anonymously auditing each neighbour's backpointer set through anonymizer nodes. Simulations on Pastry show the defence holds the malicious fraction of routing entries near the theoretical bound while keeping proximity neighbour selection.

## Contribution

Separates the eclipse attack from the Sybil attack: bounding identities is not enough, influence per identity must also be bounded. It replaces the rigid constrained routing tables of [[castro-2002-secure]] with a degree bound that preserves latency optimisation.

## Key results

- If every node has the same degree and in-degree is bounded at t times the expected out-degree, the fraction of correct nodes' out-degree consumed by malicious nodes is at most f*t/(1-f), where f is the malicious fraction (Section III analysis).
- Without proximity neighbour selection, eclipse attacks put over 70% malicious entries in neighbour sets of a 1,000-node overlay and over 80% at 5,000 nodes; in the top routing-table row over 90% at 1,000 nodes, approaching 100% at 10,000 or more.
- PNS alone reduces the overall malicious fraction to under 30% within 10 simulated hours with GT-ITM delays, but the paper reports that its effectiveness is "significantly reduced" with measured King delays.
- With a tight in-degree bound (t=1) the measured malicious fraction is about 0.25 for f=0.2, matching f*t/(1-f). The delay-stretch penalty is about 25% at a bound of 16 per row in a 20,000-node overlay and about 8% at 32.
- Auditing every 2 minutes drops the malicious fraction below 25% overall within 2 hours under 0-10% hourly churn; at 15% churn the top row stays above 30%, and doubling the audit rate brings it to about 27%. "Higher churn requires more auditing."
- Auditing costs about 2 msg/node/s, secure routing 0.2 msg/node/s; false positive rate about 10^-3 after 10 hours (about 100 of 96,000 connections).

## Methods and models

Analytical degree-bound argument; MSPastry simulations with GT-ITM and King latency data, 20% malicious nodes by default, malicious out-degree of 16 per row, churn at 0-15% per hour. I read the abstract, introduction, background, defence design, the evaluation of attacks, degree bounding, auditing under churn, overhead and false positives; I did not read the anonymity analysis in detail.

## Limitations and open questions

Assumes homogeneous degree; needs secure routing to find anonymizer sets, so it still rests on Castro-style certified ids. Effectiveness degrades as churn rises, and newly joined attackers that have not yet been audited carry most of the excess in-degree.

## Relevance to us

This is the key source for "eclipse as isolating one agent's view": in an agent swarm that learns about peers from peers, a few legitimate but colluding agents can surround a victim without any Sybil identities. The degree bound plus anonymous audit is a concrete influence bound for agent gossip: each agent's in-degree (how many other agents list it as a source) is capped and checked by challenges the audited agent cannot tell apart from normal traffic. The measured churn-versus-audit-rate trade-off maps to continuous agent spawning. Bounds influence, not identities. Related: [[castro-2002-secure]], [[heilman-2015-eclipse]], [[vyzovitis-2020-gossipsub]], [[douceur-2002-sybil]], [[bara-2026-epistemic]].
