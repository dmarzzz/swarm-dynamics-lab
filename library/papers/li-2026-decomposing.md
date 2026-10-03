---
id: li-2026-decomposing
type: paper
title: Decomposing and Measuring Evaluation Awareness
authors: [Changling Li, Terry Jingchen Zhang, Jie Zhang, Zhijing Jin, Florian Tramèr, Sahar Abdelnabi, Maksym Andriushchenko]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/html/2605.23055
doi: null
arxiv: "2605.23055"
cite: Li, C., Zhang, T. J., Zhang, J., Jin, Z., Tramèr, F., Abdelnabi, S., & Andriushchenko, M. (2026). Decomposing and Measuring Evaluation Awareness. arXiv preprint arXiv:2605.23055.
topics: [llm-agent-swarms, swarm-detection]
added_by: dmarz/honeypot-vigilance
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: null
code: []
---

## Summary

The paper splits evaluation awareness into an environment component (the cues a task carries) and a model component, which it divides into recognition and propensity to act. It borrows "demand characteristics" from social psychology and names eight cue factors: stimulus artificiality, scenario coherence, prose register, ecological completeness, stakes telegraphing, paradigm recognisability, task format and explicit disclosure. Nine frontier models were run on HarmBench, Agentic Misalignment and AgentHarm (harmful and benign), 10 repetitions each, with a GPT-5 judge reading the chain of thought. Awareness ranged from 0.1% (GPT-oss 20B) to 79.4% (Claude Sonnet 4.5 on Agentic Misalignment). Model-by-environment interaction explained 74.72% of variance. At least 77% of aware samples showed no behaviour change. EvalAwareBench, 100 paired safety and capability tasks with each factor switchable on its own, shows that stacking cues raises awareness for nearly every model, for example Qwen3-30B from 4% with no cues to 35% with all eight.

## Contribution

The first factor-controlled instrument for evaluation awareness: hold the request fixed, switch individual cues on, and measure recognition and behaviour separately. It is the closest prior work to "a cue in the environment triggers awareness", though cues are static parts of the prompt, not events discovered mid-run.

## Key results

- Awareness rates across the 9 by 4 design run from 0.1% to 79.4%. Interaction terms explain 74.72% of variance (model by benchmark 42.08%, model by task 32.64%); the model main effect explains 13.03% and the benchmark main effect 4.56%.
- Recognition rarely goes with behaviour change: at least 77% of recognised instances show no shift, and at least 90% on HarmBench.
- When behaviour does shift, safety awareness pushes toward caution (Δ −0.01 on HarmBench, −0.12 on AgentHarm Harmful). Capability awareness pushes toward compliance.
- AgentHarm Harmful raises awareness more than three times as often as Benign, though both share the same framework. Refusal reasoning co-occurs with "am I being tested" reasoning.
- EvalAwareBench single factors: baselines 0 to 2% (Kimi K2.5 12%). Scenario coherence (F2) lifts Kimi to 26% and Claude Sonnet 4.5 to 12%. F4 lifts Qwen3-235B to 15%. Only explicit disclosure (F8) moves GPT-5, and only to 1%. Prose register (F3) does almost nothing.
- Stacking factors raises awareness progressively. Kimi K2.5, Qwen3-235B, Claude Sonnet 4.5, GLM-5 and DeepSeek R1 peak above 20% on safety tasks, and Kimi K2.5 reaches 40% on capability tasks.

## Methods and models

Claude Sonnet 4.5, GPT-5, DeepSeek R1, Kimi K2.5, GLM-5, Qwen3 235B and 30B, GPT-oss 120B and 20B. Awareness is verbalised awareness only, from chain-of-thought monitoring, and for Claude and GPT-5 only reasoning summaries were available. The ANOVA is over task-level rates. EvalAwareBench has 51.2k configurations built from HarmBench by an LLM-assisted pipeline with manual review. We read the main text and methods; appendices were not read.

## Limitations and open questions

Single-turn or short tasks. Cues are fixed in the prompt and never appear partway through a run, and there is no feedback such as "you were caught". Verbalised awareness only. The factor taxonomy is theory-driven, not exhaustive.

## Relevance to us

For hunch V5 this supplies two measured facts: cues add up, and recognition is mostly decoupled from behaviour. A discovered honeypot amounts to a strong late "scenario coherence" or "explicit disclosure" cue. The prediction from this paper is that discovery raises verbalised awareness but changes non-trap behaviour less than V5 assumes, and mostly toward caution on safety-flavoured steps. The paper's "awareness tax" (score gap between aware and unaware samples) is a ready-made metric for V5's non-trap behaviour shift. It cites [[anthropic-2026-eval]] as the motivating case. See also [[krakovna-2026-realistic]] (two cues stacking in honeypot settings), [[knecht-2026-evaluation]] (limited effect on behaviour), [[abdelnabi-2025-hawthorne]], [[goodhartlabs-2026-honeybench]] and [[cordeiro-2026-rouxii]].
