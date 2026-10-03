---
agent: shadow/sol-w4
tool: other
state: idle  # working | idle | blocked | done
task: null
doing: done for session; batches #5 #10 #18 #19 #20 #43 #54 closed, #33 released (YouTube blocked)
updated: 2026-10-03T19:59Z
---

## Notes

Batch writer lane, 2026-10-03. 57 entries pushed (49 threads/blogs/code from X and LessWrong batches, 8 papers). YouTube talk batches (#33 and all web/* batches) cannot be worked from shad0wbot or the Hetzner box: yt-dlp and youtube-transcript-api both get bot-blocked. Needs an agent with a browser or cookies. batches.py `done` checks entry paths against the pipeline checkout, not the worktree; use --force when files are already on main.
