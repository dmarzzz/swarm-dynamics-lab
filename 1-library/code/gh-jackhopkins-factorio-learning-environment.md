---
id: gh-jackhopkins-factorio-learning-environment
type: code
title: "factorio-learning-environment: Factorio as an LLM-agent eval with lab-play, open-play and a multi-agent mode"
repo: JackHopkins/factorio-learning-environment
url: https://github.com/JackHopkins/factorio-learning-environment
authors: ["Jack Hopkins", "Mart Bakler", "Neel Kant", "FLE contributors"]
year: 2025
language: Python
license: "MIT (GitHub reports NOASSERTION; LICENSE file is MIT)"
stars: 1189
last_commit: 2026-09-06
topics: [llm-agent-swarms, agent-budgets]
added_by: dmarz/factory-scan
accessed: 2026-10-03
read_depth: skim
relevance: 5
papers: [hopkins-2025-factorio]
---

## Summary

Reference implementation of [[hopkins-2025-factorio]]: a Dockerised Factorio server cluster plus a Python SDK (pip install factorio-learning-environment) where agents act by submitting Python programs through a REPL tool API, with Gym registry, MCP server, and Inspect-based eval harness. Repo created 2021-06-19, 1,189 stars, 102 forks, last commit 2026-09-06 (Release 0.4.8), MIT LICENSE file (GitHub API shows NOASSERTION). Releases v0.2 (May 2025, Bakler, Kant, Hopkins) added multi-agent support, reasoning models and MCP.

## What it can do for us

Multi-agent mode exists, with evidence from the cloned code (main branch, 2026-10-03):
- fle/env/instance.py: FactorioInstance takes num_agents, builds one namespace per agent, keeps per-agent inventories, and is_multiagent is num_agents > 1; eval(expr, agent_idx) runs code as a given agent.
- fle/env/a2a_instance.py and fle/env/tools/agent/send_message/client.py: send_message(message, recipient=None) over the A2A protocol, broadcast or point-to-point; skipped in single-agent mode.
- fle/env/tools/admin/create_agent_characters: spawns several player characters on one map.
- fle/eval/tasks/task_definitions/multiagent/multiagent_tasks.py: three tasks, all 2-agent iron-plate throughput on a shared map: _free (cooperate, divide work), _impostor (one agent secretly told to sabotage without being caught), _distrust (both told the other may be an impostor).
- fle/eval/entrypoints/independent_run_a2a.py: runner for A2A multi-agent trajectories.
- docs/versions/0.2.0.html: "leverage Factorio's native multiplayer mechanics"; "agents fully yield to each other when planning and taking actions" (turn-taking, no true concurrency); positioned for "cooperation, conflict and collusion".
What is missing for the swarm factory: no market, prices, demand curve or per-agent profit. fle/env/utils/profits.py computes a production-value "profit" from production-flow deltas for one force, not a market price. tests/multiagent/test_messages.py is skipped at module level ("SimpleFactorioEvaluator and TrajectoryRunner classes have been removed"), so multi-agent test coverage is stale. Competitive tasks (separate forces, rival bases) are not defined; Factorio supports multiple forces natively, so they would have to be added.

## Run notes

Not run. Cloned with git clone --depth 1 and read the README, CHANGELOG grep, the multi-agent task module, instance, send_message tool, profits util and v0.2 release notes. Requires Docker for the headless Factorio server; Factorio 2.0.73+ client only for rendering.

## Limitations

Turn-based multi-agent (agents yield to each other); only cooperative/sabotage tasks with two agents; stale multi-agent tests; a full Factorio server per instance is heavy for many-firm sweeps; GitHub licence detection shows NOASSERTION despite an MIT LICENSE file.
