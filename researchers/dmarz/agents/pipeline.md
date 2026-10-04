---
agent: dmarz/pipeline
tool: claude-code
state: working  # working | idle | blocked | done
task: null
doing: "Pipeline lead: keeps at least three launch-ready run requests prepared for dmarz's experiments (plan, code, offline tests, scripted stage, pre-run review, chained launcher); launches nothing and makes no model calls"
updated: 2026-10-04T07:51Z
---

## Notes

Sub-agent of dmarz/fleet-monitor on halcyon, started 2026-10-04. Builders dmarz/pipeline-scarcity and dmarz/pipeline-split each prepare one study. Ready packages are reviewed by dmarz/fleet-monitor (a same-researcher check, not an independent review) and then filed as run requests in the private agentops run queue. Notes and the ready-queue ledger live in researchers/dmarz/notes/pipeline/.
