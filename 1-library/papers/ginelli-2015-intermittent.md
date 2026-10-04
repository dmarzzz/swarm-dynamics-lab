---
id: ginelli-2015-intermittent
type: paper
title: Intermittent collective dynamics emerge from conflicting imperatives in sheep herds
authors: [Francesco Ginelli, Fernando Peruani, Marie-Helène Pillot, Hugues Chaté, Guy Theraulaz, Richard Bon]
year: 2015
venue: Proceedings of the National Academy of Sciences
url: https://europepmc.org/article/MED/26417082
doi: 10.1073/pnas.1503749112
arxiv: null
cite: 'Ginelli, F., Peruani, F., Pillot, M.-H., Chaté, H., Theraulaz, G., & Bon, R. (2015). Intermittent collective dynamics emerge from conflicting imperatives in sheep herds. Proceedings of the National Academy of Sciences, 112(41), 12729–12734.'
topics: [collective-motion, criticality-measurement, collective-decision]
added_by: dmarz/collective-motion-audit
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "216 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Controlled field experiments with large groups of grazing Merino sheep show strongly intermittent
collective dynamics: slow dispersion while grazing, punctuated by fast, avalanche-like regrouping events
whose sizes span all experimentally accessible scales. An agent-based model with individual behavioural shifts, whose rates
depend on neighbours (allelomimetic, i.e. copying, responses), reproduces all observed collective
properties. The strength of allelomimetic behaviour controls a
trade-off between per-capita grazing area and time to regroup into a tight herd. Read at abstract level
(Europe PMC record; full text unreachable from this machine).

## Contribution

A rare quantitative study of collective motion in a large terrestrial mammal, and a clear example of
intermittent, state-switching collective dynamics rather than the steady flocking of Vicsek-type models.
The authors frame it as balancing exploration (foraging) against protection (cohesion), and relate it to
the debate on criticality in biology ([[romanczuk-2022-phase]]).

## Key results

- Measured: intermittent dynamics; fast regrouping events distributed over all accessible scales
  ("avalanche-like").
- Model: individual behavioural shifts driven by allelomimetic response functions reproduce the
  collective statistics (claimed in abstract; parameter values not read).
- Allelomimetic intensity sets the trade-off between grazing surface per capita and regrouping time.
- Specific group sizes, exponents and timescales are in the paper but were not read here.

## Methods and models

Experiments with groups of Merino sheep under controlled conditions in a field; tracking of individual
positions; agent-based model with individual behavioural shifts and stimulus/response functions (from abstract;
states and parameters not read).

## Limitations and open questions

- Abstract-level entry: the claim of scale-free event sizes and how it was tested are unverified here.
- Single breed and site; the role of the herding context and predators is argued, not manipulated.

## Relevance to us

A model for swarms that alternate exploration and regrouping, a pattern useful for search-and-cluster tasks
in robot or agent swarms. The allelomimetic switching rule is a simple mechanism to borrow. Related:
[[jadhav-2024-collective]] (sheep and herding dog), [[couzin-2005-effective]], [[gomez-nava-2023-fish]]
(excitable dynamics in fish).
