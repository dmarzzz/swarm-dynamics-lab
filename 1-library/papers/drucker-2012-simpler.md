---
id: drucker-2012-simpler
type: paper
title: 'Simpler sybil-proof mechanisms for multi-level marketing'
authors:
- 'Fabio A. Drucker'
- 'Lisa K. Fleischer'
year: 2012
venue: 'Proceedings of the 13th ACM Conference on Electronic Commerce (EC ''12)'
url: https://api.openalex.org/works/doi:10.1145/2229012.2229046
doi: 10.1145/2229012.2229046
arxiv: null
cite: 'Drucker, F. A., & Fleischer, L. K. (2012). Simpler sybil-proof mechanisms for multi-level marketing. In Proceedings of the 13th ACM Conference on Electronic Commerce (EC ''12), 441-458. ACM.'
topics:
- sybil-resistance
added_by: dmarz/sybil-mechanisms
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: 'OpenAlex 2026-10-03: 44'
code: []
---

## Summary

Multi-level marketing rewards buyers for direct referrals and also for indirect referrals linked through chains of direct referrals, to encourage early purchase and recruitment of influential people. Rewarding indirect referrals makes the scheme vulnerable to Sybil attacks in which a profit maximiser creates replicas of itself in the chain. The paper designs simpler referral reward mechanisms that are Sybil-proof.

## Contribution

Sybil-proof referral rewards for tree-structured recruitment, contemporaneous with and cited by [[babaioff-2012-bitcoin]].

## Key results

- The abstract states the problem and that the mechanisms are Sybil-proof; specific bounds were not in the text available to me.

## Methods and models

Referral tree model with rewards for direct and indirect referrals; replicas are inserted into the chain.

## Limitations and open questions

Abstract-level read; the OpenAlex abstract is truncated and I could not open the full paper, so the mechanism details are not recorded here.

## Relevance to us

Recruitment trees appear in agent swarms whenever agents are paid for bringing in other agents or sub-tasks. The Sybil attack is the same as in [[babaioff-2012-bitcoin]] and [[chen-2013-sybil]]: insert yourself twice in the chain. Use as a pointer to the referral-mechanism family.
