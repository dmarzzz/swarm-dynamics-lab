# Antsy v6: accept, check, or refer a receipt total

Exploratory instrument and application pilot, not an accepted hypothesis or production payment system. Plan written before implementation, 2026-10-04 UTC. Parent: [v5 issue ledger](../antsy-verification-v5/ISSUES.md). Repository refresh:3ccbfd02a6d54713103732867cd43f6d4b2f0d6b.

## Why this experiment

A receipt pipeline should not automatically accept a plausible but wrong total. Extra computation is worthwhile only if it reduces wrong acceptances or manual referrals enough to justify its measured latency. V4/v5 scored regional token recall and used annotation-perfect QA; neither tested this operational choice. V6 extracts one annotated field from pixels and lets real, fallible tools challenge the initial result.

Scope refinement: the v5 successor sketch named amount, currency, date and merchant. CORD's documented total.total_price label directly supports the amount task; inventing reference labels for other fields would weaken the experiment. V6 tests the total amount only, with explicit unsupported/ambiguous handling. It does not execute payments.

## Task and tools

Three initial candidates use Tesseract ind+eng with segmentation modes3/6/11 on the original image. One actual checker uses an autocontrasted grayscale image enlarged2× with mode6; another uses the same transformation with mode11. All five pipelines are measured once per receipt; paired policies replay their recorded outputs. Policy latency is the sum of the actual invoked-tool measurements, not a separately measured online end-to-end runtime. No ground-truth box/crop/category enters OCR or candidate extraction. Candidates come from OCR lines anchored to total/grand total/total bayar/jumlah bayar, excluding subtotal, quantity, cash, change, tax and service lines. Conflicting parsed totals within a pipeline produce an ambiguous candidate, not an arbitrary winner.

Number parsing is a declared dataset convention: plain nonnegative integers; grouped thousands with three-digit groups; optional two-digit decimal fraction; optional Rp/IDR prefix. Reject malformed groupings, negative values, embedded letters and unsupported precision. A single three-digit suffix is treated as a thousands group for this Indonesian receipt task; retain this locale assumption and do not claim general financial normalization. Candidate and gold parsing use separate entry paths; independently specified fixtures test the shared numeric contract. Ambiguous/missing reference labels are unscorable, counted in the assigned denominator and reported separately—not treated as correct abstentions.

## Data and leakage controls

Pinned CORD-v2 revision7f0115a4b758a71d6473b8d085751692da2fef98. First20 train receipts are development measurement; the prior validation100 is never a fresh evaluation. The official test split is unopened until scoring/policies and development assessment are frozen. Planned exploratory evaluation: first50 test receipts, no selection by whether a policy wins. Image hashes must be disjoint from development and prior validation. Vendor/layout independence cannot be guaranteed by image hashes: compute a text-header family fingerprint from OCR, report overlap, and treat this as a limitation rather than calling the splits vendor-independent. Retain all assigned receipts including missing candidates, reference ambiguity and failures.

Actor payloads contain only candidate amounts, confidence, tool availability, measured tool latency summaries and budget. Truth is in a separate evaluator record and used only after terminal action. A checker returns its own OCR candidate—not a correctness flag. Missing/ambiguous checker output must not increase support or alter existing candidates. Repeated identical candidates from one tool do not count as independent evidence. All tools share Tesseract; agreement is correlated, not five independent experts.

## Policies and primary measures

Freeze thresholds before fresh evaluation. Baselines: fixed initial mode6; highest-confidence initial candidate; initial agreement-or-refer; always run both checkers then agreement-or-refer; selective checking (accept initial agreement, otherwise query checkers until agreement or exhausted, then refer). Agreement means at least two distinct pipeline outputs with the same numeric amount; ties/conflicting top support refer. These policies are transparent and can fail on correlated errors.

Primary: correct automatic acceptance per assigned/scorable receipt, incorrect automatic acceptance, referral rate, conditional error among accepted, checker calls and measured incremental checker wall time. Reference-ambiguous rows remain visibly unscored. Report a sensitivity loss of wrong acceptance +0.1/0.25/0.5×referral separately from actual compute latency; these penalties are assumptions, not dollars. No fabricated human-review time. A hindsight best-candidate oracle is diagnostic only.

Model comparison is a separate qualification stage after the tool pilot: one versus five decision roles with the same candidates/tool budget, matched-call control before efficacy claims. No model launch is implied by successful OCR execution. The user requests rerunning under better conditions; this version's first rerun is the actual application/tool pilot, and its evidence determines whether a committee comparison is warranted.

## E0 development pre-run and acceptance

Fresh dedicated fleet claim required. E0:20 train images×five measured OCR pipelines, maximum100 OCR calls, timeout30s/call, one CPU worker with OMP_THREAD_LIMIT1, 15-minute stage cap, zero API/model calls. Store images/raw text privately in run storage; publish only numeric candidate values, statuses, counts, hashes and evaluation records. Dataset attribution CORD/NAVER CLOVA, CC-BY-4.0.

Before run: numeric/parser fixtures, missing-vs-zero, subtotal/cash rejection, duplicate/conflicting evidence, failure/denominator tests, hidden-truth mutation invariance, policy action legality and mutation tests must pass. Publish immutable source URL and run TLDR. Assess development scoring against reference strings locally without publishing raw receipts. Require complete assignment, zero hidden-label input, honest missing/failure accounting and measurable real checker outputs/latency. Zero tool benefit is a valid result; do not author errors or winners to force headroom.

Before fresh S1: publish E0 post-mortem, freeze all repairs and thresholds, retain independent external scoring review as pending if unavailable. Such a run remains an explicitly exploratory instrument pilot, not confirmatory efficacy; formal hypothesis gates remain closed. This replaces the broad v5 launch language with stage-specific scope: real tool measurement can proceed while independent review blocks confirmatory claims and broad model escalation.

## Visualization and reproducibility

Show candidate agreement and disagreements, actual checker invocations and elapsed times, accept/refer action, then evaluator reveal. First3 assigned receipts are fixed examples; any worst-case addition labeled post-hoc. Overview plots show correct/wrong/referral counts and measured latency separately; no decorative biological animation. Keep per-action histories for GIF/replay and all numeric outcomes for audit. Every run immutable, failures preserved, source/data/tool versions recorded, no outcome retries.

## Sources checked this session

[CORD primary repository](https://github.com/clovaai/cord) and [official dataset card](https://huggingface.co/datasets/naver-clova-ix/cord-v2), README/schema/license and split metadata checked; not a new full literature survey. CORD provides post-OCR parsing labels; Tesseract/policy performance here is measured by us, not claimed by the dataset authors. Existing biological quorum analogy remains motivation only: this is a decision-routing experiment, not an ant-colony replication.
