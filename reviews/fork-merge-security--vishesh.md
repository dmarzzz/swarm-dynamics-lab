---
id: fork-merge-security--vishesh
type: review
target: fork-merge-security
reviewer: vishesh/fm-security-review
verdict: revise
date: 2026-10-04
---

## Verdict and scope

Revise. The survey is a useful cross-community map, and the checked headline attack results largely survive source inspection. Its threshold interpretation, one experimental extrapolation, citation metadata and coverage chronology need correction before a passing research review.

Reviewed survey revision `322f69c129744781c4a4e70483b4490b1c43f27a`, initially read in repository snapshot `1aeccb259dbe538fe25cf50a022c629c0aa92c1d`. Line numbers below refer to that survey revision. This is a targeted literature review, not an independent reproduction of attacks, a full audit of 283 references, or experiment approval. No paid experiment ran. No author's read-depth field was upgraded.

## Checklist

- [x] Five cited sources checked against accessible primary material: DBA, Cerberus, BadMerging, Consensus Trap and Lamport. Required sixth check, Zhai, found a metadata defect; primary full-text access remained blocked.
- [x] Three independent searches with different wording, recorded below.
- [x] Seminal choices and documented forward-chase coverage inspected; not an independent replay of all citation queries.
- [ ] Claims consistently distinguish theorem assumptions, measurement and inference: revisions R1-R3 required.
- [ ] Coverage chronology is internally consistent: R4 required.
- Hypothesis novelty and experiment protocol checkboxes are not applicable to this survey.

## Required revisions

### R1 — Do not make statistical independence a universal threshold assumption

**Priority: high. Locations: survey lines 130, 183 and 267; related entry `lamport-1982-byzantine`.**

The Q2 framing and claim that every threshold assumes independence conflate statistical voting gains with worst-case Byzantine guarantees. Lamport's Theorem 1 bounds the number of arbitrary traitors; Section 4 explicitly permits collusion. Correlated compromise can exceed the fault budget, but does not invalidate the theorem while its budget and protocol assumptions hold. Agreement also does not establish the factual truth of an agent report. The library already carries this correction under dmarz/preflight's note.

**Correction:** separate bounded Byzantine faults, honest-output statistical assumptions, and independent-principal requirements of particular defenses. State the actual assumptions for each transfer to agents. Do not present ordinary majority voting over free text as Lamport's protocol. [Primary source, Sections 3-4](https://lamport.azurewebsites.net/pubs/byz.pdf).

### R2 — Keep the sampling result distinct from a fork-count experiment

**Priority: medium. Location: survey line 241.**

The 46.2% to 25.9% figures are supported, but “more forks made it worse” changes the manipulated variable. Consensus Trap Appendix D.1 varies sampled trajectories M from 1 to 40 for the fixed 3-corrupted/2-truthful configuration, using a precomputed response pool and bootstrap trials. It does not measure increasing the number of separately forked agents.

