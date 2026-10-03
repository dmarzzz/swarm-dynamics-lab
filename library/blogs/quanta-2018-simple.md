---
id: quanta-2018-simple
type: blog
title: "The Simple Algorithm That Ants Use to Build Bridges"
authors: [Kevin Hartnett]
year: 2018
url: https://www.quantamagazine.org/the-simple-algorithm-that-ants-use-to-build-bridges-20180226/
site: quantamagazine.org
topics: [collective-decision, swarm-robotics, swarm-intelligence]
added_by: shadow/sol-w3
accessed: 2026-10-03
read_depth: full
relevance: 2
---

## Summary

Short Quanta "Abstractions blog" piece (26 Feb 2018) on Simon Garnier's (NJIT Swarm Lab) work on army-ant bridge building, based on a 2017 study linked from the article (PubMed 28939347) and fieldwork in Panama in 2014. Two local rules explain the behaviour: an ant that slows at a gap and feels others walking over its back freezes, so successive ants stack into a bridge; and a frozen ant leaves the bridge when traffic over it drops below a threshold. The second rule makes the colony trade shortcut length against the number of ants locked into structures without any ant knowing the total. Reported numbers: colony marching at about 12 cm/s; 40 to 50 bridges maintained at once, 1 to 50 ants each; up to 20 percent of the colony locked in bridges (from a 2015 PNAS paper by the same group). The model predicts, from gap geometry, when the colony bridges versus goes around. The article closes with Melvin Gauci (Harvard) cautioning that ants may be less simple than two rules.

## Key claims

- Bridge formation needs only a traffic-triggered freeze rule; bridge size is regulated by a traffic threshold for unfreezing.
- Colonies do not build the distance-minimising bridge because locked ants are a cost; the threshold implicitly encodes that cost-benefit trade-off (Garnier's interpretation).
- Up to 20 percent of a colony can be in bridges at once (measured in the 2015 study, as reported).
- Swarm robotics has not matched this; robot reliability and battery life are named obstacles (opinion of interviewees).

## Evidence quality

Science journalism summarising two peer-reviewed field studies (2015 PNAS, 2017 model paper); numbers are reported second-hand and the underlying papers are not catalogued here. The "two simple rules" framing is the journalist's and Garnier's simplification, explicitly hedged by Gauci.

## Relevance to us

A clean example of a collective cost-benefit decision computed by a local threshold on a shared signal (traffic), with no global counter. That is the same shape as resource allocation in agent swarms where no agent sees how many peers are committed. Related biology: [[garnier-2007-biological]], [[sumpter-2009-quorum]]. The Gauci caveat applies to any "simple rules" claim about LLM agents too. Robot counterpart: [[rubenstein-2014-programmable]].
