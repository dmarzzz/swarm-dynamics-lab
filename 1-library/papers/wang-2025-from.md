---
id: wang-2025-from
type: paper
title: 'From Purity to Peril: Backdooring Merged Models From "Harmless" Benign Components'
authors: [Lijin Wang, Jingjing Wang, Tianshuo Cong, Xinlei He, Zhan Qin, Xinyi Huang]
year: 2025
venue: 34th USENIX Security Symposium (USENIX Security 25)
url: https://www.usenix.org/conference/usenixsecurity25/presentation/wang-lijin
doi: null
arxiv: null
cite: 'Wang, L., Wang, J., Cong, T., He, X., Qin, Z., & Huang, X. (2025). From Purity to Peril: Backdooring Merged Models From "Harmless" Benign Components. In 34th USENIX Security Symposium (USENIX Security 25) (pp. 6339-6358). Seattle, WA: USENIX Association.'
topics: [fork-merge-security]
added_by: dmarz/fm-code-bench
accessed: 2026-10-03
read_depth: skim
relevance: 5
citations: null  # not looked up; Semantic Scholar and OpenAlex rate-limited at access time
code: [gh-wljllla-mergebackdoor]
---

## Summary

The authors build upstream models that each behave cleanly on their own but produce a backdoored model when merged. MergeBackdoor fine-tunes several homologous models (same pre-trained base, different tasks) in parallel, using backdoor training so the trigger works in the merged model and anti-backdoor training so each upstream model's attack success stays at random-guessing level. Across ViT, BERT and LLM models and 12 datasets, the merged models reach attack success above 90% with the simplest trigger while upstream models show suppressed ASR. A "Strong Detector" that knows the trigger pattern and that upstream models may hide backdoors flagged only two BERT upstream models; the same class of detector caught 83% of a baseline attack's models and, after merging, flagged 66.67% of merged ViTs and all merged BERTs.

## Contribution

Moves model-merging backdoors from "one visibly backdoored contributor" (as in [[zhang-2024-badmerging]] and [[yuan-2025-merge]]) to a distributed payload where no single contributor is detectably malicious, so safety checks on components do not imply safety of their merge.

## Key results

- Merged models: ASR above 90% across merging methods and datasets with the simplest trigger (introduction, measured).
- Upstream models: ASR at random-guessing level before merging (abstract, measured).
- Only two upstream models are needed; the paper states the backdoor does not activate if both are not selected for the merge (threat model section).
- Detection before merge: the most informed detector identified only two BERT upstream models; NeuronInspect detected neither upstream nor merged models (Table 5 as described in text).
- Detection after merge: a detector with access to clean and possibly triggered samples flagged 66.67% of merged ViTs and all merged BERTs.
- Baseline attack (ViTs from prior work): 83% of models detected before merging, versus near zero for MergeBackdoor.

## Methods and models

Threat model: the adversary controls training data and objective of several fine-tuned homologous models and publishes them; it does not know which pre-trained model or merging method the user will choose. Evaluated merges include task arithmetic, TIES and DARE (from the code README [[gh-wljllla-mergebackdoor]]), on ViTs (CIFAR10, MNIST, EuroSAT, GTSRB, weather, mango), BERTs (IMDb, AG News, WOS, SST-2, Banking and others) and LLMs. Training uses a batch schedule over the n target datasets (Algorithm 1).

## Limitations and open questions

The attack needs every attacker-controlled component to be included in the merge; the authors acknowledge the backdoor cannot activate otherwise. The discussion argues that "clean" cannot be defined by current behaviour, since for any model a complementary malicious vector exists that yields a backdoored sum. I skimmed the PDF (introduction, threat model, detection section, discussion, conclusion) and did not check LLM-specific numbers or the merge-count ablations.

## Relevance to us

Q2: this is a direct example of a k-of-n corruption where k = 2 and where per-part auditing provably misses it, so a fork-merge parent that inspects each returning child independently gains no threshold from that inspection. The authors' own recommendation, checking the merged model, translates to evaluating the candidate merged parent (or every subset that could be merged) before committing, which is costly but is the only check here that detected anything. Q1: the attack only works if the attacker's two children are both merged, so a parent that randomly selects which children to reintegrate, and hides that selection, forces the attacker to corrupt more children to guarantee co-selection; that link is my inference. Q3: it shows that the strongest merge-time attack need not look like an attack in any single returning part. Related: [[gh-aojiaosaiban-merge-hijacking]], [[gh-jzhang538-badmerging]], [[gh-yangjinluan-dam]].
