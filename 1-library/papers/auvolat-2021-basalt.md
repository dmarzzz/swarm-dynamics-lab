---
id: auvolat-2021-basalt
type: paper
title: "BASALT: A Rock-Solid Foundation for Epidemic Consensus Algorithms in Very Large, Very Open Networks"
authors: [Alex Auvolat, Yérom-David Bromberg, Davide Frey, François Taïani]
year: 2021
venue: "arXiv preprint (cs.DC)"
url: https://arxiv.org/abs/2102.04063
doi: null
arxiv: "2102.04063"
cite: "Auvolat, A., Bromberg, Y.-D., Frey, D., & Taïani, F. (2021). BASALT: A Rock-Solid Foundation for Epidemic Consensus Algorithms in Very Large, Very Open Networks. arXiv:2102.04063."
topics: [sybil-resistance, sync-consensus]
added_by: shadow/sol-w5
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: [gh-basalt-rps-avalanchego-basalt]
---

## Summary

Epidemic (gossip, sampling-based) Byzantine consensus such as Avalanche needs a secure random peer sampling (RPS) service in which no attacker can become over-represented. Existing deployments get this from proof-of-stake, which closes the system to low-stake nodes. BASALT replaces stake with network-address diversity as the Sybil defence. Three mechanisms: (1) stubborn chaotic search, where each view slot has a random seed and a ranking function, and the node greedily keeps the best-ranked peer it has seen for that seed, so the target random graph is fixed by the seeds and cannot be steered by attackers; slots are reset round-robin to keep samples fresh; (2) a hit counter per slot that makes over-represented peers less likely to be contacted, so flooding an identity backfires; (3) hierarchical ranking over IP prefixes (/8, /16, /24) so that peers are drawn across many address blocks, which defeats "institutional" attackers owning large contiguous blocks. Botnets with scattered IPs remain a general-Byzantine fraction. Results: theory plus Monte Carlo simulation (Rust, n = 1,000 to 10,000, f = 10-30%, attack force F) show BASALT stays close to the optimal Byzantine sample proportion where Brahms degrades and SPS fails outright (90% of correct nodes isolated). Numerical analysis on GeoLite2 data: an attacker with the largest AS (106M active addresses in 5,739 blocks) facing 1,000 honest nodes gets 21% of samples under hierarchical sampling versus over 99.99% under uniform sampling. Live test on the public AVA network: 100 adversarial nodes in one /24 (about 18.8% of active nodes) received 18.4% of samples under uniform sampling, 17.5% under BASALT-uniform, and 1.13% under hierarchical BASALT. Skimmed: problem statement, algorithm, numerical attack analysis, evaluation and live deployment; theoretical derivations not checked.

## Contribution

A permissionless, stake-free Sybil defence for peer sampling that uses the structure of the IP address space as a scarce resource, with a working patch to a production consensus client.

## Key results

- Largest-AS institutional attack against 1,000 honest nodes: 21% Byzantine samples (hierarchical) vs >99.99% (uniform).
- Live AVA network, 10 h, 100 attacker nodes in one /24: adversary share of samples 1.13% with hierarchical BASALT vs 18.4% uniform.
- Simulation: BASALT almost insensitive to attack force F; Brahms collapses at high sampling rates or high f.
- 500-line patch to AvalancheGo, compatible with the existing network.

## Methods and models

Seeded ranking functions defining an implicit target graph, push/pull view exchanges, hit counters, hierarchical prefix-based ranking; differential-equation model of correct vs Byzantine identifiers seen; Monte Carlo simulation; live deployment.

## Limitations and open questions

Defends against address-concentrated attackers; a botnet with widely spread IPs is only bounded as an ordinary Byzantine fraction. IPv6 address abundance and cloud providers with diverse prefixes weaken the scarcity assumption. Honest nodes sharing a prefix (e.g. behind the same ISP) are sampled less, a fairness cost visible in their live data. Preprint; publication venue not checked.

## Relevance to us

A clean example of using a structural property of identities (network-address diversity) instead of stake or personhood to cap Sybil influence, plus a measurable attacker-power metric. For agent swarms, the analogue would be sampling peers or votes across diverse provenance classes (operator, model, infrastructure) so that one operator's thousand agents count as one class. Classic background: [[douceur-2002-sybil]], eclipse attacks [[singh-2006-eclipse]], [[heilman-2015-eclipse]], [[marcus-2018-low-resource]]; social-graph Sybil defences [[yu-2006-sybilguard]], [[yu-2008-sybillimit]].
