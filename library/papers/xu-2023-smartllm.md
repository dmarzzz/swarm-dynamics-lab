---
id: xu-2023-smartllm
type: paper
title: "SmartLLM: A New Oracle System for Smart Contracts Calling Large Language Models"
authors: [Zhenan Xu, Jiuzheng Wang, Cong Zha, Xinyi Li, Hao Yin]
year: 2023
venue: 2023 IEEE 22nd International Conference on Trust, Security and Privacy in Computing and Communications (TrustCom), Exeter, pp. 2668-2675
url: https://ieeexplore.ieee.org/document/10538566/
doi: 10.1109/trustcom60117.2023.00372
arxiv: null
cite: "Xu, Z., Wang, J., Zha, C., Li, X., & Yin, H. (2023). SmartLLM: A New Oracle System for Smart Contracts Calling Large Language Models. In 2023 IEEE 22nd International Conference on Trust, Security and Privacy in Computing and Communications (TrustCom), pp. 2668-2675. IEEE. https://doi.org/10.1109/trustcom60117.2023.00372"
topics: [sybil-resistance, llm-agent-swarms]
added_by: shadow/sol-p2
accessed: 2026-10-03
read_depth: abstract
relevance: 1
citations: "not checked (OpenAlex budget exhausted 2026-10-03)"
code: []
---

## Summary

Short TrustCom paper that reviews blockchain oracle research (architectures and key technologies for getting trustworthy off-chain data on-chain) and proposes SmartLLM, an architecture that lets smart contracts call large language models through a trustworthy-oracle mechanism. Two variants are sketched: a chain-native design and a hybrid on-chain plus off-chain design. The abstract frames the contribution as enriching smart-contract use cases with LLM capabilities; the visible introduction restates the standard oracle problem (blockchains can only guarantee tamper resistance of on-chain data, not the truth of off-chain inputs). No evaluation, threat model or Sybil discussion is visible in the abstract or introduction; the body is paywalled and no open copy was found. Note that the Crossref author list given in the batch item omits the fifth author, Hao Yin, who appears on the IEEE page and in DBLP.

## Contribution

An architectural proposal for LLM-as-oracle on blockchains; the paper is primarily a mini-survey plus design sketch.

## Key results

- Chain-native and hybrid on/off-chain SmartLLM architectures proposed (abstract).
- No quantitative results visible.

## Methods and models

Literature review and system architecture description. Details not visible.

## Limitations and open questions

Abstract-level. The classic oracle problem is a Sybil problem (who are the reporters and how many are secretly one party), but nothing visible indicates the paper addresses oracle-node identity, staking or aggregation against Sybil reporters; the collector's placement in this batch appears to be keyword-driven. Likely superseded by later LLM-oracle work.

## Relevance to us

Marginal. Catalogued for completeness of the sybil-resistance scan; the live question for agent swarms (how to aggregate LLM outputs from many possibly colluding reporters) is treated far better in the oracle and consensus literature already in the library, for example [[gilad-2017-algorand]] on the consensus side. Do not cite for Sybil claims.
