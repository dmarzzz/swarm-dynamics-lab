---
id: fbi-2024-state
type: blog
title: "State-Sponsored Russian Media Leverages Meliorator Software for Foreign Malign Influence Activity (Joint Cybersecurity Advisory AA24-191A)"
authors: [FBI, US Cyber National Mission Force, Netherlands AIVD, Netherlands MIVD, Netherlands Police, Canadian Centre for Cyber Security]
year: 2024
url: https://www.ic3.gov/CSA/2024/240709.pdf
site: IC3 / FBI joint cybersecurity advisory (government report, TLP:CLEAR)
topics: [swarm-detection, sybil-resistance]
added_by: dmarz/sd-informal
accessed: 2026-10-03
read_depth: full
relevance: 4
---

## Summary

Government advisory (9 July 2024) describing Meliorator, an "AI-enabled bot farm generation and management" package used by affiliates of Russian state media RT since at least 2022 to run fictitious personas on X targeting the US, Poland, Germany, the Netherlands, Spain, Ukraine and Israel. The tool's admin panel "Brigadir" has tabs for "souls" (persona identities generated from archetype parameters, with Faker-generated photos and bios, stored in MongoDB) and "thoughts" (automated scenarios: like, share, repost, comment, register, log in). The back end "Taras" orchestrates the bots. Three bot archetypes: full-profile bots with political bios that post most; near-empty bots used only to like; and personas built from data scraped by the Nemezida web crawler, made to look real with no AI ties, which gather followers and amplify. Evasion features: proxy IPs auto-assigned to match each persona's claimed country, automatic scraping of X email verification codes from the operator's own mail server (mlrtr.com, otanmail.com), uniform spoofed user-agent strings via a remote debugging port (9222), following mostly accounts with over 100,000 followers to blend in, and avoiding replies to DMs. Code references Facebook and Instagram, suggesting planned expansion. The advisory lists IPs, TLS certificate hashes and mail servers with first/last-seen dates, and recommends that platforms verify accounts are run by a human (KYC-like), harden verification, and review known-suspicious user agents.

## Key claims

- As of June 2024 Meliorator only worked on X.
- The bot farm was designed to evade detection at the account level (realistic profiles, geolocated proxies, selective following).
- The DOJ press release accompanying the advisory (cited in it; not opened this session) describes the domain seizures and account takedowns.

## Evidence quality

Government technical advisory with code screenshots and infrastructure indicators; based on access to the tool itself, which is unusually strong evidence. Does not say how the operation was first discovered, how many bots were active, or what share of the personas used LLM text generation (the "AI" here is mostly persona and photo generation plus automation).

## Relevance to us

A rare inside view of a production bot-swarm controller: identity generation, role specialisation (posters, likers, amplifiers) and an action scheduler, which is the same architecture an LLM agent swarm would use, with the LLM replacing the "thoughts" scripts (as in [[anthropic-2025-detecting]]). The infrastructure indicators (shared mail domains, shared certificates, shared user agent) are the kind of operator-level linkage that survives better than content-level detection.
