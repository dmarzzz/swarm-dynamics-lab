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

## Research question

Can a small reproducible NCA task reveal measurable failure and recovery regimes?

## Dossier design sketch

Carried over from the [interactive dossier](../swarm-ecology-dossier.html#nca-observatory). This is an unexecuted hunch, not an approved experiment. Counts and treatments below are planning choices; the lab’s survey and hypothesis review gates still apply.

1. First verify that usable code, model artifacts and dependencies are available; do not assume the new paper is immediately reproducible.
2. Pick one small maze or pattern task and reproduce a baseline before introducing damage.
3. Compare damaged and undamaged rollouts with explicit task scoring and visible local-state evolution.

## Measures

- Task success and recovery steps
- Effect of damaged fraction and location
- Compute used after perturbation
- Stability beyond the evaluated horizon

## Controls

- Use a documented pretrained model if available
- Distinguish reproductions from new experiments
- Match initial states and update randomness
- Report if training or weights differ from the source

## Minimum useful output

A reproducible small CA experiment with a perturbation inspector. Use older open examples if new artifacts are unavailable.

## Optional extension

Compare local rule systems and language-agent networks on a shared abstract task without claiming they are equivalent.

## Interpretation risk

Training infrastructure can consume the weekend. A reproduction needs a useful measurement or inspection contribution.

## Demo narrative

Perturb a functioning pattern or solution and show whether scored function returns.

## Review update October 3

A reproduction is a useful fallback but does not establish a new language-agent finding. Confirm runnable weights or code before selecting the project.

**Decision to resolve before promotion:** Can a controlled perturbation measurement add information beyond the existing growth-and-damage demonstration?

If the simple baseline explains the result, or the necessary evidence cannot be obtained, narrow this to a replication or park the hunch. A toy animation is not evidence that the proposed intervention works.

## Additional dossier sources

- [Reasoning with Neural Cellular Automata](https://arxiv.org/abs/2609.36126) — Local recurrent cells, asynchronous updates and visual reasoning experiments.
- [Mayalen Etcheverry: original NCA thread](https://x.com/mayalen_etc/status/2105701039148323258) — Author explanation of local communication and visual reasoning.
- [Andrew Davison on NCAs](https://x.com/AjdDavison/status/2105718855721181463) — Speculative architectural prediction; not a demonstrated replacement for transformers.
- [Growing Neural Cellular Automata](https://distill.pub/2020/growing-ca/) — Growth, persistence, damage and regeneration; interactive examples.

[All project briefs](README.md) · [Research updates](../background-readings-2026-10-03.md)
