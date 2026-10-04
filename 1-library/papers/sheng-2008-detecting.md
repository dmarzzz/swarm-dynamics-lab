---
id: sheng-2008-detecting
type: paper
title: "Detecting 802.11 MAC Layer Spoofing Using Received Signal Strength"
authors: [Yong Sheng, Keren Tan, Guanling Chen, David Kotz, Andrew Campbell]
year: 2008
venue: IEEE INFOCOM 2008, The 27th Conference on Computer Communications, pp. 1768-1776
url: https://kotz.cs.dartmouth.edu/research/sheng-spoofing/
doi: 10.1109/infocom.2008.239
arxiv: null
cite: "Sheng, Y., Tan, K., Chen, G., Kotz, D., & Campbell, A. (2008). Detecting 802.11 MAC Layer Spoofing Using Received Signal Strength. In IEEE INFOCOM 2008, The 27th Conference on Computer Communications, pp. 1768-1776. IEEE. https://doi.org/10.1109/INFOCOM.2008.239"
topics: [sybil-resistance, swarm-detection]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "168 (Crossref, 2026-10-03)"
code: []
---

## Summary

MAC addresses in 802.11 are trivially spoofable, so an attacker can impersonate an access point or a station; received signal strength (RSS) is hard to forge and tracks transmitter location, so several earlier proposals used RSS profiles to tell the real sender from an impostor. Measuring RSS from typical 802.11 transmitters across a three-floor building instrumented with 20 air monitors (AMs), the authors find that RSS from a single legitimate transmitter is not unimodal but a mixture of several Gaussians, caused by antenna diversity in commodity cards, which breaks prior detectors that assume one RSS source per device. They therefore build per-transmitter RSS profiles as Gaussian mixture models and propose three detectors: local statistics at a single AM, combination of local decisions across AMs, and a global multi-AM detector. On the same testbed, at a 3% false positive rate the three detect 73.4%, 89.6% and 97.8% of spoofing attacks respectively. Abstract only (author's project page; the publisher PDF is not open and the Dartmouth digital-commons link returned HTML); testbed attack scenarios and attacker-victim separation assumptions are stated only qualitatively in the abstract.

## Contribution

Shows that the physical-layer identity signal everyone was using (RSS) is multimodal in practice because of antenna diversity, and gives a GMM-based detector that survives it, with multi-monitor fusion pushing detection near 98% at 3% FPR.

## Key results

- RSS of one transmitter follows a mixture of Gaussians (antenna diversity).
- Detection at 3% FPR: 73.4% (single AM), 89.6% (combined local), 97.8% (global multi-AM).
- Assumes attacker and victim are physically separated by a "reasonable distance".

## Methods and models

Passive air monitors (20) on three floors; GMM RSS profiles per MAC; hypothesis tests at single-AM and multi-AM levels. Details not read.

## Limitations and open questions

Abstract-level. Co-located attacker defeats RSS methods by construction; mobile transmitters need profile updates; 2008 hardware. The Sybil variant (one radio claiming many MACs) is the mirror image of the spoofing case studied here and should be detectable by the same profiles, but the abstract does not say so.

## Relevance to us

Part of the "physical network characteristics" family of Sybil and impersonation defences that [[urdaneta-2011-survey]] lists for P2P and that robotics later adopts in [[gil-2015-guaranteeing]] and [[gil-2018-resilient]]. Its specific lesson, that the fingerprint you rely on is itself multimodal and needs a mixture model, carries over to any "fingerprint the operator" approach to detecting agent swarms (timing, latency, writing style), which is why it is also tagged swarm-detection. Companion wireless work: [[yang-2013-detection]], [[xiong-2013-securearray]].
