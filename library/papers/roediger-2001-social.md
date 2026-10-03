---
id: roediger-2001-social
type: paper
title: "Social contagion of memory"
authors: [Henry L. Roediger III, Michelle L. Meade, Erik T. Bergman]
year: 2001
venue: Psychonomic Bulletin & Review
url: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=11495127&rettype=abstract&retmode=text
doi: 10.3758/BF03196174
arxiv: null
cite: "Roediger, H. L., III, Meade, M. L., & Bergman, E. T. (2001). Social contagion of memory. Psychonomic Bulletin & Review, 8(2), 365–371."
topics: [fork-merge-security, collective-decision]
added_by: dmarz/fm
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: 285  # Crossref is-referenced-by-count, 2026-10-03
code: []
---

## Summary

Read from the PubMed abstract (Springer blocked the PDF). The paper introduces the social contagion of memory paradigm. A subject and a confederate viewed six household scenes together for either 15 or 60 seconds, then took turns recalling items in a collaborative test. The confederate sometimes reported items that were not in the scene, some highly schema-consistent (a toaster in a kitchen) and some less so (oven mitts). After a short delay the subject recalled the scenes alone. Subjects recalled the confederate's false items more often than in a no-suggestion control, and the effect was larger with 15-second viewing and with schema-consistent intrusions.

## Contribution

Establishes a laboratory paradigm in which one person's memory errors are transmitted to another through ordinary collaborative recall, the person-to-person form of the misinformation effect.

## Key results

- False recall of confederate-suggested items exceeded the no-suggestion control (measured; numbers not given in the abstract).
- Larger effect when original encoding was weaker (15 s versus 60 s exposure).
- Larger effect when the false item fit the scene schema.

## Methods and models

Subject-confederate pairs; six scenes; 2 exposure durations; collaborative recall with planted intrusions; individual recall test.

## Limitations and open questions

Abstract depth; effect sizes not checked. Confederates are scripted, so the paradigm measures how much a recipient absorbs, not how errors spread in a network.

## Relevance to us

This is the merge step of Q3 measured in humans: two agents who saw the same scene "merge" by recalling together, and the one who saw less (shorter exposure) takes on the other's planted items, especially plausible ones. Translated to a fork-merge agent, the parent is the weak encoder for whatever a child explored alone (the parent never saw that domain), so the parent is in the high-susceptibility condition by construction, and a corrupted child's most effective plants are schema-consistent ones that fit what the parent expects of that domain. This also bears on Q2: an independent second child that explored the same domain is the only stand-in for the original scene. Follow-ups: [[meade-2002-explorations]] (warnings and source tests do not remove the effect), [[numbers-2014-influences]] (partner accuracy is ignored). LLM analogue: [[de-marzo-2026-conformity]]. Mechanism: [[johnson-1993-source]].
