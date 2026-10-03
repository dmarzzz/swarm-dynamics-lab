---
id: gh-hackafterdark-phosphor
type: code
title: "phosphor: hardened Go agent runtime with layered memory-poisoning defences (single-writer vault, write-time scan, inferred-never-promotes, HMAC tamper seal)"
repo: hackafterdark/phosphor
url: https://github.com/hackafterdark/phosphor/blob/main/docs/memory/POISONING.md
authors: ["Tom Maiaroto (hackafterdark)"]
year: 2026
language: Go (repo language stats dominated by vendored C from tree-sitter grammars)
license: "NOASSERTION on GitHub (custom or unrecognised licence file, check before reuse)"
stars: 5
last_commit: 2026-10-03
topics: [fork-merge-security]
added_by: shadow/sol-w4
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Phosphor is a terminal coding-agent runtime in Go by Tom Maiaroto, described by its author as a research project and reference for agent security rather than a product. The document we catalogue, `docs/memory/POISONING.md`, lays out its memory-poisoning threat model and defences. The threat framing: memory is the highest-privilege injection surface because it is replayed into the system prompt of every later session, so a poisoned entry carries system-turn authority and persists until noticed. Defences are layered: (1) a single-writer fence, the vault is only writable through the `memory` tool and only from the primary agent context, so a sub-agent or cron prompt cannot write to shared memory, though it can read; (2) a write-time content scan that refuses ChatML-class control tokens, role-tag forgery, "ignore instructions" phrasing, and gitleaks-detected credentials, failing closed if the detector is unavailable; (3) a sanitiser that runs on every read, not only on write, because humans and sync tools also edit the files; (4) inferred content is forced to `pending` and structurally cannot reach the always-injected Tier A window until a human confirms it (trust 0.5 to 0.8, auto-promote floor 0.75); (5) quarantine of rows whose frontmatter fails to parse or whose HMAC tamper seal fails; (6) trust and status are re-derived by the index so hand-editing frontmatter cannot raise standing. Announced on X in [[x-tmaiaroto-2103944480613359729]].

## What it can do for us

A worked example of concrete merge-threshold rules for the fork-merge-security question: a sub-agent's output cannot write to the parent's durable memory at all, and anything the agent inferred (as opposed to was told) cannot self-promote into high-authority context. These map directly onto the "model output cannot increase authority" and "transformation cannot erase taint" invariants proposed in [[x-rookepoole-2104926181904539846]]. The HMAC seal plus quarantine-on-failure is also a cheap pattern for detecting offline tampering of agent state.

## Run notes

Not run. Read POISONING.md in full via the raw GitHub URL and the README; did not open `security.go`, `gate.go` or `store.go`, so the line references in the doc are the author's and unverified by us. Repo created 2026-03-08, last push 2026-10-03, 5 stars at access.

## Limitations

Single-maintainer project with 5 stars; the defences are described in prose with code line references, not evaluated against an attack benchmark. The single-writer rule relies on the generic file tools refusing vault paths (`vaultWriteGuard`), so it protects against the agent's own tools, not against a compromised host. Licence shows as NOASSERTION on GitHub. The doc truncates at the tamper-seal section in our fetch; INTEGRITY.md was not read.
