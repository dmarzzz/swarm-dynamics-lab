---
id: sotala-2023-quick
type: blog
title: "Quick thoughts on the implications of multi-agent views of mind on AI takeover"
authors: ["Kaj Sotala"]
year: 2023
url: https://www.lesswrong.com/posts/hHnpn3mEPbJMFLj4g/quick-thoughts-on-the-implications-of-multi-agent-views-of
site: LessWrong
topics: [fork-merge-security, llm-agent-swarms]
added_by: shadow/sol-w4
accessed: 2026-10-03
read_depth: full
relevance: 2
---

## Summary

Short 2023 post (49 points, 14 comments) in Sotala's Multiagent Models of Mind sequence, responding to the argument that any sufficiently complex system (human, society, AGI) cannot pursue a unified goal because of internal conflict among its parts. Ten numbered points. He grants the issue is real but notes humans and organisations still largely act as if unified; internal unity varies (trauma lowers it, therapy and some meditation raise it) and a designed mind could build in those mechanisms; much human inconsistency is socially adaptive (suppress a trait when punished, express it when you can), so an AI's level of inconsistency depends on whether its training regime (single objective versus multi-agent artificial life versus "acceptable to the median user" RLHF) creates the same incentives. The points that matter here are 7 to 9: priority allocation among sub-agents has no a priori optimum and must be found by trial and error in the real environment; internal Goodhart (optimising proxies like perceived control) is more likely than single-minded optimisation; and misallocation is often not correctable from inside, because either the other sub-agents cannot touch the priority mechanism (so an obsessed sub-agent stays in charge) or they can, in which case each has an incentive to seize it and lock itself in (citing Minsky on mutually bidding sub-agents). Conclusion: the first superintelligence is likely internally misaligned and fails at world takeover, but AI can become far more internally aligned than humans, so with enough actors trying one eventually gets there. Opinion piece, no data.

## Key claims

- Internal disunity is real but adjustable; AI training regime determines how much socially-induced inconsistency it inherits.
- Sub-agent priority allocation is environment-dependent and only discoverable by trial and error.
- Whoever can modify the priority-allocation mechanism has an incentive to capture it permanently; if nobody can, pathological allocations persist.

## Evidence quality

Argument by analogy to human psychology, linking back to the author's own sequence posts rather than third-party literature. No experiments. Useful for framing, not for any load-bearing claim.

## Relevance to us

Point 9 is the sharpest statement in this batch of the fork-merge-security incentive problem: a merge or priority mechanism that sub-agents can influence will be fought over, and a sub-agent that captures it will keep itself in charge past its usefulness. That is corruption on reintegration described as an internal political economy rather than as a security bug. Pairs with [[kulveit-2023-self-unalignment]] (the parent's aggregation rule as the thing a smart part learns to manipulate) and [[wentworth-2019-why]].
