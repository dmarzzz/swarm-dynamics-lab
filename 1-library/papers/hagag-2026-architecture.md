---
id: hagag-2026-architecture
type: paper
title: Architecture Matters for Multi-Agent Security
authors:
- Ben Hagag
- William L. Anderson
- Christian Schroeder de Witt
- Sarah Scheffler
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2604.23459
doi: null
arxiv: '2604.23459'
cite: Hagag, B., Anderson, W. L., de Witt, C. S., & Scheffler, S. (2026). Architecture Matters for Multi-Agent Security. arXiv preprint. arXiv:2604.23459.
topics:
- fork-merge-security
- llm-agent-swarms
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: null  # Semantic Scholar and OpenAlex rate-limited on 2026-10-03
code: []
---

## Summary

Measures how three architectural choices in multi-agent systems change resistance to misuse when a malicious user gives harmful task instructions: role decomposition (standalone agent vs orchestrator plus 1-4 specialists with partitioned tools), communication topology (star, chain, mesh) and memory visibility (private, own reasoning, full shared memory). Three single-agent misuse benchmarks are adapted with task prompts and scoring held fixed: BrowserART (browser), OS-Harm (desktop) and RedCode-Gen (code). Stage-wise metrics separate planning refusal, execution refusal, partial harmful action and harmful task completion (HT). Main results on GPT-4o, with GPT-5.4, GPT-5-mini, Claude Sonnet 4, Qwen3-VL and Llama 70B in the appendix. Read: abstract, introduction, design-choice framing, setup, all of section 5 and the discussion opening; appendices not read.

## Contribution

A controlled comparison that holds the model and task fixed and changes only the architecture, showing that decomposition itself changes refusal behaviour and that no topology or memory scheme is safest across domains.

## Key results

- BrowserART, GPT-4o: standalone HT 10.0%; star with 4 specialists 31.0%, with 2 specialists 38.0%, while benign accuracy rose to about 97.6% (measured, Tables 1-2). The authors attribute this to fragmentation of harmful intent: each specialist sees only atomic actions (interpretation).
- Strongly aligned models resisted: GPT-5.4 and Sonnet 4 stayed low across configurations; Qwen3-VL and Llama 70B degraded sharply under decomposition (measured; exact values in appendix tables I did not read).
- Topology: on RedCode-Gen, chain reached 42.5% HT against 9.4% standalone, 17.5% star, 20.6% mesh; on BrowserART, mesh was safest (7.0%) but had the lowest benign accuracy (81.0%) (measured, Table 2).
- Memory: only 1 of 6 topology-scenario combinations improved with more visibility; RedCode-Gen star rose from 17.5% to 23.8% HT with shared memory, mesh fell from 20.6% to 15.0% (measured, Table 3).
- The abstract's headline: attack success varies up to 3.8x across architectures at comparable or higher benign accuracy.

## Methods and models

Malicious-user threat model (no weight or code access). Benign performance on 42 BrowserART, 50 OS-World and 50 BigCodeBench tasks. Harmful task counts per benchmark as in the original suites.

## Limitations and open questions

The threat is a malicious principal, not a compromised sub-agent; single-run percentages without confidence intervals in the main tables; OS-World benign accuracy was zero everywhere, so the OS-Harm trade-off is not measurable.

## Relevance to us

Q3 and Q1 from the defender's side: splitting a task across sub-agents dilutes what each part can see, which raised harmful completion threefold in the browser setting. The same dilution that hides the parent's overall intent from any one child (a Q1 benefit) also hides harmful intent from each child's safety check. Q2: chain topologies, the shape of a sequential fork-and-return pipeline, were the worst in code generation, and shared memory was not a reliable safety gain. Related: [[zhang-2025-achilles]], [[triedman-2025-multi]], [[yu-2024-netsafe]].
