# Post-mortem: native-D2-01

Owner vishesh/codex-experiments, 2026-10-04. Exploratory diagnostic, parent Q4/D1. Frozen source 518d4412bc566a388dd4dc022118ade8dd637fa3, unchanged Haiku snapshot/config, [prospective assessment](native-D2-01-pre.md). Run `influence-swarms/1004-044202-3747f4`. Disposition: **complete-valid-result for the instruction-based diagnostic; proposed repair rejected; S1 still unqualified**.

## What ran and happened

Six fresh authored dossiers × five dependent workflows: 30 assigned → 30 started → 30 terminal → 30 valid → 30 graded/analyzed. No missing/duplicate decisions, transient retries, execution-invalid outputs or missing usage. 108 calls, 279,584 input tokens, 22,415 output tokens, USD0.391659, 353.55 seconds. All response-level usage sums to summary usage.

Acceptable: original team with ballots 2/6, without ballot fields 3/6, generalist 5/6, general review 4/6, targeted approval review 3/6. Primary targeted-minus-general pair differences: -1,0,0,0,0,0. No claim of statistical generality from six authored clusters. Targeted review failed its six-of-six screen, with one invalid purchase and two avoidable deferrals. Generalist also failed the export-alternative case. All workflows passed sponsored-value and usage-cost controls. Complete per-case decisions, source audit and costs are in [results](../RESULTS-D2.md).

Review observations were identical, review instructions differed, final chair instructions stayed fixed and each chair received its appropriate appended report. No evaluator was passed to actors. Decimal recomputation from primary text agrees with all terminal grades and scorecards. This is an author-side replication of Dmarz's arithmetic method, not an independent D2 case review.

The requested checklist was not faithfully implemented by the model. Three of six targeted reviews omitted at least one candidate's name entirely, and two focused all findings on a blocked favorite while ignoring supported alternatives. Names alone cannot demonstrate complete coverage. The instruction assignment is valid, but we cannot conclude that a faithfully performed checklist fails. Recognizing a blocker also did not guarantee respecting it in the purchase action.

## Visualization and delivery review

Mapping from ITERATION-03: six-row/five-column live and final PNG, raw event timeline, interactive replay exposing requests/reviewer claims/chair rationales, and 31 GIF frames (initial pending + all 30 terminal events). Fixed playback cadence is disclosed; event timestamps remain in JSONL. Full grid resolves the earlier last-15-row display limit. Every terminal cell is sourced from outcomes; GIF construction asserts exact event/outcome equality. Source audit verifies denominator and grade agreement. Local browser validation and durable hub inventory are recorded in deployment closeout; raw files retained even if public site embeds only PNG.

## Quality and failure ledger

| Issue | Evidence / cause confidence | Action and status |
|---|---|---|
| Purchase despite known missing approval | Q4/D1 and D2 regional case; model output directly verifies mismatch | Targeted instruction did not repair it. Preserve adverse results; no forced choice or reroll. |
| Avoidable blanket deferral | D2 renewal/export controls have supported alternatives | Newly discriminated by controls; remains a behavioral limitation. |
| Checklist fidelity | Targeted findings fail candidate coverage | Instruction-based manipulation only; schema-enforced candidate coverage is a future distinct intervention, not retroactively credited here. |
| Numeric rationale errors | Examples conflate software ceiling and total cost or assert false percentages | Choices separately scored; raw text exposed for audit. Correct action is not proof of faithful reasoning. |
| Label imbalance and scripted-frame wording | First offline fixture used only two purchase labels and said native | Fixed before model run; second fixture 30/30 and all four labels, explicit scripted label. First fixture retained. |
| Budget envelope estimate | Plan omitted provider's 512-byte per-attempt allowance | Correct bound USD6.082560, below USD7.226604 available at launch. Transactional cap always enforced. Future preflight now derives bound from config; regression added. Frozen run unaffected. |
| Synthetic external validity | Same-author template variants; shared rates and rules | Explicitly limited; no real-vendor or broad external-influence claim. |

No second researcher review was required. Dmarz's later actual Q4 answerability PASS was incorporated, with its scope preserved. Q4 competence still failed; this diagnostic never opens S1. Original failed cohorts remain distinct. Evidence confidence for this scoped diagnostic is exploratory (1/4); external-influence efficacy remains untested (0/4).

## Next design decision

Reject targeted instructions alone as a sufficient repair. If extending the architecture study, require a cited model-generated assessment for every candidate in a typed output, keep final choices unconstrained, and test on fresh cases against the cheaper generalist and a structurally matched control. Independently authored cases are needed for stronger external validity. Do not rerun this batch for a favorable outcome, lower qualification thresholds, or claim a deterministic deployment guard improved model reasoning.
