---
id: piatek-2007-incentives
type: paper
title: "Do incentives build robustness in BitTorrent?"
authors: [Michael Piatek, Tomas Isdal, Thomas Anderson, Arvind Krishnamurthy, Arun Venkataramani]
year: 2007
venue: 4th USENIX Symposium on Networked Systems Design and Implementation (NSDI '07), Cambridge, MA, pp. 1-14
url: https://www.usenix.org/legacy/events/nsdi07/tech/piatek/piatek.pdf
doi: null
arxiv: null
cite: "Piatek, M., Isdal, T., Anderson, T., Krishnamurthy, A., & Venkataramani, A. (2007). Do incentives build robustness in BitTorrent? In Proceedings of the 4th USENIX Symposium on Networked Systems Design and Implementation (NSDI '07), pp. 1-14. USENIX Association."
topics: [sybil-resistance, collective-decision]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "not available (no DOI; OpenAlex rate-limited at access time; the batch metadata lists 376)"
code: []
---

## Summary

The BitTyrant paper. BitTorrent's tit-for-tat (TFT) unchoking was widely credited with making the protocol robust to free riding. Using measurements of real swarms (client populations, upload-capacity distributions) the authors build a simple model relating upload to download rate and find that nearly all peers contribute bandwidth that does not improve their own download, i.e. there is large altruism, concentrated in a minority of high-capacity peers, and it is not a consequence of TFT. They then design BitTyrant, a strategic client that, without protocol changes, chooses which peers to reciprocate with and at what rate so as to maximise download per unit upload (estimating each neighbour's reciprocation threshold and ramping contributions just above it). On live Internet swarms a 1 Mbit/s BitTyrant client gets a median 70% download performance gain. In a 350-node PlanetLab swarm where every peer runs BitTyrant but still donates excess capacity, performance surprisingly improves; but when strategic peers withhold the excess, average completion time for a low-capacity peer goes from 314 s to 733 s and for a 100 KB/s peer from 108 s to 190 s, so universal strategic behaviour hurts the swarm. Related work notes Shneidman et al.'s Sybil-based manipulations of BitTorrent (one client presenting many identities to collect more optimistic unchokes) as a separate exploit class with "straightforward fixes". Read: abstract, introduction, the model and the evaluation sections (Figures 11-12 discussion), related work and conclusion; the BitTyrant implementation details skimmed.

## Contribution

Empirically refutes the folk theorem that TFT makes BitTorrent incentive-robust: performance rests on unrewarded altruism by a few high-capacity peers, and a rational client can capture it.

## Key results

- Median 70% download gain for a 1 Mb/s BitTyrant client on live swarms.
- All peers contribute non-performance-improving bandwidth (model + traces).
- Universal BitTyrant with excess capacity retained: faster swarm; with excess withheld: low-capacity peer completion 314 s -> 733 s, 100 KB/s peer 108 s -> 190 s.
- Sybil-style identity multiplication is acknowledged as an orthogonal attack on optimistic unchoking (via Shneidman et al.), not the one studied here.

## Methods and models

Trace-driven model of TFT reciprocation parameterised by measured upload-capacity distribution; BitTyrant client built on Azureus; evaluation on live swarms and on PlanetLab (350 nodes, 5 MB file, 128 KB/s seed capacity).

## Limitations and open questions

2007 BitTorrent client ecosystem; the "robustness" result is about bandwidth reallocation, not about identity. Whether the proposed fixes for Sybil unchoking abuse were adopted is not covered.

## Relevance to us

Context for the reciprocity-protocol branch of sybil-resistance: it shows that even before Sybils, a bilateral incentive mechanism that looks robust can rest on altruism that strategic agents harvest, and that the per-agent gain (70%) is on the same order as the 2x Sybil bound later proved for proportional response in [[cheng-2024-tight]]. Useful next to [[kash-2012-optimizing]] (scrip economies) and the Sybil-in-P2P framing of [[levine-2006-survey]] and [[urdaneta-2011-survey]]. For LLM agent economies the lesson is to measure who is actually subsidising the system before trusting an incentive design. Root: [[douceur-2002-sybil]].
