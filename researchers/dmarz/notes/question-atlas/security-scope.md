# Security, identity, and detection candidate scope

**HUMAN-REQUESTED UNREVIEWED HUNCHES.** This file and `security.json` are a brainstorming collection for human selection. They are not accepted hypotheses, a completed survey, or permission to run experiments. The user explicitly requested broad questions, related hypotheses, and ways to test them before human review. Keeping these candidates under the researcher's notes follows the repository's hunch provision. Formal promotion still requires the appropriate survey and independent review.

The collection contains 36 candidates: SEC-01–12 for `fork-merge-security`, SEC-13–24 for `sybil-resistance`, and SEC-25–36 for `swarm-detection`. Each has a falsifiable direction, test sketch, comparators, separate utility and failure measures, confounds, prerequisites, and two or three existing source records. No study was run, no new source records were added, and no source read-depth field was changed.

## What this pass inspected

Read the repository protocol and dmarz directives; inspected the current pre-experiment synthesis, fork-merge synthesis, Sybil/Flashbots synthesis, detection taxonomy, and the fork-merge and Sybil survey status, gaps, tools, and saturation sections. The large existing syntheses were read selectively, not audited line by line. Read summaries, methods/limitation excerpts, or source metadata from 57 cited library entries. Existing entry read-depth labels describe the original cataloguing agents' work; they do not mean this pass independently read all 57 underlying papers.

Reopened these primary anchors to check the candidate framing:

- [BadMerging](https://arxiv.org/html/2408.07362): abstract, introduction, and threat-model framing. It concerns weight-space merging and supports keeping that object distinct from returning text reports. No training procedure was reproduced.
- [MemTX](https://arxiv.org/html/2607.23929v1): protocol and typed-repair passages. The primary text explicitly limits repair to recorded provenance and distinguishes compensation bookkeeping from environment replay. Its action gate is not a guarantee that every action parameter derives from safe beliefs.
- [BuilderNet refunds](https://buildernet.org/docs/refunds): the published flat-tax and identity-constraint definitions. The page warns that the rule described is indicative and actual implementation includes modifications. SEC-14 transfers a published mechanism idea into a toy task setting; it does not claim to replicate current production behavior.
- [On Sybil-Proof Mechanisms](https://arxiv.org/html/2407.14485v5): abstract, introduction, and the boundaries of the stated single-parameter result. Its theorem does not automatically apply to every task allocator or every multi-good environment.
- [Beyond Interaction Patterns](https://arxiv.org/html/2502.17344): matched organic controls, test definition, evaluation, and limitations. This provides a concrete caution against inferring coordination from raw similarity without a relevant null comparison.
- [Simplistic Collection and Labeling Practices](https://arxiv.org/abs/2301.07015): primary abstract alongside the fuller repository record; no independent reanalysis of its datasets.
- [Identifying AI Web Scrapers Using Canary Tokens](https://arxiv.org/html/2605.13706): attribution setup and inference robustness passages, including false matches, missed emissions, and intermediary routing. These motivate separating content exposure from operator ownership.
- [Black-Box Forensics](https://arxiv.org/abs/2606.22698): primary abstract alongside the repository record. Same-prompt linking is not treated as verified same-operator identification.

These were targeted framing checks, not full reads of every method, exhaustive novelty searches, or closure of the existing survey gates.

## Boundaries carried into the candidates

- Classical Byzantine agreement permits arbitrary coordinated faults within its fault bound and message assumptions. It does not assume independent coin-flip failures, and agreement is not factual truth. An older sentence in the fork-merge synthesis remains overly broad; this collection follows the correction in the pre-experiment synthesis and the appended Lamport note.
- Returning a text report, changing persistent memory, changing permissions, and merging model weights are separate experimental objects. SEC-09 concerns small isolated classifiers only. None of the other candidates borrows its threshold or security guarantees.
- True dependency graphs, operator labels, and coalition ownership can be evaluator ground truth or explicitly privileged ceilings. They are never silently available to the evaluated policy. Access logs show retrieval, not necessarily causal semantic dependence.
- Rejection, abstention, isolation, and memory reset can appear safe by eliminating usefulness. Every intervention sketch includes legitimate task performance or another explicit cost of that behavior.
- Per-key or per-credential rate limits do not establish one-person-one-agent. Resource conservation, credential issuance, delegation, shared infrastructure, and multiple radios are distinct assumptions.
- Model attribution, prompt attribution, common ownership, coordinated behavior, and harmful intent are different targets. A shared model or a shared cloud service does not by itself establish any of the latter three.
- Synthetic prevalence scenarios test review-queue behavior; they do not estimate wild agent prevalence. Paired sessions and messages within one interacting episode are not independent replicates.
- All proposed adversarial conditions use synthetic data, controlled local systems, or authorized test setups. Canary sketches use fictional local facts. Market sketches use simulated value and payments. No live attacks, covert tracking, external messages, or production financial actions are proposed.

## Remaining caveats before selection

Several load-bearing neighboring records remain abstract-level, including shared-memory honeytoken theory, the personhood analysis, survey-assistance studies, and the bot realism study. Candidates citing them identify that limitation and ask for full-method checks before promotion. The formal mechanisms, privacy constructions, and attestation semantics also need specialized review if selected; a simulation using ideal primitives cannot validate real cryptographic security.

The novelty tags classify intended study type, not verified novelty. Replication and boundary tests are included deliberately. The broad older synthesis claims that no one has studied particular agent settings remain bounded by their search coverage and are not repeated as established absence claims here.

Some overlap with memory, quorum, regrowth, external influence, robotics, and measurement candidates in other lanes is intentional. Human review should merge duplicates by causal question rather than select two variants merely because they use different terminology. Particularly strong cross-links are SEC-03 (evidence versus identity), SEC-06–07 (repair and stale returners), SEC-08/13 (attention budgets), SEC-25/27 (what detection identifies), and SEC-30/34 (measurement under scarce or incomplete observations).

The exact review thresholds, sample sizes, cost ceilings, permitted hardware, and access arrangements remain to be specified after human selection. Hardware and human-participant sketches are explicitly marked as requiring those resources; they are not immediately runnable commitments.
