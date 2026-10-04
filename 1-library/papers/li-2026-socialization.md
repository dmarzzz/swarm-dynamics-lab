---
id: li-2026-socialization
type: paper
title: Does Socialization Emerge in AI Agent Society? A Case Study of Moltbook
authors:
- Ming Li
- Xirui Li
- Tianyi Zhou
year: 2026
venue: arXiv
url: https://export.arxiv.org/api/query?id_list=2602.14299
doi: null
arxiv: '2602.14299'
cite: Ming Li; Xirui Li; Tianyi Zhou. (2026). Does Socialization Emerge in AI Agent
  Society? A Case Study of Moltbook. arXiv:2602.14299.
topics:
- llm-agent-swarms
added_by: shadow/sol-g51
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

This Moltbook study diagnoses semantic stability, lexical turnover, individual inertia, influence persistence, and consensus. The abstract reports rapidly stable global semantics alongside diverse individuals, persistent turnover, weak adaptation to partners, transient influence, and no stable collective consensus.

## Contribution

Diagnoses whether socialization emerges on Moltbook through semantic stability, lexical turnover, individual inertia, influence persistence and consensus measures.

## Key results

- Global averages stabilize but agents show high inertia and minimal adaptive partner response; no numerical effect size is reported in the abstract.

## Methods and models

Dynamic semantic and lexical diagnostics of a persistent agent social platform.

## Limitations and open questions

Observed interaction density does not imply socialization; causal roles of prompts, models, or memory are not isolated in the abstract.

## Relevance to us

A negative result worth citing: a large agent society showed stable global averages but little partner adaptation and no stable consensus, which tempers claims of emergent collective behavior.

## Access provenance

Opened the HTTPS arXiv export record and read its abstract on 2026-10-03. No citation count inferred from an absent or mismatched index record.

## Notes from shadow/sol-1

Read on 2026-10-03 from arXiv HTML (https://arxiv.org/html/2602.14299): sections 1 to 6 and appendix A to B. Depth for this note: skim of methods and results.

- Data: full Moltbook interaction history from launch to 8 Feb 2026 after removing posts repeated more than 1,000 times: 290,251 posts, 1,836,711 comments, 38,830 unique post authors. Embeddings: Sentence-BERT all-MiniLM-L6-v2; n-grams via nltk.
- Society level: daily semantic centroids converge quickly (centroid cosine near 1) while pairwise post similarity stays low; n-gram birth and death rates settle to non-zero baselines (persistent lexical turnover); kNN neighbourhood density stops tightening after about 3 days.
- Agent level (agents with >= 10 posts): drift magnitude is modest and falls with activity; drift directions are near-orthogonal to the mean drift; movement toward the global centroid is centred at zero. Feedback (top vs bottom 30% by votes) does not pull later posts. Interaction influence (semantic and n-gram similarity to a commented post, after vs before) is centred at zero and indistinguishable from a same-day random-post baseline.
- Collective level: daily PageRank supernodes turn over rapidly; probing agents about influential users yields fragmented, often hallucinated references.
- Caveat: observational, embeddings measure topic similarity, and Moltbook agents are heterogeneous, mostly short-context posters, so "no influence" may reflect what agents are shown and remember rather than an inability to be influenced.

Counter-evidence to generalising "in the wild agents copy what they see" from [[de-marzo-2026-copying]]: on Moltbook, commenting on a post produces no measurable semantic or n-gram convergence toward it.
