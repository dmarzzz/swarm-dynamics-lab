---
id: sun-2007-ddos
type: paper
title: "DDoS Attacks by Subverting Membership Management in P2P Systems"
authors: [Xin Sun, Ruben Torres, Sanjay Rao]
year: 2007
venue: 2007 3rd IEEE Workshop on Secure Network Protocols (NPSec), Beijing, pp. 1-6
url: https://ieeexplore.ieee.org/document/4371618
doi: 10.1109/npsec.2007.4371618
arxiv: null
cite: "Sun, X., Torres, R., & Rao, S. (2007). DDoS Attacks by Subverting Membership Management in P2P Systems. In 2007 3rd IEEE Workshop on Secure Network Protocols (NPSec), pp. 1-6. IEEE. https://doi.org/10.1109/NPSEC.2007.4371618"
topics: [sybil-resistance]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "12 (Crossref, 2026-10-03)"
code: []
---

## Summary

Shows that malicious participants in a P2P system can turn its membership management into a reflector for large-scale DDoS against hosts that are not even in the overlay. The attacks exploit three common design choices: push-based membership dissemination (nodes accept and forward membership records they receive), the allowance of many distinct logical identifiers (DHT IDs) for the same physical identifier (IP address), originally added to accommodate hosts behind NATs, and weak or absent validation of membership information. An attacker injects records that map many logical IDs to the victim's IP, so ordinary peers flood the victim with protocol traffic. The significance is demonstrated on two mature deployed systems with contrasting membership designs, the DHT-based Kad network and the gossip-based End System Multicast (ESM) streaming system. Abstract only (IEEE paywalled, no OA copy); attack volumes and amplification factors are not visible from the abstract (the authors' later IMC/ToN work on Kad reports multi-Mbit/s floods from a single attacker).

## Contribution

Identifies many-logical-IDs-per-IP, a deliberate NAT accommodation, as the root enabler of P2P reflective DDoS, and demonstrates it on both structured and gossip-based membership protocols.

## Key results

- Membership subversion enables DDoS on non-participants in Kad and ESM (abstract; magnitudes not visible).
- Three enabling design choices named: push membership, multiple logical IDs per physical ID, weak validation.

## Methods and models

Protocol analysis and experiments on deployed Kad and ESM. Details not read.

## Limitations and open questions

Abstract-level read; 6-page workshop paper; mitigations (per-IP ID limits, membership validation via handshakes) are only implied.

## Relevance to us

The clearest statement that permitting many identifiers per physical endpoint, even for a benign reason (NAT), is what makes identity-based reflection attacks possible, which generalises directly to agent registries that let one operator or host register many agents without validation. Companion to [[steiner-2007-exploiting]] (same Kad DDoS vector measured) and [[davis-2008-sybil]]; eclipse relatives [[heilman-2015-eclipse]]; taxonomy [[urdaneta-2011-survey]]. Root: [[douceur-2002-sybil]].
