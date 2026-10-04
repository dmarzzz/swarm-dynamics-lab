---
slug: scaling-agent-systems
title: Towards a Science of Scaling Agent Systems
authors: Yubin Kim, Ken Gu, Chanwoo Park, Chunjong Park, Samuel Schmidgall, A. Ali Heydari, Yao Yan, Zhihan Zhang, Yuchen Zhuang, Yun Liu, Mark Malhotra, Paul Pu Liang, Hae Won Park, Yuzhe Yang, Xuhai Xu, Yilun Du, Shwetak Patel, Tim Althoff, Daniel McDuff, Xin Liu
org_or_venue: arXiv (cs.AI) — arXiv:2512.08296v3; no venue/comment field listed
date: 2025-12-09 (v1); v2 2025-12-17; v3 2026-04-08 (version read = v3)
status: found
fetched: 2026-10-03
urls_loaded:
  - "https://export.arxiv.org/api/query?search_query=ti:%22Science+of+Scaling+Agent+Systems%22&max_results=10"
  - "https://arxiv.org/abs/2512.08296"
  - "https://arxiv.org/html/2512.08296v3"
  - "https://arxiv.org/html/2512.08296"
  - "https://ar5iv.labs.arxiv.org/html/2512.08296"
  - "https://ar5iv.labs.arxiv.org/html/2512.08296v3"
library_ids:
  - kim-2025-towards
---

## What it is (2-4 sentences)

An attempt to fit an explicit *scaling law* for agent systems: a regression that predicts task
performance from model capability, agent count, coordination structure, tool count, and measured
coordination-overhead variables. The authors run 260 controlled configurations over six agentic
benchmarks, five canonical architectures (single-agent plus Independent / Centralized /
Decentralized / Hybrid multi-agent), and three LLM families, holding tools, prompts and compute
budget fixed so the architecture is the only thing varying. The headline is *not* "more agents is
better" — it is that adding agents has a sign that flips depending on task structure, and that the
flip is predictable. This is the single best source in the shortlist for the "when does coordination
stop paying" question.

## Method / setup (what they actually did; models, N, tasks, baselines)

- **Benchmarks (6, v3):** BrowseComp-Plus (web retrieval), Finance-Agent (financial analyst),
  PlanCraft (Minecraft sequential planning), WorkBench (business tool selection),
  SWE-bench Verified (GitHub issues), Terminal-Bench (CLI/sysadmin). (§4.1, Table 1.)
  ⚠ v1/v2 used **four** benchmarks (Finance-Agent, BrowseComp-Plus, PlanCraft, Workbench);
  SWE-bench Verified + Terminal-Bench were added by v3. This matters for reading the limitations
  (see below).
- **Architectures (5):** Single-Agent System (SAS), Multi-Agent Independent, Decentralized,
  Centralized, Hybrid. (Table 2.)
- **Models (3 families, 9 models):** GPT-5-nano / GPT-5-mini / GPT-5; Gemini-2.0 Flash /
  Gemini-2.5 Flash / Gemini-2.5 Pro; Claude Sonnet 3.7 / Sonnet 4 / Sonnet 4.5. (§4.1.)
- **N:** 260 configurations = (9 models x 5 architectures x 4 benchmarks = 180) + (8 models x
  5 architectures x 2 benchmarks = 80). Per-configuration runs: 50-100 instances on four
  benchmarks; **20-instance subsets** on SWE-bench Verified and Terminal-Bench (Docker cost). (§4.1.)
- **Agent counts:** n_a in {1, 3, 5, 7, 9} (reported on the earlier-version render; the v3 fit
  treats n_a as a continuous log term).
- **Control:** tools, prompts and *total reasoning tokens* matched across conditions
  (mean mu = 4,800 tokens per trial); multi-agent teams got equal total budget by giving each agent
  fewer iterations, while SAS got proportionally more reasoning rounds. (§4.1.) This is the
  methodological move that makes the comparison about coordination rather than compute.
- **Baseline:** SAS with identical tools/prompts/budget. Results normalized as
  (mean_MAS - mean_SAS) / mean_SAS x 100%.
- **The model (Eq. 1, §4.3):** a linear/quadratic regression
  P = b0 + b1(I-Ibar) + b2(I-Ibar)^2 + b3 log(1+T) + b4 log(1+n_a) + b5 log(1+O%) + b6 c + b7 R
  + b8 E_x + b9 log(1+A_e^trace) + b10 P_sa + 9 interaction terms + eps,
  where I = Intelligence Index (composite capability, range 42-71), T = tool count (2-16),
  n_a = agent count, O% = coordination overhead (% token increase vs SAS), c = message density,
  R = redundancy rate, E_x = coordination efficiency (success per turn cost),
  A_e^trace = trace-level error-amplification factor, P_sa = single-agent baseline performance.
  Validation = 5-fold held-out at experiment level.

## Key results (numbers with units; mark each "measured" or "claimed")

