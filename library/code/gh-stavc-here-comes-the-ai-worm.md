---
id: gh-stavc-here-comes-the-ai-worm
type: code
title: 'Here-Comes-the-AI-Worm (formerly ComPromptMized): RAGworm self-replicating prompt and DonkeyRail guardrail'
repo: StavC/Here-Comes-the-AI-Worm
url: https://github.com/StavC/Here-Comes-the-AI-Worm
authors: [Stav Cohen, Ron Bitton, Ben Nassi]
year: 2024
language: Jupyter Notebook
license: none detected by GitHub API
stars: 234
last_commit: 2025-09-07
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-code-bench
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: [cohen-2024-here]
---

## Summary

The repository for the Morris II / RAGworm work by Cohen, Bitton and Nassi; the old URL StavC/ComPromptMized now redirects here. The README describes an adversarial self-replicating prompt that, when retrieved by a RAG-based email assistant, makes the assistant perform a payload and copy the prompt into its outgoing messages, which then land in other assistants' RAG stores. Measured in the paper as summarised in the README: super-linear propagation with each client compromising 20 new clients within 1 to 3 days depending on emails sent per day. The repo also ships DonkeyRail, a guardrail reported at true-positive rate 1.0, false-positive rate 0.017 and 7.6 to 38.3 ms added latency. Folders hold datasets, a self-replication test across LLMs, worm evaluation code and a legacy arXiv v1 code drop [[cohen-2024-here]].

## What it can do for us

Q3: this is the closest public code to "corrupted child re-infects the parent". The worm's mechanism, a retrieved record that both triggers an action and reproduces itself into the next store, is the same shape as a child report that rewrites the parent's memory and is then copied into the next generation of children. The self-replication test folder can measure, per model, whether a returned report reproduces injected text verbatim, which is a measurable precondition for propagation through merges. Q2: DonkeyRail is an example of a merge-time detector and gives one published operating point (TPR 1.0, FPR 0.017) to compare quorum-based schemes against.

## Run notes

Not run. Code is in notebooks (`DonkeyRail.ipynb` ends with a usage pipeline). Needs API access to the LLMs evaluated.

## Limitations

No licence file, so reuse terms are unclear. The legacy code is marked unmaintained. Propagation is through email RAG among peers, not a hierarchical fork and merge, so the topology differs. The guardrail's robustness to adaptive worms designed against it is claimed for out-of-distribution prompts, not for an adversary who knows the detector.
