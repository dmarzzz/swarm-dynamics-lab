---
id: annessi-unknown-private
type: talk
title: MEV Roast | Private Searching on Private Transactions - Robert Annessi (Flashbots)
authors:
- Robert Annessi
year: unknown
url: https://www.youtube.com/watch?v=3vzOXOUMLpo
venue: Flashbots MEV Roast
topics:
- sybil-resistance
added_by: shadow/sol-w8
accessed: '2026-10-03'
read_depth: full
relevance: 5
---

## Summary

Annessi studies whether a user can keep a transaction secret while a searcher keeps its strategy secret. At 1:26-4:11 he shows why SGX isolation alone does not eliminate a malicious search program leaking through outputs, networking or resource-usage covert channels. At 5:21-8:38 an MPC proof of concept uses a restricted straight-line search language, comparisons and conditional release of a signed backrun to a builder. At 8:46-14:12 he walks through a Uniswap-v2 trade example. At 14:13-17:30 he reports approximately 40 hours and hundreds of gigabytes of communication for one transaction/strategy in the strongest tested setting, and proposes restricted SGX or specialized cryptography as future paths. Q&A narrows the guarantee: builders are trusted and receive the output; MPC does not magically make arbitrary outputs safe.

## Relevance to us

Useful containment example for untrusted subprograms: hidden inputs and attestation do not establish absence of deliberate exfiltration. The proof of concept is explicitly impractical, and trusted-builder assumptions exclude end-to-end secrecy. Publication year could not be verified from the reachable oEmbed metadata or blocked landing page.

## Reading notes

Read the entire timestamped transcript retrieved with yt_transcript.sh (Apify fallback). Automatic captions contain transcription errors; numerical claims below are attributed to the speaker, not independently replicated. 
