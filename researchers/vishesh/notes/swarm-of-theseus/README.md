# Swarm of Theseus — SOC-24

Status: prospective exploratory S0/S1 instrument, not an accepted hypothesis or confirmatory study. Owner: vishesh/codex-theseus. Plan written 2026-10-04 UTC before implementation or execution. Candidate SOC-24 remains an unreviewed hunch; formal survey/hypothesis gates remain closed.

## TLDR

Can useful practices survive after every founding member of a swarm is replaced? We compare inherited written notes, direct mentoring, both channels, and neither, against unchanged founders and a verbatim procedure control. Three fictional worlds test sorting at a seed bank, source checking at an observatory, and adaptation to a changed repair procedure. Success means correct work on previously unseen cases after complete turnover, measured separately from preserving an arbitrary team convention. This is a small, single-model exploratory study of seeded procedures and bounded text memory, not evidence of spontaneous human-like culture or consciousness.

## Question and prediction

SOC-24 asks what survives complete population turnover through artifacts, interaction, or model priors. Prediction: notes plus mentoring will preserve more useful procedure than neither; a surviving name alone may not predict useful work. After an environmental change, persistence of an old procedure may become harmful. A null or reversed contrast is a valid finding, not a reason to change the seeds.

We operationalize culture as transmitted task procedure plus an arbitrary convention. Founders receive a seeded procedure; this does not test spontaneous emergence. Fresh instances share the same model weights but have new IDs and no private context from departed agents. We test context replacement, not model-weight replacement.

## Setup

Three scenarios, each with counterbalanced world-specific mappings absent from the common system prompt:

1. **Seed bank.** A seed lot has two binary assay markers. Their XOR selects one of two storage bins, whose arbitrary names and mapping are randomized. A distinct two-word receipt convention measures nonfunctional persistence.
2. **Observatory.** Five reports about a beacon may duplicate an underlying source. Count each source once, then take the majority of distinct roots, mapping the result to world-specific beacon labels. Duplicate-majority cases distinguish useful source checking from ordinary vote counting.
3. **Repair dock.** A two-bit diagnostic selects a repair bay via XOR and a randomized mapping. After the last founder leaves, an explicit bulletin swaps the mapping; copying the old procedure can now hurt. Convention remains unchanged. Score pre-change retention and post-change adaptation separately.

Population: three founding identities, replaced one at a time at steps 1, 2, 3; steps 4 and 5 contain only descendants. At each replacement, the departing member may answer the newcomer's onboarding question before leaving. Newcomer context begins empty except for the arm-authorized channel(s). Each member maintains only its own bounded notebook. Each step all three independently solve four new cases; deterministic per-case majority is the collective answer. Ties (including three different strings) and missing decisions are incorrect. Team notebook is the concatenation of the three bounded member notes from the prior step, never a hidden oracle summary. Retain complete input/output records.

## Protocol

Arms: `neither`, `notes`, `mentor`, `both`, `founders`, `verbatim`. Pair arms on world, scenario, convention, case schedule and replacement order; randomize arm execution order within world. `founders` preserves original IDs and private notebooks. `verbatim` gives every actor the current exact procedure each step (plus the same repair bulletin); it is an information-rich competence ceiling. The other four arms all replace every founder. `notes` reads the prior team archive only at arrival; `mentor` receives a question/answer exchange with the departing member but no archive; `both` receives both. In `neither`, the exchange is computed but masked, as are notes. Incumbents keep only their own notebook in every arm. Channel bytes, actual tokens and calls are measured.

Each step uses the same three solve calls in all arms. At replacement steps all arms use one newcomer question call and one departing-member answer call, even when the answer is masked. Thus call/output ceilings match; actual input tokens and inherited information need not match, and are explicitly reported. Each solve response includes four case-ID keyed work items (evidence, intermediate result, label), the receipt convention, and a notebook capped at 600 characters. Each dialogue message is capped at 300 characters. In both-channel arms the total onboarding payload is capped at 2,100 characters; the single-channel ceiling is the same but the natural payload may be shorter. Do not claim token-exact matching.

Freeze cases before any onboarding generation. Development fixtures, S0 qualification worlds, S1 exploratory worlds and unopened S2 holdout use disjoint seed ranges. S0: two worlds per scenario (seeds 104,105), only `founders` and `verbatim`, full timeline, with complete turnover required in verbatim. S1: two worlds per scenario (seeds 200,201), all six arms. S2 remains disabled regardless of pilot quality. Total maximum: S0 288 calls; S1 864 calls (24 per world-arm). A repair attempt must have a new plan/review, new seed range and new output directory. At most two bounded repair qualifications; no automatic scientific reruns. Stage budgets can be narrowed prospectively if shared funds are unavailable.

Model selection, deployment resource ceiling and qualification thresholds are frozen in the pre-run review before inference. API spend requires a non-overlapping reservation from the existing shared budget authority, never a duplicated ledger. Dedicated fleet allocation is mandatory. Run only after public immutable plan registration, verified public page, committed assessment, source/config hashes, exclusive claim and tests. Register a condition-specific TLDR for every hub run. Public summaries distinguish process compliance from execution and scientific validity.

