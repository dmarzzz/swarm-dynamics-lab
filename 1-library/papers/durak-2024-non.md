---
id: durak-2024-non
type: paper
title: "Non-Transferable Anonymous Tokens by Secret Binding"
authors: ["F. Betül Durak", "Laurane Marco", "Abdullah Talayhan", "Serge Vaudenay"]
year: 2024
venue: "Proceedings of the 2024 ACM SIGSAC Conference on Computer and Communications Security (CCS '24)"
url: https://eprint.iacr.org/2024/711
doi: "10.1145/3658644.3670338"
arxiv: null
cite: "Durak, F. B., Marco, L., Talayhan, A., & Vaudenay, S. (2024). Non-Transferable Anonymous Tokens by Secret Binding. In Proceedings of the 2024 ACM SIGSAC Conference on Computer and Communications Security, pp. 2460-2474. ACM. Full version: IACR Cryptology ePrint Archive 2024/711."
topics: [sybil-resistance]
added_by: dmarz/sybil-credentials
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "13 (Crossref, 2026-10-03)"
code: []
---

## Summary

Non-transferability (NT) means a credential can only be used by its intended owner. The paper notes NT had not been formally treated for anonymous tokens (lightweight anonymous credentials in the Privacy Pass family). It considers a client who "buys" access tokens that may be redeemed anonymously but must not be transferred, studies the trade-off between anonymity and security through NT, formalises new security notions, designs a suite of protocols with different flavours of NT (binding tokens to a client secret), proves them secure and implements them. It also argues that existing anonymous credentials with NT cannot be used directly as anonymous tokens without security and complexity costs. Found by forward citation chasing from [[davidson-2018-privacy]] (Semantic Scholar citations endpoint).

## Contribution

Targets the token-pooling ("hoarding") weakness that both the 2018 Privacy Pass paper and RFC 9576 ([[davidson-2024-privacy]]) flag: because plain tokens are bearer objects, many clients can hand theirs to one client.

## Key results

- Formal NT notions for anonymous tokens and a suite of constructions with proofs and an implementation (abstract). No numbers read.

## Methods and models

Not read beyond the abstract.

## Limitations and open questions

NT by secret binding discourages transfer by making it costly to share the secret; it cannot stop a principal from running many agents that all hold the same secret, which is a cloning question ([[camenisch-2006-how]]) rather than a transfer question. Not checked whether the paper discusses this.

## Relevance to us

In agent swarms, Sybil amplification often happens by pooling: many cheap accounts acquire tokens and one agent spends them. Non-transferable tokens are the direct countermeasure on the token side; paired with rate limits per secret ([[yun-2026-anonymous]]) they bound what any one principal's agent fleet can spend.
