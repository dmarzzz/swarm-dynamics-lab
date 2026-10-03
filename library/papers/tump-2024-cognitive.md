---
id: tump-2024-cognitive
type: paper
title: "A Cognitive Computational Approach to Social and Collective Decision-Making"
authors: ["Alan N. Tump", "Dominik Deffner", "Timothy J. Pleskac", "Pawel Romanczuk", "Ralf H. J. M. Kurvers"]
year: 2024
venue: "Perspectives on Psychological Science"
url: https://doi.org/10.1177/17456916231186964
doi: "10.1177/17456916231186964"
arxiv: null
cite: "Tump, A. N., Deffner, D., Pleskac, T. J., Romanczuk, P., & Kurvers, R. H. J. M. (2024). A Cognitive Computational Approach to Social and Collective Decision-Making. Perspectives on Psychological Science, 19(2), 538–551. https://doi.org/10.1177/17456916231186964"
topics: ["collective-decision", "llm-agent-swarms", "crowds-and-traffic"]
added_by: dmarz/collective-decision-audit
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "34 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Perspective arguing that collective dynamics should be studied with experiments in which people interact repeatedly in real time and with formal cognitive models fitted to each individual, so that individual cognition and group dynamics can be linked in both directions. The authors illustrate the approach with evidence-accumulation (drift-diffusion) models and reinforcement-learning models applied to interactive group experiments.

## Contribution

Bridges the physics-style collective-behaviour models that idealise individuals (Vicsek, voter model) and cognitive psychology, which models individuals in static social settings. It proposes cognitive modelling as the middle ground, a framing relevant to agents whose individual "cognition" is rich, such as humans or LLMs.

## Key results

- Conceptual review, no new data. Three aims: how individual cognition drives social systems, how social systems change individual cognition, and the feedback between the two.
- Evidence-accumulation models capture both choices and response times, and so the timing of social information, which static designs lose (authors' argument, illustrated with prior studies).
- Reinforcement-learning models capture how social learning strategies evolve over repeated decisions.

## Methods and models

Literature synthesis. The drift-diffusion and RL frameworks are presented with recommended tooling (Stan, PyMC3, Turing). Published online 2023, in the March 2024 issue. I read the abstract and introduction and skimmed the model sections.

## Limitations and open questions

Programmatic; the gain over simpler models is argued case by case. Fitting individual-level cognitive models in large groups is data-hungry.

## Relevance to us

The methodological frame for measuring LLM-agent swarms as cognitive agents rather than as particles: fit accumulation thresholds and social weights per agent, then predict group outcomes. Related: [[bate-2026-indecision]] (accumulation with social waves), [[mann-2018-collective]], [[becker-2017-network]], [[lorenz-2011-how]].
