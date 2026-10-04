# Antsy v7: different workers, different evidence?

Exploratory tool-worker diversity pilot; no accepted hypothesis or new LLM-agent result. Written before implementation. Parent: [v6 post-mortem](../antsy-receipt-v6/reviews/S1-post.md). Review is not required by the owner's current directive; no independent review is claimed.

## TLDR

Test whether changing OCR engine family changes shared errors, and whether respecting duplicate provenance and dissent improves receipt-total decisions. Measure five real workers on the same receipt, then compare related versus mixed three-worker teams under majority versus provenance/dissent aggregation. Compare every team to each individual worker. Report wrong acceptance together with coverage and measured compute; a more cautious policy cannot claim success merely by referring more. Zero hosted-model calls; this qualifies reusable diversity instrumentation before LLM workflows.

## Question and prediction

Does mixed-engine evidence reduce same-wrong answers relative to related Tesseract variants, and does a dissent-preserving decision rule prevent wrong majorities without excessive referral? Prediction: a second engine will supply some correct totals absent from Tesseract, but shared pixels, layout and extraction code can still cause common errors. Dissent protection may reduce wrong acceptances at the cost of coverage; it may fail to provide useful advantage over the strongest single worker. Higher disagreement alone is not success: incompetent workers can be highly different.

Intended decision: whether distinct perception paths provide enough complementary information for a later equal-budget one-versus-five decision-agent study. No urgency effect or biological replication is tested. Engine changes confound quality, training and architecture; this pilot does not identify a pure causal effect of an abstract diversity scalar.

## Setup

Pin the v6 CORD-v2 revision. Prior train0–19, validation0–99 and test0–49 are used regression/development material. S0: train20–39,20 qualification receipts. S1: test50–99,50 receipts not previously opened by this study. Verify image hashes against all prior records and across stages before OCR. Holdout status is study-local, not a claim that pretrained engines never saw CORD. Dataset merchant/layout independence is unverified and reported as a limitation.

Workers: T0/T1/T2 are Tesseract ind+eng modes3/6/11 on original pixels. R0/R1 use pinned RapidOCR/ONNX models on original and grayscale-autocontrasted2× pixels. RapidOCR supplies a second model/engine family; it is not assumed independent merely because its name differs. Record actual package/model hashes, input/transformation hashes, common extractor hash and delivered observations. No conversation history, peer messages, mutable cross-receipt memory or evaluator labels enter workers. Gold is read separately from gt_parse.total.total_price. All worker outputs retain statuses, candidate provenance and measurement times. Raw receipt/OCR text remains private; publish numeric candidates, evidence-region hashes, configuration hashes and events.

The normalized total contract remains conservative. Expand legitimate label coverage prospectively to TOTAL, GRAND TOTAL/GRANDTOTAL, TOTAL BAYAR, JUMLAH BAYAR and AMOUNT DUE/DUE, allowing label punctuation and amount-before-label when the remainder is exactly a valid amount. Reject subtotal (including hyphens), quantity, cash/change, tax/service lines, multi-number tails and conflicting totals. No arbitrary numeric salvage or annotation-directed crop. These changes apply identically to all engines; there is no comparison to old v6 accuracy as though only aggregation changed.

## Protocol

Write and test instrument before S0. Record a fresh exclusive approved-fleet claim and current public-plan receipt before loading the second engine or collecting any experimental output. S0 maximum100 OCR invocations; S1 maximum250. One process, capped engine threads,45s per OCR invocation and30-minute stage cap. Maximum one bounded repair qualification on train40–59 if a material instrument/competence defect appears; preserve prior attempt. No automatic S2 or repeated holdout tuning. Zero model/API calls or new infrastructure creation planned; retain original Antsy spending ledger without resetting authority.

Qualification: all20 assignments accounted for; zero hidden-label inputs or execution failures; at least16 scorable references; at least one individual worker gets >=50% of scorable totals correct and each engine family produces >=2 correct totals. This qualifies a useful perception comparison, not efficacy. If failure is a software defect, repair it prospectively on development, then use the reserved qualification set. If genuine weak competence remains, do not relabel it as a successful comparison.

