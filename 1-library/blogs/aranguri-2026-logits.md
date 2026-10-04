---
id: aranguri-2026-logits
type: blog
title: "Logits as a new monitor for evaluation awareness"
authors: [Santiago Aranguri]
year: 2026
url: https://www.lesswrong.com/posts/PK7ZvFZxrgpYtrpF4/logits-as-a-new-monitor-for-evaluation-awareness-1
site: LessWrong (Goodfire)
topics: [llm-agent-swarms]
added_by: dmarz/honeypot-vigilance
accessed: 2026-10-03
read_depth: skim
relevance: 3
---

## Summary

LessWrong post (4 June 2026, author affiliated with Goodfire) proposing a training-free "logit monitor" for evaluation awareness. At each sentence boundary in the chain of thought, it forces a fixed set of eval-aware phrases and multiplies their token probabilities, giving the exact probability that the model would say it is being evaluated next. On Kimi K2.5 and Qwen3 32B, with Fortress and Petri prompts as evaluations and WildChat as deployment, the logit monitor reaches AUROC 0.79 from a single rollout. Counting verbalisations plateaus at 0.75 even with 100 rollouts. Applied before any reasoning, it already gives 0.74 (separation) and 0.77 (prediction). Whether a given rollout verbalises awareness explains 0.4% of the monitor's score variance, while whether the prompt ever produces verbalisations explains 24.9%. The author concludes that awareness is mostly set by the prompt rather than built up through reasoning.

## Key claims

- Eval-aware probability can be read at every step of a rollout without training a probe, at 10 to 100 times fewer rollouts than counting verbalisations.
- In these single-prompt settings, awareness is largely fixed at the start by the prompt.

## Evidence quality

Independent research post with quantitative results on two open models and public prompt sets. Not peer-reviewed. We read it through a fetch summary, not line by line.

## Relevance to us

A ready instrument for V5. Running the logit monitor at every step of an agent run gives an awareness time series, so a jump at the moment of honeypot discovery would be visible directly instead of being inferred from occasional verbalisations. Its finding that awareness is set by the prompt is for single prompts. Whether a cue discovered mid-run resets it is exactly V5's question. See [[knecht-2026-evaluation]] (position effects) and [[li-2026-decomposing]].
