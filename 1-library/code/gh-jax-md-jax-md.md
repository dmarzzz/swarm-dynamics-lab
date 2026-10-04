---
id: gh-jax-md-jax-md
type: code
title: "JAX MD: differentiable, GPU-accelerated molecular dynamics in JAX, usable for self-propelled particle and active-matter simulation"
repo: jax-md/jax-md
url: https://github.com/jax-md/jax-md
authors: ["Samuel Schoenholz", "Ekin Dogus Cubuk", "Google"]
year: 2019
language: Jupyter Notebook
license: "Apache-2.0"
stars: 1464
last_commit: 2026-08-18
topics: [active-matter, collective-motion]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

A molecular-dynamics library written in JAX: spaces with periodic boundaries, neighbour lists, energy functions, integrators (NVE, NVT, Brownian, Langevin) and automatic differentiation through whole trajectories; runs on CPU, GPU and TPU. NeurIPS 2020 paper arXiv 1912.04232. Apache-2.0, 1.5k stars, last commit 2026-08-18.

## What it can do for us

The seed task asked for GPU particle simulation: with a custom force term and the Brownian integrator JAX MD can run tens of thousands of active particles and differentiate order parameters with respect to interaction parameters. Vicsek-style alignment needs a custom update since it is not a potential.

## Run notes

Not run. Metadata (stars, licence, last commit) taken from the GitHub API on 2026-10-03; README read via the API.

## Limitations

Not a swarm simulator out of the box; no alignment-rule primitives; JAX install and GPU drivers required for the advantage. Not run.
