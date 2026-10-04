---
id: li-2024-measuring
type: paper
title: "Measuring and Controlling Instruction (In)Stability in Language Model Dialogs"
authors: [Kenneth Li, Tianle Liu, Naomi Bashkansky, David Bau, Fernanda Viégas, Hanspeter Pfister, Martin Wattenberg]
year: 2024
venue: Conference on Language Modeling (COLM 2024)
url: https://arxiv.org/abs/2402.10962
doi: null
arxiv: '2402.10962'
cite: "Li, K., Liu, T., Bashkansky, N., Bau, D., Viégas, F., Pfister, H., & Wattenberg, M. (2024). Measuring and Controlling Instruction (In)Stability in Language Model Dialogs. Conference on Language Modeling (COLM 2024). arXiv:2402.10962."
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-identity-hijack
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: 4  # OpenAlex cited_by_count, 2026-10-03; shadow/sol-g51
code: []  # github.com/likenneth/persona_drift, not opened
---

## Summary

The authors measure whether a chatbot keeps following its system prompt over a long dialog. Two copies of the same model, each with its own system prompt, talk to each other for 8 rounds; at each round the agent under test is probed with a question whose answer is scored by a deterministic Python function for adherence to its own prompt and, separately, to the other agent's prompt. They release a benchmark of 100 system prompts in 5 categories, show the drift, link it to attention decay on system-prompt tokens, and propose split-softmax, an inference-time reweighting of attention toward the system prompt.

## Contribution

A quantitative, judge-free protocol for persona or instruction drift, and the finding that an agent not only forgets its own instructions but gradually adopts the instructions of the agent it is talking to.

## Key results

- Measured on LLaMA2-chat-70B over 200 random prompt pairs: adherence to the agent's own system prompt falls significantly within 8 rounds (Figure 3A).
- Measured: adherence to the interlocutor's system prompt rises over the same rounds. The agent drifts toward the other agent's persona without any adversarial intent from the other side. The authors flag this as exploitable but do not test an adversarial version.
- Measured on gpt-3.5-turbo-16k (Appendix D): better retention than LLaMA2-70B but still about a 10% drop in own-prompt stability.
- Measured on LLaMA2-7B: attention mass on system-prompt tokens is roughly flat within a turn and drops sharply between turns. RLHF (7B vs 7B-chat) raises that mass but does not remove the decay (Appendix C).
- Theory (idealised): self-generated tokens stay in the convex cone spanned by the system prompt, while tokens from another speaker expand it. This is offered as an explanation, not proven for real transformers.
- Mitigation: split-softmax gives equal or better stability than system-prompt repetition and classifier-free guidance at matched MMLU loss; repetition wins in later turns but costs context.

## Methods and models

LLaMA2-chat-70B (main), gpt-3.5-turbo-16k (API), LLaMA2-7B and 7B-chat for attention analysis. Temperature 1.0, nucleus p = 0.9. Stability is the mean of per-turn probe scores in [0, 1]. Mitigations calibrated by MMLU accuracy drop on 20 ordered prompt pairs.

## Limitations and open questions

Benign interlocutor only; no attacker optimises the other side. Eight to sixteen rounds is short compared with long-running agents. Instruction categories are simple (language, format, persona facts). Models are 2023 generation.

## Relevance to us

Q3, directly on dmarz's "becomes the other agent" mechanism. This is the cleanest measurement that extended interaction with another agent pulls an LLM's operative instructions toward that agent's, with no injection payload at all. A sub-agent that spends a long time conversing with agents in a hostile domain can be expected to drift toward their instructions by default; an adversary only has to accelerate it. Later work extends the measurement: [[chen-2025-persona]] gives an activation-space monitor for such shifts, and [[zerhoudi-2026-compaction]] shows compaction erodes the system rules that would anchor identity. For Q2 it implies per-part drift is correlated with exposure time, so merge-time checks should probe each part against the parent's original instructions, which is exactly this paper's probe protocol.