- **Fit quality — measured.** R^2_train = 0.463; **R^2_cv = 0.373 (+/- 0.170 SD)** with the
  Intelligence Index; R^2_cv = 0.413 (+/- 0.130) with a task-grounded Agentic Capability Index
  (ACI = mean single-agent performance across the six benchmarks). AIC = -236.3. (§4.3.)
  Simpler nested models: intelligence+tools+agents only R^2_cv = 0.360; adding coordination
  structure R^2_cv = 0.363 (Table 3). **So the elaborate model buys ~0.01-0.05 R^2_cv over a
  three-variable one — read the "scaling law" framing against that.**
- **Sign flip by task — measured.** Best case **+80.8%** relative to SAS (Finance-Agent,
  Centralized MAS: 0.631 vs SAS 0.349). Worst case **-70.0%** (PlanCraft, Independent MAS:
  0.170 vs SAS 0.568). PlanCraft is negative for *every* MAS variant, -39.1% (Hybrid) to -70.0%
  (Independent); Finance-Agent is positive for every variant, +57% to +80.8%. (Fig. 2, §4.2.)
  Decomposable analysis task => multi-agent wins; sequential planning => multi-agent loses badly.
- **Coordination overhead — measured (Table 5).** Token overhead vs SAS: Independent **+58%**,
  Decentralized **+263%**, Centralized **+285%**, Hybrid **+515%**. Coordination efficiency
  E_x (success per turn cost): SAS n/a, Independent 0.234, Decentralized 0.132, Centralized 0.120,
  Hybrid 0.074 — i.e. efficiency falls monotonically as coordination richness rises.
- **Error amplification — measured (Table 5).** A_e^trace relative to SAS = 1.0:
  **Independent 17.2**, Decentralized 7.8, Hybrid 5.1, **Centralized 4.4**. The architecture with
  *no* communication amplifies errors most, because nothing catches them; centralized verification
  is the cheapest suppressor.
- **The baseline paradox — measured + claimed.** Interaction term
  b_hat[P_sa x log(1+n_a)] = **-0.236, p = 0.004** (Table 4), with a stated threshold
  **P_sa* ~ 0.45**: above ~45% single-agent accuracy, adding agents yields negative returns (§4.3).
  The coefficient is measured; the specific 0.45 crossing point is a derived claim from this fit and
  should be treated as order-of-magnitude, not a constant.
- **Turn-count power law — measured.** T = 2.72 x (n + 0.5)^1.724, R^2 = 0.974. SAS 7.2 +/- 2.1
  turns; Hybrid 44.3 +/- 12.4 turns (6.2x SAS). (§4.4.) Superlinear in agent count.
- **Other significant interactions — measured (Table 4).** Efficiency x tools
  b_hat = -0.096 (p = 0.002) — tool-heavy tasks penalize coordination. Redundancy x n_a
  b_hat = +0.024 (p = 0.034) — redundant agent output is mildly *helpful*, not purely waste.
  Marginal/non-significant: O% x T (p = 0.211), A_e^trace x T (p = 0.332), reported as
  "directional patterns" only.
- **Architecture selection — measured.** The fit picks the best-performing architecture for
  **87% of held-out configurations**, vs 20% random and 54% capability-only. (Abstract, §4.3.)
  This is the paper's strongest practical result: *relative* architecture choice transfers even
  though absolute performance prediction does not (R^2_cv 0.373).
- **Benchmark noise — measured.** BrowseComp-Plus coefficient of variation sigma/mu = 0.32 vs
  WorkBench 0.12 (§4.1) — browsing tasks are ~2.7x noisier across configurations.

## Limitations the source admits + ones you noticed

**Admitted** (retrieved from the ar5iv mirror, which renders an **earlier version** — its abstract
says "four diverse benchmarks", so these six items are the v1/v2 Limitations section; the v3
Section 5 text could not be pulled through the page fetcher, see "Not found" below):
1. Agent scaling only to **nine** agents; emergent behaviour of larger collectives untested.
2. All agents share identical base architectures, differing only in scale and role prompt — no
   genuinely heterogeneous teams.
3. Tool-heavy environments named as "a primary failure mode" needing specialized protocols.
4. **No per-model prompt optimization** — identical prompts across conditions, despite known
   prompt sensitivity.
5. Benchmark scope may miss embodied agents, multi-user interaction, long-horizon temporal tasks.
6. Economic viability: tokens and latency grow substantially with agent count "often without
   proportional performance gains".

**Noticed:**
- **The matched-token control cuts both ways.** Holding total tokens fixed means each agent in a
  9-agent team gets ~1/9 the reasoning. Some of the measured multi-agent *loss* is therefore
  thinned per-agent reasoning, not coordination failure per se — the paper's own earlier-version
  limitation hints at this ("prohibitively thin" per-agent capacity). A deployment that gives each
  agent a full budget is a different experiment, and more expensive.
- **R^2_cv = 0.373 is weak for something called a scaling law.** ~63% of variance unexplained, and
  the SD (+/-0.170) means some folds fit near-zero. The 87% architecture-selection figure is the
  defensible claim; the regression coefficients are suggestive.
