---
id: kulveit-2024-hierarchical
type: blog
title: "Hierarchical Agency: A Missing Piece in AI Alignment"
authors: ["Jan Kulveit"]
year: 2024
url: https://www.lesswrong.com/posts/xud7Mti9jS4tbWqQE/hierarchical-agency-a-missing-piece-in-ai-alignment
site: LessWrong
topics: [fork-merge-security, collective-decision, llm-agent-swarms]
added_by: shadow/sol-w4
accessed: 2026-10-03
read_depth: skim
relevance: 2
---

## Summary

A 2024 post (123 points, 23 comments) in which Kulveit (Alignment of Complex Systems group, see [[kulveit-2022-announcing]]) explains his hierarchical-agency research programme as an edited transcript of a conversation with Claude. The core claim: agents composed of agents (corporations and departments, states and citizens, organisms and cells, an AI composed of parts tracking helpfulness, harmlessness and so on) are everywhere, but there is no good mathematical formalism for them. His desiderata for one: scale-free (objects at every level are the same type, so a coalition is an agent, not a "contract"), expressive enough for real conflicts between levels and for a superagent gaining agency at its subagents' expense, and the objects must carry intentionality (beliefs and goals, including goals about other layers, e.g. a corporation wanting its employees more loyal). He operationalises "is the collective really an agent" by Dennett's intentional stance: a superagent exists where modelling the collective as an agent is predictive. Surveyed and found wanting: game theory (coalitions are a different type from players), category theory (too abstract), flat multi-agent systems, hierarchical MDPs (actions not beliefs), mechanism design (agents versus mechanisms); public choice and active inference are named as the closest. The safety motivation is that an AI's internal parts interact and the whole evolves, including by the AI shaping its own training, which connects to Ngo's value systematisation and Kulveit's self-unalignment problem. Programmatic and conceptual; no formalism is actually delivered in the post. We read the first roughly 60% of the transcript.

## Key claims

- A scale-free, intentionality-carrying formalism for agents made of agents is missing and would matter for alignment the way game theory mattered for strategy.
- Whether a collective is a superagent is an empirical question answered by the predictive value of the intentional stance toward it.
- An AI can be read as a committee of parts tracking different objectives, whose interaction and evolution (including via self-shaped training) is the thing to formalise.

## Evidence quality

Opinion and research agenda. No experiments, no proofs; the transcript format is explicitly an attempt to lower inferential distance. Cites related LessWrong sequences (Cartesian Frames, value systematisation, self-unalignment), not the published literature on hierarchical control or multi-level selection.

## Relevance to us

Frames the fork-merge question at the right level: a parent that forks and merges sub-agents is a two-layer hierarchical agent, and "the superagent gaining agency at the expense of subagents" or the reverse is exactly the corruption-on-reintegration failure in abstract form. Useful mainly for vocabulary and for the Dennett-stance test of when a swarm should be modelled as one agent (also relevant to swarm-detection framing). Pairs with [[wentworth-2019-why]], which gives one concrete committee construction Kulveit's desiderata would want to generalise.
