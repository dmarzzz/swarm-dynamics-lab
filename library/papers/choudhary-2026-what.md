---
id: choudhary-2026-what
type: paper
title: What Does It Take to Detect an AI Agent? Minimal Feature Sets for Behavioral Detection under Browser Automation
authors:
- Vishisht Choudhary
- Lukas Schmidt
- Anne Zoë Kenntner
- Feras Skhab
- Michel Osswald
- Jens Ernstberger
year: 2026
venue: North East AI Agents Day 2026 workshop (arXiv preprint)
url: https://arxiv.org/abs/2607.26935
doi: 10.48550/arXiv.2607.26935
arxiv: '2607.26935'
cite: Choudhary, V., Schmidt, L., Kenntner, A. Z., Skhab, F., Osswald, M., & Ernstberger, J. (2026). What Does It Take to Detect an AI Agent? Minimal Feature Sets for Behavioral Detection under Browser Automation. Accepted at the North East AI Agents Day 2026 workshop. arXiv preprint arXiv:2607.26935.
topics:
- swarm-detection
- llm-agent-swarms
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: full
relevance: 4
citations: null
code: []
---

## Summary

Choudhary, Schmidt, Kenntner, Skhab, Osswald and Ernstberger argue that agents are a third traffic class and test it on 14,000+ human CAPTCHA mouse sessions (CaptchaSolve30k), 5,000 synthetic bot sessions in three archetypes, and 1,025 real sessions of Claude driving Chrome through MCP/Playwright on ten web tasks. Binary human-vs-bot detectors let 39.1% (MLP), 34.5% (SAINT) and 30.0% (random forest) of agent sessions through as human. A three-class model detects every agent session in 30 runs. A five-level evasion ladder (Bezier paths, WGAN-GP trajectories, GAN plus jitter and Fitts timing, replay of real human cursor data; 2,299 evasion sessions) never evades it. Two features, mouse_event_rate plus click_duration_std or teleport_click_ratio, give 100% agent recall with precision 0.994 to 1.000.

## Contribution

Shows the separating signal under Playwright/CDP automation is an absence pattern in raw input events, not anything about LLM reasoning, and gives a minimal feature set by exhaustive search over 9,401 gradient-boosted models.

## Key results

- Measured: binary detectors miss 39.1% (MLP), 34.5% (SAINT), 30.0% (RF) of agents; XGBoost catches all but through missing-event features the authors call coincidental.
- Measured: three-class agent F1 = 1.000 across 3 model families x 10 seeds.
- Measured: 100% agent detection at all five evasion levels including human-trajectory replay (524 replay sessions).
- Measured: none of the four 'pause-think-act' timing features survive backward elimination; the necessary pair is mouse_event_rate and click_duration_std.
- Measured: the single 'perfect' feature cursor_path_linearity is degenerate (agent precision 0.33, macro-F1 0.17).

## Methods and models

SAINT tabular transformer with denoising pre-training, plus GBM, RF and MLP baselines; 70/15/15 splits, 10 seeds, Clopper-Pearson intervals. Features: 17 continuous behavioural and 7 binary environment features with missingness indicators. Evasion via rule-based paths, conditional WGAN-GP trained on 14,342 human segments, and KD-tree-warped human replay.

## Limitations and open questions

One agent (Claude) on one driver (Playwright); bots are synthetic Gaussian draws, so macro-F1 values depend on that simulation; human data comes from CAPTCHA solving, a different task from the agent tasks (the authors run a task-agnostic ablation to address this). The paper itself says OS-level input injection or hardware-backed input would sidestep the signal; that case is untested.

## Relevance to us

Useful negative and positive at once: CDP-driven agents are trivially flagged today, but the signal is an implementation artifact that a swarm operator can remove by injecting OS-level events, as the screenshot-plus-OS-input solver in [[salman-2026-captchas]] already does. Corroborates the cursor-teleport finding in [[wang-2026-fp-agent]].

## Notes from dmarz/sd-attribution

This lane catalogued the same source independently (added_by dmarz/sd-attribution, accessed 2026-10-03). Its distinct content:

- Frontmatter `venue` in this lane's version: North East AI Agents Day 2026 workshop; arXiv preprint
- Frontmatter `doi` in this lane's version: null
- Frontmatter `cite` in this lane's version: Choudhary, V., Schmidt, L., Kenntner, A. Z., Skhab, F., Osswald, M., & Ernstberger, J. (2026). What Does It Take to Detect an AI Agent? Minimal Feature Sets for Behavioral Detection under Browser Automation. arXiv:2607.26935.
- Frontmatter `read_depth` in this lane's version: abstract

### Summary

Argues that binary human-versus-bot detectors structurally misroute AI agents, and builds a three-class detector (human, bot, AI agent). Binary MLP and SAINT detectors misclassify 39.1% and 34.5% of real agents as human; adding an agent class gives agent F1 1.000 in 30 runs. Across a five-level evasion ladder including GAN trajectories and replayed human cursor data (2,299 sessions) there were zero agent misses, because Playwright does not emit the raw pointer-move and wheel-delta streams of physical devices. Two features (mouse_event_rate, teleport_click_ratio) give 100% agent recall.

### Contribution

Identifies the signal as a browser-automation absence signature, not evidence of reasoning, which says when detection will fail.

### Key results

- Binary detectors call 39.1% (MLP) and 34.5% (SAINT) of agents human (abstract).
- Three-class agent F1 1.000 across 30 runs; zero agent misses over 22,990 per-seed predictions under evasion (abstract).
- Two features reach 100% agent recall with precision 0.994; five features macro-F1 0.991 (abstract).

### Methods and models

Controlled benchmark; exhaustive search over feature subsets of size 1-5 (9,401 GBMs); evasion ladder.

### Limitations and open questions

The authors stress the signal is an automation artefact: agents driving real input devices or OS-level injection would not show it. Abstract-only reading.

### Relevance to us

A clear statement of what current agent detection actually keys on, and therefore of its expiry date. Related: [[wang-2026-fp-agent]], [[rmus-2026-process]].
