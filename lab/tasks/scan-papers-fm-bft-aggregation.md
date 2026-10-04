---
id: scan-papers-fm-bft-aggregation
type: task
title: 'Catalogue the papers: Byzantine thresholds for merging (BFT, robust aggregation, design diversity)'
kind: scan
status: claimed
priority: p0
owner: dmarz/fm-bft-aggregation
for: null
created: 2026-10-03
created_by: dmarz/fm
depends_on: []
topics:
- fork-merge-security
- sync-consensus
claimed_at: 2026-10-03T18:12Z
updated: 2026-10-03T18:12Z
---

## Goal

Context from dmarz: Richard Sutton has suggested that an agent with many resources will likely split into parts that go off (for example to explore a distant information domain) and later merge back. Attack surface: corrupt one part so that when it merges back it corrupts the parent. Questions: (1) how a parent can hide which sub-agent or swarm it will reintegrate; (2) whether a Byzantine-style threshold or protocol can force an attacker to corrupt k of n parts; (3) what the strongest attack vector is (for example prompt injection that overwrites a sub-agent memory so it takes on another agent identity and cuts others out). This task: question (2).

## Done when

- At least 15 entries catalogued with topic `fork-merge-security`, including every review article found.
- At least 4 read in full.
- Coverage note filled and `python3 scripts/lab.py check` passes.

## Coverage note

Filled by dmarz/fm-bft-aggregation, 2026-10-03.

**Result.** 36 new library entries tagged fork-merge-security, plus `## Notes from dmarz/fm-bft-aggregation` (and the topic tag where missing) on 8 existing entries: [[lee-2026-robust]] (read in full; notes carry the measured numbers), [[jo-2025-byzantine]], [[leblanc-2013-resilient]], [[huang-2024-resilience]], [[luo-2025-weighted]], [[bara-2026-epistemic]], [[yang-2026-sok]] (review article), [[li-2026-when]]. Read in full: [[kim-2025-correlated]], [[liu-2026-consensus]], [[lee-2026-robust]], [[knight-1986-experimental]], [[narang-2026-inference]], [[shamir-1979-share]] (6). Review articles found and catalogued or noted: [[guerraoui-2024-byzantine]] (Byzantine ML primer, ACM CSUR), [[yang-2026-sok]] (SoK on multi-agent LLM security, existing entry, noted).

New entries by cluster:
- Classical thresholds: [[lamport-1982-byzantine]], [[castro-1999-practical]], [[dolev-1986-reaching]], [[shamir-1979-share]], [[huber-1964-robust]].
- Design diversity and correlated failure: [[avizienis-1985-n-version]], [[knight-1986-experimental]], [[ron-2026-n-version]], [[nogueira-2026-systematic]], [[almeida-2026-effectiveness]].
- Byzantine-robust aggregation (ML): [[blanchard-2017-byzantine]], [[yin-2018-byzantine]], [[el-mhamdi-2018-hidden]], [[alistarh-2018-byzantine]], [[baruch-2019-little]], [[xie-2019-fall]], [[karimireddy-2020-learning]], [[karimireddy-2020-byzantine]], [[allen-zhu-2020-byzantine]], [[cambus-2025-approximate]], [[guerraoui-2024-byzantine]].
- LLM error correlation and voting limits: [[kim-2025-correlated]], [[goel-2025-great]], [[li-2026-state]], [[chen-2026-when]], [[denisov-blanch-2026-consensus]], [[tieman-2026-inferred]], [[alavi-2025-more]].
- LLM Byzantine protocols and merge gates: [[liu-2026-consensus]], [[zheng-2025-rethinking]], [[xu-2026-certifiable]], [[berdoz-2026-can]], [[nilayam-2026-heterogeneous]], [[narang-2026-inference]], [[lin-2026-beyond]], [[bu-2026-re-derivability]].

