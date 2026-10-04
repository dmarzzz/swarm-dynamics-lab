---
id: wulff-2025-timing
type: paper
title: "Timing of pre-retrieval warnings matters in reducing memory errors in a repeated testing misinformation study"
authors: [Alia N. Wulff, Jessica Karanian, Elizabeth Race, Ayanna K. Thomas]
year: 2025
venue: Scientific Reports
url: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=39762387&rettype=abstract&retmode=text
doi: 10.1038/s41598-024-84154-0
arxiv: null
cite: "Wulff, A. N., Karanian, J., Race, E., & Thomas, A. K. (2025). Timing of pre-retrieval warnings matters in reducing memory errors in a repeated testing misinformation study. Scientific Reports, 15(1), 963."
topics: [fork-merge-security]
added_by: dmarz/fm
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Read from the PubMed abstract; author names checked against Crossref. The study concerns retrieval-enhanced suggestibility (RES): the misinformation effect is larger when a person is tested on an event before being exposed to misleading post-event information, which the authors relate to reconsolidation triggered by the test. Participants saw an event; 24 hours later they either took a test or not, then read a narrative with misleading details. A general warning about the narrative's quality was then given, followed by the final test either immediately (Experiment 1) or after another 24 hours (Experiment 2). Warnings reduced RES when given soon after the misinformation but not when the warning and test were delayed 24 hours.

## Contribution

Locates a time window for defence: after retrieval-plus-misinformation, the original detail is still accessible for a while, and a warning inside that window helps; outside it, it does not.

## Key results

- Prior testing increases the misinformation effect (RES), as in earlier work (replicated).
- Immediate post-misinformation warning reduced RES (Experiment 1, measured).
- Warning delayed 24 hours did not reduce RES (Experiment 2, measured).

## Methods and models

Two behavioural experiments; event encoding, 24-hour delay, optional initial test, misleading narrative, general warning, final test at two delays.

## Limitations and open questions

Abstract depth; sample sizes and effect sizes not read. Only general warnings were tested.

## Relevance to us

For Q3 timing and for defence scheduling. RES says that an agent which has just recalled a memory (re-read it into context) is more vulnerable to misinformation about that memory, the behavioural counterpart of [[nader-2000-fear]] and [[hupbach-2007-reconsolidation]]. The warning-window result suggests that if a parent is going to check a merge, the check must happen at merge time while the pre-merge state is still recoverable; an audit a "day" later finds an already-integrated memory, consistent with the post-warning failures in [[loftus-2005-planting]]. For agents this is an argument for keeping the pre-merge snapshot until the audit runs, since unlike humans an agent can retain the original exactly.
