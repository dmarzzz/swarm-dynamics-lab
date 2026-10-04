---
id: amrouni-2021-abides
type: paper
title: "ABIDES-Gym: Gym Environments for Multi-Agent Discrete Event Simulation and Application to Financial Markets"
authors: ["Selim Amrouni", "Aymeric Moulin", "Jared Vann", "Svitlana Vyetrenko", "Tucker Balch", "Manuela Veloso"]
year: 2021
venue: "ACM International Conference on AI in Finance (ICAIF 2021)"
url: https://arxiv.org/abs/2110.14771
doi: "10.1145/3490354.3494433"
arxiv: "2110.14771"
cite: "Amrouni, S., Moulin, A., Vann, J., Vyetrenko, S., Balch, T., & Veloso, M. (2021). ABIDES-Gym: Gym Environments for Multi-Agent Discrete Event Simulation and Application to Financial Markets. Proceedings of the Second ACM International Conference on AI in Finance (ICAIF '21). https://doi.org/10.1145/3490354.3494433"
topics: [marl-emergence, meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "67 (Semantic Scholar, 2026-10-03)"
code: [gh-jpmorganchase-abides-jpmc-public]
---

## Summary

Proposes a general technique for wrapping a discrete-event multi-agent simulator, in which time advances by events rather than fixed steps, into the OpenAI Gym interface, so a single experimental agent can be trained with model-free RL against a population of simulated agents. Implemented on ABIDES and ABIDES-Markets with two benchmark environments, a daily investor and an execution agent.

## Contribution

A recipe for exposing one agent of an event-driven multi-agent simulation as a Gym environment, which is the same interface needed to drop an LLM policy into a scripted population.

## Key results

- Two Gym environments for financial markets (daily investor, execution) (abstract).

## Methods and models

Not read beyond the abstract.

## Limitations and open questions

Only the abstract was read. The Gym layer pins gym 0.18 and ray 1.7 in the repository, which did not install on our Mac.

## Relevance to us

Template for "one learning or LLM agent among many scripted agents" experiments in event-driven markets; see [[gh-jpmorganchase-abides-jpmc-public]].
