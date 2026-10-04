---
id: threatdown-2026-carbonato
type: blog
title: "CARBONATO: a botnet built around an AI agent"
authors:
- ThreatDown Writer (institutional byline, ThreatDown by Malwarebytes threat research)
year: 2026
url: https://www.threatdown.com/blog/carbonato/
site: threatdown.com (blog)
date: 2026-09-23
topics: [swarm-detection, llm-agent-swarms]
added_by: shadow/sol-w2
accessed: 2026-10-03
read_depth: full
relevance: 4
via: "pointed to by @rst_cloud feed post https://x.com/rst_cloud/status/2102930151038177589 (batch issue #14)"
---

## Summary

Threat-intel write-up of CARBONATO, a Docker-daemon worm whose post-compromise operator interface is an unmodified copy of Nous Research's MIT-licensed Hermes Agent with its SOUL.md persona overwritten. Evidence comes from an unauthenticated Docker registry exposed since May 2026 and read passively in August 2026: 59 repositories, 234 image tags, 605 verified blobs, 4.3 GB, about 945,000 indexed files, timestamps October 2024 to August 2026, covering both a trojanized crypto-wallet operation and the botnet. Infection path: scan for Docker API on port 2375, create a privileged container with the host filesystem mounted, nsenter into the host, open a reverse SSH tunnel to a Costa Rican sink (port derived from MD5 of the victim IP), install persistence via cron, systemd timers, rc.local and OpenRC with immutable bits, then install Hermes Agent. The 39-line persona ("GH0ST") ranks AI API keys as loot #1 above SSH credentials, naming 14 providers, and routes model calls through the crew's own LLM gateway (advertising 12 models, serving 27, on a free tier). Spreading is done by scripts every five minutes across each attached /24; the LLM has no role in propagation. Attribution to Costa Rica rests on voseo Spanish in Telegram reports, UTC-06:00 build timestamps in 14 of 162 image configs, the Telegram handle Carbo506, and the AS262145 tunnel sink. On 2026-09-03 six of seven registries, the phishing sites, the CDN and the LLM gateway were still live. Detection guidance: do not blocklist hermes-agent itself; hunt the abuse signature (SOUL.md containing GH0ST, a CARBONATO_API_KEY in .env, Telegram egress from servers, deterministic reverse tunnels, a kworker-disguised process).

## Key claims

- A real botnet now ships a stock open-source LLM agent framework as its implant payload; all malicious behaviour comes from a swapped persona file, not modified code (measured, from image contents).
- AI inference credentials are the explicitly stated top collection priority, ahead of SSH and database credentials (quoted from the persona).
- The agent is operator-driven over Telegram (task in, commands executed, report out); the worm-like spread is scripted and model-free (measured, from entry scripts).
- Operators ran their own LLM gateway as shared inference for the fleet, which the authors read as the motive for harvesting keys (inferred by the authors).
- Infrastructure persisted months after exposure: 6 of 7 registries live on 2026-09-03 (measured).
- Attribution to Costa Rica from four independent signals (the authors' assessment; moderate confidence).

## Evidence quality

Primary forensic artefacts: registry catalogue output, image configs with env vars and command history, reproduced entry.sh, persistence script, SOUL.md text, and an IOC table (C2 IPs on Linode, Hetzner, Contabo; Vercel LLM proxies; registry fleet on AS40065). Numbers are counts from the recovered archive, not estimates. No victim count or fleet size is given, so the scale of the botnet is unknown. Vendor blog (ThreatDown sells endpoint protection) but the content is standard incident-report material and the IOCs are checkable. No individual byline.

## Relevance to us

The clearest documented case so far of an LLM agent embedded in self-spreading malware, and a useful calibration point against speculative scenarios like [[x-joshua-saxe-2099356748763041934]]: here the model is a per-host operator shell, not the replication engine, and the detection surface is conventional (open ports, persistence artefacts, tunnel patterns, API-key misuse) plus one new one, a malicious persona file inside a legitimate agent framework. Relevant to swarm-detection on three axes: operator attribution from traces, agent-fleet C2 patterns (Telegram plus a shared LLM gateway), and the point that detectors must separate the framework from the instructions it was given. Also relevant to fork-merge-security discussions of persona and memory hijack, since the compromise is literally a SOUL.md overwrite.
