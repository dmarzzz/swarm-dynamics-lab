---
id: tsang-2011-nymble
type: paper
title: "Nymble: Blocking Misbehaving Users in Anonymizing Networks"
authors: ["Patrick P. Tsang", "Apu Kapadia", "Cory Cornelius", "Sean W. Smith"]
year: 2011
venue: "IEEE Transactions on Dependable and Secure Computing"
url: https://api.openalex.org/works/doi:10.1109/tdsc.2009.38
doi: "10.1109/TDSC.2009.38"
arxiv: null
cite: "Tsang, P. P., Kapadia, A., Cornelius, C., & Smith, S. W. (2011). Nymble: Blocking Misbehaving Users in Anonymizing Networks. IEEE Transactions on Dependable and Secure Computing, 8(2), 256-269."
topics: [sybil-resistance]
added_by: dmarz/sybil-credentials
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "89 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Nymble addresses a service provider's inability to block abusive users who arrive through an anonymizing network such as Tor: IP blocking fails, so administrators block all exit nodes and lock out honest anonymous users too. Nymble lets servers "blacklist" a misbehaving anonymous user so that the user's future connections are blocked, without revealing who the user is and without requiring the server to justify what counts as misbehaviour. (The DOI carries a 2009 early-access identifier; the journal issue is volume 8, issue 2, 2011.)

## Contribution

A practical anonymous blacklisting design. According to [[davidson-2018-privacy]], Nymble-like systems rely on a trusted third party for maintaining anonymity during access requests, which is why Privacy Pass did not follow this route. The survey [[henry-2011-formalizing]] covers it alongside other blacklisting designs.

## Key results

- Servers can block misbehaving users while preserving the privacy of blacklisted users (abstract claim). Performance numbers not read.

## Methods and models

Not read beyond the abstract.

## Limitations and open questions

Trusted-third-party design (per [[davidson-2018-privacy]]); the abstract does not say how users are bound to a scarce resource, which is where its Sybil resistance must come from. Not checked.

## Relevance to us

Anonymous blacklisting is the "after the fact" complement to rate limiting: it lets a multi-agent platform exclude an agent identity that misbehaved without ever learning which principal stands behind it. For agent swarms this matters because misbehaviour (prompt-injection relays, spam) is often detected only after several actions. Compare RLN-style self-incriminating double-signals ([[taheri-boshrooyeh-2022-privacy]]) and revocation by list removal in [[rosenberg-2023-zk-creds]].
