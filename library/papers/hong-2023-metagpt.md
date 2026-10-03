---
id: hong-2023-metagpt
type: paper
title: 'MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework'
authors:
- Sirui Hong
- Mingchen Zhuge
- Jiaqi Chen
- Xiawu Zheng
- Yuheng Cheng
- Ceyao Zhang
- Jinlin Wang
- Zili Wang
- Steven Ka Shing Yau
- Zijuan Lin
- Liyang Zhou
- Chenyu Ran
- Lingfeng Xiao
- Chenglin Wu
- Jürgen Schmidhuber
year: 2023
venue: arXiv preprint
url: https://arxiv.org/abs/2308.00352
doi: null
arxiv: '2308.00352'
cite: 'Hong, S., Zhuge, M., Chen, J., Zheng, X., Cheng, Y., Zhang, C., Wang, J., Wang, Z., Yau, S. K. S., Lin, Z., et al. (2023). MetaGPT: Meta programming for a multi-agent collaborative framework. arXiv preprint arXiv:2308.00352.'
topics:
- llm-agent-swarms
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: "156 (OpenAlex W4385963839, arXiv record, 2026-10-03); Semantic Scholar 2550 same day"
code: []
---

## Summary

MetaGPT encodes human Standardized Operating Procedures (SOPs) into prompt sequences so that role-specialised agents (product manager, architect, engineer, QA) work in an assembly line and verify each other's intermediate artefacts. The stated motivation is that naively chaining LLMs causes "cascading hallucinations"; structured workflows reduce them. On collaborative software-engineering benchmarks it produces more coherent solutions than earlier chat-based multi-agent systems.

## Contribution

Showed that imposing organisational structure (roles plus structured handoffs) is a strong control on error propagation in LLM collectives; the opposite design philosophy to emergent, decentralised coordination.

## Key results

- Better coherence and pass rates on software benchmarks than chat-based MAS (abstract claim; numbers not read).

## Methods and models

Role agents with SOP-derived prompts, structured documents as messages, publish-subscribe shared message pool. Code: https://github.com/geekan/MetaGPT

## Limitations and open questions

Hand-designed hierarchy; small teams; [[cemri-2025-why]] finds MetaGPT still fails often and has more verification-stage failures than ChatDev.

## Relevance to us

Reference point for "centralised, designed" coordination when comparing against emergent swarms ([[kim-2025-towards]] measures that centralised verification limits error amplification to 4.4x).
