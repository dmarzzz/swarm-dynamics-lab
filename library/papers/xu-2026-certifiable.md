---
id: xu-2026-certifiable
type: paper
title: 'Certifiable Semantic Agreement Among LLM Agents: What the Admissibility Instrument Decides'
authors:
- Haoran Xu
- Lei Zhang
- Iadh Ounis
- Xianbin Wang
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2606.07316
doi: null
arxiv: '2606.07316'
cite: 'Xu, H., Zhang, L., Ounis, I., & Wang, X. (2026). Certifiable Semantic Agreement Among LLM Agents: What the Admissibility Instrument Decides. arXiv preprint arXiv:2606.07316.'
topics:
- fork-merge-security
- llm-agent-swarms
- sync-consensus
added_by: dmarz/fm-bft-aggregation
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Builds H-CSC, a protocol in which a committee of LLM agents commits per round to a semantic result, a verdict, or a typed abort, each backed by a 2f+1 distinct-signer certificate, and asks whether agreement on meaning buys anything over agreement on a label. A containment lemma shows that whenever the shared semantic core is large enough to make the verdict deterministically valid, the verdict margin already exceeds f, so semantic certification cannot commit more tasks than a certificate-wrapped majority at matched guarantees; measurements agree. What matters is the admissibility instrument that decides which rationales count. Against adversaries that keep the verdict but corrupt the reasoning, a training-free lexical predicate detects attacks far better than a fine-tuned encoder, and embedding-distance filters fail on free-text rationales because honest agents disperse more than attacks displace.

## Contribution

A negative result on what BFT-style certificates can add for LLM committees, and a measurement that the real defensive work sits in the per-message admissibility check, not in the quorum rule.

## Key results

- Proved (per abstract): containment lemma; no coverage separation from certificate-wrapped majority at matched deterministic guarantees.
- Measured (per abstract): verdict-preserving reasoning attacks detected by a 442 MB fine-tuned encoder at AUROC 0.621 to 0.744 (0 to 8 percent TPR at 5 percent honest FPR) versus a lexical predicate at AUROC 0.865 to 0.982 (38 to 80 percent TPR); 50 tasks, 200 attacks, 400 honest runs.
- Measured (per abstract): 90th-percentile honest angular distance 0.992 rad versus a 0.65 rad attack radius, so embedding filters are not viable on free text; tightening the output schema cuts dispersion twenty-fold.
- Reported: a tie-break capture vulnerability in the authors' own protocol, with a four-line fix.

## Methods and models

2f+1 distinct-signer certificates, typed commit or abort outcomes, digest commitments with similarity-preserving sketches. Only the abstract was read.

## Limitations and open questions

Abstract-level reading. The authors claim no safety or coverage advantage over verdict-only certification.

## Relevance to us

Q2 and Q3. For Q2: a 2f+1 quorum over returning sub-agents certifies only what the per-message check can see. For Q3: the abstract names the attack class most relevant to merge poisoning, an adversary that keeps the visible verdict correct and corrupts the carried reasoning, which would pass any vote on outcomes and still enter the parent's memory. Their finding that embedding filters cannot separate such attacks on free text, while constrained output schemas can, suggests that a parent should merge structured, schema-checked summaries rather than free-text memories. Compare [[lee-2026-robust]] and [[liu-2026-consensus]].
