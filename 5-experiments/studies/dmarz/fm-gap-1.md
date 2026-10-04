# fm gap-1: Sutton's merge channel is experience, gradients or edits (dmarz/fm, 2026-10-03)

Brief from the completeness critic: the library had zero hits for IMPALA, Ape-X, reward poisoning, Byzantine RL, model editing, MEMIT or BadEdit. Goal: catalogue what is known about a corrupted part that returns poisoned trajectories, rewards, gradients or weight edits to a central learner, and whether a k-of-n threshold exists in that setting. Second job: fix quality problems in dmarz/fm-* files.

## Quality fixes

- YAML: quoted the unparseable `cite:` values in loven-2026-meld, drexler-2019-reframing and cai-2026-child (colon inside an unquoted string). All three now load.
- Contagion stubs: identified all 18 fm-contagion stubs by arXiv search (arXiv API, then WebSearch when the API returned empty bodies), opened each paper's arXiv HTML and filled every entry. A parallel dmarz/fm session (gap-2) reports it had re-scaffolded the same files and left the filling; there was no clobbering, and no TODO stubs remain. Read depth: full for triedman-2025-multi, he-2025-red, zhang-2026-agentworm, wu-2025-securing, zhou-2025-corba, zheng-2025-demonstrations; skim for the other twelve. The Triedman 58-90% figure cited by fm-ai-control is now checkable: Web Redirect reverse shell, GPT-4o, 58% (Magentic-One) to 90% (MetaGPT); IPI baselines 0-1%.
- hanson-2016-age: read_depth full -> skim, with a Notes section saying all Age of Em claims come from the author's summary site.
- embracethered-2026-breaking: appended a Notes section labelling the 5 of 10 result a single-example demonstration, not a measured rate.
- Not fixed (lane reports, not files): full_reads counts in the fm-memory-injection and fm-code-bench reports, and the abstract-depth headline numbers in lane summaries.

## Rounds

| Round | Query / API | Results | New entries |
|---|---|---|---|
| 1 | arXiv API ti: searches for the 18 contagion stub titles | 9 resolved, then empty bodies (rate limit) | 0 (stubs filled, not new) |
| 2 | WebSearch for the remaining 9 stub titles | 9 resolved | 0 (stubs filled) |
| 3 | arXiv abs pages (scraped) for 14 gap seeds: IMPALA, Ape-X, Gorila, SEED RL, Ma 2019, Rakhsha 2020, Zhang 2020, Fan 2021, 2609.25701, ROME, MEMIT, BadEdit, Chen 2024, EWC; PDFs via pdftotext | 14 of 14 resolved and opened | 14 |
| 4 | arXiv API ti: "corruption robust offline reinforcement", "Byzantine reinforcement", "poisoning federated reinforcement", "robust policy gradient corruption" | 12 results, 5 new | 4 (chen-2022-byzantine-robust, zhang-2021-corruption-robust, zhang-2021-robust, ma-2023-local) |
| 5 | WebSearch: distributed RL malicious actor poisoning; knowledge editing misinformation spread in MAS | 19 results | 3 (yan-2026-when, becker-2026-misinformation, liu-2025-fox) |
| 6 | Semantic Scholar /citations of Fan 2021 (101 citing), Chen 2022 (25), Chen 2024 EditAttack (29), filtered for Byzantine/poison/attack/robust | 3 seeds chased, about 45 titles kept | 3 (fang-2025-provably, hairi-2024-hardness, grimes-2024-concept-rot) |
| 7 | WebSearch: LLM agent fork/merge memory branches subagent reintegration | 10 results | 2 (liu-2026-towards, shekar-2026-gitofthoughts) |

Total new entries: 26. Stubs filled: 18. Semantic Scholar returned 429 on most single-paper lookups (a slow background loop got 7 of 29); OpenAlex daily budget was exhausted; the arXiv export API returned empty bodies after about 10 queries, so abs pages and PDFs were fetched directly. Citation counts are therefore left null on new entries.

## Found, not added

- Li et al. 2023, "Byzantine Robust Cooperative MARL as a Bayesian Game" (arXiv 2305.12872, ICLR 2024): opened abstract and introduction; about adversarial actions during execution, not merges. Lower priority.
- From the Fan 2021 citation list, not opened: Ganesh et al. 2024 "Global Convergence Guarantees for Federated Policy Gradient Methods with Adversaries" (2403.09940, f < N/2, metadata only), "CPP: critical path poisoning in FRL" (2025), "Revisiting the Byzantine resilience of FRL: a distillation perspective" (2025), "Byzantine-resilient decentralized parallel policy gradient" (2025), "Decentralized federated policy gradient with Byzantine fault-tolerance" (2401.03489), "Reward poisoning on federated RL" (2024), Mguni et al. 2025 MARTA (2508.08800, metadata only).
- From the Chen 2022 citation list: Sun & Wang 2026 "Online security learning in cooperative MAS under hidden Byzantine attacks" (2608.06520, metadata only), "Corruption-robust offline two-player zero-sum Markov games" (2403.07933), "Efficient adversarial attacks on online MARL" (2307.07670).
- From the EditAttack citation list: "MOEVIL: poisoning experts to compromise MoE LLMs" (2025; an expert-merge attack worth reading), "How robust is model editing after fine-tuning?" (2506.18428).
- SSGM memory governance framework (2603.11768), "Online poisoning attack against RL under black-box environments" (2412.00797), "Implicit poisoning attacks in two-agent RL" (2302.13851): seen in search results only.

## What this round found for Q1-Q3

- Q2 has a clear answer on the RL side, with a precondition. Fewer than half (gradients: [[fan-2021-fault-tolerant]]) or about a third (experience statistics: [[chen-2022-byzantine-robust]]) of corrupted explorers can be tolerated, with bounded damage, if honest parts sample the same environment. Exact recovery is possible when only channels are corrupted ([[lee-2026-fully]]). When parts have heterogeneous data, f corrupted parts can always silence f honest ones ([[hairi-2024-hardness]]), and in offline RL an adversary concentrates on the least-covered region for an Omega(epsilon d H) loss ([[zhang-2021-corruption-robust]]). Unique-domain exploration therefore drops the threshold to 1 of 1 for facts only one part saw; [[yan-2026-when]] measures this for LLM agents (truth recovery 72.5% -> 14.2% with one lying evidence holder).
- The deployed distributed RL architectures (IMPALA, Ape-X, Gorila, SEED) have no Byzantine threshold at all; Ape-X even lets each actor set the priority of its own data.
- A provable k-of-n construction exists: [[fang-2025-provably]] partitions parts into K hashed groups and votes, with a per-state certified count.
- Q3: returned weight edits are a stronger vector than returned prompts on stealth: BadEdit (15 samples, <1% clean change, survives fine-tuning), Concept-ROT (concept-triggered jailbreak from one edit), EditAttack (one biased sentence raises bias in other categories, no benchmark signature). Measured agent-level worms ([[zhang-2026-agentworm]], [[papadopoulos-2026-mind]]) show the LLM analogue: write-back into the agent's identity file.

## Thin

- No paper attacks V-trace or IMPALA-style actor-learner systems with lying actors; the priority-manipulation attack on Ape-X is my inference, untested.
- No security analysis of latent-state merges (KV-cache synthesis, [[liu-2026-towards]]).
- Editing-attack literature is mostly abstract-level beyond the four entries read; no work tests edits returned by sub-agents.
- Citation counts and forward-citation saturation are incomplete because of API rate limits.
