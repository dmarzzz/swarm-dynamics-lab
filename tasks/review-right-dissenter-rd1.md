---
id: review-right-dissenter-rd1
type: task
title: Review Right Dissenter RD-1 design and offline prototype
kind: review
status: done
priority: p1
owner: dmarz/inbox-design-feedback
for: dmarz
created: 2026-10-03
created_by: vishesh/codex-decision-models
depends_on: []
topics:
- dissent
- decision-models
updated: 2026-10-04T04:17Z
history:
- 2026-10-04T03:56Z reassigned for: shadow -> dmarz at the request of vishesh (task creator side), via Discord
claimed_at: 2026-10-04T04:17Z
outputs:
- researchers/dmarz/notes/inbox-reviews-2026-10-04/right-dissenter-review.md
---

## Goal

Independently audit researchers/vishesh/notes/dissent/PLAN.md and the offline prototype. This is a design/implementation review, not evidence that the formal literature gate has passed or permission to launch. No model calls or holdout access.

## Done when

- Derive the bridge, build and alarm examples by hand; run the offline tests.
- Inspect truth separation, source deduplication, withdrawal/reopening, resource comparability, failure denominators and strongest deterministic/always-check baselines.
- Check whether controlled grammar fixtures can justify any native-model contribution; state remaining prior-art and semantic-corpus requirements.
- Record a reviewer-owned verdict with exact source revision and blockers. Do not access reserved qualification or holdout seeds.
