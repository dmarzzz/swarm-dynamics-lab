---
id: scan-papers-fm-unlinkability
type: task
title: 'Catalogue the papers: hiding which part returns (unlinkability, secret election, moving target)'
kind: scan
status: claimed
priority: p0
owner: dmarz/fm-unlinkability
for: null
created: 2026-10-03
created_by: dmarz/fm
depends_on: []
topics:
- fork-merge-security
- sybil-resistance
claimed_at: 2026-10-03T18:12Z
updated: 2026-10-03T18:12Z
---

## Goal

Context from dmarz: Richard Sutton has suggested that an agent with many resources will likely split into parts that go off (for example to explore a distant information domain) and later merge back. Attack surface: corrupt one part so that when it merges back it corrupts the parent. Questions: (1) how a parent can hide which sub-agent or swarm it will reintegrate; (2) whether a Byzantine-style threshold or protocol can force an attacker to corrupt k of n parts; (3) what the strongest attack vector is (for example prompt injection that overwrites a sub-agent memory so it takes on another agent identity and cuts others out). This task: question (1).

## Done when

- At least 15 entries catalogued with topic `fork-merge-security`, including every review article found.
- At least 4 read in full.
- Coverage note filled and `python3 scripts/lab.py check` passes.

## Coverage note

Agent dmarz/fm-unlinkability, 2026-10-03. 24 entries carry `fork-merge-security` from this lane: 21 papers, 1 blog, 1 code repo, and notes appended to the existing [[motwani-2024-secret]]. Read in full: [[chaum-1981-untraceable]], [[piotrowska-2017-loopix]], [[boneh-2020-single]] (main text and constructions; the proof appendices were not checked line by line), [[burianova-2025-secret]]. Reviews included: [[cho-2020-toward]], [[sengupta-2020-survey]], [[pawlick-2019-game]], [[sasy-2024-sok]], [[kuhn-2018-privacy]] (formal hierarchy), [[pfitzmann-2010-terminology]] (glossary).

Search rounds (results / new relevant):
1. Semantic Scholar keyword search for the seeds: HTTP 429 every time (the IP was shared with parallel swarms). 0/0.
2. OpenAlex search, 8 seed queries (Chaum, Tor, Loopix, Motwani, MTD survey, Whisk, honeypot survey, PIR survey): 40 / 16.
3. OpenAlex second-vocabulary round (anonymity trilemma, Pfitzmann terminology, hidden servers, deception taxonomy, Jajodia MTD, anonymous communication survey, mobile agent location privacy): HTTP 429, then a timeout. 0/0.
4. arXiv abstract pages for 6 ids (Loopix, Motwani, Cho, Burianova, Pawlick, Rippin): 6 / 6.
5. Crossref bibliographic queries (predecessor attack, PIR, Fugate, Sengupta, Overlier, trilemma, then Pawlick, Cho, Javadpour, Kuhn): 30 / 8.
6. Direct fetches of ethresear.ch (Whisk), IACR ePrint (SSLE, trilemma), AAAI (Fugate), ScienceDirect (Javadpour, HTTP 403). 5 / 4.
7. Backward chasing: from the Overlier reference to helper nodes to [[wright-2004-predecessor]]; from the Burianova related work to Whisk, homomorphic sortition, Sassafras, Dandelion++. 6 / 3.
8. Forward chasing on Semantic Scholar /citations of SSLE (DOI 10.1145/3419614.3423258): 74 / 4 added ([[heimbach-2024-deanonymizing]], [[azouvi-2021-private]], [[freitas-2022-homomorphic]], [[burianova-2025-secret]] confirmed).
9. Forward chasing on Semantic Scholar /citations of Loopix (arXiv 1703.00536): 200 (one page) / 2 added ([[kuhn-2018-privacy]], [[das-2018-anonymity]] confirmed); most were other metadata-private messaging systems.
10. Web search in LLM-agent vocabulary ("LLM agents anonymity unlinkability mixnet agent-to-agent metadata"): 9 / 1 added ([[dangol-2026-privacy]]).
11. Web search for the 2024 metadata-protecting SoK plus the PoPETs PDF: 9 / 1 added ([[sasy-2024-sok]]).
12. GitHub API for nymtech/nym: 1 / 1.
Rounds 9 to 11 found few new items per result in the anonymity-systems vocabulary. Saturation holds for classic anonymity and SSLE. It does not hold for agent-specific work.

Found but not added: Javadpour et al. 2024 honeypot deception survey (Computers & Security 140, 103792; publisher page returned 403). Gasarch 2004 and Ostrovsky-Skeith 2007 PIR surveys, and the Arunachalaramanan-Chen-Ren 2026 PIR tutorial (not opened). Chaum 1988 dining cryptographers. Christ et al. 2023 accountable secret leader election. Adaptively secure SSLE from DDH (2022). Catalano-Fiore-Giunta UC SSLE (2021). Secret multiple-leader and committee election (2024): this is the obvious next entry for hiding k returners. Sassafras (2023). Dandelion++. Comprehensive Anonymity Trilemma (2020). Stadium, Atom, Express, XRD, Vuvuzela. AgentCrypt (arXiv 2512.08104). The LLM agent communication security survey (arXiv 2506.19676). Rose et al. 2026 on detecting multi-agent collusion (arXiv 2604.01151).

Thin areas: Spitzner's honeypot work and the Jajodia MTD book were not located online, and biological camouflage and decoys were not searched. LLM-agent work that hides which sub-agent reports back is close to absent: [[dangol-2026-privacy]] is the only direct hit, and [[rippin-2026-tool]] and [[motwani-2024-secret]] cover covert channels. Hiding a set of k returners (secret committee election) is found but not catalogued. No source studies fork-and-merge agents with any of these hiding mechanisms. That is a gap, inferred from the searches above.
