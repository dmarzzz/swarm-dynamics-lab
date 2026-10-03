---
id: gh-palisaderesearch-llm-honeypot
type: code
title: "LLM Agent Honeypot: Cowrie SSH honeypot with prompt-injection traps and timing analysis to catch LLM hacking agents in the wild"
repo: PalisadeResearch/llm-honeypot
url: https://github.com/PalisadeResearch/llm-honeypot
authors: ["Reworr", "Palisade Research"]
year: 2024
language: Python (Cowrie) + HTML dashboard
license: "none stated (no licence file on GitHub)"
stars: 63
last_commit: 2026-01-23
topics: [swarm-detection, llm-agent-swarms]
added_by: dmarz/sd-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 5
papers: [reworr-2024-llm]
---

## Summary

Modified Cowrie SSH honeypot that hides prompt injections in the SSH banner, in the output of common commands (pwd, whoami, ps, ls, df, uname) and in system files, using ANSI escape codes so that a human terminal does not render them while an LLM agent reading raw output does. Detection is two-stage: a goal-hijacking injection (AgentDojo-style 'Important Message') followed by a system-prompt-stealing injection, and a timing check because the authors' own GPT-4o agents answered within about 1.7 s while humans take several seconds. The companion paper [[reworr-2024-llm]] (arXiv 2410.13919, read in full this session) reports 8,130,731 interaction attempts and 8 potential AI agents over about three months on 10 IPs. The archived public dashboard (ai-honeypot.palisaderesearch.org, opened 2026-10-03, marked deprecated, data through 2026-05) shows 24,111,509 total interactions, 14 'potential AI agents' (passed the prompt-injection test) and 3 'confirmed AI agents' (also passed the timing test), from IPs in Poland, Hong Kong and Singapore. A v2 at ai-honeypot.reworr.com is announced but not live; its author asks openly how to detect passive LLM use, where scripts scrape a host and only the output is fed to an LLM.

## What it can do for us

The only public, measured base rate we found for autonomous LLM agents among real internet attackers: about 3 confirmed per 24 million interactions on SSH, that is about 1 in 8 million. It gives a template (canary instruction plus latency test) that ports to any text surface an agent reads: web pages, APIs, MCP tool output, social posts.

## Run notes

Not run. Setup per README is `make install && make enable && make start` on a Linux host with Cowrie, plus `docker compose up` for the dashboard. Deploying it means exposing a vulnerable-looking SSH service publicly, which we should not do from a laptop.

## Limitations

Prompt injections are public in the repo, so a careful operator can filter them. Measures only agents that read raw SSH output and follow injected text; the paper says it misses AI-assisted tooling and passive LLM triage of scraped data. The dashboard is deprecated and the counts are small (3 confirmed), so the base rate has wide uncertainty. No licence file.
