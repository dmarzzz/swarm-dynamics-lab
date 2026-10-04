---
id: smedley-2023-searching
type: blog
title: Searching On MEV-Share
authors:
- Brock Smedley
- Shea Ketsdever
year: 2023
url: https://writings.flashbots.net/searching-on-mev-share
site: Flashbots Writings
topics:
- sybil-resistance
added_by: shadow/sol-w7
accessed: '2026-10-03'
read_depth: skim
relevance: 3
---

## Summary

This guide explains how searchers act on partially disclosed transaction hints instead of public signed transactions. The matchmaker fills transaction hashes into bundles, enforces inclusion and refund predicates, and limits builder access. Nested bundle composition enables collaborating searchers to extend each other's strategies, making the protocol a concrete example of constrained multi-party cooperation.

## Key claims

- The April 30 snapshot records 32,011 of 974,972 Ethereum transactions, 3.28%, originating from Protect.
- Default hints disclose a transaction hash and supported pool addresses, not transaction amount, direction, or signature.
- A composed bundle's permitted builders are the intersection of the lists chosen by its contributing users and searchers.

## Evidence quality

Vendor technical guide with API examples, open protocol specifications, client libraries, and example bots. This entry reads the guide only; bots, matchmaker enforcement, and real deployment guarantees were not tested. Adoption statistics are a historical snapshot.

## Relevance to us

Useful adversarial mechanism-design background: permissions combine by intersection at composition rather than expanding automatically. No Sybil authentication claim is made, and transaction addresses should not be confused with independent actors. Compare [[passerat-palmbach-2024-mitigating]] for encrypted computation instead of hints.
