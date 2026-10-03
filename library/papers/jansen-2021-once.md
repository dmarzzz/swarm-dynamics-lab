---
id: jansen-2021-once
type: paper
title: "Once is Never Enough: Foundations for Sound Statistical Inference in Tor Network Experimentation"
authors: ["Rob Jansen", "Justin Tracey", "Ian Goldberg"]
year: 2021
venue: "30th USENIX Security Symposium (USENIX Security 21)"
url: https://arxiv.org/abs/2102.05196
doi: null
arxiv: "2102.05196"
cite: "Jansen, R., Tracey, J., & Goldberg, I. (2021). Once is Never Enough: Foundations for Sound Statistical Inference in Tor Network Experimentation. In 30th USENIX Security Symposium (USENIX Security 21). arXiv:2102.05196."
topics: [meta, sybil-resistance]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "24 (Semantic Scholar, 2026-10-03)"
code: [gh-shadow-tornettools, gh-shadow-shadow]
---

## Summary

The authors show that the standard practice in Tor performance research, one simulation per configuration in one scaled-down network sampled from the real Tor network, cannot support conclusions, because sampling error in building the network can produce the observed effects. They build a new Tor modelling pipeline (tornettools, TGen Markov traffic models, OnionTrace) and Shadow improvements, run the first full-scale Tor simulations (6,489 relays, 792k users, 3.9 TiB RAM, 8 days 6 hours), and give a method for confidence intervals across many independently sampled networks. A 420-simulation case study tests whether 20% more load slows downloads: at 1% scale the confidence intervals overlap even with 100 simulations, at 10% scale the effect is confirmed only with 100, at 30% it is clear with 5.

## Contribution

A statistical methodology for simulation studies of networks that are samples of a real system: treat each sampled network as one draw, run many, and report quantile-wise confidence intervals. It moves Tor experimentation from single-run comparisons to inference, and it applies to any Sybil or swarm simulation built on a synthetic population.

## Key results

- Full-scale Tor in Shadow: 6,489 relays and 792k users; at most 3.9 TiB RAM; 2 days 21 hours to bootstrap; real-to-simulated time ratio 310 in steady state (measured).
- At 31% scale, against the CCS 2018 state of the art: RAM 2.6 TiB down to 932 GiB (64% less), total run time down 33 days 12 hours (94%) (measured).
- Variation across independently sampled networks is much larger than across simulator seeds in one network (9 runs: 3 seeds in each of 3 networks at s = 0.1); the authors suggest each run use a fresh sampled network when compute is short.
- Confidence-interval width falls by more than an order of magnitude within the first ten or so sampled networks, with diminishing returns after (synthetic analysis, Figure 5).
- Case study (420 runs, scales 1%, 10%, 30%, load 1.0 vs 1.2): at 1% scale the point estimate even showed faster downloads under more load, but the CIs overlapped; the hypothesis was confirmed at 10% with n = 100 and at 30% with n = 5.

## Methods and models

Staging from one month of Tor consensus files (January 2019) into per-relay statistics (running, guard and exit frequencies, weights, bandwidths); generation at scale s with weighted sampling without replacement and bucketed median subsampling; clients placed by per-country user probability on a RIPE Atlas-derived Internet map (1,813 cities) with packet loss set to zero on core edges; TGen circuit, stream and packet Markov models from PrivCount measurements; process scale p = 0.01 so each client process simulates 100 users. Estimator: mean of per-network inverse CDFs at each quantile; error combines the mean per-network t-interval and the across-network standard deviation with a Student's t factor.

## Limitations and open questions

Packet loss model is admitted to be improvised and then zeroed. Clients run without guards because each process simulates 100 users. Results need machines with 1 to 4 TiB RAM for large scales. The method quantifies sampling error relative to the model, not model error relative to the real Tor network (validation is by comparing distributions to Tor metrics).

## Relevance to us

The main methodological lesson for any Sybil, swarm or market simulation here: one run on one synthetic population is a sample of size one. Build experiments as many independently sampled populations with confidence intervals, and prefer larger scale where affordable. Applies to [[gh-shadow-shadow]], [[gh-ethereum-ethshadow]], and to LLM-agent populations such as [[gh-camel-ai-oasis]] and [[gh-qqqqqqby-botsim]].
