---
name: Candidate batch
about: A claimable batch of source candidates for the library (normally created by scripts/batches.py publish)
title: "[batch] <source>/<topic>: <n> candidates (<batch-id>)"
labels: batch
assignees: ""
---

Batch `<batch-id>`: <n> <source> candidates, topic `<topic>`. File: `lab/candidates/<source>/<batch-id>.jsonl`.

**How to work it** (full flow in `lab/PIPELINE.md`):

1. `python3 scripts/batches.py claim <this-issue> --agent <researcher>/<agent>`
2. For each item: open the source, `python3 scripts/lab.py find "<url>"`, then `python3 scripts/lab.py new <kind> <id> --agent <id>` and fill every TODO to the AGENTS.md bar.
3. Tick the box as you go. Skip off-topic, dead or already-catalogued items with a one-line reason in a comment.
4. Keep `python3 scripts/lab.py sync --agent <id> --every 180` running.
5. `python3 scripts/batches.py done <this-issue> --agent <id> --entries <paths>` closes this.

A claim with no issue activity (comment, edit, ticked box) for 90 minutes is stale and anyone may claim it again.

## Items

- [ ] **1.** <url>  
  <title>  
  _<author>, <date>, score <n>_

## Done when

- Every item is ticked or explicitly skipped with a reason.
- Each kept item has an entry in `1-library/<dir>/` that passes `python3 scripts/lab.py check`, tagged with the batch topic.
- Threads: full text archived. Blogs: evidence-quality section filled. Related entries linked as `[[id]]`.
- `done` comment lists the entry paths.
