---
id: park-2026-cross
type: paper
title: "Cross-Agent Campaign Attribution: Linking Asynchronous Attacks Across LLM Agents"
authors: ["SangJin Park", "Myungsub Choi", "Jineok Kim", "Minseung Kang"]
year: 2026
venue: "Second Workshop on Agents in the Wild (AIWILD) at ICML 2026; arXiv preprint"
url: https://arxiv.org/abs/2607.18826
doi: null
arxiv: "2607.18826"
cite: "Park, S., Choi, M., Kim, J., & Kang, M. (2026). Cross-Agent Campaign Attribution: Linking Asynchronous Attacks Across LLM Agents. Second Workshop on Agents in the Wild (AIWILD), ICML 2026. arXiv:2607.18826."
topics: [swarm-detection, sybil-resistance]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: skim
relevance: 5
citations: null
code: []
---

## Summary

Formalises cross-agent asynchronous campaign attribution: linking sessions that hit different, independent LLM agents behind one shared proxy to the same adversarial campaign, with no shared runtime, labels or attacker identity. A2FV scores session pairs from three proxy-visible residue channels (tool-use structure, timing, prompt stylometry). On the synthetic SCD-v1 benchmark it reaches 0.82 pairwise AUC, while per-session injection detectors and chunked LLM judges used as linkers stay near chance.

## Contribution

Turns "is this one attacker spread across many agents?" into a benchmarked linking task, adapting APT campaign-correlation and provenance-graph ideas to LLM agent traffic.

## Key results

- A2FV pairwise campaign AUC 0.82 on SCD-v1 (abstract); per-session score-delta linkers and chunked LLM judges remain near chance.
- Structural (tool-call n-gram) residue is the strongest single channel and stylometric residue is complementary; timing is weak alone and gets zero calibrated weight.
- Static evasion (paraphrase, timing jitter, tool shuffle, singly or combined) lowers partition quality more than pairwise separability.
- Crossed-style control: when style directives are swapped across attackers, stylometry-only collapses and the structural channel provides the surviving lower-bound signal.
- Native OpenClaw and LangGraph trace probes stay above random after schema mapping.

## Methods and models

SCD-v1: 70% benign traffic adapted from AgentDojo and AgentBench, 15% isolated attacks, 15% multi-session campaigns; 40 adversary personas across four payload families; matched L0/L1/L2 evasion triplets; generators GPT-5.5 and Gemma-4-31B with Qwen and Gemini regenerations. Features: hashed tool-call n-grams and failure pivots, gap statistics with Hartigan's dip, char and byte n-gram TF-IDF. HDBSCAN for partitions. I read the main text; the HTML rendering dropped most table numbers, so only abstract-level figures are quoted here; appendices not read.

## Limitations and open questions

Synthetic, partly single-generator benchmark; labels are personas, not real attackers. Fully adaptive attackers with score feedback are out of scope. Assumes one administrative proxy that sees every agent's traffic; cross-tenant use would need privacy-preserving aggregation.

## Relevance to us

The closest prior work to linking a distributed swarm across many target agents. Its finding that tool-use structure survives style changes while timing adds little is a concrete design constraint for our detectors. Compare conversational linking [[white-2026-black]], system-prompt clones [[chen-2026-do]], and accountability via vendor logs [[chocron-2026-who]].
