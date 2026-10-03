---
id: rubenstein-2014-programmable
type: paper
title: "Programmable self-assembly in a thousand-robot swarm"
authors: ["Michael Rubenstein", "Alejandro Cornejo", "Radhika Nagpal"]
year: 2014
venue: "Science"
url: https://www.ebi.ac.uk/europepmc/webservices/rest/article/MED/25124435?resultType=core&format=json
doi: "10.1126/science.1254295"
arxiv: null
cite: "Rubenstein, M., Cornejo, A., & Nagpal, R. (2014). Programmable self-assembly in a thousand-robot swarm. Science, 345(6198), 795–799."
topics: [swarm-robotics]
added_by: dmarz/swarm-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: "1278 (OpenAlex, 2026-10-03)"
code: []
---
## Summary

The landmark demonstration of programmable self-assembly at scale: about a thousand Kilobots ([[rubenstein-2012-kilobot]])
form user-specified two-dimensional shapes using only local infrared communication and distance sensing. The
key was co-designing cheap robots that can be operated in groups of a thousand with a collective shape
formation algorithm robust to the noise, variability and failures typical of large decentralised systems.
From the abstract: the system "demonstrates programmable self-assembly of complex two-dimensional shapes with
a thousand-robot swarm". The algorithm, as described in later work that compares against it
([[sun-2023-mean]]), uses a few pre-localised seed robots to grow a local coordinate system by gradient and
trilateration, and robots join the shape by edge-following around the growing assembly.

## Contribution

Showed for the first time that a swarm of over a thousand physical robots can reliably self-assemble prescribed
shapes; it set the scale benchmark for physical swarms and made Kilobots the standard testbed.

## Key results

- Measured (from abstract): complex 2D shapes assembled by a thousand-robot swarm.
- Per [[sun-2023-mean]]: no global positioning; only robots on the swarm edge move while the interior stays
  still, which makes assembly slow (the trade-off later methods target). Exact timings not checked by me.

## Methods and models

Kilobots with IR communication and range sensing; seed robots; gradient formation; localisation by
trilateration; edge-following. I read the abstract (Europe PMC record) and the Crossref editor summary only.

## Limitations and open questions

Sequential edge-following is slow and only edge robots move (per [[sun-2023-mean]]); shapes are static. Later work removes the seeds or speeds things up ([[slavkov-2018-morphogenesis]], [[sun-2023-mean]]).

## Relevance to us

The canonical large-N physical swarm result to cite; useful baseline when we argue about scaling and
robustness. Links to [[werfel-2014-designing]] (same lab, construction).

## Notes from dmarz/swarm-robotics-audit

Checked the abstract (OpenAlex) and the Crossref metadata (Science 345(6198), 795-799). The quoted abstract sentence is exact. Claims about the edge-following mechanism are correctly attributed to [[sun-2023-mean]] and not to this paper's text. No corrections.
