---
id: review-fork-merge-security
type: task
title: 'Review: fork-and-merge security survey'
kind: review
status: done
priority: p1
owner: vishesh/fm-security-review
for: vishesh
created: 2026-10-04
created_by: shadow/sol-fm
depends_on:
- survey-fork-merge-security
topics:
- fork-merge-security
claimed_at: 2026-10-04T14:39Z
updated: 2026-10-04T14:42Z
outputs:
- reviews/fork-merge-security--vishesh.md
---

## Goal

Cross-researcher review of `surveys/fork-merge-security.md` (owner dmarz, gate-closed by shadow/sol-fm on
2026-10-04). The reviewer must belong to a researcher other than dmarz. File
`reviews/fork-merge-security--<your-researcher>.md`
(`python3 scripts/lab.py new review fork-merge-security--<researcher> --agent <id>`), spot-check five cited
entries against their sources, and set `verdict: pass` or `verdict: revise`.

Context the reviewer should know: dmarz/fm wrote and merged this survey incomplete on 2026-10-03 (the
saturation floor was failing because the gap-fill rounds were still finding work on a rate-limited shared IP).
shadow/sol-fm ran a saturation + forward-citation pass on 2026-10-04 (OpenAlex only; Semantic Scholar was
429 all day), chased the forward citations of `bagdasaryan-2020-how` (805 citers) and
`christiano-2018-supervising` (26) that issues #75 and #51 recorded as never run, and catalogued the three
entries those chases plus a secret-committee search produced: `xie-2020-dba`, `lyu-2023-poisoning`,
`zhai-2024-secret`. The last two logged search rounds are now 1/8 and 0/40, so `lab.py gate
fork-merge-security` passes.

## Done when

- `reviews/fork-merge-security--<researcher>.md` exists with `verdict: pass` or `revise` and five spot-checks.
- Spot-check at minimum the three entries sol-fm added (`xie-2020-dba`, `lyu-2023-poisoning`,
  `zhai-2024-secret`) since they are abstract-depth and added under deadline, plus two of dmarz's full reads.
- If `revise`, name the specific defects (overstated read_depth, numbers that need the body, citation that
  does not resolve) so the owner's agents can fix them.
- Known limitations to weigh, not necessarily blockers: the three sol-fm entries are abstract-depth
  (OpenAlex abstracts); the open issues #74 (contagion scan never reran its own search), #76 (read-depth
  audit across the lane) and #51 (remaining paywalled classics) are still open and narrower in scope.

## Review outcome — 2026-10-04

Completed by vishesh/fm-security-review. Output: `reviews/fork-merge-security--vishesh.md`, verdict **revise**. All three sol-fm additions inspected, plus the two requested dmarz full-read entries and Lamport. Five primary-source checks were possible; Zhai received a publisher-metadata check with primary full-text access explicitly limited. Four actionable revision groups, three independent searches, and scoped missed-work/coverage findings are recorded. Task completion means the review was delivered, not that the survey passed.
