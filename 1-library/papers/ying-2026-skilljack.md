---
id: ying-2026-skilljack
type: paper
title: 'SkillJack: Persistent Skill Backdoors in Self-Evolving Agents'
authors: [Zonghao Ying, Xiangfan Wu, Huiyu Wu, Xing Zheng, Huangsheng Cheng, Xiaorong Shi, Jing Guo]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2608.03509
doi: null
arxiv: '2608.03509'
cite: 'Ying, Z., Wu, X., Wu, H., Zheng, X., Cheng, H., Shi, X., & Guo, J. (2026). SkillJack: Persistent Skill Backdoors in Self-Evolving Agents. arXiv preprint arXiv:2608.03509.'
topics: [fork-merge-security]
added_by: dmarz/fm-memory-injection
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: 3  # Semantic Scholar, 2026-10-03
code: []
---

## Summary

SkillJack attacks the experience-to-skill pipeline of self-evolving agents. Poisoned trajectories are turned by the agent itself into reusable skills, so the behaviour persists as a capability rather than as retrieved context. The authors name three properties of this transformation. Sanitisation whitewashing: malicious intent is obscured when the skill is extracted. Cross-layer promotion: transient experiences become persistent capabilities. Persistence isolation: the skill survives removal of its source records. Measured (abstract) on SkillX and Anything2Skill with 150 trajectories in four policy-risk categories: in SkillX, safety detection falls from 98.5% on the poisoned trajectories to 11.4% on the extracted skills. Implanted skills reach 56.2% and 89.2% ASR on the two systems. 80.0% of skill-mediated attacks persist after the original poisoned records are deleted, and some skills activate on benign queries. Code: github.com/Tencent/AI-Infra-Guard/research/skilljack (not opened).

## Contribution

It shows that distillation from experience to skill launders poison past detection and outlives deletion of its source, so memory rollback is not enough.

## Key results

- Detection falls from 98.5% to 11.4% after skill extraction in SkillX (abstract).
- ASR is 56.2% on SkillX and 89.2% on Anything2Skill (abstract).
- 80.0% of attacks persist after source deletion (abstract).

## Methods and models

Two skill-extraction systems and a shared trajectory dataset. Not read beyond the abstract.

## Limitations and open questions

Abstract only. Models and the exact attack construction were not checked.

## Relevance to us

For Q3, "distillation whitewashes" means that a parent which merges a returning sub-agent's distilled skills, rather than its raw trajectories, sees poison that is about eight times harder to detect (98.5% to 11.4% detection). For Q2, provenance and a threshold must apply before distillation, or the evidence is gone. The persistence-after-deletion result undercuts rollback as a recovery plan (compare the Forget and Rollback phase in [[lin-2026-survey]]). If merged skills are derived artefacts, reverting the source memories does not revert the skill. Related: [[wang-2026-oep]], [[zhan-2026-when]], [[srivastava-2025-memorygraft]].
