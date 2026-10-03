---
id: ethresearch-2023-collusion
type: blog
title: 'Collusion Resistance and Plurality in Quadratic Mechanisms (Paper Summary)'
authors:
- 'Jmiller4'
year: 2023
url: https://ethresear.ch/t/collusion-resistance-and-plurality-in-quadratic-mechanisms-paper-summary/14545
site: ethresear.ch
topics:
- sybil-resistance
- collective-decision
added_by: dmarz/sybil-mechanisms
accessed: 2026-10-03
read_depth: full
relevance: 4
---

## Summary

A forum post by Jmiller4, dated 4 January 2023, summarising a paper by Glen Weyl, Leon Erichsen and Joel Miller on making quadratic funding resistant to coordinated groups by using information about which agents belong to which groups. It defines collusion resistance as three diminishing-returns properties and compares Pairwise Discounting, Cluster Match, Connection-Oriented Cluster Match (COCM) and Eigen Match against them. The post names the paper 'Collusion Resistance and Plurality in Quadratic Mechanisms'; the SSRN record for the same author group is titled 'Beyond Collusion Resistance: Leveraging Social Information for Plural Funding and Voting' (SSRN 4311507, 2022), which I could not open (HTTP 403), so I catalogue the summary post rather than the paper.

## Key claims

- Collusion resistance is defined as: an agent contributing x attracts O(sqrt x) matching; a coordinating group contributing x collectively attracts O(sqrt x); if x agents join a group each contributing y, matching is O(sqrt x) and O(sqrt y).
- Pairwise Discounting attenuates parts of the funding but lacks diminishing returns from adding members.
- Cluster Match builds synthetic group donations and applies quadratic funding to them, but fails diminishing returns for agents and for groups.
- Connection-Oriented Cluster Match combines ideas from Pairwise Discounting and Cluster Match and achieves all three properties.
- Eigen Match uses eigenvectors of the social graph's adjacency matrix to calibrate funding.
- The analysis assumes accurate information about group memberships.

## Evidence quality

A summary of a formal paper by one of its authors, posted on the Ethereum research forum. Claims are mathematical properties of the mechanisms; the post contains no empirical evaluation and does not claim Sybil resistance or deployment. A later Gitcoin blog post on COCM came up in search but returned HTTP 502 and is not catalogued. The underlying mechanism is quadratic funding from [[buterin-2019-flexible]].

## Relevance to us

COCM is the most developed attempt to make a breadth-rewarding aggregation rule robust by discounting contributions from agents that are socially connected, rather than by proving identities. For an agent swarm the analogue is to discount votes or contributions from agents that share an operator, a funding source or a communication cluster. Note that the guarantees cover coordinated real agents and depend on correct group data; pure Sybils that hide their links are outside the model, so it complements identity cost ([[mazorra-2023-cost]]) rather than replacing it. Compare the social-network false-name-proofness in [[conitzer-2010-using]] and the reputation impossibility in [[cheng-2005-sybilproof]].
