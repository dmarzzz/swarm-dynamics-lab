---
slug: debate-or-vote
title: "Debate or Vote: Which Yields Better Decisions in Multi-Agent Large Language Models?"
authors: Hyeong Kyu Choi, Xiaojin Zhu, Sharon Li
org_or_venue: NeurIPS 2025 Spotlight (arXiv:2508.17536, cs.CL / cs.MA)
date: 2025-08-24 (v1); v2 2025-10-23 (version read = v2)
url_loaded: https://export.arxiv.org/api/query?search_query=ti:%22Debate+or+Vote%22&max_results=10
  https://arxiv.org/abs/2508.17536
  https://arxiv.org/html/2508.17536v2
  https://arxiv.org/html/2508.17536
status: found
fetched: 2026-10-03
---

## What it is (2-4 sentences)

A decomposition study: it takes Multi-Agent Debate (MAD) apart into the two things it actually does
— **sample N independent answers and aggregate them (Majority Voting)**, and **let the agents read
each other and revise (Debate)** — then measures each contribution separately. The empirical answer
across seven NLP benchmarks is that majority voting carries essentially all of the gain, and debate
rounds often make things worse. The theoretical answer is a proof that, under homogeneous agents
with uniform belief updates, debate forms a **martingale** over belief trajectories, so its expected
correctness is unchanged by construction — debate can move an individual answer but cannot be
expected to move the aggregate toward truth. They then show two cheap interventions that break the
martingale (bias the update toward correction) and do help.

## Method / setup (what they actually did; models, N, tasks, baselines)

- **Benchmarks (7) with sample sizes (Table 1):** Arithmetics (100 questions), GSM8K (300 sampled
  from the test split), MMLU Professional Medicine (272), MMLU Formal Logic (126), HellaSwag (300
  sampled), CommonsenseQA (300 sampled), HH-RLHF (300 preference pairs sampled).
- **Models:** Qwen2.5-7B-Instruct and Llama3.1-8B-Instruct as the two primary models;
  Qwen2.5-32B-Instruct as an extension (Table 3). All open-weight, all small — see limitations.
- **Agents / rounds:** N = 5 agents in the main comparison, ablated N = 1..5 (Fig. 3). Debate rounds
  T = 2, 3, 5. Decoding: temperature 1.0, nucleus p = 0.9, max 512 tokens.
- **Baselines and conditions:**
  - *Single agent* — one sample.
  - *Majority Voting (MV)* — aggregate the N initial responses {y_i,0} by vote, **no debate**
    (conceptually T = 0). This is the baseline the whole paper is about.
  - *Decentralized MAD* — every agent sees all peers' previous responses.
  - *Sparse MAD* — sparse communication topology (each agent sees a subset).
  - *Centralized MAD* — a central agent aggregates.
  - *Heterogeneous agents* (Table 4) — distinct personas, a side experiment.
- **The decomposition move:** measure accuracy at the initial round (= the voting contribution) and
  again after T debate rounds (= voting + debate). The delta is debate's isolated contribution.
- **Theory:** model debate as a stochastic belief process (a DCM-style update); prove Theorem 2,
  E[p_i,t | alpha_{t-1}] = p_i,t-1, i.e. a martingale, then verify empirically that measured belief
  trajectories are flat (Fig. 4).

## Key results (numbers with units; mark each "measured" or "claimed")

- **Averages across the seven benchmarks — measured (Table 1).**
  - Qwen2.5-7B-Instruct: single agent **72.05%**, Majority Voting **76.91%**,
    Decentralized MAD (T=2) **73.77%**, Sparse MAD (T=2) **73.30%**,
    Centralized MAD (T=2) **65.51%**.
  - Llama3.1-8B-Instruct: single agent **62.03%**, Majority Voting **72.42%**,
    Decentralized MAD (T=2) **69.29%**, Sparse MAD (T=2) **69.90%**,
    Centralized MAD (T=2) **60.94%**.
  Read it as: ensembling buys **+4.9pp (Qwen) / +10.4pp (Llama)** over a single agent; adding debate
  on top of ensembling *costs* **-3.1pp (Qwen) / -3.1pp (Llama)** at T=2, and **Centralized MAD is
  worse than a single agent** on both models (-6.5pp / -1.1pp).
- **Per-benchmark worst cases — measured (Table 1, Qwen2.5-7B).** Arithmetics: MV **0.9900** vs
  Decentralized MAD T=5 **0.6700** (a 32pp collapse). GSM8K: MV **0.9400** vs MAD T=5 **0.8333**.
  MMLU Formal Logic: MV **0.5397** vs MAD T=5 **0.4762**. More debate rounds make it worse, not
  better — the degradation is monotone in T on these.
