---
id: christiano-2018-supervising
type: paper
title: Supervising strong learners by amplifying weak experts
authors: [Paul Christiano, Buck Shlegeris, Dario Amodei]
year: 2018
venue: arXiv
url: https://arxiv.org/abs/1810.08575
doi: null
arxiv: "1810.08575"
cite: Christiano, P., Shlegeris, B., & Amodei, D. (2018). Supervising strong learners by amplifying weak experts. arXiv preprint arXiv:1810.08575.
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-sutton
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: null
code: []
---

## Summary

Introduces Iterated Amplification: an expert H answers a question by decomposing it into subquestions, each answered by the current learned agent X; the composite Amplify_H(X) produces training targets, and X is trained by supervised learning to imitate it. Repeating this, X "approximates" the behaviour of "an exponentially large team of copies of H", and "the hierarchical decomposition itself is discarded as an artifact of training". Experiments use five algorithmic tasks (for example permutation powering, sequential assignments, shortest paths, union-find, wildcard search) with a hard-coded decomposition oracle in place of a human. Measured result: Iterated Amplification solved the tasks "with at worst a modest slowdown" relative to supervised learning on ground truth; supervised learning needed tens of millions of labelled examples, whereas amplification needed tens of thousands of calls to the decomposition oracle. The paper reuses context encoding across subquestions, which it reports speeds training by an order of magnitude.

## Contribution

A concrete, tested fork-and-distill loop: fan a task out to many copies of the current agent, then fold the composite behaviour back into a single agent by training.

## Key results

- Tens of thousands of oracle decompositions versus tens of millions of supervised labels on the algorithmic tasks (figures and Table 2 in the paper).
- The trained agent need not mirror the decomposition used to train it.

## Methods and models

Transformer encoder-decoder models on algorithmic tasks; decomposition provided by an algorithm H rather than a human; context-encoding and question-answering phases.

## Limitations and open questions

The authors state the experiments do not show that humans can decompose real tasks or that messy decompositions are learnable. Adversarial subagents are not considered in the paper; the companion blog posts on reliability and security amplification discuss them.

## Relevance to us

Iterated Amplification is a fork-merge loop in which the merge is distillation into weights, the same channel Sutton has in mind ([[sutton-2025-father]]). It makes Q3 concrete: a corrupted subanswer from one copy becomes a training target and is distilled into the next X, and since "the hierarchical decomposition itself is discarded", the provenance that would let a parent trace and roll back a bad contribution is lost at merge time. Its defences live in [[christiano-2016-reliability]] (voting among copies) and [[christiano-2016-security]] (decomposing inputs so no copy sees all of them). Compare the speculative-decoding style verification in [[dwarkesh-2025-what]].
