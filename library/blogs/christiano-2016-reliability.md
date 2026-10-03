---
id: christiano-2016-reliability
type: blog
title: Reliability amplification
authors: [Paul Christiano]
year: 2016
url: https://www.alignmentforum.org/posts/6fMvGoyy3kgnonRNM/reliability-amplification
site: AI Alignment Forum (reposted 2019-01-31; first published 2016-10-20 on ai-alignment.com)
topics: [fork-merge-security, sync-consensus, collective-decision]
added_by: dmarz/fm-sutton
accessed: 2026-10-03
read_depth: full
relevance: 5
---

## Summary

Christiano observes that composing many weak agents into a stronger one lowers reliability: if each of 10 combined decisions fails with probability 1%, the combination fails with about 10%, and repeated amplification drives failure toward 1. Reliability amplification asks for a procedure that turns a policy distribution that is epsilon-close to benign (modelled as a mixture: aligned with probability 1 minus epsilon, adversarial with probability epsilon) into one that is delta-close with delta much smaller than epsilon. His proposal: sample three agents, let them deliberate, each proposes an action, then approval-vote and pick randomly among the maximally approved. Two adversaries out of three occurs with probability O(epsilon squared); the interesting case is one adversary and two aligned agents, which helps only if aligned agents recognise good actions better than chance. He contrasts this with classic redundant computation (compute three times, majority vote, epsilon to O(epsilon squared)) and lists three ways the agent case is harder: there may be many correct answers, so aligned copies must build consensus (with 99 good answers and 1 bad one chosen uniformly and no ability to agree, error cannot fall below 1%); abilities must be balanced, since "if the unaligned agent is much smarter than the aligned agents, then it can increase the probability of failures which are too subtle"; and deliberation costs each agent thinking time. For sequential decisions, agents must share a "consensus private state", or choosing one agent's plan commits to that agent. An approval-voting implementation was added to his ALBA code (commit 1cbaae).

## Key claims

- Naive composition of weak agents compounds failure probability.
- Best case for 3-way voting among copies is epsilon to O(epsilon squared); realistic case is epsilon to O(epsilon) with a better constant.
- Voting among copies requires a consensus mechanism when correct answers are not unique.
- A much smarter adversarial member can bias outcomes in ways the honest members cannot detect.

## Evidence quality

Theoretical argument in a blog post, with a toy implementation mentioned but no reported measurements.

## Relevance to us

The closest prior statement of Q2 in the AI-alignment literature, written for copies of one policy. It gives the threshold arithmetic directly: with independent corruption probability epsilon per child, a merge that requires agreement of 2 of 3 children fails with O(epsilon squared). It also names the conditions under which the arithmetic breaks, each of which maps to fork-merge: corruption must be independent across children (a shared vulnerability across identical copies, as in [[bostrom-2023-propositions]], breaks it); correct answers must be comparable (children exploring different domains, as in [[sutton-2025-father]], have nothing to vote over, so k-of-n requires overlapping assignments); and a corrupted child must not be much more capable than honest ones (a child that has absorbed a hostile domain may well be). The sequential-state point is the merge problem itself: picking one child's "vision" commits the parent to that child. Companion to [[christiano-2016-security]] and [[christiano-2018-supervising]].
