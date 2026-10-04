---
id: gh-rozbb-zkcreds-rs
type: code
title: "zkcreds-rs: Rust library for issuer-agnostic anonymous credentials from zkSNARKs"
repo: rozbb/zkcreds-rs
url: https://github.com/rozbb/zkcreds-rs
authors: ["Michael Rosenberg", "Jacob White"]
year: 2021
language: Rust
license: Apache-2.0 OR MIT (README; GitHub reports NOASSERTION)
stars: 74
last_commit: 2022-09-29
topics: [sybil-resistance]
added_by: dmarz/sybil-credentials
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: [rosenberg-2023-zk-creds]
---

## Summary

Code accompanying the zk-creds paper ([[rosenberg-2023-zk-creds]]): a Rust library (arkworks, Groth16) for designing anonymous credential systems with general-purpose zero-knowledge proofs, with a partial Python (PyO3/maturin) wrapper and a web demo. Benchmarks run with `cargo bench` (criterion) and write proof sizes to `proof_sizes.csv`; passport benchmarks need a JSON dump of a US passport made with the authors' Android passport-reader app.

## What it can do for us

Gives working gadgets for list-based issuance, rate limiting, linkable (per-context) pseudonyms and clone resistance, which are the building blocks for a per-principal, rate-limited anonymous agent identity in a swarm experiment.

## Run notes

Not run. README: `python3 -m venv .env && source .env/bin/activate && pip install maturin && maturin develop && python3 python-examples/web-demo.py` (README notes the Python wrapper is incomplete); `cargo bench` for benchmarks. Paper reports peak prover memory about 824 MB.

## Limitations

Research code, last commit September 2022. Groth16 requires per-circuit trusted setup. Passport benches are US-only.
