---
id: lloyd-2025-there
type: paper
title: "\"There Has To Be a Lot That We're Missing\": Moderating AI-Generated Content on Reddit"
authors: [Travis Lloyd, Joseph Reagle, Mor Naaman]
year: 2025
venue: Proceedings of the ACM on Human-Computer Interaction, vol. 9, CSCW264 (ACM CSCW 2025)
url: https://arxiv.org/abs/2311.12702
doi: 10.1145/3757445
arxiv: "2311.12702"
cite: "Lloyd, T., Reagle, J., & Naaman, M. (2025). \"There Has To Be a Lot That We're Missing\": Moderating AI-Generated Content on Reddit. Proceedings of the ACM on Human-Computer Interaction, 9(CSCW264). https://doi.org/10.1145/3757445"
topics: [swarm-detection]
added_by: shadow/sol-w4
accessed: 2026-10-03
read_depth: skim
relevance: 2
citations: null  # Semantic Scholar rate-limited at access time
code: []
---

## Summary

Qualitative CSCW study based on fifteen semi-structured interviews, conducted within a year of ChatGPT's launch, with volunteer moderators of Reddit communities that restrict AI-generated content (AIGC). RQ1 asks why such communities restrict AIGC; RQ2 asks what moderators have experienced. On RQ1, moderators cite content quality (poorly written, inaccurate, off-topic), social dynamics (fewer opportunities for human connection, strained relationships, violated shared values) and governance (AIGC raises the scale and sophistication of existing bad behaviour). On RQ2, clarifying rules and norms with the community partly contained the disruption, but enforcement is hard: moderators believe they can detect AIGC, yet rely on time-consuming, imperfect heuristics that look for "tells" in content and behaviour, automated detectors are not reliable enough to automate the decision, and accusing a member of posting AIGC is socially sensitive. The authors frame communities through Preece's empathic communities, Lave and Wenger's communities of practice and Jenkins' knowledge communities to explain why attitudes differ, link to their own quantitative work showing content-generation subreddits most likely to adopt AI rules, and recommend platform designs that support authenticity signalling, keep members aware of norms, synthesise detection evidence for moderators, and let communities opt out of generative AI features. We read the abstract, introduction and first related-work section; the findings and discussion sections were not read.

## Contribution

An early, grounded account of how human community stewards actually detect and govern machine-generated participation, documenting that detection in practice is heuristic, labour-intensive and norm-mediated rather than tool-driven.

## Key results

- Fifteen moderators of AIGC-restricting subreddits; motivations cluster into content quality, social dynamics and governance burden.
- Moderators report being able to detect AIGC but only through slow, inaccurate heuristics on textual and behavioural tells; no automated tool was trusted to decide alone.
- Norm clarification with the community reduced disruption more than detection tooling did.
- Content-generation communities are most likely to have AI rules; social-support communities least (from the authors' linked quantitative study).

## Methods and models

Semi-structured interviews (n = 15) with Reddit moderators, qualitative coding; no computational model or dataset beyond the interviews. Interviews conducted in the first year after ChatGPT's release.

## Limitations and open questions

Small, self-selected sample from communities that already restrict AIGC, so it says nothing about communities that welcome it; a snapshot from 2023 when AIGC was a single-author phenomenon rather than agent populations. The authors flag possible bias in moderators' heuristics (who gets accused). What "tells" moderators use is described qualitatively, not measured against ground truth.

## Relevance to us

Peripheral to swarm detection but a useful baseline for the human side of the problem: the frontline detectors of machine participation in 2023 were volunteers with heuristics, and the paper's recommendation to synthesise signals for them is the same gap that 2026 volunteer swarm-chasers fill by hand ([[x-napleszionist-2106372439093412024]]). Shows that behavioural tells, not content classifiers, carried the load even before agents coordinated. Related platform-side framing: [[x-himanshiet-2103730840144633924]].
