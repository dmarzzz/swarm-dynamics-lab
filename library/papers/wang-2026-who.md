---
id: wang-2026-who
type: paper
title: "Who Is Behind the Harness? Fingerprinting LLMs through Agentic Behavior"
authors: ["Chuyi Wang", "Xiaohui Xie", "Tongze Wang", "Fangchen Luo", "Yong Cui"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2609.28559
doi: null
arxiv: "2609.28559"
cite: "Wang, C., Xie, X., Wang, T., Luo, F., & Cui, Y. (2026). Who Is Behind the Harness? Fingerprinting LLMs through Agentic Behavior. arXiv:2609.28559."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: null
code: []
---

## Summary

LIDAR identifies the LLM behind a coding agent from how it executes tasks rather than what it writes. Three paired coding probes (Verify, Recover, Resolve) each hold the repair goal fixed and change one condition, for example a transient test failure or a stale test that conflicts with the spec. Six trajectories form one fingerprint sample, turned into 958 behavioural fields and scored with a Jeffreys-smoothed count model. Over 36 models from seven families it reaches 95.13% Top-1 under OpenCode and 88.36% under mini-swe-agent.

## Contribution

First active black-box fingerprint for models inside agent harnesses, and shows that text-level fingerprints ([[pasquini-2024-llmmap]], [[gao-2024-model]], [[bruckner-2026-one]]) transfer poorly once a harness mediates output.

## Key results

- 36-model closed set: Top-1 95.13% / MRR 0.9736 (OpenCode), 88.36% / 0.9336 (mini-swe-agent); best mean in all six metric-harness comparisons.
- Under mini-swe-agent LIDAR beats the best baseline by 35.96 Top-1 points over MET and 28.09 MRR points; under OpenCode the margin over MET is 1.69 Top-1 points.
- Ablations: distribution-level features alone 89.81% Top-1, instance-level alone 75.00%, combined 93.52%; dropping Resolve costs 8.33 points.
- Provider-side manipulation on six close GLM/Qwen models: identity-obfuscation instructions cost LIDAR at most 11.11 Top-1 points; a forced output notice cost nothing; baselines lost up to 33.33 and 83.33 points.
- Trajectory organisation (ordering, repetition, backtracking) carries 50.6-53.6% (mini-swe-agent) and 67.8-70.5% (OpenCode) of the identity evidence; no single action dominates.

## Methods and models

Enrollment and query sets of 6 fingerprint samples per model-harness pair (36 trajectories each). Harness adapters map native events to shared action roles. Features: 756 instance-level per-variant fields plus 202 distribution-level mean and SD fields; latency, raw commands and self-reports excluded. Identifier: per-field state binning frozen on enrollment, Jeffreys half-count probabilities, average log-likelihood score.

## Limitations and open questions

Closed-set only; the open-set threshold is described but not evaluated. Requires running probes in the target agent, so it suits auditing a service, not observing strangers. An adaptive provider tuning a model to imitate trajectories is not tested.

## Relevance to us

Shows that agent behaviour, not just text, identifies the model, which matters when swarm members act through tools. The probe-pair idea (same task, one controlled perturbation) is reusable for a honeypot that hands visiting agents a transient failure and watches the recovery. Related: [[ediga-2026-trace]] (terminal command sequences), [[wang-2026-agentprov]] (tool-call distributions), [[lugoloobi-2026-known]] (UI traces).
