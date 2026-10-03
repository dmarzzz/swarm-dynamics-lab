---
id: garland-2020-fighting
type: talk
title: Fighting Hate Speech with AI & Social Science (with Joshua Garland, Mirta Galesic,
  and Keyan Ghazi-Zahedi)
authors:
- Joshua Garland
- Mirta Galesic
- Keyan Ghazi-Zahedi
- Michael Garfield
year: 2020
url: https://dts.podtrac.com/redirect.mp3/cdn.simplecast.com/audio/812a29/812a2932-f271-4e9b-a23f-8d2d443a1682/c1c95f86-9029-4443-a97b-611349233bd9/38-fighting-hate-speech-with-ai-and-social-science_tc.mp3?aid=rss_feed&feed=OzDH_At2
venue: COMPLEXITY, 2020-07-15
topics:
- swarm-detection
- collective-decision
added_by: shadow/sol-aud
accessed: '2026-10-03'
read_depth: full
relevance: 5
---

## Summary

Joshua Garland, Mirta Galesic, and Keyan Ghazi-Zahedi discuss hate/counterspeech classification and organized response with host Michael Garfield. Read the complete approximately 66-minute Deepgram transcript. Some analyses belong to a paper still in draft, and the speakers explicitly distinguish association from causation.

- [08:12] Self-marked participation in Reconquista Germanica and insider account information for Reconquista Internet enable unusually large training sets. [20:15] The researchers study nearly 200,000 resolved reply trees on German news-outlet accounts rather than isolated utterances alone. Group-derived labels are a labeling strategy, not proof that every group's tweet is hateful or counterspeech.
- [23:21] The pipeline combines document embeddings and logistic regression, with diverse trained experts voting on hate, counter, or neutral categories. [31:14] Garland describes using high-confidence thresholds such as 93% and excluding ambiguous cases. [33:31] German-speaking crowdworkers are repeatedly screened; around 25 reliable coders provide human comparison, with stronger agreement for hate than counter classifications.
- [38:12] Organized counterspeech is associated with more counter tweets, slightly less hate, and changed reply dynamics. At [41:10], Galesic says the observational dataset cannot establish causal effects given simultaneous societal events. [47:35] Lower hate proportions coexist with indications of more polarized discourse, so effectiveness is explicitly multidimensional.
- [51:46] Choice models infer reply-attachment patterns favoring visibility, such as roots, recent posts, or heavily liked nodes, without access to campaign decision rooms. [55:53] Garland warns that an earlier hate-root/counter-leaf structural result changed with the algorithm and needs checking. [57:34] Randomizing display rules is proposed to frustrate gaming, not evaluated as a successful intervention here.

## Relevance to us

High-value source for campaign-level interaction analysis, weakly supervised labels, confidence filtering, and human validation. It makes the crucial point that organized coordination can serve counterspeech as well as abuse, and that a better-looking content statistic can hide worsening polarization. The classifiers target speech categories, not bots or LLM agents; do not turn the reported confidence threshold into detector accuracy or a claim of successful swarm attribution.
