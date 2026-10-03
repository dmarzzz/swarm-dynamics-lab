---
id: wu-2024-cbil
type: paper
title: "CBIL: Collective Behavior Imitation Learning for Fish from Real Videos"
authors: ["Yifan Wu", "Zhiyang Dou", "Yuko Ishiwaka", "Shun Ogawa", "Yuke Lou", "Wenping Wang", "Lingjie Liu", "Taku Komura"]
year: 2024
venue: "ACM Transactions on Graphics"
url: https://arxiv.org/abs/2504.00234
doi: "10.1145/3687904"
arxiv: "2504.00234"
cite: "Wu, Y., Dou, Z., Ishiwaka, Y., Ogawa, S., Lou, Y., Wang, W., Liu, L., & Komura, T. (2024). CBIL: Collective Behavior Imitation Learning for Fish from Real Videos. ACM Transactions on Graphics, 43(6), 242:1-242:17."
topics: [collective-motion, marl-emergence]
added_by: dmarz/collective-motion-recent
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "3 (OpenAlex W4404526574, 2026-10-03)"
code: []
---
## Summary

Learns fish schooling behaviour directly from videos without tracked trajectories. A masked video autoencoder learns compact implicit states from 2D video in a self-supervised way; adversarial imitation learning then matches the distribution of motion patterns in that latent space, with bio-inspired rewards and priors to stabilise training. The trained policy animates schools, transfers across species, and can flag abnormal fish behaviour in wild videos.

## Contribution

Imitation learning of collective motion from raw video, removing the need for multi-animal tracking.

## Key results

- Claimed (abstract): realistic, diverse schooling animation; cross-species use; anomaly detection.

## Methods and models

Masked video autoencoder, adversarial imitation (GAIL-like), multi-agent policy (details not read).

## Limitations and open questions

Abstract only; graphics-oriented evaluation, not a biological validation of interaction rules.

## Relevance to us

A learned generative model of schools; compare [[mcgraw-2024-parallel]] and the 3D tracker from the same group [[phurtivilai-2026-trackfish3d]].