**Main finding for Q2 (separating measured from inferred).** Classical results give clean k-of-n thresholds: n >= 3f + 1 for unauthenticated agreement, any n with signatures ([[lamport-1982-byzantine]]); n >= 3t + 1 synchronous and 5t + 1 asynchronous for approximate agreement ([[dolev-1986-reaching]]); n > 2f + 2 for Krum ([[blanchard-2017-byzantine]]); breakdown point of one half for the median (standard robust statistics; framing in [[guerraoui-2024-byzantine]], body not read). Every one assumes faults are independently caused. Measured: that assumption failed for human N-version programs (z = 100.5, [[knight-1986-experimental]]), fails for coding agents (429 vs 115 coincident failures, [[ron-2026-n-version]]; 0.43 of the independence gain, under 0.3 within one model, [[nogueira-2026-systematic]]) and for LLM answers (agreement-when-both-wrong 0.60 on HELM, rising with accuracy, [[kim-2025-correlated]]). Proved: correlated errors give majority voting a positive error floor ([[li-2026-state]]); outcome-level voting cannot be robust to both minority and slight-majority corruption ([[liu-2026-consensus]]). Measured: under a shared injected directive, adding votes makes majority voting worse (46.2 to 25.9 percent over 1 to 40 votes, [[liu-2026-consensus]]). Constructions that change the merge rather than the count do better in the papers' own tests: MSR filtering on (F+1, F+1)-robust graphs with receiver-side scoring ([[lee-2026-robust]]), per-token quorum over separately kept parts instead of weight averaging ([[narang-2026-inference]]), token-level interleaving ([[liu-2026-consensus]]), effective-independent-source counting for memories ([[lin-2026-beyond]]). Inferred, not measured anywhere found: how these behave when many forks of one model ingest the same adversarial content, which is the fork-merge case.

**APIs and rate limits.** Semantic Scholar search and batch returned 429 for most calls (shared IP with parallel swarms); citation endpoints worked on retry. OpenAlex daily budget exhausted (no key). arXiv export API returned 429; arXiv abs and HTML pages worked and were used for metadata and full text. Crossref worked for DOIs. Classical PDFs fetched from author or course sites and the Wayback Machine (sunnyday.mit.edu and pmg.csail.mit.edu timed out directly).

**Rounds** (results seen / new entries):
1. Crossref bibliographic search for classical seeds (Lamport, Castro-Liskov, Dolev et al., Shamir, Avizienis, Knight-Leveson, Huber): 21 / 7.
2. arXiv abs pages for Byzantine ML seeds named in the brief (Krum, trimmed mean, Bulyan, centered clipping, bucketing, SafeguardSGD, Byzantine SGD, A Little Is Enough, Fall of Empires): 9 / 9.
3. Web search, LLM vocabulary ("correlated errors", "majority voting adversarial agents Byzantine threshold", Byzantine ML primer): 28 / 8.
4. Web search for CP-WBFT, Knight-Leveson replications, Avizienis PDF: 28 / 5 (incl. two LLM N-version papers).
5. Semantic Scholar forward citations of [[jo-2025-byzantine]] (17), [[kim-2025-correlated]] (56), [[liu-2026-consensus]] (7), [[lee-2026-robust]] (10): 90 / 9.
6. Web search, model-merging and software-diversity vocabulary (Byzantine model merging, Galapagos N-version): 18 / 1.
7. Semantic Scholar keyword searches in neighbouring vocabularies (model merging, N-version LLM, threshold cryptography for agents, self-consistency robustness): blocked by 429, 0 / 0.
Last two productive rounds found 9/90 (10 percent) and 1/18 (6 percent) new.

**Found but not added** (seen in listings, not opened or out of lane): Galapagos automated N-version programming (arXiv 2408.09536); Model Merging in the Era of LLMs survey (2603.09938; belongs to fm-merge-poisoning); Be Careful Who You Trust, corrupted communication in Stag Hunt (2609.31704); Fully Byzantine-Resilient MARL (2609.25701); Decomposing Wrong-Consensus Agreement in Self-Consistency (2608.18795); Free-MAD consensus-free debate (2509.11035); Jas AI-paired N-version (2606.07828); N-Version Assessment of Generative AI (2409.14071); Kleinberg and Raghavan, Algorithmic monoculture and social welfare (PNAS 2021, cited by [[kim-2025-correlated]]); Mendes and Herlihy multidimensional approximate agreement (STOC 2013, cited by Krum); Hampel on breakdown point; BlockAgents ([[chen-2024-blockagents]] exists but no abstract reachable, so no note added).

**Thin.** (1) No paper measures k-of-n merge robustness when the corrupted parts share an adversarial input, the core fork-merge case; all LLM correlation numbers are for natural errors. (2) Threshold signatures and verifiable secret sharing applied to agent memory commits: nothing found beyond [[shamir-1979-share]]. (3) Breakdown points for aggregating free text or memories, as opposed to vectors, are undefined in the literature found; [[xu-2026-certifiable]] is the closest. (4) Citation counts are null for most arXiv entries because Semantic Scholar was rate-limited.
