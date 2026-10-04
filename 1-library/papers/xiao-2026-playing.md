---
id: xiao-2026-playing
type: paper
title: "Playing Along: Learning a Double-Agent Defender for Belief Steering via Theory of Mind"
authors: [Hanqi Xiao, Vaidehi Patil, Zaid Khan, Hyunji Lee, Elias Stengel-Eskin, Mohit Bansal]
year: 2026
venue: arXiv
url: https://arxiv.org/abs/2604.11666
doi: null
arxiv: "2604.11666"
cite: "Xiao, H., Patil, V., Khan, Z., Lee, H., Stengel-Eskin, E., & Bansal, M. (2026). Playing along: Learning a double-agent defender for belief steering via theory of mind. arXiv preprint arXiv:2604.11666."
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Read from the arXiv abstract. The authors define ToM-SB (Theory of Mind for Steering Beliefs), a privacy task in which a defender LLM acts as a "double agent": it engages an attacker who is trying to extract sensitive information and tries to make the attacker believe it has succeeded while giving it nothing true. Frontier models (Gemini3-Pro, GPT-5.4) often fail to fool attackers in hard scenarios where the attacker has partial prior knowledge, even with theory-of-mind prompting. Training defenders with reinforcement learning on fooling rewards, theory-of-mind rewards or both improves results, and the two abilities improve each other: rewarding fooling alone improves theory of mind and vice versa. Combined-reward defenders beat the prompted frontier models on hard scenarios and generalise to stronger, out-of-distribution attackers.

## Contribution

Turns the counterintelligence move of feeding an adversary false confirmation into a trainable LLM task with measured success.

## Key results

- Prompted frontier models struggle to fool attackers that hold partial prior knowledge (abstract claim; rates not read).
- RL-trained double-agent defenders outperform them; fooling success and theory-of-mind accuracy are well correlated across four attackers and six defender methods (abstract claim).

## Methods and models

ToM-SB benchmark, RL training with fooling and ToM rewards, in- and out-of-distribution attackers. Details not read.

## Limitations and open questions

Abstract only. The defender protects a secret in a dialogue; it is not a sub-agent being turned and later merged.

## Relevance to us

Bears on Q1 and on the defender's side of Q3. A child sent into a hostile domain could be trained to "play along" when probed, giving an attacker the impression that it has been compromised or that it is the child that will return, while carrying nothing useful; this is the controlled-enemy-agent playbook in [[cowden-2014-pioneering]] run by the defender. It also cuts the other way: the same capability in an attacker-controlled child is what makes a turned child hard to detect at merge, because it can model the parent's checks and satisfy them. The measured result that partial prior knowledge makes fooling much harder suggests that what the attacker already knows about the parent's merge protocol is the key variable for Q1 hiding.
