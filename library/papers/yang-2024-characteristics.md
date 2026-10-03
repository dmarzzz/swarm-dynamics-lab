---
id: yang-2024-characteristics
type: paper
title: Characteristics and prevalence of fake social media profiles with AI-generated faces
authors:
- Kai-Cheng Yang
- Danishjeet Singh
- Filippo Menczer
year: 2024
venue: Journal of Online Trust and Safety 2(4), 2024
url: https://arxiv.org/abs/2401.02627
doi: 10.54501/jots.v2i4.197
arxiv: '2401.02627'
cite: Yang, K.-C., Singh, D., & Menczer, F. (2024). Characteristics and prevalence of fake social media profiles with AI-generated faces. Journal of Online Trust and Safety, 2(4). https://doi.org/10.54501/jots.v2i4.197. arXiv:2401.02627.
topics:
- swarm-detection
- sybil-resistance
added_by: dmarz/sd-ai-content
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 35 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Builds a dataset of 1,420 Twitter (X) accounts whose profile pictures are GAN-generated faces and shows they spread scams and spam and amplify coordinated messages. Detects such profiles from a GAN artefact (consistent eye placement) plus human annotation, then applies the method to a random sample of active users to estimate a lower bound of 0.021% to 0.044% of profiles, about 10K daily active accounts.

## Contribution

A platform-wide prevalence lower bound for fake personas built with generative AI, and a cheap artefact-based detector.

## Key results

- Measured (abstract): 1,420 GAN-face accounts catalogued.
- Measured (abstract): prevalence lower bound 0.021%-0.044% of active Twitter users, around 10K daily active accounts.

## Methods and models

Eye-position artefact of StyleGAN faces as a filter, human annotation, random sampling of active users. Abstract read only.

## Limitations and open questions

Only GAN faces with the eye-alignment artefact; diffusion-model faces would be missed. Abstract depth.

## Relevance to us

Generative profile images as an account-level Sybil marker; coordinated amplification links it to [[yang-2023-anatomy]]. Independent replication with a different pipeline: [[ricker-2024-ai]].
