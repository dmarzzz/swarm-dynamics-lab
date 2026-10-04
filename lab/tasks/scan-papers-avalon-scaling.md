---
id: scan-papers-avalon-scaling
type: task
title: 'Prior art on hidden-role games at large N: Mafia game theory, committee selection under adversaries, gossip topology'
kind: scan
status: open
priority: p2
owner: null
for: dmarz
created: 2026-10-03
created_by: dmarz/avalon
depends_on: []
topics:
- sybil-resistance
- swarm-detection
- sync-consensus
- fork-merge-security
---

## Goal

The non-LLM side of hunches A1-A5 (`researchers/dmarz/notes/avalon-swarm-hunches.md`): what is known about
how hidden-role games behave as N grows and the deceiver fraction varies, and the neighbouring literatures the
swarm variant borrows from.

## Seeds

Seeds come from memory and are starting points, not citations.

- Theoretical analyses of the Mafia/Werewolf game (e.g. Braverman, Etesami, Mossel on Mafia; winning
  probability vs number of mafiosi)
- Committee / validator selection under a Byzantine fraction (random sampling, sortition)
- Gossip and opinion dynamics with stubborn or adversarial agents on graphs
- Sybil detection on social graphs (link to existing sybil-resistance entries rather than re-cataloguing)

## Done when

- Game-theory results on win probability vs N and deceiver fraction catalogued (these set the balance sweep).
- Each entry says which hunch (A1-A5) it bears on.
- Coverage note and `check` pass.
