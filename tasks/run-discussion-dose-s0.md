---
id: run-discussion-dose-s0
type: task
title: Prepare and run the first real-model discussion-dose qualification
kind: build
status: claimed
priority: p1
owner: dmarz/discussion-dose
for: dmarz
created: 2026-10-03
created_by: dmarz/discussion-dose
depends_on: []
topics: []
claimed_at: 2026-10-03T23:50Z
updated: 2026-10-03T23:50Z
---

## Goal

Add the native Anthropic adapter, qualify with Haiku 4.5, and report every exploratory attempt. Human authorized paid pilot; formal S2 remains disabled.

## Done when

- [x] Native adapter, accounting, and offline tests pass.
- [ ] Deploy pinned revision and run the credential-enabled pilot.
- [ ] Publish qualification results and release fleet claim.

## Progress

Runtime deployed; first real-provider attempt `discussion-dose/775e3cd6` was blocked by insufficient Anthropic API credits before any model output. User asked to fund billing. Preserve failed attempt and resume declared preflight v2 after funding; full S0 remains unsubmitted.
