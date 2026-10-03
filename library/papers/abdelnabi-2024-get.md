---
id: abdelnabi-2024-get
type: paper
title: "Get my drift? Catching LLM Task Drift with Activation Deltas"
authors: [Sahar Abdelnabi, Aideen Fay, Giovanni Cherubin, Ahmed Salem, Mario Fritz, Andrew Paverd]
year: 2024
venue: IEEE Conference on Secure and Trustworthy Machine Learning (SaTML 2025)
url: https://arxiv.org/abs/2406.00799
doi: null
arxiv: '2406.00799'
cite: "Abdelnabi, S., Fay, A., Cherubin, G., Salem, A., Fritz, M., & Paverd, A. (2025). Get my drift? Catching LLM Task Drift with Activation Deltas. IEEE Conference on Secure and Trustworthy Machine Learning (SaTML 2025). arXiv:2406.00799."
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-identity-hijack
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Defines task drift as an LLM deviating from the user's original instruction after processing external data, the effect of a successful indirect prompt injection. The authors record activations before and after the model reads an external data block and train simple linear probes on the difference (the activation delta) to detect drift. They release TaskTracker, a dataset of over 500K instances with representations from six models.

## Contribution

A white-box detector of goal hijacking that is trained without attack examples and generalises to unseen attack types.

## Key results

- Reported (abstract): a linear classifier on activation deltas detects task drift with near-perfect ROC AUC on an out-of-distribution test set.
- Reported (abstract): it generalises to prompt injections, jailbreaks and malicious instructions without being trained on them.
- Requires no fine-tuning of the LLM and is compatible with prompting defences.

## Methods and models

Six open models' activations; two probing methods; TaskTracker dataset. Only the abstract was read.

## Limitations and open questions

White-box access needed; adaptive attacks against the probe are not covered in the abstract; drift is measured over one external data block, not long trajectories.

## Relevance to us

Q3 defence and Q2 instrument. The activation delta is a natural merge-time test: run the parent's model on its own task with and without a returning part's memory or report in context, and probe the difference. If the part's content shifts the parent's task representation, quarantine it. This only works when the parent controls a white-box model. Related: [[chen-2025-persona]], [[wallace-2024-instruction]], [[greshake-2023-not]] (same group's attack paper).
