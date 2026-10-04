---
id: rao-2025-detecting
type: paper
title: Detecting LLM-Generated Peer Reviews
authors:
- Vishisht Rao
- Aounon Kumar
- Himabindu Lakkaraju
- Nihar B. Shah
year: 2025
venue: arXiv preprint
url: https://arxiv.org/html/2503.15772
doi: null
arxiv: '2503.15772'
cite: 'Rao, V., Kumar, A., Lakkaraju, H., & Shah, N. B. (2025). Detecting LLM-Generated Peer Reviews. arXiv preprint arXiv:2503.15772.'
topics:
- swarm-detection
added_by: dmarz/sd-honeypots
accessed: '2026-10-03'
read_depth: skim
relevance: 5
citations: null
code: []
---

## Summary

Embeds a hidden instruction in a manuscript PDF (white text, a custom font whose glyphs render as different letters, or obfuscated "cryptic" prompts) that asks any LLM writing a review to include a watermark phrase chosen at random per review: a fake citation, a rare technical term from the 1,000 least-used ICLR 2024 keywords, or a fixed opening sentence. Because the watermark is drawn by the organiser independently of the review process, the false-positive probability for a human review is bounded without any model of human writing. The authors give hypothesis tests that control the family-wise error rate across thousands of reviews with more power than Bonferroni or Holm.

## Contribution

The canary-trap idea made statistically rigorous: a planted, randomised, agent-only instruction plus an FWER-controlled test. The paper also notes that Latona et al. estimated at least 15.8% of ICLR 2024 reviews were AI-assisted.

## Key results

- Random fake-citation watermark appears in 98.6% of LLM-generated reviews on average across models and injection methods (measured).
- Over 94% of watermarked reviews keep the watermark after LLM paraphrasing (measured).
- Zero false positives when applied to over ten thousand human reviews; Bonferroni and Holm corrections become infeasible (flag nothing) at that scale (measured).
- Font-embedding injection made the watermark appear in all 10 regenerations in ChatGPT 4o in their example (reported).

## Methods and models

Datasets: ICLR 2024 submissions, Peer Review Congress 2022 abstracts, PeerRead, NSF proposals; multiple commercial LLMs; Algorithms 2 and 3 reallocate the error budget adaptively across reviews and watermarks. Skimmed: intro, design criteria, watermark types, detection algorithms and headline results.

## Limitations and open questions

Requires the agent to ingest the planted document whole; a reviewer who strips hidden text, uses OCR on rendered pages, or instructs the model to ignore embedded instructions defeats it. Ethics of planting instructions in documents is discussed by [[lin-2025-hidden]].

## Relevance to us

The best template for statistically defensible canary detection at population scale: choose a random canary per exposure, then test with FWER control. For swarm detection, replace "review" with "post" or "reply" and "manuscript" with any bait document agents read. [[seiden-2026-identifying]] borrows its collision argument. Related: [[gharami-2025-chatgpt]], [[collu-2025-misleading]].
