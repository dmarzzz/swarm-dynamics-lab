---
id: gh-fabriziocafolla-openai-crawlers-ip-ranges
type: code
title: "openai-crawlers-ip-ranges: weekly-refreshed lists of OpenAI's published egress IPs (GPTBot, ChatGPT-User, OAI-SearchBot) plus nginx rules to block UA spoofers"
repo: FabrizioCafolla/openai-crawlers-ip-ranges
url: https://github.com/FabrizioCafolla/openai-crawlers-ip-ranges
authors: [FabrizioCafolla]
year: 2025
language: Shell
license: MIT
stars: 40
last_commit: 2026-09-28
topics: [swarm-detection]
added_by: shadow/sol-w1
accessed: 2026-10-03
read_depth: full
relevance: 2
papers: []
---

## Summary

Small repository by Fabrizio Cafolla (created 2025-01-21, MIT, 40 stars) that mirrors OpenAI's officially published IP prefix JSON files for its three web agents, `searchbot.json`, `chatgpt-user.json` and `gptbot.json` from openai.com, and flattens them into plain IP and CIDR text lists per bot and combined. A bash script (`openai/openai-get-ip-ranges.sh`, read in full) curls the three JSON files and extracts `.prefixes[].ipv4Prefix` with jq; commits titled "feat: update" land weekly (2026-09-14, 09-21, 09-28 seen). The README's motivation is that robots.txt does not stop requests carrying OpenAI user agents, either because OpenAI ignores it or because other bots spoof the UA, and it gives an nginx `geo` plus `map` config that returns 403 for any request claiming GPTBot, ChatGPT-User or OAI-SearchBot from an IP outside the official list. The combined CIDR file had 287 lines (281 unique; the per-bot lists overlap) at access, mostly /28 and /25 blocks in Microsoft Azure address space plus one /17 (9.129.0.0/17).

## What it can do for us

A ground-truth allowlist for attributing web traffic to OpenAI-operated agents, and the inverse, for flagging traffic that claims to be an OpenAI agent but is not. In a swarm-detection pipeline this is the "declared operator" baseline: requests from these ranges are OpenAI's own agent fleet (including ChatGPT agent sessions acting for users, the ChatGPT-User UA), while UA-claimed OpenAI traffic from elsewhere is impersonation. Steven Lim used the combined list in a Microsoft 365 KQL hunting query after the OpenAI wiki incident ([[x-0x534c-2096982209307816377]], [[x-openai-2096133504417616165]]). It is also a concrete example of IP-provenance attribution, which signed-request schemes such as [[gh-cloudflare-web-bot-auth]] aim to replace.

## Run notes

Not run. I downloaded `openai/openai-cidr-ranges-all.txt` with curl and counted lines (287 total, 281 after `sort -u`). The update script needs bash, curl and jq; `bash openai-get-ip-ranges.sh` in `openai/` regenerates all files from openai.com.

## Limitations

IPv4 only (the script extracts only `ipv4Prefix`). It only covers agents OpenAI runs from its own published ranges; any agent run by a third party on OpenAI models (API customers, Operator-style agents run elsewhere, research sandboxes) egresses from other IPs and is not covered. Combined files concatenate per-bot lists without deduplication. The upstream JSON is authoritative; this repo adds a weekly lag. Single maintainer.
