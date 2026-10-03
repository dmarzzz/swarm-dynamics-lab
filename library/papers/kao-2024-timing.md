---
id: kao-2024-timing
type: paper
title: "Timing decisions as the next frontier for collective intelligence"
authors: ["Albert B. Kao", "Shoubhik Chandan Banerjee", "Fritz A. Francisco", "Andrew M. Berdahl"]
year: 2024
venue: "Trends in Ecology & Evolution"
url: "https://arxiv.org/abs/2312.02187"
doi: "10.1016/j.tree.2024.06.003"
arxiv: "2312.02187"
cite: "Kao, A. B., Banerjee, S. C., Francisco, F. A., & Berdahl, A. M. (2024). Timing decisions as the next frontier for collective intelligence. Trends in Ecology & Evolution, 39(10), 904–912. https://doi.org/10.1016/j.tree.2024.06.003"
topics: ["collective-decision"]
added_by: dmarz/collective-decision-audit
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "18 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Opinion and review article arguing that collective-intelligence research has studied almost only spatial decisions (where to go: nest sites, food patches, directions) and neglected temporal decisions (when to act: departure, migration onset, flight from a predator). The authors lay out why timing decisions differ in kind and call for new models and experiments.

## Contribution

Names a gap in the field: none of the standard mechanisms (many-wrongs averaging, quorum, leadership, emergent sensing) has been tested on when-decisions. It sits alongside the reviews [[conradt-2005-consensus]] and [[couzin-2009-collective]] as an agenda piece, and builds on the consensus-cost models of [[conradt-2003-group]].

## Key results

- Conceptual, no new data. Key asymmetries argued: options in time are strictly ordered and only the present is available; past moments can be sampled but the future cannot (information asymmetry); animals usually signal readiness to go but have no signal for "not yet", and such signals are often binary.
- A signalling dilemma: if each individual signals only at its own optimal time, the group leaves late; if all signal early, the collective departure is biased early.
- Cites social effects on timing in birds, mammals and fish, but reports no prior work that tests collective intelligence on timing decisions (authors' claim).

## Methods and models

Literature synthesis with a conceptual figure contrasting spatial and temporal option sampling; points to optimal stopping, marginal value theorem and drift-diffusion models as starting theory. I read the arXiv version (2312.02187); the published version may differ in wording.

## Limitations and open questions

No formal model is proposed. Whether known mechanisms (quorum thresholds, which are inherently temporal, as in [[pratt-2006-tunable]]) already cover parts of the problem is not fully engaged.

## Relevance to us

A ready hypothesis space for a hackathon: build a when-to-go swarm task (agents with noisy private optimal times, binary readiness signals, quorum departure) and test whether the group beats individuals. Related: [[sumpter-2009-quorum]], [[ward-2011-fast]], [[berdahl-2013-emergent]], [[bate-2026-indecision]].