- **Martingale result — proved (Theorem 2), then measured (Fig. 4).**
  E[p_i,t | alpha_{t-1}] = p_i,t-1. Empirical belief trajectories are "essentially flat", which is
  the predicted signature. This is the paper's mechanism: debate is a fair game, not a hill-climb.
- **Agent-count ablation — measured (Fig. 3).** Accuracy rises with N from 1 to 5 for *both* MV and
  MAD, with MV staying comparable-or-better throughout. So the benefit people attribute to "more
  agents debating" is the benefit of **more independent samples**, not of the debating.
- **Interventions — measured (Table 2).**
  - *MAD-oracle* (lock agents that already hold the correct answer; infeasible, upper bound):
    Decentralized MAD T=5 on MMLU Formal Logic rises **0.5000 -> 0.6825** (+18.3pp).
  - *MAD-Conformist* (an agent matching the majority vote keeps its answer): Decentralized T=2
    average **0.7332 -> 0.7625** (+2.9pp).
  - *MAD-Follower* (30% probability of adopting the majority response): Decentralized T=2 average
    **0.7332 -> 0.7629** (+3.0pp).
  Both feasible interventions beat vanilla MAD and neither reaches the oracle. Note what they *are*:
  both work by **pulling debate back toward the majority vote**. The fix for debate is more voting.
- **Where MAD wins — measured, and it is thin.** Qwen2.5-32B on GSM8K: Decentralized MAD T=2
  **94.00%** vs MV **94.33%** — a tie, MV still nominally ahead. Heterogeneous agents (Table 4) on
  MMLU Professional Medicine show larger MAD gains, which the authors read as the "potential benefit
  of assigning diverse personas" — i.e. the win condition for debate is **agent diversity**, which
  the homogeneous theory explicitly excludes.
- **Claimed, not quantified.** The abstract's "Majority Voting alone accounts for most of the
  performance gains typically attributed to MAD" is **not given as a single percentage** anywhere I
  could find; it is the qualitative reading of Table 1. Quote the table averages, not a
  share-of-gain number.

## Limitations the source admits + ones you noticed

**Admitted (Appendix H):**
- Homogeneous-agent setting is the main object of study (and is exactly the assumption the theory
  needs).
- Evaluation is primarily **closed-ended** tasks; only a brief CNN/DailyMail summarization probe
  for open-ended.
- The DCM belief model may not capture all LLM behaviour.
- Small agent counts (N = 5) for compute reasons; theoretical conditions like N > K/Delta^2 remain
  unverified at the scales where they would bite.

**Noticed:**
- **Model scale is small.** Two 7-8B models plus one 32B. All the measured MAD damage may be partly
  "small models are bad at revising under peer pressure". Frontier models could behave differently,
  and the paper does not test any. This is the single biggest threat to transferring the conclusion.
- **The martingale theorem is an assumption-shaped result.** It holds *under homogeneous agents and
  uniform belief updates*. Heterogeneous agents, asymmetric confidence, or an agent with privileged
  evidence all break the premise — and Table 4's persona result plus the follow-up literature
  (arXiv:2601.19921, see below) both exploit exactly that. So "debate cannot help" is a statement
  about a specific idealization, not a general law. Do not over-cite it.
- **Majority voting needs a well-defined answer to vote on.** Six of seven benchmarks are
  multiple-choice or short-numeric. The MV baseline is unusually strong in that regime and gets much
  weaker where answers are free-form, long, or compositional — which is where real agent systems
  live.
- **"Centralized MAD" being worse than a single agent** is a striking number that deserves more
  scrutiny than the paper gives it; it suggests an aggregator-prompt artifact as much as a finding.
- **Decimal discrepancy to flag:** two independent reads of Table 1/2 gave the Decentralized T=2
  Qwen average as **0.7377** and **0.7332**. Re-check against the PDF before quoting to 4 digits.

## Relevance to the hackathon shortlist

- **Collective Sensing (local/global/no comms, partial obs, known truth):** this paper is the
  **baseline you are required to beat, and it is harder than it looks**. If your "no comms"
  condition aggregates N partial observations by vote and your "local/global comms" conditions let
  agents talk, then this paper predicts the talking conditions will *lose* to the silent one unless
  the agents hold genuinely different evidence. That is actually good news for the project: partial
  observability is precisely the heterogeneity the martingale theorem excludes, so **Collective
  Sensing has a principled reason to expect comms to help where debate did not** — each agent has
  private evidence the others cannot sample. State that explicitly; it is the project's whole
  justification. Concrete asks: (1) always run MV-over-N-independent-agents as a baseline, not just
  single-agent; (2) sweep agent count N and show your comms gain survives at matched N (Fig. 3 is
  the template); (3) sweep rounds T and check for the monotone degradation they saw.
