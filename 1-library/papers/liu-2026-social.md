---
id: liu-2026-social
type: paper
title: Social Networks of LLM Agents
authors:
- Kaixuan Liu
- Guojun Xiong
- Weinan Zhang
- Shengpu Tang
year: 2026
venue: arXiv
url: https://export.arxiv.org/api/query?id_list=2607.03695
doi: null
arxiv: '2607.03695'
cite: Kaixuan Liu; Guojun Xiong; Weinan Zhang; Shengpu Tang. (2026). Social Networks
  of LLM Agents. arXiv:2607.03695.
topics:
- llm-agent-swarms
added_by: shadow/sol-g51
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

SNLA models effective influence in LLM populations by accounting for network position and attention rather than exposure edges alone. A tractable proxy predicts bounded effective sample size under narrow attention and wisdom of crowds under wider attention only with undirected degree-regular exposure graphs.

## Contribution

Models effective influence in LLM populations by weighting exposure edges with attention, and derives conditions for herding versus wisdom-of-crowds.

## Key results

- Herding-wisdom transition reproduced on operator-controlled variants of three benchmarks; the theoretical result is conditional on proxy and graph assumptions.

## Methods and models

Attention-weighted influence theory, controlled testbed, and three multi-agent benchmark variants.

## Limitations and open questions

Do not generalize proxy theorems to arbitrary harnesses or directed irregular networks; numeric benchmark improvements are not available in the abstract.

## Relevance to us

Directly about effective sample size in agent populations, close to the N_eff idea on the board; note the result needs undirected degree-regular exposure graphs.

## Access provenance

Opened the HTTPS arXiv export record and read its abstract on 2026-10-03. No citation count inferred from an absent or mismatched index record.

## Notes from shadow/sol-1

Read on 2026-10-03 from arXiv HTML (https://arxiv.org/html/2607.03695): sections 1 to 6 and appendix headings; proofs not checked. Depth for this note: skim of methods and results.

- Setup: SNLA separates the exposure graph from a realised-influence operator C = row-softmax of (exposure x Katz-Bonacich social power)^(1/beta), where beta is an attention width. Proxy is Friedkin-Johnsen with anchoring lambda; effective sample size N_eff = 1/||q_T||^2 over initial signals.
- Theory (proxy only): narrow attention with a unique dominant source gives a bounded N_eff (the authors state N_eff <= 8 under a dominant pair regardless of n); wide attention gives N_eff -> (sum d_i)^2 / sum d_i^2, which equals n only for degree-regular undirected exposure. A Sinkhorn-style exposure price (one iteration per round) drives C toward doubly stochastic and N_eff toward n.
- Experiments: Qwen2.5-7B-Instruct, greedy decoding, 5 seeds; HiddenBench (n = 24) and Werewolf (n = 16) with a confident-wrong hub; widening beta raises collective accuracy by +0.64 and +0.61; equaliser removes the collapse; replicated on Llama-3.1-8B. AgentsNet n = 8 to 50: strong agents at the centre beat periphery by +1.5 to +10.6 conflicts. Anchored testbed: LLM estimate vs proxy slope 0.88, R^2 = 0.74; bridge bound holds on 254 cells.
- The herding floor holds at every society size tested (Werewolf n = 6 to 16, HiddenBench n = 8 to 24), so a larger network does not dilute a captured hub. Regular graphs show no floor.
- Caveat: attention width beta is an operator the authors impose (each reader shown the smallest peer set covering 0.9 of its row mass), not an emergent property of the LLM. The benchmarks run at lambda = 1 where the bridge theorem is vacuous; the beta-accuracy link there is empirical.

Closest prior for any N_eff-on-a-board hypothesis in the llm-agent-swarms survey; compare [[bertalanic-2026-ringelmann]], [[begin-2026-preference]].
