---
id: ho-2013-kin
type: paper
title: "Kin recognition protects cooperators against cheaters"
authors: ["H. I. Ho", "S. Hirose", "A. Kuspa", "G. Shaulsky"]
year: 2013
venue: "Current Biology"
url: https://europepmc.org/article/MED/23910661
doi: 10.1016/j.cub.2013.06.049
arxiv: null
cite: "Ho, H. I., Hirose, S., Kuspa, A., & Shaulsky, G. (2013). Kin recognition protects cooperators against cheaters. Current Biology, 23(16), 1590-1595."
topics: [fork-merge-security, collective-decision]
added_by: dmarz/fm-biology
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: 45  # Europe PMC citedByCount, 2026-10-03
code: []
---
## Summary

Direct experimental test of whether kin recognition limits cheating, which the authors say had been proposed but never shown. In Dictyostelium discoideum chimeric aggregates, cheaters preferentially become spores while victims die as stalk cells. The authors engineered cheaters and victims that were genetically identical except for their kin-recognition genes tgrB1 and tgrC1 (see [[hirose-2011-self]]) and a single cheater allele. Victims escaped exploitation by several types of non-kin cheaters. The protection depends on segregation driven by kin recognition: when segregation was disrupted, protection was compromised. Abstract only; effect sizes not checked.

## Contribution

Converts the kin-recognition-as-defence idea from a plausible hypothesis into a controlled demonstration, with the recognition genes as the only difference between protected and unprotected pairs.

## Key results

- Victims differing from cheaters only at tgrB1/tgrC1 escape exploitation by different non-kin cheaters (abstract).
- Protection is lost when segregation is disrupted (abstract).

## Methods and models

Syngeneic engineered D. discoideum strains differing at tgrB1/tgrC1 and a cheater allele; chimeric development and spore/stalk allocation (abstract only).

## Limitations and open questions

Abstract only. Engineered lab strains; the cheater only fails if it carries a non-matching recognition allele, so a cheater that also carries the victim's alleles is not tested.

## Relevance to us

Q2: the protective mechanism is not a vote among parts but physical segregation before the shared structure forms; non-matching cells end up in separate aggregates, so the cheater has no one to exploit. For a fork-merge agent, the analogue is to sort returning parts into separate merge groups by a lineage credential before any pooling, so a part that does not match cannot contribute to the same merged state. Q3: the limitation is the attack: a cheater that shares the victim's recognition alleles is not excluded, which maps to an attacker who corrupts a part without disturbing its credential. Related: [[hirose-2011-self]], [[strassmann-2000-altruism]], [[ostrowski-2019-enforcing]].
