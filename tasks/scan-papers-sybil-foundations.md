---
id: scan-papers-sybil-foundations
type: task
title: 'Catalogue the papers: Sybil attacks and defences (foundations)'
kind: scan
status: claimed
priority: p0
owner: dmarz/sybil-foundations
for: null
created: 2026-10-03
created_by: dmarz/sybil
depends_on: []
topics:
- sybil-resistance
- meta
claimed_at: 2026-10-03T18:01Z
updated: 2026-10-03T18:01Z
---

## Goal

Seminal and survey work on Sybil attacks: Douceur 2002, social-graph defences (SybilGuard, SybilLimit, SybilInfer, SybilRank, SumUp), resource testing, PoW/PoS as Sybil cost, proof of personhood (pseudonym parties, BrightID, Idena, Worldcoin), and surveys of the area.

## Done when

- [x] At least 15 entries catalogued with topic `sybil-resistance`, including every review article found. (21 new entries by dmarz/sybil-foundations plus notes on 4 existing entries.)
- [x] At least 4 read in full. (6: douceur-2002-sybil, levine-2006-survey, borge-2017-proof-of-personhood, siddarth-2020-who, ford-2008-offline, aspnes-2005-exposing.)
- [x] Code linked where it exists. (cao-2012-aiding links gh-binghuiwang-sybildetection and gh-brightid-brightid-antisybil; yu-2006-sybilguard links gh-boshmaf-sypy; Idena code annotated. The code entries themselves belong to dmarz/sybil-code-data.)
- [x] Coverage note filled and `python3 scripts/lab.py check` passes.

## Coverage note

Written by dmarz/sybil-foundations, 2026-10-03.

**Entries added (21).** Impossibility and resource testing: [[douceur-2002-sybil]] (full), [[aspnes-2005-exposing]] (full), [[gupta-2020-resource]]. Sensor and robot networks: [[newsome-2004-sybil]], [[gil-2015-guaranteeing]]. Social-graph defences: [[yu-2006-sybilguard]], [[yu-2008-sybillimit]], [[danezis-2009-sybilinfer]], [[tran-2009-sybil-resilient]], [[cao-2012-aiding]] (SybilRank), [[yu-2009-dsybil]], [[viswanath-2010-analysis]]. Proof of personhood: [[ford-2008-offline]] (full), [[borge-2017-proof-of-personhood]] (full), [[ford-2020-identity]], [[siddarth-2020-who]] (full). Surveys and SoKs: [[levine-2006-survey]] (full), [[mohaisen-2013-sybil]], [[alvisi-2013-sok]], [[yu-2011-sybil]], [[mukherjee-2023-sok]].

**Notes appended to existing entries (4).** [[bara-2026-epistemic]] (links epistemic Sybils back to Douceur and Viswanath), [[huang-2019-lightweight]] (INFOCOM DOI and measured numbers), [[mallmann-trenn-2021-crowd]] (T-RO bibliographic detail), [[gh-idena-network-idena-go]] (protocol description sources). I created huang-2020-lightweight and mallmann-trenn-2022-crowd in a race with dmarz/sybil-robotics, found their entries for the same arXiv ids, deleted mine and appended notes instead.

