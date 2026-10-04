---
id: deploy-hub-replay-json
type: task
title: Deploy hub change so the public site can serve replay.json (agentops PR #20)
kind: admin
status: open
priority: p1
owner: null
for: dmarz
created: 2026-10-04
created_by: dmarz/discussion-dose
depends_on: []
topics: []
---

## Goal

For the agentops agent (dmarz/agentops). swarm-labs-agentops PR #20 (branch `discussion-dose-v2-launcher`) adds the deliberation live view and replay player to swarm-live; the site is already deployed from that branch. The replay player still 404s on the public site because the hub's read token only serves images and `frame.json`. Commit `5db067c` adds `replay.json` to `READ_ARTIFACT_NAMES` in `hub/hub.py`.

## Done when

- [ ] PR #20 merged to main (so a later site deploy from main keeps the view).
- [ ] Hub deployed with `scripts/safe-deploy.sh hub` (waits for no active runs; restart affects all workers).
- [ ] `curl https://swarm-live.pages.dev/api/a/discussion-dose-v2/14b3bd88/replay.json` returns `kind: deliberation-replay`, and the run page shows the replay player with frames.
