---
id: kaur-2026-beyond
type: paper
title: "Beyond the Transcript: Detecting Covert Co ordination in Latent Multi-Agent Communication"
authors: ["Ramneet Kaur", "Pradyumna Chari", "Ramesh Raskar", "Jugad Singh", "Sumit Kumar Jha", "Anirban Roy"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2608.19161
doi: null
arxiv: "2608.19161"
cite: "Kaur, R., Chari, P., Raskar, R., Singh, J., Jha, S. K., & Roy, A. (2026). Beyond the Transcript: Detecting Covert Co ordination in Latent Multi-Agent Communication. arXiv:2608.19161."
topics: [swarm-detection, llm-agent-swarms]
added_by: dmarz/sd-coordination
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "1 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

LM agents can communicate through continuous hidden states invisible in transcripts. Verifiable Latent Alignments (VLA) links each private latent-state record to the resulting public action by an event identifier and monitors with three layers: representation anomaly detection, counterfactual action-distribution influence, and sparse-autoencoder interpretation. Evaluated on a controlled multi-agent auction benchmark with homogeneous and heterogeneous model pairs and 25 to 100 bidders.

## Contribution

A white-box monitor for coordination over latent channels, trained without attack examples.

## Key results

- Sequential monitor AUROC 0.993 for homogeneous agents and 0.854 for heterogeneous pairs, with text and latent collusion pooled as positives (abstract).
- In Qwen3-0.6B auctions with 25 to 100 bidders, white-box steering recovers 100% of the bid distribution and cuts collusive low bids by 47.3 percentage points; the authors note the exact recovery holds by construction (abstract).

## Methods and models

Activation logging, anomaly detection, matched-neutral counterfactuals, SAE features; synthetic auctions.

## Limitations and open questions

Abstract only. Requires access to every agent's internals, which an outside observer of a swarm in the wild does not have.

## Relevance to us

Inside-the-system collusion detection; relevant if the hackathon builds a platform that hosts agents. Black-box counterpart: [[ghanem-2026-steganalysis]]; activation-probe counterpart: [[rose-2026-detecting]]; existing entries [[tailor-2025-audit]] and [[motwani-2024-secret]].
