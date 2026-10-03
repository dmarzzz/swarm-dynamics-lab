# nca-observatory

Status: HUNCH, not a hypothesis; no survey has passed the gate. Author's own triage, not a team ranking: Lift High · Difficulty Hard · Novelty Established concept · Event fit Exploratory · ~20–32+ builder-hours (estimate).

## Background

Neural cellular automata update cell states with a shared learned local rule. Their appeal is that growth and recovery can arise from repeated local computation. Classical cellular automata use specified rules and are a useful teaching baseline, but they do not reproduce a trained NCA.

## Closest prior work

- **Growing Neural Cellular Automata · 2020** — https://distill.pub/2020/growing-ca/  
  Includes interactive growth and damage experiments and runnable notebook links. A damage inspector alone would repeat an existing demonstration.
- **Reasoning with Neural Cellular Automata · 2026** — https://arxiv.org/abs/2609.36126  
  The paper behind the shared X thread connects local computation to reasoning tasks. Confirm code, checkpoints and the exact task before promising a reproduction.

## Where it applies

A reproducibility and perturbation workbench: vary damage location, asynchronous updates and runtime, then measure whether task function returns.

## The angle

Reproduce one released checkpoint and add a systematic perturbation sweep with saved seeds. If weights are unavailable, present the classical CA study under its own name.

## What to watch

The browser illustration below is a hand-specified cellular automaton, with no trained weights. Its behavior says nothing about the new paper’s accuracy.
