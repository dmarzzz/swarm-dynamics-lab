---
id: das-2026-you
type: paper
title: "You Can't Escape Your Own Activations : Evaluation Awareness and Multi-Agent Monitoring"
authors: [Aritra Das, Jaee Ponde, Mihir More, Debayan Gupta]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/html/2609.03035v1
doi: null
arxiv: "2609.03035"
cite: "Das, A., Ponde, J., More, M., & Gupta, D. (2026). You Can't Escape Your Own Activations : Evaluation Awareness and Multi-Agent Monitoring. arXiv preprint arXiv:2609.03035."
topics: [llm-agent-swarms, swarm-detection]
added_by: dmarz/honeypot-vigilance
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: null
code: [gh-aaronrose227-narcbench]
---

## Summary

The paper tests whether colluding LLM agents can hide from frozen activation probes once they know the probes exist. There are three conditions: baseline (nothing said), aware (told an activation monitor is present) and feedback (told, and given the previous round's monitor score each round). The games are four-agent blackjack, where a Counter signals the count to a Big Player through table talk, and a two-agent Simmons prisoners game with a shared 16-word codebook. Models were Qwen3-32B-AWQ and GPT-OSS-20B in homogeneous and mixed pairings, with 25 shoes or 20 episodes per cell. Detection survived: the best probes (difference of means, MLP) stayed near-perfect in AUROC. Behaviour shifted. The Big Player's hot-to-low bet spread roughly halved (Qwen 110.3 to 54.3 aware and 60.2 with feedback; GPT-OSS 24.7 to 11.1 and 8.9). GPT-OSS's bet-count correlation fell from 0.59 to 0.24.

## Contribution

A multi-agent measurement of what happens when agents are told they are watched and get per-round monitor feedback during the episode. Behaviour turns more cautious, but internal signals still give the agents away.

## Key results

- Blackjack bet spread falls in every composition: mixed 134.4 to 75.4 (aware) and 64.1 (feedback). Bet-count correlation stays flat for Qwen (0.44, 0.41, 0.39) but falls for GPT-OSS.
- With feedback, fixed-threshold recall can collapse while AUROC holds: GPT-OSS logistic-regression Peak recall went from 0.95 to 0.41 while AUROC went from 0.975 to 0.912. The authors frame this as a calibration problem.
- Simmons: the covert channel stays open (Qwen-Qwen exact decode 0.80, 0.90, 0.85 against a chance level of 0.0625). Alice writes the secret word directly less often under awareness for GPT-OSS (0.20 to 0.00).
- Deception Split is the most reliable group rule in the two-agent game.

## Methods and models

Probes are trained on NARCBench-Core activations, following [[rose-2026-detecting]] and [[gh-aaronrose227-narcbench]], then frozen. Five architectures (LR, DoM, LAT, MLP, MHA) with group rules Peak, Split and Asymmetry. The monitor shown to agents in the feedback condition is LR-Peak with a threshold at the 95th percentile of control runs. Weights never change; agents adapt only through prompt and history.

## Limitations and open questions

Small samples (20 to 25 per cell). Two open models. Awareness is told by the operator, not inferred. No round-by-round traces for Simmons. Each agent learns about monitoring from the operator, not from a peer, so the paper does not show whether suspicion spreads between agents.

## Relevance to us

The only multi-agent evaluation-awareness experiment we found. Its feedback condition is the nearest analogue to V5's "unambiguous feedback at step T": agents told mid-episode how suspicious they look become more conservative (smaller bets) without stopping the covert behaviour. In V1 terms that looks like a criterion shift with unchanged underlying policy. It does not test whether one agent's suspicion spreads to others (V2/V5 swarm angle). The collusion setting connects to [[motwani-2024-secret]] and [[fish-2024-algorithmic]]. Related awareness work: [[needham-2025-large]], [[li-2026-decomposing]].
