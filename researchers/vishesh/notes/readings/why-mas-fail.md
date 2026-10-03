---
slug: why-mas-fail
title: Why Do Multi-Agent LLM Systems Fail?
authors: Mert Cemri, Melissa Z. Pan, Shuyi Yang, Lakshya A. Agrawal, Bhavya Chopra, Rishabh Tiwari, Kurt Keutzer, Aditya Parameswaran, Dan Klein, Kannan Ramchandran, Matei Zaharia, Joseph E. Gonzalez, Ion Stoica
org_or_venue: NeurIPS 2025 Datasets and Benchmarks Track (published); arXiv:2503.13657 (cs.AI); UC Berkeley et al.
date: 2025-03-17 (v1); v2 2025-04-22; v3 2025-10-26 (version read = v3)
status: found
fetched: 2026-10-03
urls_loaded:
  - "https://arxiv.org/abs/2503.13657"
  - "https://arxiv.org/abs/2503.13657v1"
  - "https://arxiv.org/html/2503.13657v3"
  - "https://export.arxiv.org/api/query?search_query=ti:%22Why+Do+Multi-Agent+LLM+Systems+Fail%22&max_results=10"
  - "https://proceedings.neurips.cc/paper_files/paper/2025/hash/b1041e52d3be19f0a9bc491657488e4a-Abstract-Datasets_and_Benchmarks_Track.html"
library_ids:
  - cemri-2025-why
---

## What it is (2-4 sentences)

The empirical failure-mode paper for multi-agent LLM systems. The authors hand-read 150 execution
traces (averaging **over 15,000 lines of text** each) from real open-source MAS frameworks using a
grounded-theory procedure with six expert annotators, and derive **MAST** — the Multi-Agent System
Failure Taxonomy: **14 failure modes in 3 categories**. They then validate an LLM-as-a-Judge
annotator against the human labels and use it to scale annotation to **1,642 traces** across 7
frameworks (the MAST-Data release). The sting in the tail is the intervention study: targeted fixes
(better role prompts, an added verification step) buy only **+9.4% to +15.6%** success and leave
overall completion low — so the failures are architectural, not promptable away.

## Method / setup (what they actually did; models, N, tasks, baselines)

- **Taxonomy construction (§3.1-3.2):** grounded theory on **150 traces** — open coding, constant
  comparative analysis, memoing, theorizing, run to theoretical saturation. **Six** expert human
  annotators. Three iterative agreement rounds with three expert annotators per round, refining
  MAST definitions between rounds.
- **Frameworks in the grounded-theory phase (§3.1):** HyperAgent, AppWorld, AG2, ChatDev, MetaGPT
  (five). **Frameworks in the full MAST-Data release (Table 1):** ChatDev, MetaGPT, HyperAgent,
  AppWorld, AG2, **Magentic-One, OpenManus** (seven — the latter two added as held-out
  generalization systems).
- **MAST-Data composition (Table 1, §3.4):** **1,642 annotated traces** total —
  210 traces human-evaluated + human-annotated + LLM-annotated;
  400 traces LLM-annotated only (ProgramDev-v2);
  1,032 traces human-evaluated + LLM-annotated across various benchmarks.
- **LLM-as-a-Judge (§3.3, Table 2):** judge model = **OpenAI o1**, prompted with the execution
  trace, the MAST definitions, and few-shot examples.
- **Models studied inside the MAS (abstract, Appendix F):** GPT-4o / GPT-4, Claude 3 / Claude 3.7
  Sonnet, Qwen2.5, CodeLlama.
- **Task domains:** coding, math, general agentic (ProgramDev / ProgramDev-v2, AppWorld, MathChat).
- **Baseline / comparison structure:** this is a *diagnostic* paper, so the comparisons are
  (a) framework vs framework, (b) model vs model within a fixed framework, (c) pre- vs
  post-intervention success rate in two case studies. There is no single-agent-vs-multi-agent
  performance baseline of the kind the scaling paper runs.

## Key results (numbers with units; mark each "measured" or "claimed")

