---
id: scan-flashbots-sybil
type: task
title: 'Catalogue Flashbots work touching Sybil resistance'
kind: scan
status: open
priority: p0
owner: null
for: null  # set to a researcher name to direct the task at them
created: 2026-10-03
created_by: dmarz/sybil
depends_on: []
topics: [sybil-resistance]
---

## Goal

Every public Flashbots source (writings.flashbots.net, collective.flashbots.net, Flashbots papers and GitHub) that deals with Sybil resistance, identity cost, spam, or rate limiting: order flow auctions and refunds, MEV-Share, Protect, spam from on-chain searching, BuilderNet and TEE attestation as identity, SUAVE, timing games, mev-boost relays. Public sources only: this repo is public.

## Done when

- Every relevant Flashbots source found is catalogued (papers, blogs, code) with topic `sybil-resistance`.
- Each entry states which Sybil problem it addresses and the defence used.
- Coverage note filled and `python3 scripts/lab.py check` passes.

## Coverage note

