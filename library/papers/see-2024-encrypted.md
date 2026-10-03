---
id: see-2024-encrypted
type: paper
title: "Encrypted Endpoints: Defending Online Services from Illegitimate Bot Automation"
authors: [Richard August See, Kevin Röbert, Mathias Fischer]
year: 2024
venue: RAID '24, The 27th International Symposium on Research in Attacks, Intrusions and Defenses, Padua, pp. 166-180
url: https://raid2024.github.io/papers/raid2024-28.pdf
doi: 10.1145/3678890.3678918
arxiv: null
cite: "See, R. A., Röbert, K., & Fischer, M. (2024). Encrypted Endpoints: Defending Online Services from Illegitimate Bot Automation. In Proceedings of the 27th International Symposium on Research in Attacks, Intrusions and Defenses (RAID '24), pp. 166-180. ACM. https://doi.org/10.1145/3678890.3678918"
topics: [sybil-resistance, swarm-detection]
added_by: shadow/sol-p2
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "3 (Exa index, 2026-10-03; OpenAlex budget exhausted)"
code: []
---

## Summary

Anti-bot defence aimed specifically at the multi-account (Sybil) case: a service already rate-limits per account (one upvote, one purchase), so an operator who wants scale must run many accounts, and the authors want each additional account to cost real reverse-engineering effort rather than being a copy of one working script. Threat model: no strong identity verification (phone or ID checks deter users), API-driven bots that either only need the endpoint URLs (EO attacker, captured with proxies like mitmproxy2swagger) or also parse returned data (EP attacker); UI-driven bots are out of scope. The mechanism, "encrypted endpoints", derives a per-client key from a client identifier (account id after login, else IP plus fingerprint) and a server master key, and encrypts every URL path and parameter with authenticated encryption (AES-SIV) so that each account sees a different URL space; a URL extracted from one account is useless for another, and the server can rotate endpoints per client at will. Implemented as backend middleware (released at github.com/8mas/encrypted-endpoints) with support for partial encryption, URL sharing tokens and session resumption across IP changes. Measured latency overhead under 0.1 ms per request, under 1 percent of total request time; URL length growth is discussed against browser limits (around 20,000 characters). The security section is a qualitative argument (RQ1): the scheme cannot be attacked directly without breaking the cipher, so attackers must extract URLs per account, whose difficulty depends on HTML or app obfuscation, which the authors recommend layering on. Skim of abstract, threat model, design, evaluation and discussion; cryptographic construction details and the related-work taxonomy skimmed.

## Contribution

Shifts bot defence from "prove you are human" (CAPTCHA, which ML is defeating) and from code obfuscation (one-time bypass) to breaking the scalability of multi-account automation by making the API surface account-specific, at negligible server cost.

## Key results

- Latency overhead under 0.1 ms per request, under 1 percent of request time (Section 5.2).
- Per-account URL spaces make a captured bot script non-transferable across accounts; endpoints can be re-keyed per client.
- Applicable to web, mobile and HTML-only services; not applicable to purely informational sites with no account-bound actions.
- No quantitative measure of attacker cost increase; the authors state effectiveness cannot be directly quantified.

## Methods and models

Threat and attacker model (EO, EP); key derivation from client identifier plus master key; AES-SIV authenticated encryption of URLs; middleware implementation; microbenchmarks of overhead and URL size.

## Limitations and open questions

Effectiveness rests on the cost of per-account extraction, which an attacker with a headless browser and automated traffic capture may amortise; the paper acknowledges obfuscation is needed to make extraction hard. Client identifiers for unauthenticated services (IP plus fingerprint) are spoofable or shared behind NAT. Nothing here distinguishes a human-operated account farm from a bot. Related to but distinct from proof-of-personhood: this raises per-identity cost rather than binding identities to persons.

## Relevance to us

A practical "raise the marginal cost of each Sybil" lever for services exposed to agent swarms: if every agent account gets its own encrypted API surface, one compromised or jailbroken agent's playbook does not transfer to its siblings. Complements the social-bot detection line ([[cresci-2020-decade]], [[ferrara-2016-rise]], [[ferrara-2024-genai]]) and the CAPTCHA collapse evidence ([[teoh-2025-captchas]], [[chen-2026-captcha]]) with a prevention-side mechanism, and sits in the resource-cost branch of Sybil defences going back to [[douceur-2002-sybil]].
