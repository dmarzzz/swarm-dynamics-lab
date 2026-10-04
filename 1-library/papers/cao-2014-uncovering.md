---
id: cao-2014-uncovering
type: paper
title: "Uncovering Large Groups of Active Malicious Accounts in Online Social Networks"
authors: ["Qiang Cao", "Xiaowei Yang", "Jieqi Yu", "Christopher Palow"]
year: 2014
venue: "Proceedings of the 2014 ACM SIGSAC Conference on Computer and Communications Security (CCS)"
url: http://www.cs.duke.edu/~xwy/publications/SynchroTrap-ccs14.pdf
doi: "10.1145/2660267.2660269"
arxiv: null
cite: "Cao, Q., Yang, X., Yu, J., & Palow, C. (2014). Uncovering Large Groups of Active Malicious Accounts in Online Social Networks. In Proceedings of the 2014 ACM SIGSAC Conference on Computer and Communications Security (pp. 477–488). ACM."
topics: [swarm-detection, sybil-resistance]
added_by: dmarz/sd-coordination
accessed: 2026-10-03
read_depth: skim
relevance: 5
citations: "292 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

SynchroTrap, deployed at Facebook and Instagram, finds malicious accounts by the observation that accounts controlled by one attacker perform loosely synchronized actions: they act on the same targets (pages, apps, followees, IPs) at around the same time for a sustained period. It computes pairwise Jaccard similarity of timestamped actions within time windows, partitioned by target or IP, clusters accounts by single-linkage, and aggregates daily chunks into weekly results on Hadoop and Giraph.

## Contribution

The industrial proof that synchrony-based group detection works at platform scale with near-zero false positives, and an analysis that bounds the action rate an attacker can sustain without being caught, whatever the number of accounts.

## Key results

- In one month (August 2013) at Facebook and Instagram: more than 2 million malicious accounts and 1,156 large campaigns found.
- Precision from manual inspection by Facebook's security team: page likes 99.0% (730K accounts, 357M actions), Instagram follows 99.7% (589K accounts), app installs 100%, photo uploads 100%, logins 100%.
- About 274K malicious accounts caught per week on average over a deployment of more than ten months.
- Processing: a few hours for a day of data and about 15 hours for a weekly aggregation on a 200-machine cluster.
- Security analysis: the detector caps the rate of synchronized malicious actions even for an attacker with unlimited accounts, so evasion requires spreading actions out in time, which reduces attack throughput.

## Methods and models

Action = (user, timestamp, constraint such as target ID or IP). Two accounts match on an action if they hit the same constraint within a time window; similarity is the Jaccard of matched actions. Single-linkage clustering over a similarity threshold; incremental processing. Cross-checked against SybilRank ([[yu-2006-sybilguard]] lineage, implemented in [[gh-binghuiwang-sybildetection]]).

## Limitations and open questions

I read the introduction, design overview and evaluation tables, not the full system sections. Precision is from sampled manual inspection; recall is unknown. Campaigns that spread actions widely in time or use many distinct targets trade throughput for evasion, which an LLM agent swarm with cheap accounts may accept.

## Relevance to us

The strongest in-the-wild number for synchrony-based detection of one operator's many accounts. Its evasion bound (throughput versus synchrony) is the right frame for whether patient agent swarms escape detection. Generalised in [[pacheco-2021-uncovering]].
