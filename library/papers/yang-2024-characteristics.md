---
id: yang-2024-characteristics
type: paper
title: Characteristics and prevalence of fake social media profiles with AI-generated faces
authors:
- Kai-Cheng Yang
- Danishjeet Singh
- Filippo Menczer
year: 2024
venue: Journal of Online Trust and Safety
url: https://arxiv.org/abs/2401.02627
doi: 10.54501/jots.v2i4.197
arxiv: '2401.02627'
cite: Yang, K.-C., Singh, D., & Menczer, F. (2024). Characteristics and Prevalence of Fake Social Media Profiles with AI-generated Faces. Journal of Online Trust and Safety, 2(4). https://doi.org/10.54501/jots.v2i4.197 (preprint arXiv:2401.02627).
topics:
- swarm-detection
- sybil-resistance
added_by: dmarz/sd-bots
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 21 (Crossref, 2026-10-03)
code: []
---

## Summary

The authors assembled 1,420 Twitter accounts using GAN-generated faces and showed they run scams, spam and coordinated amplification. Using the fixed eye position of StyleGAN faces plus human annotation, they screened a random sample of active users and estimated a lower bound of 0.021% to 0.044% of active accounts with GAN faces, roughly 10,000 daily active accounts.

## Contribution

One of the first in-the-wild prevalence estimates for a generative-AI tell on a major platform, with released code and data.

## Key results

- Dataset of 1,420 GAN-face accounts engaged in scams, spam and coordinated messaging.
- Lower-bound prevalence 0.021%-0.044% of active Twitter accounts, about 10K daily active accounts.
- Eye-placement heuristic plus manual verification used as the detector; [[ricker-2024-ai]] reports this alignment-only screen has a high false discovery rate (85.86% before manual review) and misses cropped faces.

## Methods and models

Eye-landmark alignment test against the canonical StyleGAN position, followed by human annotation; applied to a random sample of active users (about 254K images per [[ricker-2024-ai]]).

## Limitations and open questions

Abstract-level read. Only GAN faces; lower bound by construction. Twitter data access has since closed.

## Relevance to us

Base-rate anchor for 'generative-AI accounts in the wild': about 1 in 2,000-5,000 accounts in 2023 by one tell. Companion to [[yang-2023-anatomy]] (LLM text) and [[ricker-2024-ai]] (larger sample, 0.052%).
