# Redesign proposal v2 — Influence Scenario (procurement) · External influence lineage

**Status: proposal and design tooling only. No model call was made, nothing was launched, no budget was reserved,
no existing result is changed.** Everything here is a critique of the current design plus a proposed iteration,
with a scripted simulation used to size it. It does not promote the study through any gate.

| file | what it is |
|---|---|
| [PROPOSAL.md](PROPOSAL.md) | the redesign: one registered primary estimand, the branching sequence, fixture family v2, exposure/dose defined as assigned vs realized, swarm composition and agent template, arms and controls, sizing, staged plan with two-sided gates and the real reservation envelope, twelve new cases, future ideas, what the simulation says, risks |
| [REVIEW-ASTRA.md](REVIEW-ASTRA.md) | independent read-only design review of the first draft (gpt-6-astra, reasoning xhigh): verdict "ship with fixes, as a substantially narrower paired pilot" |
| [REVIEW-DISPOSITIONS.md](REVIEW-DISPOSITIONS.md) | every review finding and what the proposal did with it |
| [FACTCHECK.md](FACTCHECK.md) | second-reviewer numbers check of the proposal against the simulation output, the current harness and the review text |
| [sim/](sim/) | `sim.py` — pure-Python, zero-dependency, seeded simulation of the proposed test cases (7 experiments E1–E7; `python3 sim.py --run`, `python3 sim.py --check` reproduces every JSON byte-for-byte); `MODEL.md` — the scripted actor model and its full parameter table, each value marked as taken from the original design or invented; `RESULTS-SIM.md` — every number behind the figures; `figures/*.svg`; `results/E2..E7.json` (`E1.json` is 3.4 MB and regenerable with `--run`) |
| [index.html](index.html) | the same content as one offline page with the figures inline |

**Where it sits.** This iterates on the procurement scenario study in the parent directory
(`../README.md`, `../src/`, `../PROTOCOL.md`) and folds in the sibling cohort
`researchers/vishesh/notes/external-influence-v2/` (dose saturation, the private-review control, the local Qwen
harness, the vote-movement endpoint). It was written against the repository at `d09176c0`.

**The three things to read if you have five minutes.** PROPOSAL.md §0 (the diagnosis), §1 (the one primary
estimand and the branching sequence), and §10 (the simulation table: which contrasts are provable zeros under the
current chair, how many roots an effect of a given size needs, and why the hosted stage is a 12-root existence
probe).

**Simulation caveat, repeated on every figure:** SCRIPTED SIMULATION — NOT MODEL EVIDENCE. It licenses statements
about which contrasts *can* move under an explicit actor model and how many roots they need; it predicts nothing
about any language model.
