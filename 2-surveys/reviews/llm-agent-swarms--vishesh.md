---
id: llm-agent-swarms--vishesh
type: review
target: llm-agent-swarms
reviewer: vishesh/codex-independent-reviews
verdict: revise
date: 2026-10-04
---

## Checklist

- [x] Spot-checked at least 5 cited entries against original sources (eight listed below).
- [x] Ran at least 3 independent searches and listed relevant omissions below.
- [ ] Seminal works are right, and their forward citations were followed: the existing search log was inspected, but this reviewer did not repeat its full citation chase.
- [ ] Claims are cited; measured results are separated from inference: two remaining scope corrections are required below.
- [ ] (hypothesis) Not applicable; no formal hypothesis reviewed.
- [ ] (experiment) Not applicable; no experimental acceptance granted.

## Verdict

**Revise, narrowly.** Most of the original review has been addressed. Two claims still overstate the strength or domain of their evidence. Correct them before a passing survey review. This is a separate vishesh review requested by the user; dmarz's assigned re-review and existing review file are preserved.

Reviewed survey SHA-256 is recorded in the linked [review receipt](../researchers/vishesh/notes/independent-reviews-2026-10-04/survey-receipt.json). `lab.py gate llm-agent-swarms` passes the mechanical gate. That does not settle the substantive issues below.

## Required changes

