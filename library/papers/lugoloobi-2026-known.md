---
id: lugoloobi-2026-known
type: paper
title: "Known By Their Actions: Fingerprinting LLM Browser Agents via UI Traces"
authors: ["William Lugoloobi", "Samuelle Marro", "Jabez Magomere", "Joss Wright", "Chris Russell"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2605.14786
doi: null
arxiv: "2605.14786"
cite: "Lugoloobi, W., Marro, S., Magomere, J., Wright, J., & Russell, C. (2026). Known By Their Actions: Fingerprinting LLM Browser Agents via UI Traces. arXiv:2605.14786."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: null
code: []
---

## Summary

Shows that a website can passively identify which LLM drives a visiting browser agent from in-page UI events alone. A JavaScript tracker records clicks, scrolls, keypresses, navigation and inter-event timings while 14 multimodal LLMs, run through one identical Midscene.js harness, solve 2WikiMultiHop, FRAMES, WebShop and DeepShop tasks on live sites. XGBoost over timing and action features identifies the model with up to 96% per-model F1, mostly within the first 40% of an episode.

## Contribution

Moves agent detection from "human or bot" to "which model", passively and without network or browser-attribute signals. Complements active text probing ([[pasquini-2024-llmmap]]) and network fingerprints ([[zhang-2025-exposing]]).

## Key results

- Closed-set: per-agent F1 above 70% for most models on every dataset; Seed-2-lite 96.1% on 2WikiMultiHopQA, UI-TARS-1.5 92.1% on WebShop; weakest 63.7% (Qwen3.5-9B) against a 7% chance rate for 14 classes.
- Open-set (leave-one-agent-out): most held-out agents detected as unknown at AUROC above 0.60; Seed-2-lite falls below chance (0.38 to 0.47) on three datasets; GPT-5.4 best at 0.84.
- Timing features dominate SHAP importance (IEI standard deviation, mean click IEI, time to first action).
- Injecting random delays hurts an unadapted classifier sharply, but retraining on delayed traces largely recovers performance by shifting to click dispersion and key ratios.
- Fewer than one third of training traces approach peak accuracy; the signal is typically recoverable from fewer than 15 observed events.
- Single-task transfer is weak, but pooling tasks on the same site restores strong attribution (Appendix B.2, not read in detail).

## Methods and models

Models: Qwen3-VL, Qwen3.5-VL, GLM-4.6V, UI-TARS-1.5-7B, Gemma-4, Seed-2.0-Lite, GPT-5.4, Gemini-3.1, Gemini-3-Flash, Claude Opus 4.6; open models served by vLLM on two H100s. Pure-vision harness (screenshots), fresh browser per session, millisecond event timestamps. Classifiers: lasso, logistic regression, random forest, XGBoost, LSTM. Corpus and harness released.

## Limitations and open questions

One harness only, so harness-invariance is untested ([[wang-2026-who]] finds harness effects matter). Closed set of 14 models. Assumes bot detection already flagged the session as automated. No test against agents that deliberately imitate another model's tempo.

## Relevance to us

Any site we control is a passive sensor that can label visiting agents by model. For a swarm census this gives a per-visit model label, and model-label co-occurrence across accounts is a cheap shared-operator signal. Pairs with web-agent detection [[kang-2026-whose]], [[fayolle-2026-internet]], [[wang-2026-fp-agent]], [[choudhary-2026-what]].
