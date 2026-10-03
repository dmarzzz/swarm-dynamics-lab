---
id: google-2025-adversarial
type: blog
title: "Adversarial Misuse of Generative AI"
authors: [Google Threat Intelligence Group]
year: 2025
url: https://cloud.google.com/blog/topics/threat-intelligence/adversarial-misuse-generative-ai
site: Google Cloud Blog (GTIG threat report)
topics: [swarm-detection]
added_by: dmarz/sd-informal
accessed: 2026-10-03
read_depth: skim
relevance: 3
---

## Summary

Vendor threat report (29 January 2025) from Google's Threat Intelligence Group on how government-backed hacking (APT) and information-operations (IO) actors used the Gemini web app, found by correlating GTIG's existing tracking of these actors with Gemini prompts, reviewed by analysts with LLM assistance. APT groups from more than 20 countries used Gemini, Iran and China most. Iranian IO actors made about three quarters of all IO prompts; among China-linked IO, DRAGONBRIDGE made about three quarters of that activity. IO uses were research, persona and message creation, translation and localization, and reach: automating distribution, SEO and operational security. Russian IO actors asked about building AI chatbots and LLM developer tools. Google found only low-effort, unsuccessful jailbreak attempts using public prompts, and attempts to abuse Google products (Gmail phishing, account-verification bypass) failed.

## Key claims

- Generative AI gives threat actors productivity, "not yet the game-changer it is sometimes portrayed to be"; no novel capabilities observed.
- The overwhelming majority of misuse is using LLMs to accelerate tasks; directing an agent to take malicious actions was not observed in this period.

## Evidence quality

Vendor report; aggregate shares without absolute counts; attribution relies on GTIG's prior actor tracking, not described in detail. Skimmed: read the summary, jailbreak section, APT country summaries and IO section; skipped detailed APT case lists.

## Relevance to us

A third provider's view (after [[openai-2025-disrupting]] and [[anthropic-2025-detecting]]) that early 2025 state IO used LLMs for content, not for autonomous agent swarms. It is the baseline against which the later orchestration cases (Claude deciding bot engagement; [[anthropic-2025-disrupting]]) look like a step change. The method, joining known-actor infrastructure with model usage logs, is a detection route only model providers have.
