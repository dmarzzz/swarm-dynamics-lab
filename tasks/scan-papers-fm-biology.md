---
id: scan-papers-fm-biology
type: task
title: 'Catalogue the papers: fission-fusion and fusion parasitism in biology'
kind: scan
status: claimed
priority: p1
owner: dmarz/fm-biology
for: null
created: 2026-10-03
created_by: dmarz/fm
depends_on: []
topics:
- fork-merge-security
- collective-decision
claimed_at: 2026-10-03T18:12Z
updated: 2026-10-03T18:12Z
---

## Goal

Context from dmarz: Richard Sutton has suggested that an agent with many resources will likely split into parts that go off (for example to explore a distant information domain) and later merge back. Attack surface: corrupt one part so that when it merges back it corrupts the parent. Questions: (1) how a parent can hide which sub-agent or swarm it will reintegrate; (2) whether a Byzantine-style threshold or protocol can force an attacker to corrupt k of n parts; (3) what the strongest attack vector is (for example prompt injection that overwrites a sub-agent memory so it takes on another agent identity and cuts others out). This task: biological analogues (colony fusion, allorecognition, germline parasitism, social parasites, fission-fusion societies).

## Done when

- At least 15 entries catalogued with topic `fork-merge-security`, including every review article found.
- At least 4 read in full.
- Coverage note filled and `python3 scripts/lab.py check` passes.

## Coverage note

Agent dmarz/fm-biology, 2026-10-03. 29 entries added, all tagged `fork-merge-security`; `lab.py check` 0 errors 0 warnings, `lab.py verify` 0 problems (one url-only warning: Buschinger 2009 has no DOI).

**Read in full (4):** stoner-1996-somatic, grum-grzhimaylo-2021-somatic, tsutsui-2003-genetic, giraud-2002-evolution. Skimmed (results sections or main body): bastiaans-2016-experimental, buschinger-2009-social, aureli-2008-fission. The rest at abstract depth.

**Reviews catalogued (7):** strassmann-2011-kin, lenoir-2001-chemical, buschinger-2009-social, aureli-2008-fission, siddle-2013-tale, madgwick-2019-greenbeard, ostrowski-2019-enforcing.

**APIs and rounds.**
- Round 1, seed lookups. Semantic Scholar search returned 429 immediately; OpenAlex returned 6 results for 5 queries, then 429 for the rest of the session. Switched to Europe PMC REST (`/search`, `resultType=lite` sorted by citations, then `resultType=core` by DOI for abstracts). Queries: "Botryllus germ cell parasitism", "Botryllus stem cell parasitism chimera", "Dictyostelium cheater", "Dictyostelium kin discrimination", "fission-fusion dynamics primates", "slave-making ants", "social parasite ant inquiline", "Argentine ant supercolony" (8 queries, 48 results, about 14 relevant).
- Round 2, other lanes: "devil facial tumour disease allograft", "canine transmissible venereal tumor clonal origin", "transmissible cancers bivalves", "CRISPR acquired resistance viruses prokaryotes", "CRISPR interference limits horizontal gene transfer", "vegetative incompatibility virus transmission Cryphonectria", AUTH Buss somatic, "allorecognition clonal invertebrates evolution", "self-recognition social amoebae allelic pairs", "fission-fusion populations" (10 queries, 50 results, about 12 relevant). Crossref bibliographic search for Aureli 2008, Buschinger 2009, Cortesi 2001 (2 of 5 queries answered before 429).
- Round 3, reviews and follow-ups: "high relatedness protects multicellular cooperation", "kin discrimination cooperation microbes review", allorecognition and transmissible-cancer review filters (5 queries, 2 new relevant).
- Round 4, citation chasing: Semantic Scholar `/paper/DOI:10.1073/pnas.79.17.5337/citations` (Buss 1982) returned 100 citing papers, 8 judged relevant, 6 added. The same call for Stoner 1996 failed after 6 retries (429).
- Full text: NCBI PMC article HTML (curl) for Stoner, Tsutsui, Giraud, Grum-Grzhimaylo, Bastiaans 2016. Buss 1982, Foster 2002 and Cortesi 2001 are scanned PDFs on PMC, and the PDF links sit behind a bot check, so those stay at abstract depth. Aureli 2008 PDF from eva.mpg.de; Buschinger 2009 PDF from myrmecologicalnews.org.

**Found but not added.** Lakkis and Lechler 2013 "Origin and biology of the allogeneic response" (mammalian transplant immunology, off-lane). "Vegetative incompatibility in fungi: From recognition to cell death, whatever does the trick" (DOI 10.1016/j.fbr.2016.08.002, a review; title from the Semantic Scholar citation list of Buss 1982, authors not checked, not in Europe PMC, abstract not opened). Zhang et al. 2014 Genetics, vic loci restricting mycovirus transmission (opened abstract; left out because cortesi-2001-genetic covers the same barrier with numbers). Barrangou et al. 2007 CRISPR acquired resistance (opened abstract; left out because marraffini-2008-crispr covers transfer between lineages directly). Pearse and Swift 2006 DFTD allograft (opened abstract; covered by siddle-2013-reversible). Tsutsui et al. 2000 PNAS reduced genetic variation in Argentine ants (listed only). Rinkevich et al. 2013 stem cell cycling in Botryllus and Voskoboynik and Weissman 2014 (listed in search results only). A classic allorecognition review I looked for by Crossref query returned 429 and was not identified. Gruenheit et al. 2017 polychromatic greenbeard locus in Dictyostelium (listed only). Vos and Velicer 2009 Myxococcus social conflict (listed only). Murchison 2012 and Stammnitz 2018 devil genomes (listed only).

**Thin.** Horizontal gene transfer beyond CRISPR (restriction-modification, plasmid incompatibility) is covered by one entry. Immune self/non-self theory (danger model, discontinuity theory) has no entry; Lakkis 2013 was the only hit in this round. No primary measurement of fission-fusion reunion behaviour (greeting, information exchange at reunion) beyond the Aureli framework. Coral and hydroid chimerism (Hydractinia allorecognition, coral chimeras) appears in the Buss citation list and was not opened. No biological study found that measures a threshold of the form "k of n parts must be corrupted"; the closest are Cortesi 2001 (multi-locus barrier, roughly additive on the logit scale) and the frequency-dependent cheater advantage in Grum-Grzhimaylo 2021 (cheater only wins below about 30 percent).
