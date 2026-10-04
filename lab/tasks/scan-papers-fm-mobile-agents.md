---
id: scan-papers-fm-mobile-agents
type: task
title: 'Catalogue the papers: mobile-agent security and Byzantine state merge'
kind: scan
status: claimed
priority: p1
owner: dmarz/fm-mobile-agents
for: null
created: 2026-10-03
created_by: dmarz/fm
depends_on: []
topics:
- fork-merge-security
claimed_at: 2026-10-03T18:12Z
updated: 2026-10-03T18:12Z
---

## Goal

Context from dmarz: Richard Sutton has suggested that an agent with many resources will likely split into parts that go off (for example to explore a distant information domain) and later merge back. Attack surface: corrupt one part so that when it merges back it corrupts the parent. Questions: (1) how a parent can hide which sub-agent or swarm it will reintegrate; (2) whether a Byzantine-style threshold or protocol can force an attacker to corrupt k of n parts; (3) what the strongest attack vector is (for example prompt injection that overwrites a sub-agent memory so it takes on another agent identity and cuts others out). This task: 1990s-2000s mobile agents visiting hostile hosts and returning, plus Byzantine CRDTs and replica reconciliation.

## Done when

- At least 15 entries catalogued with topic `fork-merge-security`, including every review article found.
- At least 4 read in full.
- Coverage note filled and `python3 scripts/lab.py check` passes.

## Coverage note

Filled by dmarz/fm-mobile-agents, 2026-10-03.

**Entries added (22: 19 papers, 1 blog, 2 code; all tagged fork-merge-security):** papers: harrison-1995-mobile, farmer-1996-security, minsky-1996-cryptographic, yee-1997-sanctuary, sander-1998-protecting, jansen-1999-mobile (NIST review), algesheimer-2001-cryptographic, li-2004-secure, schneider-2005-implementing (review), mahajan-2010-depot, torres-arias-2016-omitting, torres-arias-2019-in-toto, kleppmann-2020-byzantine, jacob-2021-conflict-free, kleppmann-2022-making, lamb-2022-reproducible, ladisa-2022-taxonomy (SoK), menetrey-2022-attestation (review), bhattacharya-2025-perpetual; blog: crowdstrike-2021-sunspot; code: gh-ept-byzantine-eventual (ran: mocha 7/7 passing, evaluation output identical to committed data), gh-in-toto-in-toto.

**Read in full (8):** kleppmann-2022-making, kleppmann-2020-byzantine, jacob-2021-conflict-free, sander-1998-protecting (1998 preprint), yee-1997-sanctuary (1997 TR), minsky-1996-cryptographic, schneider-2005-implementing, farmer-1996-security.

**APIs and access.** Semantic Scholar, OpenAlex and the arXiv export API returned HTTP 429 from this host for the whole session (OpenAlex Retry-After about 5.5 h), shared with parallel agents. Worked: Crossref (metadata, citation counts, DOI checks), arxiv.org abs/pdf pages, OpenCitations v2 citations endpoint (forward chasing), GitHub via gh, Wayback Machine availability API (old PostScript preprints, text extracted locally), author/institution pages, WebSearch and WebFetch. Springer chapter pages and PDFs were blocked (client challenge), so several 1998 LNCS chapters were only reachable through archived preprints.

**Rounds (results / new).**
1. Crossref title lookups for the 10 seeds: 10 / 10 identified, metadata only.
2. Direct PDF fetches (arXiv, USENIX, NIST, Kleppmann site, Cornell): 9 / 9 readable.
3. Springer PDFs for 7 LNCS seeds: 7 / 0 (all blocked).
4. WebSearch for free copies of seeds (Sander, Schneider, Karjoth, Chess, Vigna, Yee, Hohl): 7 queries, about 60 results / 6 usable new (Algesheimer, Jansen countermeasures, Loureiro survey, Amro survey, Schneider-Zhou survey, Minsky TR).
5. Wayback lookups for 1990s preprints: 11 / 4 retrieved (Sander-Tschudin, Yee, Harrison-Chess, Farmer); Vigna PDFs found on his site but font-encoded and unreadable.
6. Neighbouring vocabulary (fork consistency, fork-join-causal, untrusted storage, equivocation): 4 / 3 new (SUNDR, Depot, Jacob et al.).
7. Supply chain as "merge an untrusted branch" (in-toto, Git metadata, reproducible builds, SolarWinds, SoK): 6 / 5 new.
8. Forward citations via OpenCitations: Kleppmann 2022 (12 citing), Yee 1999 (72 citing), Sander-Tschudin 1998 (279 citing); titles resolved for the newest 40 of each, about 90 / 6 relevant new candidates (black hole search with Byzantine agents, agent alliances threshold signatures, proof-carrying CRDTs, two surveys), 1 added.
9. WebSearch on black hole search and on agent itinerary anonymity: 2 queries, 20 results / 2 new (Bhattacharya et al. added; one inaccessible).
Saturation not reached; the last round still produced new relevant items.

**Found but not added (could not open full text or abstract, or low value):** Chess, Grosof, Harrison et al. 1995 "Itinerant agents for mobile computing"; Farmer, Guttman, Swarup 1996 ESORICS "Authentication and state appraisal"; Schneider 1997 "Towards fault-tolerant and secure agentry" (WDAG, LNCS 1320); Hohl 1998 "Time limited blackbox security"; Vigna 1998 "Cryptographic traces for mobile agents" (PDF on author site is font-encoded); Karjoth, Asokan, Gulcu 1998 "Protecting the computation results of free-roaming agents"; Roth 1999 "Mutual protection of co-operating agents" and Roth 2002 "Programming Satan's agents" (ENTCS 63, attacks on mobile agent protocols; Q3, high priority); Westhoff et al. 1999 "Protecting a mobile agent's route against collusions" (Q1); Di Luna, Flocchini et al. 2025 "Exploring Dangerous Graphs with Byzantine Companions" (ICDCS, Q2); Markou and Shi 2019 "Dangerous Graphs" survey; Chattopadhyay and Prasad 2022 "Mobile Agent Security Against Malicious Hosts: A Survey" (SN Computer Science); "Mobile Agents System Security: A Systematic Survey", ACM Computing Surveys 50(5) (doi 10.1145/3095797; ACM page returned 403, authors not checked); "Agent Alliances: A Means for Practical Threshold Signature" (ARES 2007); "Proof-Carrying CRDTs allow Succinct Non-Interactive Byzantine Update Validation" (2025); Jansen 2000 "Countermeasures for Mobile Agent Security" (opened, overlaps NIST SP 800-19); Loureiro, Molva, Roudier "Mobile Code Security" (opened, older and thinner than NIST); Amro 2014 arXiv 1410.4147 survey (opened, low quality).

**What is thin.** Q1 (hiding which part returns): only side remarks (random platform choice in Sander-Tschudin, route reversal in Yee, the anonymity future-work item in NIST); the itinerary-anonymity and route-protection papers were not reachable. Q3: the classical attack literature (Roth's attacks on Karjoth-style protocols, truncation and interleaving attacks) is catalogued only indirectly. No 1990s source was read on executing a returned agent's state appraisal in practice. Semantic Scholar citation chasing was not possible; OpenCitations coverage of 1990s LNCS is partial.
