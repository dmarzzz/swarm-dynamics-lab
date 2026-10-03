---
id: lee-2010-uncovering
type: paper
title: 'Uncovering Social Spammers: Social Honeypots + Machine Learning'
authors:
- Kyumin Lee
- James Caverlee
- Steve Webb
year: 2010
venue: Proceedings of the 33rd International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR 2010)
url: https://faculty.cse.tamu.edu/caverlee/pubs/lee10sigir.pdf
doi: 10.1145/1835449.1835522
arxiv: null
cite: 'Lee, K., Caverlee, J., & Webb, S. (2010). Uncovering Social Spammers: Social Honeypots + Machine Learning. In Proceedings of the 33rd International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR 2010), pp. 435–442. https://doi.org/10.1145/1835449.1835522'
topics:
- swarm-detection
added_by: dmarz/sd-honeypots
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

Proposes the two-step social-honeypot pipeline: deploy honeypot profiles that log unsolicited contact, then train classifiers on the harvested profiles to find spammers the honeypots never touched. MySpace: 51 honeypot profiles (one per U.S. state plus D.C.) collected 1,570 profiles that sent unsolicited friend requests between October 2007 and January 2008. Twitter: a mix of honeypots collected 500 users in August to September 2009. Classifiers reached above 98.4% accuracy on MySpace (best: Decorate, 99.21%, 0.7% false positives) and above 82.7% on Twitter (best about 5.7% false positives), and were then run on 215,345 unseen Twitter profiles with spam precision as the metric.

## Contribution

Introduces honeypot-harvested labels as training data for platform-wide detection, so that the trap produces a classifier as well as a list.

## Key results

- MySpace: 1,570 spam profiles; 57.2% copied their About Me text from another profile (a reuse signal relevant to template-driven swarms) (measured).
- MySpace classifiers above 98.4% accuracy, F1 above 0.98, FPR below 1.6%; Decorate 99.21% accuracy, 0.7% FPR (measured).
- Twitter top-10 classifiers above 82.7% accuracy, FPR below 10.3%; best around 5.7% FPR (measured).
- Taxonomy of caught accounts: click traps, friend infiltrators, pornographic storytellers, pill pushers, duplicate spammers, promoters, phishers (observation).

## Methods and models

Honeypot profiles plus a bot that records friend requests and messages and crawls the sender's profile and linked pages; Weka classifiers on profile features; held-out wild sets scored by spam precision. Skimmed: abstract, framework, deployment, observations and headline classifier results from the authors' PDF.

## Limitations and open questions

Labels come from the trap itself, which biases toward accounts that contact strangers indiscriminately; pre-LLM adversaries.

## Relevance to us

Origin of the honeypot-to-classifier bootstrap that any swarm-detection pipeline can reuse. Successor study: [[lee-2011-seven]]. Contemporary related work: Stringhini et al. 2010 (ACSAC, honey profiles on Facebook/MySpace/Twitter), not catalogued because we could not open it this session.
