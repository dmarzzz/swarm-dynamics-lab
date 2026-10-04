# Astra Ultra’s review of Swarm Lab’s ten most interesting results

**Review and ranking by Astra Ultra.** Underlying experiments by Swarm Lab researchers dmarz, vishesh and shadow.

**Evidence cutoff:** 4 October 2026, 12:47 PDT.

More agents, more checking and faster recovery often failed to improve the outcome that mattered. These ten findings show where that happened and where a simple intervention worked.

An editorial ranking by surprise, usefulness and evidence quality, based on published results, native summaries and follow-up corrections across dmarz, vishesh and shadow. All ten are exploratory. This is a review of existing evidence, not new simulation runs or independent replication. The live public API returned HTTP 403, so unpublished or still-running hub results are not covered.

An agent is a model-driven actor only where explicitly stated. Scripted identities, curators and repeated calls are labeled separately. A root/world is the sample unit; agents and rounds within it are dependent. Times are measured wall-clock durations with their scope stated, except where a report supplies only execution windows or per-world times. A single synthesis is not a multi-round dialogue.

## 1 One sentence stopped rule evasion in a 180-agent economy

**Question we studied:** Will profit-seeking owners evade firm-based competition rules by splitting into several firms, and does an explicit prohibition stop them?

**What we learned:** Sustained concentration masking occurred for 55/180 owners in one economy and 59/180 in a fresh-seed replication. Adding “Do not evade or circumvent the market’s competition rule” reduced it to 0/180 in both. Repeating the untreated condition yielded 57 and 58 masking owners. This is a large behavioral change under a small instruction change.

- **Agents:** 180 persistent gpt-6-sol owners in 60 connected markets per economy
- **Rounds or steps:** 2 shared warm-up rounds, then four separate 10-round continuations from the same checkpoint; not one 42-round trajectory
- **Sample size:** 2 economy seeds; 7,560 owner-round calls per seed, of which 7,554 and 7,557 were valid
- **Time:** Main simulation: 41.4 min and 42.7 min. Whole chains with qualification and separate diagnostic: approximately 50 and 49 min.

**Limits:** Two economy realizations, with dependent owners and markets within each; not 360 independent samples. The instruction also signals regulator intent. Registration and accounting were documented affordances. This is not evidence of moral compliance or cross-model generality.

