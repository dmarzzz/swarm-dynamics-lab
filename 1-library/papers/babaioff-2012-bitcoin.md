---
id: babaioff-2012-bitcoin
type: paper
title: 'On Bitcoin and Red Balloons'
authors:
- 'Moshe Babaioff'
- 'Shahar Dobzinski'
- 'Sigal Oren'
- 'Aviv Zohar'
year: 2012
venue: 'Proceedings of the 13th ACM Conference on Electronic Commerce (EC ''12)'
url: https://arxiv.org/pdf/1111.2626
doi: 10.1145/2229012.2229022
arxiv: '1111.2626'
cite: 'Babaioff, M., Dobzinski, S., Oren, S., & Zohar, A. (2012). On bitcoin and red balloons. In Proceedings of the 13th ACM Conference on Electronic Commerce (EC ''12), 56-73. ACM.'
topics:
- sybil-resistance
- collective-decision
- sync-consensus
added_by: dmarz/sybil-mechanisms
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: 'OpenAlex 2026-10-03: 238 (EC version)'
code: []
---

## Summary

Nodes that learn a fee-paying Bitcoin transaction compete with every other informed node for the fee, so they have an incentive not to relay it. The authors model relaying over a forest of d-ary trees of height H and propose reward schemes that pay nodes on the chain from the seed to the authorizer. Because a node can insert fake copies of itself into the chain, the schemes must be Sybil-proof. The (beta, H)-almost-uniform scheme pays every chain member beta and the authorizer 1 + beta(H - h + 1), mimicking the payment it would get from cloning. A Hybrid scheme combining beta = 1 and beta = 1/H achieves full propagation with no duplication as the only profile that survives every order of iterated removal of weakly dominated strategies, using a constant number of seeds and expected total payment at most 3.

## Contribution

The first positive Sybil-proof result for information propagation that relies on iterated dominance rather than dominant strategies, plus an impossibility showing dominant-strategy Sybil-proofness is unattainable. It frames the 2009 DARPA red balloon recursive incentive scheme as vulnerable to Sybils.

## Key results

- Theorem 2.1: with d >= 3, at least 7 seeds and at least 2/beta + 6 other informed nodes, only profiles where every node within depth H propagates and never duplicates survive every iterated elimination order; total payment 1 + H beta.
- Corollary 2.2: beta = 1/H with at least 2H + 13 seeds gives total payment 2; beta = 1 with at least 15 seeds gives payment H + 1.
- Theorem 2.3 (Hybrid scheme): d >= 3, t >= 15 seeds (7 on a 1 + log H scheme, t - 7 on the 1/H scheme) yields expected payment at most 3, worst case 2 + log_d H, and at least (t-7)/t of the network informed.
- Theorem 3.1: for H >= 3 no Sybil-proof reward scheme makes propagation without duplication a dominant strategy for all nodes at depth 3 or less.
- The key intuition measured in the proof: cloning once before relaying shrinks each child's subtree by one level, losing almost a factor d of descendants who could earn relay rewards.

## Methods and models

Game-theoretic model with a distribution phase and a computation phase; authorization probability is uniform over real informed nodes (fake identities do not raise it). Strategy of a node depends only on the length of the chain it observes. Proofs by a phi-subgame induction on the maximum number of clones a node may insert. Appendix maps the scheme onto Bitcoin transaction fields.

## Limitations and open questions

Network is modelled as complete d-ary trees, not random graphs, and nodes have equal hash power; the authors list random d-regular graphs and heterogeneous CPU as open. The solution concept is iterated dominance, not dominant strategy, by necessity. No implementation or empirical test.

## Relevance to us

Any swarm that pays agents for recruiting or forwarding (referral trees, task delegation chains, gossip relays) faces the same tension: informed agents lose by sharing, and paying for sharing invites agents to clone themselves into the chain. The almost-uniform scheme is a concrete template: pay the final worker as if it had cloned, so cloning adds nothing. The impossibility result says a designer should expect only equilibrium-level guarantees. Related referral work: [[drucker-2012-simpler]], [[chen-2013-sybil]], [[zhang-2023-collusion]], [[chen-2022-sybil]].
