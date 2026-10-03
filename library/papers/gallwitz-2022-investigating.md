---
id: gallwitz-2022-investigating
type: paper
title: Investigating the Validity of Botometer-based Social Bot Studies
authors:
- Florian Gallwitz
- Michael Kreil
year: 2022
venue: Disinformation in Open Online Media (MISDOOM 2022), Lecture Notes in Computer Science
url: https://arxiv.org/abs/2207.11474
doi: 10.1007/978-3-031-18253-2_5
arxiv: '2207.11474'
cite: Gallwitz, F., & Kreil, M. (2022). Investigating the Validity of Botometer-Based Social Bot Studies. In Disinformation in Open Online Media (MISDOOM 2022), Lecture Notes in Computer Science, pp. 63-78. Springer. https://doi.org/10.1007/978-3-031-18253-2_5 (preprint arXiv:2207.11474).
topics:
- swarm-detection
added_by: dmarz/sd-bots
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: 16 (Crossref is-referenced-by-count, 2026-10-03)
code: []
---

## Summary

Gallwitz and Kreil argue that using a bot classifier score with a chosen threshold to estimate bot prevalence is circular, because the threshold encodes a prior on bot prevalence, and then manually audit accounts that two peer-reviewed Botometer studies counted as bots. In a deterministic sample of 109 'bots' following German party accounts and 121 'vaccine bots' from a US study, they found no account that fits the definition of a malicious social bot; 116 of the 121 were plainly human.

## Contribution

The sharpest negative result against score-threshold prevalence estimates of bots in the wild. It moves the burden of proof onto any study that reports a bot share without releasing account lists for audit.

## Key results

- Replicating Keller and Klinger's German-party follower study in May 2019 with the same 0.76 (3.8/5) threshold gave 270,572 of 521,991 accounts (51.8%) as bots, five times the 9.9% the original study reported; a 0.5 threshold gave 67%.
- Of 109 inspected 'bots' (scores 3.857-4.931) none was a social bot; more than 20% had posted exactly one tweet, a pattern Botometer reliably scored near maximum.
- Of 121 inspected 'vaccine bots' (from 197,971 flagged at the 0.5 threshold, 3.8% of 5.1M accounts), 116 were human-operated with no sign of automation and 5 were benign automation (IFTTT feeds, a hashtag retweet bot); the authors extrapolate about 190k human accounts falsely counted.
- False-positive rates on known humans measured by the authors: 47% of US Congress members (April 2018, dropping to 0.4% in May 2019), 12% of Nobel laureates, 17.7% of Reuters journalists, 35.9% of dpa staff; false negatives: 36% of New Scientist's known bots and 60.7% of Botwiki bots scored human.
- Cites two other studies that manually checked Botometer output: 0 bots in 500 hand-labelled users (Botometer flagged 29), and 1 automated account among 68 flagged.

## Methods and models

Theoretical argument via the Bayes decision rule (adjusting the threshold is equivalent to setting p(Bot), the quantity being estimated). Empirical part: deterministic sampling (every 2,500th or 1,500th account in a sorted list) from two studies' bot lists, manual inspection of timelines, clients, timing (accountanalysis.app) and identity of the operators.

## Limitations and open questions

Small audited samples (230 accounts) from two studies; one study's data were re-collected 20 months later, so drift could explain part of the gap. The authors did not audit accounts Botometer scored human, so they cannot give a full confusion matrix. Botometer has since changed and the Twitter API that made audits possible is gone. Strongly worded; see the reply in [[cresci-2023-demystifying]].

## Relevance to us

Any team that wants to report 'X% of agents in this population are AI' must not do it by thresholding a detector trained elsewhere. The circularity argument applies directly to LLM-agent detectors: a prevalence estimate needs a calibration set drawn from the target population. Pairs with [[rauchfleisch-2020-false]] and [[hays-2023-simplistic]].