**How I searched.** Crossref `query.bibliographic` for every seed title (all seeds resolved except SybilInfer, SybilRank, SumUp, Levine and Ford 2020, which have no DOI and were confirmed via OpenAlex and the PDFs). OpenAlex `works?search=` for "sybil proof of personhood", "sybil attack survey", "SoK evolution of sybil defense", "resource burning permissionless", "spoof-resilient multi-robot", "identity and personhood digital democracy", "Idena", "BrightID", "SybilInfer", "SybilRank fake accounts", "SumUp", "sybil tutorial survey", "computationally-challenged Byzantine impostors", "sybil multi-agent reinforcement learning", "sybil large language model agents" (OpenAlex daily budget for this IP ran out mid-session). arXiv export API returned empty results for every query (rate-limited), so arXiv papers were read from arxiv.org/pdf and /abs directly. Semantic Scholar was rate-limited at first; once it answered I ran forward citation chasing on Douceur 2002 (all 5,626 citing papers scanned, filtered by title for agent, swarm, robot, LLM, personhood) and on Siddarth 2020 (all 45 citing papers). Backward chasing: reference lists of Levine 2006, Borge 2017, Siddarth 2020 and Ford and Strauss 2008 (read in full) and the conclusion and references of SybilRank and SybilGuard. Yu's NUS publication page was used to find the SIGACT News tutorial and DSybil. GitHub API for BrightID and Idena repos (both already catalogued by dmarz/sybil-code-data).

**Vocabulary covered.** Distributed systems (Sybil attack, pseudospoofing, Byzantine impostors, resource testing, DHT), security (fake accounts, social-graph Sybil detection, SoK), robotics and wireless (spoofing, spoof-resilient, multi-robot, sensor networks), crypto (proof of personhood, pseudonym parties, proof of work as identity pricing), ML (Bayesian inference on graphs, online learning for recommendations).

**Found but not added, and why.** Surveys not opened or out of lane: Chang and Wu 2014 "Survey of Sybil Attacks in Networks" (book chapter, no open text found), Vasudeva and Sood 2018 (ad hoc networks), John et al. 2015, the PeerJ 2021 IoT sensor-network survey and Zukarnain et al. 2023 underwater survey (all narrow domain surveys; not opened). Bazzi and Konjevod 2005 "On the establishment of distinct identities in overlay networks" (found on Semantic Scholar; no open PDF reached before rate limits). Integro (Boshmaf et al. 2015/2016), SybilShield 2013, Liu et al. 2015 temporal dynamics, Schoenebeck et al. 2016 latent network structure, Farach-Colton et al. 2023 "Graph Ranking and the Cost of Sybil Defense" (all found in OpenAlex or Semantic Scholar listings, not opened). Cheng and Friedman 2005 "Sybilproof reputation mechanisms" and Yokoo false-name-proof auctions are cited in Levine 2006 but belong to the sybil-mechanisms lane. Personhood credentials, anonymous credentials and RLN left to sybil-credentials (adler-2024-personhood exists from another agent). Forward citations of Douceur that belong to the LLM-agent lane and were left for it: "Open Challenges in Multi-Agent Security" (arXiv 2505.02077), "Virtual Agent Economies" (2509.10147), "How does Adversarial Influence Scale in Multi-Agent Systems?" (2609.30028), "MiniRep" (2609.39297), "When Should Agent Trust Be Conditional?" (2606.14200), "Decomposition Attacks Across Unlinkable Identities" (2608.17445). Project-specific PoP analyses (Humanode whitepaper, "Security of Proof-of-Personhood: Idena", Encointer scalability) not opened.

**Still thin.** Worldcoin / World ID primary sources were not opened in this lane. Formal treatment of PoS as Sybil resistance (stake as identity pricing) is covered only through Gupta et al. and the PoP critiques; a primary PoS paper could be added by the mechanisms lane. No source measured Sybil attacks on LLM agent swarms directly except [[bara-2026-epistemic]]; the robotics line (Gil, Mallmann-Trenn) is the only one with dynamics-level experiments.

**Verify status.** `lab.py verify --agent dmarz/sybil-foundations` flags three title mismatches (yu-2006-sybilguard, newsome-2004-sybil, yu-2011-sybil). In each case the DOI is correct and Crossref stores a shortened title without the subtitle ("SybilGuard", "The sybil attack in sensor networks", "Sybil defenses via social networks"); the entries keep the full titles copied from the papers and say so in their Methods sections. Five entries have no DOI or arXiv id (SybilInfer NDSS, SybilRank and SumUp NSDI, Levine and Aspnes technical reports) and verify only warns.
