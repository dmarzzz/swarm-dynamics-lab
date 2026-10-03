---
id: gh-pmocz-activematter-python
type: code
title: "activematter-python: Philip Mocz's single-file Vicsek model (N=500, L=10, eta=0.5) from the 'Create Your Own Active Matter Simulation' tutorial"
repo: pmocz/activematter-python
url: https://github.com/pmocz/activematter-python
authors: ["Philip Mocz"]
year: 2021
language: Python
license: "GPL-3.0"
stars: 23
last_commit: 2025-05-08
topics: [collective-motion, active-matter]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: ran
relevance: 3
papers: [vicsek-1995-novel]
---

## Summary

A 60-line NumPy implementation of the standard 2D Vicsek model: N=500 particles, box L=10 with periodic boundaries, speed v0=1, interaction radius R=1, dt=0.2, Nt=200 steps, noise eta=0.5, each step aligning each particle to the mean heading within R and adding uniform angular noise, with a matplotlib animation. Accompanies a Medium tutorial. GPL-3.0, 23 stars, last commit 2025-05-08.

## What it can do for us

A readable reference implementation of exactly the model in [[vicsek-1995-novel]] to check order-parameter behaviour against, and a template for adding our own interaction rules (e.g. a shared-board analogue). The noise sweep below reproduces the ordered-to-disordered transition qualitatively.

## Run notes

git clone https://github.com/pmocz/activematter-python (HEAD 8149292). Script run_vicsek.py copies the update loop verbatim (plotting removed) and sweeps eta with seed 17, reporting the Vicsek order parameter va = |mean velocity| / v0 after 200 steps. Output 2026-10-03: eta=0.1 va=1.000; eta=0.5 va=0.985; eta=1.0 va=0.946; eta=2.0 va=0.793; eta=4.0 va=0.216. 5 runs x 500 particles x 200 steps in 10.1 s on CPU (the O(N^2) neighbour loop is pure Python over N).

## Limitations

O(N^2) Python loop, so N beyond a few thousand is slow; tutorial code, no tests; GPL-3.0.
