# Telephone T0: prospective study plan

Version T0, 2026-10-04. **Exploratory design; not an executable or admitted run packet.** [Setup](SETUP.md), [background](BACKGROUND.md), [annotation specification](ANNOTATION.md). Written before Telephone-specific implementation and collection. Earlier source-prefix inspection is disclosed development exposure, not preregistered Telephone data.

## TLDR

Test whether source-linked structured retelling preserves evidence-supported claims better than prose across three fresh-agent hops. Compare with original-source retrieval and a deterministic ledger/lookup reference. First construct a verified AI Village development casebook; then, if feasible and separately admitted, use 8 qualification and 24 sealed evaluation task components with three paired arms. Measure retained supported meaning, unsupported additions and lost uncertainty. Observational case findings and controlled replay effects remain separate; neither recreates the historical Village's counterfactual future.

## Question and prediction

For bounded task evidence from AI Village, does structured claim/status/source representation improve hop-three supported retention relative to prose under the same per-call token caps? Candidate prediction: less loss of attribution and qualification, without more unsupported assertions. This is an end-to-end representation comparison: structure, instructions and source identifiers change together. It does not isolate typography alone.

A secondary question is whether re-opening original evidence is more useful than preserving ever-better summaries. Retrieval superiority favors retrieval. Accurate copied source facts and graph lineage are useful deterministic controls; a solved task does not need a model.

## Setup

**Unit:** a connected task/claim/artifact component. Use one focal claim bundle and one cutoff per component, with 3–6 predeclared critical information obligations. Include a legitimate unknown/qualified state when evidence requires it. All shared artifacts, claim ancestry and dependent tasks stay in one split, including reuse from other experiments.

**Candidate allocation:** 8 development components, 8 disjoint qualification components, 24 disjoint evaluation components. Eight development components target four coverage strata: ordinary faithful retelling, uncertainty/attribution, correction/supersession, and unavailable-source ambiguity (two each). These are mechanism coverage targets, not prevalence weights. Qualification aims for two per stratum; evaluation six per stratum. If real independent components do not support the allocation, revise prospectively before outcomes rather than relabeling variants as independent data.

Development selection includes published incidents and any task connected to previously inspected source prefixes. Later holdouts must avoid those dependencies; a new row ID is insufficient. Use a metadata-first eligible-task inventory, frozen selection seed, fixed time windows and a logged inclusion/exclusion ledger. Keep an unfiltered availability denominator before selecting stratified cases. No arm-result-based selection. Split exact model/scaffold regimes in reporting; do not infer causal model rankings from historical exposure.

**Evidence:** actor inputs contain only the declared available archive; unknown historical access excludes an episode from the historical-visibility cohort. A separately labeled constructed-information cohort may use explicitly supplied records, but is never pooled as reconstructed historical context. Tool receipts/screenshots support operational claims; chat and memory remain assertions. Later facts can audit the record separately but cannot become knowledge the actor should have had at the cutoff.

**Gold:** two annotation passes freeze critical obligations, atomic facts, support/contradiction/unknown labels, possible source sets and permissible uncertainty. Same-owner rechecking is not independent review. Preserve disagreements and unresolved cases. Gold, family labels, original identities where unnecessary, future evidence and operator context are excluded from delivered inputs.

## Protocol

Stage D is offline case preparation and baseline verification, not a paid experiment. Build the coherent task archive and code the annotation/scoring contracts before implementing model execution. The existing shared builder provides only initial components. Any scripted experimental sweep still follows applicable public-plan rules; ordinary software fixtures are labeled as such.

If D supports a useful task, freeze one provider/model, tokenizer, decoding configuration, all prompts, sampler, source and scoring hashes before S0. Proposed maximum input 4,096 tokens and output 512 tokens per call, including full serialized instructions and identifiers. Episodes that cannot fit without breaking critical evidence are excluded before assignments; no silent partial records. Context is reset every hop with no provider conversation state or operator memory. Same model for all arms and hops; serial calls, paired components, seed-controlled randomized arm order. Hosted responses need not be deterministic.

| Arm | Hop 1 | Hops 2–3 | Interpretation |
|---|---|---|---|
| P: prose | Full permitted source bundle; ordinary faithful handoff instruction | Previous hop's prose only, plus common task instruction | Reference transmission chain |
| S: source-linked structure | Same source bundle; facts/status/uncertainty/source-ID fields | Previous structured handoff only, plus the same schema/task instruction | Primary representation intervention; source IDs do not grant access to omitted text |
| R: original-source retrieval | Same source bundle and task | Previous prose plus deterministic BM25 retrieval from the original permitted archive within the common input cap | Practical access-policy control; intentionally different source access, not a pure format ablation |

