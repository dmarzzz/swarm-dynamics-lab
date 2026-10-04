# Dataset and simulator update: scope and audit

Status: **human-requested, unreviewed hunches for selection**. This is a bounded update of the atlas, not a completed survey or authorization to run experiments. Snapshot: `bf74eb0` (2026-10-03). The 32 Hugging Face sweep additions were inventoried from `ad723697` through `7866552`; all 32 local records were read, together with the three new talk records. The simulator merge at `bf74eb0` added one further dataset record, also inspected below. Selected primary pages were opened below. No datasets were downloaded, no loaders or experiments were run, and no source record or read-depth field was changed. A catalogue entry establishes a lead, not verified availability, correct labels, a usable split or permission to redistribute data.

## Exact atlas changes

- Added **MTH-07–MTH-15**: independent relabelling, sequence-level splits, evaluator hindsight, translation effects, attempted-run reliability, session-versus-team identity, cross-task ranking validity, crawler effects, and entropy’s held-out predictive value.
- Added **SIM-05–SIM-07**: reconstructing outcomes from committed events, joint-action support in offline MARL, and deployable versus endpoint-wise best-of-many comparisons.
- Refined **RL-03**, **MTH-01–MTH-06**, **SIM-01–SIM-04**, and **PHY-03**, **PHY-23**, **PHY-25**. Existing IDs and core questions were retained; methods now has 44 entries and physical still has 38.
- No formal hypotheses, experiment protocols, new library records, analysis results, infrastructure changes or new claims of novelty were created. The parent handles overall synthesis, generated artifacts and repository checks.

## All 32 new dataset records inspected

The constraints below come from local catalogue cards except where a primary-page check is listed in the following section. Counts are source-reported, not a loader validation. Licences, configuration files and actual reuse conditions must be verified at the chosen revision before a finalist is promoted.

| Source | Consequential scope or prerequisite | Atlas use |
|---|---|---|
| [[data-agent-collusion-2026]] | Shared base task sequences across conditions; private reflections are not ordinary-monitor observations. | MTH-08; security lane owns mechanism tests. |
| [[data-agent-ipi-structured-2026]] | Synthetic structured clean/attacked pairs, not a swarm trace corpus; licence unspecified. | Security lead, no general prevalence claim. |
| [[data-agent-safetybench-2024]] | Task/environment test specifications are not automatically executed interaction trajectories. | Future controlled benchmark lead. |
| [[data-agent-town-economy-2026]] | Access to data/analysis does not include the simulation platform; run acceptance and export provenance require care. | MTH-03/04/11, SIM-05. |
| [[data-agentlogs-2026]] | Relational task/session/event tables; public repositories above a sampling threshold; user handles are not verified operators. | MTH-12. |
| [[data-bayesian-social-deduction-2025]] | Manually gated; size-category metadata is not a checked episode count. | Access-dependent game lead. |
| [[data-c2c-ai-vs-ai-2026]] | Board-matched conditions and private objectives; deals and payoff are distinct outcomes; no human games released. | MTH-13. |
| [[data-camel-ai-society-2023]] | Synthetic role dialogue, shared generator, noncommercial terms; no automatic task-truth guarantee. | Background only. |
| [[data-diplomacy-deception-2020]] | Messages nested in 12 games; sender intent and recipient belief differ; reuse terms need checking. | MTH-10 conceptual label distinction. |
| [[data-dtap-bench-2026]] | Task/config/judge assets need inspection to establish actual trace coverage; prospective execution must be sandboxed. | Future controlled benchmark lead. |
| [[data-hanabi-llm-logs-2026]] | Mixed file schemas, scaffold/model imbalance, engine assistance and judge ratings need separating. | MTH-08/09/13. |
| [[data-instrumental-choices-2026]] | Single-agent audit traces, not collective causality; unspecified licence. | Security lane lead with boundary. |
| [[data-jscmp4-moltbook-2026]] | Comment collection depends on thread activity; moderation and field semantics change over time. | MTH-14. |
| [[data-mallm-debate-2025]] | Many configurations; decision reached and agreement are not correctness labels. | MTH-02/06. |
| [[data-mast-2025]] | Large set uses judge labels; small human subset and changing taxonomy versions require mapping. | MTH-07. |
| [[data-mcphunt-2026]] | Exact canaries and diagnostic labels concern tool traces; not proof of collective infection. | Security lane lead. |
| [[data-moltbook-injection-2026]] | Keyword/heuristic positives are not verified successful injection; stated rate conflicts with given count denominator. | Security caution, not success or prevalence ground truth. |
| [[data-moltnet-2026]] | Integrates overlapping crawls; owner-handle metadata does not certify identity or common control; upstream terms matter. | MTH-14. |
| [[data-multiagent-entropy-2026]] | Released summaries omit raw stage-one traces and token tensors; underlying benchmark terms apply. | MTH-15. |
| [[data-multiagentfraudbench-2025]] | Posts-only release, synthetic scenarios, overlapping labelled subset; noncommercial/share-alike terms. | Security lane avoids assuming interaction graphs. |
| [[data-og-marl-2024]] | Viewer index rows do not count experience; archives and environment versions must be inspected. | SIM-06. |
| [[data-sandbagging-games-2025]] | Finetuned single-model audit organisms, not a swarm benchmark; unspecified licence. | Security boundary only. |
| [[data-scam-conversation-2024]] | Synthetic dialogues with limited generator provenance; not real victims or field prevalence. | Background only. |
| [[data-social-llm-networks-2026]] | Topology/text/sentiment metadata; timing, exposure order and independent replicas unverified. | PHY-25 conditional analogy. |
| [[data-sotopia-2024]] | CSV omits model/reward metadata present in JSON; bare Creative Commons tag leaves exact terms unresolved. | MTH-09/13. |
| [[data-sotopia-pi-2024]] | Generated social training data and third-party prompt inputs; check training overlap and share-alike terms. | Training-corpus lead, no held-out assumption. |
| [[data-stego-collusion-2026]] | Multiple formats repeat responses; version-specific invalidity and post-hoc labels can create shortcuts. | Security lane owns detector/mechanism questions. |
| [[data-swarmbench-2025]] | Agent/game logs have different schemas; grid task names do not establish continuous physical mechanics. | SIM-03, PHY-03/23. |
| [[data-swarmworld-2026]] | Matched discovery episodes, separate frozen-artifact assays, one shared policy; engine access separate. | MTH-01, SIM-07. |
| [[data-trail-2025]] | Gated terms restrict redistribution despite MIT metadata; mixed single/multi-agent subset. | MTH-07 only after access terms. |
| [[data-werewolf-game-reasoning-2025]] | Original and translated events/notes are paired measurements; original-player authorship unresolved. | MTH-10. |
| [[data-who-and-when-2025]] | Failed tasks only; attribution annotations are not counterfactual responsibility; licence unspecified. | MTH-07 comparison, no failure base rate. |

