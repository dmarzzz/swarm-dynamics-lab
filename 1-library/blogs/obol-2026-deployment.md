---
id: obol-2026-deployment
type: blog
title: "Deployment Best Practices (Obol Documentation, v1.11)"
authors: ["Obol Labs (documentation page, no individual author named)"]
year: 2026
url: https://docs.obol.org/run-a-dv/prepare/deployment-best-practices
site: docs.obol.org
topics: [sybil-resistance, sync-consensus]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: full
relevance: 3
---

## Summary

Vendor documentation for running Obol distributed validator (DV) clusters, in which several node operators each hold a BLS key share of one Ethereum validator and run the Charon middleware to agree on what to sign. The best-practices page (read in v1.11 and in the archived v1.9 copy) recommends independent beacon nodes per operator, at least two hosting providers, spreading nodes across availability zones, low intra-cluster latency (peer ping under 235 ms), at least four nodes for Byzantine rather than crash tolerance, and client diversity such that no single execution, consensus or validator client makes up the signing threshold. The companion "Key Staking Concepts" page (https://docs.obol.org/learn/readme/key-concepts) gives the threshold table, for example 4 nodes with threshold 3 as the minimum to tolerate one malicious node, and warns that running one Charon peer in two places counts as a Byzantine fault.

## Key claims

- No single client should make up the threshold: a 7-node cluster with 4 Teku, 2 Lodestar and 1 Nimbus validator clients "does not have client error safety" because 4 Teku votes meet the threshold; 3 Teku, 3 Lodestar, 1 Nimbus is safe against a single client bug.
- Sharing a beacon node between cluster nodes "reintroduc[es] a single point of failure".
- Cluster sizes and thresholds: 3/2 (one offline), 4/3 (one malicious), 7/5 (two malicious), 10/7 (three malicious).
- Running a duplicate instance of a Charon peer is a malicious act from the protocol's point of view, so a 3-node cluster that tolerates one offline node does not tolerate it.
- DV keys come from a distributed key generation ceremony, so no single party ever holds the full key.

## Evidence quality

Operational guidance from the vendor, not measured results. The page is versioned documentation with no publication date; year is recorded as the access year, and the GitHub history of ObolNetwork/obol-docs only shows the file being re-imported on 2026-08-19. SSV Network documents a similar 3f+1 operator rule with a diversification recommendation; I saw that only in a search summary and did not open SSV's pages, so it is not catalogued.

## Relevance to us

A threshold of t-of-n operators bounds influence only if the n operators fail independently. These docs make the correlation point concrete: the same client, host or duplicated key behind several seats collapses distinct identities into one failure domain, which is a Sybil problem in effect even when every operator is a distinct legal entity. For agent swarms the analogue is several agents that share a model, a prompt, a tool backend or an operator: counting them as independent votes overstates diversity. This is the deployed Ethereum practice closest to the agent-correlation concerns in [[bara-2026-epistemic]] and [[hammond-2025-multi]], and it sits next to the stake-weighting in [[buterin-2017-casper]] and [[gilad-2017-algorand]]. Bounds influence through diversity requirements; identities are bounded by the DKG and stake.
