---
id: dathathri-2024-scalable
type: paper
title: Scalable watermarking for identifying large language model outputs
authors:
- Sumanth Dathathri
- Abigail See
- Sumedh Ghaisas
- Po-Sen Huang
- Rob McAdam
- Johannes Welbl
- Vandana Bachani
- Alex Kaskasoli
- Robert Stanforth
- Tatiana Matejovicova
- Jamie Hayes
- Nidhi Vyas
- Majd Al Merey
- Jonah Brown-Cohen
- Rudy Bunel
- Borja Balle
- Taylan Cemgil
- Zahra Ahmed
- Kitty Stacpoole
- Ilia Shumailov
- Ciprian Baetu
- Sven Gowal
- Demis Hassabis
- Pushmeet Kohli
year: 2024
venue: Nature 634, 818-823 (2024)
url: https://www.nature.com/articles/s41586-024-08025-4
doi: 10.1038/s41586-024-08025-4
arxiv: null
cite: Dathathri, S., See, A., Ghaisas, S., Huang, P.-S., McAdam, R., Welbl, J., Bachani, V., Kaskasoli, A., Stanforth, R., Matejovicova, T., et al. (2024). Scalable watermarking for identifying large language model outputs. Nature, 634, 818-823. https://doi.org/10.1038/s41586-024-08025-4.
topics:
- swarm-detection
added_by: dmarz/sd-ai-content
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 345 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Describes SynthID-Text, a production text watermark that changes only the sampling procedure (tournament sampling), integrates with speculative sampling, and is detected without running the LLM. Evaluations show better detectability than comparable schemes with no measurable change in capability, and a live experiment over nearly 20 million Gemini responses confirmed preserved quality. It is deployed in Gemini.

## Contribution

First documented production deployment of an LLM text watermark at scale, which makes provider-side detection of one vendor's output feasible in the wild.

## Key results

- Measured (abstract): live Gemini experiment over nearly 20 million responses showed no quality loss.
- Measured (abstract): improved detectability over comparable methods across multiple LLMs.

## Methods and models

Tournament sampling watermark; speculative-sampling integration; benchmark, human side-by-side and live A/B evaluation. Read the publisher abstract only.

## Limitations and open questions

Only covers text from cooperating providers; open-weight models and paraphrasing remove it ([[zhang-2023-watermarks]], [[krishna-2023-paraphrasing]]). Detection at population scale (for example scanning a platform for SynthID) is not reported. Abstract depth.

## Relevance to us

The one deployed watermark: a swarm built on Gemini without paraphrasing would be detectable by the provider, so watermark presence is a weak operator-attribution signal. Third parties can detect that a watermark exists ([[gloaguen-2024-black]]).
