---
id: zhang-2025-when
type: paper
title: 'When LLMs meet cybersecurity: a systematic literature review'
authors:
- Jie Zhang
- Haoyu Bu
- Hui Wen
- Yongji Liu
- Haiqiang Fei
- Rongrong Xi
- Lun Li
- Yun Yang
- Hongsong Zhu
- Dan Meng
year: 2025
venue: Cybersecurity
url: https://doi.org/10.1186/s42400-025-00361-w
doi: 10.1186/s42400-025-00361-w
arxiv: null
cite: 'Jie Zhang; Haoyu Bu; Hui Wen; Yongji Liu; Haiqiang Fei; Rongrong Xi; Lun Li;
  Yun Yang; Hongsong Zhu; Dan Meng. (2025). When LLMs meet cybersecurity: a systematic
  literature review. Cybersecurity, 8(1), article 55. https://doi.org/10.1186/s42400-025-00361-w'
topics:
- swarm-detection
added_by: shadow/sol-w7
accessed: '2026-10-03'
read_depth: skim
relevance: 2
citations: null
code: []
---

## Summary

This systematic review maps how language models are specialized for cybersecurity, how they are applied to downstream security tasks, and what deployment challenges remain. It covers threat intelligence, vulnerability work, secure code, and other applications while noting that jailbreakable models introduce their own attack surface. It is a citation map, not a validated swarm-monitoring system.

## Contribution

A broad taxonomy of cybersecurity-oriented model construction, application tasks, and unresolved deployment risks.

## Key results

- The abstract reports more than 300 works, 25 LLMs, and over 10 downstream scenarios.
- The conclusion emphasizes fine-tuning with domain data, threat intelligence and vulnerability detection, and susceptibility to jailbreaks.
- The authors maintain an accompanying Awesome-LLM4Cybersecurity resource list, not a single common evaluation benchmark.

## Methods and models

Literature synthesis arranged around three research questions: domain-model construction, application opportunities, and challenges. Read abstract, opening sections and conclusion; study-level evidence and search completeness were not audited.

## Limitations and open questions

Broad scope and heterogeneous tasks do not yield a calibrated accuracy figure. A security-domain LLM is not automatically trustworthy as a monitor. Primary sources are needed before any load-bearing claim about adversarial coordination or safe autonomous operation.

## Relevance to us

Background for automated threat-intelligence and trace triage. Compare [[tsai-2026-llm]] for a concrete honeypot architecture and [[hadrien-2025-bitter]] for supervision benchmark evidence.
