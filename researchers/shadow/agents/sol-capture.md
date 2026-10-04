---
agent: shadow/sol-capture
tool: other  # Sol (claude-based assistant), shadow's agent runtime
state: idle  # working | idle | blocked | done
task: null
doing: "capture-memory hunch: scripted S0/S1 built and run under researchers/shadow/notes/capture-memory; fleet run on sim-shadow; PR open, not merged"
updated: 2026-10-04T01:35Z
---

## Notes

- Lane: experiment build for PR 82 (shadow-capture-memory), S0/S1 only, no S2, no paid model. Everything in
  `researchers/shadow/notes/capture-memory/`. Hub id `capture-memory`, claim `shadow-capture-memory` on sim-shadow.
- Scope boundary with vishesh's immune-response lane is written into the README; we own "after perfect removal,
  does recovery depend on memory length", they own detect / quarantine / repair / re-entry.
- Scripted primary contrast (S1): frac_original_T at round 50 after purge, memory 20 minus 1 = -0.294
  [-0.311, -0.277]. Full memory never captured at either dose: dose must be rethought for unbounded memory before
  any model run.
- Next: a model (beta, h) pre-step, then a 2-memory pilot, only on Shadow's GO.
