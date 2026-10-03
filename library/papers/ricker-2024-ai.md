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
venue: Proceedings of the 27th International Symposium on Research in Attacks, Intrusions and Defenses (RAID 2024)
url: https://arxiv.org/abs/2404.14244
doi: 10.1145/3678890.3678922
arxiv: '2404.14244'
cite: 'Ricker, J., Assenmacher, D., Holz, T., Fischer, A., & Quiring, E. (2024). AI-Generated Faces in the Real World: A Large-Scale Case Study of Twitter Profile Images. In Proceedings of the 27th International Symposium on Research in Attacks, Intrusions and Defenses (RAID ''24), pp. 513-530. https://doi.org/10.1145/3678890.3678922'
topics:
- swarm-detection
- sybil-resistance
added_by: dmarz/sd-bots
accessed: '2026-10-03'
read_depth: full
relevance: 4
citations: 11 (Crossref, 2026-10-03)
code: []
---

## Summary

A measurement study of how many Twitter accounts use StyleGAN2 (thispersondoesnotexist) faces as profile pictures. The authors built a face pre-filter plus a ResNet-50 detector trained on images that had been uploaded to and re-downloaded from Twitter, calibrated a threshold on 910 hand-labelled images, and ran it on 14,989,385 profile images from the 1% stream in March 2023. They found 7,723 generated faces (0.052%) and then characterised the accounts: bulk-created, short-lived and often part of coordinated spam networks.

## Contribution

The largest in-the-wild base rate for one generative-AI tell in social media accounts, with error rates estimated on held-out labels and an independent set, and a demonstration that a cheap per-account artefact can surface whole coordinated networks.

## Key results

- Prevalence 0.052% (7,723 of 14,989,385 profile images); estimated false negative rate 3.03% (2.75% on an independent set of 1,420 documented fakes) and false discovery rate 1.4%.
- Pre-trained GAN detectors failed on Twitter-processed images; training on images round-tripped through Twitter was necessary.
- 52.07% of fake-face accounts were suspended nine months later versus 5.01% of a random real-face sample; 52.38% were created in 2023 (versus 6.22%).
- One cluster of 1,579 accounts created 16-20 February 2023 (up to 754 in a day), 94.93% with exactly 106 followers and 95.31% following exactly two accounts, posting templated tweets with a Chinese hashtag; an Arabic cluster of 1,806 accounts shared the same template.
- Of 1,000 still-active fake-face accounts inspected in 2024, 36.1% posted political content and 33.1% finance (mostly crypto).

## Methods and models

Pipeline: BlazeFace pre-filter (face present, inter-eye distance at least 0.1), ResNet-50 classifier trained on Twitter-processed TPDNE and FFHQ images plus 10,000 proxy-real images of high-follower accounts; threshold 0.99 chosen by F1 on manual labels assisted by landmark alignment and GAN inversion. Account and tweet analysis on the 1% stream; sentence-embedding clustering of 111,165 tweets.

## Limitations and open questions

Only StyleGAN2/TPDNE faces are targeted; diffusion-model faces and cropped faces are out of scope, so 0.052% is a lower bound for AI faces in general. One week of collection, before the post-2023 API shutdown, so not replicable on X today. The authors note their rate exceeds the 0.021-0.044% of [[yang-2024-characteristics]] and attribute the gap to better recall and to excluding default avatars.

## Relevance to us

Shows the generic recipe for swarm detection by artefact: find a cheap per-agent tell, calibrate on hand labels, then pivot from flagged accounts to the coordination structure (shared creation dates, identical follower counts, templated text). The same pivot is how [[yang-2023-anatomy]] found an LLM botnet. A likely LLM-era analogue is a model-specific text or behaviour tell.

## Notes from dmarz/sd-ai-content

This lane catalogued the same source independently (added_by dmarz/sd-ai-content, accessed 2026-10-03). Its distinct content:

- Frontmatter `venue` in this lane's version: RAID 2024 (27th International Symposium on Research in Attacks, Intrusions and Defenses)
- Frontmatter `cite` in this lane's version: 'Ricker, J., Assenmacher, D., Holz, T., Fischer, A., & Quiring, E. (2024). AI-Generated Faces in the Real World: A Large-Scale Case Study of Twitter Profile Images. In Proceedings of the 27th International Symposium on Research in Attacks, Intrusions and Defenses (RAID 2024). ACM. https://doi.org/10.1145/3678890.3678922. arXiv:2404.14244.'
- Frontmatter `read_depth` in this lane's version: abstract
- Frontmatter `citations` in this lane's version: 31 (Semantic Scholar, 2026-10-03)

### Summary

Measures AI-generated profile pictures on Twitter with a multi-stage detection pipeline over nearly 15 million profile images and finds 0.052% were artificially generated. Examines the flagged accounts and their tweets and uncovers coordinated inauthentic behaviour, with motives including spam and political amplification.

### Contribution

Independent large-scale prevalence estimate of generated faces on one platform, plus links from image signal to coordination.

### Key results

- Measured (abstract): 0.052% of about 15 million Twitter profile pictures AI-generated.
- Observed (abstract): patterns of coordinated inauthentic behaviour among flagged accounts; spam and political amplification motives.

### Methods and models

Multi-stage pipeline combining data sources and detectors for generated faces. Abstract read only.

### Limitations and open questions

Image-only signal; operators can swap to real stolen photos. Abstract depth.

### Relevance to us

Agrees in order of magnitude with [[yang-2024-characteristics]] (0.02-0.05%). Both show the image tell is a seed for finding coordinated clusters rather than a detector on its own.
