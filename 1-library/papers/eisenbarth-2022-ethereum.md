---
id: eisenbarth-2022-ethereum
type: paper
title: "Ethereum's Peer-to-Peer Network Monitoring and Sybil Attack Prevention"
authors: [Jean-Philippe Eisenbarth, Thibault Cholez, Olivier Perrin]
year: 2022
venue: Journal of Network and Systems Management, vol. 30, no. 4, article 65
url: https://zenodo.org/record/7410868
doi: 10.1007/s10922-022-09676-2
arxiv: null
cite: "Eisenbarth, J.-P., Cholez, T., & Perrin, O. (2022). Ethereum's Peer-to-Peer Network Monitoring and Sybil Attack Prevention. Journal of Network and Systems Management, 30(4), 65. https://doi.org/10.1007/s10922-022-09676-2"
topics: [sybil-resistance, swarm-detection]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "26 (Crossref, 2026-10-03)"
code: []
---

## Summary

Measurement study of Ethereum's discv4 Kademlia-style discovery network with a Sybil angle. The authors build Crawleth, a crawler that enumerates the DHT (IPv4 only, 1M file-descriptor limit) and records IP, port, node ID (public key), geolocation and AS for every reachable node, running it continuously through September 2021 and again at the February 2022 node-count peak. Network-level findings: healthy churn and geographic spread, but strong concentration, with the top ten ASes hosting about 60% of nodes. Sybil-pattern findings: using a threshold of more than two node IDs per IP, September 2021 showed 7,780 unique IPs holding 396,963 unique node IDs, the heaviest single IP holding about 14,000 identities (over 10,000 for several), at a rate of 1,217 such IPs (21,942 IDs) per hour; in February 2022 9,500 IPs held 183,731 IDs and 13% of IPs held 75% of all node IDs, 69.2% of these aliases sitting in the top ten ASes. Only five /24 subnets exceeded their 10%-of-subnet threshold (214 nodes total). Node-ID prefix distribution matched the theoretical uniform curve (N ~ 439,561), so no large localized eclipse placement was visible, which the authors attribute to the DHT storing no data worth eclipsing. They cannot distinguish attack from misconfiguration or node-infrastructure providers but note either way it centralises the network. Proposed mitigation: a monitoring system that classifies suspicious nodes (multi-identity IPs, dense subnets, prefix clustering) by thresholds, a smart contract to publish revocation lists, and an third-party tool that makes clients drop connections to listed peers; tested on an Ethereum test network. Read: abstract, introduction, background on discv4 and prior Sybil/eclipse work (Steiner's KAD numbers, Marcus et al.'s eclipse countermeasures), crawler design, Section 6 suspicious-pattern analysis with all figures above, and the mitigation architecture; AS/geography sections skimmed.

## Contribution

First large-scale empirical census of identity multiplication in Ethereum's discovery layer, with concrete thresholds for flagging Sybil-like behaviour and a revocation architecture.

## Key results

- Sept 2021: 7,780 IPs with >2 node IDs holding 396,963 IDs; max ~14,000 IDs on one IP.
- Feb 2022: 13% of IPs hold 75% of node IDs; 69.2% of aliases in the top-10 ASes.
- No measurable eclipse-style prefix clustering; ID prefix distribution matches uniform.
- Mitigation validated on testnet (monitoring + on-chain list + client-side revocation).

## Methods and models

Custom DHT crawler, month-long and peak-period measurements, threshold-based anomaly classification, prototype revocation pipeline. Code status not stated in the parts read.

## Limitations and open questions

Cannot attribute intent (attack vs infrastructure providers); IPv4 only; thresholds hand-set; revocation via smart contract raises governance questions; discv5 and post-merge consensus-layer networks not covered.

## Relevance to us

Hard numbers for what "one entity, many identities" looks like in a live permissionless network today: tens of thousands of identities per IP are routine and mostly tolerated, which is exactly the baseline an agent registry should expect. The detection features (identities per source, subnet density, ID-space clustering) and the detect-publish-revoke loop are directly reusable for swarm-detection. Compare the KAD precedent [[steiner-2007-exploiting]], eclipse mechanics [[heilman-2015-eclipse]], Ethereum eclipse detection [[xu-2020-am]], and taxonomy [[urdaneta-2011-survey]]. Root: [[douceur-2002-sybil]].
