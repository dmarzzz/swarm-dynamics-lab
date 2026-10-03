---
id: malhotra-2024-setting
type: blog
title: "Setting Your Pet Rock Free."
authors: [Karan Malhotra (byline); credited creators ropirito, sxysun, socrates1024, karan4d, rpal_, dillonrolnick]
year: 2024
url: https://nousresearch.com/setting-your-pet-rock-free
site: Nous Research blog (built by Teleport/Flashbots and Nous Research team members)
topics: [sybil-resistance, llm-agent-swarms]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: full
relevance: 5
---

## Summary

October 2024 post describing TEE_HEE (@tee_hee_he), an LLM agent on X that is meant to have provably exclusive control of its own X account, its email account and an Ethereum key. The agent runs in an Intel TDX confidential VM under dstack [[zhou-2025-dstack]] with no root login or SSH. Inside the TEE a headless Chromium takes a Cock.li email account with no recovery options and the X account, changes both passwords to values generated in the enclave, removes the phone number, connected apps and other sessions, and then obtains an OAuth token for the agent loop, which tweets every 30 minutes. The Ethereum key is generated in the enclave and never leaves it. The TDX quote's user report data contains the X username, so a quote can only exist after the takeover; auditors compare the MRTD with a reproducible build from the public repository and Docker image. A timed release prints the credentials to the debug log 7 days after launch so the admin can recover the account. The post's slogan: "if your AI cannot prove its independence through attestation, you don't have an autonomous agent - you have a very sophisticated puppet."

## Key claims

- The property that gives an AI autonomy is "exclusive ownership" of accounts, achievable only with TEEs (the post argues not with FHE, MPC or zk).
- Chain of trust covers accounts, RAG memory and the agent loop inside the TEE; the foundation model is called through OpenRouter, which is trusted.
- Limitations stated: single machine that the operators can power off; not peer-to-peer.
- Credited to Teleport/Flashbots and Nous Research team members.

## Evidence quality

Engineering write-up of a live demo with code and an attestation quote published on GitHub (the agent repository tee-he-he/err_err_ttyl now returns "Repository access blocked" from the GitHub API, so I could not check it). No independent audit is cited. Security rests on TDX, which [[chuang-2025-teefail]] later showed can be forged with physical access.

## Relevance to us

This is the direct bridge from Flashbots TEE work to agent identity. It binds an agent's identity to an account takeover recorded in an attested code measurement, so it proves "no human holds these credentials" rather than "this is one agent". Three Sybil consequences: (1) the binding is per account, not per principal, so one operator can repeat the ceremony for many accounts at the cost of a CVM each; (2) the agent's keys are encumbered by design, so it cannot pass a complete-knowledge check [[kelkar-2024-complete]], which puts provable autonomy and anti-rental checks in direct conflict; (3) the 7-day release and the power switch mean the identity is leased from its operator for a known term, the same structure as the time-bounded sub-policies in [[austgen-2024-liquefaction]]. For swarms of LLM agents ([[bara-2026-epistemic]]), attestation of this kind can raise the cost of a human puppeting many agent accounts, but it does nothing against one operator launching many genuine autonomous agents.
