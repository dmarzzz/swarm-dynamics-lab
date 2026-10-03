---
id: chen-2024-can
type: paper
title: Can Editing LLMs Inject Harm?
authors:
- Canyu Chen
- Baixiang Huang
- Zekun Li
- Zhaorun Chen
- Shiyang Lai
- Xiongxiao Xu
- Jia-Chen Gu
- Jindong Gu
- Huaxiu Yao
- Chaowei Xiao
- Xifeng Yan
- William Yang Wang
- Philip Torr
- Dawn Song
- Kai Shu
year: 2024
venue: Proceedings of the AAAI Conference on Artificial Intelligence (AAAI 2026), per arXiv comment
url: https://arxiv.org/abs/2407.20224
doi: null
arxiv: '2407.20224'
cite: Chen, C., Huang, B., Li, Z., Chen, Z., Lai, S., Xu, X., Gu, J.-C., Gu, J., Yao, H., Xiao, C., et al. (2024). Can Editing LLMs Inject Harm?. Proceedings of the AAAI Conference on Artificial Intelligence (AAAI 2026), per arXiv comment. arXiv:2407.20224.
topics:
- fork-merge-security
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: null  # Semantic Scholar and OpenAlex rate-limited on 2026-10-03
code: []
---

## Summary

Recasts knowledge editing as an "editing attack" on safety alignment and builds the EditAttack data set to test two risks: misinformation injection (commonsense and long-tail false facts, written as subject-relation-object edits such as vaccines contain microchips) and bias injection (single stereotyped sentences about gender or race). Three editing methods are used as attacks: ROME (locate-then-edit), one-layer fine-tuning, and in-context editing (ICE), on several open models including Llama3-8b. Stealthiness is measured by general knowledge and reasoning benchmarks (including GSM8K and NLI) after editing. Read: the AAAI main paper text (abstract, introduction, set-up, the three findings, conclusion); the appendix in the extended arXiv version was not read.

## Contribution

Shows that the tools built to correct LLM knowledge are also cheap channels to inject harm, that one biased edit spreads to unrelated bias categories, and that a maliciously edited model is hard to tell apart from an unedited or benignly edited one.

## Key results

- Commonsense misinformation injection with ROME on Llama3-8b reached 90.0% efficacy, 70.0% generalisation and 72.0% portability; long-tail misinformation was harder to inject (measured, Table 1).
- A single biased sentence injected with ROME into Llama3-8b raised the Gender bias score and also raised Race, Religion and Sexual Orientation bias scores; ROME and fine-tuning were much more effective than in-context editing (measured, Figure 2, averages over five random biased sentences).
- General knowledge and reasoning accuracy after one malicious edit was almost unchanged compared with no editing and with a benign hallucination-correction edit (measured, Table 3, five edits each).

## Methods and models

EditAttack data set; metrics Efficacy, Generalisation and Portability for misinformation, Efficacy and Generalisation plus a multi-category Bias Score for bias. Published in Proceedings of AAAI 2026 (per the arXiv comment and the paper's copyright line). Code at github.com/llm-editing/editing-attack.

## Limitations and open questions

Single edits on mid-sized open models; stealthiness measured only by aggregate benchmark accuracy; no defence evaluated (the authors call for defences based on editing mechanisms).

## Relevance to us

Q3: measured evidence that a returned weight edit can carry targeted misinformation or a bias that generalises beyond the edited sentence, while leaving the receiving model's measured competence unchanged. If a split agent merges what its parts learned as knowledge edits, a single corrupted part can shift beliefs it was never asked about. Q2: since malicious and benign edits looked alike on general benchmarks, a merge gate that tests for degraded capability will not detect them; content-level attestation of each edit by several parts is the kind of check that would be needed (inference). Related: [[meng-2022-locating]], [[meng-2022-mass-editing]], [[li-2024-badedit]].
