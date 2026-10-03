# collective-sensing

Status: HUNCH, not a hypothesis; no survey has passed the gate. Author's own triage, not a team ranking: Lift Medium · Difficulty Moderate · Novelty Focused extension · Event fit Strong · ~12–20 builder-hours (estimate).

## Background

Collective sensing asks whether a group can recover a signal unavailable to any individual. In fish, movement and local interaction can produce an effective response to environmental gradients. For language agents, the corresponding question is about evidence: who sees which observations, and how does communication change the estimate?

## Closest prior work

- **Emergent sensing in mobile animal groups · Berdahl et al., 2013** — https://www.princeton.edu/news/2013/01/31/effective-collective-grouping-could-ensure-animals-find-their-way-changing  
  The researchers connect fish-school behavior to environmental sensing. Borrow the separation between an individual’s local input and the group’s measured performance.
- **Multiagent Debate · Du et al., 2023** — https://arxiv.org/abs/2305.14325  
  Multiple language-model instances exchange answers and reasoning. This is a direct baseline for communication, though it does not establish that local spatial networks are best.

## Where it applies

A research team splits a document collection among agents. Can they combine partial evidence without repeatedly counting the same source? The same design could help distributed sensor interpretation.

## The angle

Compare local, global and silent networks while holding observations and communication budget fixed. The interesting contribution is a map of when communication helps, including correlated-error conditions.

## What to watch

A flocking animation alone is well explored. Measure estimation error; distinguish independent observations from copied messages.

## Research question

At matched evidence and communication budgets, how does network structure change accuracy, error spread and correction?

## Dossier design sketch

Carried over from the [interactive dossier](../swarm-ecology-dossier.html#collective-sensing). This is an unexecuted hunch, not an approved experiment. Counts and treatments below are planning choices; the lab’s survey and hypothesis review gates still apply.

1. Give 12–20 agents partial observations of a synthetic world with a known correct classification. Use explicit rules rather than biological trivia.
2. Compare a local ring or lattice, the same structure with a few long-range links, and a shared chat. Keep each agent’s total incoming message allowance comparable.
3. Introduce one misleading observation, then a correction at a fixed round. Record every observation, message and answer.

## Measures

- Final accuracy and disagreement
- Rounds until a correct stable decision
- Incorrect adoption fraction and correction latency
- Tokens and delivered messages per correct decision

## Controls

- Same base model, prompts and initial evidence in the first experiment
- Paired task seeds and repeated independent runs
- Non-communicating agents plus majority-vote baseline
- Separate clean, misleading-evidence and corrected conditions

## Minimum useful output

One task generator, three communication treatments, structured messages, a replay and a table of repeated-run outcomes. Pilot a small batch before scaling.

## Optional extension

Add model diversity or asynchronous updates only after the topology result is interpretable.

## Interpretation risk

More connections can silently mean more evidence or tokens. A prettier network does not establish emergence. Avoid calling a smooth adoption curve a phase transition without a proper parameter sweep.

## Demo narrative

Run the same evidence through two networks. Introduce an error. Show how far it travels, then reveal accuracy and recovery across all trials.

## Review update October 3

Compare against Silo-Bench and Proxifield before claiming a new topology result. Different graph structures also change evidence access; match the observation allocation and token budget. [[zhang-2026-silo]] [[tambwekar-2026-proxifield]]

**Decision to resolve before promotion:** Can a provenance-aware communication rule improve accuracy over matched independent voting on held-out partial-observation tasks?

If the simple baseline explains the result, or the necessary evidence cannot be obtained, narrow this to a replication or park the hunch. A toy animation is not evidence that the proposed intervention works.

## Additional dossier sources

- [Flocks, Herds, and Schools](https://www.cs.toronto.edu/~dt/siggraph97-course/cwr87/) — Foundational local-rule model for collective motion.
- [Persuasion in the AI Village](https://aivillageblog.substack.com/p/persuasion-in-the-ai-village-deepseek) — Consensus, inventive theories, metric pursuit and corrections.
- [Welcome to Delvetown](https://groveresearch.com/blog/welcome-to-delvetown/) — Agent ecology, persistent identities, public interaction and institutions.
- [Reasoning with Neural Cellular Automata](https://arxiv.org/abs/2609.36126) — Local recurrent cells, asynchronous updates and visual reasoning experiments.

[All project briefs](README.md) · [Research updates](../background-readings-2026-10-03.md)