- **Inter-annotator agreement — measured.** Cohen's **kappa = 0.88** in the final round (three
  expert annotators, 15 traces drawn from the 150-trace sample) (§3.2). Generalization check on two
  *new* systems (OpenManus, Magentic-One) and two new benchmarks: **kappa = 0.79** (§3.4).
- **LLM judge agreement — measured (Table 2).** **94% accuracy** against the held-out
  human-annotated set; **kappa = 0.77** with few-shot examples (vs **kappa = 0.58** without — the
  few-shot calibration is doing real work). Recall 0.77, precision 0.833, F1 0.80.
- **MAST taxonomy with measured frequencies (Fig. 1 caption / Appendix A):**
  - **FC1. System Design Issues** — FM-1.1 Disobey task specification **11.8%**;
    FM-1.2 Disobey role specification **1.5%**; FM-1.3 Step repetition **15.7%**;
    FM-1.4 Loss of conversation history **2.80%**;
    FM-1.5 Unaware of termination conditions **12.4%**.
  - **FC2. Inter-Agent Misalignment** — FM-2.1 Conversation reset **2.20%**;
    FM-2.2 Fail to ask for clarification **6.80%**; FM-2.3 Task derailment **7.40%**;
    FM-2.4 **Information withholding 0.85%**; FM-2.5 Ignored other agent's input **1.90%**;
    FM-2.6 Reasoning-action mismatch **13.2%**.
  - **FC3. Task Verification** — FM-3.1 Premature termination **6.20%**;
    FM-3.2 No or incomplete verification **8.20%**; FM-3.3 Incorrect verification **9.10%**.
  The three largest single modes are **step repetition (15.7%)**, **reasoning-action mismatch
  (13.2%)** and **unaware of termination conditions (12.4%)**. Verification failures (FC3) sum to
  **~23.5%** — about a quarter of all failures are the system not checking its own work.
- **Framework failure rates — measured.** Across the seven SOTA open-source MAS, failure rates range
  **41% to 86.7%** (Introduction; per-framework detail Fig. 5 / Appendix B). These systems fail the
  *majority* of tasks in several cases.
- **Intervention case study 1 — AG2 MathChat (§5.3, Appendix H.1) — measured.** Adding a structured
  prompt with an explicit verification section, same model and same user prompt:
  **+9.4% success rate**.
- **Intervention case study 2 — ChatDev (§5.3, Appendix H.2) — measured.** Improved agent role
  specifications (prompt only): **+9.4%** on ProgramDev. Adding a high-level task-objective
  verification step: **+15.6%** on ProgramDev. Authors note overall success "remained low" and
  failures persisted.
- **Model comparison inside one framework — measured (Fig. 8, Appendix F).** MetaGPT on
  ProgramDev-v2: **GPT-4o showed 39% fewer FC1 failures than Claude 3.7 Sonnet**; both showed high
  FC3, i.e. verification failures are model-independent.
- **Architecture comparison — measured (Fig. 9, Appendix F).** MetaGPT vs ChatDev, both on GPT-4o,
  ProgramDev-v2: MetaGPT had **60-68% fewer FC1 and FC2** failures; ChatDev had **1.56x fewer FC3**
  failures. Neither architecture dominates — they trade design failures against verification
  failures.
- **Claimed, not measured.** That the taxonomy's three categories are the right carve-up; that the
  measured headroom implies "better MAS design" is the route forward. Both are reasonable readings,
  but they are the authors' interpretation of a frequency distribution.

## Limitations the source admits + ones you noticed

**Admitted:**
- Taxonomy completeness: "We do not claim it covers every potential failure pattern" (§4).
- **Attribution is deliberately skewed toward design.** They acknowledge failures may stem from
  "fundamental limitations of current LLMs, such as hallucination or instruction following", but
  chose to focus on patterns where system design can help (§4). So MAST systematically under-counts
  base-model failures — important when reading the frequency table.
