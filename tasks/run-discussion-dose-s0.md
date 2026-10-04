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
updated: 2026-10-03T23:55Z
history:
- '2026-10-03T23:54Z released by dmarz/discussion-dose: Implementation deployed and verified; pilot blocked by Anthropic API credits. Resume preflight v2 after user funds account; S0 not queued.'
claimed_at: 2026-10-03T23:55Z
---

## Goal

Add the native Anthropic adapter, qualify with Haiku 4.5, and report every exploratory attempt. Human authorized paid pilot; formal S2 remains disabled.

## Done when

- [x] Native adapter, accounting, and offline tests pass.
- [ ] Deploy pinned revision and run the credential-enabled pilot.
- [ ] Publish qualification results and release fleet claim.

## Progress

Runtime deployed. Billing-blocked attempt `discussion-dose/775e3cd6` preserved. Funded preflight `discussion-dose/00820f46` passed all 8 episodes for $0.615028. Qualification startup `discussion-dose/6c9284c3` failed before calls when server configuration refreshed the credential file; SOPS-backed launcher fixed. Declared qualification v2 `discussion-dose/3e4b084a` is now running on pinned e8ae7a4; first world completed with 8 valid correct episodes.
