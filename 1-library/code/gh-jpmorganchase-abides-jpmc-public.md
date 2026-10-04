---
id: gh-jpmorganchase-abides-jpmc-public
type: code
title: "ABIDES (J.P. Morgan): ABIDES-Core, ABIDES-Markets and ABIDES-Gym multi-agent discrete-event market simulator"
repo: jpmorganchase/abides-jpmc-public
url: https://github.com/jpmorganchase/abides-jpmc-public
authors: ["J.P. Morgan AI Research", "Selim Amrouni", "Aymeric Moulin", "Jared Vann", "Svitlana Vyetrenko", "Tucker Balch", "Manuela Veloso"]
year: 2021
language: "Python"
license: "BSD-3-Clause (GitHub reports NOASSERTION)"
stars: 175
last_commit: 2023-12-13
topics: [meta, marl-emergence]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: ran
relevance: 4
papers: [byrd-2019-abides, amrouni-2021-abides]
---

## Summary

Simulates: a general multi-agent discrete-event kernel (ABIDES-Core), an exchange with limit order books and stylised trading agents (ABIDES-Markets), and OpenAI Gym wrappers for RL agents (ABIDES-Gym). Interaction model: agents communicate only through kernel messages with latency models; experimental agents can be driven step by step through Gym. Scale: the reference RMSC04 config has 1,117 agents (1,000 noise, 102 value, 12 momentum, 2 market makers, 1 exchange); we ran it on a Mac at about 67,500 messages per second. LLM-driven: not built in, but the Gym interface makes an LLM policy a drop-in experimental agent. Adversarial hooks: none native. Weight: pure Python but pinned to 2021 dependencies. Archived by J.P. Morgan.

## What it can do for us

A tested latency-aware message kernel plus a Gym bridge: the quickest route to "one adaptive (or LLM) agent among 1,000 scripted agents" experiments, which maps onto one LLM searcher among scripted searchers, or one Sybil cluster among honest traders.

## Run notes

Cloned to /private/tmp/claude-501/-Users-halcyon/91c0102b-dec1-491c-bac9-3e6625d95c8f/scratchpad/simenv/abides. The pinned requirements (pandas 1.2.4, numpy 1.22, gym 0.18, ray 1.7, pomegranate 0.14.5) do not install on this Mac. Path that worked: `uv venv -p 3.10`, `uv pip install "numpy<2" "pandas<2" scipy==1.13.1 coloredlogs tqdm psutil`, `uv pip install --no-deps -e abides-core -e abides-markets`. scipy 1.15.3 failed to load on Darwin 27 (dlopen error in _spropack), so scipy was pinned to 1.13.1. pomegranate 0.14.8 failed to compile with Cython, so a 15-line shim of GeneralMixtureModel.from_json().sample() (lognormal and normal mixture, used only for order sizes) was put on PYTHONPATH. Ran `PYTHONPATH=shim python run_rmsc04.py` (rmsc04.build_config(seed=0, end_time="10:00:00"); abides.run(cfg)). Result: 1,117 agents, 09:30 to 10:00 simulated in 1.4 s wall time, 57,958 messages at 67,545 messages per second, 5,060 L1 order-book snapshots; final best bid 99,916 at size 400. ABIDES-Gym was not installed (needs gym and ray).

## Limitations

Archived and dependency-rotted: ancient pins, needs a pomegranate shim on modern Python. Equity-market specific; no notion of blocks, mempools or identity.
