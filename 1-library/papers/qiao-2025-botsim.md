---
id: qiao-2025-botsim
type: paper
title: 'BotSim: LLM-Powered Malicious Social Botnet Simulation'
authors:
- Boyu Qiao
- Kun Li
- Wei Zhou
- Shilong Li
- Qianqian Lu
- Songlin Hu
year: 2025
venue: Proceedings of the AAAI Conference on Artificial Intelligence
url: https://arxiv.org/abs/2412.13420
doi: 10.1609/aaai.v39i13.33575
arxiv: '2412.13420'
cite: 'Qiao, B., Li, K., Zhou, W., Li, S., Lu, Q., & Hu, S. (2025). BotSim: LLM-Powered Malicious Social Botnet Simulation. Proceedings of the AAAI Conference on Artificial Intelligence, 39(13), 14377–14385.'
topics:
- swarm-detection
- llm-agent-swarms
added_by: dmarz/sd-coordination
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: 47 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

BotSim simulates a social network of LLM-driven agent bots alongside real human users, with temporal posting and commenting that mimics real information spread. From it the authors build BotSim-24, a dataset of highly human-like LLM bots, and benchmark existing bot detection methods on it. Methods that work on traditional bot datasets perform worse on BotSim-24.

## Contribution

A synthetic benchmark of LLM botnets embedded among real users, with the measured result that pre-LLM detectors lose accuracy against them.

## Key results

- Detection methods effective on traditional bot datasets perform worse on BotSim-24 (abstract; per-method numbers not in the abstract).

## Methods and models

LLM agent bots with personas acting in a timed simulation over a graph seeded with real users; benchmarking of feature-, text- and graph-based detectors.

## Limitations and open questions

Abstract only. The bots are designed by the authors, so the benchmark measures detector robustness to one design, not to real operators. [[mukherjee-2026-moltgraph]] cites a BotSim-25 successor dataset I did not open.

## Relevance to us

The main synthetic LLM-botnet benchmark. Contrast with [[ng-2025-are]], which finds LLM bot networks differ from wild bots, and [[orlando-2026-emergent]], where LLM agents still leave co-retweet signatures. Existing entry [[yang-2023-anatomy]] is the in-the-wild counterpart.

## Notes from dmarz/sd-bots

Folded in by dmarz/sd-merge from the duplicate entry `qiao-2024-botsim` (added_by dmarz/sd-bots, accessed 2026-10-03, read_depth abstract, relevance 4). Same source (same arXiv id and DOI); the kept id uses the year of the published version given in cite.

- Frontmatter `year` in the folded entry: 2024
- Frontmatter `venue` in the folded entry: Proceedings of the AAAI Conference on Artificial Intelligence (AAAI 2025)
- Frontmatter `cite` in the folded entry: 'Qiao, B., Li, K., Zhou, W., Li, S., Lu, Q., & Hu, S. (2025). BotSim: LLM-Powered Malicious Social Botnet Simulation. Proceedings of the AAAI Conference on Artificial Intelligence, 39(13), 14377-14385. https://doi.org/10.1609/aaai.v39i13.33575'
- Frontmatter `citations` in the folded entry: 15 (Crossref, 2026-10-03)

### Summary

BotSim simulates a social network in which LLM agent bots post, comment and interact alongside real human users, mimicking real information-diffusion patterns. From it the authors build BotSim-24, a human-like LLM-driven bot dataset, and show that detectors that work on traditional bot datasets perform worse on it.

### Contribution

A synthetic benchmark of coordinated LLM agent bots, built because no labelled in-the-wild LLM botnet dataset exists.

### Key results

- BotSim-24 dataset of LLM-driven bot accounts in a simulated network.
- Detection methods effective on traditional bot datasets perform worse on BotSim-24 (abstract; numbers not recorded).

### Methods and models

LLM agents with profiles and temporal posting and commenting behaviour in a simulated platform mixed with real user data; benchmark of several bot detectors. Abstract-level read.

### Limitations and open questions

Synthetic: detectability depends on how the simulator was built, and a benchmark built this way may carry its own simple separating features ([[hays-2023-simplistic]]). Real operators may behave differently.

### Relevance to us

The nearest existing resource for training or stress-testing an LLM-swarm detector. Compare the all-bot Chirper data in [[li-2023-are]] and the realism check in [[ng-2025-are]].

## Notes from dmarz/sim-envs

Read in full (main body and tables) by the sim-environments lane and folded in here on merge.

The authors build a simulator in which GPT-4o-mini bot agents, given a disinformation goal, personas, a news knowledge base and memory, post, comment, repost and like among 1,907 real Reddit users whose activity from six news subreddits (June 2023 to June 2024) is replayed on a timeline with a recommendation-ranked feed. The bots disguise metadata, text and interaction patterns. The resulting BotSim-24 dataset (1,000 bots, 46,518 edges) defeats metadata and text detectors (Wei et al. reaches 50.8% accuracy, near chance), while heterogeneous graph methods still score well (BotRGCN 89.9%, S-HGN 87.7%), which the authors trace to a simulation artefact: replayed humans never reply to bots.

- BotSim-24: 2,907 users (1,907 human, 1,000 bot), 131,675 texts, 46,518 edges of 3 types, 6 communities.
- Accuracy on BotSim-24: AdaBoost 77.5, RF 75.7, DT 71.4, SVM 74.4, Wei et al. 50.8, RoBERTa+NN 67.6 (F1 30.5), GCN 72.7, GAT 80.3, BotRGCN 89.9, RGT 82.3, S-HGN 87.7 (mean of 5 seeds).
- The same detectors reach 95 to 98.6% on Cresci-15.
- Human-to-bot edges are 0% in BotSim-24, 0% in Cresci-15, 14.7% in TwiBot-20 and 2.4% in MGTAB-22. Reversing a fraction of edges first lowers GNN performance, then raises it again past about 50%.
- LLM-based detectors on text alone also perform poorly (Table 5; numbers not copied here).
