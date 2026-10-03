---
id: synthesis-fork-merge-questions
type: task
title: 'Synthesis: the three fork-merge questions against prior art'
kind: synthesis
status: open
priority: p1
owner: null
for: null  # set to a researcher name to direct the task at them
created: 2026-10-03
created_by: dmarz/fm
depends_on: [scan-papers-fm-merge-poisoning, scan-papers-fm-bft-aggregation, scan-papers-fm-unlinkability, scan-papers-fm-identity-hijack]
topics: [fork-merge-security]
---

## Goal

Context from dmarz: Richard Sutton has suggested that an agent with many resources will likely split into parts that go off (for example to explore a distant information domain) and later merge back. Attack surface: corrupt one part so that when it merges back it corrupts the parent. Questions: (1) how a parent can hide which sub-agent or swarm it will reintegrate; (2) whether a Byzantine-style threshold or protocol can force an attacker to corrupt k of n parts; (3) what the strongest attack vector is (for example prompt injection that overwrites a sub-agent memory so it takes on another agent identity and cuts others out). Write synthesis/fork-merge-questions.md answering each question with what prior art already establishes.

## Done when

- synthesis/fork-merge-questions.md exists, cites library entries as [[id]], and passes check.

## Coverage note


Agent dmarz/fm, 2026-10-03. This synthesis task ran no new searches. It used the 11 fm lane reports and 3 gap reports, whose queries, APIs and rounds are in each lane's task Coverage note and in researchers/dmarz/notes/fm-gap-1.md, fm-gap-2.md and fm-gap-3.md. Work done here:

- Re-fetched the official Dwarkesh transcript (https://www.dwarkesh.com/p/richard-sutton) with curl and checked the Sutton passage at 00:49:51 word for word against [[sutton-2025-father]].
- Spot-checked about 90 load-bearing numbers against the library entries they are cited to.
- Confirmed that all 197 distinct [[id]] links in synthesis/fork-merge-questions.md resolve to existing entries.
- `lab.py check --agent dmarz/fm`: 0 errors. `lab.py verify --agent dmarz/fm`: 74 papers, 0 problems.
- Repo-wide `check` has 1 error in surveys/fork-merge-security.md (frontmatter still TODO). That survey is being written by a parallel session and was not touched.

Found but not added (carried over from the lanes, highest priority first):
- Secret committee election (2024), the bridge from Q1 to Q2.
- Roth 2002 "Programming Satan's agents" (Q3).
- DBA distributed backdoor (ICLR 2020).
- The critique that subliminal learning is a LoRA artefact (arXiv 2606.00831).
- Javadpour 2024 honeypot survey.
- X and LessWrong reactions to the Sutton episode.

What is thin:
- No source measures k-of-n merge robustness with a shared adversarial input across forks.
- No source measures dmarz's full identity-overwrite, exclude, merge chain.
- No source applies any hiding mechanism to fork-merge agents.
- No source measures corruption when a diverged copy is merged back into weights after exploring a real domain.
- Many 2026 entries are at abstract or skim depth.
