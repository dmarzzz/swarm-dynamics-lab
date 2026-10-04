---
id: synthesis-sybil-flashbots
type: task
title: 'Synthesis: how Flashbots Sybil work relates to swarm and agent Sybil resistance'
kind: synthesis
status: open
priority: p1
owner: null
for: null  # set to a researcher name to direct the task at them
created: 2026-10-03
created_by: dmarz/sybil
depends_on: [scan-papers-sybil-foundations, scan-papers-sybil-robotics, scan-papers-sybil-llm-agents, scan-flashbots-sybil]
topics: [sybil-resistance]
---

## Goal

Write 3-synthesis/sybil-flashbots.md mapping each Flashbots Sybil problem and defence onto its analogue in robot swarms, P2P networks and LLM agent collectives, and naming the open problems that transfer.

## Done when

- [x] 3-synthesis/sybil-flashbots.md exists, cites library entries as [[id]], and passes check. (2026-10-03: 98 distinct entries cited, all present in 1-library/; lab.py check 0 errors.)

## Coverage note

dmarz/sybil-flashbots, 2026-10-03. This is a synthesis task, so no new searches were run and no library entries were added. Inputs were the lane reports from sybil-foundations, sybil-robotics, sybil-llm-agents, sybil-mechanisms, sybil-flashbots, sybil-flashbots-informal, sybil-code-data, sybil-credentials and the two gap fills (P2P and TEE identity), plus the Summary sections of about 90 library entries tagged sybil-resistance, read locally with grep and awk. Every [[id]] in 3-synthesis/sybil-flashbots.md was checked by script to exist under 1-library/ (98 distinct ids). Numbers quoted were spot-checked against the entries (for example gamma 0.719 in bara-2026-epistemic, the over-80% Base spam figure in flashbots-2025-mev).

Structure: (1) a nine-row table mapping Flashbots Sybil problems (refund farming, searcher-as-user injection, on-chain spam, endpoint flooding and re-entry, builder stake splitting, TEE attestation as identity, identity rental via encumbrance, timing games, private order-flow networks) to Flashbots defences and to robot-swarm, P2P and LLM-agent analogues; (2) the mint-cost versus extracted-value frame, sorting defences into raise-cost, lower-value and tolerate; (3) transfers in both directions; (4) ten candidate survey questions, phrased as questions for a prior-art survey, not hypotheses.

Left out: library entries on collusion and wash trading beyond glynn-2026-wash and motwani-2024-secret, and the anonymous-credential detail from the credentials lane beyond what the table needed. Rows marked (adjacent) use Ethereum research posts that are not Flashbots-authored.

Thin: two table cells have no analogue in the library (identity rental and timing games in robot swarms). The Flashbots side rests mostly on forum posts, docs and code; SUAVE economic-security posts, mev-share-node rate limits and Protect thresholds are still unread (see scan-flashbots-sybil). Several "transfer" claims are marked inferred because no source tests them.

