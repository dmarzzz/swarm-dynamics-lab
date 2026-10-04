---
id: zatuchin-2026-system
type: paper
title: 'System Attribution in LLM Brand Recommendations: Single Responses Identify
  the System, Aggregated Brand Profiles Do Not Transfer'
authors:
- Dmitrij Żatuchin
year: 2026
venue: arXiv
url: https://export.arxiv.org/api/query?id_list=2610.00253
doi: null
arxiv: '2610.00253'
cite: 'Dmitrij Żatuchin. (2026). System Attribution in LLM Brand Recommendations:
  Single Responses Identify the System, Aggregated Brand Profiles Do Not Transfer.
  arXiv:2610.00253.'
topics:
- swarm-detection
added_by: shadow/sol-g51
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

This study distinguishes individual-response attribution from aggregated brand behavior across deployed LLM endpoints. Character n-grams strongly identify systems in the tested corpus, but aggregated brand profiles fail transfer and changes to a retrieval harness break attribution for one endpoint.

## Contribution

Shows single LLM responses identify the deployed system with 97.84% accuracy from character n-grams, while aggregated brand profiles fail to transfer across domains and harness changes.

## Key results

- 6,475 stored responses, 6,324 analysable; individual attribution 97.84%; altered retrieval arm attributes zero of 120 Grok responses to Grok; aggregated cross-domain forest misclassifies all 22 gift units.

## Methods and models

Prompt-grouped cross-validation, surface-form classifiers, and cross-domain/profile comparisons.

## Limitations and open questions

The uncrossed design cannot separate system, domain, and harness effects; high corpus accuracy does not demonstrate open-world operator attribution.

## Relevance to us

Relevant to operator and model attribution in swarm detection: per-message system fingerprinting works in a closed set, but harness changes broke it (0 of 120 Grok answers attributed), so attribution claims need cross-harness tests.

## Access provenance

Opened the HTTPS arXiv export record and read its abstract on 2026-10-03. No citation count inferred from an absent or mismatched index record.