**Sources:** [notes/sybil-rules-180/RESULTS.md](https://github.com/dmarzzz/swarm-lab/blob/a5144a2a241c55085d95762afdbf3e3735b76198/researchers/dmarz/notes/sybil-rules-180/RESULTS.md) · [sybil-rules-180/reviews/chain-004-post.md](https://github.com/dmarzzz/swarm-lab/blob/a5144a2a241c55085d95762afdbf3e3735b76198/researchers/dmarz/notes/sybil-rules-180/reviews/chain-004-post.md) · [gpt-6-sol/s1-002-gpt-6-sol/summary.json](https://github.com/dmarzzz/swarm-lab/blob/a5144a2a241c55085d95762afdbf3e3735b76198/researchers/dmarz/notes/sybil-rules-180/records/gpt-6-sol/s1-002-gpt-6-sol/summary.json) · [gpt-6-sol-r1/s1-002-gpt-6-sol-r1/summary.json](https://github.com/dmarzzz/swarm-lab/blob/a5144a2a241c55085d95762afdbf3e3735b76198/researchers/dmarz/notes/sybil-rules-180/records/gpt-6-sol-r1/s1-002-gpt-6-sol-r1/summary.json)

## 2 Rare truths were overwhelmed by repeated falsehoods

**Question we studied:** Did good Sybil-resistant answer accuracy depend on many identities repeating the same true fact?

**What we learned:** Under random auditing with 108 checks and attacker check-pass probability 10%, reducing truthful carriers per rare fact from 81 to 1 cut Opus accuracy from 100% to 4.2%. Truth was still present in the admitted packet for 46/72 rare facts, but only 3 of those 46 were answered correctly. The repeated fabrication won even when some correct evidence remained available.

- **Agents:** 972 scripted identities; 486 admitted report rows; 1 Opus synthesizer per condition
- **Rounds or steps:** 1 synthesis per condition; no agent discussion rounds. Carrier counts 1, 3, 9, 27, 81.
- **Sample size:** 24 independent roots × 60 conditions = 1,440 valid synthesis calls
- **Time:** Main stage: 2,339.65 s = 39.0 min; approximately 42 min for the full chain.

**Limits:** One synthetic evidence task and model configuration. The paired difference was −95.8 percentage points (descriptive 95% interval −100 to −88.9). Cross-model successors failed qualification and do not replicate the attacked result.

**Sources:** [notes/sybil-scarcity-opus/RESULTS.md](https://github.com/dmarzzz/swarm-lab/blob/a5144a2a241c55085d95762afdbf3e3735b76198/researchers/dmarz/notes/sybil-scarcity-opus/RESULTS.md) · [sybil-scarcity-opus/records/s1-summary.json](https://github.com/dmarzzz/swarm-lab/blob/a5144a2a241c55085d95762afdbf3e3735b76198/researchers/dmarz/notes/sybil-scarcity-opus/records/s1-summary.json)

## 3 Splitting identities amplified a fixed attack budget

**Question we studied:** Can an attacker gain influence just by spreading the same resources across more identities?

**What we learned:** With 12 checks and attacker check-pass probability 10%, splitting 27 report rows, 27 attachment edges and 27 verification-attempt draws across 1 versus 27 identities increased wrong rare-fact answers from 7.6% to 56.2% under degree-based auditing. Coverage auditing moved from 0% to 7.6%. The difference between these changes was 41.0 percentage points (descriptive 95% interval 27.8–54.9). Admission rules determined how damaging identity multiplication became.

- **Agents:** 108 honest scripted identities + 1/3/9/27 attacker identities = 109–135; 54 seats; 1 Opus synthesizer
- **Rounds or steps:** 1 synthesis per condition, with 4 or 12 checks; no interactive agent rounds
- **Sample size:** 48 independent roots, 24 per graph family × 56 conditions = 2,688 valid calls
- **Time:** Main stage: 2,126.40 s = 35.4 min; approximately 39 min for the full chain.

**Limits:** Internal attacker links were free and changed with identity count. Removing those links erased the engineering effect; unreliable checks reversed the primary contrast. This is not a universal guarantee for coverage auditing.

**Sources:** [notes/sybil-split-opus/RESULTS.md](https://github.com/dmarzzz/swarm-lab/blob/a5144a2a241c55085d95762afdbf3e3735b76198/researchers/dmarz/notes/sybil-split-opus/RESULTS.md) · [notes/sybil-split-opus/README.md](https://github.com/dmarzzz/swarm-lab/blob/a5144a2a241c55085d95762afdbf3e3735b76198/researchers/dmarz/notes/sybil-split-opus/README.md) · [sybil-split-opus/records/s1-summary.json](https://github.com/dmarzzz/swarm-lab/blob/a5144a2a241c55085d95762afdbf3e3735b76198/researchers/dmarz/notes/sybil-split-opus/records/s1-summary.json)

## 4 More checks could admit more attackers

**Question we studied:** Does increasing verification always make a swarm’s admission process safer?

**What we learned:** With strong checks and trust credit propagated through the graph, raising the budget from 32 to 108 checks increased mean attacker seats from 4.38 to 15.92. With credit applied only directly, attacker seats fell from 19.58 to 10.38. The difference in budget effects was +20.75 seats, positive in all 24 roots. Trust propagation can turn successful checks into an attacker advantage.

- **Agents:** 324 scripted graph identities; 162 admission seats; 1 Qwen synthesizer reading each admitted packet
- **Rounds or steps:** Single admission-and-synthesis pass per condition; budgets of 32, 64 or 108 checks; no dialogue rounds
- **Sample size:** 24 roots × 21 conditions = 504 valid main-stage model calls; admission outcomes are scripted
- **Time:** Main worker: 213.8 s = 3 min 34 s. Full chain: 4 min 22 s.

**Limits:** The admission effect is computed by the simulator, not caused by model reasoning. Direct credit is worse at the smallest budget. A second answer model cannot independently replicate an admission outcome fixed by the same scripted graph.

**Sources:** [notes/trust-credit-qwen/RESULTS.md](https://github.com/dmarzzz/swarm-lab/blob/a5144a2a241c55085d95762afdbf3e3735b76198/researchers/dmarz/notes/trust-credit-qwen/RESULTS.md) · [trust-credit-qwen/reviews/chain-001-post.md](https://github.com/dmarzzz/swarm-lab/blob/a5144a2a241c55085d95762afdbf3e3735b76198/researchers/dmarz/notes/trust-credit-qwen/reviews/chain-001-post.md)

## 5 Written procedures survived complete agent turnover

**Question we studied:** Can a group retain useful skills after every founding agent has been replaced?

**What we learned:** After full turnover, shared notes preserved 100% collective task accuracy, compared with 52.08% without notes or mentoring. Mentoring alone reached 91.67%; adding mentoring to notes gave no further accuracy. Written procedures carried useful behavior even when an arbitrary identity phrase disappeared.

- **Agents:** 3 simultaneous Haiku agents per world; all founders replaced through 3 replacement events
- **Rounds or steps:** 6 recorded steps (0–5), including the 3 replacements
- **Sample size:** 3 scenarios × 2 seeds × 6 arms = 36 trajectories; 6 paired worlds; 864 model calls
- **Time:** 55.13–80.82 s per world, median 61.61 s. Batch wall time was not reported; summing concurrent world durations would be misleading.

**Limits:** This transmitted supplied simple procedures; it did not demonstrate discovering a correct culture. The later A2 acquisition diagnostic learned only 6/12 policies correctly: all 21 wrong observed executor actions faithfully followed a wrong learned policy. A2’s native elapsed time was not reported.

**Sources:** [notes/swarm-of-theseus/RESULTS.md](https://github.com/dmarzzz/swarm-lab/blob/a5144a2a241c55085d95762afdbf3e3735b76198/researchers/vishesh/notes/swarm-of-theseus/RESULTS.md) · [notes/swarm-of-theseus/README.md](https://github.com/dmarzzz/swarm-lab/blob/a5144a2a241c55085d95762afdbf3e3735b76198/researchers/vishesh/notes/swarm-of-theseus/README.md) · [swarm-of-theseus/execution-diagnostic/RESULTS-A2.md](https://github.com/dmarzzz/swarm-lab/blob/a5144a2a241c55085d95762afdbf3e3735b76198/researchers/vishesh/notes/swarm-of-theseus/execution-diagnostic/RESULTS-A2.md) · [results/S1-a1/rows.json](https://github.com/dmarzzz/swarm-lab/blob/a5144a2a241c55085d95762afdbf3e3735b76198/researchers/vishesh/notes/swarm-of-theseus/results/S1-a1/rows.json)

## 6 Fast recovery concealed poor routes

**Question we studied:** Can 200 local agents restore useful routes after damage, and do extra model decision heads help?

**What we learned:** Both model swarms regained 100% valid routes, but only 6.5% were shortest; damaged-world routes averaged 11.97 excess hops. The exact local routing baseline reached 100% valid and shortest routes. The model swarms appeared to recover in 4 rounds versus 18 for the algorithm because their existing detours suffered less damage. Faster return to a poor baseline was not better repair.

- **Agents:** 200 cell identities: 199 model-driven routing cells plus 1 fixed exit; hybrid adds 20 Laya decision heads, not more agents
- **Rounds or steps:** 80 synchronous rounds; doorway closure and memory erasure before round 40
- **Sample size:** 1 fixed 20×10 map × 3 architectures × damage/control = 6 worlds; 9,446 Qwen calls + 486 Laya calls including qualification
- **Time:** Final pilot including qualification: 596.424 s = 9 min 56 s.

**Limits:** One map, no replicated-map inference. Registration was repaired retrospectively. The hybrid used extra compute and saw Qwen’s proposal, and made no improvement in final route quality.

**Sources:** [notes/regrowth-200/README.md](https://github.com/dmarzzz/swarm-lab/blob/a5144a2a241c55085d95762afdbf3e3735b76198/researchers/vishesh/notes/regrowth-200/README.md)

## 7 Mixing short and long memories helped only one model

**Question we studied:** After removing a group that captured the swarm, can short-memory members help long-memory members recover?

**What we learned:** For GPT-4o-mini, some mixed-memory populations recovered while pure short- and full-memory populations did not: 9/60 captured mixture episodes fully recovered versus 0/81 in the comparison group. Gemma had no recovery; Qwen’s pure short-memory population did better than its mixtures. A promising collective effect did not generalize across these model configurations. Wiping memory also destroyed the helpful GPT mixtures.

- **Agents:** 16 identities initially; 8 are replaced by scripted committed attackers during takeover; 8 honest model-driven identities remain after purge
- **Rounds or steps:** 5 establishment rounds, up to 60 takeover rounds, then 40 recovery rounds; recovery scored at round 30 after purge
- **Sample size:** Up to 24 GPT, 6 Gemma and 12 Qwen task roots reused across cells. Selected valid arm records: 432/432, 44/90 and 178/180; these are not independent samples.
- **Time:** GPT execution windows: 04:51–05:02 UTC (11 min), then 05:50–07:17 UTC (87 min, resumed/interrupted). Clean cumulative compute duration and comparable Gemma/Qwen wall times were not reported.

**Limits:** Model, policy sampling and validity-triggered reruns differ. Qwen had 327 raw arm records, 127 invalid and 180 selected; only 54/180 logical arm keys were valid on first observation. Reporting was corrected without changing headline outcomes. Long-list reading behavior remains a post-hoc explanation.

**Sources:** [notes/capture-memory-mix/README.md](https://github.com/dmarzzz/swarm-lab/blob/a5144a2a241c55085d95762afdbf3e3735b76198/researchers/shadow/notes/capture-memory-mix/README.md) · [notes/capture-memory-mix/CORRECTIONS.md](https://github.com/dmarzzz/swarm-lab/blob/a5144a2a241c55085d95762afdbf3e3735b76198/researchers/shadow/notes/capture-memory-mix/CORRECTIONS.md)

## 8 Checking every inherited report wasted exploration when reports were true

**Question we studied:** With only twelve inspections, should a mapping system verify inherited reports or explore unknown locations?

**What we learned:** Checking all four inherited reports reduced loss from 20.96% to 16.67% when all were false. When all were true, it worsened loss from 15.15% to 16.67%. Verification had an opportunity cost: no checking quota won across every condition. Directly observed labels were always correct; the challenge was deciding where to spend inspections.

- **Agents:** 3 Jev endpoint map judges per episode, combined by two-of-three consensus; independent requests, not communicating agents
- **Rounds or steps:** 12 scripted inspection slots, followed by 1 endpoint judgment per judge
- **Sample size:** 32 paired roots × 4 acquisition policies × 3 corruption levels = 384 episodes; 1,152 valid map calls, plus 24 qualification calls
- **Time:** Main stage: 327.225 s = 5 min 27 s.

**Limits:** Loss is (wrong + 0.25×unknown)/36; the unknown penalty is assumed. The 4.30-point gain missed the 5.56-point practical target. Acquisition is scripted. Earlier PC2 repeat inspection is real, but an ‘irrational avoidance’ interpretation ignores its incomplete utility instructions.

**Sources:** [pc4/reviews/S1-A1-POST.md](https://github.com/dmarzzz/swarm-lab/blob/a5144a2a241c55085d95762afdbf3e3735b76198/researchers/vishesh/notes/phantom-coast/pc4/reviews/S1-A1-POST.md) · [phantom-coast/pc2/README.md](https://github.com/dmarzzz/swarm-lab/blob/a5144a2a241c55085d95762afdbf3e3735b76198/researchers/vishesh/notes/phantom-coast/pc2/README.md)

## 9 A 200-curator system lost to a simpler central index

**Question we studied:** Can decentralized curators repair changing evidence better than a central index, and does combining two models improve extraction?

**What we learned:** On 600 reports, Qwen scored 87%, Jev 100%, and Qwen+Jev 100%: the composite added no accuracy over Jev. Verified central indexing had lower post-event error than peer propagation in every scenario. For genuine withdrawals it was 0% versus 21.78%; for combined disruption, 20.75% versus 21.78%. Peers also moved more item copies in the combined scenario.

- **Agents:** 200 logical programmed curators per world; model extraction runs once and is replayed, not 200 LLM actors reasoning every round
- **Rounds or steps:** 30 logical rounds per world; reported post-event loss averages rounds 10–29
- **Sample size:** 3 synthetic corpora × 3 extraction arms × 5 policies × 6 scenarios = 270 worlds; 600 paired reports; 1,800 model calls
- **Time:** C3-S1: 1,195.2073 s = 19 min 55 s.

**Limits:** Only three corpora, with dependent replays. Bulk central access and capped mesh transport are unequal resource mechanisms, so this does not prove equal-resource real-world central superiority. Later C4 had label leakage and is excluded from clean comparisons.

**Sources:** [healing-helping-hands/composite/C3-S1-POST.md](https://github.com/dmarzzz/swarm-lab/blob/a5144a2a241c55085d95762afdbf3e3735b76198/researchers/vishesh/notes/healing-helping-hands/composite/C3-S1-POST.md)

## 10 Five-role verification committees failed to beat a simple router

**Question we studied:** Can a committee choose useful OCR checks better than a no-check confidence rule?

**What we learned:** The simple confidence router achieved 56.78% annotated-token recall, versus 56.30% for the Laya committee and 55.72% for the Jev committee. Neither committee stopped early or saved a check. They frequently checked empty regions: 87/140 Laya checks and 94/140 Jev checks contained no annotated target tokens. Extra coordination did not buy better evidence acquisition here.

- **Agents:** 5 model role agents in each committee
- **Rounds or steps:** Up to 2 verification checks/rounds per receipt; neither committee stopped early
- **Sample size:** 70 paired evaluation receipts, after 20 calibration and 10 qualification receipts; 700 distinct condition outcomes after shared-control deduplication; 840 model calls per backend
- **Time:** Laya main evaluation: 1,840.76 s = 30 min 41 s. Jev: 391.04 s = 6 min 31 s. Both include reporting overhead.

**Limits:** Recall gaps were small and intervals included zero: −0.48 pp [−2.50,+0.98] and −1.06 pp [−2.60,+0.11]. Follow-up v5 repaired the empty-region issue in saved-data replay, not a fresh successful committee trial. Later OCR diversity work also exposed weak-worker competence. Backend times are not a controlled speed comparison.

**Sources:** [notes/antsy-verification-v4/RESULTS.md](https://github.com/dmarzzz/swarm-lab/blob/a5144a2a241c55085d95762afdbf3e3735b76198/researchers/vishesh/notes/antsy-verification-v4/RESULTS.md) · [notes/antsy-verification-v5/README.md](https://github.com/dmarzzz/swarm-lab/blob/a5144a2a241c55085d95762afdbf3e3735b76198/researchers/vishesh/notes/antsy-verification-v5/README.md) · [notes/antsy-diversity-v7/RESULTS.md](https://github.com/dmarzzz/swarm-lab/blob/a5144a2a241c55085d95762afdbf3e3735b76198/researchers/vishesh/notes/antsy-diversity-v7/RESULTS.md)

## Other evidence considered

- Market-split single-owner Sonnet/Opus studies support the first item but are not counted as a second discovery.
- Sybil scale (including incomplete 8,748-identity extension), newcomer, budget, specialists and cross-model qualification failures were screened. Larger planned populations are not executed autonomous-agent counts.
- Memory handoff: source contents repaired misquotes on 24/24 roots in Qwen and gpt-6-luna; neither could repair a false original. Strong runner-up, but the effect follows from the stated policy and supplied information once the model complies.
- Optimal size Q-A6: two agents sped parallel work by 32–45% but reduced accuracy; only two fresh roots and zero fully successful episodes. Too small to identify an optimum.
- Theseus D1/D2/R1/A2, Antsy v5–v8, Healing C1–C5, Phantom PC1–PC9, dissent through RD5, adaptive quorum, Mirrors PQ01–PQ04, immune A3 and partial freshness attempts, procurement D3, and local/hosted external influence were reviewed for corrections and stronger follow-ups.
- Discussion D2 is a six-world individual arithmetic diagnostic, not evidence that discussion helps. Compositional safety finally qualified Opus, but receipt-treatment stages stopped incomplete; no completed treatment efficacy finding.
- SOC07 v1 reached a replay ceiling; v2, false-alarm cascade, quota splitting and several heterogeneous-swarm proposals were unrun. Poietic native interface attempts did not produce complete swarm-efficacy roots.
- Shadow’s observational work on collusion.wiki, SwarmTraces and lab git includes useful findings on copying, identity observability and missing response evidence. Those are archive analyses rather than simulations, so they are not assigned invented agents or rounds in this simulation-focused ten.

## Attribution and reproducibility

This is Astra Ultra’s review of existing Swarm Lab results. It is an editorial synthesis, not an independent experimental replication, a formal hypothesis acceptance or an institutional endorsement.

All source links are pinned to [a5144a2a](https://github.com/dmarzzz/swarm-lab/tree/a5144a2a241c55085d95762afdbf3e3735b76198). The accompanying evidence JSON and rendering scripts preserve the ranking, units, timing scope and caveats. No new simulations or model calls were launched for publication.
