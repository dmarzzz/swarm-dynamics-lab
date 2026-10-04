---
agent: shadow/sol-capture
tool: other  # Sol (claude-based assistant), shadow's agent runtime
state: idle  # working | idle | blocked | done
task: null
doing: "capture-memory: PRs 82 + 83 merged to main; Q0 + S2_pilot (12 real-model episodes, 0.03 USD) done, results/S2.md on main; next = per-pair prior fit + model-side dose sweep, waiting on hypothesis review"
updated: 2026-10-04T05:00Z
---

## Notes

- Lane: capture-memory hunch under `researchers/shadow/notes/capture-memory/` (hypothesis shadow-capture-memory on
  main, status `proposed`, not accepted). Scripted S0/S1/S1b done. Hub id `capture-memory`.
- 2026-10-04 04:00Z: Shadow's GO for the costed pilot. Q0 (model qualification) validity 1.00 on the hub; S2_pilot
  queued and running: N 12, W1_INSIDE, memory 1 @ 0.42 and full @ 0.54 (scripted dose-rule doses carried over,
  labelled), arms A0/A1, 6 dev tasks x 1 seed. Four workers on shad0wbot (sim-shadow unreachable, port 22 refused;
  every other fleet box under an exclusive claim). No agentops claim held.
- Scope boundary with vishesh's immune-response lane unchanged: we own "after perfect removal, does recovery depend on
  memory length"; they own detect / quarantine / repair / re-entry.
- Next: results/S2_pilot.md + S2.md summary, post-mortem, hub analysis run, comment on PR 83.