R uses a task query frozen before arm outcomes, not evaluator labels or model-generated hints. Reserve a predeclared portion of the input cap for archive retrieval after measuring tokenizer costs; finalize that exact split before S0. The deterministic reference carries the frozen permitted source bundle or annotated extractive ledger without invented facts. Its reference information advantage, if it uses human annotations, is reported as an oracle ceiling, not a fair automatic competitor. Also run a non-oracle literal/reference lookup and extraction baseline using only actor-visible fields.

Each modeled chain has exactly three requests. S0 proposes 8 components × 3 arms × 3 hops = **72 requests**. S1 proposes 24 × 3 × 3 = **216 requests**. Total maximum **288 requests**, 96 chains over 32 components; no model development calls, repeats, repair allowance or automatic retry included. Token ceilings imply at most 1,179,648 input and 147,456 output tokens before provider-specific overhead; cost must be recomputed from the actual full request and current prices. These numbers are a feasibility proposal, not authority to spend.

Score outputs blind to arm where the representation permits it; disclose residual format unblinding. Annotation receives only the evidence necessary for the judgment, with gold/source review separate from condition evaluation. Do not ask a model to judge its own answers as the sole truth source.

## Metrics

Primary: for each component and arm, hop-three fraction of predeclared critical obligations retained with correct support status, time, scope, attribution and qualification. An omitted obligation scores zero; unsupported strengthening does not count as retention. Use the paired component mean of **S minus P** with equal component weights. Obligations are fixed before outputs, so verbose answers cannot inflate the denominator.

Safety counterpart: unsupported added assertions per output and per component, plus any unsupported critical action/commitment. A retention improvement with more unsupported critical commitments fails the adoption screen. Report factual precision, critical completeness and uncertainty preservation separately; abstaining on everything does not pass completeness.

Secondary: hop-one-to-hop-three change, first observed mutation location, mutation type, source-citation validity, correction survival, unnecessary abstention, tokens, latency and total cost. Observational trace edge precision/coverage is separate from replay fidelity. Semantic similarity is descriptive only; it cannot certify meaning preservation or ancestry.

For S1 show all 24 paired component differences, a paired component bootstrap interval with fixed seed and disclosed limitations, and descriptive stratum tables. With 24 independent components, a single rate near .5 has roughly ±20 percentage-point 95% uncertainty. For a difference bounded in [-1,1], worst-case standard-error bound is about .204, so this pilot cannot establish modest improvements. No claim of rare-error safety from zero events. Multiple secondary endpoints are exploratory, not separately significant discoveries.

## Qualification, stopping and decisions

Before S0: all privacy/visibility/label controls and parser baselines pass; source hashes and full-context reset checks verified; actor payload invariant to evaluator-only metadata. Deliberately wrong policies must fail. Unknown/missing outcomes must remain distinguishable from correct abstention.

Proposed S0 gate, finalized before dispatch: 72 valid outputs and fully reconciled assignments; each arm retains at least 85% of its critical obligations at hop 1; no unsupported critical commitment in the ordinary controls; all known-unknown controls preserve uncertainty at hop 1. Examine every miss and all three-hop traces. This tests competence and instrument usability, not the treatment effect. A baseline ceiling stops a model-necessity claim. S0 failure stops; no automatic prompt repair or threshold reduction.

Only separately admitted S1 uses the frozen qualified instrument. A provisional descriptive adoption screen is S−P retention ≥0.10 with no increase in unsupported critical commitments; report uncertainty regardless. R matching/exceeding S favors source retrieval. Null/adverse results argue against added structure; insufficient precision is inconclusive, not support.

Stop on the first transport failure, source/rights boundary violation, cap violation or invalid output; preserve raw sanitized response and reservations, mark dependent later hops unavailable, and leave remaining assignments unstarted. No historical future substitutions or silent replacements. Report assigned/started/terminal/valid/scored/analyzed separately. Primary completed-pair estimates get all-assigned best/worst bounds; unobserved treatment differences are not zero.

## Resources, registration and closeout

This request authorizes design and offline preparation, not native collection. No machine is needed now. A future owner-directed launch without another explicit budget uses the standing cumulative USD2 authority, but the 288-call proposal must first demonstrably fit that cap including infrastructure and uncertainty reserves or be redesigned before approval. Do not request a redundant default-budget approval, invent an additional allowance, or borrow another study's ledger. No model/provider has been chosen and no affordable envelope is claimed.

Before native collection: concrete owner scope decision, provider-transfer terms, exact cost reservations, dedicated approved-account allocation, runtime/source checks, immutable public plan registration and actual page verification. No researcher sign-off is required. Development, qualification and evaluation each retain their evidence and limitations. A published draft is not preregistered execution.

Private visualization: per-component timeline of source → hop1 → hop2 → hop3, field-preservation matrix, and links to retained evidence. Public fallback: aggregate retention/unsupported-claim trajectories with missing hops explicit; no licensed excerpts. Renderer remains to be built and tested against fixture failures. Every attempted stage receives operational and scientific post-mortem, cost reconciliation and resource release. A valid negative result may finish Telephone.
