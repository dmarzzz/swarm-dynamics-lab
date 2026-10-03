---
id: data-swarmworld-2026
type: dataset
title: 'SwarmWorld paper data: event traces of 50-200 LLM agents discovering and exchanging material technologies in a shared simulated world (60 episodes)'
authors:
- lamm-mit
year: 2026
url: https://huggingface.co/datasets/lamm-mit/swarmworld-data
license: Apache-2.0
size: 60 analysed episodes (48 at 800 ticks, 12 at 3,200 ticks), about 8.4 GB
format: 'Compressed JSONL event traces (studies/*.jsonl.gz) with study manifests, metadata CSVs (studies, episodes, files), analyses, figures and a technology atlas'
topics:
- llm-agent-swarms
- swarm-intelligence
added_by: dmarz/hf-sweep
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers:
- pal-2026-swarmworld
---

## Summary

Data package for [[pal-2026-swarmworld]] (arXiv 2608.26081). Populations of N=50, 100 and 200 LLM agents (all using the same gpt-5.6-luna policy) share a world in which they build, test, teach, trade and fork programs for material technologies. 48 matched 800-tick episodes cover four conditions (full, no-explicit-culture, no-communication, independent-search best-of-N baseline) x three sizes x four seeds; 12 more N=100 episodes run 3,200 ticks with frozen portfolio checkpoints. Held-out seeds test the artifact portfolios without agents. Every isolated baseline trace is included.

## Access

https://huggingface.co/datasets/lamm-mit/swarmworld-data, not gated, Apache-2.0. Simulation engine repo (lamm-mit/SwarmWorld) may stay private until release.

## Relevance to us

One of the few released full action traces of 100+ LLM agents interacting, with ablations of communication and culture: good raw material for testing coordination-inference or swarm-signature methods. Agents "fork programs", which touches fork-merge questions only loosely.
