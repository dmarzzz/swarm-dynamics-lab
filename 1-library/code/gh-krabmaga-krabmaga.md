---
id: gh-krabmaga-krabmaga
type: code
title: "krABMaga: Rust ABM engine re-engineering MASON, with Bevy visualisation, WASM, parallel and MPI features"
repo: krABMaga/krABMaga
url: https://github.com/krABMaga/krABMaga
authors: ["Carmine Spagnuolo", "Alessia Antelmi", "Matteo D'Auria", "Daniele De Vinco", "ISISLab, University of Salerno"]
year: 2021
language: Rust
license: "MIT"
stars: 224
last_commit: 2026-09-28
topics: [collective-motion, meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: ran
relevance: 4
papers: []
---

## Summary

One line: general discrete-event ABM in Rust (MASON's Schedule/Agent/State concepts; 2D/3D continuous fields with cell-bucketed neighbour queries, grids, networks); measured here about 3.5 to 3.8 million agent-steps/s for boids on one M1 Max core from 200 to 10,000 agents and 1.7M/s at 100,000 agents, roughly 340x Mesa; no LLM integration; no adversarial hooks (write another Agent type); light to run (cargo build --release, about 20 s first build).

Developed at ISISLab (University of Salerno), previously named Rust-AB. Examples live in a separate repo (krABMaga/examples: flockers, flockers_mpi, ants foraging, Schelling, Sugarscape, wolf-sheep-grass, virus on network, SIR with genetic-algorithm exploration, Bayesian forest fire). Features include Bevy-based visualisation, in-browser WASM builds, a TUI runner, parameter-exploration macros (including distributed MPI exploration) and a reproducibility check macro.

## What it can do for us

The fastest CPU option we actually ran: a 10,000-boid, 1,000-step run takes 2.9 s on one core, so 10^4 to 10^5 agent swarms with sweeps over attacker fractions are cheap on a laptop. Rust also makes it a reasonable host for an inspectable, deterministic core with LLM agents sitting outside (agents in Rust, policy calls batched out to Python or an HTTP model server).

## Run notes

git clone https://github.com/krABMaga/examples.git; the stock flockers main() calls simulate!, which opens a terminal UI and panics without a TTY ("Failed to initialize input reader"). I patched flockers/src/main.rs to read N, STEPS and SIDE from the environment and replaced the macro with a manual loop (Schedule::new(); state.init(&mut schedule); for _ in 0..step { schedule.step(&mut state) }) timed with Instant. cargo build --release -p flockers (krabmaga 0.6.2, 20.5 s). Runs 2026-10-03 on an M1 Max, serial build, density kept at 0.02 agents per unit area (side 100 for 200 agents), interaction radius 10: N=200, 100 steps 0.005 s (3.68M agent-steps/s); N=1000, 100 steps 0.026 s (3.79M/s); N=10,000, 1,000 steps 2.90 s (3.45M/s); N=100,000, 100 steps 5.92 s (1.69M/s). The parallel feature (cargo build --features parallel) was slower on this machine: 0.80M/s at 10k and 0.77M/s at 100k. Note get_neighbors_within_relax_distance returns everything in nearby buckets, not an exact radius filter, so this boids variant is approximate, and its rule weights differ from Mesa's; the about 340x figure versus Mesa's 10.8k/s is order-of-magnitude.

## Limitations

Small team and community. The default simulate! macro needs an interactive terminal. The parallel feature did not help on this workload. No built-in data collection as rich as Mesa's; plotting is via macros. Pre-1.0 API (0.6.x).