Supplemental simulator-merge record: [[data-moltbook-dataset-2026]] was also read. It documents retrieval completeness, an older top-level-reply omission in the derived graph, and changing schema fields. Added as a third MTH-14 anchor; MIT repository versus CC-BY dataset wording needs clarification. Its collection audits are useful evidence about observation limits, not certified bot identity or social ground truth. This brings the update’s inspected new dataset records to **33**.

## Primary-page checks in this update

Read card/README text and selected metadata or schema previews; this is not full paper reading or loaded-data inspection. The links record where factual constraints were checked. These checks do not inherit another agent’s `ran` or `full` source status.

- [MAST](https://huggingface.co/datasets/mcemri/MAST-Data): distinguished judge labels from the 19 human-annotated traces; taxonomy rounds and absent labels need explicit handling.
- [Hanabi logs](https://huggingface.co/datasets/Mahesh111000/Hanabi_data): checked the three scaffold descriptions and schema error. Engine-generated belief assistance, raw game state, prompt visibility and judge move ratings are separate channels; file membership is not randomized treatment.
- [Agent Town Economy](https://huggingface.co/datasets/sajalregmi4/agent-town-economy): checked quarantine/accounting caveats, two actual layouts behind multiple world IDs, and pulse-versus-export metric authority. Six quarantines concern tool-call failures and one is a completed low-tourism outlier under the stated exclusion rule. Runtime changes confound model-arm attribution; external accounts must be included in conservation. These are source warnings, not errors independently reproduced here.
- [OG-MARL](https://huggingface.co/datasets/InstaDeepAI/og-marl): citation card and archive listing; the displayed 74 rows are an index, not 74 trajectories.
- [Sotopia](https://huggingface.co/datasets/cmu-lti/sotopia): checked CSV versus JSON metadata retention and ambiguous licence specificity.
- [Werewolf](https://huggingface.co/datasets/ReneeYe/werewolf_game_reasoning): paired Chinese/English fields and stated translation provenance; no claim that translation fidelity was tested.
- [Entropy release](https://huggingface.co/datasets/AgenticFinLab/multiagent-entropy-rawdata): confirmed stage-one raw traces/tensors are excluded, constraining prospective routing and token-level remeasurement.
- [SwarmBench](https://huggingface.co/datasets/6cf/swarmbench): mixed agent/game schemas; preview Flocking prompt requests shape formation although prose describes cohesion/alignment. Exact task code and release matching must settle the definition. No physical transport or flocking result is inferred from its name.
- [SwarmWorld](https://huggingface.co/datasets/lamm-mit/swarmworld-data): checked manifest/trace paths, seed-level comparison units, isolated-search member availability and endpoint-wise best-of-N definition. Held-out frozen-artifact trials do not create new agent discoveries or measure adaptive deployment.
- [AgentLogs](https://huggingface.co/datasets/risenlab/agentlogs): checked table relationships, the v0.2 revision recommendation, sampling scope and missing-session information. No large event table was downloaded.
- [Supplemental Moltbook dataset](https://github.com/takschdube/moltbook-dataset): repository README opened for collection-completeness and historical graph-construction cautions; no archive loaded.
- Social-LLM-Networks page and raw README attempts returned tool errors. PHY-25 therefore relies on the existing local record and explicitly requires temporal-exposure verification.

## Simulator, talk and factory research incorporated

Read the now-merged `2-surveys/sim-environments.md` at `bf74eb0`, plus relevant records: [[gh-google-deepmind-concordia]], [[gh-sotopia-lab-sotopia]], [[zhou-2024-is]], [[gh-floriangroetschla-agentsnet]], [[radax-2010-timing]], [[ellis-2022-smacv2]], [[gh-oxwhirl-smacv2]], [[gh-mesa-mesa]], [[gh-jofmi-agentpy]], [[grimm-2020-odd]], [[gh-apromisedland-trustworthy-agent-simulation]], [[gh-ruc-gsai-yulan-swarmintell]], [[gh-google-deepmind-hanabi-learning-environment]], and [[papoudakis-2021-benchmarking]]. The survey remains in-progress. Its source inspection and teammate CPU smoke tests are useful implementation leads; they do not establish saturation, reproducibility of our proposed interventions or a cross-workload speed ranking.

Opened the primary abstracts for [Radax and Rengs](https://arxiv.org/abs/1008.0941), [SMACv2](https://arxiv.org/abs/2212.07489), and [Zhou et al.](https://arxiv.org/abs/2403.05020), and the [tass README](https://github.com/apromisedland/trustworthy-agent-simulation). Scheduler dependence, observation-blind diagnostic policies and omniscience inflation are established concerns; SIM-01–03 are concrete boundary tests of those ideas. Tass supplies a possible offline resume/export substrate, with source validation claims clearly distinct from LLM-behavior evidence. Mesa/AgentPy teammate timings used nonidentical models and are not a controlled comparison; SIM-04 explicitly matches semantics first.

Read local talk records [[blumenkamp-2020-emergence]], [[ndousse-2021-icml]], and [[zaslavsky-2023-noga]], which contain other agents’ recovered-caption reading notes. No talk was independently watched or transcript fully reread here. Zaslavsky informs RL-03’s separation of representational distortion, message complexity and task value; caption-level evidence does not support exact effect sizes or communication-safety guarantees. Blumenkamp’s fixed-cooperator/self-interested-agent setting and Ndousse’s social learning/expertise cues are relevant to the mechanism lanes; neither is evidence for LLM collusion or fork reintegration.

Read factory-scan’s `lab/researchers/dmarz/log/2026-10-03-hf-sweep.md` in its other worktree without modifying it. Its Hugging Face scan explains the 32-card addition and unresolved linked papers; Kaggle/Zenodo coverage and source data loading were not completed. The factory agent file supplied no further completed result. Earlier read-only simulator-worktree inspection was superseded by the merged main snapshot.

## Selection boundaries

Licensing, download access, split construction, loader/schema checks, label provenance and source/version correspondence are explicit prerequisites, not approval paperwork added after a chosen test. Offline means that a first discriminating analysis can avoid model calls once lawful usable data exist; it does not mean the data are already ready. MTH-13 is access-dependent because common model/scaffold support may not exist, and SIM-06 requires training and a compatible online environment.

The security lane handles attack mechanisms and containment questions. This update instead audits measurement and external validity; private reflections, owner handles, heuristic labels and posts-only corpora are not promoted into attack success or operator ground truth. All retrospective comparisons remain observational unless their source assignment is verified. No inference about real human societies, physical swarms or production reliability follows solely from a toy game or one model’s simulated episodes.
