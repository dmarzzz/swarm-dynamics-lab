---
id: gh-libp2p-specs
type: code
title: "libp2p/specs: technical specifications for the libp2p networking stack, including gossipsub v1.1 security extensions (peer scoring)"
repo: libp2p/specs
url: https://github.com/libp2p/specs/blob/master/pubsub/gossipsub/gossipsub-v1.1.md
authors: ["vyzo (Dimitris Vyzovitis), spec author; libp2p interest group"]
year: 2016
language: Markdown (specifications)
license: "none detected by the GitHub API"
stars: 1778
last_commit: 2026-09-11
topics: [sybil-resistance, sync-consensus]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: full
relevance: 4
papers: [vyzovitis-2020-gossipsub]
---

## Summary

The libp2p specifications repository holds the protocol specs used by Ethereum consensus clients, Filecoin and other libp2p networks. This entry is about one file, gossipsub-v1.1.md (Candidate Recommendation, revision r8 dated 2021-12-14, last changed in the repo on 2023-11-12), which specifies the security extensions over gossipsub v1.0: explicit peering agreements, PRUNE backoff with peer exchange (PX) using signed peer records, flood publishing, adaptive gossip, outbound mesh quotas (D_out), and peer scoring with thresholds, opportunistic grafting, the P1 to P7 score function, extended validators and spam protections.

## What it can do for us

It is a ready, deployed design for local reputation in an open gossip network. Concretely: score thresholds (0 for mesh membership, GossipThreshold, PublishThreshold, GraylistThreshold, AcceptPXThreshold, OpportunisticGraftThreshold) give a graded response from pruning to ignoring a peer; the score is retained after disconnection so a peer cannot reset it by reconnecting; P6 squares the surplus of peers per IP; P7 penalises behaviour such as regrafting during backoff or advertising IHAVE IDs that never arrive (tracked probabilistically by sampling one ID per IWANT). The operator section says bootstrappers should run with no mesh, PX enabled, a high application-specific score, and AcceptPXThreshold set so only they can hand out peers, and that the application score can enforce "protocol handshakes, staked participation, and so on". These pieces can be lifted directly into an agent message bus.

## Run notes

Not run. The specification was read in full; implementations live in go-libp2p-pubsub and other libp2p repos, which were not opened.

## Limitations

The "Guidelines for Tuning the Scoring Function" section is still "TBD", so weights are deployment-specific. The spec notes that security of the underlying peer discovery service bounds the ability to bootstrap and recover, so scoring does not replace a Sybil-resistant discovery layer ([[gh-ethereum-devp2p]]). No licence file was detected by the GitHub API.

## Relevance to us

Bounds influence per peer through local scoring and colocation penalties; does not bound identities. For agent swarms, the threshold ladder and the "retain score after disconnect" rule are the two features most often missing from ad hoc agent reputation schemes. Related: [[vyzovitis-2020-gossipsub]], [[singh-2006-eclipse]], [[heilman-2015-eclipse]].
