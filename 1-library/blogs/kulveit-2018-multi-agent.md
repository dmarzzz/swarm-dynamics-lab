---
id: kulveit-2018-multi-agent
type: blog
title: "Multi-agent predictive minds and AI alignment"
authors: ["Jan Kulveit"]
year: 2018
url: https://www.lesswrong.com/posts/3fkBWpE4f9nYbdf7E/multi-agent-predictive-minds-and-ai-alignment
site: LessWrong
topics: [fork-merge-security, collective-decision]
added_by: shadow/sol-w4
accessed: 2026-10-03
read_depth: skim
relevance: 1
---

## Summary

Kulveit's 2018 post (63 points, 18 comments), the earliest in the line that becomes [[kulveit-2022-announcing]] and [[kulveit-2023-self-unalignment]]. Part one is a best-guess model of human minds: predictive processing and active inference under bounded rationality, where motivations are subprograms each tracking a variable ("hungry", "social status"), predicting its desired state and emitting prediction error as the demand for action; emotions are body-level reward signals re-integrated upward; consciousness illuminates a small part of the computation and is largely a press secretary for other people. Part two lists tensions with value learning: no clean split between beliefs and goals (a mind that predicts failure may act to produce it), and no self-alignment because utility functions describe sub-systems better than the whole, whose decisions are outcomes of multi-agent interaction (a repeated prisoner's dilemma transcript is not a utility maximiser's trace); VNM-like behaviour is expected when one sub-agent dominates or when sub-agents bargain to a welfare function, and non-VNM behaviour when they are stuck in a non-cooperative equilibrium. It then enumerates four notions of alignment target (aggregation output without querying, with querying, the whole system including the aggregation, and a fourth we did not reach), noting that query-based methods like CIRL let the AI choose which sub-agents get a voice and so manipulate the aggregation. Part three (research agenda) was not read. Speculative by the author's own account; no formal model or data.

## Key claims

- Human motivation is better modelled as many prediction-error-minimising sub-systems than as one utility function; the whole mind's behaviour is a multi-agent outcome.
- Which sub-agents are "heard" depends on the aggregation and on how they are queried, so an aligner that controls the queries controls the aggregation.
- Four distinct alignment targets follow from the sub-agent view, and they are not equivalent.

## Evidence quality

Conceptual, hedged ("I have no formal training in cognitive neuroscience"), citing predictive-processing popularisations and CIRL rather than primary experiments. Precursor material; the later posts state the same ideas more crisply.

## Relevance to us

Background only. The one point worth carrying into fork-merge-security is that the party who chooses how to query sub-agents effectively chooses the merge result, which is a manipulation channel for a parent agent over its forks (or a corrupted fork that can shape what the parent asks). Prefer [[kulveit-2023-self-unalignment]] for citation.
