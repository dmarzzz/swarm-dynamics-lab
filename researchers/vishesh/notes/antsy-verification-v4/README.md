# Antsy: test before trust

**Question:** when three OCR configurations disagree about a real receipt, which output should a system trust—and which small verification would most improve that decision?

A receipt-processing service can run several cheap OCR configurations, but reviewing every output is expensive. High OCR confidence is not proof that the important text was recovered. Antsy gives a decision-maker two regional quality checks and asks it to select one output. Five local Laya roles propose checks and vote on when to stop. They compete against a fixed configuration, confidence alone, random checks, a deterministic check rule, and one agent with all the same observations.

This is exploratory S0/S1 engineering in owned notes, not a reviewed hypothesis or a production OCR benchmark. The [earlier API study](../adaptive-quorum-v2/repair-v3/SPEC.md) remains available; [its bad decisions](BAD-DECISIONS.md) motivated this redesign. V4 changes the application and intervention. It does **not** replicate v3's urgency treatment: verification credits replace scheduled evidence arrivals, and there is no measured deadline effect here.

## Why run this?

We should pay for a swarm only if there is a useful decision to make and it makes that decision better. Three progressively stronger tests can reject the idea:

1. **Is selection useful?** On 20 calibration receipts, the best fixed configuration recovered 60.2% of annotated tokens; choosing the actual best configuration for each receipt would recover 66.8%. The 6.6 percentage-point gap passes the predeclared 1-point relevance threshold. This ceiling is known only to the evaluator.
2. **Is verification useful?** Do purchased regional checks recover that headroom, or merely change an already adequate choice? Compare quality, regret and checks against no-check controls.
3. **Is a committee useful?** Do five roles improve on a single agent and a deterministic rule enough to justify their extra calls? A negative answer is a useful result; there is no requirement that adaptive quorum win.

The calibration result is an observed development-set fact, not the final evaluation result. It establishes a reason to test routing, not a reason to deploy agents.

## Setup

- **External tasks:** all 100 receipts in the revision-pinned CORD-v2 validation split. No hand-assigned winners, simulated OCR errors or synthetic evidence arrivals. Original receipt authors and annotations determine difficulty.
- **Real alternatives:** Tesseract page segmentation modes 3, 6 and 11, all using Indonesian plus English recognition on the same unmodified images. We measure all three outputs once and reuse that fixed counterfactual table across policies.
- **Available evidence:** per-configuration confidence and word counts in top, middle and bottom image thirds. Prompts expose confidence, a calibrated quality estimate, and bought QA responses; word counts are retained for audit but do not enter decisions in v4.
- **Paid check:** reveal the annotation-based token recall of one configuration in its least-confident unchecked region. This models a perfectly accurate human QA service. It is a strong, explicit idealization; labels are not free to actors.
- **Action:** choose a configuration to check, or stop. A shared deterministic selector commits to the highest estimated quality after the checks. We test verification allocation, not unrestricted visual reasoning or end-to-end field extraction.

The agents cannot view receipt images or strings. They reason over compact quality summaries. All OCR has already run, so this study measures selection and verification—not savings from avoiding OCR calls, API price differences or actual human review time.

## Protocol

Calibration IDs 0–19 determine the best fixed configuration and one additive confidence correction per mode. IDs 20–29 screen the instrument after policy freeze. IDs 30–99 form the 70-receipt exploratory comparison. The official test split remains unopened. Calibration outcome inspection is allowed; evaluation outcomes remain uninspected until policy code and this protocol are committed.

Each receipt receives all seven arms under identical measured OCR and reference data. The five-role fixed and adaptive policies share exactly the same potential ballots until adaptive stopping; later unused ballots do not count as adaptive calls. Two checks maximum, deterministic tie-breaking, seed 71 for random checks. No outcome-based retries or evaluation-set tuning. The independent analysis unit is the receipt, not a vote, check or policy row.

See [the mapping to the original project briefs](CONNECTIONS.md). Read [SPEC.md](SPEC.md) for exact estimators, prompts, thresholds and controls; [RUN.md](RUN.md) for reproduction; [SOURCES.md](SOURCES.md) for sources and read-depth boundaries. Machine and attempt records identify frozen commits. The [pre-run assessment](reviews/S0-S1-pre.md) includes acceptance criteria and the visual mapping.

