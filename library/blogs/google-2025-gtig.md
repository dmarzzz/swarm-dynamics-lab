---
id: google-2025-gtig
type: blog
title: "GTIG AI Threat Tracker: Advances in Threat Actor Usage of AI Tools"
authors: [Google Threat Intelligence Group]
year: 2025
url: https://cloud.google.com/blog/topics/threat-intelligence/threat-actor-usage-of-ai-tools
site: Google Cloud Blog (GTIG threat report)
topics: [swarm-detection]
added_by: dmarz/sd-informal
accessed: 2026-10-03
read_depth: skim
relevance: 3
---

## Summary

Vendor threat report (5 November 2025) updating [[google-2025-adversarial]]. GTIG reports the first malware families that call LLMs during execution ("just-in-time" AI): PROMPTFLUX, an experimental VBScript dropper found in early June 2025 whose "Thinking Robot" module queries the Gemini API (hard-coded key, gemini-1.5-flash-latest) for antivirus-evasion code, and a variant that asks Gemini to rewrite its entire source every hour; PROMPTSTEAL, a Python data miner that queries Qwen2.5-Coder-32B-Instruct via the Hugging Face API for one-line Windows commands to collect files; a Go ransomware proof of concept that generates Lua scripts at runtime; a reverse shell with hard-coded prompts aimed at fooling LLM-based security analysis; and QUIETVAULT, a credential stealer that uses on-host AI CLI tools to hunt for secrets. Actors also use social-engineering pretexts in prompts (posing as capture-the-flag students or researchers) to get past safeguards, and an underground market for AI tooling matured in 2025. For IO actors, GTIG saw Gemini used for research, content and building tooling to automate workflows, but did not find the generated articles in the wild or evidence the automation worked.

## Key claims

- Malware that depends on a hosted model API carries a detectable and revocable dependency (API keys, model endpoints); Google disabled the assets.
- PROMPTFLUX appears to be in development or testing and could not compromise a victim at the time.

## Evidence quality

Vendor report with malware family descriptions; no sample hashes reproduced here and no prevalence numbers. Skimmed: read the summary, malware table and PROMPTFLUX section, plus the IO paragraph.

## Relevance to us

For swarm detection, the interesting point is the dependency: autonomous malicious agents that call hosted models expose themselves to the model provider (keys, prompt patterns), while those on open weights (PROMPTSTEAL via Qwen on Hugging Face) shift that vantage point to whoever hosts the weights. The IO finding (automation attempted, not observed working) is a negative data point for state IO agent swarms as of late 2025.
