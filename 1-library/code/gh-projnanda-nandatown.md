---
id: gh-projnanda-nandatown
type: code
title: "nandatown: local test track and sandbox for multi-agent protocols (twelve replaceable protocol layers, seeded simulation, fault injection, evidence bundles)"
repo: projnanda/nandatown
url: https://github.com/projnanda/nandatown
authors: ["Project NANDA (MIT, Ramesh Raskar's group and contributors)"]
year: 2026
language: Python
license: "Apache-2.0"
stars: 50
last_commit: 2026-10-02
topics: [llm-agent-swarms, sybil-resistance, meta]
added_by: shadow/sol-w4
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Nanda Town is Project NANDA's open sandbox for testing how AI agents behave as a system rather than as individuals: discovery, trust establishment, value exchange, negotiation and coordination under faults. Agent-to-agent interaction is split into twelve replaceable protocol layers (transport, communication, identity, registry, auth, trust, payments, coordination, negotiation, memory, privacy, data facts), and contributions are PRs that add a protocol, a plugin implementing it in one layer, and a test. Three modes: the Lab (scripted participants in a seeded discrete-event simulation, deterministic and replayable), the Track (a FastAPI coordinator over SQLite with subprocess HTTP-mailbox participants), and the Path (an existing A2A endpoint). Every run writes a portable evidence bundle. The default Track profile `quote-crash-restart` has a seller crash after claiming a job, gets fenced and restarted, and rejects stale-fence acks; the `marketplace` Lab scenario has two sellers and a buyer discover each other, haggle, settle via escrow, survive a duplicated delivery, build reputation from signed receipts and reuse a remembered counterparty. The README cites the SSRN paper "Towards Sandboxes for the Internet of Agents" (abstract id 5801322) as its framing. Repo created 2026-05-15, rebuilt main branch with legacy code archived at `archive/legacy`; 50 stars. Announced for societies work by Raskar in [[x-raskarmit-2104019174850806252]].

## What it can do for us

A ready-made harness for small controlled agent-society experiments where the protocol layer is the independent variable: swap the trust or identity layer, inject a fault, and compare outcomes against invariants. The identity, registry, auth and trust layers are the natural place to test sybil-resistance mechanisms (which is why that topic is tagged); the scenarios with reputation from signed receipts are a baseline for identity-based trust. Mock-model runs need no API key and complete in seconds, so it is cheap to iterate.

## Run notes

Not run. Read the project site (nandatown.projectnanda.org) and the README on main. Install per README: `python3 -m venv .venv && source .venv/bin/activate && pip install -e .` (Python 3.11+), then `nandatown run` for the default Track profile or `nandatown run marketplace` for the Lab scenario.

## Limitations

Populations in the Lab are scripted, not LLM-driven, unless you wire a model endpoint, so emergent behaviour is bounded by the scenario author. The README is explicit that a passing scenario is evidence only about the systems that scenario exercises. 50 stars and a recent rewrite, so expect churn; the legacy PR history does not imply code that runs on main. The SSRN paper it cites was not opened and is not catalogued.
