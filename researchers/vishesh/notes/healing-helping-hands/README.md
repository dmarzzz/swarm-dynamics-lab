# Healing Helping Hands: a living evidence atlas

**Prospective exploratory v2 plan.** This document is published before the new implementation is executed. The prior [routing pilot](../regrowth-200/README.md) remains a separate experiment (`regrowth-200`), including its missing-registration failure. V2 uses experiment ID `healing-helping-hands`. No new result is claimed by this plan.

## TLDR

Can 200 document scouts keep an evidence atlas correct when research reports are withdrawn or agents lose memory? Each scout reads one short fictional report; neighbors exchange evidence. Compare sharing evidence alone with sharing evidence plus withdrawal notices, and with no sharing. Separately compare Qwen alone, Qwen with an independent Qwen check on 20 scouts, Qwen with an independent Laya check on those scouts, and exact extraction. Measure evidence-supported answers, stale citations, missing evidence, correction speed and compute. Three pilot corpus seeds support a small descriptive comparison, not a claim about real scientific research.

## Question and prediction

Primary mechanism question: does propagating source-withdrawal notices reduce post-withdrawal answer error and stale citations compared with keeping the same notices local, with all evidence and initial recipients held fixed? Expected benefit is conditional on information reaching affected scouts. No-sharing tests whether communication is useful; no-event and erasure-only cases test for costs and mechanism specificity.

Secondary model question: does an independent Laya attachment improve extraction and downstream atlas correctness relative to a same-Qwen attachment on the same 20 positions? Both attachments get the report and claim but do not see the first Qwen answer. Disagreement becomes UNCERTAIN, symmetrically in both attachment arms. The two attachment arms have equal call slots, not necessarily equal token/FLOP cost. Every model arm is compared with exact fixture extraction to separate semantic errors from propagation errors.

## Setup

A synthetic research corpus contains 20 atomic claims about whether a named intervention improves a named benchmark outcome. Five independent source roots per claim each have two report copies: 100 roots, 200 documents, 200 scout identities. Documents are explicitly fictional and make no real scientific claims. Evidence labels are SUPPORT, REFUTE or UNCERTAIN. A report about a different outcome supplies no evidence for the queried claim.

Scouts occupy a 20 × 10 grid with four-neighbor connections and separate memories; agent i initially receives document i and curates claim i modulo 20. Each claim has ten curators. Source identifiers and authenticated withdrawal notices are environment metadata, not discoveries by the model. Signed metadata is assumed trustworthy; forged notices and autonomous credibility detection are outside this pilot. At each synchronous round, scouts exchange their prior-round records; evidence duplicates are keyed by document and aggregation counts each source root once. Each scout only sees its own memory. The evaluator alone has the full fixture and current valid-source set.

Qwen3 0.6B performs one local semantic extraction per scout. Twenty seeded, stratified scout positions optionally receive an independent second model extraction. After extraction, propagation, tombstones, deduplication and aggregation are deterministic mechanisms. This tests a model-backed evidence system, not 200 autonomous researchers making new language decisions each round. The 200-node animation must make that boundary explicit.

## Protocol

Before coding changes, publish this plan. Before any qualification or world execution, commit source, register the immutable README and verify that the running tracked files match that commit. Qualification: 30 balanced document/claim pairs (10 per label), with dedicated seed 8000. Each model must score at least 85% overall, at least 70% within each label and zero schema/provider errors. A failed head is reported as failed qualification; do not silently replace it, lower the gate or retune against pilot outcomes. Engineering scenarios may still execute with explicitly exact extraction. Failed qualification is a useful outcome, never a successful intervention result.

Pilot seeds 8101, 8102 and 8103 are disjoint from qualification; held-out 8301–8310 remain unexecuted. Four extraction definitions (exact, Qwen, Qwen+Qwen, Qwen+Laya), three communication policies (none, evidence-only, evidence+withdrawals), four event scenarios (none, withdrawal, erasure, combined) give 144 planned worlds. Extraction tapes are shared across all policy/scenario comparisons for a seed. Qwen-only and both composite arms share the first extraction; additional heads act only on the same 20 seeded identities. These are paired computational counterfactuals, not independent model replications.

All worlds run 24 rounds. At round 10, withdrawal scenarios invalidate one seeded source root per claim, delivered initially to the original scout for that root. Erasure removes memory and locally known notices from 40 seeded scouts; information remains elsewhere. Combined applies erasure then delivers notices. Recipients and erased identities are identical across extraction/policy arms. No event gives the matched trajectory. Evidence-only retains locally received withdrawal tombstones but does not forward them. Evidence+withdrawals forwards both records and tombstones. None retains only local information/notices. Tombstones take precedence over stale records and are idempotent.

No model call retries. Reserve each attempted call before dispatch, use bounded timeouts, cap at 2,000 Qwen calls and 300 Laya calls including qualification, and a 30-minute whole-attempt deadline. A provider/schema failure during extraction aborts that seed's model tape and marks dependent worlds not-run; exact worlds remain separately eligible. Every assignment has a durable terminal record. Record failed attempts, not just successful responses. Sequential inference is chosen for a simple verifiable budget at this scale; shared weights do not imply concurrent model execution.

