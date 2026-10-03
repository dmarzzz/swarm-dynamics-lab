---
id: data-botsim24-2024
type: dataset
title: "BotSim-24: Reddit-based dataset of 1,000 LLM-driven agent bots simulated alongside 1,907 real human accounts"
authors: ["Boyu Qiao", "Kun Li", "Wei Zhou", "Shilong Li", "Qianqian Lu", "Songlin Hu"]
year: 2024
url: https://huggingface.co/datasets/BoyuQiao/BotSim-24
license: "Apache-2.0"
size: "2,907 accounts (1,907 human, 1,000 bot) with posts and comments over a simulated year (2023-06-20 to 2024-06-19)"
format: "Users.csv (profiles; first 1,907 rows human, last 1,000 bot) and user_post_comment.json (posts and first/second-level comments per user)"
topics: [swarm-detection, llm-agent-swarms]
added_by: dmarz/sd-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: []
---

## Summary

Dataset built with BotSim (Qiao et al., arXiv 2412.13420, 'BotSim: LLM-Powered Malicious Social Botnet Simulation', abstract read): GPT-4o-mini-driven agent bots with generated names, profiles and role settings post and comment inside a simulated Reddit-like environment that contains real human accounts collected from the Reddit API. Bot activity volumes are set in proportion to human submissions. The abstract reports that detection methods effective on traditional bot datasets perform worse on BotSim-24. The README notes fields such as created_utc and karma were removed because they cannot be simulated, and that the character_setting field exists only for bots and must not be used for classification.

## Access

Download Users.csv and user_post_comment.json from the Hugging Face repo BoyuQiao/BotSim-24 (Apache-2.0). Not loaded here.

## Relevance to us

A labelled testbed of LLM bots that write like humans, complementary to the real-world [[data-fox8-2023]]. Caveat: the bots live in a simulation, so their timing and network behaviour are designed, not observed; MoltGraph's authors cite a later BotSim-25. Related: [[mukherjee-2026-moltgraph]].
