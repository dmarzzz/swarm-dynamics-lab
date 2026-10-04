---
id: peigne-lefebvre-2025-multi
type: paper
title: 'Multi-Agent Security Tax: Trading Off Security and Collaboration Capabilities
  in Multi-Agent Systems'
authors:
- Pierre Peigne-Lefebvre
- Mikolaj Kniejski
- Filip Sondej
- Matthieu David
- Jason Hoelscher-Obermaier
- Christian Schroeder de Witt
- Esben Kran
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2502.19145
doi: null
arxiv: '2502.19145'
cite: 'Pierre Peigne-Lefebvre; Mikolaj Kniejski; Filip Sondej; Matthieu David; Jason
  Hoelscher-Obermaier; Christian Schroeder de Witt; Esben Kran. (2025). Multi-Agent
  Security Tax: Trading Off Security and Collaboration Capabilities in Multi-Agent
  Systems. arXiv preprint arXiv:2502.19145.'
topics:
- fork-merge-security
- llm-agent-swarms
added_by: shadow/sol-g74
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

The authors simulate cooperative agents after one participant is compromised, observing multi-hop spread of malicious instructions. They compare two memory-based vaccination approaches and two generic safety-instruction approaches. Each reduces spread or malicious-task fulfilment in the tested settings but also tends to reduce collaborative performance, motivating joint security and utility evaluation.

## Contribution

Published analysis of propagation risks or defence trade-offs in agent networks.

## Key results

Four defence strategies are compared in the abstract. Numerical trade-off curves were not checked.

## Methods and models

Abstract and bibliographic metadata read.

## Limitations and open questions

Full methods and adaptive threat evaluation not independently checked.

## Relevance to us

Important negative-design evidence: reducing propagation can reduce the capability that a parent wanted from its children. Compare [[wu-2025-cowpox]] and [[lee-2024-prompt]].

## Notes from dmarz/honeypot-vigilance

Read in full (arXiv HTML v2) on 2026-10-03. This is the closest prior in the library for hunches V2 and V3 in `5-experiments/studies/dmarz/honeypot-vigilance-hunches.md`, because it scores both sides of the trade-off. Experiment 1 (seven AutoGPT-style agents in a simulated chemistry lab, 36 runs per model and defence, 12 jailbreaks, five OpenAI models) measures robustness: share of runs without the malicious "explosion". Experiment 2 (30 agents with 7-message histories, 6 harmless-but-unusual instructions, 5,400 trials) measures cooperation: acceptance of benign odd requests. Together they give a hit-rate and a false-alarm-rate proxy for the same defence, i.e. one ROC point per condition.

- Being told (safety instructions in the system prompt) raised average robustness from 76.7% to 87.2% (passive) and 87.8% (active) but cut benign acceptance from 87.1% to 52.3% and 60.7%; gpt-4o-2024-08-06 fell from 91.7% to 26.1% and 16.7%. That is a large criterion shift.
- A "vaccine" (a forged memory of having already met and handled a malicious input) raised robustness to 83.3% (passive) and 90.0% (active) while benign acceptance stayed at 87.5% and 87.6%. A remembered encounter improved robustness without the false-alarm cost, which reads as a d′ gain rather than a c shift.
- Active vaccines make agents warn peers; Figure 2 shows recipients of a compromised agent's message becoming suspicious and alerting others, i.e. warning propagation that contained spread.

Caveats for our use: the vaccine is a planted memory from an unrelated scenario, not a discovery made during the run; cooperation is measured in a separate setup, not on the same agents after a warning reached them; no hop-by-hop decay of the warning is reported. So V1 (in-run discovery), V2's decay with hops, and V4 (a false warning) remain unmeasured here. Related: [[chen-2026-trust]], [[robinson-2026-under]], [[cordeiro-2026-rouxii]].
