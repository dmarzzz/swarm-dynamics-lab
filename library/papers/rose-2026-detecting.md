---
id: rose-2026-detecting
type: paper
title: "Detecting Multi-Agent Collusion Through Multi-Agent Interpretability"
authors: ["Aaron Rose", "Carissa Cullen", "Sahar Abdelnabi", "Philip Torr", "Brandon Gary Kaplowitz", "Christian Schroeder de Witt"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/html/2604.01151
doi: null
arxiv: "2604.01151"
cite: "Rose, A., Cullen, C., Abdelnabi, S., Torr, P., Kaplowitz, B. G., & de Witt, C. S. (2026). Detecting Multi-Agent Collusion Through Multi-Agent Interpretability. arXiv:2604.01151."
topics: [swarm-detection, llm-agent-swarms]
added_by: dmarz/sd-coordination
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "6 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

Introduces NARCBench, a three-tier benchmark for collusion detection under distribution shift: Core (50 committee-vote scenarios in 17 domains, four agents, colluders steer the vote while hiding it), Transfer (six structurally different families such as code-review sabotage, pump-and-dump, CI/CD sabotage, RAG poisoning) and Stego (steganographic blackjack card counting). Five probing techniques project each agent's activations onto a learned deception direction and aggregate across agents to classify a scenario. Collusion detection is framed as a composite hypothesis test with an unknown colluding subgroup.

## Contribution

Extends activation probes from single-agent deception to group-level collusion detection and measures zero-shot transfer.

## Key results

- Every model reaches 1.00 AUROC in-distribution; on Llama-3.1-70B the five techniques reach 0.73 to 0.93 AUROC zero-shot on Transfer and 0.99 to 1.00 on Stego (abstract).
- Models tested: Qwen3-32B, Llama-3.1-70B, DeepSeek-R1 32B, GPT-OSS-20B; detection improves with model capability.
- No single technique dominates, consistent with their theory that no group statistic is uniformly most powerful.
- AUROC hides deployment performance: on Transfer, recall at 1% FPR is low even for the best method, while Stego is separated perfectly by one method.
- On an emergent-collusion setting from Shi et al. (229 of 480 rounds with collusion) transfer is mixed, so probes fitted to instructed collusion only partly capture emergent collusion.

## Methods and models

Linear deception probes on residual activations; group aggregation statistics (peak suspicion, deception split, activation alignment and two trained ones); generalised likelihood-ratio tests. Code and data: github.com/aaronrose227/narcbench (not catalogued).

## Limitations and open questions

Collusion in Core is instructed, not emergent. White-box access to every agent is required. I skimmed the introduction, setup, results and the emergent-collusion section.

## Relevance to us

The best-measured white-box group detector and an honest report of its low recall at strict FPR. Compare black-box approaches [[tailor-2025-audit]], [[ghanem-2026-steganalysis]] and audit framework [[nakamura-2026-colosseum]].
