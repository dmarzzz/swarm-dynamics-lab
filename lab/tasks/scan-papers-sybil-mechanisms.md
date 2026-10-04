---
id: scan-papers-sybil-mechanisms
type: task
title: 'Catalogue the papers: false-name-proof mechanisms and Sybil-proof reputation'
kind: scan
status: claimed
priority: p1
owner: dmarz/sybil-mechanisms
for: null
created: 2026-10-03
created_by: dmarz/sybil
depends_on: []
topics:
- sybil-resistance
- collective-decision
claimed_at: 2026-10-03T18:01Z
updated: 2026-10-03T18:01Z
---

## Goal

Mechanism design under free identities: false-name-proof auctions and voting (Yokoo et al.), Sybil-proof reputation (Cheng and Friedman), Sybil-proof incentive and referral networks, Shapley and attribution under splitting, quadratic funding and cluster matching, airdrop Sybil economics.

## Done when

- [x] At least 15 entries catalogued with topic `sybil-resistance`, including every review article found. Progress: 25 entries (22 papers, 1 blog, 2 code). Review article found and catalogued: conitzer-2010-using.
- [x] At least 4 read in full. Progress: 4 full (pan-2024-sybil, mazorra-2023-cost, babaioff-2012-bitcoin, conitzer-2010-using) plus 3 skims (yokoo-2004-effect, patel-2025-maxshapley, buterin-2019-flexible).
- [x] Code linked where it exists. Progress: gh-spaddle-boat-maxshapley linked from patel-2025-maxshapley; gh-brunomazorra-llms-sybils catalogued. The code link printed in mazorra-2023-cost (BrunoMazorra/CostsOfSybils) returns 404.
- [x] Coverage note filled and `python3 scripts/lab.py check` passes (0 errors, 0 warnings for dmarz/sybil-mechanisms on 2026-10-03; verify: 20 papers, 0 problems).

## Coverage note

Agent dmarz/sybil-mechanisms, 2026-10-03.

**APIs and queries.** Semantic Scholar returned HTTP 429 for every call this session (search and /citations), so search and citation chasing ran on OpenAlex and the arXiv API instead. OpenAlex search: "false-name bids combinatorial auctions", "mechanism design prevent false-name manipulations", "Sybilproof reputation mechanisms", "On Bitcoin and red balloons", "Sybil-proof referral", "false-name-proof voting", "anonymity-proof Shapley value", "false-name-proof", "Sybil-proof mechanisms", "quadratic funding sybil", "airdrop sybil", "Shapley value splitting manipulation", "sybil-proof incentive tree", "false-name-proof matching", "sybil attack quadratic voting", "Beyond collusion resistance connection-oriented cluster matching". arXiv API: all:"sybil-proof" (20 results), ti:"Beyond Collusion Resistance", "connection-oriented cluster match", "quadratic funding" AND sybil (both empty). Forward citations via OpenAlex cites: filter on Yokoo 2004, Cheng and Friedman 2005, Babaioff 2012, Conitzer and Yokoo 2010, Pan 2024 and Chen 2013. Reference lists read in full for Pan 2024, Mazorra and Della Penna 2023 and Conitzer and Yokoo 2010. Web search for the Yokoo preprint and the Miller/Weyl/Erichsen paper. GitHub API for repos linked from papers and the BrunoMazorra account.

**Found but not added, and why.**
- Wagman and Conitzer, false-name-proof voting with costs (AAAI 2008; IJGT 2014, doi 10.1007/s00182-013-0397-3) and Conitzer et al., False-Name-Proofness in Social Networks (WINE 2010): no abstract or full text reachable (publisher elides abstracts in OpenAlex and Semantic Scholar). Their results are described second-hand in conitzer-2010-using.
- Miller, Weyl, Erichsen, Beyond Collusion Resistance (SSRN 4311507): SSRN returned 403; catalogued the authors' ethresear.ch summary instead (ethresearch-2023-collusion). Gitcoin's COCM blog returned 502.
- Kesidis et al. 2009 multiplicative reputation chains, Zhang et al. 2020 Sybil-proof answer querying (arXiv 2005.13224), Zheng et al. 2024 information propagation with budgets (arXiv 2405.14293), Zhang et al. 2015 incentive tree for crowdsourcing, Liu et al. budget-feasible crowdsensing, Ersoy et al. transaction advertisement: same family as chen-2013-sybil and zhang-2023-collusion; left for a later pass to keep the lane to about 25.
- Nag 2025, Sybil proofness in competitive combinatorial exchanges (arXiv 2512.10203, FC26 poster): abstract read; dropped for count, worth adding.
- Guo and Conitzer, false-name-proofness with bid withdrawal (arXiv 1208.6501), Sakurai et al. deep false-name-proof auctions (2019), Fioravanti and Masso false-name-proof voting under separable preferences (2024), Bonifacio and Fioravanti (2026), Iwasaki et al. hiring a team (arXiv 1106.2378), Sonoda et al. facility location (AAAI 2016), Nehama et al. facility location on graphs (2022), Landa et al. Sybilproof indirect reciprocity (INFOCOM 2009), Seuken and Parkes Sybil-proof accounting with transitive trust (2014), Shahaf et al. Sybil-resilient reality-aware social choice (IJCAI 2019), Lenzi 2024 Sybil-resistant voting (arXiv 2407.01844), Hu et al. 2026 "Dissociative Identity: language model agents lack grounding for reputation mechanisms": seen in search or citation lists only, not opened.
- Detection-side airdrop papers (Kaczynski and Wiacek 2026, Sun et al. 2026, Liu et al. arXiv 2505.09313): ML Sybil detection belongs more to the detection lanes; only liu-2022-fighting added as a pointer.

**What is still thin.**
- No full reads of the referral-mechanism papers (Drucker and Fleischer, Chen et al. 2013) or of Cheng and Friedman; all are abstract-level.
- Retroactive public goods funding (Optimism RetroPGF) and Gitcoin passport-style identity scoring: not searched in this pass.
- Hu et al. 2026 on LLM agents and reputation, and the BrunoMazorra LLMs-Sybils experiments, are the only direct LLM-agent links; the paper PDF in that repo was not read.
- Flashbots-affiliated mechanism work beyond pan-2024-sybil (for example Schlegel and Mamageishvili on other auctions) was not searched in this lane; the Flashbots lanes should cover it.
- Semantic Scholar citation chasing should be rerun when the rate limit clears.
