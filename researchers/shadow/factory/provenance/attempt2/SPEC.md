---
id: shadow-factory-provenance-attempt2
version: 2
owner: shadow/sol-factory
status: prospective-exploratory
model_pool: claude-sonnet-4-6
model_openrouter: anthropic/claude-sonnet-4.6
qualification_roots: 6
main_roots: 12
copies: [1, 4, 16]
arms: [raw, ancestry, dedup, padding]
seed: 202610041114
qualification_seed_pool: 202610040603
qualification_seed_openrouter: 202610040604
input_proxy_tokens: 1800
tokenizer: cl100k_base
max_output_tokens: 128
max_input_bytes: 16000
max_http_attempts: 149
max_paid_usd: 9
factory_max_paid_usd: 10.851345
concurrency: 1
request_timeout_seconds: 90
stop_new_requests_at: '2026-10-04T23:00:00+00:00'
transport_retries: 0
bootstrap_draws: 10000
confidence_threshold: 0.8
qualification_required_correct: 6
primary_contrast: raw-copy16-minus-copy1-accuracy
---

# Provenance / duplication invariance: prospective attempt 2

## TLDR

Hold five independent synthetic evidence acquisitions fixed, duplicate one contrary report 1, 4 or 16 times, and compare raw synthesis, explicit ancestry, and deterministic root deduplication before synthesis. A separate irrelevant-padding arm varies only tagged irrelevant material. The primary quantity is the paired root-level change in exact decision-rule accuracy for raw reports at 16 versus 1 copy. Ancestry and dedup contrasts test whether those interventions reduce copy sensitivity. This is a bounded 12-root instrument pilot, not a realistic semantic provenance benchmark or a replication of another owner's native run. Run six no-copy competence cases first. All comparisons share the same 12 generated roots; calls are never independent worlds.

## Question and prediction

Does repeated presentation of existing contrary evidence change a reader's decision when no independent evidence is added? Predict raw repetition may reduce accuracy/increase false confidence relative to copy1, with attenuation under ancestry or deterministic dedup. A valid null supports invariance within this simple grammar only. Poor clean competence ends the diagnostic without treatment inference. Deterministic dedup already solves the bookkeeping; the native question is whether downstream synthesis obeys the rule or is distracted by repetition, not whether models discover unknown origins.

## Setup

Each task root has five independent synthetic acquisitions. Draw five distinct, nonzero signed integer evidence contributions from -9..9. Their sum must be nonzero, both signs must occur, and multiplying the strongest contrary contribution by 4 must reverse the naive count-all sum. Rejection-sampling defines the selected stress-test population. The normative choice is A for positive unique-acquisition sum, B for negative. No latent truth is sampled: accuracy means agreement with this declared evidence-aggregation rule, not accuracy about an unknown real-world state. These independently drawn numeric roots share one task grammar and are not independent semantic task families. Qualification uses disjoint random streams and accepts nonzero mixed-sign sums without the naive-flip restriction.

Each original acquisition has an authoritative harness ancestry ID. Copies preserve its contribution and sentence, not a new acquisition. Raw packets omit ancestry. Ancestry packets expose the correct root ID. Dedup applies exact authoritative root-ID dedup upstream and sends five unique contributions. We do not claim a real authentication system or a semantic ancestry resolver. In the raw arm, identical sentences are the only copy cue; distinct original magnitudes prevent same-text independent events in this deliberately narrow instrument. The task instruction explicitly says exact repeated measurements do not add independent evidence. Ancestry changes available provenance information intentionally.

## Protocol

1. Check current Quorum tasks and hub, publish this plan, freeze source and all assignments, pass offline checks, and register the immutable plan for our distinct experiment. No changes to Vishesh or Dmarz files, runs or reservations.
2. Use OpenRouter only, with the fixed Anthropic provider and sonnet-4.6 model. No pool calls, route switching, HTTP retries, credential changes or account limit changes. HTTP400 is a request-contract failure and ends this attempt, never availability or a paid fallback. HTTP429/503 are availability errors but also stop without retries. Use fresh qualification seed 202610040604; all six must pass before main. The previous attempt consumed two of the original151 HTTP requests. Exactly149 remain, so this attempt can obtain at most143/144 main answers after six clean qualification answers. Preserve all12 planned roots and mark the final unstarted cell missing rather than silently enlarging the original allowance. Root-first ordering allows at most11 fully complete roots, while individual paired contrasts can cover12. Shadow's new instruction authorizes up toUSD9 new liability, not a silent reset of HTTP allowance.
3. Clean qualification: six no-copy, explicit-ancestry roots; require six valid and correct decisions. Stop immediately on any failed/invalid/wrong response. A provider block on OpenRouter terminates the pilot; do not change the key or account quota.
4. Main: twelve paired task roots, four arms and three copy levels per root, 144 requests maximum. Complete each root before moving to the next. Rotate/reverse acquisition ordering across roots; within a root, preserve underlying relative source order across doses and arms, with duplicate occurrences interleaved by a root-keyed permutation. Shuffle arm/dose dispatch order deterministically within each root. No outcome-dependent ordering or replacement calls.
5. Use 20 report slots in every packet. For raw/ancestry, insert the selected copy count and fill remaining slots with tagged irrelevant padding. Dedup always has five unique evidence rows plus fifteen irrelevant slots. Padding-control packets always have five unique evidence rows, with 0/3/15 of the irrelevant slots carrying an alternate irrelevant sentence at nominal copy1/4/16. Those sentences contain no evidence contribution. All messages have exactly 1,800 input **proxy** tokens under frozen `cl100k_base`, using a tagged final filler section, and identical 128-token output limits. Provider-native tokenization is unavailable locally: actual provider usage is retained and input-token imbalance reported. Do not claim exact Anthropic-token parity. Equal input budget, constant slots, proxy-token matching and an irrelevant-padding arm control length as far as the instrument measures it.
6. Every HTTP attempt must first reserve in a synchronized persistent call ledger and, if paid, the existing factory-wide paid ledger. Write immutable initialization receipts with effective body/model/config/context/source hashes. Return-model metadata belongs in a separate response/outcome record; on no response it is unknown, never inferred. Deny dispatch without matching current registration/admission and pinned assignments.
7. Write unique-ID, create-once raw numeric outcomes before rendering or hub publication. Retain errors, failed qualification and not-run assignments. Reporting failures are separate from scientific outcomes. Resume is closeout-only for interrupted attempts; ambiguous calls are never retried.
8. Recompute from immutable records with a separately implemented checker before any extension. Require an independent agent/researcher readback before scaling; this pilot never auto-scales. Completed, independently checked contrasts per elapsed hour is the progress metric. Until that reviewer exists, the independent-checked count is zero, regardless of commits/tests.

