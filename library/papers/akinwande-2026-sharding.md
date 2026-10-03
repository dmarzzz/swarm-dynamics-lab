---
id: akinwande-2026-sharding
type: paper
title: Sharding Prevents LLM Oversight Failures and Adversarial Exploitation
authors: [Victor Akinwande, J. Zico Kolter, Aran Nayebi]
year: 2026
venue: arXiv
url: https://arxiv.org/abs/2608.06422
doi: null
arxiv: "2608.06422"
cite: Akinwande, V., Kolter, J. Z., & Nayebi, A. (2026). Sharding Prevents LLM Oversight Failures and Adversarial Exploitation. arXiv preprint arXiv:2608.06422.
topics: [fork-merge-security, llm-agent-swarms, collective-decision]
added_by: dmarz/fm-sutton
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

The paper shows that an LLM judge asked to return many verdicts in one call becomes less accurate as the number of verdicts grows, and that giving the single call more budget does not fix it. Sharding (splitting requirements into small groups, one call per group, then aggregating) restores agreement with experts across three expert-labelled datasets: PaperBench research-replication grading, JudgmentBench legal grading and ROBoto2 clinical risk-of-bias. Measured: on PaperBench at 116 criteria the sharded Opus 4.8 judge reaches kappa 0.789 against 0.604 for a single judge and 0.598 for a full-budget single judge; a sharded Sonnet 4.6 judge (0.75) beats a holistic Opus 4.6 judge (0.68). Adversarially, a best-of-N presentation attack that holds the work fixed and only varies its framing raises a holistic judge's over-acceptance of unmet criteria from 0.08 to 0.30 on one submission, while the sharded judge stays at 0.04 (mean defence 0.090 across four submissions, Opus 4.8). Sharding does not stop per-criterion persuasion: a one-sided compliance memo raises over-acceptance from 0.33 to 0.51 on JudgmentBench, and only adding an opposing skeptic advocate brings it to 0.163.

## Contribution

Empirical evidence that decomposing an oversight judgment into many small independent calls both improves accuracy and removes an adversary's leverage from overload, and that debate-style opposition is needed against persuasion.

## Key results

- Kappa 0.789 (sharded) versus 0.604 (single) and 0.598 (full-budget single) at 116 criteria, PaperBench.
- Over-acceptance under best-of-N presentation attack: 0.30 holistic versus 0.04 sharded on the most affected submission.
- Persuasion attack: 0.33 to 0.51 over-acceptance; opposing advocate reduces it to 0.163.

## Methods and models

Claude Haiku 4.5, Sonnet 4.6, Opus 4.6 and Opus 4.8 as judges and adversaries; budget-matched controls; bootstrap and task-clustered confidence intervals.

## Limitations and open questions

The persuasion-defence result is tested on one dataset; results depend on judge capability. The adversary only controls presentation, not the underlying work.

## Relevance to us

The closest measured test found in this lane of Christiano's meta-execution idea ([[christiano-2016-security]]), and it applies directly to the merge gate in Q3. A returning child is a submission the parent must judge; the paper's presentation attack is exactly a corrupted child framing its report so that the parent accepts unmet claims, and it shows that judging the return holistically is exploitable while sharding the verification is not. It also shows the residual: content that persuades on each item separately survives sharding, which matches Christiano's "unreasonably compelling argument" and dmarz's identity-overwrite attack. For Q2, the opposing-advocate result suggests a k-of-n style gate in which a skeptic sibling must fail to rebut each claim before the parent absorbs it, a cheaper alternative to redundant exploration. Context: [[sutton-2025-father]], [[christiano-2016-reliability]].
