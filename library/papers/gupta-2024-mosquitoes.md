---
id: gupta-2024-mosquitoes
type: paper
title: "Mosquitoes integrate visual and acoustic cues to mediate conspecific interactions in swarms"
authors: ["Saumya Gupta", "Antoine Cribellier", "Serge B. Poda", "Olivier Roux", "Florian T. Muijres", "Jeffrey A. Riffell"]
year: 2024
venue: "Current Biology"
url: https://pmc.ncbi.nlm.nih.gov/articles/PMC11491102/
doi: "10.1016/j.cub.2024.07.043"
arxiv: null
cite: "Gupta, S., Cribellier, A., Poda, S. B., Roux, O., Muijres, F. T., & Riffell, J. A. (2024). Mosquitoes integrate visual and acoustic cues to mediate conspecific interactions in swarms. Current Biology, 34(18), 4091–4103.e4."
topics: [collective-motion]
added_by: dmarz/collective-motion-recent-audit
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "16 (OpenAlex W4402043566, 2026-10-03)"
code: []
---

## Summary

Asks how swarming Anopheles coluzzii males track females while avoiding collisions with other males, given that males hear female flight tones but are poor at hearing each other. Tethered-flight virtual reality experiments show mosquitoes steer in response to small visual objects that mimic nearby conspecifics; without sound they tend to turn away (avoidance), while a female flight tone gates the response so males steer toward the object (attraction). Visual cues alone change wingbeat amplitude and frequency. Free-flight swarm data show similar thrust-based responses to nearby conspecifics, consistent with visually mediated collision avoidance.

## Contribution

Establishes multisensory (visual plus acoustic) gating of conspecific interactions in an insect swarm, overturning the assumption that Anopheles rely almost only on hearing. Gives a sensory mechanism for the short-range repulsion rule used in swarm models.

## Key results

- Measured (tethered): steering toward visual objects strongly increased in males when paired with female flight tones; acoustic cues gate visual responses.
- Measured (tethered): visual stimuli alone altered wingbeat amplitude and frequency in both sexes.
- Measured (free flight): flight kinematics modulated near conspecifics in a way matching tethered responses (thrust changes), interpreted as collision avoidance.
- Visual panel pixel subtends 3.75 degrees, equivalent to a mosquito about 15 body lengths away.

## Methods and models

Tethered flight simulator with LED panels showing starfield patterns derived from real swarm images and moving objects, with or without playback of male/female flight tones; wingbeat analysis. Free-flight swarm recordings of lab-reared An. coluzzii with 3D tracking (Muijres lab). Preprint posted on bioRxiv May 2024.

## Limitations and open questions

Tethered animals may not behave like free fliers; free-flight evidence is correlational. Interaction range of vision in dim dusk light is limited. Read at skim depth (summary, introduction, key results).

## Relevance to us

Gives empirical grounding to a perception-gated interaction rule (repel by default, attract when a mate cue is present), a pattern that could be implemented as a context-switching rule in agent models. Companion to [[cribellier-2026-complex]]; perception-based interaction in vertebrates: [[zheng-2024-body]], [[xiao-2024-perception]], [[krongauz-2024-vision]].
