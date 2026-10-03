---
id: wolf-2013-accurate
type: paper
title: "Accurate decisions in an uncertain world: collective cognition increases true positives while decreasing false positives"
authors: ["Max Wolf", "Ralf H. J. M. Kurvers", "Ashley J. W. Ward", "Stefan Krause", "Jens Krause"]
year: 2013
venue: "Proceedings of the Royal Society B: Biological Sciences"
url: https://doi.org/10.1098/rspb.2012.2777
doi: "10.1098/rspb.2012.2777"
arxiv: null
cite: "Wolf, M., Kurvers, R. H. J. M., Ward, A. J. W., Krause, S., & Krause, J. (2013). Accurate decisions in an uncertain world: collective cognition increases true positives while decreasing false positives. Proceedings of the Royal Society B: Biological Sciences, 280(1756), 20122777. https://doi.org/10.1098/rspb.2012.2777"
topics: ["collective-decision", "swarm-intelligence"]
added_by: dmarz/collective-decision-audit
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "105 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Combines a signal-detection model with a human predator-detection experiment to show that groups can escape the individual trade-off between true and false positives. In the model, individuals who apply a simple quorum rule to the choices of other group members raise their hit rate and lower their false-alarm rate at the same time. In the experiment, people who saw others' choices did exactly this, the effect grew with group size, and they used a quorum threshold between the group's average true- and false-positive rates.

## Contribution

Gives the signal-detection framing of quorum decisions: where [[sumpter-2009-quorum]] and [[ward-2008-quorum]] show quorums improve accuracy in a binary choice, this paper shows they shift the whole ROC trade-off, which is the argument [[bose-2017-collective]] cites for treating collectives with individual decision theory.

## Key results

- Model: a quorum rule over others' binary detections increases true positives and decreases false positives simultaneously (analytical, per abstract).
- Experiment (humans, predator-detection task): after observing others, individuals increased true positives and decreased false positives; the effect strengthened with group size; the quorum threshold sat between the average true- and false-positive rates of others; individuals adjusted the quorum to group performance (per abstract).
- Abstract-level reading only; group sizes, rates and sample sizes were not checked because the publisher page and PMC full text were blocked from this machine.

## Methods and models

Signal-detection theory with independent individual detections pooled by a quorum threshold; human laboratory experiment framed as predator detection. Details not read.

## Limitations and open questions

Assumes independent individual errors; correlated errors (e.g. after social influence, see [[lorenz-2011-how]]) would weaken the benefit. The human task is a stand-in for animal predator detection, so transfer to animal groups is argued, not shown.

## Relevance to us

A ready-made metric pair (true- and false-positive rates against group size and quorum threshold) for any swarm detection experiment, including LLM-agent ensembles voting on a classification. Links to [[ward-2008-quorum]], [[ward-2011-fast]], [[krause-2010-swarm]] and [[sumpter-2009-quorum]].
