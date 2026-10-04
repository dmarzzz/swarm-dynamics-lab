# Pre-run assessment s0-local-001

- Experiment / owner / stage: market-split / dmarz / exploratory scripted S0.
- Parent: first attempt. Status: ready.
- Question: can the market, controls, accounting and visual replay be trusted before API use?
- Expected: programmed registration can reduce firm HHI while owner HHI is unchanged. A negative search result is acceptable if controls work. Invalid accounting or missing visual artifacts is uninformative.

## Design and assessment

Use the frozen design and prospective protocol. Three policies paired on identical task/seed demand shocks; task is the cluster, not firm or frame. S0 has tasks 0–1, seed 11, 12 rounds, three regulator cells, fee 20 and threshold 0.38: 18 episodes. Holdout is untouched. Strongest comparator is exact ownership aggregation; no-regulator gross-profit parity checks resource conservation. The primary purpose is qualification, not a hypothesis test. Regulator rules are actor-visible; evaluator counterfactuals are not. One decision per owner per round, even after registration.

## Changes and unresolved issues

Initial template adaptation. No question-specific survey/hypothesis approval exists; only exploratory S0/S1 permitted. API discovery, model competence and power remain untested. Validate deterministic pairing, manual HHI/fines, treasury/capacity conservation, no-regulator parity, ownership negative control, high-cost deterrence, invalid-output preservation, leakage boundary and renderer transitions with `src/selftest.py` before this launch.

## Frozen execution plan

Commit this review and all protocol/source first. Exact source SHA, design SHA, prompt SHA, runtime and stage params accompany outputs. Run `python3 src/worker.py --local S0 --attempt s0-local-001` then analyze its combined JSONL. Dependencies: Python 3.9+, PyYAML, numpy, matplotlib and Pillow; versions captured in deployment record. One local worker, 18 episodes, 20-minute cap, 0 API calls, $0 cost, no credentials. No retries or favorable-result reruns; preserve partial traces and count invalids. If any gate fails, repair with a new pre-run assessment before fleet promotion.

## Visualization mapping

Use `visualization.md`, version market-split-v1, bound to each cell and its first preselected task 0/seed 11. Every round retained; 12 replay frames per cell, 1800×1200 final PNG and 1080×720 GIF. Verify registration at rounds 4/5, concentration gap, finance labels and failed-state renderer. Local output is `results/s0-local-001/`; fleet UI verification follows only after local qualification. The GIF's round cursor and final PNG substitute for unsupported scrub controls. Rendering never alters policy input or RNG. Raw traces survive render failure; missing artifacts block advancement.