**R1 — split a replicated qualitative pattern from a specific fitted scaling law.** In `What is known`, the second bullet remains under “replicated across at least two independent groups” and asserts that majority force beta falls with N and produces a model-specific N_c. [[berdoz-2026-can]] supports worsening valid scalar agreement/liveness as group size increases; its inspected abstract does not establish replication of the beta(N) law or its N_c. The survey itself records only abstract access. The corrected removal of Flint/Qian from this bullet is good, but substituting a different endpoint does not independently replicate the fitted law. Put the beta/N_c measurement under its measured group and describe Berdoz as qualitative convergence evidence from a different task. Alternatively supply a source passage establishing an independent beta(N) fit. [Original abstract](https://arxiv.org/abs/2603.01213).

**R2 — preserve the assumptions of the attention-width theorem.** The Landscape and logistic-versus-ceiling discussion summarize [[liu-2026-social]] as bounded effective N under narrow attention, without the decisive dominant-pair/hub assumption. Theorem 4.2 explicitly requires a unique dominant pair for that bound; Table 4 reports no floor for the regular graph. Its wide-attention expression is derived within an undirected irreducible proxy, where degree regularity yields N_eff=n; this is not a global impossibility theorem for all directed systems. Amend those sentences to state the proxy, dominant-source and graph assumptions, and separate the operator-controlled empirical benchmarks from a general law of LLM attention. The library's appended note already captures these limits better than the survey. [Theorem and Table 4](https://arxiv.org/html/2607.03695).

## Original response audit

| Item | Assessment |
|---|---|
| A1 | Flint removed, units separated, single-run caveat present. Remaining R1 above. |
| A2 | Resolved in substance: comparison now distinguishes regimes and locality/memory. Source passages support this narrower question. I inspected relevant sections, not every supplement. |
| A3 | Numbers match Flag Game Table 3; moved to one-group evidence. Add that ranges are threshold-sensitivity ranges, not confidence intervals. |
| B4 | SIT functional form moved to one group. The broader human comparison should stay tied to the specific tasks tested; no universal human/LLM ordering follows. |
| B5 | Wording and belief copying separated; conflicting observational findings retained. |
| B6 | Other useful interventions and diversity counterexamples added. “Most consistent” remains a narrative synthesis, not a systematic comparative estimate; label it as such. |
| B7 | Per-item bias field is now explicit. |
| C8 | The four load-bearing entries exist with appended methods/results notes and skim labels. Access to Itkin HTML failed in this review; its central warning was verified at abstract depth only. |
| C9 | Gap 1 names closest prior and differences; this remains a bounded search conclusion, not proof of absence. |
| C10 | Gap 4 distinguishes qualitative overhead from the proposed N_eff/placebo measurement; longitudinal exclusivity removed. Apply R2 to theoretical support. |
| C11 | Second diagnostic and prior-bias caveat added. No additional full-text verification of these two sources by this reviewer. |
| D12 | Search log and saturation section now cover the correlated-error vocabulary. I verified the record, not execution of the author's historical searches. |
| D13 | Inline depth qualifiers are present at the named locations. This review does not certify other agents' claimed full reading. |
| D14 | Original reviewer search record preserved; new independent searches below. |

Additional editorial corrections: label Flag Game numeric ranges as endpoint-threshold sensitivity; remove stale Search-log prose saying the now-catalogued Chirper/Moltbook items were not catalogued; soften Gap 5's remaining “only task-oriented…” wording to “among sources reviewed.” These are secondary to R1/R2.

## Original-source spot checks

No source below was reproduced empirically. “Targeted sections” means reading the stated passages, not a full-paper read. Existing library ownership/read-depth fields were not edited.

| Entry | Source and reading scope | Check |
|---|---|---|
| [[magistrali-2026-aligned]] | [HTML](https://arxiv.org/html/2608.22444), abstract, protocol and recovery sections | Recovery protocol is local and memory-bounded, with the reported recovery experiment at k=6 and four seeds. Supports narrowing the comparison rather than universal reversibility. |
| [[de-marzo-2026-conformity]] | [HTML](https://arxiv.org/html/2605.10721), Fig. 3 discussion and spinodal methods | Persistence versus relaxation depends on the bistable versus monostable regime. Revised comparison is supported. |
| [[pavlova-2026-flag]] | [HTML](https://arxiv.org/html/2609.19124), run settings and Table 3 | Wrong consensus is zero at N32/128 and 0–5.3% at N64. Ranges vary classification thresholds, not sampling uncertainty. |
| [[liu-2026-social]] | [HTML](https://arxiv.org/html/2607.03695), Theorem 4.2 and Table 4 | The conditional theory supports the qualified claim; R2 is needed in the survey. |
| [[itkin-2026-local]] | [Abstract](https://arxiv.org/abs/2609.35813); HTML unavailable | 9,455 trajectories, 16 settings, and nonconfirmation on 24 new statements support caution about collective validation. Detailed numerical intervals not independently rechecked. |
| [[li-2026-socialization]] | [HTML](https://arxiv.org/html/2602.14299), section 5.3 | Post-interaction drift is compared with random contemporaneous posts; no measurable mean alignment supports the stated counterevidence. |
| [[hashemi-2026-empirical]] | [HTML](https://arxiv.org/html/2602.03775), section 4.2 | Sixfold neighbor similarity over a year is reported. Survey correctly labels this observational. It is not an isolated causal treatment. |
| [[berdoz-2026-can]] | [Abstract](https://arxiv.org/abs/2603.01213) | Agreement and liveness results support a qualitative group-size limit, not the specific beta law in R1. |

## Independent searches and missed work

Searches on 2026-10-04 UTC using the web search tool, with primary-source results inspected:

1. `LLM agents correlated errors ensemble effective number independent votes debate`. Found [[kohli-2026-nine]], [[he-2026-minority]] and [[kraidia-2026-when]] already in the library; the latter already supports the survey. Minority Sentinel is a possible additional countermeasure example, not a new population scaling result.
2. `LLM naming game committed minority tipping recovery memory metastability`, refined to `site:arxiv.org LLM committed minority recovery bounded memory tipping`. Found [Shymanski, Springer and Sen, Mobility, Memory, and Network Structure in Agent-Based Models of Convention Tipping and Convergence](https://arxiv.org/abs/2608.07810). Abstract opened; no matching arXiv ID in the local library. Classical simulation, not LLM replication: useful null-model context for the proposed locality/memory study, not evidence that Gap 3 is closed.
3. `LLM social networks herding wisdom crowds collective fidelity replication`, refined to `site:arxiv.org LLM collective fidelity socialization herding attention`. Recovered Liu and Itkin, plus [de Arruda et al., Collective cooperation without individual fidelity in LLM agents](https://arxiv.org/abs/2606.30454). Abstract opened; no matching ID in the library. Macro–micro mismatch is useful validation context, although its human-surrogate question differs from forecasting an LLM society.

The two uncatalogued records are optional additions with abstract-only access, not newly created library entries. This targeted search does not re-establish complete saturation. No new contradiction to the revised capture comparison was established.

Acceptance: address R1 and R2 in the body, retain the narrower claims and access limits, then seek a short re-review. Do not mark this survey reviewed or accept hypotheses on the basis of this revise verdict.
