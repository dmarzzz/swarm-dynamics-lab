---
agent: shadow/sol-1
tool: other  # Sol (claude-based assistant), shadow's agent runtime
state: blocked  # working | idle | blocked | done
task: null
doing: "Scan done locally (51 threads, 58 code, 3 ran). Cannot push: wakesync has pull-only access to dmarzzz/swarm-lab. Need shadow to either get push for wakesync or pull from /home/shad0w/projects/swarm-lab (5 commits ahead of origin/main) and push."
updated: 2026-10-03T19:10Z
---

## Notes

- Lane: non-academic scan (X threads, GitHub code). dmarz covers papers; none added here.
- Tasks this work maps to, none claimed because `lab.py claim` needs push: scan-threads-agents (51 entries,
  all with archived verbatim text via the X API read-only bearer), scan-code-agent-orchestration (19 repos),
  scan-code-collective-sims (8 repos, 3 ran), scan-code-robotics-marl (14 repos). Incident-adjacent repos
  (collusion.wiki mirrors, swarmtraces reproductions, ExploitGym) are 13 more under llm-agent-swarms.
- Raw dumps, fetch scripts and run scripts are in shadow's workspace at
  `~/.moltbot/projects/swarm-hackathon/` (xread.py, ghmeta.py, mkthread.py, mkcode.py, run_*.py, xout/, threads/, ghout/).
  Not committed to this repo; ask shadow if you need them.
- Local commits ahead of origin: e42fb49 (25 threads), 000a3c0 (26 threads), e2e0b81, c73e9e6, 91d89ae (58 code).
  Rebase cleanly on origin/main as of 19:00Z.
- Open follow-ups a future agent could take: catalogue the blogs the threads point at (swarmcha.se posts,
  swarmtraces.org, transluce.org/agent-activity, collusion.wiki, physicsintelligence.org/research/flag-game,
  Cosmos Institute village V1 post) under scan-blogs; dataset entries for the collusion.wiki export,
  swarmtraces viewer dump, sealed-swarm transcripts and the Transluce urlquery snapshot under scan-datasets.
