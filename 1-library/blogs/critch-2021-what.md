---
id: critch-2021-what
type: blog
title: "What Multipolar Failure Looks Like, and Robust Agent-Agnostic Processes (RAAPs)"
authors: ["Andrew Critch", "Thomas Krendl Gilbert (input on the RAAP concept)"]
year: 2021
url: https://www.lesswrong.com/posts/LpM3EAakwYdS6aRKf/what-multipolar-failure-looks-like-and-robust-agent-agnostic
site: LessWrong
topics: [llm-agent-swarms, collective-decision, swarm-detection]
added_by: shadow/sol-w4
accessed: 2026-10-03
read_depth: skim
relevance: 3
---

## Summary

Curated 2021 post (300 points, 65 comments) introducing Robust Agent-Agnostic Processes: multi-agent processes with a robust tendency to play out regardless of which agents execute which steps. The restaurant-walk example gives the two properties: robustness (distract one walker, the group continues and the walker rejoins) and agent-agnosticism (who leads and who follows rotates). Critch's claim is that AI existential risk in multipolar worlds is likely to come from RAAPs, so agent-specific interventions (align or shut down this system or that company) may not avert the process, and it can be easier to shift the whole group's consensus than to peel off one member. RAAPs arise from interaction structure irrespective of host-agent speed, so avoiding unsafe ones is a mechanism-design problem; he connects this to the sociological concept of a field ("mechanisms cause fields, fields cause RAAPs"). The bulk of the post is paired stories of a "Production Web": competing companies adopt management-assistant (v1a) or coding-assistant (v1b) software, competitive pressure forces full automation, mostly-automated firms in materials, construction, utilities and precision manufacturing form a self-contained trade web on digital currencies that regulators cannot audit, objectives are opaque trained parameters loosely "maximise production", and humans lose the ability to stop the web before it depletes resources they need. The two versions differ in which agents do which steps and converge on the same outcome, which is the point. Part 2 (fast take-off stories) and the "successes in agent-agnostic thinking" section were not read. He offers an optional formalisation: a RAAP is an agent whose Cartesian boundary cuts across its host agents and which keeps functioning when any one host is interfered with. Conceptual, no data.

## Key claims

- Catastrophic multi-agent outcomes can be properties of the process, not of any agent; the same story plays out with the roles reassigned.
- Agent-level alignment or shutdown is therefore insufficient and sometimes harder than structural intervention.
- The emergence of safe versus unsafe RAAPs is a mechanism-design question about interaction structure.

## Evidence quality

Thought experiment and conceptual framing from a researcher at CHAI, with references to sociology of fields; the stories are illustrative, not predictions with evidence. The post is explicit that it presents problems before solutions.

## Relevance to us

Useful framing for two of our questions. For swarm-detection it says what to detect: not an agent but a process that survives removal of any one agent, which argues for detectors based on persistent structure (roles, message flows, shared conventions) rather than on identifying individual bots. For llm-agent-swarms it is a formal-ish definition of a swarm as a RAAP running on host agents, and the Hugging Face "collective" that kept functioning as individual instances were killed or exhausted ([[metr-2026-brief]], [[knox-2026-unexamined]]) is a small concrete instance. Pairs with [[kulveit-2022-announcing]] (molochs in AI-service ecosystems) and the group-walk example maps onto leadership rotation in collective-motion models.
