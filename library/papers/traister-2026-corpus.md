---
id: traister-2026-corpus
type: paper
title: A Corpus of Real Scam- and Spam-Call Conversations from an Active Voice-Agent Honeypot
authors:
- Ethan Traister
- Dennis Tsang Ng
- Siyu Zhang
- Huaiyu Guo
- Tommy Duong
- Tyler Wu
- Yuchen Zhou
- Xingyu Shen
- Jiaqi Wu
- Simiao Ren
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2609.29528
doi: null
arxiv: '2609.29528'
cite: Traister, E., Ng, D. T., Zhang, S., Guo, H., Duong, T., Wu, T., Zhou, Y., Shen, X., Wu, J., & Ren, S. (2026). A Corpus of Real Scam- and Spam-Call Conversations from an Active Voice-Agent Honeypot. arXiv preprint arXiv:2609.29528.
topics:
- swarm-detection
added_by: dmarz/sd-honeypots
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Seeds dedicated phone numbers into the lead-generation channels fraud operations harvest and answers inbound calls with a low-latency conversational agent playing a plausible target persona. Every call is recorded, transcribed and auto-labelled. In 53 days it captured 10,015 inbound scam and spam calls (6,601 with two or more turns), about 895 hours of audio and 328,869 turns from 5,665 originating numbers. About three in five substantive calls were predatory-but-legal lead generation and about one in seven an outright scam (949). The agent was recognised as non-human in only about 5% of engaged calls, and scam detectors trained on synthetic dialogue lost precision on real traffic.

## Contribution

An active LLM honeypot that holds conversations with operators at scale and measures how often the adversary notices it is talking to an AI.

## Key results

- 10,015 calls in 53 days; 6,601 multi-turn; 5,665 numbers; 949 scams (measured).
- Agent recognised as non-human in about 5% of engaged calls (measured).
- Human review agreed with the holistic label 75% of the time on the binary decision (measured).
- Detectors trained on published synthetic dialogue collapse in precision on real calls (measured).

## Methods and models

Seeded numbers; conversational voice agent; three-channel audio; per-turn latency telemetry; automatic labelling with human validation. Abstract-level read.

## Limitations and open questions

Abstract only; targets human-run (and possibly automated) call operations, not LLM swarms specifically.

## Relevance to us

Shows LLM honeypots can sustain long engagement with real adversaries (95% not detected), and that synthetic training data misleads detectors, a caution for swarm detectors trained on simulated swarms. Related: [[bridges-2025-sok]], [[sladic-2023-llm]].
