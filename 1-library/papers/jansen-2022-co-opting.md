---
id: jansen-2022-co-opting
type: paper
title: "Co-opting Linux Processes for High-Performance Network Simulation"
authors: ["Rob Jansen", "Jim Newsome", "Ryan Wails"]
year: 2022
venue: "2022 USENIX Annual Technical Conference (USENIX ATC 22)"
url: https://www.usenix.org/conference/atc22/presentation/jansen
doi: null
arxiv: null
cite: "Jansen, R., Newsome, J., & Wails, R. (2022). Co-opting Linux Processes for High-Performance Network Simulation. In 2022 USENIX Annual Technical Conference (USENIX ATC 22), 327\u2013350."
topics: [meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: [gh-shadow-shadow]
---

## Summary

Presents Phantom, a redesign of the Shadow simulator in which a discrete-event network simulator directly executes unmodified applications as ordinary Linux processes, combining process control, system-call interposition and efficient data transfer to bring the processes under simulated time. The abstract reports Phantom up to 2.2 times faster than the earlier Shadow, up to 3.4 times faster than ns-3 and up to 43 times faster than gRaIL on large P2P benchmarks, and comparable to Shadow on large Tor simulations.

## Contribution

The architecture that current Shadow uses: real processes instead of in-process plugins, making unmodified binaries (including Go and Rust clients) runnable in a deterministic network simulation.

## Key results

- Up to 2.2x faster than Shadow, 3.4x faster than ns-3 and 43x faster than gRaIL on large P2P benchmarks (abstract).
- Comparable to Shadow on large Tor network simulations (abstract).

## Methods and models

Not read beyond the abstract. Per the abstract: a discrete-event simulator plus Linux process control and system-call interposition.

## Limitations and open questions

Only the abstract was read; benchmark details, determinism guarantees and limits are not checked here.

## Relevance to us

Explains why [[gh-shadow-shadow]] can host real Ethereum clients ([[gh-ethereum-ethshadow]]) or real agent binaries: emulation-level realism with simulation-level control.
