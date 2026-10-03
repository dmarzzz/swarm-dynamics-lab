---
id: ricker-2024-ai
type: paper
title: 'AI-Generated Faces in the Real World: A Large-Scale Case Study of Twitter Profile Images'
authors:
- Jonas Ricker
- Dennis Assenmacher
- Thorsten Holz
- Asja Fischer
- Erwin Quiring
year: 2024
venue: RAID 2024 (27th International Symposium on Research in Attacks, Intrusions and Defenses)
url: https://arxiv.org/abs/2404.14244
doi: 10.1145/3678890.3678922
arxiv: '2404.14244'
cite: 'Ricker, J., Assenmacher, D., Holz, T., Fischer, A., & Quiring, E. (2024). AI-Generated Faces in the Real World: A Large-Scale Case Study of Twitter Profile Images. In Proceedings of the 27th International Symposium on Research in Attacks, Intrusions and Defenses (RAID 2024). ACM. https://doi.org/10.1145/3678890.3678922. arXiv:2404.14244.'
topics:
- swarm-detection
- sybil-resistance
added_by: dmarz/sd-ai-content
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 31 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Measures AI-generated profile pictures on Twitter with a multi-stage detection pipeline over nearly 15 million profile images and finds 0.052% were artificially generated. Examines the flagged accounts and their tweets and uncovers coordinated inauthentic behaviour, with motives including spam and political amplification.

## Contribution

Independent large-scale prevalence estimate of generated faces on one platform, plus links from image signal to coordination.

## Key results

- Measured (abstract): 0.052% of about 15 million Twitter profile pictures AI-generated.
- Observed (abstract): patterns of coordinated inauthentic behaviour among flagged accounts; spam and political amplification motives.

## Methods and models

Multi-stage pipeline combining data sources and detectors for generated faces. Abstract read only.

## Limitations and open questions

Image-only signal; operators can swap to real stolen photos. Abstract depth.

## Relevance to us

Agrees in order of magnitude with [[yang-2024-characteristics]] (0.02-0.05%). Both show the image tell is a seed for finding coordinated clusters rather than a detector on its own.
