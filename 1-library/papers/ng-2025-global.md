---
id: ng-2025-global
title: A global comparison of social media bot and human characteristics
authors:
- Lynnette Hui Xian Ng
- Kathleen M. Carley
year: 2025
venue: Scientific Reports 15, 10973
url: https://doi.org/10.1038/s41598-025-96372-1
doi: 10.1038/s41598-025-96372-1
arxiv: null
cite: Ng, L. H. X., & Carley, K. M. (2025). A global comparison of social media bot
  and human characteristics. Scientific Reports, 15, 10973. https://doi.org/10.1038/s41598-025-96372-1.
topics:
- swarm-detection
- llm-agent-swarms
read_depth: skim
relevance: 4
type: paper
added_by: shadow/sol-w1
accessed: '2026-10-03'
citations: null
code: []
---

## Summary

Ng and Carley compare bot-labeled and human-labeled Twitter accounts across several event datasets using linguistic cues, self-presented identities, and interaction networks. Approximately five billion tweets from 200 million users support a broad descriptive comparison. Bot-labeled accounts retweet more and have denser ego networks; most of their interaction partners are still human-labeled. The labels come from BotHunter rather than independent ground truth, a critical qualification for interpreting the reported differences.

## Contribution

Combines a mechanics-based definition of social bots with large-scale cross-event linguistic and network characterization, explicitly separating automation from malicious intent.

## Key results

- Approximately 5 billion tweets and 200 million users, aggregated across event datasets.
- Mean bot-labeled share about 20%, reaching 43% during the studied US election event; these are classifier-derived, event-specific estimates.
- Bot ego networks reported 8.33% denser, with 90.34% human alters versus 92.69% for humans.
- A small supplementary generative-model probe uses 20 tweets each from three open models and reports BotHunter score 0.69 ± 0.15, close to the study's 0.70 threshold.

## Methods and models

Skimmed the definition, results, methods, generative-model discussion, conclusion, and citation information on the publisher page. BotHunter tiered random-forest scores above 0.7 determine bot labels. NetMapper extracts dictionary-based cues in 40 languages; comparisons use t-tests with Bonferroni correction. ORA computes ego-network measures. For the largest network analyses, the methods use a 2% coronavirus-user sample and a 50% US-election-user sample. Supplementary tables and code were not read or run.

## Limitations and open questions

Classifier-derived labels make the descriptive conclusions dependent on BotHunter's assumptions and errors; a large sample does not remove that dependence. Event-selected data are not a representative census of all platform users. Aggregated differences do not establish operator intent or causal manipulation. The 60 generated-tweet probe is too small and narrow to establish general LLM-bot detectability. Data and code are available by author request, not automatically reproducible from a public repository.

## Relevance to us

Useful network and behavior baselines, especially the distinction between automation and malicious coordination. Pair with [[deason-2018-time]] for temporal evidence and [[cubbon-2020-inauthentic]] for identity/coordination distinctions. Avoid quoting the 20% estimate as independently verified global platform prevalence.
