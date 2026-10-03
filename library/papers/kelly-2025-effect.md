---
id: kelly-2025-effect
type: paper
title: "The effect of source reliability and information credibility on judgments of information quality in intelligence analysis"
authors: [Megan O. Kelly, David V. Budescu, Mandeep Dhami, David R. Mandel]
year: 2025
venue: Judgment and Decision Making
url: https://www.cambridge.org/core/journals/judgment-and-decision-making/article/effect-of-source-reliability-and-information-credibility-on-judgments-of-information-quality-in-intelligence-analysis/E67548E8010A47345C3439D45D9EC6B3
doi: 10.1017/jdm.2025.10007
arxiv: null
cite: "Kelly, M. O., Budescu, D. V., Dhami, M., & Mandel, D. R. (2025). The effect of source reliability and information credibility on judgments of information quality in intelligence analysis. Judgment and Decision Making, 20, e36."
topics: [fork-merge-security, collective-decision]
added_by: dmarz/fm
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

Two experiments on how people use the NATO AJP-2.1 information-evaluation scales, the "Admiralty Code" used in defence and security since the 1940s. Each report carries a source reliability letter (A "completely reliable" to E unreliable, F "cannot be judged") and an information credibility number (1 "confirmed by other sources" to 6 "truth cannot be judged"). Experiment 1 used 74 intelligence analysts (52 Canadian, 22 UK); Experiment 2 used 175 non-experts from Canada and the US. Participants rated accuracy, informativeness, trustworthiness and likelihood of use for reports with manipulated reliability and credibility, twice each to measure test-retest consistency. Read from the open-access article page via a fetch-and-summarise tool, so treat as skim.

## Contribution

Measures how the two dimensions of the standard intelligence source code combine in practice, using working analysts, instead of assuming they are used as designed.

## Key results

- Both dimensions had large main effects on quality ratings: in analysts, η²G = .51 for source reliability and .48 for information credibility; in non-experts, .27 and .26.
- A reliability × credibility interaction (η²G = .03 and .01): credibility counted more when the source was reliable, so the dimensions are not treated as independent.
- For trustworthiness, high-reliability/low-credibility reports (A5) were rated above low-reliability/high-credibility ones (E1) in all three analyst comparisons: the source dominated. For accuracy, analysts rated E1 above A5 (t(73) = 2.30, p = .024, d = 0.27).
- Judged accuracy was the main predictor of intent to use the information in both samples; trustworthiness did not predict use in analysts.
- Test-retest error was lowest for moderately inconsistent pairs, contrary to the authors' attribute-consistency hypothesis.

## Methods and models

Mixed factorial repeated-measures design, 100-point sliders, three levels each of reliability and credibility, test-retest within session.

## Limitations and open questions

Only one evaluation system; no operational context given with the ratings; analyst expertise with the code not verified. The study measures how ratings are combined, not whether rated reports turned out true. It does not test the corroboration rule itself, only reports pre-labelled as "confirmed by other sources".

## Relevance to us

The Admiralty Code is a working answer to Q2 from intelligence practice: grade the returning source and the returned content on separate axes, and reserve the top content grade for information confirmed by other, independent sources. For fork-merge agents this maps to two separate merge-gate scores per child report: a reliability score for the child (track record, integrity checks) and a credibility score for each claim (corroboration by other children that explored independently). The measured interaction and the dominance of source reliability for trust show the failure mode: a trusted returning agent's uncorroborated claims get through, which is exactly the doubled-agent attack in [[cowden-2014-pioneering]]. A merge rule should therefore compute credibility mechanically from independent corroboration rather than let the parent combine the two by judgment. Human evidence that receivers ignore partner reliability: [[numbers-2014-influences]]. BFT counterpart: [[lamport-1982-byzantine]].