- **Quorum (independent evidence vs repeated copies; false commit vs delay):** this is the paper the
  project is practically built on. (a) The **decomposition method is directly reusable**: measure
  accuracy at round 0 (independent) vs after exchange, and the delta is what communication did —
  that is exactly how you separate "independent evidence" from "echoes". (b) The **martingale result
  is your theoretical warrant**: repeated copies of the same belief cannot shift expected
  correctness, so a quorum that counts copies is counting nothing. (c) The **intervention finding is
  the design lesson with a sting**: both of their working fixes (MAD-Conformist, MAD-Follower) work
  by biasing agents toward the majority — which raises *false commit* risk when the majority is
  wrong. Their MAD-Follower uses a **30% adoption probability**; that is a tunable knob you can
  present as the false-commit/delay dial. (d) Their *oracle* bound (+18.3pp on MMLU Formal Logic)
  tells you the ceiling available to a perfect "who-is-actually-right" detector — i.e. how much a
  good quorum rule can win at most.
- **Telephone (atomic claims through retellings; lost evidence, inflated certainty):** the
  martingale is the precise statement of what Telephone should *violate*. A fair-game process has
  flat expected belief; a telephone chain is predicted to show **drift plus variance growth** — so
  the measurement to make is not "did the answer change" but "did the belief trajectory stay a
  martingale". Their Fig. 4 flat-trajectory plot is the figure to reproduce and break. Second gift:
  their T=2/3/5 sweep showing monotone degradation with more rounds (Arithmetics 0.99 -> 0.67 at
  T=5) is an existing retelling-depth result you can cite as prior evidence that depth hurts.
  Pitfall: they only track belief in the *final answer*, never the supporting evidence — so
  "inflated certainty with lost evidence" is a genuinely unmeasured phenomenon here, which is the
  gap your project fills. Also note the Centralized-MAD-worse-than-single-agent result as a warning
  that a summarizer in the chain can be the lossy element, not the fix.

## Quotable (<=15 words each, verbatim, with location)

- "Majority Voting alone accounts for most of the performance gains typically attributed to MAD" — abstract
- "We prove that it induces a martingale over agents' belief trajectories" — abstract
- "debate alone does not improve expected correctness" — abstract
- "simple ensembling methods remain strong and more reliable alternatives in many practical settings" — abstract
- "In most cases, majority voting performs on par with MAD" — Table 1 discussion (per extraction)

## Not found / could not verify (queries tried, what was ambiguous)

- **No explicit "X% of the gain is voting" figure exists** located. Searched the HTML of
  v2 and the no-version HTML render with a targeted prompt for a share-of-gain percentage; the claim
  is qualitative, supported by Table 1. Do not invent a percentage for it.
- Table 1 is reported here as averages across the seven benchmarks as returned by the HTML reader;
  the per-cell values I quote (Arithmetics, GSM8K, MMLU Formal Logic) came from a separate read of
  the same table and are consistent with the averages, but the Decentralized-T=2 average has a
  0.7377/0.7332 discrepancy between the two reads (noted above).
- All extraction was via the page fetcher over arXiv HTML, not a direct PDF read.
- **Related-but-distinct paper, identified during discovery:** `arXiv:2601.19921` (checked at the
  assignment's prompt) is **NOT** one of the four. It is *"Demystifying Multi-Agent Debate: The Role
  of Confidence and Diversity"* — Xiaochen Zhu, Caiqi Zhang, Yizhou Chi, Tom Stafford, Nigel
  Collier, Andreas Vlachos; cs.CL/cs.AI; v1 2026-01-09, v3 2026-06-03; no venue listed. It is a
  **direct follow-up to this paper**: it accepts the martingale critique ("under homogeneous agents
  and uniform belief updates, debate preserves expected correctness"), identifies the two missing
  mechanisms as **diversity of initial viewpoints** and **calibrated confidence communication**, and
  reports that its two lightweight interventions beat both vanilla MAD and majority vote across six
  reasoning-oriented QA benchmarks. If any shortlist project argues "comms *can* beat voting", that
  is the paper to pair with this one — it is the constructive answer to this paper's negative
  result, and it is highly relevant to Quorum (confidence calibration) and Collective Sensing
  (diversity of private views). It was fetched from `https://arxiv.org/abs/2601.19921` but has no
  note file of its own in this assignment.
