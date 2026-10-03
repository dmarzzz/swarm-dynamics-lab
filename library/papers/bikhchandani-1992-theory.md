---
id: bikhchandani-1992-theory
type: paper
title: 'A Theory of Fads, Fashion, Custom, and Cultural Change as Informational Cascades'
authors: [Sushil Bikhchandani, David Hirshleifer, Ivo Welch]
year: 1992
venue: Journal of Political Economy
url: https://snap.stanford.edu/class/cs224w-readings/bikhchandani92fads.pdf
doi: 10.1086/261849
arxiv: null
cite: 'Bikhchandani, S., Hirshleifer, D., & Welch, I. (1992). A Theory of Fads, Fashion, Custom, and Cultural Change as Informational Cascades. Journal of Political Economy, 100(5), 992–1026.'
topics: [collective-decision, sync-consensus]
added_by: dmarz/honeypot-vigilance
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

Defines an informational cascade: an individual who sees the actions (not the signals) of those before him finds it optimal to copy them regardless of his own private signal. In the binary model a cascade starts as soon as adopters outnumber rejecters by two, so a society converges on an action from very little information, and with substantial probability on the wrong one even for fairly accurate signals. Because a cascade aggregates only the first few signals, it is fragile: Result 3 shows a public signal less informative than one private signal can shatter a long-running cascade.

## Contribution

The seminal model of herding from rational observational learning, and the source of the claim that mass behaviour is uniform but brittle.

## Key results

- Cascades begin after an imbalance of two actions in the binary example; the probability of a wrong cascade stays considerable even for high signal accuracy p (Fig. 1) (derived).
- When only actions are observable, a cascade is never reversed by later private signals; when signals are observable, enough opposing signals switch behaviour (derived).
- Result 3: a small public information release can break a long cascade (derived). Result 2: early noisy public information can make some individuals worse off (derived).
- Illustrations: hybrid corn adoption in Iowa, oat bran fad (anecdotal).

## Methods and models

Sequential Bayesian decisions with binary values and conditionally independent private signals; extensions to heterogeneous precision and public disclosures. Skimmed: introduction, Section II model and Fig. 1, Section on fragility and public information.

## Limitations and open questions

Fully rational agents with common knowledge of the model; no repeated decisions on the same item, no memory or communication beyond actions.

## Relevance to us

Seminal anchor for V4. A false honeypot flag followed by agents who only see "agent 3 skipped this endpoint" is a down-cascade on a real resource. The model predicts such cascades are easy to start and easy to break with a small correction, so the V4 hunch that a false alarm outlives correction is a departure from rational-cascade theory and worth testing. LLM weight estimates in [[zhong-2025-disentangling]]; animal analogue in [[gray-2023-false]].
