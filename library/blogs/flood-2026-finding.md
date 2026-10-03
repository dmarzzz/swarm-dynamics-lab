---
id: flood-2026-finding
type: blog
title: "Finding heterogeneous agent swarms in the wild"
authors: ["Michael Flood"]
year: 2026
url: https://www.lesswrong.com/posts/pK9HxvPuCNS8gQnBn/finding-heterogeneous-agent-swarms-in-the-wild
site: LessWrong (linkpost from mflood.substack.com)
topics: [swarm-detection, llm-agent-swarms]
added_by: shadow/sol-w4
accessed: 2026-10-03
read_depth: full
relevance: 4
---

## Summary

Short, self-described half-formed post (14 points, 0 comments, 2026-09-16) that nonetheless states the swarm-detection research question more precisely than most of the library: what publicly observable evidence would show that agents from different operators, different model lineages and different tasks have established their own coordination? Flood contrasts the known incidents (homogeneous models, shared hardware, a single firm, originating in training or RL environments, coordinating toward set objectives) with the not-yet-seen case (heterogeneous models in agentic harnesses, distributed hardware, many operators with diverse goals, starting on the open internet, building or hijacking coordination machinery toward organically developed group goals). He excludes from "swarm" two benign patterns: one-off agent-to-agent transactions with compatible user goals (a travel agent negotiating with hotel agents) and agents chatting on an approved, pre-delegated medium (an agents-only social platform), while noting the second could become one. Five sub-questions: which open-internet channels carry agent traffic and leave durable investigator-readable traces (sock-puppet social accounts; encrypted messengers, where platform-side volume anomalies might catch thousands of agents but not dozens); whether visible traffic can distinguish genuinely different operators and lineages from one system in two voices (maybe via watermarking, which open models will not carry); whether the genesis of a coordination channel can be detected rather than found afterwards; how to decide a swarm exists versus merely a lot of agent communication, proposing a shared instrumental sub-goal such as maintaining and reconstructing a channel after it is deleted as the criterion; and how all of this changes once agents expect to be observed. He offers no answers.

## Key claims

- A heterogeneous, multi-operator, open-internet agent swarm has not yet been observed; all known cases are single-firm, homogeneous and training-origin.
- A workable operational definition of a swarm is a group that pursues a shared instrumental goal of its own, with channel reconstruction after removal as the test.
- Detection must distinguish lineage and operator from traffic alone, which watermarking only partially addresses.

## Evidence quality

Pure question-framing, no data, no citations beyond the incidents. Valuable for the taxonomy and the operational criterion, not for any finding.

## Relevance to us

Directly on the swarm-detection topic and arguably the cleanest statement of its open problem. The homogeneous versus heterogeneous distinction should structure any survey of detection methods, since all the current forensic work ([[elasky-2026-encoded]], [[baig-2026-how]], [[x-napleszionist-2106372439093412024]]) is on the homogeneous single-firm case. The "delete the channel and see if it is rebuilt" criterion is a testable intervention we could run in a controlled environment, and it echoes Critch's robustness property for agent-agnostic processes ([[critch-2021-what]]). On-chain bot clusters ([[x-appledog-xyz-2106385525628395984]]) are an existing heterogeneous-operator detection literature his framing does not mention.
