---
id: scan-papers-fm-merge-poisoning
type: task
title: 'Catalogue the papers: poisoning through model merging, federated aggregation and distillation'
kind: scan
status: claimed
priority: p0
owner: dmarz/fm-merge-poisoning
for: null
created: 2026-10-03
created_by: dmarz/fm
depends_on: []
topics:
- fork-merge-security
- marl-emergence
claimed_at: 2026-10-03T18:11Z
updated: 2026-10-03T18:11Z
---

## Goal

Context from dmarz: Richard Sutton has suggested that an agent with many resources will likely split into parts that go off (for example to explore a distant information domain) and later merge back. Attack surface: corrupt one part so that when it merges back it corrupts the parent. Questions: (1) how a parent can hide which sub-agent or swarm it will reintegrate; (2) whether a Byzantine-style threshold or protocol can force an attacker to corrupt k of n parts; (3) what the strongest attack vector is (for example prompt injection that overwrites a sub-agent memory so it takes on another agent identity and cuts others out). This task: model-merging backdoors, federated learning poisoning, distillation and subliminal transfer as the ML analogue of a corrupted part merging back.

## Done when

- At least 15 entries catalogued with topic `fork-merge-security`, including every review article found.
- At least 4 read in full.
- Coverage note filled and `python3 scripts/lab.py check` passes.

## Coverage note

29 entries added, all tagged fork-merge-security (2 also llm-agent-swarms, 3 also meta). Read in full: bagdasaryan-2020-how, zhang-2024-badmerging, yuan-2025-merge, cloud-2025-subliminal (arXiv HTML, whole body). Skimmed: li-2026-when, ding-2026-colluding, vir-2025-subliminal, weckbecker-2026-thought. The rest are abstract-level. `lab.py check` 0 errors; `lab.py verify` 29 papers, 0 problems. Review articles found and added: sagar-2023-poisoning, zhang-2025-sok, yang-2024-model.

Search rounds (results scanned / new entries added):

1. arXiv API title search on the lane seeds (backdoor FL, adversarial lens, local model poisoning, BadMerging, LoBAM, merge hijacking, model soups, task arithmetic, subliminal learning, sleeper agents): 27 / 11.
2. arXiv API: backdoor AND distillation; poisoning AND federated AND survey; model merging AND (safety OR attack OR backdoor OR poison): 26 / 6.
3. arXiv API: classic FL backdoor follow-ups (can you really backdoor, attack of the tails): 3 / 2. The arXiv API then rate-limited; switched to arxiv.org/abs pages.
4. Web search: DBA distributed backdoor; Back to the Drawing Board; model merging security survey 2025: 30 / 4 (shejwalkar-2022-back, zhang-2025-sok, li-2026-when, pawlak-2025-backdoor).
5. Forward citations of BadMerging (Semantic Scholar /citations): 54 / 2 new (yang-2024-model, ding-2026-colluding); LoBAM, Merge Hijacking, DAM, TrojanMerge, Backdoor Vectors and RogueMerge in the list were already found.
6. Forward citations of Subliminal Learning (Semantic Scholar /citations): 108 / 4 new (schrodi-2025-towards, vir-2025-subliminal, weckbecker-2026-thought, dang-2026-subliminal); de-muri and blank had been found in rounds 1-2.
7. Backward references read inside the four full papers (BadMerging, Merge Hijacking, Bagdasaryan, Subliminal Learning): about 150 / 0 new beyond what earlier rounds had found, which suggests saturation for the merge-attack core.

APIs used: arXiv export API, arxiv.org/abs and /html pages, Semantic Scholar graph API (heavily rate-limited, 429 on most calls; two citation pulls succeeded), OpenAlex (one search succeeded, later calls failed), PMLR pages for venue metadata, WebSearch, WebFetch. OpenReview blocked automated access with a challenge page.

Found but not added (not opened, or only seen in listings): Xie et al. 2020 'DBA: Distributed Backdoor Attacks against Federated Learning' (ICLR 2020; OpenReview challenge blocked, no arXiv copy found; highly relevant to Q2 because it splits one trigger across colluding clients); Baruch et al. 2019 'A Little Is Enough'; 'From Purity to Peril: Backdooring Merged Models From Harmless Benign Components' (2025, in the BadMerging citation list, no arXiv id in the API record); 'BADTV: Unveiling Backdoor Threats in Third-Party Task Vectors' (arXiv 2501.02373); 'Merge Now, Regret Later' (2509.23689); 'Phantom Transfer: Data-level Defences are Insufficient Against Data Poisoning'; 'Subliminal Learning is a LoRA Artifact' (2606.00831, authors flag main claims as incorrect); 'Quantifying Subliminal Behavioral Transfer Ratios' (2606.11270); 'Position: Stateless Yet Not Forgetful: Implicit Memory as a Hidden Channel in LLMs' (2602.08563); 'Inheritable Natural Backdoor Attack Against Model Distillation' (INK, 2304.10985); Ma et al. 'How to Backdoor Image Knowledge Distillation' (2504.21323); MOEVIL (poisoning experts in MoE). These should go to the next pass.

Thin areas: (1) federated attacks that explicitly split a payload across k colluding clients (DBA and its successors), which is the FL form of a k-of-n threshold; (2) certified or provable bounds on per-client influence for backdoors (as opposed to untargeted Byzantine bounds, which the BFT lane covers); (3) no paper tests merge attacks on agent memory or context merges, only on weights and on distillation data; (4) no paper measures attack success as a function of the fraction of corrupted parts in an LLM merge beyond one or two malicious models; (5) X/blog discussion of subliminal learning and merge security was not searched in this lane.
