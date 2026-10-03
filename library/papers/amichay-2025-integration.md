---
id: amichay-2025-integration
type: paper
title: "On the integration of collective motion and temporal synchrony in animal collectives"
authors: ["Guy Amichay", "Máté Nagy"]
year: 2025
venue: "Movement Ecology"
url: https://pmc.ncbi.nlm.nih.gov/articles/PMC12220076/
doi: "10.1186/s40462-025-00573-2"
arxiv: null
cite: "Amichay, G., & Nagy, M. (2025). On the integration of collective motion and temporal synchrony in animal collectives. Movement Ecology, 13(1), 47."
topics: [collective-motion, sync-consensus]
added_by: dmarz/collective-motion-recent-audit
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "1 (OpenAlex W4411848511, 2026-10-03)"
code: []
---

## Summary

A review that puts spatial alignment (flocking, schooling, modelled by Vicsek) and temporal synchronisation (cricket chorusing, firefly flashing, frog calling, modelled by Kuramoto) in one frame. Both are phase-matching processes on a circle (heading angle versus oscillator phase), so the models share a mathematical core, but they differ in natural frequencies (present in Kuramoto, absent in Vicsek), in the role of noise (quenched frequency disorder versus annealed directional noise) and above all in mixing: in moving groups the interaction network reconfigures as individuals move, while many synchronising choruses have nearly fixed neighbourhoods. The authors organise the empirical and theoretical literature along a continuum from fixed topologies to highly mixing systems and point to swarmalators as the bridge.

## Contribution

A conceptual synthesis written for behavioural ecologists, from the group behind the zebrafish temporal-coupling work. Its specific claim is that mixing (rate of neighbour switching) is the main axis on which spatial and temporal collective order differ and should be studied comparatively.

## Key results

- Review, no new data. Claims: Vicsek and Kuramoto both reduce to matching of circular variables; the key differences are intrinsic frequencies, the type of disorder, and network mixing.
- Identifies 'temporal leadership' (who entrains whom in time) as essentially unexplored empirically, by analogy with directional leadership in informed-minority models.
- Open questions named: whether mixing helps or hurts coordination, how network temporality changes outcomes (e.g. more versus less mobile firefly swarms), and use of VR/AR/mixed reality for causal experiments.

## Methods and models

Narrative review. Fig. 1 sets out Kuramoto, swarmalator and Vicsek equations side by side and examples (alternating frog calls, starling velocity fluctuations, goldfish tailbeat phase coupling with robots, zebrafish burst coupling). Sections move from fixed neighbourhoods (experiments then theory, for each of temporal synchrony and collective motion) to dynamic neighbourhoods.

## Limitations and open questions

Read at skim depth (abstract, introduction, framework and outlook sentences). Conceptual: offers no quantitative test of the mixing hypothesis. Emphasis is on animal systems; robot and active-matter work on mobile oscillators is only touched on.

## Relevance to us

Gives us the vocabulary for coupling motion and timing in one simulator (heading plus an internal phase), which is what swarmalators do; the mixing rate is a natural control parameter for a hackathon experiment. Builds on [[amichay-2024-revealing]] (burst coupling in zebrafish pairs) and connects to [[de-lamo-2025-data]] (partial burst-and-coast synchrony) and the swarmalator line in sync-consensus. Same group: [[li-2025-reverse]], [[couzin-2025-collective]].
