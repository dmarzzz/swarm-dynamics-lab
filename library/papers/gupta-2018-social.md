---
id: gupta-2018-social
type: paper
title: 'Social GAN: Socially Acceptable Trajectories with Generative Adversarial Networks'
authors:
- Agrim Gupta
- Justin Johnson
- Li Fei-Fei
- Silvio Savarese
- Alexandre Alahi
year: 2018
venue: 2018 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)
url: https://arxiv.org/abs/1803.10892
doi: 10.1109/cvpr.2018.00240
arxiv: '1803.10892'
cite: 'Gupta, A., Johnson, J., Fei-Fei, L., Savarese, S., & Alahi, A. (2018). Social GAN: Socially Acceptable Trajectories with Generative Adversarial Networks. In 2018 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2255–2264. https://doi.org/10.1109/cvpr.2018.00240'
topics:
- crowds-and-traffic
- collective-motion
added_by: dmarz/crowds-and-traffic-audit
accessed: '2026-10-03'
read_depth: skim
relevance: 3
citations: 2046 (Crossref is-referenced-by-count, 2026-10-03; OpenAlex budget exhausted)
code: []
---

## Summary

Treats pedestrian trajectory forecasting as a multimodal problem: given 3.2 s of observed positions for everyone in a scene, generate several socially plausible futures rather than one average path. An LSTM encoder–decoder generator conditioned on a pooled summary of all other people is trained adversarially against an LSTM discriminator, with a "variety loss" that only penalises the best of k samples so the generator spreads its output. On the five ETH/UCY scenes it beats linear, LSTM and Social LSTM baselines on displacement error when allowed 20 samples, and runs about 16 times faster than Social LSTM.

## Contribution

Moved data-driven crowd prediction from deterministic regression ([[alahi-2016-social]]) to generative, multimodal forecasting, and replaced grid-based social pooling with a scene-wide MLP-plus-max-pool over relative positions. It established the best-of-20 ADE/FDE protocol on ETH/UCY that most later learned predictors (for example [[salzmann-2020-trajectron]]) report against, a protocol later criticised for rewarding diversity over calibration ([[korbmacher-2022-review]]).

## Key results

Measured on ETH, HOTEL, UNIV, ZARA1, ZARA2 (leave-one-scene-out), ADE/FDE in metres for 8 / 12 predicted steps (3.2 / 4.8 s):
- Average ADE: linear 0.54 / 0.79, LSTM 0.43 / 0.70, Social LSTM 0.45 / 0.72, SGAN-20V-20 0.39 / 0.58, SGAN-P 20VP-20 0.41 / 0.61.
- Average FDE: linear 0.98 / 1.59, Social LSTM 0.91 / 1.54, SGAN-20V-20 0.78 / 1.18.
- With a single sample (1V-1), SGAN is no better than the LSTM baselines (ADE 0.49 / 0.74), so the gains rely on scoring the best of 20 samples.
- Speed: 16x faster than Social LSTM at inference (table 2).
- Qualitative: the pooling variant (SGAN-P) produces predictions that avoid collisions, groups walking together and speed changes in four hand-picked scenarios.

## Methods and models

Inputs: relative displacements embedded by an MLP into an LSTM encoder. Pooling module: for each person, relative positions to all others are passed through an MLP and max-pooled into a pooled vector P_i. Decoder LSTM initialised with encoder state, P_i and noise z. Discriminator: LSTM encoder classifying real versus generated full trajectories. Loss: adversarial loss plus variety loss L = min_k ||Y − Ŷ^(k)||_2 over k samples. Data: ETH and UCY datasets at 0.4 s per step. Code: https://github.com/agrimgupta92/sgan (MIT, 918 stars, last push 2023-11-24, per GitHub API).

## Limitations and open questions

- Best-of-k evaluation flatters generative models; single-sample accuracy is not better than simpler baselines.
- ETH/UCY scenes are sparse and short; behaviour in dense crowds, where physical interactions dominate ([[gu-2025-emergence]]), is untested.
- No physical constraints; predictions can still collide or be dynamically infeasible (addressed in [[salzmann-2020-trajectron]]).

## Relevance to us

The reference generative model for "learn the interaction rule from data" in crowds, and a baseline to compare with physics-based rules ([[helbing-1995-social]], [[karamouzas-2014-universal]]). For swarm work it is a template for learning a pooled neighbour representation that is permutation invariant (MLP plus max-pool), as in deep-sets style swarm policies. Related robot-navigation use: [[chen-2019-crowd]].
