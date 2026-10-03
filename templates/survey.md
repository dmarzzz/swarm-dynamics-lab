---
id: {{id}}
type: survey
title: TODO
owner: {{researcher}}
agents: [{{agent}}]
status: in-progress  # set to complete only when `python3 scripts/lab.py gate {{id}}` passes
started: {{date}}
topics: [TODO]
questions:
  - TODO the questions this survey must answer
seminal: []  # library ids of the foundational works; each must be cited below
search_log:
  # One row per search round, in the order you ran them. `results` = relevant hits you looked at,
  # `new` = how many of those were not already in library/. The last rounds must show saturation.
  # where: semantic-scholar google-scholar openalex dblp pubmed arxiv biorxiv openreview github
  #        papers-with-code huggingface x bluesky hn reddit lesswrong web youtube
  #        citations-backward citations-forward
  - {where: TODO, query: "TODO", date: {{date}}, results: 0, new: 0}
---

## Scope

TODO what is in and out of scope, and why.

## Search log

TODO narrative of the search: which seeds you started from, which citation trails you followed, what dead ends
you hit. The structured log lives in the frontmatter.

## Landscape

TODO the schools of thought, model families, or research communities, and how they relate. Cite every claim
as [[<id>]].

## What is known

TODO established results with citations. Separate what was measured from what was inferred.

## Open problems and disagreements

TODO where results conflict, what nobody has done, what the field argues about.

## Code, data and tools

TODO the usable implementations, simulators and datasets, with what state they are in.

## Gaps

TODO candidate openings for us. Gaps, not hypotheses: describe what is missing, not what we will claim.

## Saturation

TODO evidence the search is exhaustive: the last rounds returned almost nothing new, and the forward
citations of the seminal works are covered.
