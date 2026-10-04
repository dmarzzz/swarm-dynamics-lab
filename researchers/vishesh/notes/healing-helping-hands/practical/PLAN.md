# Healing Helping Hands: practical repair comparison

## TLDR

Can 200 local evidence curators keep a shared knowledge base current when sources retract findings, new evidence arrives, source lineage is unreliable, or the central index is temporarily unreachable? Compare the same recorded semantic outputs with ordinary central indexes and local sharing. This is a **scripted architecture diagnostic using saved Jev outputs**, not a fresh model evaluation, a new real-paper corpus, or evidence that Qwen/Laya now qualify.

## Question and prediction

Parent: [pilot-03 post-mortem](../reviews/pilot-03-post.md). New feedback: [PI next experiments, Conditional B](../../../../dmarz/notes/next-experiments-2026-10-04/README.md) (repository path: researchers/dmarz/notes/next-experiments-2026-10-04/README.md). That review requests central append-only controls, matched extraction and source budgets, benign learning, incomplete/misleading lineage, integrated incorrect-or-missing claims and update-retention guardrails. The old pilot's perfect semantic reference and programmed propagation are acknowledged, not relabeled as autonomy. The present design adds an even stronger central version-aware comparator.

Practical interpretation: choose a synchronization policy for an evidence index. We do not claim new research novelty, human-verified scientific truth, a fresh semantic generalization result, or a cost advantage from 200 agents. This S0 engineering diagnostic does not bypass the lab's independent research-review gates.

## Protocol

Attempt `practical-01`, parent `pilot-03`. Inputs are the three saved corpora and Jev extraction tapes for seeds 8701–8703; record file SHA-256 and parent source 46678b2b99936383d01b268075e0ae2cf8b405fc. No new inference or model credentials. Held-out seeds 8301–8310 remain unopened. For each corpus use two prespecified placement seeds, corpus seed + 10000 and + 20000. Shuffle the same 200 document-to-curator assignments once per layout and reuse them in every arm/scenario.

Each curator has a stable ID on a 20×10 four-neighbor grid, one assigned source document, and a query claim `id % 20`. There are 100 independent source roots, two copies each, and 20 claims. Copies are deduplicated by root before aggregation. Contradictory extraction labels for one root yield UNCERTAIN. Claim consensus is SUPPORT if more valid roots support than refute, REFUTE for the reverse, otherwise UNCERTAIN. UNCERTAIN can mean a legitimate tie; separately record missing evidence and abstention.

Withhold root R4 of each claim initially; release its two existing recorded documents at round 10. This is benign new learning from previously recorded outputs, not newly inferred evidence. Initially curators receive their document only if it belongs to R0–R3. Every arm gets exactly the same documents, notice payloads and entry nodes. Event recipients are original source curators; central systems must ingest their messages, not receive evaluator truth directly. Root identity and publisher `publisher-{claim}` are actor-visible. Truth uses the original fixture labels and actual withdrawals; actors use only saved tape labels and received records.

Five arms:

1. `central-append`: shared central index, no withdrawal handling, per-curator last successful query cache.
2. `central-verified`: same index/cache, accepts a withdrawal only if its supplied authenticated issuer matches the target record publisher and the target root exists. Missing lineage cannot trigger deletion. A pending valid notice is retained until its target arrives.
3. `peer-append`: local document propagation, no deletion.
4. `peer-blind`: local propagation, accepts any supplied concrete target root, ignoring issuer validation.
5. `peer-verified`: local propagation with the identical public-metadata verification rule used by central-verified.

The authentication flag is supplied incident metadata, not a learned detector or a cryptographic implementation. Unknown or mismatching lineage must be rejected/unresolved, not mapped using gold. All arms retain source records and apply tombstones at query time. Erasure is not repeated in this attempt: pilot-03 already tested it; the new failure is stale or wrongly invalidated evidence.

Six scenarios, with benign R4 release in every scenario:

- `benign`: no withdrawal; tests useful learning and harmful deletion.
- `withdrawal`: one seeded R0–R3 root per claim genuinely withdrawn at round 10; correct notices.
- `forged`: no true withdrawal; notices target the same selected roots but carry a mismatching authenticated issuer. Tests restraint.
- `missing-lineage`: true withdrawals but notices omit the target root. Tests the boundary of metadata-based repair; residual stale answers are an expected valid adverse outcome.
- `central-outage`: true withdrawals with correct notices; curators in columns 10–19 cannot reach the central index during rounds 10–19, while the local mesh stays connected.
- `combined`: true withdrawals plus forged notices against a different valid root, and the same central outage. Genuine and forged incident types are supplied; no hidden detector is added.

At round 10 release new documents and inject notices before communication. At round 20 restore central connectivity; retain queued uploads. Record pre-communication event snapshots at 10 and 20. Run 30 synchronous rounds (0–29), with ingress then communication then scoring. Central systems can upload all pending own observations and read their query claim in one logical round when reachable; this deliberately strong low-latency baseline is not latency-matched to mesh hops. Every peer directed edge sends at most four previously unseen records per round, notices before documents, stable ID order, synchronous delivery. Track actual transmitted item copies; central upload plus query-response item copies count as traffic, peer transmissions likewise. Do not claim equal traffic or actual network bandwidth: report the tradeoff. Both architectures receive the same exogenous evidence/update budget; total model calls are zero.

## Metrics

180 assignments = 3 known corpus tapes × 2 layouts × 6 scenarios × 5 arms. Corpus is the semantic cluster; layouts are sensitivity repeats, not six independent semantic replications. Agents, claims and rounds are dependent observations. Report per-corpus means over its layouts, then mean/range over three corpora; no confidence interval or significance claim.

