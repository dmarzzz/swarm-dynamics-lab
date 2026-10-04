---
id: hoel-2013-quantifying
type: paper
title: 'Quantifying causal emergence shows that macro can beat micro'
authors: ['Erik P. Hoel', 'Larissa Albantakis', 'Giulio Tononi']
year: 2013
venue: 'Proceedings of the National Academy of Sciences'
url: https://europepmc.org/article/MED/24248356
doi: 10.1073/pnas.1314922110
arxiv: null
cite: 'Hoel, E. P., Albantakis, L., & Tononi, G. (2013). Quantifying causal emergence shows that macro can beat micro. Proceedings of the National Academy of Sciences, 110(49), 19790–19795.'
topics: [criticality-measurement]
added_by: dmarz/criticality-measurement
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: '357 (OpenAlex, 2026-10-03)'
code: []
---

## Summary

Introduces causal emergence: using effective information (EI), the mutual information between
maximum-entropy interventions on a system's state and its effects, the authors show for simple discrete
systems that EI can be larger at a coarse-grained macro level than at the micro level when macro mechanisms
are more deterministic or less degenerate.

## Contribution

Seminal quantitative definition of causal emergence (macro beating micro), the reference point
for later information-decomposition approaches such as [[rosas-2020-reconciling]].

## Key results

- For certain causal architectures EI peaks at a macro scale in space or time (analytic/simulated toy systems).
- Causal emergence = gain in EI moving from micro to macro.

## Methods and models

Effective information computed on transition probability matrices under uniform interventions;
coarse-grainings of logic-gate and Markov-chain systems.

## Limitations and open questions

Requires full knowledge of micro transition probabilities and uses interventional maximum-entropy
distributions rather than observed dynamics, a point [[rosas-2020-reconciling]] criticises. Abstract-level
read.

## Relevance to us

Background for any emergence metric on swarms; practical application to trajectory data is
easier with [[rosas-2020-reconciling]].
