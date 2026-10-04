---
id: zaslavsky-2023-noga
type: talk
title: "Noga Zaslavsky: Information-constrained Emergent Communication in Multi agent Systems"
authors: [Noga Zaslavsky]
year: 2023
url: https://www.youtube.com/watch?v=rnUZJYktZGE
venue: "Israel Institute for Advanced Studies, 33rd Advanced School in Economic Theory, Day 6 Session 2; uploaded 2023-07-04"
topics: [marl-emergence, collective-decision]
added_by: shadow/sol-aud
accessed: 2026-10-03
read_depth: full
relevance: 5
---

## Summary

Noga Zaslavsky presents an information-constrained account of emergent lexicons, connecting cognitive-science evidence with multi-agent utility optimization. Recovered a previously blocked inbox source through the caption helper's Apify fallback, then read all 1,931 timestamped caption segments through the closing applause, approximately 86 minutes. Opened the YouTube landing page through Jina for title, institute, and upload date. This is a full-transcript read, not inspection of the slides; automatic captions garble technical terms and do not expose numerical plot values reliably.

- [00:22] She asks how a shared lexicon emerges rather than assuming one. Task-specific utility optimization and task-agnostic information constraints have complementary shortcomings. [25:29] The information-bottleneck account trades lexicon complexity against reconstruction accuracy; broad cross-language color-naming comparisons use shared perceptual representations and a simplified shared prior, with a fitted tradeoff parameter rather than independent prediction of each language's parameter.
- [41:18] She compares color naming in one Ghanaian language in 1978 and 2018. Both systems remain close to the modeled efficiency bound, whereas [46:15] 50 hypothetical random-drift trajectories diverge. This is evidence against that particular null process, not proof that efficiency is the only evolutionary pressure; she explicitly denies exclusivity at [47:15].
- [59:19] The integrated multi-agent objective distinguishes downstream task utility, communication complexity, and representational distortion. [63:51] Vector-quantized variational information bottleneck combines discrete, stochastically encoded communication with a continuous learned embedding space. Speaker and listener networks learn a codebook, reconstruction, and actions; [66:28] a navigation example separates accurate transmission of a target representation from successful physical movement to it.
- [70:49] A natural-object naming dataset contains about 25,000 images across seven high-level domains. Held-out-domain tests [72:01] support an accuracy-weighted objective's transfer benefits, and [73:17] learned embedding clusters are illustrated without using their displayed English labels as training labels. Precise effect sizes and baseline names are not recoverable confidently from these captions. [76:52] Predicting the tradeoff parameter before fitting remains future work.

## Relevance to us

A direct multi-agent communication design reference: rewarding immediate task success alone can produce brittle protocols, while additional pressure to preserve shared representations can support transfer. Useful for distinguishing message compression, representational agreement, and downstream action outcomes in swarm evaluation. It studies cooperative communication and semantic grounding, not adversarial messages, forked-memory reintegration, or Byzantine safety. It does not establish that human-like semantics guarantee interpretable or safe LLM-agent swarms.
