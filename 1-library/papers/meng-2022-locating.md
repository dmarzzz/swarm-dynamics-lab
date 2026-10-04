---
id: meng-2022-locating
type: paper
title: Locating and Editing Factual Associations in GPT
authors:
- Kevin Meng
- David Bau
- Alex Andonian
- Yonatan Belinkov
year: 2022
venue: Advances in Neural Information Processing Systems 35 (NeurIPS 2022)
url: https://arxiv.org/abs/2202.05262
doi: null
arxiv: '2202.05262'
cite: Meng, K., Bau, D., Andonian, A., & Belinkov, Y. (2022). Locating and Editing Factual Associations in GPT. Advances in Neural Information Processing Systems 35 (NeurIPS 2022). arXiv:2202.05262.
topics:
- fork-merge-security
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: skim
relevance: 3
citations: null  # Semantic Scholar and OpenAlex rate-limited on 2026-10-03
code: []
---

## Summary

Uses causal tracing (corrupting the subject tokens in the input, then restoring individual hidden states from a clean run) to locate where GPT models recall a factual association, finds that mid-layer MLP modules at the last subject token are decisive, and then edits a single fact by a rank-one update to one MLP's output projection, treating the MLP as a key-value associative memory (Rank-One Model Editing, ROME). Introduces the CounterFact dataset of 21,919 counterfactual edits with measures of efficacy, generalisation to paraphrases, and specificity (neighbouring subjects left unchanged). Read: abstract, introduction, the causal tracing and ROME sections, evaluation set-up, limitations, conclusion and ethical considerations; tables only partly transcribed.

## Contribution

Evidence that factual associations are localised and directly editable in weights, and an editing method that keeps both generalisation and specificity where fine-tuning and hypernetwork editors (KE, MEND) trade one off against the other.

## Key results

- Causal tracing on GPT-2 XL (1.5B) attributes a large indirect effect to mid-layer MLPs at the last subject token (measured; the average total effect reported is 18.6%).
- On zsRE and CounterFact, ROME inserts a counterfactual fact that generalises to paraphrases while keeping specificity, unlike the baselines (measured; exact scores in Tables 1-2, not transcribed here).
- Edits are directional (a fact and its inverse need two edits) and one fact is edited at a time (stated limitation).
- The authors note in their ethics section that direct editing "has the potential for abuse, such as adding malicious misinformation, bias, or other adversarial data to a model" (stated, not tested).

## Methods and models

GPT-2 XL and GPT-J; key vector from the subject representation, value vector optimised to produce the new object; closed-form rank-one update using an estimate of the key covariance. NeurIPS 2022 (per the PDF footer). Code and data at rome.baulab.info.

## Limitations and open questions

Single-fact edits; factual associations only; edited models confabulate plausible related facts (stated).

## Relevance to us

Q3: establishes that a small, closed-form weight change can install a chosen belief in a model while leaving nearby behaviour intact, which is what makes an "edit" a plausible thing for a returning part to carry. If parts of a split agent return their learning as weight deltas or edits rather than as text, the merge channel accepts objects that are hard to inspect and specific by design. Q2: specificity is the problem for detection: an edit that changes only the targeted fact will pass a merge-time check on general behaviour. Successors that scale this and weaponise it: [[meng-2022-mass-editing]] (thousands of edits), [[li-2024-badedit]] (backdoors), [[chen-2024-can]] (misinformation and bias). Related: [[kirkpatrick-2017-overcoming]].
