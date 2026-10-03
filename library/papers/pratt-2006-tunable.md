---
id: pratt-2006-tunable
type: paper
title: "A tunable algorithm for collective decision-making"
authors: ["Stephen C. Pratt", "David J. T. Sumpter"]
year: 2006
venue: "Proceedings of the National Academy of Sciences"
url: https://doi.org/10.1073/pnas.0604801103
doi: "10.1073/pnas.0604801103"
arxiv: null
cite: "Pratt, S. C., & Sumpter, D. J. T. (2006). A tunable algorithm for collective decision-making. Proceedings of the National Academy of Sciences, 103(43), 15906–15910. https://doi.org/10.1073/pnas.0604801103"
topics: ["collective-decision"]
added_by: dmarz/collective-decision
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "159 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Emigrating Temnothorax curvispinosus colonies use one decision algorithm, a stepwise commitment scheme with a quorum rule, but tune its parameters (search and acceptance rates of candidate nests) to emphasise speed when their old nest is destroyed and accuracy when it is intact. The authors propose general but tunable algorithms as a design feature of complex systems.

## Contribution

Shows algorithmic versatility rather than a fixed rule; the data were re-analysed in [[sumpter-2009-quorum]] to show steeper quorums under low urgency.

## Key results

- Colonies emigrate faster but less accurately under high urgency by raising acceptance and search rates (experiment plus agent-based model).
- Abstract-level reading only; numbers beyond the abstract were not checked.

## Methods and models

Laboratory emigrations with intact versus destroyed home nests and good versus mediocre candidates; agent-based model from Pratt et al. (2005).

## Limitations and open questions

One species; parameter changes inferred via model fitting.

## Relevance to us

Template for a swarm controller with an urgency parameter. Related: [[franks-2003-speed]], [[sasaki-2018-psychology]].