Primary endpoint: mean fraction of curator queries incorrect **or missing all usable source records** over rounds 10–29 (200 queries/round). Primary contrast: central-append error minus peer-verified error, separately by scenario. A legitimate correct UNCERTAIN answer with evidence is not counted as missing. Also report the stronger central-verified contrast, peer-blind versus peer-verified, and all arm absolute outcomes. Never pool scenarios into one success score.

Secondary/guardrails: atlas accuracy (majority of ten curators per claim), stale-citation fraction and count, false invalidations of active source roots, valid-source coverage, learned-R4 retention among curators querying its claim, abstention, traffic item copies, and first post-event round beginning three consecutive rounds with >=95% correct nonmissing curator queries. If threshold never reached, report null, not zero. Scoring uses evaluator truth only after actor state has advanced. Correct-but-missing answers must not inflate success.

Useful-effect rule adopted as a descriptive diagnostic: >=20% relative primary error reduction versus central-append **and** at most 3 percentage points lower final R4 retention. Always state absolute difference; relative improvement is undefined when baseline error is zero. This rule is not a scientific promotion gate. A strong central baseline winning is useful evidence. Failure under missing lineage is a scope boundary, not justification to fabricate target identities. Report effect on gold and source availability so ineffective events cannot masquerade as robustness.

## Setup

Standard-library Python, one bounded worker on freshly allocated sim-vishesh (claim vishesh-healing-practical-01, fleet PR 76). Source and input hashes are frozen and checked. No model is initialized. See the pre-run assessment for test results and exact command.

## Acceptance and repair

Before launch: tests establish missing-evidence scoring, deduplication, conflict/tie handling, proper issuer validation, pending notices, synchronous per-edge budget, central cache/outage/recovery, source/actor truth separation, and terminal denominator accounting. Input tapes must match all 600 archived labels and original qualification provenance; that is a reuse check, not a new competence screen. Freeze code and input hashes, register this immutable plan and condition-specific TLDR, verify public registration, and obtain a fresh exclusive fleet allocation.

A completed diagnostic requires all 180 assignments terminal or explicitly not-run, every saved metric reproducible, actual outage/withdrawal/forgery/update injections recorded, zero hidden retries, and plots reconciled against raw history. Null/adverse findings remain results. Execution defects get a new attempt ID with a prospective amendment; do not overwrite practical-01 or change endpoints after seeing outcomes. Wall limit 15 minutes, one CPU worker, zero model calls, $0 incremental inference, no external datasets. Keep the existing Jev $0.10 budget ledger unchanged. Resume reporting without rerunning computation.

## Visualization mapping H3

All run IDs bind attempt/seed/layout/arm/scenario. Record each logical round, 200 curator outcomes/memory counts/stale counts, central connectivity, claim atlas, traffic, and exact state hashes. Five side-by-side or selectable 20×10 grids use green=correct nonmissing, red=incorrect, gray=missing; black outline marks disconnected central clients. Use redundant labels/legend, fixed axes and mobile layout. Curves show incorrect-or-missing queries, stale citations and new-evidence retention with event markers at 10 and 20. No animation interpolates unobserved states. Evaluator colors/gold stay outside actor payloads.

Default replay: first corpus 8701, first layout 18701, combined scenario, all arms; selected now, not after outcome inspection. Retain every round and pre-event snapshot. Live hub progress reports terminal assignment counts; final measured GIF and PNG are public-supported fallbacks. Full local interactive replay has scenario/seed/layout selectors, play/pause and a labeled time cursor. Public hub does not promise arbitrary HTML hosting. Render initial/event/final frames plus results table. Check numerical values against saved data, visible outage start/end, playback, keyboard/mobile behavior and honest missing/failed states. Rendering is offline, no model calls; unavailable visuals are a publication defect to repair, not a reason to rerun inference.

## Remaining unresolved work

Qwen and Laya remain unsuitable under prior gates. This iteration repairs baseline, lineage, utility and failure-scenario gaps; it does not repair their semantic capability. A future composite-agent diagnostic needs a distinct plan and fresh qualification; previous failed tasks cannot become held-out evidence. Real-paper curation needs human annotations, independently authored tasks and external review before efficacy claims. No claim that the entire research program is failure-proof is warranted.

## Prospective amendment: practical-02 capacity sensitivity

Written after practical-01 and its [post-mortem](POST-01.md), before practical-02 execution. Practical-01 remains an adverse result: no scenario met the utility rule, and peer delivery lost substantial new evidence under the four-item cap. The active next attempt is `practical-02`, parent practical-01, still exploratory S0 with the same saved pilot-03 semantic inputs.

Change **only the peer per-directed-edge packet cap from 4 to 16**. Run all 180 assignments again under the same seeds, layouts, arms, events, 30 rounds and scoring. Central controls must be byte-identical to practical-01 in all scientific output fields. This is an explicitly post-outcome engineering sensitivity check, not an independent replication or confirmation. Keep both capacity settings in the final table. Report per-corpus paired cap differences, final learning retention and traffic. All previous metrics/utility thresholds remain unchanged; no further cap will be selected based on performance in this cycle.

Prediction: increasing capacity improves delivery but increases traffic, while source verification still cannot identify targetless notices. Plausible negative outcome: high capacity still fails to beat central append or loses on the retention guardrail. Strong central-verified controls remain mandatory. The purpose is to bound the prior conclusion to its transport regime, not find a favorable swarm result.

Zero model calls and inference spend, one CPU worker, 900 seconds, same still-exclusive experiment allocation through subsequent diagnostic stages. Fresh public plan/source check and an acknowledged hub start are required. `reporting.launch` is the tracked repaired entry point. Preserve practical-01 results unchanged. Visualization mapping H3 applies, with a visible packet-cap label and distinct attempt ID; first corpus/layout/combined remains the default. No-new-model claim and all remaining scope limits persist.
