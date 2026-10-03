---
id: chen-2026-captcha
type: paper
title: "CAPTCHA Solving for Native GUI Agents: Automated Reasoning-Action Data Generation and Self-Corrective Training"
authors: ["Yuxi Chen", "Haoyu Zhai", "Chenkai Wang", "Rui Yang", "Lingming Zhang", "Gang Wang", "Huan Zhang"]
year: 2026
venue: "ICML 2026 (accepted; arXiv preprint)"
url: https://arxiv.org/abs/2603.23559
doi: "10.48550/arXiv.2603.23559"
arxiv: "2603.23559"
cite: "Chen, Y., Zhai, H., Wang, C., Yang, R., Zhang, L., Wang, G., & Zhang, H. (2026). CAPTCHA Solving for Native GUI Agents: Automated Reasoning-Action Data Generation and Self-Corrective Training. Accepted to ICML 2026. arXiv preprint arXiv:2603.23559."
topics: ["swarm-detection", "sybil-resistance", "llm-agent-swarms"]
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 2
citations: "2 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Chen, Zhai, Wang, Yang, Zhang, Wang and Zhang train ReCAP, a native GUI agent (end-to-end VLM on screenshots) that solves modern interactive CAPTCHAs while keeping general GUI-agent skill. They build a dynamic CAPTCHA system with seven types, auto-generate large sets of solving trajectories with reasoning traces, and turn failed trajectories into self-correction data. ReCAP substantially improves CAPTCHA success over its base agents on synthetic and real-world test sets without losing general benchmark performance.

## Contribution

Shows CAPTCHA solving can be trained into a general computer-use agent rather than bolted on as a separate solver.

## Key results

- Measured (abstract): substantial CAPTCHA-success gains over base agents; numbers not in the abstract.

## Methods and models

Synthetic CAPTCHA environment, automated trajectory generation, self-corrective fine-tuning. Abstract only.

## Limitations and open questions

Abstract only.

## Relevance to us

Evasion-side result: future agents will ship with CAPTCHA skill built in, so the 'needs a dedicated solver' failure in [[ousat-2026-broken]] is temporary.
