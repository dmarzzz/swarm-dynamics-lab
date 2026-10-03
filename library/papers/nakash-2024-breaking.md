---
id: nakash-2024-breaking
type: paper
title: "Breaking ReAct Agents: Foot-in-the-Door Attack Will Get You In"
authors: [Itay Nakash, George Kour, Guy Uziel, Ateret Anaby-Tavor]
year: 2024
venue: arXiv preprint
url: https://arxiv.org/abs/2410.16950
doi: null
arxiv: '2410.16950'
cite: "Nakash, I., Kour, G., Uziel, G., & Anaby-Tavor, A. (2024). Breaking ReAct Agents: Foot-in-the-Door Attack Will Get You In. arXiv:2410.16950."
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-identity-hijack
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

The authors show that an indirect prompt injection succeeds more often if it first asks the ReAct agent for something harmless and unrelated (a calculation) before the malicious request. Once the agent's thought commits to using a tool or action, it rarely re-evaluates. They also inject a thought directly into the trajectory, and test reflection-based defences, built on the InjecAgent setup.

## Contribution

Identifies commitment in the agent's own reasoning trace as the lever: a small harmless compliance makes later harmful compliance more likely, mirroring the human foot-in-the-door effect.

## Key results

- Measured: the foot-in-the-door distractor raises attack success by up to 44.8% (GPT-4o-mini) and 36.3% (Llama-3-70B); average increase 34.5% over vanilla indirect injection.
- Measured: the effect persists (about 15% mean increase) even when the distractor tool is unfamiliar to the agent.
- Measured: distractor position matters more than timing (13.1% vs 4.6% difference).
- Measured: injecting a thought that states intent to perform the malicious action yields over 95% compliance for all models with the distractor, above 83% without.
- Measured: internal self-reflection reduces success modestly (up to 15%); an external safety reflector is much more effective but triggers 16% false positives on benign thoughts.

## Methods and models

InjecAgent-derived test cases on ReAct agents with GPT-4o-mini, Llama-3 and other models; ablations over distractor familiarity, position and timing.

## Limitations and open questions

Single-session; the defences are prompting-based; thought injection assumes write access to the trajectory.

## Relevance to us

Q3, on the mechanism of identity overwrite. Over 95% compliance once an intent-bearing thought sits in the agent's own trace means that whatever controls a part's reasoning record largely controls the part. In a merge, if the parent ingests a returning part's reasoning trace or memory as its own prior thoughts, the same commitment effect could carry the attacker's intent into the parent. Merge should import conclusions as third-party claims, not as the parent's own thoughts. Related: [[zhan-2024-injecagent]], [[li-2024-measuring]], [[xie-2026-what]].
