---
id: piotrowska-2017-loopix
type: paper
title: The Loopix Anonymity System
authors: [Ania M. Piotrowska, Jamie Hayes, Tariq Elahi, Sebastian Meiser, George Danezis]
year: 2017
venue: arXiv preprint (cs.CR)
url: https://arxiv.org/abs/1703.00536
doi: 10.48550/arxiv.1703.00536
arxiv: '1703.00536'
cite: Piotrowska, A. M., Hayes, J., Elahi, T., Meiser, S., & Danezis, G. (2017). The Loopix Anonymity System. arXiv:1703.00536.
topics: [fork-merge-security, sybil-resistance]
added_by: dmarz/fm-unlinkability
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: 200+ citing papers (Semantic Scholar citations endpoint returned 200 on one page, 2026-10-03)
code: [gh-nymtech-nym]
---

## Summary

Loopix is a message-based mix network that hides who talks to whom, and whether anyone is talking at all, against a global passive adversary plus some corrupt mixes and providers. Each message takes an independently chosen route through a stratified topology of Poisson mixes, where every hop delays it by an exponentially distributed, sender-chosen amount. Clients emit real messages, drop-cover messages and loop-cover messages that return to themselves, each as a Poisson stream, so their outgoing traffic looks the same whether or not they are communicating. Mixes also send loops to themselves and treat missing loops as evidence of an (n-1) blocking attack. A Python prototype on AWS handled about 225-300 messages per second per mix with under 1.5 ms processing overhead and second-scale end-to-end latency.

## Contribution

Showed that cover traffic plus continuous-time Poisson mixing gives strong unobservability against a global adversary at seconds of latency, with a tunable trade between delay, cover rate and real rate.

## Key results

- Poisson mix modelled as M/M/inf; mean messages in a mix follow Pois(lambda/mu) (Lemma 1); memorylessness means all messages in a pool are equally likely next (Theorem 1), and mix loops further dilute the adversary's linking probability (Theorem 2).
- Client sender unobservability is perfect against the GPA because traffic is always Pois(lambda_P + lambda_L + lambda_D) regardless of real activity; receiver unobservability holds with an honest provider that pads inbox pulls to a constant size.
- Simulated end-to-end anonymity (100 senders, lambda = 2): likelihood difference epsilon falls toward zero as lambda/mu rises (lambda/mu >= 2 recommended) and with 3 or more layers; epsilon grows with the percentage of corrupt mixes (Figure 7).
- Prototype: about 0.6 ms per packet, latency overhead rising by only 0.37 ms from 50 to 500 clients; end-to-end latency fits a Gamma distribution (mean 1.93 s at Exp(2) per-hop delay).
- Active (n-1) attacks are detected because an attacker cannot distinguish a mix's own loops from other traffic and so cannot block selectively without losing loops.

## Methods and models

Sphinx packet format; providers as first and last layer; analytic queueing results; Python simpy simulation for entropy and likelihood-difference metrics (50-100 runs); AWS EC2 prototype with 6 mixes in 3 layers and 4 providers serving about 500 clients.

## Limitations and open questions

Sybil attacks are excluded by assumption (providers vouch for users); corrupt providers weaken receiver unobservability and are left to future work; reliable delivery, replies and statistical disclosure over long periods are not analysed. Security depends on the ratio of traffic rate to mean delay.

## Relevance to us

Q1, and the closest engineering template. Loops are exactly what a fork-merge parent can use: it continuously emits decoy sub-agents or decoy return messages whose traffic is indistinguishable from real returns, so an observer cannot tell which return is real or whether any real return happened, and missing loops reveal an attacker who blocks all but one path to isolate the returning part (the network analogue of corrupting the channel so only the compromised sub-agent gets through). Costs are explicit: cover bandwidth and seconds of delay, consistent with the bound in [[das-2018-anonymity]]. Note the Sybil exclusion: if an attacker can spawn many fake sub-agents, the cover set is diluted, which ties back to [[douceur-2002-sybil]] and [[kleinstein-2025-sybil]]. Descends from [[chaum-1981-untraceable]]; contrasts with [[dingledine-2004-tor]]; deployed descendant [[gh-nymtech-nym]].
