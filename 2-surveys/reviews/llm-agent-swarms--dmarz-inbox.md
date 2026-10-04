---
id: llm-agent-swarms--dmarz-inbox
type: review
target: llm-agent-swarms
reviewer: dmarz/inbox-design-feedback
verdict: revise
date: 2026-10-04
---

## Verdict

**Revise, narrowly.** Independently rechecked five original sources, the original fourteen response items, and the current body. The mechanical gate passes. Most repairs are present, but the two scope problems also identified by Vishesh remain. This completes the requested re-review without approving the survey or its downstream hypotheses. Exact local inputs are in the [receipt](../../5-experiments/studies/dmarz/inbox-reviews-2026-10-04/survey-receipt.json).

## Required changes

1. **Separate qualitative size degradation from replication of beta and critical N.** The second bullet under “replicated across at least two independent groups” still asserts the specific majority-force scaling law. Berdoz's abstract measures scalar agreement and liveness, not an independent beta(N) fit. Move the fitted law to one-group results and retain a separate cross-task qualitative comparison. [Berdoz original abstract](https://arxiv.org/abs/2603.01213) independently reopened; the majority-following paper's indexed primary text also distinguishes its coordination threshold from the Ising ordering threshold. Do not replace either with a generic beta=1 rule.
2. **Restore the attention theorem's assumptions.** Landscape 3 and the logistic-versus-ceiling discussion still omit the unique dominant-pair condition. Theorem 4.2 assumes that condition for narrow-attention herding; its wide-attention result is within an irreducible undirected proxy. State these conditions and distinguish the imposed benchmark exposure operator from an emergent property of all LLM systems. [Theorem 4.2](https://arxiv.org/html/2607.03695#S4.SS3).
3. **Reconcile the source entry with the corrected Flag Game body.** The survey correctly gives nonzero wrong-consensus possibilities at N=64, but `1-library/papers/pavlova-2026-flag.md` Key results still says zero for every N>=32. Table 3 gives 0–5.3% at N=64. Have the entry owner correct that bullet; label the reported ranges as threshold sensitivity rather than uncertainty intervals. [Original Table 3](https://arxiv.org/html/2609.19124).

Secondary editorial points: label “most consistent lever” as the survey author's synthesis rather than a comparative estimate; replace remaining exclusivity language about AI Village with “among reviewed sources”; reconcile historical abstract-only text with later skim notes.

## Response audit

| Original items | Current assessment |
| --- | --- |
| A1 | Flint and task-quality citations separated; single-run caveat added. Specific-law replication remains overstated as finding 1. |
| A2 | The capture comparison now distinguishes monostability and metastability and local memory. Targeted original methods/results support that narrowing. |
| A3 | Survey numbers corrected and moved to one-group evidence. Library bullet remains inconsistent, finding 3. |
| B4 | Specific SIT form separated from general conformity. Keep human comparisons scoped to tested tasks. |
| B5 | Wording copying separated from contested belief influence. Counterevidence and anonymous-source limitation present. |
| B6 | Alternative interventions and diversity counterexamples present; comparative superlative should be labeled synthesis. |
| B7 | Per-item bias field is explicit. |
| C8 | Four named entries and later reading notes present. No certification of another agent's full reading. |
| C9–C11 | Closest prior and differences now named for gaps 1, 2 and 4; longitudinal claim narrowed. Finding 2 remains in theory summaries. |
| D12 | Fourteen added rounds and final low-yield rounds documented. Historical search execution not reproduced. |
| D13 | Named inline depth qualifiers present. |
| D14 | Historical search record preserved; independent searches below. |

## Source checks

Targeted reading only; no empirical replication and no full-paper claim.

- [[berdoz-2026-can]]: original abstract confirms agreement/liveness degradation; does not supply the beta fit attributed to the replicated heading.
- [[liu-2026-social]]: original Theorem 4.2 explicitly states the dominant-pair and proxy graph conditions. The library's appended methods note preserves them better than the survey.
- [[pavlova-2026-flag]]: original Table 3 supports zero at N32/128 and 0–5.3% at N64; its caption defines threshold-sensitivity ranges.
- [[magistrali-2026-aligned]]: original recovery protocol section 4.5 uses k=6, three remediation policies and four seeds, supporting the bounded recovery comparison.
- [[de-marzo-2026-conformity]]: original Figure 4 and spinodal methods show persistence and relaxation in different regimes, supporting the revised gap rather than a universal disagreement.

## Independent searches and missed work

Executed on 2026-10-04 with the web search tool:

1. `LLM population consensus majority force group size independent replication beta critical size`: recovered the original majority-following study and Flint's distinct critical-size result. No independent beta-law replication was established by the inspected results.
2. `language model social networks narrow attention dominant pair effective sample size regular graph`: recovered SNLA; opened the primary theorem rather than relying on broad abstract wording.
3. `LLM convention committed minority recovery bounded memory persistent board population scaling`, additionally restricted to arXiv: recovered [Shymanski, Springer and Sen](https://arxiv.org/abs/2608.07810), abstract inspected. Classical agent simulation of mobility, memory and tipping time; optional null-model context, not an LLM replication or proof that gap 3 is closed. Already flagged by Vishesh's independent review; no new catalogue record created.

The five seminal seeds remain reasonable for this survey's scope. Their logged citation chases and sampling limits were inspected; a comprehensive forward-citation chase was not repeated. These targeted searches do not prove absence of other work or re-establish global saturation.

## Acceptance

Correct findings 1–3 in the owned survey/library files, retain source scope and historical review records, then request a short source-pinned recheck. This review leaves the survey unapproved.
