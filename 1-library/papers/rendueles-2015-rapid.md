---
id: rendueles-2015-rapid
type: paper
title: "Rapid and widespread de novo evolution of kin discrimination"
authors: ["O. Rendueles", "P. C. Zee", "I. Dinkelacker", "M. Amherd", "S. Wielgoss", "G. J. Velicer"]
year: 2015
venue: "Proceedings of the National Academy of Sciences of the United States of America"
url: https://europepmc.org/article/MED/26150498
doi: 10.1073/pnas.1502251112
arxiv: null
cite: "Rendueles, O., Zee, P. C., Dinkelacker, I., Amherd, M., Wielgoss, S., & Velicer, G. J. (2015). Rapid and widespread de novo evolution of kin discrimination. Proceedings of the National Academy of Sciences of the United States of America, 112(29), 9076-9081."
topics: [fork-merge-security, collective-decision]
added_by: dmarz/fm-biology
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: 63  # Europe PMC citedByCount, 2026-10-03
code: []
---
## Summary

Uses the social bacterium Myxococcus xanthus, whose swarming colonies merge freely only with close relatives. Natural isolates showed that colony-merger incompatibilities are strong barriers, especially by reducing chimerism in multicellular fruiting bodies formed near territory borders. In laboratory evolution, the generic process of adaptation, in any selective environment, repeatedly produced kin-discriminatory behaviour between evolved populations and their common ancestor, and discrimination evolved indirectly between replicate populations that adapted separately to the same habitat. Patterns suggest many different genetic mechanisms. Some populations acquired strong incompatibility abruptly, others gradually. The authors compare this to reproductive isolation between separated sexual populations and linguistic divergence between human cultures. Abstract only.

## Contribution

Shows that merge incompatibility between lineages arises as a by-product of separate adaptation, without selection for discrimination itself.

## Key results

- Colony-merger incompatibility reduces chimerism in fruiting bodies of natural isolates (abstract).
- Evolved populations repeatedly became incompatible with their ancestor and with each other, across many habitats (abstract).
- Onset abrupt in some lines, gradual in others (abstract).

## Methods and models

Colony-merger assays among natural M. xanthus isolates and among experimentally evolved populations; mutation-accumulation comparisons (abstract only).

## Limitations and open questions

Abstract only; numbers of populations and timescales not checked.

## Relevance to us

Q1 and Q3. Sub-agents sent to different domains diverge, and this paper shows that divergence alone makes them fail to merge with the parent and with each other, with no attacker involved. Two consequences for fork-merge agents: a parent must expect benign incompatibility from long-separated parts, so "fails to merge cleanly" is weak evidence of corruption; and an attacker who wants a part accepted has to keep it close to the parent's expected state, which is a constraint a defender can measure. For Q1, divergence also makes returning parts distinguishable from each other, which works against hiding which one returns unless parts are re-homogenized before merge. Related: [[aureli-2008-fission]] on reunion costs, [[hirose-2011-self]].