Primary factorial cells use related team T0/T1/T2 and mixed team T0/T1/R0. Each has three measured worker outputs. All five outputs are collected once for every receipt and replayed across rules, so collection is shared; operational team costs are reported separately. Equal worker count is not equal compute: report actual cost and single-worker comparisons, and do not claim a compute-matched causal effect. R1 is an auxiliary same-family diversity measurement and robustness team T0/R0/R1, not an extra independent test unit.

Rules: majority accepts a unique amount with >=2 agreeing valid outputs, else refers. Provenance/dissent first deduplicates identical computation origins, then accepts only when >=2 distinct computations agree and no valid computation supplies another amount; otherwise refers. Different segmentation settings are distinct computations but not independent engine families. Family count is reported as supporting provenance, not converted into independent votes. Duplicate identity, new display name and replayed same-origin output must not change this rule. A dissenting singleton triggers referral, not automatic acceptance of the minority. No correctness label or uncalibrated OCR confidence chooses the accepted value.

Negative controls: duplicate one computation under extra display IDs (same provenance root); shuffle irrelevant display names; permute worker order. Preserve the semantic evidence set. Positive offline control: a correct minority against a correlated wrong majority must trigger referral under dissent protection. These are software fixtures, not authored experimental wins. Natural hard receipts are retained; any constructed stress cases are reported separately from real data.

## Metrics

Receipt is the paired analysis unit; five workers and multiple policies do not multiply sample size. Independent vendor/layout clusters are unknown. Primary operating points: correct/wrong/refer per assigned and scorable receipt, accepted-error risk, coverage, and measured operational tool seconds. Display the risk–coverage tradeoff; only describe a practical improvement when wrong acceptances fall without more than5 percentage points of coverage loss, or coverage rises without additional wrong acceptances.50 cases offer weak precision; report paired receipt bootstrap intervals and individual accepted-error Wilson intervals, not safety guarantees. No outcome-dependent sample expansion.

Reusable worker similarity profile has separate layers:

1. Declared differences: engine/model hash, prompts (not applicable here), preprocessing, tools/extractor, observation sources, communication and memory. Never collapse these into an unsupported single distance.
2. Delivered evidence: input/region/provenance overlap. Same pixels and shared extractor remain common dependencies even across engines. A crop hash is provenance, not proof of semantic independence.
3. Behavioral agreement: exact-answer agreement among co-answering workers; missingness agreement reported separately, plus all-assigned denominators. Mutual abstention is not evidence of independent verification.
4. Outcome dependence: same-wrong-answer rate, double-wrong acceptance rate, joint non-correct rate including missingness, and correctness phi correlation (null when variance is zero). Report counts and co-answering denominators; do not call every disagreement diversity benefit.
5. Complementarity: correct-i/wrong-or-missing-j, unique correct candidate contribution, oracle headroom, and rescued versus lost correct decisions. Stratify pair statistics by image-size tertiles fixed from S0 and report within-stratum counts to expose difficulty confounding; residual dependence is still not a causal estimate.

No N_eff claim from five related workers and50 cases. LLM continuation must add exact model/provider, prompt/tool/context/memory/message hashes, independent initial judgments, repeats separating sampling instability from systematic differences, and matched-call controls. This run establishes the measurement interface and tool-worker behavior only.

## Visualization mapping

Live progress by assigned receipt; final 1800px outcome/cost chart; pairwise same-wrong and disagreement heatmaps with denominators; all-case decision matrix; saved-event animation of the first3 assigned receipts, showing candidates before decision and evaluator truth only after commitment. Any selected failure illustration is labeled post-hoc. Trace is a replay of measured outputs, not real-time parallel execution. Missing/failed rows remain visible. Plots cannot affect worker outputs or consume measurement RNG.

## Prior work and limits

Sources opened this iteration: [Kuncheva's author-maintained diversity overview](https://lucykuncheva.co.uk/ensemble_diversity.html), which catalogs pairwise agreement/error-dependence measures; [Guo et al. calibration paper page](https://proceedings.mlr.press/v70/guo17a.html), supporting separation of confidence from correctness probability; [RapidOCR official repository](https://github.com/RapidAI/RapidOCR), documenting its PaddleOCR-derived ONNX implementation. Read depth is overview/abstract/README, not a full new survey. Existing v6 data establishes the local correlated-error failure. Metrics here are operational definitions, not a claim that the literature provides a universal agent-diversity score.
