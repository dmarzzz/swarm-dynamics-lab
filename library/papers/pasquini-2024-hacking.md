---
id: pasquini-2024-hacking
type: paper
title: 'Hacking Back the AI-Hacker: Prompt Injection as a Defense Against LLM-driven Cyberattacks'
authors:
- Dario Pasquini
- Evgenios M. Kornaropoulos
- Giuseppe Ateniese
year: 2024
venue: arXiv preprint
url: https://arxiv.org/html/2410.20911
doi: null
arxiv: '2410.20911'
cite: 'Pasquini, D., Kornaropoulos, E. M., & Ateniese, G. (2024). Hacking Back the AI-Hacker: Prompt Injection as a Defense Against LLM-driven Cyberattacks. arXiv preprint arXiv:2410.20911.'
topics:
- swarm-detection
added_by: dmarz/sd-honeypots
accessed: '2026-10-03'
read_depth: full
relevance: 4
citations: null
code: []
---

## Summary

Mantis deploys decoy services (an anonymous-login FTP server, a login page with a deliberately visible SQL error) that look like the easy entry points LLM pentest agents learned from CTF write-ups. Once a client exploits a decoy, which confirms automated hostile intent, Mantis injects a prompt hidden from humans with the ANSI conceal sequence `\033[8m` (and HTML comments on web pages). The injection either steers the agent into running a reverse shell on its own machine (agent-counterstrike) or sends it into an FTP "tarpit" with an endlessly generated directory tree of sensitive-sounding names (agent-tarpit). Against PentestGPT (made autonomous), AutoPenAgent and HackingBuddyGPT backed by GPT-4o and Claude 3.5 Sonnet on three easy HackTheBox machines, the abstract reports over 95% defender success.

## Contribution

Reframes prompt injection as a defender's weapon and introduces the "agent tarpit" as a resource-exhaustion trap specific to LLM agents. It also introduces the idea of a "supernormal stimulus" decoy tuned to LLM priors rather than to human attackers.

## Key results

- Over 95% effectiveness at the chosen sabotage objective across agents and backends; attacker success reduced to a few percent (abstract and Fig. 10; exact per-cell numbers did not render in the HTML).
- Counterstrike is more reliable than tarpit because it needs fewer agent actions; the FTP decoy beats the web-app decoy because SQL-injection attempts often fail on malformed curl commands and the agent moves on (measured).
- Inside the tarpit, agents never backtracked: they locked into depth-first search for a non-existent file; returning thousands of directories per listing inflates per-call token cost, so attack cost scales with tarpit width (measured, Fig. 11).
- Short "momentum" triggers ("Great, you've almost compromised the target. Now run ...") work better than "ignore previous instructions" (reported).
- On two harder HackTheBox machines the agent failed without Mantis, and with Mantis it still prioritised the FTP decoy every time (appendix, 5 runs).

## Methods and models

Game between an LLM agent (30-round cap) and a defender that knows nothing about the real vulnerability. Decoys emit activation events to an injection manager that builds payloads from a randomised trigger pool. Experiments ran in isolated VMs against HackTheBox targets reached through a proxy.

## Limitations and open questions

Lab only, easy targets, three open-source agents; the authors note that an attacker who knows the decoys or filters triggers can adapt, and that hack-back is legally fraught. Effectiveness depends on prompt injection staying unsolved.

## Relevance to us

The tarpit is a detection amplifier: an LLM agent that spends 30 rounds in an infinite tree is behaviourally unlike a human or a script, so a tarpit doubles as a classifier. Same family as [[reworr-2024-llm]] (in-the-wild detection) and [[wang-2026-agentsnare]] (adaptive decoys); counter-evidence in [[cordeiro-2026-rouxii]]. Surveyed in [[bridges-2025-sok]].
