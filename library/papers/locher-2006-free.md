---
id: locher-2006-free
type: paper
title: "Free Riding in BitTorrent is Cheap"
authors: [Thomas Locher, Patrick Moor, Stefan Schmid, Roger Wattenhofer]
year: 2006
venue: 5th Workshop on Hot Topics in Networks (HotNets-V), Irvine, CA, pp. 85-90
url: https://conferences.sigcomm.org/hotnets/2006/locher06free.pdf
doi: null
arxiv: null
cite: "Locher, T., Moor, P., Schmid, S., & Wattenhofer, R. (2006). Free Riding in BitTorrent is Cheap. In Proceedings of the 5th Workshop on Hot Topics in Networks (HotNets-V), pp. 85-90. ACM SIGCOMM."
topics: [sybil-resistance, collective-decision]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "not available (no DOI; OpenAlex rate-limited at access time; batch metadata lists 240)"
code: []
---

## Summary

Presents BitThief, a BitTorrent client that never uploads a byte and still downloads whole files at competitive speed. Its tricks: re-announce aggressively to the tracker (asking for the maximum 200 peers, usually trimmed to 50) and use the DHT to collect far more peer addresses than normal clients, open connections to all of them, never announce any pieces, and fetch whatever any optimistic unchoke offers. On seven public torrents (31 MB to 798 MB, hundreds to ten thousand peers) BitThief is often faster than the official client, especially with many seeders and small files, and even when restricted to downloading only from leechers (no seeders) it still completes because optimistic unchoking from many leechers adds up. The sharing-communities section shows the opposite pressure also fails: private trackers that enforce sharing ratios rely on self-reported upload/download amounts in tracker announcements, so a client can announce bogus upload totals (the authors reach a sharing ratio of 1.4 on TorrentLeech without uploading a bit), and can also announce fake peers so the tracker's peer list fills with clients that do not exist, inflating seeder/leecher counts and slowing swarm starts; community swarms are additionally more generous to free-riders because members over-upload to protect their ratios. Uploading garbage data is noted not to help. Read: abstract, introduction, BitThief design, Table 1 and the seeder/leecher experiments, sharing-community exploits, discussion; related-work details skimmed.

## Contribution

Early demonstration that BitTorrent's piece exchange does not actually enforce reciprocity, and that the ratio-based social layer built on top is defeated by trivially faked self-reports and phantom peers.

## Key results

- Full downloads with zero upload across seven live torrents; faster than the official client in seeder-rich and small-file cases.
- Downloads succeed even when restricted to leechers only.
- Faked tracker announcements give a 1.4 sharing ratio with no uploads; fake peer announcements pollute tracker peer lists.
- Garbage uploads do not improve performance.

## Methods and models

Custom Java client (BitThief, released), live measurements in 2006 against mainline client as baseline; private tracker experiments.

## Limitations and open questions

Workshop-length measurement with a handful of torrents; 2006 protocol and tracker behaviour; no formal model. Suggested fixes (cross-checking announced totals across time and torrents, or distributed trackers) are sketched only.

## Relevance to us

The phantom-peer and fake-self-report findings are a small, concrete Sybil story: identities and contribution claims that nobody verifies get inflated as soon as they confer benefit, and the fix is independent verification rather than more reporting. Pairs with [[sirivianos-2007-free]] (large-view exploit) and [[piatek-2007-incentives]] (BitTyrant) as the three empirical refutations of BitTorrent incentive robustness, and with [[cheng-2024-tight]] for the later theory. For agent platforms that track reputation from self-reported activity, this is the cautionary precedent. Root: [[douceur-2002-sybil]].
