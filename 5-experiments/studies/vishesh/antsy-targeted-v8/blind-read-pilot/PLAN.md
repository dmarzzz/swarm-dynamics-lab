# Antsy: does showing the proposed total make a checker less useful?

Prospective offline design, 2026-10-04. **Not funded, corpus not frozen, no native launch authorized by this document.** Preserve [Q2's negative](../literal-v2r/POST-MORTEM.md). The decision is whether to pursue independent reading rather than adding proposal-conditioned checking to a payment-total extraction workflow. No actual payments are executed.

## Paired contrast

For each receipt, collect six fresh calls from the same pinned Haiku route and configuration: two direct normalized-total readers D1/D2, two literal-token readers A/B, an image checker C shown A's token, and one separate checker control K shown a precomputed wrong token. B never sees A, C, D1/D2 or evaluation labels. A and B have identical role instructions; distinct IDs are not diversity treatments. C sees the identical image plus A's token and must return its own exact source token/label before its boolean. Randomize the serial order of D1/D2/A/B with a frozen seed; C follows A. K uses a separate context. Never initialize workers from the operator's conversation.

Derive four policies from the retained calls:

| Policy | Calls per service | Accept rule |
|---|---:|---|
| Direct agreement | 2 | D1 and D2 return identical valid canonical totals |
| Literal + code | 1 | A returns a supported token and locale-bound parser succeeds |
| Blind second read | 2 | A and B independently quote the same complete numeric token and both parse identically |
| Proposal-conditioned check | 2 | C approves A, independently returns exactly A's complete token, and parser succeeds |

All other semantic outcomes refer. Structural/transport failures remain missing execution outcomes, not referral. Never normalize malformed direct answers into correct baseline decisions. Freeze token equality as exact digit/separator equality after stripping only outer whitespace; do not repair digits, fuzzy-match quotes or use gold. Parse rules and locale information are identical across policies. Report strict-format disagreements and normalized agreement separately, without changing acceptance afterward.

The blind versus conditioned contrast changes task and information access; it tests two deployable verification packages, not an isolated causal effect of anchoring alone. Shared A allows a paired comparison but creates dependent policies. Same model, same pixels, separate requests establish context separation only. They do not establish independent errors, distinct architecture, complementary evidence or population diversity. No architecture/model/agent-count sweep is included.

## Case intake and label firewall

Target 12 scorable real receipt units: 3 in each of two source-locale by two source-quality cells. Add 2 genuinely unresolved-total cases as a separate referral challenge, one from each source locale, for 14 units total. Quality categories are clear versus degraded-but-adjudicable, judged on delivered pixels before model calls. Degraded means faint, blurred, damaged or occluded target digits that remain resolvable by the adjudication protocol; do not manufacture image damage to populate a cell. Locale is determined from source provenance, not punctuation. Record separator convention within each locale. Currency/locale is supplied consistently as external metadata; this does not test inferring locale.

Candidate sources: [CORD maintainer documentation](https://github.com/clovaai/cord) describes Indonesian receipts; [SROIE competition paper](https://arxiv.org/abs/2103.10213) documents a separate receipt OCR/information-extraction corpus. Pin the second source's authoritative release, license and locale provenance before using it. Dataset/source differences confound locale comparisons: strata are coverage checks, not estimates of locale effects. If second-source access/provenance fails, stop preparation with a documented gap; do not relabel comma/period formats as locales.

Intake is capped at 24 candidates per source, ordered by a preregistered hash rule after revision pinning. Exclude every prior Antsy source ID/image hash, all prepared qualification/evaluation packets, and perceptual duplicates. Keep the earlier 18-case E1/E2 reserve unchanged. Fresh means unseen by experimental agents in this project; no claim about foundation-model training contamination. Intake/annotation exposure is disclosed and does not become model evaluation evidence.

Before freezing, a source-only pass records exact total token, semantic total label, currency/locale, quality, target bounding box and uncertainty without viewing dataset gold. A separate pass compares dataset annotation. Agreement supports a label; a discrepancy requires another source-only adjudication by a distinct annotator blinded to both candidate labels and all model output. This is data-label adjudication, not a researcher sign-off gate. If that adjudication is unavailable or pixels remain ambiguous, retain it as unresolved; never decide by model consensus, sum-of-items arithmetic or the eventual treatment output. No claim of independent annotation is permitted for two passes by the same operator.

Select the first 3 adjudicated cases in each cell plus the first unresolved case per locale. If cells cannot be filled within 48 candidates, report infeasibility before funding; do not silently replace the design. Freeze original and delivered-image hashes, source revisions/IDs, selected and excluded candidates/reasons, quality decisions, adjudication records, evaluator-only labels and actor-only manifests. No annotations, bounding boxes, labels or corrupt-control answers enter actors; original full images are delivered equally. Private images/receipt identifiers stay outside public Git.

## Control and competence

K receives one plausible wrong proposal per receipt, fixed before collection: substitute one total digit without changing the token's separator grammar, and verify the result is absent from every relevant total/payment row in delivered pixels. Where the total is unresolved, choose a well-formed absent token and record the limited nature of that test. Corruptions are artificial verifier challenges and do not estimate natural error prevalence. Score both boolean rejection and enforced exact-token rejection; the latter must not conceal a semantically poor checker.

Before funding, complete offline format/referral/partial-output/budget/trace tests using historical data only. Native reader competence is measured in the pilot: report A/B and D1/D2 individually, not just agreements. No fabricated qualification receipt, favorable reroll or threshold relaxation. This finite pilot is the competence/feasibility test, not a successor to the failed Q2 qualification or an automatic path to its evaluation.

## Analysis, stopping and decision value

Primary descriptive contrast: blind versus conditioned wrong acceptance and correct service, paired on 12 scorable receipt units. Show rescue/harm tables relative to literal-only and direct agreement; wrong/accepted risk alongside correct/assigned coverage, referral/assigned and missing/assigned. Display all outcomes by quality and locale with denominators. Treat the two unresolved cases separately: an accepted value is unsupported, not proven numerically wrong; referral is safe handling, not a correct total. Report digit disagreement, token/boolean contradiction and shared wrong-token rates. K calls are nested controls, not extra receipt units.

No significance claim or population error-correlation estimate. Even zero wrong accepts in 12 independent cases gives a one-sided 95% upper bound near22%; merchant/layout clustering weakens generalization further. The sample is intended to reveal mechanisms cheaply, not certify payment safety. Show original reading → second reading/check → deterministic amount → accept/refer for every case using observed data only. Do not animate fictitious agent deliberation.

Run the fixed roster, including scientific errors. Stop on the first transport, route, accounting, malformed-structure or trace-integrity failure; preserve incomplete and unstarted assignments. One request in flight, no automatic retry, no replacements, 30-minute wall-clock limit. Scientific errors are outcomes and do not trigger outcome-dependent stopping. A claim of progress needs at least two literal-only errors prevented, zero introduced wrong accepts, at least8/12correct service, and complete reconciliation; these are descriptive advancement criteria, not statistical evidence. Otherwise park or propose a justified new design to PI. If A makes no errors, the verifier-benefit question is uninformative and does not justify scaling automatically.

## Finite proposed envelope

Stage name: **B1-blind-versus-conditioned-pilot**. Maximum14 receipts ×6 calls =84 calls. Maximum512 output tokens and conservative8192 input tokens per call; reserveUSD0.015 before each dispatch at the previously verified route prices. **Proposed maximum additional API exposure USD1.26.** Reverify current prices/route/token accounting before funding; if they exceed this bound, revise the proposal rather than dispatch. Existing approved-team allocation only with verified zero incremental charge; otherwise infrastructure needs an explicit bounded revised envelope. No provisioning is proposed. No model calls or new charges have occurred in this preparation.

Carry known APIUSD0.220104 plus provisional legacyUSD5hold; proposed API-inclusive carried exposureUSD6.480104 if the full pilot bound were authorized. This is part of the USD200 project aggregate and constrained by the existing USD20 Antsy slice, not a separate pool. Shared historical fleet billing remains centrally reconciled. PI funding/selection, complete case freeze/adjudication, source/runtime verification, public immutable plan and page verification, dedicated current allocation and original-ledger admission are required. Current funding reservationUSD0. Finish every attempt with saved-response replay, native trace audit, honest scientific post-mortem, cost reconciliation and worker release.
