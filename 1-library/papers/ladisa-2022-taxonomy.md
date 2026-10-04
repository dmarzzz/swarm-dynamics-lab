---
id: ladisa-2022-taxonomy
type: paper
title: "Taxonomy of Attacks on Open-Source Software Supply Chains"
authors: ["Piergiorgio Ladisa", "Henrik Plate", "Matias Martinez", "Olivier Barais"]
year: 2022
venue: "arXiv preprint (cs.CR); published as \"SoK: Taxonomy of Attacks on Open-Source Software Supply Chains\" in 2023 IEEE Symposium on Security and Privacy"
url: https://arxiv.org/pdf/2204.04008
doi: null
arxiv: "2204.04008"
cite: "Ladisa, P., Plate, H., Martinez, M., & Barais, O. (2022). Taxonomy of Attacks on Open-Source Software Supply Chains. arXiv:2204.04008 [cs.CR]. Published version: SoK: Taxonomy of Attacks on Open-Source Software Supply Chains, 2023 IEEE Symposium on Security and Privacy (SP), pp. 1509-1526, doi:10.1109/SP46215.2023.10179304."
topics: [fork-merge-security, meta]
added_by: dmarz/fm-mobile-agents
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "183 (Crossref, S&P 2023 version, 2026-10-03)"
code: []
---

## Summary

A systematisation of how attackers inject malicious code into open-source artifacts that downstream projects then execute. The taxonomy is an attack tree with disjunctive refinement covering 107 unique attack vectors, linked to 94 real-world incidents and mapped to 33 safeguards. It was built from a review of 183 scientific works plus grey literature, and validated with surveys of 17 domain experts and 134 software developers, who also rated the utility and cost of the safeguards. Top-level branches cover developing and advertising a distinct malicious package (for example typosquatting), injecting into the source of a legitimate package (via a contributor's merge request or a compromised maintainer account), injecting during the build, and injecting during distribution. I read the abstract, introduction, methodology and attacker model and looked through the tree structure.

## Contribution

The broadest single map of "how a trusted merge pipeline gets poisoned" in a deployed ecosystem, with real incidents attached to each leaf. A review-type source for this lane.

## Key results

- 107 attack vectors, 94 incidents, 33 safeguards (counts from the paper).
- Validation surveys: 17 experts, 134 developers.
- Attacker goal: get code executed in downstream contexts; payloads include exfiltration, backdoors and second-stage downloads.
- Contribution via merge request and maintainer account takeover are distinct branches with distinct safeguards.

## Methods and models

Systematic literature review, attack-tree modelling, expert and developer surveys.

## Limitations and open questions

Taxonomy assigns each instance to one class; survey validation measures perceived correctness, not detection rates.

## Relevance to us

Q3: the merge-request and maintainer-takeover branches are the software analogue of a returning sub-agent: a contribution from an apparently legitimate party is merged into a trusted line. Many incidents rely on social trust in the contributor, which maps to a parent trusting a child because it is its own fork. Q2: the safeguards list (multi-party review, signed commits, reproducible builds, scoped tokens) gives candidate merge gates and their reported costs. Related: [[torres-arias-2019-in-toto]], [[torres-arias-2016-omitting]], [[lamb-2022-reproducible]], [[crowdstrike-2021-sunspot]].
