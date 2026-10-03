---
id: gh-m1kuw1ll-mmasim
type: code
title: "MMASim: Mesa agent-based simulator of MEV-Boost builder bidding wars"
repo: M1kuW1ll/MMASim
url: https://github.com/M1kuW1ll/MMASim
authors: ["Fei Wu", "Thomas Thiery"]
year: 2024
language: "Python"
license: "MIT"
stars: 30
last_commit: 2025-02-19
topics: [sybil-resistance, marl-emergence]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: ran
relevance: 4
papers: [wu-2023-strategic]
---

## Summary

Simulates: one MEV-Boost auction slot in 10 ms steps: builders receive public (mempool) and private (exclusive order flow) value signals as Poisson processes and bid with Naive, Adaptive, Last-Minute, Stealth or Bluff strategies under global relay delay and per-builder latency, with random auction end. Interaction model: Mesa ([[gh-mesa-mesa]]) agent-based model, synchronous steps. Scale: 12 builders in the default run; the paper ran 10,000 auctions per setting. LLM-driven: no, but a new strategy class could call one. Adversarial hooks: strategic bluffing and cancellation are native strategies; no identity layer, so one operator running several builders (builder Sybils or collusion) must be added. Weight: 347-line main.py, Mesa 2.3.4 or older, seconds per auction.

## What it can do for us

The closest existing ABM to Flashbots' world: a base for "N LLM builders plus scripted builders" bidding experiments and for adding operator-controlled builder clusters to study collusion and Sybil bidding.

## Run notes

Cloned to /private/tmp/claude-501/-Users-halcyon/91c0102b-dec1-491c-bac9-3e6625d95c8f/scratchpad/simenv/MMASim. `uv pip install "mesa<=2.3.4" numpy pandas matplotlib scipy` in the shared venv, then `MPLBACKEND=Agg python main.py`. Default model Auction(N=4, A=4, L=4, S=0, B=0, rate_public_mean=0.082, rate_private_mean=0.04, T_mean=12, delay=1). Ran in 23 s wall (8 s CPU) and printed: winning agent 2, winning bid 0.03849 ETH, winner profit 0.00675, winner total signal 0.04523, winning bid time 1,199 ms (auction length 12 s in 10 ms steps), auction efficiency 0.842. runscript.py (batch sweeps to CSV) was not run.

## Limitations

Script, not a library: parameters are edited in main.py, plotting runs at import. Pinned to Mesa 2.x (Mesa 3 changed the API). One slot only; no relay, proposer or cross-slot dynamics.
