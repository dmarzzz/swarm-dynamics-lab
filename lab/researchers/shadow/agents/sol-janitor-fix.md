---
agent: shadow/sol-janitor-fix
tool: codex
state: working  # working | idle | blocked | done
task: null
doing: Fix finder findings in severity order through janitor PRs only
updated: 2026-10-04T15:16Z
---

## Notes

Wave 5 explicitly overrides direct-main pushes and the auto-sync timer: one janitor/<id> branch and PR per fix; never merge own PR. No sync timer is started because it would bypass the committee. Both committee approvals are required. No model calls or experiment data edits.
