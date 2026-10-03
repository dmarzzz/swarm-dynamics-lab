---
agent: shadow/sol-w5
tool: other
state: idle  # working | idle | blocked | done
task: null
doing: worked batches #28 #29 #30 #27 #55 #56 #77 #72 #71; free sybil-resistance batches remain
updated: 2026-10-03T20:20Z
---

## Notes

Batch worker. Earlier: #6, #7 (x/llm-agent-swarms).
Round 2: #28/#29/#30 crowds talks, #27 criticality, #55/#56/#77 swarm-detection papers, #72/#71 sybil-resistance papers.
Gotchas:
- batches.py done checks entry paths against the pipeline checkout, not your worktree; use --force once the entries are on main.
- YouTube blocks transcript fetches from this host (yt-dlp, youtube-transcript-api, innertube get_transcript all bot-walled). Descriptions/abstracts still come through a plain curl of the watch page (ytInitialPlayerResponse / attributedDescription); talks from those are abstract depth. Prefer cataloguing the underlying paper.
- Id collisions with parallel agents happen (#77: three ids taken by sol-g51 minutes earlier). On rebase conflict keep theirs, append your read as "Notes from <agent>".
- Journal versions with a different title than the arXiv preprint fail `lab.py verify`; set arxiv: null and mention the preprint id in the summary.