- **n = 20 on SWE-bench Verified and Terminal-Bench.** Two of six benchmarks rest on 20 instances
  per configuration — binomial noise alone is ~+/-11pp at p=0.5. Treat anything driven by those two
  as directional.
- **Three model families, all frontier-commercial, all late-2025/2026.** No open-weight models, so
  the capability axis is confounded with vendor-specific agentic post-training.
- **A_e^trace, c, R, E_x are *outcome-correlated* regressors.** Error amplification and coordination
  efficiency are measured from the same traces whose success is being predicted, so part of the fit
  is tautological. The purely *ex-ante* variables are capability, tool count, agent count and P_sa.
- **One version-drift hazard for citation:** v1/v2 vs v3 differ in benchmark count (4 vs 6). Cite
  v3 explicitly.

## Relevance to the hackathon shortlist

- **Collective Sensing (local/global/no comms, partial obs, known truth):** this is the closest
  existing analogue and it hands you three things. (a) **The comms conditions are already named and
  measured**: "no comms" = their Independent architecture, "local" = Decentralized, "global" =
  Centralized, plus Hybrid. Use those names so results are comparable. (b) **The headline number to
  try to reproduce**: Independent (no comms) has the *worst* error amplification, 17.2x vs SAS,
  while Centralized is 4.4x — so the prediction for a partial-observation sensing task is that
  no-comms swarms do not merely fail to help, they *amplify* individual error, and a central
  verifier is the cheapest fix. (c) **The pitfall**: match the token budget across comms conditions
  or your "comms helps" result is just "more compute helps". Also steal their normalization
  ((MAS - SAS)/SAS x 100%) and their single-agent-with-full-observation baseline. Their fitted threshold motivates checking how gains vary with baseline strength; it does not establish a universal 45% cutoff for a new partial-observation task.
- **Quorum (independent evidence vs repeated copies; false commit vs delay):** two direct gifts.
  (a) Their **redundancy rate R** is exactly your "repeated copies" axis, and it is measured as a
  regressor with a *positive* interaction with agent count (+0.024, p = 0.034) — so the literature
  position you are arguing against is "redundancy is harmless or mildly good"; your contribution is
  showing it inflates *confidence* without adding evidence. (b) Their **centralized-verification
  finding** (4.4x vs 7.8x/17.2x error amplification) is the architectural argument for a quorum
  *arbiter* rather than peer-to-peer agreement. For the false-commit-vs-delay tradeoff, measure delay directly in the proposed quorum system. Their fitted turn-count curve T = 2.72(n+0.5)^1.724 is a result for their evaluated systems, not a transportable latency law for quorum size.
- **Telephone (atomic claims through retellings; lost evidence, inflated certainty):** the
  **A_e^trace error-amplification metric is the metric you want**, lifted directly: define
  amplification as the factor by which a per-hop error rate shows up in the final retelling vs a
  one-hop baseline. Their numbers give you a reference scale (4.4x to 17.2x over short agent
  chains) and their mechanism claim gives you the hypothesis to test: chains *without* a central
  verification step propagate more. Their Hybrid architecture averaging 44.3 turns is also a warning
  about your experimental cost. Pitfall to avoid: they measure amplification on *success*, not on
  *claim fidelity* — so your contribution is separating "got the answer wrong" from "lost the
  evidence while keeping the answer", which their framework cannot see.

## Quotable (<=15 words each, verbatim, with location)

- "a coordination yields diminishing returns once single-agent baselines exceed certain performance" — abstract (sic, including the stray "a")
- "architectures without centralized verification tend to propagate errors more than those with centralized coordination" — abstract
- "architecture-task alignment determines collaborative success" — abstract
- "mismatched coordination degrades the performance" — abstract, final sentence
- "Token consumption and latency grow substantially with agent count, often without proportional performance gains" — Limitations (earlier-version render, item 6)

## Not found / could not verify (queries tried, what was ambiguous)

- **The v3 Limitations section (Section 5) and Conclusion could not be retrieved.** Tried
  `https://arxiv.org/html/2512.08296v3`, `.../2512.08296v3#S5`, and `https://arxiv.org/html/2512.08296`
  — all three returned the paper truncated after §4.5, with §5 present only as a table-of-contents
  link. The six admitted limitations above come from `https://ar5iv.labs.arxiv.org/html/2512.08296`,
  which **renders an earlier version** (confirmed: its abstract says "four diverse benchmarks:
  Finance-Agent, BrowseComp-Plus, PlanCraft, and Workbench", vs v3's six). A follow-up check of
  `https://ar5iv.labs.arxiv.org/html/2512.08296v3` returned the same earlier-version content.
  If the v3 limitations are load-bearing for a claim, read the PDF directly.
- **No venue.** The arXiv comment field is empty and no journal_ref is present as of 2026-10-03, so
  this is arXiv-only / under review as far as can be verified. Do not cite a conference for it.
- **All numbers above were extracted by the page fetcher from the arXiv HTML, not read directly off
  the PDF.** Table/section attributions are as that reader reported them. Spot-check any single
  number before putting it in a slide.
- Agent-count range {1,3,5,7,9} is reported from the earlier-version render; not re-confirmed
  against v3 text.
