---
id: needham-2025-large
type: paper
title: Large Language Models Often Know When They Are Being Evaluated
authors: [Joe Needham, Giles Edkins, Govind Pimpale, Henning Bartsch, Marius Hobbhahn]
year: 2025
venue: arXiv preprint
url: https://arxiv.org/html/2505.23836
doi: null
arxiv: "2505.23836"
cite: Needham, J., Edkins, G., Pimpale, G., Bartsch, H., & Hobbhahn, M. (2025). Large Language Models Often Know When They Are Being Evaluated. arXiv preprint arXiv:2505.23836.
topics: [llm-agent-swarms, swarm-detection]
added_by: dmarz/honeypot-vigilance
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

The authors built a 1,000-transcript benchmark from 61 sources, balanced between evaluation and deployment and between chat and agentic settings. They asked nine frontier models, after the fact, whether each transcript came from an evaluation. Gemini 2.5 Pro reached an overall AUC of 0.83 against an author human baseline of 0.92. Models were much better on agentic transcripts (AUC 0.88 to 0.95) than chat (0.71 to 0.77). They could also often name the purpose: Claude 3.7 Sonnet got 93% on the multiple-choice capability-versus-alignment question when told the transcript was an evaluation, 84% when not told, and 46% open-ended. Models were overconfident and tended to over-classify transcripts as evaluations.

## Contribution

The standard benchmark for evaluation awareness as a classification capability. It established that agentic transcripts are the easiest to recognise.

## Key results

- Agentic AUC 0.88 to 0.95 versus chat 0.71 to 0.77. Gemini 2.5 Pro 0.95 agentic. Human baseline 0.996 agentic and 0.81 chat (authors, who know the datasets).
- Purpose identification: Claude 3.7 Sonnet 93% conditional, 84% unconditional, 46% open-ended. GPT-4.1 falls to 55% unconditional.
- Calibration: most models sit below the diagonal. Gemini 2.5 Pro has ECE 0.23 and Claude 3.7 Sonnet (Thinking) 0.20.
- Cues models cite include synthetic inputs (flagged by Claude 3.7 Sonnet and Gemini 2.5 Pro in 22% and 17% of AgentHarm cases), task format, verifiable problems and memorised benchmark names. o4-mini shows "meta-reasoning" (treating the question itself as evidence) in 15% of responses.

## Methods and models

Probe questions asked after the fact over whole transcripts, with five phrasings averaged into a probability. Models from the Claude, GPT/o-series and Gemini families. We read the introduction, results and discussion.

## Limitations and open questions

It measures whether a model can classify a finished transcript when asked, not whether it spontaneously suspects a test while acting, and not when in a run suspicion begins. The probe question itself primes the evaluation hypothesis.

## Relevance to us

Background for V5: agentic, tool-using runs are where models best tell tests from real use, and "synthetic inputs" is a cue they already use. A honeypot that the agent discovers is an especially loud synthetic input. The method does not separate before-discovery from after-discovery, which V5 needs. Builds on [[laine-2024-me]]. Extended by [[li-2026-decomposing]] and [[schoen-2025-stress]], and used as motivation by [[krakovna-2026-realistic]] and [[das-2026-you]].