## Metrics

Gold is the source-balanced consensus of the surviving reports using their fixture labels: more SUPPORT roots yields SUPPORT, more REFUTE yields REFUTE, ties or no informative roots yield UNCERTAIN. This is recoverable evidence consensus, not an assertion of scientific truth. A scout's answer uses its local extracted labels and known withdrawals. Conflicting labels within a root become UNCERTAIN. Atlas answer is the majority of the ten curators for that claim; tied votes become UNCERTAIN. Report local-scout accuracy separately from 20-claim atlas accuracy.

Primary outcome: mean atlas error across rounds 10–23 (integrated post-event error), compared as evidence+withdrawals minus evidence-only in withdrawal/combined worlds. Report each seed, their paired mean and range; three corpus seeds are too few for persuasive confidence intervals. Secondary: source coverage (unique valid informative roots available locally / possible), stale-citation fraction among cited informative roots, abstention, false confident assertions, final atlas accuracy, rounds until at least 95% atlas accuracy sustained for three rounds, initial event impact, extraction confusion matrices, attachment disagreements, calls/tokens/time and failed assignments. Recovery can be null and is not substituted with zero. Include no-event trajectories; do not rank recovery times without checking pre-event competence and initial impact.

## Robustness and reliability acceptance

Test source deduplication, no cross-claim leakage, synchronous snapshots, deterministic tape replay, withdrawal idempotence and propagation, erasure recoverability, independent head blindness, exact source matching and append-only journals. Inject timeout, malformed JSON and budget exhaustion into fake adapters: failed calls count, errors retain type-only diagnostics, and all dependent assignments terminate honestly. Test null recovery and first post-event indexing. Completion is not model competence or experimental success.

Seven routing-environment tests are preserved; they are not evidence that v2 is correct. New invariants and negative controls are required. Models must pass semantic qualification before their tapes support interpretation. No guarantee that Laya helps, nor that any model succeeds. Source-order and option-order permutations in qualification guard against fixed-direction/first-option behavior observed in v1.

## Visualization plan

Replay only recorded frames: 200 scout cells show current local claim state/accuracy, a 20-claim atlas shows consensus and evidence support, and a source panel exposes roots, copies, withdrawals and head disagreements. Display the event boundary and erased scouts, paired policy views, time curves for accuracy/coverage/stale citations, and a seed/arm/scenario selector. Scrubbing and source inspection must work on mobile and keyboard. Missing/failed worlds are visibly not-run; never substitute generated animation for missing results. Export a measured outcome figure and an animated replay of a representative recorded pair. Choose that pair by a fixed rule (first seed, combined scenario), not by best result.

## Research basis and limits

The [FEVER task](https://fever.ai/dataset/fever.html) separates supported, refuted and insufficient-evidence claims; this motivates the three-way extraction task, but we do not run FEVER or claim comparable performance. [ALCE](https://arxiv.org/abs/2305.14627) motivates measuring citation support separately from answer quality. [FActScore](https://arxiv.org/abs/2305.14251) motivates atomic claim-level checks. Sources inspected at abstract/task-description depth on 2026-10-04; this focused design check is not an exhaustive prior-art survey. No accepted hypothesis or confirmatory S2 stage is claimed.

The corpus is synthetic and small, labels are engineered, and propagation/aggregation are programmed. A next-stage real-paper curation study requires a frozen corpus, human evidence annotations, extraction validation and a separately registered plan. This pilot should teach which failure comes from language understanding, which comes from obsolete evidence, and what extra independent model checks cost.

## Repair 01: typed outcome interface, declared before attempt 02

Attempt 01 preserved: Qwen scored 25/30 overall (83.3%) and 5/10 on REFUTE, below the unchanged 85% overall / 70% per-label gate. Laya scored 27/30 (90%) and passed. Consequently 36 exact-extraction worlds ran and 108 model worlds were not-run; no model pilot success is claimed. This is a semantic-interface failure, not an infrastructure outage.

Attempt 02 changes Qwen's response interface to the concrete report outcome IMPROVED, NOT_IMPROVED or NOT_MEASURED, with two negation/unknown examples. A fixed mapping turns those into SUPPORT, REFUTE or UNCERTAIN because all claims explicitly assert improvement. This is a narrow typed extraction interface, not a general-purpose fact verifier. Laya continues to classify independently from the raw claim/report; neither head sees the other answer. No scripted gold-label correction or silent fallback is allowed.

Fresh qualification uses 60 balanced cases (20 per class), procedure names 131–150 and seed 8001, with explicit no-gain and unevaluated-outcome paraphrases. Gate remains 85% overall and 70% per class. Pilot corpus seeds change to 8201–8203; 8101–8103 and the first qualification remain development evidence. Held-out 8301–8310 remain unexecuted. Prompt, response schema, label mapping and exact qualification fixtures are committed before attempt 02. All other treatments, measures and 30-minute/2,000-Qwen/300-Laya call limits remain unchanged. This is an architecture revision, not a retry of the failed outcomes.
