---
id: influence-native-rerun
type: task
title: Run the revised procurement influence experiment
kind: build
status: claimed
priority: p1
owner: vishesh/codex-experiments
for: vishesh
created: 2026-10-03
created_by: vishesh/codex-experiments
depends_on: []
topics: []
updated: 2026-10-04T04:17Z
history:
- '2026-10-04T02:51Z released by vishesh/codex-experiments: Native Q0-Q3 attempts, measured replays and post-mortems published. Q2 fully valid but failed competence; Q3 diagnostic passed without opening comparison gate. Full fresh qualification and paired comparison require additional authorized budget. Dedicated claim released in agentops PR 64; no workers remain.'
- '2026-10-04T03:43Z released by vishesh/codex-experiments: Iteration 2 implemented and offline validated: 24 tests, 12/12 scripted decisions, zero paid calls. Q4 native run awaits additional authorized shared budget, review-influence-q4-dossiers and fresh exclusive fleet allocation. See scenario/ITERATION-02.md.'
claimed_at: 2026-10-04T04:17Z
---

## Goal

Implement native bounded collection, qualify the redesigned procurement study and run a paired comparison within the shared budget.

## Done when

- [x] Freeze and test native runner and fresh qualification cases.
- [x] Run qualification and diagnose any failures without replacing original outcomes.
- [ ] Run the eligible bounded comparison, publish measured replay and post-mortem, and release the dedicated allocation.

## Coverage note

Four native attempts published with immutable evidence, measured GIF/HTML replays and post-mortems. Q2: 9 valid, 7 acceptable; Q3: 3 valid deferrals on a targeted diagnostic, not full qualification. The comparison remains unrun pending fresh full qualification and more authorized shared budget. Dedicated worker is stopped; claim release requested. See scenario/RESULTS.md.

Iteration 2: fresh pull and PI feedback incorporated; four new Q4 dossiers, selected-deployment approval control, answer-label counterbalance, exact Q4 gate and missingness-aware paired analysis. 24 tests pass, 12/12 scripted decisions acceptable. No new model result. Native collection requires additional authorized shared budget, independent dossier review (review-influence-q4-dossiers), and fresh dedicated allocation. See scenario/ITERATION-02.md.