**Correction:** describe repeated response sampling under the fixed corruption mixture. Mark transfer to fork-count scaling as an inference requiring its own experiment. Preserve the strong-injection condition. [Primary source, Appendix D.1](https://arxiv.org/html/2604.17139#A4.SS1).

### R3 — Repair the new entries and keep guarantees within checked evidence

**Priority: medium. Locations: `library/papers/zhai-2024-secret.md` lines 8 and 11; `lyu-2023-poisoning.md` line 36; `xie-2020-dba.md` line 27; survey line 163.**

- Zhai's DOI is valid, but IEEE's deposited Crossref record gives pages **5060-5074**, not 4482-4497, and its full-text link identifies **10504302**, not the stored 10502325. Title, seven authors and year match. Correct the bibliographic record and use the DOI as the stable link. IEEE returned a browser challenge, so this review does not certify the paper's proofs or the survey's transfer of per-leader communication complexity to arbitrary committee-member cost. Preserve abstract-depth qualification and specify communication cost, not unqualified cost. [Publisher-deposited metadata](https://api.crossref.org/works/10.1109/TIFS.2024.3390584), [DOI](https://doi.org/10.1109/TIFS.2024.3390584).
- Cerberus used two image datasets and LOAN credit-risk data; the entry incorrectly calls all three image benchmarks. Its 3-dataset/13-defense headline and coordinated trigger/model-deviation mechanism are supported. Correct the dataset description. [Primary PDF, Experimental Evaluation/Table 1](https://ojs.aaai.org/index.php/AAAI/article/view/26083/25855).
- DBA's abstract supports trigger decomposition and evasion of two tested robust FL algorithms. It does not establish the entry's universal assertion that per-part inspection sees nothing malicious or that only the merged model exhibits the behavior. Narrow this to the measured defense setting, or supply a body-level experiment for that stronger claim. [Author-institution abstract](https://research.ibm.com/publications/dba-distributed-backdoor-attacks-against-federated-learning).

### R4 — Reconcile the coverage chronology and bound absence claims

**Priority: medium. Locations: survey lines 291-300 and 303-310.**

The current gate passes, yet line 307 still says its tail fails, and line 308 says Bagdasaryan was not forward-chased. The frontmatter, status banner and shadow/sol-fm's October 4 log report the later 805-citer chase and passing tail. Label those older statements historical and identify remaining coverage gaps separately.

The broad absence claims also need a search/date/scope qualifier. The text itself reports unfinished mobile-agent and agent-specific unlinkability coverage; two low-yield committee/FL rounds do not establish saturation across all those lanes. Use “not found in the documented search” and define what counts as an end-to-end agent fork/merge. This revision does not require exhausting every neighboring field or treating rate limits as misconduct.

## Source spot-checks

| Cited entry | Material actually checked in this review | Outcome |
|---|---|---|
| [[xie-2020-dba]] | IBM Research author-institution abstract and authors; OpenReview forum/PDF challenged | Core abstract claims supported; stronger per-part invisibility claim needs narrowing (R3). No full-text claim. |
| [[lyu-2023-poisoning]] | AAAI publisher abstract, metadata, PDF experimental setup and Tables 1-2 | Core mechanism and evaluation scope supported; dataset error confirmed (R3). Selected sections only. |
| [[zhai-2024-secret]] | IEEE URL attempted; DOI-specific publisher-deposited Crossref metadata retrieved | Wrong pages and mismatched IEEE record confirmed. No accessible primary abstract/full text, so theorem/complexity claims remain unverified here. |
| [[zhang-2024-badmerging]] | arXiv HTML experimental setup and Tables 2, 3, 6 and 8 | On-task five-algorithm values and 8-task ASR above 92% supported. Entry's “above 90% for other target classes” needs qualification: Table 8 includes Acura Integra Type R at 86.82%. This is CLIP image classification, not decoder-agent evidence. |
| [[liu-2026-consensus]] | arXiv HTML Sections 3-4, Proposition 1 and Appendix D.1 | Headline values supported; R2 corrects the survey's extrapolation. Proposition requires anonymous **and symmetric** outcome aggregation and its stated corruption condition; retain those qualifications. |
| [[lamport-1982-byzantine]] | Author-hosted PDF message assumptions, Theorem 1, signed-message construction | Threshold result supported; universal independence claim contradicted (R1). |

BadMerging primary source: [experimental tables](https://arxiv.org/html/2408.07362). The two requested dmarz full-read entries checked were BadMerging and Consensus Trap. Their existing `full` labels describe the original cataloguers' work, not this review's selected-section checks. I cannot retrospectively certify what another reader opened.

## Independent searches and missed work

All searches ran October 4, 2026 through web search. Counts are not reported as saturation statistics: ranked search output is not an exhaustive corpus.

1. `LLM fork join subagent summary merge prompt injection benchmark security`: returned ASB and the UK AISI agent-security competition/ART material among broader benchmarks. ASB is already cited. No retrieved result alone established a direct end-to-end counterexample to the narrowly defined fork/merge gap. Search snippets were not treated as empirical verification.
2. `Byzantine quorum correlated failures independence adversarial faults model merging`: surfaced **The Honest Quorum Problem: Epistemic Byzantine Fault Tolerance for Agentic Infrastructure**, Jun He and Deying Yu, arXiv:2607.16109. I opened the [primary arXiv abstract](https://arxiv.org/abs/2607.16109); no match for its title/id was found in the library or survey. It directly separates agreement from semantic correctness and proposes bounds for correlated invalid endorsements. Add or explicitly scope out this relevant theoretical neighbor. Abstract-only candidate, not a validated empirical defense and not yet catalogued as a library entry.
3. `secret committee selection adaptive adversary hidden identities agent fork merge`: returned mixed blockchain, agent-fork documentation and commercial material. No new experimentally validated hiding defense was established. Targeted follow-ups for Zhai's title/IEEE identifier led to the R3 metadata check; they did not overcome primary full-text access limits.

## Seminal coverage and gate evidence

The seven seminal choices cover the declared historical branches. Existing lane records document forward chasing for Sander, SSLE, BadMerging, Greenblatt, Perez, Buss and Korzhyk, with pagination/title-filter limits. Checked evidence resides in `tasks/scan-papers-fm-{mobile-agents,unlinkability,merge-poisoning,ai-control,identity-hijack,biology}.md` and `researchers/dmarz/notes/fm-gap-2.md`. The later Bagdasaryan/Christiano work is in `researchers/shadow/log/2026-10-04-sol-fm.md`. These are recorded searches, not independently reproduced citation counts.

`lab.py gate fork-merge-security` passed. Repository validation before filing reported 0 errors and 5 pre-existing unresolved-reference warnings. A mechanical pass is retained separately from this **revise** verdict. A focused re-review can clear R1-R4 without repeating the entire survey; no new experiment or second unrelated approval is requested.
