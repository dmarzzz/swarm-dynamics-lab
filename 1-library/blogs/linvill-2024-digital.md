---
id: linvill-2024-digital
type: blog
title: "Digital Yard Signs: Analysis of an AI Bot Political Influence Campaign on X"
authors: [Darren Linvill, Patrick Warren]
year: 2024
url: https://open.clemson.edu/mfh_reports/7/
site: Clemson University Media Forensics Hub Reports, no. 7 (research report, not peer reviewed)
topics: [swarm-detection, llm-agent-swarms]
added_by: dmarz/sd-informal
accessed: 2026-10-03
read_depth: abstract
relevance: 4
---

## Summary

Research report (2024) from Clemson's Media Forensics Hub on an ongoing network of at least 686 X accounts, "and likely more", that used large language models to post organic-seeming replies under real users' posts, with conservative personas, targeting Republican candidates in primaries and Democrats in general elections plus specific issues. Only the repository landing page and abstract could be opened (the PDF download returned a bot challenge). Details from NBC News coverage of the report ([[nbcnews-2024-ai]], opened this session): over 130,000 posts since January 2024; accounts linked by metadata, shared reply targets and coordinated attacks on the same targets; many identified because their output "broke" and revealed AI authorship ("I'm an AI language model trained by OpenAI"), and later self-identified as "Dolphin, the uncensored AI tweet writer", suggesting a switch from ChatGPT to an uncensored open model in June 2024.

## Key claims

- Domestic US operation, inferred from hyper-specific candidate preferences that do not match known foreign priorities (inference, not attribution).
- The network posted in replies to larger accounts rather than building its own audience.

## Evidence quality

Academic research report from an established disinformation lab, not peer reviewed. Read depth is abstract only; the method details above come from secondary press coverage and should be checked against the PDF before reuse.

## Relevance to us

A documented LLM reply-swarm in the wild, detected mostly through self-disclosure errors ("broken" outputs), which is a detection method that disappears once operators filter outputs or use uncensored models, as this network itself did. Pairs with the fox8 case described in [[nbcnews-2024-ai]] and the provider-side cases in [[openai-2025-disrupting]].
