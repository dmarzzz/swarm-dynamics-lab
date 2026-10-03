---
id: mannocci-2026-detection
type: paper
title: 'Detection and Characterization of Coordinated Online Behavior: A Survey'
authors:
- Lorenzo Mannocci
- Michele Mazza
- Anna Monreale
- Maurizio Tesconi
- Stefano Cresci
year: 2026
venue: ACM Computing Surveys
url: https://arxiv.org/html/2408.01257
doi: 10.1145/3839225
arxiv: '2408.01257'
cite: 'Mannocci, L., Mazza, M., Monreale, A., Tesconi, M., & Cresci, S. (2026). Detection and Characterization of Coordinated Online Behavior: A Survey. ACM Computing Surveys, 58(16), 1–38. https://doi.org/10.1145/3839225'
topics:
- swarm-detection
- meta
added_by: dmarz/sd-coordination
accessed: 2026-10-03
read_depth: skim
relevance: 5
citations: 23 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Systematic review of the coordinated-online-behaviour literature. A Scopus plus Google Scholar search (2014 to 2026) gave 1,206 records; 83 survived screening and a backward reference search added 42, for a corpus of 125 papers. The authors reconcile platform definitions (Meta, X, YouTube, Reddit, TikTok) with academic ones, define coordination by actors, actions and intent, and characterise it along four dimensions: authenticity, harmfulness, orchestration and time-variance. They then split methods into detection (mostly network-science pipelines: user selection, coordination-network construction, filtering, community discovery; plus unsupervised and supervised ML) and characterization (indicators per dimension).

## Contribution

The reference review for this subtopic as of 2026. It gives a common vocabulary and a four-step pipeline into which almost every detector in the field fits, and it lists the open problems that matter for detecting agent swarms: no statistically grounded null model, sensitivity to time-window choices, scarce ground truth, and generative AI.

## Key results

- Corpus: 125 papers after PRISMA screening (1,206 screened). Most study a single platform, mainly Twitter/X; only about ten are multi- or cross-platform.
- Network filtering is done by fixed similarity thresholds in the large majority of works; the survey notes thresholds are "typically selected arbitrarily, without a strong underlying theoretical motivation". A minority use statistically validated edges or k-nearest-neighbour graphs.
- Few works build multiplex networks without flattening them before community detection; compound co-actions are "almost completely unexplored".
- Validation is mostly post-hoc characterization; ground truth comes from platform takedown archives (X transparency releases); simulation-based validation is rare, with one LLM-agent simulation cited ([[orlando-2026-emergent]]).
- "Authentic spontaneous and harmless coordinated behavior is completely unstudied", so detectors have no characterised negative class.
- On generative AI the authors state that its effect on coordination detection is "still unknown" (their wording, not a measurement).

## Methods and models

Literature review with a PRISMA flow. Taxonomy of co-actions (co-retweet, co-URL, co-hashtag, co-image, synchronized posting), time-window types (adjacent, sliding, fixed sizes from minutes to days), similarity measures (cosine on TF-IDF, Jaccard), filters and community algorithms, tabulated per paper. I read the method sections on network filtering, ML methods, validation and open challenges, not every table.

## Limitations and open questions

Scope is social media coordination; algorithmic collusion in markets, physical swarms and LLM-agent collusion inside multi-agent systems are out of scope. The open challenges section (null models, temporal parameters, cross-platform identity, attribution) is a list of research directions, not results.

## Relevance to us

Start here for this subtopic. The pipeline it describes is what [[pacheco-2021-uncovering]] introduced, [[luceri-2024-unmasking]] refined and [[mukherjee-2026-moltgraph]] applied to an agent-only platform. The lack of null models is the opening for a hackathon contribution: a statistically grounded test for "these N agents are one swarm". Companion code: the authors' interactive website (not catalogued here).

## Notes from dmarz/sd-bots

Folded in by dmarz/sd-merge from the duplicate entry `mannocci-2024-detection` (added_by dmarz/sd-bots, accessed 2026-10-03, read_depth abstract, relevance 5). Same source (same arXiv id and DOI); the kept id uses the year of the published version given in cite.

- Frontmatter `year` in the folded entry: 2024
- Frontmatter `url` in the folded entry: https://arxiv.org/abs/2408.01257
- Frontmatter `cite` in the folded entry: 'Mannocci, L., Mazza, M., Monreale, A., Tesconi, M., & Cresci, S. (2026). Detection and Characterization of Coordinated Online Behavior: A Survey. ACM Computing Surveys, 58(16), Article 401, 1-38. https://doi.org/10.1145/3839225 (preprint arXiv:2408.01257, 2024).'
- Frontmatter `read_depth` in the folded entry: abstract
- Frontmatter `citations` in the folded entry: 1 (Crossref, 2026-10-03)

### Summary

A survey of coordinated online behaviour research that reconciles industry terms such as Meta's 'coordinated inauthentic behavior' with academic definitions, proposes a framework of actors, actions and intent, and reviews detection and characterisation methods. It argues coordination should be described along authenticity, harmfulness, orchestration and time-variance, and lists open challenges; an interactive companion site indexes the surveyed papers.

### Contribution

The current reference survey for coordination detection, the method family most likely to catch LLM swarms whose per-account content looks human.

### Key results

- Framework: coordinated behaviour as actors, actions and intent (abstract and search snippet).
- Four dimensions: authenticity, harmfulness, orchestration, time-variance.
- Reviews detection methods, mostly similarity networks over shared actions (co-retweet, co-URL, co-hashtag, synchronous timing).

### Methods and models

Systematic survey. Abstract-level read; companion website not opened.

### Limitations and open questions

Covers human and bot coordination together; does not focus on LLM agents. Published version 2026, preprint 2024.

### Relevance to us

Entry point for the coordination branch of swarm detection. Methods it surveys include [[pacheco-2021-uncovering]] and [[luceri-2024-unmasking]]; tested on video in [[luceri-2026-coordinated]].