## Metrics

Primary: mean **regret**, the difference between the best of the three measured OCR recalls and the selected recall, reported with paired quality differences against the strongest simple controls. Also report checks per receipt, physical and logical model calls, inference time, exact annotated total-price token recovery, and the fraction within two points of the oracle.

Recall is a spatially matched, normalized token-multiset score over CORD's annotated lines. It is not full-text precision, numerical amount correctness, field extraction accuracy or payment safety. The exact-price secondary score checks annotated tokens including extras; normalization ignores punctuation and token order. It must not be read as exact financial transcription.

Show quality versus verification cost, and descriptive utility at check costs 0, 0.01, 0.02 and 0.05 recall units. No conversion to dollars is asserted. Receipt bootstrap intervals describe this sample's paired differences, not generalization to arbitrary languages, layouts or OCR systems.

## Expected behavior and what would be interesting

It is reasonable to expect the fixed configuration to be hard to beat, confidence to miss some OCR failures, and occasional regional checks to reverse a mistaken choice. It is **not** safe to expect more roles to improve decisions: they share one checkpoint, consume overlapping evidence and can repeat the same error. Fixed verification spends more; adaptive verification may save checks but miss useful corrections.

The interesting result is a boundary: where checks correct errors, where they mislead the whole-receipt estimate, and whether the committee adds value after simpler explanations are tested. A swarm losing to a fixed configuration would argue for keeping this application simple. A modest gain with many more model calls may still be operationally unattractive.

The biological connection is limited: distributed assessment and commitment resemble collective site selection, but these agents have no embodied exploration, independent sensory noise or evolved signaling. This analogy motivates an allocation question; it is not evidence of biological fidelity.

## What the viewer should see

A measured comparison chart, an oracle-headroom plot, and time-ordered replays for the first three receipts in each run—not selected success stories. A replay shows estimated quality, actual paid checks, votes, stopping and final selection. Hidden scores appear only after commitment. There are no decorative ants implying movements or observations that did not occur.

**Completed results:** [the skeptical assessment](RESULTS.md) reports both 70-receipt studies. Confidence alone achieved 56.78% recall, versus 56.30% for Laya and 55.72% for Jev committees; neither adaptive committee saved checks. Both full runs passed the integrity audit with zero invalid calls. Earlier Jev qualification failures remain documented. A failed run remains visible, with the repair and its unchanged or amended protocol identified separately.

## PI follow-through — 2026-10-04 UTC

Both frozen evaluations are complete; the [results](RESULTS.md) supersede the [PI review's](https://github.com/dmarzzz/swarm-lab/blob/e0a3170/researchers/dmarz/notes/next-experiments-2026-10-04/README.md) historical running-status snapshot. Neither committee improved the observed mean over confidence alone or activated useful early stopping. Keep that completed comparison intact. It is evidence about this selector and QA contract, not a reason to abandon verification generally or rerun these receipts until a committee wins.

A successor is conditional on fresh development documents demonstrating both decision headroom and informative purchasable checks. Repair empty-region handling and unequal-region weighting before testing efficacy. Use measured, imperfect checker outputs and actual review cost, with explicit abstain/escalate actions; distinguish choosing an OCR output from correcting its contents. Compare confidence/no-check, a competent single solver, a deterministic value-of-information policy and a committee with the same initial evidence and declared total resource allowance. Qualify cases that require both stopping and continued checking before expanding beyond one versus five decision agents.

Freeze a required-field decision loss and report correct receipt-level decisions, false confident decisions, warranted abstention, checks and total cost. Token recall remains secondary. The existing 4.18-point recall headroom is not comparable to the PI's proposed 5-point improvement in receipt-level field decisions: those are different endpoints. The latter is a candidate useful-effect target to justify prospectively, not a threshold already established by v4.

Use new document families for development and untouched evaluation, cluster duplicates and dependent vendor/layout templates, and size evaluation from paired uncertainty. Do not tune on these 70 evaluation receipts. These are successor-design requirements; no new run, model allocation or modification of the completed protocol follows from this amendment.

## Separately authorized Jev comparison

[The Jev pre-run plan](reviews/Jev-pre.md) freezes the same task/policies for a distinct hosted model condition. Fresh competence and receipt qualification are required. Laya remains separately reported; access to a credential is not a qualification result.
