---
id: zhou-2025-sotopia-s4
type: paper
title: "SOTOPIA-S4: a user-friendly system for flexible, customizable, and large-scale social simulation"
authors: ["Xuhui Zhou", "Zhe Su", "Sophie Feng", "Jiaxu Zhou", "Jen-tse Huang", "Hsien-Te Kao", "Spencer Lynch", "Svitlana Volkova", "Tongshuang Sherry Wu", "Anita Woolley", "et al."]
year: 2025
venue: "arXiv preprint"
url: https://arxiv.org/abs/2504.16122
doi: null
arxiv: '2504.16122'
cite: "Zhou, X., Su, Z., Feng, S., Zhou, J., Huang, J., Kao, H.-T., Lynch, S., Volkova, S., Wu, T. S., Woolley, A., et al. (2025). SOTOPIA-S4: A user-friendly system for flexible, customizable, and large-scale social simulation. arXiv:2504.16122."
topics: [llm-agent-swarms]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "18 (Semantic Scholar, 2026-10-03)"
code: [gh-sotopia-lab-sotopia]
---

## Summary

Packages the SOTOPIA social-interaction framework as a pip-installable system with a simulation engine, a REST API server for managing simulations and a web UI so non-programmers can design, run and analyse multi-turn, multi-party LLM interactions with custom evaluation metrics. Demonstrated on dyadic hiring negotiation and multi-party planning.

## Contribution

Turns a research benchmark into a reusable simulation service with an experimenter-facing UI.

## Key results

- Two use cases (hiring negotiation, multi-party planning); no quantitative scale numbers in the abstract.

## Methods and models

Code lives in the sotopia-lab/sotopia repository (link from the arXiv HTML).

## Limitations and open questions

Abstract only. 'Large-scale' here means many episodes of small-group conversations, not large populations.

## Relevance to us

Borrow idea: REST-managed simulation runs plus a web UI for non-programmers. Code [[gh-sotopia-lab-sotopia]]; original benchmark [[zhou-2023-sotopia]].
