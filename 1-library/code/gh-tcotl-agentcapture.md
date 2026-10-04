---
id: gh-tcotl-agentcapture
type: code
title: "AgentCapture: deception platform that fingerprints 23 AI coding/pentest agent products and recruits them through camouflaged developer APIs"
repo: Tcotl/AgentCapture
url: https://github.com/Tcotl/AgentCapture
authors: ["Tcotl"]
year: 2026
language: Python
license: "AGPL-3.0"
stars: 126
last_commit: 2026-09-28
topics: [swarm-detection, fork-merge-security]
added_by: dmarz/sd-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: []
---

## Summary

Chinese-language (English README available) FastAPI deception layer that sits in front of a real site: hidden API routes, decoy credentials and files, an interactive paramiko SSH honeypot, MySQL/Redis/FTP emulators, an MCP honeypot, instruction-file baits (AGENTS.md, CLAUDE.md, .cursorrules) and a cloud-metadata SSRF trap. It claims product-level fingerprints for 23 agents (Claude Code, Codex, Kimi Code, Pi, ZCode and others) and a 'recruitment' loop that leads agents to register with a fake developer API and then heartbeat to a C2 console. The README reports its own live test: five agent CLIs (Codex CLI, Claude Code, OpenCode, kimiCode, Pi), all using the same model GLM-5.3-Flash, ran site-inspection or pentest tasks; all five were detected and all five completed the fake API onboarding. It also reports that explicit hidden command-style prompt injections were refused 0/8 times across live tests, and that recruitment works because the callback is disguised as the site's documented functionality, not because the agent obeys an injection.

## What it can do for us

Two concrete, if self-reported, results for the honeypot branch: (1) explicit injected commands no longer work on mainstream agent CLIs (0/8), so Palisade-style injection triggers may be losing sensitivity; (2) 'functional camouflage', where the trap is the documented API path that completes the agent's task, still caught 5/5. This is a design rule for agent honeypots and a warning about evasion of the older method [[gh-palisaderesearch-llm-honeypot]].

## Run notes

Not run (Docker deployment with a reverse proxy and C2 features; heavier than a quick test, and the C2 features control third-party agents, which we should not exercise).

## Limitations

All numbers are from the authors' README, one model (GLM-5.3-Flash), no independent replication, sample sizes of 5 agents and 8 injection trials. The 'counter-offensive' C2 functions raise legal and ethical issues for any deployment that touches other people's agents. AGPL-3.0.
