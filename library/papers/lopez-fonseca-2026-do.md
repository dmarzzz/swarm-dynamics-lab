---
id: lopez-fonseca-2026-do
type: paper
title: "Do Generative AI Assistants Respect robots.txt? Tracing Web Access Beyond Visible Answers"
authors: ["Gabriel Lopez-Fonseca", "David Rodriguez", "Stefan Bechtold", "Jose M. Del Alamo"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2607.14447
doi: "10.48550/arXiv.2607.14447"
arxiv: "2607.14447"
cite: "Lopez-Fonseca, G., Rodriguez, D., Bechtold, S., & Del Alamo, J. M. (2026). Do Generative AI Assistants Respect robots.txt? Tracing Web Access Beyond Visible Answers. arXiv preprint arXiv:2607.14447."
topics: ["swarm-detection"]
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: "1 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Lopez-Fonseca, Rodriguez, Bechtold and Del Alamo test ten AI assistants with web search under four robots.txt conditions (allow all, disallow all, allow only the assistant's UA, disallow only it) over 200 trials, using server logs and secret codes embedded in pages to separate actual page access from answer correctness. Compliance varies widely: some follow the rules, others fetch disallowed pages without requesting robots.txt or use generic User-Agents that make attribution hard. Access and visible answers also diverge in both directions.

## Contribution

Controlled per-assistant robots.txt compliance test that uses embedded secrets, a light canary method, to verify access independent of the answer.

## Key results

- Measured (abstract): 10 assistants, 4 conditions, 200 trials.
- Measured (abstract): some assistants accessed restricted resources without requesting robots.txt; some used generic User-Agents.
- Measured (abstract): assistants sometimes accessed pages without surfacing content, or failed to access allowed pages.

## Methods and models

Controlled websites, server-side logs, secret codes in pages, four robots.txt conditions. Abstract only.

## Limitations and open questions

Abstract only; per-assistant results not checked.

## Relevance to us

Confirms with ground truth that user-triggered AI fetchers often hide behind generic browser identities, which is why identity must come from fingerprints or canaries ([[seiden-2026-identifying]]).
