---
id: priyanshu-2026-secret
type: paper
title: 'Got a Secret? LLM Agents Can''t Keep It: Evaluating Privacy in Multi-Agent
  Systems'
authors:
- Aman Priyanshu
- Supriti Vijay
- Esha Pahwa
year: 2026
venue: arXiv
url: https://export.arxiv.org/api/query?id_list=2605.27766
doi: null
arxiv: '2605.27766'
cite: 'Aman Priyanshu; Supriti Vijay; Esha Pahwa. (2026). Got a Secret? LLM Agents
  Can''t Keep It: Evaluating Privacy in Multi-Agent Systems. arXiv:2605.27766.'
topics:
- llm-agent-swarms
added_by: shadow/sol-g51
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

The authors simulate thousands of socially interacting LLM agents to test privacy leakage over a month. The arXiv export abstract reports more privacy violations than single-turn evaluation, contagion after observing peers leak, and persistent leakage despite explicit privacy instructions.

## Contribution

Simulates thousands of socially interacting LLM agents for a month to measure privacy leakage under peer pressure, including contagion after observing peers leak.

## Key results

- Export abstract: violations increase from 19.95% to 45.30% across OpenAI models; peer leakage association eightfold; safeguarded leakage remains above 37.8%.

## Methods and models

Moltbook-style multi-agent simulation with socially pressured privacy evaluation.

## Limitations and open questions

The inspected HTML excerpt reports a different peer-leakage multiplier, 5.1, so the abstract figure requires full-text/version reconciliation before reuse. Simulation and judge-based evaluation are not field measurements.

## Relevance to us

A measured peer-contagion effect in an LLM population, relevant to how one compromised agent changes the behavior of others; reconcile the eightfold versus 5.1x figure (see Limitations) before quoting it.

## Access provenance

Opened the HTTPS arXiv export record and read its abstract on 2026-10-03. No citation count inferred from an absent or mismatched index record.