- Closed-source systems (e.g. Manus) excluded for lack of trace transparency and undisclosed
  underlying models (Appendix B.3).
- Interventions gave "limited results"; "not all failure modes are resolved, and task completion
  rates still remain low" (§5.3).
- Generalization: validated on seven open-source frameworks and two model families; proprietary or
  novel architectures untested.

**Noticed:**
- **The percentages are a distribution over *observed failures*, not over tasks.** FM-2.4
  Information withholding at 0.85% does not mean withholding is rare in agent systems — it means it
  is rarely the label an annotator assigned. Low-visibility failures (exactly the ones Telephone and
  Quorum care about) are the ones hardest to spot in a 15,000-line trace, so this table is biased
  toward *legible* failures. Treat the small numbers as a detection floor, not a base rate.
- **The LLM judge was calibrated on the same taxonomy it is scoring**, so the 1,432 LLM-annotated
  traces inherit MAST's blind spots. kappa = 0.77 is good agreement, but agreement with human
  labels on a 14-way scheme is not the same as recovering ground-truth causes.
- **Frameworks are from 2024-early-2025.** ChatDev, MetaGPT, AG2 and AppWorld are a specific
  generation of orchestration code, and the models inside are GPT-4o/Claude 3-era. Some modes
  (loss of conversation history at 2.8%; conversation reset at 2.2%) are partly artifacts of small
  context windows that 2026 models do not have. The verification modes (FC3) are the ones most
  likely to have aged well.
- **No cost or latency axis at all.** Unlike the scaling paper, nothing here tells you what a
  failure mode *costs* to fix or to tolerate.
- **The +9.4% / +15.6% deltas have no stated CI or n.** They are the paper's most-quoted numbers and
  the least statistically furnished. Use them as "small single-digit-to-mid-teens improvement", not
  as point estimates.

## Relevance to the hackathon shortlist

- **Collective Sensing (local/global/no comms, partial obs, known truth):** MAST gives you a
  **pre-built, peer-reviewed label set for scoring your traces**, which saves you inventing a coding
  scheme and makes your results legible to anyone who knows this paper. Three modes map almost
  one-to-one onto Collective Sensing's hypotheses: **FM-2.4 Information withholding (0.85%)** is
  literally "an agent held evidence it did not share" — your partial-observation setup is a
  purpose-built instrument for measuring that properly, and the paper's own 0.85% is so implausibly
  low that *re-measuring it under controlled partial observability is a contribution in itself*.
  **FM-2.5 Ignored other agent's input (1.90%)** is the "comms channel exists but does not work"
  failure that separates your local/global conditions from no-comms. **FM-1.4 Loss of conversation
  history (2.80%)** is the mechanism by which global comms can fail to beat local. Pitfall it warns
  you about: with base failure rates of 41-86.7%, your task difficulty must be tuned so the ground
  truth is recoverable at all, or every condition will floor out and the comms comparison will be
  noise.
- **Quorum (independent evidence vs repeated copies; false commit vs delay):** the FC3 category is
  the project's charter. **FM-3.1 Premature termination (6.20%)** *is* false commit; **FM-3.2 No or
  incomplete verification (8.20%)** and **FM-3.3 Incorrect verification (9.10%)** are the two ways a
  quorum rule can be wrong (it did not check, vs it checked and got it wrong) — and that split is
  worth adopting as your metric decomposition, because "incorrect verification" at 9.1% says a
  *badly designed* quorum is worse than the no-verification case it replaces. **FM-1.5 Unaware of
  termination conditions (12.4%)** is the delay side of the dial. The intervention result is the
  number to beat and the honest framing for your pitch: adding a verification step bought
  **+15.6%**, the single largest intervention in the paper, which both justifies working on quorum
  mechanisms *and* sets the realistic expectation — this is a double-digit improvement on a low
  base, not a solve. Also steal **FM-2.4 + FM-2.5** as the mechanism by which repeated copies look
  like independent evidence.
