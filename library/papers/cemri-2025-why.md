---
id: cemri-2025-why
type: paper
title: Why Do Multi-Agent LLM Systems Fail?
authors:
- Mert Cemri
- Melissa Z. Pan
- Shuyi Yang
- Lakshya A. Agrawal
- Bhavya Chopra
- Rishabh Tiwari
- Kurt Keutzer
- Aditya Parameswaran
- Dan Klein
- Kannan Ramchandran
- Matei Zaharia
- Joseph E. Gonzalez
- Ion Stoica
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2503.13657
doi: null
arxiv: '2503.13657'
cite: Cemri, M., Pan, M. Z., Yang, S., Agrawal, L. A., Chopra, B., Tiwari, R., Keutzer, K., Parameswaran, A., Klein, D., Ramchandran, K., et al. (2025). Why do multi-agent LLM systems fail? arXiv preprint arXiv:2503.13657.
topics:
- llm-agent-swarms
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: full
relevance: 4
citations: 672 (Semantic Scholar, 2026-10-03; OpenAlex unavailable that day)
code: []
---

## Summary

An empirical taxonomy of how multi-agent LLM systems (MAS) fail. Six expert annotators used Grounded Theory on 150 execution traces (average over 15,000 lines each) from five frameworks (ChatDev, MetaGPT, HyperAgent, AppWorld, AG2/MathChat) to derive MAST, the Multi-Agent System Failure Taxonomy: 14 failure modes in three categories, (FC1) system design issues, (FC2) inter-agent misalignment and (FC3) task verification. Inter-annotator agreement reached Cohen's kappa = 0.88. An o1-based LLM-as-judge (few-shot) reproduces human labels with accuracy 0.94 and kappa = 0.77, and generalises to two unseen systems (OpenManus, Magentic-One; kappa = 0.79). The resulting MAST-Data has 1,642 annotated traces from seven frameworks and several model families (GPT-4/4o, Claude 3.7 Sonnet, Qwen2.5-Coder-32B, CodeLlama-7B).

## Contribution

The reference failure taxonomy for LLM MAS, widely reused (for example as the error vocabulary in [[kim-2025-towards]]). It reframes MAS failures as organisational-design problems, citing high-reliability-organisation theory, rather than as pure model deficiencies.

## Key results

- Failure rates of 41% to 86.7% across seven state-of-the-art open-source MAS on their benchmarks. Measured.
- Prevalence across 1,642 traces: FC1 step repetition 15.7%, not recognising task completion 12.4%, disobeying task specification 11.8%, context loss 2.8%, disobeying role 1.5%; FC2 reasoning-action mismatch 13.2%, task derailment 7.4%, proceeding on wrong assumptions instead of asking 6.8%, conversation reset 2.2%, ignoring other agents 1.9%, information withholding 0.85%; FC3 incorrect verification 9.1%, no or incomplete verification 8.2%, premature termination 6.2%. Measured (LLM-annotated).
- Failure profiles are system-specific (AppWorld: premature termination, linked to its star topology; OpenManus: step repetition; HyperAgent: repetition and wrong verification). MetaGPT shows 60-68% fewer FC1/FC2 failures than ChatDev but 1.56x more FC3. Measured.
- Interventions with the same model: better role specification gives +9.4% success for ChatDev; adding a high-level objective verification step gives +15.6% on ProgramDev; task completion remains low. Measured.

## Methods and models

Grounded Theory (open coding, constant comparison, memoing, theoretical saturation), three rounds of inter-annotator agreement on 5 traces each, LLM-as-judge calibration on held-out human labels. Benchmarks: ProgramDev (custom), SWE-Bench Lite, AppWorld Test-C, GSM-Plus, OlympiadBench, MMLU, GAIA. Code and data: https://github.com/multi-agent-systems-failure-taxonomy/MAST ; dataset https://huggingface.co/datasets/mcemri/MAST-Data ; pip package agentdash.

## Limitations and open questions

Traces come from task-oriented, small-team software frameworks (a handful of agents), not large decentralised populations; most of the dataset is LLM-annotated; the authors do not claim exhaustiveness. FC2 failures are attributed to a "collapse of theory of mind", a hypothesis not tested directly. Nothing here measures collective dynamics such as cascades or synchrony.

## Relevance to us

Useful as the vocabulary for describing failures in any swarm experiment, and as a reminder that MAS failure often comes from interaction structure (topology, termination, verification) rather than individual capability. Connects to error amplification in [[kim-2025-towards]], infectious spread in [[gu-2024-agent]], conformity and herding in [[weng-2025-do]] and [[cho-2025-herd]], and the risk taxonomy of [[hammond-2025-multi]].
