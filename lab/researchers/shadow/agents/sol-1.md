---
agent: shadow/sol-1
tool: other  # Sol (claude-based assistant), shadow's agent runtime
state: working  # working | idle | blocked | done
task: survey-llm-agent-swarms
doing: "Survey complete and pushed (passes gate). Waiting on cross-researcher review (task review-llm-agent-swarms, for dmarz/vishesh). Next: hypotheses once reviewed; blog/dataset entries for swarmcha.se, swarmtraces, collusion.wiki if time."
updated: 2026-10-03T23:05Z
---

## Notes

- Lane: non-academic scan (X threads, GitHub code) done and closed: scan-threads-agents, scan-code-agent-orchestration,
  scan-code-collective-sims, scan-code-robotics-marl all `done` with coverage notes (gaps stated honestly: collective-sims
  9/15 repos, orchestration 0/3 ran, robotics-marl 1/3 ran).
- Survey llm-agent-swarms: complete, 16 search rounds, 60+ cites, 8 new papers added (pavlova-2026-flag read in full).
  Semantic Scholar 429'd all afternoon; used OpenAlex + arXiv export API instead.
- Raw dumps, fetch scripts and run scripts are in shadow's workspace at
  `~/.moltbot/projects/swarm-hackathon/` (xread.py, ghmeta.py, survey_search.py, arxiv_meta.py, survey_search/*.json).
  Not committed to this repo; ask shadow if you need them.
- Open follow-ups: catalogue the blogs the threads point at (swarmcha.se posts, swarmtraces.org, transluce.org/agent-activity,
  collusion.wiki, physicsintelligence.org/research/flag-game, Cosmos village V1 post) under scan-blogs; dataset entries for the
  collusion.wiki export, swarmtraces dump, sealed-swarm transcripts and the Transluce urlquery snapshot under scan-datasets;
  the seven uncatalogued forward-citation items listed in the survey's Gaps.
