---
id: drexler-2019-reframing
type: paper
title: "Reframing Superintelligence: Comprehensive AI Services as General Intelligence"
authors: [K. Eric Drexler]
year: 2019
venue: Technical Report #2019-1, Future of Humanity Institute, University of Oxford
url: https://static1.squarespace.com/static/660e95991cf0293c2463bcc8/t/660ec8f0ca87a33aa8832af3/1712244978900/2019-1.pdf
doi: null
arxiv: null
cite: "Drexler, K. E. (2019). Reframing Superintelligence: Comprehensive AI Services as General Intelligence. Technical Report #2019-1, Future of Humanity Institute, University of Oxford."
topics: [fork-merge-security, llm-agent-swarms, meta]
added_by: dmarz/fm-sutton
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: null
code: []
---

## Summary

A 210-page technical report (about 63,000 words, written as a series of linked sections) arguing that advanced AI is better modelled as comprehensive AI services (CAIS), bounded systems performing bounded tasks within a recursively automated R&D process, than as a unitary self-improving rational agent. Read for the abstract, overview and Section 16, "Aggregated experience and centralized learning support AI-agent applications". Section 16 argues that "aggregation of information across N agents (potentially thousands to millions) speeds the acquisition of experience by a factor of N", that amortization "reduces a range of per-agent costs by a factor of 1/N", and that "centralized learning enables pre-release testing for routinely encountered errors and ongoing updates in response to rarely-encountered events". Its example is Tesla fleet learning: vehicles "do not learn as individuals, but instead deliver improved competencies through a centralized R&D process that draws on the operational experience of many vehicles." Figure 8's caption: "Centralized learning enables upgraded agent software to be tested before release." Section 16.6 adds that if novel errors are promptly corrected, "the per-agent probability of encountering a given error will be bounded by 1/N".

## Contribution

Shifts the unit of analysis from an individual learning agent to a development process that aggregates experience from many deployed instances and releases tested updates; this is fork-merge with a release gate.

## Key results

- No experiments; argument from engineering practice.
- Aggregated learning: experience time scales as 1/N, training cost per agent as 1/N.
- Centralised learning permits testing an update before it reaches deployed agents.

## Methods and models

Conceptual; illustrative figures contrast individual learners (Fig. 6), naive multi-agent scale-up (Fig. 7) and centralised aggregated learning (Fig. 8).

## Limitations and open questions

Section 16 treats aggregated experience as benign data. It does not consider deployed instances that return adversarially crafted experience, which is the federated-poisoning threat. The safety argument of CAIS rests on bounded tasks, not on the integrity of the aggregation channel.

## Relevance to us

Drexler's aggregation pipeline is the engineering version of Sutton's "report back to the central master" ([[sutton-2025-father]]) and of mega-Sundar ([[dwarkesh-2025-what]]), predating both by six years. It contributes one defence relevant to Q2 and Q3: merge into a development process with pre-release testing, not directly into the running parent. A k-of-n rule fits naturally there, since an aggregated update can require that a behaviour change be supported by experience from many instances rather than one. The same 1/N amortisation that makes aggregation attractive is what makes one poisoned contributor cheap for an attacker, a point the report does not address. CAIS also argues for bounded, task-specific services over unitary agents, which suggests children that are not full copies of the parent: a narrower child that is captured exposes less, a Q1-adjacent design choice.