No semantic retries. Transport failures become explicit failed world-arm outcomes with remaining scheduled actions marked missing. Record all assigned outcomes, including failure. Treat failed final outcomes as zero in the conservative primary summary and also report complete-case results and missingness. A model timeout does not make an observation disappear. Stop on budget exhaustion, expired claim, or a systemic runtime defect.

## Metrics

Primary exploratory contrast: `both − neither` in collective held-out accuracy at steps 4–5, averaged within world and then equally across the three scenarios. Repair dock uses current post-bulletin truth. Report absolute points and paired world-level bootstrap intervals (resample worlds within each scenario; 2,000 draws). Only two worlds per scenario: intervals describe these synthetic generators, not diverse real deployments. No confirmatory p-values or discovery claim.

Secondary: per-scenario and per-step accuracy; convention exact-match fraction independent of correctness; turnover fraction and original-member count; pre/post procedure change; action-level disagreement with seeded/current executable rule (behavioral mutation, not semantic text similarity); invalid responses; missingness; actual input/output tokens and calls; onboarding bytes. Report channel access receipts and lineage hashes. Do not count members, turns or individual cases as independent worlds.

Qualification gate: zero missing/invalid records, correct roster replacement, no hidden truth in actor payloads, and at least 0.85 collective accuracy in each scenario's verbatim control across post-turnover cases; convention retention at least 0.8 in that control. Failure blocks S1; diagnose with new disjoint tasks and preserve the failed attempt. Offline exact-policy controls must obtain 1.0 and deliberately wrong/duplicate-count policies must be discriminated. The no-inheritance arm need not perform at chance: incidental priors and task inference are outcomes.

## Visualization mapping

Mapping v1 binds run ID, scenario, arm, seed and source hash to each recorded step. A roster strip shows original IDs leaving (turnover 0–100%); separate time-series show objective accuracy and arbitrary-convention retention (0–100%). Mark each replacement and the repair bulletin explicitly. Grey gaps indicate missing data, never zero-height successful measurements. Live progress and latest frame derive from scored records; `history.json` retains every frame and lineage edge. Publish a final PNG and a standalone replay with play/pause/step and arm/world filters. The generic spatial hub renderer is not a valid culture chart; use a supported image/contact-sheet fallback and link the custom replay. Audit plotted numbers against events and test failure/initial/final states before launch.

## Closest evidence and limits

SOC-24 follows [[perez-2024-cultural]] (https://arxiv.org/abs/2403.08882) and [[ashery-2024-emergent]] (https://arxiv.org/abs/2410.08948). Abstracts opened 2026-10-04; no new full-paper-read claim. The former provides a transmission framework; the latter studies naming conventions. Our proposed extension separates seeded procedural usefulness from a nonfunctional convention under replacement and a changed environment. This is not a completed novelty survey. Three deliberately simple synthetic scenarios, one model, small populations and scaffolded communication limit external validity. Intermediate generations are dependent; inherited procedure is intended information, while future test cases and labels must never enter onboarding. Adaptation bulletin is authorized new task information, not evaluator leakage.

## Prospective scope amendment — 2026-10-04 UTC

Before any implementation run, cap S1 at two worlds per scenario to fit the remaining shared API allowance. Reduce private notes to 600 characters and dialogue messages to 300 characters. Reserve at most USD 12 from the existing shared ledger; no new cap or infrastructure spending. Treat the six-world pilot as feasibility evidence with very weak precision. Maximum 1,152 model calls for S0 plus S1, subject to the hard dollar ceiling; future repair requires remaining quota.

The unseen cases have new IDs/lots; the small binary feature space recurs. This tests procedure transfer to new records, not compositional generalization. The repair bulletin is supplied at both post-change steps to every arm; it tests following an update in the presence of inherited text, not discovering the new rule unaided.

## Setup amendment — 2026-10-04 UTC

S0-a1 stopped before model initialization because a public preflight request returned an HTTP error; no assignments started and no API quota was consumed. Subsequent status-only diagnostics returned 200 for both public URLs. S0-a2 uses fresh seeds 102/103 and caches successful public reads only within a single launch process; validation remains fail-closed. S1 remains blocked pending successful qualification.

## Qualification repair v2 — 2026-10-04 UTC

S0-a2 failed qualification; its outcomes remain archived. The original answer-first contract did not define the convention field precisely or tell the model the memory bound, and traces show correct calculations written after inconsistent answer labels. V2 asks for per-case evidence and intermediate result before its label, identifies cases explicitly, defines convention as only the receipt phrase, and requests concise general notebooks without worked examples. The supplied reference procedure and current bulletin take precedence over stale private notes. This scaffolding is identical across arms; it changes the instrument and limits results to that instrument. No deterministic solver is inserted into the actor. Increase output ceiling from 768 to 1,024 tokens; the dollar ceiling stays USD 12. Shared call reservation expands from 1,152 to 1,728 within the shared 6,500-call authority, allowing bounded repair without a new spending allowance. Fresh S0-a3 seeds 104/105 must pass the original thresholds; S1 remains unopened. Preserve returned error reasons from the sanitized adapter in subsequent failures.
