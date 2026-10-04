---
id: gh-juliadynamics-abmframeworkscomparison
type: code
title: "ABMFrameworksComparison: CI-run benchmark of the same ABMs (WolfSheep, Flocking, Schelling) in Agents.jl, Ark.jl, MASON, NetLogo and Mesa"
repo: JuliaDynamics/ABMFrameworksComparison
url: https://github.com/JuliaDynamics/ABMFrameworksComparison
authors: ["Timothy C. DuBois", "JuliaDynamics contributors"]
year: 2020
language: Julia, Python, Java, NetLogo
license: "none stated (GitHub reports NOASSERTION)"
stars: 27
last_commit: 2026-06-17
topics: [meta, collective-motion]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 4
papers: [datseris-2022-agents]
---

## Summary

One line: not a simulator but a benchmark harness; each model has a DECLARATION.md spec and one implementation per framework, run in CI with 100 reproducible seeds and the median time reported; latest table (Agents.jl 6.2.10, Ark.jl 0.5.1, MASON 22.0, NetLogo 6.4.0, Mesa 3.2.0) has Flocking-large time ratios 1.0 / 0.36 / 0.61 / 19.14 / 59.5 and Flocking-small 1.0 / 0.74 / 1.42 / 15.37 / 159.29; LLM and adversarial hooks not applicable.

Maintained by the Agents.jl developers but open to PRs from other communities. Lines of code are also tabulated (Flocking: Agents.jl 42, Ark.jl 137, MASON 159, NetLogo 82 (689 with GUI), Mesa 94). Ark.jl (ark-ecs/Ark.jl, Apache-2.0, 84 stars) is an archetype entity-component-system for Julia that now beats Agents.jl on every model in the table.

## What it can do for us

Gives us a fair, declared flocking benchmark to slot our own runs into, and the declaration-first method (spec file, same seeds, median of 100) is the right protocol for our own framework comparisons. Our krABMaga and AgentPy boids numbers ([[gh-krabmaga-krabmaga]], [[gh-jofmi-agentpy]]) are not on this harness, so they are only roughly comparable.

## Run notes

Not run. The README's route is bash runall.sh with julia, python, java, javac, bc and NetLogo on the path (Linux recommended).

## Limitations

Developer-run benchmark of their own framework; the README itself invites PRs that may speed up other implementations. Mesa column is Mesa 3.2.0, before mesa-frames. Only three models.
