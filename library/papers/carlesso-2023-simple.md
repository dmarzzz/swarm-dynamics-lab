---
id: carlesso-2023-simple
type: paper
title: "A simple mechanism for collective decision-making in the absence of payoff information"
authors: ["Daniele Carlesso", "Justin M. McNab", "Christopher J. Lustri", "Simon Garnier", "Chris R. Reid"]
year: 2023
venue: "Proceedings of the National Academy of Sciences"
url: "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10629567/fullTextXML"
doi: "10.1073/pnas.2216217120"
arxiv: null
cite: "Carlesso, D., McNab, J. M., Lustri, C. J., Garnier, S., & Reid, C. R. (2023). A simple mechanism for collective decision-making in the absence of payoff information. Proceedings of the National Academy of Sciences, 120(29), e2216217120. https://doi.org/10.1073/pnas.2216217120"
topics: ["collective-decision", "swarm-intelligence", "swarm-robotics"]
added_by: dmarz/collective-decision-audit
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "15 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Weaver ants (Oecophylla smaragdina) build hanging chains of their own bodies to bridge vertical gaps, but they cannot know whether the far side is worth reaching until the chain is complete. The authors show colonies cap their investment and do not complete chains over gaps taller than 90 mm. Individual ants join at the chain tip and stay longer the closer the tip is to the ground, and a distance-based joining and leaving model reproduces the colony-level cap without assuming complex cognition.

## Contribution

A collective decision under payoff uncertainty that is solved by a local stopping rule rather than by quality assessment and recruitment, unlike nest-site and foraging choices such as [[seeley-2012-stop]] or [[pratt-2006-tunable]]. It adds self-assembly to the collective-decision catalogue.

## Key results

- Chains formed over gaps of 25, 35 and 50 mm (5 analysed trials each, chosen from 10); colonies did not complete chains for gaps above 90 mm.
- 92 per cent of 96 tracked joiners attached within the bottom 10 mm of the chain (mean 1.83 mm from the tip); 43 per cent extended past the tip.
- 88 per cent of 41 tracked leaving events were from the bottom 10 mm; residence times ranged from 3.3 to 117.8 s (mean 23.2 s, SD 26.3).
- Ants showed more "reaching" toward the platform when it was closer (GLMM, N = 327, z = -2.626, P < 0.01); residence time depended on distance to the ground (Cox model).

## Methods and models

Laboratory apparatus with a raised trail and a platform with food at a set height below; video at 24 fps, manual tracking in Fiji; mixed-effects and survival (Cox) models; a theoretical chain-formation model with distance-dependent joining and leaving rates. I skimmed the significance statement, introduction and first results sections, not the model derivation.

## Limitations and open questions

Laboratory colonies, a narrow range of gap sizes, and a cap inferred from failures at larger gaps. Whether the rule is adaptive across natural payoff distributions is argued, not tested.

## Relevance to us

A distributed stopping rule that bounds group investment without payoff information, directly portable to swarm robots that self-assemble or to agent swarms deciding how many workers to commit to an unknown task. Related: [[sumpter-2009-quorum]], [[kao-2024-timing]].
