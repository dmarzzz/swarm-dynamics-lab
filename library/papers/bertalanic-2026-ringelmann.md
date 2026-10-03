---
id: bertalanic-2026-ringelmann
type: paper
title: 'The Ringelmann Effect in Multi-Agent LLM Systems: A Scaling Law for Effective Team Size'
authors:
- Blaž Bertalanič
- Carolina Fortuna
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2606.02646
doi: null
arxiv: '2606.02646'
cite: 'Bertalanič, B., & Fortuna, C. (2026). The Ringelmann Effect in Multi-Agent LLM Systems: A Scaling Law for Effective Team Size. arXiv preprint arXiv:2606.02646.'
topics:
- llm-agent-swarms
- sync-consensus
- criticality-measurement
added_by: dmarz/llm-agent-swarms-recent
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: 0 (OpenAlex, 2026-10-03); 5 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Counting nominal agents conflates cost with independent evidence, so the authors measure effective team size with the Kish design effect: N_eff = N / (1 + (N - 1) rho_N), where rho_N is the equicorrelation-scale pairwise agreement after communication. Modelling rho_N = c N^{-beta} gives the Ringelmann efficiency curve R(N) = N_eff/N = 1/(1 + c(N - 1)N^{-beta}) with three regimes: hard ceiling N_eff -> 1/c (beta = 0), sublinear N^beta/c (0 < beta < 1) and linear (beta >= 1). A DeGroot-style mean-field theorem, assuming non-modal agents see k random peers and adopt the modal answer with probability alpha_1 per modal peer, predicts disagreement decays as (1 - alpha_1)^{k tau}, so peer count k and rounds tau enter only through k tau and agreement is approximately N-independent (beta ~ 0). Experiments with teams of N = 1-30 on MMLU-Hard (724 items), GSM-Hard (1,017) and GPQA Diamond (198), with debate, self-correction (own answer as "peer"), a noise placebo (unrelated peers' answers) and self-consistency, fit the law in 44 model x task x condition cells (in-sample R^2 >= 0.97, median 0.999). Dense debate sits in the hard-ceiling regime on all tasks; the noise placebo matches self-correction, so peer content adds nothing beyond re-evaluation; only cross-family (heterogeneous) teams lower c.

## Contribution

Gives LLM collectives a shared unit (N_eff) and a two-parameter, pilot-predictable scaling law, tying together the social-psychology Ringelmann effect, Kish's survey-design effect, correlated-Condorcet theory and a DeGroot consensus closure. Its placebo design is the cleanest test so far of whether "peer interaction" matters. Directly challenges [[qian-2025-scaling]] and [[li-2024-more]]; consistent with [[yang-2026-understanding]] (diversity), [[zhang-2025-stop]] and [[kim-2025-towards]].

## Key results

- Measured: Qwen2.5-7B dense debate: beta ~ 0 with c = 0.85 (MMLU-Hard), 0.57 (GSM-Hard), 0.81 (GPQA), i.e. ceilings 1/c ~ 1.2, 1.8, 1.2 effective agents.
- Measured: GSM-Hard without peer influence is sublinear (c ~ 0.33-0.43, beta ~ 0.25); noise placebo c = 0.33, beta = 0.27 vs self-correction c = 0.34, beta = 0.25; replicated at Qwen2.5-32B (c = 0.45, beta = 0.18 for both).
- Measured: Llama-3.1-8B and Ministral-8B also beta = 0 on MMLU-Hard (c 0.62-0.71) and GPQA (c 0.55, 0.57). Qwen2.5-32B tightens ceilings (c = 0.96, 0.77, 0.97). Qwen3-8B thinking: 87.2% solo, debate rho = 0.983 at N = 5, N_eff = 1.02.
- Measured: k tau collapse: configurations with equal k tau give agreement within Delta rho ~ 0.04 (k in {1, 2, 4, 9, 29}, tau 1-6), looser at tau = 1.
- Measured: cross-family teams lower c from 0.85 to 0.54 (MMLU-Hard), 0.57 to 0.35 (GSM-Hard), 0.81 to 0.56 (GPQA), beta still ~ 0.
- Measured: parameters fitted on N in {2, 3, 5} extrapolate to N = 30 with <= 12% mean relative error vs >= 31% (power law) and >= 68% (logistic) alternatives.
- Measured: team accuracy is equivalent across communication modes within +-5 pp (TOST p < 0.02); GSM-Hard accuracy 10% -> 26-28% from re-evaluation (self-correction +18.2 pp, debate +16.4 pp). Debate costs 10-45x more prompt tokens per effective agent.

## Methods and models

Fully connected teams, three rounds (R1 independent, R2-R3 post-communication), zero-shot structured RATIONALE/FINAL/CONF format, plurality voting. N in {1, 2, 3, 5, 7, 10, 15, 20, 30}. N_eff at answer level (2^{entropy of answers}) and correctness level (ICC of binary correctness). Bounded least squares for (c, beta) with beta in [0, 1]; item-level bootstrap. Models: Qwen2.5-7B/32B-Instruct, Llama-3.1-8B, Ministral-8B, Qwen3-8B (thinking), Gemini 3.1 Flash-Lite; appendices add a HumanEval pilot, a two-rate (learning vs sycophancy) mean-field extension, and a fit to classical human Ringelmann data. No code URL seen in the main text.

## Limitations and open questions

- Role-symmetric teams on bounded QA; whether agentic or spatial tasks show the same regimes is open.
- beta constrained to [0, 1] by construction; the linear regime is never observed, so whether any design reaches it is untested (the authors list MoA and verifier pipelines as falsification tests).
- The mean-field theorem assumes modal agents never switch and a stable mode.
- Fully connected topology in main experiments; sparse communication enters only through k.

## Relevance to us

The quantitative null model for any LLM swarm scaling claim: report N_eff and (c, beta), include a noise placebo, and expect hard ceilings for homogeneous swarms. The k tau product law is a mean-field prediction we can test on sparse spatial swarms where k is set by perception radius ([[ruan-2025-benchmarking]]). Related: [[fortuna-2026-multi-agent]], [[chen-2024-are]], [[tran-2026-single]], [[de-marzo-2024-ai]].

## Notes from dmarz/llm-agent-swarms-recent-audit

Audit 2026-10-03: spot-checked against the arXiv abstract page (2606.02646, submitted 31 May 2026). Title, authors, the R(N) law, 44 conditions, R^2 > 0.99, the 30-agent MMLU-Hard ceiling, the placebo result and heterogeneity as the only escape all match. Per-cell (c, beta) values were not re-checked in this audit. No corrections.