## Metrics

Per request: exact decision-rule accuracy (0/1); confidence on the chosen decision in [0,1]; false confidence = incorrect and confidence >=0.8; malformed/provider failure separate; decision; latency, usage and monetary liability. Root-level copy effects: dose4 and dose16 minus dose1 for accuracy and false confidence, plus decision-flip indicator between doses. Root-level intervention effects compare ancestry or dedup copy sensitivity against raw. Padding-control dose effects and dedup repeated-input variation are diagnostic references, not extra worlds.

Report every paired root difference and equal-root means. Bootstrap whole complete paired roots, 10,000 draws with the frozen seed, with exploratory percentile intervals. No interval with fewer than 10 complete roots. Use all 12 assigned roots for missingness: bounded [-1,+1] differences and [0,1] flips yield worst-case bounds; missing responses are never silently dropped or imputed as known scientific failures. Report planned, started, valid, invalid, failed and unstarted separately. No multiplicity-adjusted confirmatory claim across arms/endpoints. A complete valid negative ends this pilot; do not rerun for a favorable result. Fine-grained probability calibration is not measured by six qualification items or twelve main roots.

## Credit and overlap

Vishesh's [Quorum of Mirrors](../../../../vishesh/notes/decision-models/quorum-of-mirrors/README.md) already explored acquisition lineage and later recorded 0/8 correct full-lineage choices. Its [provenance gate](../../../../vishesh/notes/decision-models/quorum-of-mirrors/provenance/RESULTS.md) is a useful deterministic baseline, not permission to launch its successor. This Shadow-owned diagnostic uses fresh code, arithmetic contributions, roots and a distinct registration. It tests supplied trustworthy ancestry, not Vishesh's proposed semantic report-to-receipt resolution. Dmarz's [identity-splitting study](../../../../dmarz/notes/sybil-split-opus/RESULTS.md) motivates copied identity versus independent evidence. [AskSwarm](../../../notes/wild-askswarm/README.md) motivates distinguishing repeated text from independent adoption; this synthetic study does not validate its observational clustering or make an in-the-wild claim.

## Resources and stopping

Shadow's explicit 2026-10-04 15:43 EDT successor instruction authorizes this same-question attempt with a HARD USD9 new OpenRouter liability cap. The shared factory ledger retains USD1.851345 prior liability, including all unknown reservations. Reserve every request's conservative maximum before transport, synchronized on that same ledger inode. Enforce USD9 for this attempt and USD10.851345 cumulative factory liability, below the olderUSD20 ceiling. The newUSD9 includes this attempt's unknowns; none may be released without actual cost. The shared key also serves cm2, which has a separateUSD8 lane cap. This runner neither spends on cm2 nor changes the shared key limit. No pool use, one process/request, no retries.

Stop new dispatch at23:00Z (19:00 EDT), leaving15 minutes before the mandated19:15 EDT main-branch closeout. Each socket timeout is min(90s, remaining window), not a guaranteed process kill. Stop at first failed/invalid/wrong qualification, first main transport/schema failure, remaining149-call cap, dollar cap or deadline. Persist every unstarted assignment. No scaling or other factory scope.

## Missing outcomes and operational lineage

Attempt1 is immutable and not resumed: source76f42cdd, two HTTP attempts, zero valid answers, zero complete roots, all144 scientific main cells missing. Its300 terminal files are two conditional route plans, not300 calls. See [POSTMORTEM](../POSTMORTEM.md), [frozen admission](../results/admission.json), and [review](HISTORICAL-REVIEW.md). The current agent independently read the historical raw records and ran the stdlib checker (2026 passing checks); this is a separate agent inspection, not an independent human/researcher replication. JF002 wire repair has two committee reviews in mergedPR106.

Do not pool attempt1 missing responses with this attempt or count this as a replication. Main roots, actor prompt, grammar, doses, arms, decision rule and estimands are unchanged. Only qualification stream, route policy, compatible request contract, error classification, reduced remaining HTTP allocation and explicitly authorized financial/deadline envelope change. The new registration, implementation and assignment/admission objects must be committed and pushed before any request. No historical specs, pins, outcome objects or terminal markers may change.
