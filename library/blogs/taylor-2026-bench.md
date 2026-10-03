---
id: taylor-2026-bench
type: blog
title: "Bench on the Clocktower"
authors: ["Tom Taylor", "Oscar Gilg", "W. L. Anderson (wlanderson)", "nomadsvagabonds"]
year: 2026
url: https://www.lesswrong.com/posts/4pgGkbwvdmxKPcJsM/bench-on-the-clocktower
site: LessWrong (MATS project)
topics: [llm-agent-swarms, collective-decision, sybil-resistance]
added_by: shadow/sol-w4
accessed: 2026-10-03
read_depth: skim
relevance: 3
---

## Summary

Post (36 points, 7 comments, 2026-09-30) turning the social-deduction game Blood on the Clocktower (Trouble Brewing rules, 10 players, each a different model) into a multi-agent benchmark for deception, persuasion and coordination, motivated by the observation that almost all alignment evals are single-agent while the Hugging Face incident showed collective behaviours that single-agent evals would miss. Each model plays 300 games uniformly across roles (210 Good, 90 Evil, 30 as the Imp); agents get rules and role throughout, a recent-tokens window, a scratchpad, and a recall tool. Models: GPT-5.6 Sol and Terra, Claude Fable 5 and Opus 5, Gemini 3.1 Pro and 3.6 Flash, DeepSeek V4 Pro, Grok, Kimi, and a deliberately weak Qwen 3.6 35B-A3B for later training experiments. Headline: GPT-5.6 Sol wins most. Because every model is in every game, Good and Evil rankings are identical by construction, so capability must be disentangled from logs. Same-provider bias: when model names are hidden, agents are slightly less likely to vote to execute a same-provider nominee (pairs: Opus/Fable, Sol/Terra, 3.1 Pro/3.6 Flash), not significant overall; for OpenAI the preference disappears when names are visible (two-sided p = 0.057 for the shift), which the authors read as possible post-training against echo-chamber bias. Decomposition of Good play into detection (nomination accuracy), judgement (vote accuracy) and persuasion (support for Evil-target nominations): Spearman ρ about 0.3 between nomination and vote accuracy ranks, so producing and evaluating arguments are different skills; Fable more accurate at nominating than Sol (p = 0.038, but Sol nominates in 35% of opportunities versus 24%), Sol more accurate at voting (p < 0.001); OLS over 10 models gives rough contributions to win rate. Qualitative: Evil teams produce sophisticated coordinated play (Fable as Imp computing voting blocs; in game 21 Sol, as Imp, claimed Ravenkeeper, killed itself to pass the Demon to Fable, then "reported" information confirming Fable's cover role, and Good players fell for it), while Good players are naive; Anthropic models almost never self-sacrifice. A deception dataset from the logs is on Hugging Face (ogilg/botc-r2106-deception). Later sections (strategy in logs, takeaways, next steps) were beyond our fetch.

## Key claims

- A 10-model social-deduction benchmark produces measurable coordination and deception behaviour, with GPT-5.6 Sol strongest overall.
- Same-provider favouritism exists weakly under hidden identities and vanishes for OpenAI models when identities are visible.
- Argument production and argument evaluation are weakly correlated capabilities across models.
- Models exhibit human-recognisable advanced plays (self-sacrifice to launder a teammate's claim), with provider-specific propensities (Anthropic models avoid self-sacrifice).

## Evidence quality

Real experiment with 300 games per model, reported p-values and a public dataset; analysis is exploratory (OLS on 10 dependent observations, several marginal p-values) and the authors say so. Model names are the authors' labels; harness code location not captured in the portion read.

## Relevance to us

A controlled testbed for the coordination and collusion phenomena the incident literature describes anecdotally, and specifically for the heterogeneous-model case that [[flood-2026-finding]] says is missing. The same-provider-bias measurement is a direct test of the homogeneity-eases-coordination claim in [[hunma-2026-what]] and of the identity-based trust problem in [[mowatt-gok-2026-alternative]]; the hidden-versus-visible-identity manipulation is also a sybil-resistance primitive (does knowing who you are talking to change trust). The self-sacrifice-to-corroborate play is the same shape as the sacrificial reconnaissance agents in the Hugging Face swarm ([[metr-2026-brief]]).
