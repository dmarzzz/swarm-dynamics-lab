---
id: gh-shadow-shadow
type: code
title: "Shadow: discrete-event network simulator that runs unmodified Linux binaries over a simulated network"
repo: shadow/shadow
url: https://github.com/shadow/shadow
authors: ["Rob Jansen", "Shadow developers"]
year: 2011
language: "Rust"
license: "BSD-3-Clause-style (NRL notice; GitHub reports NOASSERTION)"
stars: 1728
last_commit: 2026-09-30
topics: [sybil-resistance, swarm-detection, meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 5
papers: [jansen-2021-once, jansen-2022-co-opting]
---

## Summary

Simulates: IP networks (TCP/UDP, routing, latency and loss from a graph) carrying real application processes. Interaction model: conservative discrete-event simulation; unmodified Linux binaries are co-opted by syscall interposition so their clocks, sockets and randomness are simulated. Scale demonstrated: full-size Tor, 6,489 relays and 792k simulated users, needing 3.9 TiB RAM [[jansen-2021-once]]; the README promises thousands of processes on a laptop or server. LLM-driven: any process can be an agent, so an LLM agent binary can run inside, but its outbound API calls would need a simulated host, and wall-clock LLM latency breaks simulated time. Adversarial hooks: none packaged; Sybils are just more hosts in the YAML config, partitions and latency are edits to the network graph, Byzantine behaviour means running a modified binary. Weight: Linux-only build (Rust plus C), RAM-bound; not runnable on macOS. Maintained by the Shadow team (originated at the U.S. Naval Research Laboratory), active as of 2026-09-30.

## What it can do for us

The strongest substrate for running real P2P or agent binaries (Tor, Ethereum clients via [[gh-ethereum-ethshadow]], libp2p) in a deterministic, replayable network where we inject hundreds of Sybil hosts and measure eclipse or routing capture. Determinism means a fork-merge corruption bug found once can be replayed exactly.

## Run notes

Not run. Stars, licence and last commit from the GitHub API on 2026-10-03; README read via the API. Shadow is Linux-only (syscall interposition with seccomp and ptrace or shared-memory IPC), so it cannot be installed on the Mac; use orbital-one or a Linux VM.

## Limitations

Linux only. No built-in adversary library; every attack is a config plus a binary you write. Simulated time requires all I/O to go through Shadow, so agents calling external LLM APIs need a stub or local model process inside the simulation. Real-time ratio grows with load (Tor at 100% ran at 310x slower than real time per [[jansen-2021-once]]).
