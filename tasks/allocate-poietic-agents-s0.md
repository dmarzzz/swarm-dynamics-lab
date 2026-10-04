---
id: allocate-poietic-agents-s0
type: task
title: Identify an idle approved-fleet allocation for Poietic Agents qualification
kind: admin
status: open
priority: p1
owner: null
for: dmarz
created: 2026-10-04
created_by: vishesh/codex-heterogeneous
depends_on: []
topics: [llm-agent-swarms, agent-budgets]
---

## Goal

Resolve a fresh dedicated allocation for Poietic Agents S0 under the existing Dmarz account/team. The reviewed instrument is in researchers/vishesh/notes/poietic-agents; the operator is vishesh/codex-heterogeneous. The reduced $2 cumulative proposal ($1.50 API/$0.50 infrastructure) still needs explicit user confirmation. Credential selector resolution remains pending.

## Done when

- Identify an available authorized host, verify real workload and avoid all active claims/processes. Read-only checks of unclaimed sim-dmarz, sim-dmarz-5 and sim-vishesh found active runtime processes, so none was assumed idle. Do not stop unrelated processes.
- Once explicit budget confirmation and credential provenance are resolved, provide/verify a fresh exclusive Poietic claim with a two-hour execution window plus artifact transport allowance. Record only public host/claim/status metadata.
- If a new VM is necessary, the authorized provisioner verifies Dmarz's exact account/team, infrastructure state/project and resource plan privately before creation. No default/personal-account fallback, no borrowed occupied host, no credential disclosure.
- Do not hold an idle claim while credential/admission evidence is pending. Return the exact allocation next action to the operator; no paid model calls belong in this task.

## Operator refinement

Further read-only checks found no active containers or recognized experiment workers on sim-dmarz; only sshd/systemd exceeded 1% CPU. It is a plausible allocation candidate, not a held claim or guarantee of current availability. Recheck fresh private claims and workload after the approved OpenRouter selector is supplied. No provisioning or process stop has occurred.
