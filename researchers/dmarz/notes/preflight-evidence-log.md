# Evidence log for pre-experiment research

Author: dmarz/preflight. Date: 2026-10-03. Working research notes, not a survey or hypothesis.

User request: "okay so come up with some things to cover before we start getting our hands dirty then do it and merge it into main plz"

## Scope and repository snapshot

Started from `origin/main` at `9acb62c`. Read the local protocol, researcher directives, inbox and status; inspected the existing synthesis documents, review, and Vishesh's quorum, memory, regrowth, coordination and external-influence briefs. Earlier discussion had inspected all then-visible remote branches and PRs; by this pass the fork-merge and Sybil material was present in the starting main tree. The new synthesis belongs to task `synthesis-pre-experiment-research`.

Used an isolated branch because the user explicitly requested a merge. Registration, claim and completion use `scripts/lab.py`; branch sync runs only against that branch. No other researcher's notes, existing survey statuses, hypothesis files or experiment files are modified.

## Searches and primary-source inspection

The following is an executed search trail, not a reconstructed saturation log. Search-engine hit counts are not stable denominators; no saturation rate is claimed. All eight proposed additions returned no match through `lab.py find` using their arXiv IDs or distinguishing title phrases before creation.

| Pass | Queries or retrieval route | Outcome |
|---|---|---|
| Agent-memory predecessors | Re-opened `2609.30813`, `2605.14421`; searched `MemTX agent memory rollback`; followed CPB's reference discussion to `2607.23929` | Three missing papers catalogued. |
| Classical provenance | `Provenance semirings Green Karvounarakis Tannen 2007 pdf`; author-hosted PDF; DOI lookup | One missing paper catalogued. |
| Recovery | `survey of rollback-recovery protocols Elnozahy 2002 pdf`; author-hosted final manuscript and Crossref metadata | One missing paper catalogued. |
| Identification | Re-opened `1004.4704`; searched Aronow/Samii interference framework; followed `1305.6156` | Two missing papers catalogued. |
| Attention | `Demers Keshav Shenker analysis simulation fair queueing algorithm 1989 pdf`; university-hosted PDF and Crossref | One missing paper catalogued. |
| Existing agent controls | Re-opened primary abstracts `2410.02506` and `2609.19183` | Existing AgentPrune and capacity entries reused; no read-depth upgrade. |
| Fault assumptions | Read Lamport's author-hosted PDF, especially problem definition and message assumptions | Appended a bounded interpretive correction to the existing entry. |
| Runnable predecessors | Inspected GitHub metadata and README for `lxy1134/iclr_2027` and `lxy1134/MEMTX_` | Access and licensing limits recorded in the synthesis; no execution. |

Searches also surfaced Doyle's truth-maintenance paper, but its full text was not inspected and no new entry or substantive claim is based on it. No social search, exhaustive forward-citation chase, or independent replication was performed. This is a targeted comparison, not a replacement for the gate.

## Read-depth ledger

All eight additions are marked `skim`. None is marked `full` or `ran`.

| Entry | Material inspected |
|---|---|
| [[li-2026-benchmark]] | v1 HTML: introduction, methods, experimental setup, results, instrument figure caption, correction discussion, reproduction section, Appendix S. |
| [[ouyang-2026-memlineage]] | v1 HTML: introduction, trust assumptions, evaluation and recovery discussion, conclusion. |
| [[li-2026-memtx]] | v1 HTML: introduction, commit and repair mechanisms, invariants, evaluation tables and conclusion. |
| [[shalizi-2011-homophily]] | v3 HTML: introduction, causal examples and their descriptions, constructive responses, conclusion; not every proof. |
| [[aronow-2013-estimating]] | v4 HTML: introduction, exposure mappings, misspecification, application and conclusion; not every proof. Metadata uses the original 2013 preprint year and explicitly notes v4. |
| [[green-2007-provenance]] | Author PDF: introduction, worked examples, main construction, conclusion; not every proof. |
| [[elnozahy-2002-survey]] | Author PDF: introduction, model, checkpoint/logging examples and conclusion; recovery figure visually inspected. |
| [[demers-1989-analysis]] | University PDF: introduction, allocation unit discussion, scheduling construction, simulation figure/table and discussion; simulation page visually inspected. |

ArXiv titles and authors were read from primary metadata. Classical publication details came from the author PDFs and bibliographic records; DOI title matching is separately checked by `lab.py verify`. A broad Crossref query batch encountered HTTP 429 after two successful results. It was not treated as evidence of search exhaustion. PBFT full-text retrieval failed at the attempted endpoints, so no new empirical assertion about PBFT is added. The correction rests on the accessible Lamport source.

## Claim and scope audit

- Recommendations are labeled as inferences; no absence claim is promoted into a novelty finding.
- Source ancestry, declared ancestry, inferred ancestry and retrieved context are distinguished.
- Existing precursor mechanisms are acknowledged; their formal and empirical scopes are not expanded.
- Failure prevention, task recovery, and reversal of external effects are separated.
- Agent counts and message counts are not treated as independent sample sizes.
- Fault-count guarantees are separated from statistical independence and factual accuracy.
- Dataset checks inherited from teammates are attributed and dated, not presented as fresh downloads.
- No payloads, model trials, installations of external research code or benchmark runs were performed.

This is the author's self-audit. It is not a cross-researcher review and does not satisfy the survey-review gate. Validation command outcomes are recorded in the session log.