- **Telephone (atomic claims through retellings; lost evidence, inflated certainty):** the two
  highest-frequency modes are directly yours. **FM-1.3 Step repetition (15.7%)** — the most common
  single failure in the corpus — is a retelling loop; **FM-2.6 Reasoning-action mismatch (13.2%)**
  is the signature of inflated certainty (the agent states a conclusion its own reasoning does not
  support), and at 13.2% it is the second most common mode measured. **FM-2.3 Task derailment
  (7.40%)** is semantic drift across hops. So Telephone can claim it is instrumenting the #1 and #2
  most frequent failure modes in the field's reference taxonomy — a strong framing line. Methods to
  copy: the **grounded-theory-then-LLM-judge pipeline** is the right shape for scoring atomic claims
  at scale (hand-label a small set, validate a judge against it, report kappa, then scale), and
  their numbers give you the bar to hit — **kappa 0.88 human-human, 0.77 judge-human, 94% judge
  accuracy**; report yours in the same terms. Their trace size (15,000+ lines each) is also a
  warning: design your retelling traces to be *short and atomically labelled* from the start, or
  you will not be able to annotate them in a hackathon.

## Quotable (<=15 words each, verbatim, with location)

- "their performance gains on popular benchmarks are often minimal" — abstract (v3)
- "the first Multi-Agent System Failure Taxonomy (MAST)" — abstract (v3)
- "identified failures require more sophisticated solutions" — abstract (v3)
- "We do not claim it covers every potential failure pattern" — Section 4 (per extraction)
- "not all failure modes are resolved, and task completion rates still remain low" — Section 5.3 (per extraction)

## Not found / could not verify (queries tried, what was ambiguous)

- **Newer version / venue check : done, and the answer is yes on venue, no on a newer
  preprint.** arXiv latest is **v3, 2025-10-26**; the arXiv comment field says only "ArXiv v3" and
  journal_ref is empty, so arXiv alone would *not* tell you it is published. The published version
  is **NeurIPS 2025, Datasets and Benchmarks Track**, confirmed from the proceedings abstract page
  (`proceedings.neurips.cc/.../b1041e52d3be19f0a9bc491657488e4a-Abstract-Datasets_and_Benchmarks_Track.html`),
  which lists the same title and author set and states "1600+ annotated traces ... 7 popular MAS
  frameworks" and "150 traces". A **web search** was used to find that proceedings URL (noted per
  instruction); the venue itself was then verified by fetching the proceedings page directly, not
  from the search snippet. One wording discrepancy: the proceedings page labels the volume
  "Advances in Neural Information Processing Systems 38 ... (NeurIPS 2025)" while a search snippet
  said "39th Conference" — volume 38 / conference 39 for 2025 are both plausible; cite it simply as
  NeurIPS 2025 D&B Track.
- The proceedings **PDF** could not be parsed (the page fetcher returned raw PDF object-stream data), so the
  published version's abstract was read from the proceedings HTML abstract page instead, and only its
  first 125 characters were legible there.
- **Substantial v1 -> v3 drift, documented so citations do not get crossed.** v1 (2025-03-17)
  analyzed **five** frameworks over "**over 150 tasks**", named the taxonomy **MASFT** (not MAST),
  called category 1 "specification and system design failures" and category 3 "task verification
  **and termination**", and had no named dataset. v3 renames the taxonomy **MAST**, introduces
  **MAST-Data (1,642 traces, 7 frameworks)**, and shortens the category names. **Cite v3 and the
  NeurIPS version for MAST/MAST-Data; v1 if you need the MASFT name.**
- All in-paper numbers above were extracted by the page fetcher over the arXiv HTML of v3, not read
  from the PDF. The FM-level percentages are attributed by that reader to the Fig. 1 caption /
  Appendix A; verify any single percentage before putting it on a slide.
- Could not verify whether the 14 FM percentages sum to 100% (they sum to 100.05% as listed (FC1 44.2 + FC2 32.35 + FC3 23.5), which is
  consistent with a per-trace single-label distribution, but the paper permits multiple labels per
  trace elsewhere — the exact denominator was not confirmed).
