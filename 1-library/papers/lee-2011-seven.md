---
id: lee-2011-seven
type: paper
title: 'Seven Months with the Devils: A Long-Term Study of Content Polluters on Twitter'
authors:
- Kyumin Lee
- Brian Eoff
- James Caverlee
year: 2011
venue: Proceedings of the International AAAI Conference on Web and Social Media (ICWSM)
url: https://ojs.aaai.org/index.php/ICWSM/article/view/14106
doi: 10.1609/icwsm.v5i1.14106
arxiv: null
cite: 'Lee, K., Eoff, B. D., & Caverlee, J. (2011). Seven Months with the Devils: A Long-Term Study of Content Polluters on Twitter. Proceedings of the International AAAI Conference on Web and Social Media, 5(1), 185–192. https://doi.org/10.1609/icwsm.v5i1.14106'
topics:
- swarm-detection
added_by: dmarz/sd-honeypots
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: null
code: []
---

## Summary

Sixty social honeypot accounts on Twitter posted random tweets sampled from the public timeline (plain text, @replies to each other, links, trending topics), followed and replied only to each other, and logged every account that followed or messaged them. From 30 December 2009 to 2 August 2010 they tempted 36,043 accounts; after dropping accounts that hit more than one honeypot and short-lived accounts, 22,223 polluters were profiled against 19,276 random users confirmed still active after three months. Classifiers on demographic, follow-graph, content and temporal-history features separated the two groups with about 98% accuracy, and a model trained on honeypot catches transferred to an independent set of accounts reported to @spam and later suspended.

## Contribution

The canonical long-run social-honeypot deployment, with the key methodological argument for a passive trap: an account that engages in no legitimate activity should attract no legitimate contact, so anything that contacts it is suspect. It also shows that honeypot catches can bootstrap a classifier that generalises beyond the trap.

## Key results

- 36,043 accounts tempted; 5,773 (24%) followed more than one honeypot; one account was tempted by 27 honeypots (measured). Multi-honeypot hits are themselves a coordination signal.
- Twitter eventually suspended 5,562 (23%) of 23,869 single-honeypot catches, on average 18 days after the honeypot caught them and up to 204 days later (measured): traps detect earlier than the platform.
- Polluters followed about 2,123 and had about 2,163 followers on average, posted about four tweets a day to look normal, and showed follower churn: mean change rate of following 29.6 vs 1.5 for legitimate users (measured).
- Random Forest 98.42% accuracy (F1 0.984); boosted 98.62%; transfer to 2,833 independently suspended @spam accounts 96.75% (bagged 98.37%, F1 0.992) (measured, 10-fold CV and held-out set).
- Under simulated obfuscation, single feature groups give 76% (demographics only) to 96% (follow network only); three groups give 95-98% (measured).

## Methods and models

Honeypot accounts with hourly re-crawling of every tempted account (tweets, following/follower counts, status); EM clustering into duplicate spammers, duplicate @ spammers, malicious promoters, friend infiltrators; 30 Weka classifiers; chi-squared feature ranking (top: std. dev. of following IDs, change rate of following). Read in full from the AAAI PDF.

## Limitations and open questions

Labels are 'tempted by a honeypot', not ground truth; random 'legitimate' users may include polluters (authors argue this lowers measured accuracy). Pre-LLM adversaries; content features like compression ratio and duplicate tweets will not catch LLM-written variety.

## Relevance to us

The base methodology for social-platform honeypots aimed at swarms: inert bait accounts, a hit log, follow-up crawling, then a classifier. The multi-honeypot overlap statistic is a cheap coordination detector. LLM-era counterparts: [[reworr-2024-llm]] for infrastructure, [[cornelissen-2018-deploying]] for a political replication. Precursor: [[lee-2010-uncovering]].
