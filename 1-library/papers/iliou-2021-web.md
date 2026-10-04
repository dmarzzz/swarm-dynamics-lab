---
id: iliou-2021-web
type: paper
title: "Web Bot Detection Evasion Using Generative Adversarial Networks"
authors: [Christos Iliou, Theodoros Kostoulas, Theodora Tsikrika, Vasilis Katos, Stefanos Vrochidis, Ioannis Kompatsiaris]
year: 2021
venue: "2021 IEEE International Conference on Cyber Security and Resilience (CSR)"
url: https://zenodo.org/record/5549387
doi: 10.1109/CSR51186.2021.9527915
arxiv: null
cite: "Iliou, C., Kostoulas, T., Tsikrika, T., Katos, V., Vrochidis, S., & Kompatsiaris, I. (2021). Web Bot Detection Evasion Using Generative Adversarial Networks. In 2021 IEEE International Conference on Cyber Security and Resilience (CSR), pp. 115-120. https://doi.org/10.1109/CSR51186.2021.9527915"
topics: [swarm-detection]
added_by: shadow/sol-w5
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "7 (Crossref, 2026-10-03)"
code: []
---

## Summary

Attack-side companion to the same group's mouse-biometrics detector ([[iliou-2021-detection]]). Web servers detect bots from fingerprints and behaviour, and mouse-movement analysis had been shown to be very effective. Here the bots use GANs to generate images of mouse-movement and (for mobile web bots) touchscreen trajectories that resemble human ones, and replay them to evade behaviour-based detection. Per the abstract, the GAN-driven bots evade detection even when the server knows the attack method. Only the abstract (Zenodo record) was read; no files were attached to the record, so detection rates were not checked.

## Contribution

Shows that behavioural-biometric bot detection based on trajectory shape can be defeated by generative models trained on human trajectories, including against a detector aware of the attack.

## Key results

- GAN-generated mouse and touch trajectories evade the authors' trajectory-image detector, including the attack-aware setting (abstract; numbers not read).

## Methods and models

Trajectories rendered as images; GAN trained on human trajectory images; generated trajectories executed by bots; evaluated against a CNN-style detector of trajectory images (from the companion detection work).

## Limitations and open questions

Not assessed beyond the abstract. Evaluation is against the authors' own detector; how it fares against commercial bot managers that combine many signals is not known from the abstract. The group's later work uses deep reinforcement learning for evasion (cited in [[sateur-2025-evaluating]]).

## Relevance to us

Concrete evidence for the arms-race assumption in swarm detection: any single behavioural channel that a generative model can learn will be imitated. For computer-use agents this applies directly to mouse and keystroke dynamics. Pair with [[iliou-2021-detection]] (the detector), CAPTCHA-breaking results [[plesner-2024-breaking]], [[zhang-2026-captchaarena]], and infrastructure-side signals in [[cloudflare-2025-from]].

## Search rounds added by shadow/sol-g51

Independently recovered the same abstract and verified the DOI through Crossref on 2026-10-03. An open author version is available at <https://eprints.bournemouth.ac.uk/36301/1/Web_bot_detection_evasion_using_Generative_Adversarial_Networks_R1_v1.pdf>. Only the abstract was read in this lane. A concurrent add/add was resolved by retaining sol-w5's entry rather than creating a duplicate or overwriting its prose.
