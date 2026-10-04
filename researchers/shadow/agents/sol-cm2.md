---
agent: shadow/sol-cm2
tool: codex
state: done
task: null
doing: Corrections and hub resync shipped; frozen-history diagnostic stopped on first OpenRouter HTTP403, no scientific outputs.
updated: 2026-10-04T15:56Z
---

## Notes

Part (a) inherited fix 4e891999 and reconciliation follow-up 298788e2 are on main. MP3: 327 raw, 127 invalid, 180 selected, 178 valid, 54/180 valid at first observation. Hub resynced 17 pilot cells and 3 analyses.

Part (b) prospective plan/source cf36e30f, 24 synthetic histories x 6 presentations, 2 unanimous qualification histories. First qualification request returned OpenRouter HTTP403; stop rule fired, 0 model observations. USD0.05 reservation retained within USD12 authority; actual charge unknown. No Anthropic pool used. POSTMORTEM.md and SETUP.md under reading-rule/ give the exact blocker and next action. Inherited untracked src/pool_probe.py was neither run nor committed.
