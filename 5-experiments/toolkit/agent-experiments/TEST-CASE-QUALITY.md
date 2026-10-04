# Evaluate the test cases before evaluating the agent

A good case tests a useful declared capability, supplies the evidence that capability requires, has a defensible target, and distinguishes the intended mechanisms. Difficulty and model failure are not quality scores. Apply this rubric during [iteration](ITERATION.md), before calling a dataset experiment-ready, and again when traces expose defects. The owning task performs the assessment; this adds no researcher-approval gate.

## Evidence-linked case and suite evaluation

For each row record **pass, fail, or limited**, the check/acceptance criterion, evidence and remaining scope limit. Define numeric floors prospectively for the study; there is no universal case count or average score that can compensate for a fatal flaw.

| Dimension | What makes a good case/suite | Evaluation evidence |
|---|---|---|
| Decision relevance | A result changes a named scientific or engineering decision; case connects to the actual task | Trace the evidence → interpretation → action → scored consequence; state favorable/null/adverse implications |
| Answerability | Inputs determine the target, or deliberately justify abstention; no hidden author fact is needed | Evidence spans or executable witness; insufficient/ambiguous controls; inspect alternative reasonable readings |
| Target/scorer validity | Labels implement the declared rule and distinguish wrong, unknown, invalid and missing | Separate label construction from predictor; independent calculation/implementation where feasible; disclose same-author checking; audit discrepancies |
| Actor isolation | No gold labels, rationale, future information, private operator context or accidental ID/position cue | Actor schema allowlist, serialization checks, label/position balance, opaque-ID and order perturbations |
| Mechanism isolation | Matched conditions change the declared factor, with ordinary controls and invariant variants | Input-diff checks; evidence/capacity/compute conservation; counterfactual targets and causal limits |
| Challenge and coverage | Necessary failures, easy controls, abstention and adverse cases; avoid trivial-only or impossible-only sets | Prospective coverage matrix, source/scenario construction audit, floor/ceiling interpretation, retain all sampled cases |
| Strong comparisons | Best feasible relevant simple controller receives equivalent allowed evidence | Run rule/parser/retrieval baseline, plus ablations; never infer model value solely from weak-baseline misses. A solved baseline can be appropriate for a model-robustness question |
| Realism and scope | Operational structure relevant to use, with assumptions explicit | Document provenance, rights, domain facts, synthetic mechanisms, omitted complexity; real records or independent authorship when broader claims need them |
| Independence and precision | Counts reflect actual task/event roots, not copies, turns or variants | Split/group by source and scenario; prospective precision or finite-support rationale; disclose template dependence |
| Holdout integrity | Evaluation is protected from tuning and selective inclusion | Freeze source/parser/scorer first; record split unit, hashes, access history and release policy. Generated holdouts do not imply new linguistic distributions or independent authorship |
| Robustness and failure handling | Labels stable to irrelevant changes and responsive to meaningful changes | Reordering, renaming, duplication, missingness, corrupt evidence, contradiction and malformed-output checks; no silent exclusions |
| Reproducibility and costs | Every assigned case and outcome is recoverable; realistic resource bounds | Versioned corpus/manifest, exact commands, all-case output reconciliation, native request/token/cost envelope before launch |

## Readiness is specific, not a badge

Record separately:

1. **Case ready for stated scope:** no unresolved answerability, target/scorer, leakage or contrast defect; all predeclared critical checks pass; coverage and limits support that exact inference. Mark broader claims unsupported. A synthetic controlled experiment can qualify without pretending to be a field study.
2. **Native instrument qualified:** the exact model/interface can perform the necessary clean task; parse success alone is insufficient. This cannot be granted by offline case tests.
3. **Run admitted:** concrete scope decision, public immutable plan and registration, runtime/source, budget/ledger and exclusive approved-account allocation are current.

If a critical case check fails, improve or replace cases within the iteration and rerun the relevant checks. Preserve old results; never silently relabel native outcomes. If usefulness fails because the question is already answered, finish/park rather than manufacture difficulty. If real data or access is genuinely missing, complete feasible construction and name the specific blocker. Do not substitute a future-work list for feasible offline repairs.

## Compact case-evaluation record

Keep this within the owned setup/design record or link one machine-readable assessment: intended claim/decision; case and root counts; source/rights and authoring; coverage; label evidence; baseline results; mutation/fault checks; split and contamination history; each dimension's status/evidence; case readiness; native qualification/admission; exact next action. Automated checks support, but do not replace, the owning task's scientific judgment.

## Three checks exposed by the revised study review

Use these within the existing dimensions, without adding another approval stage:

- **Count at the same level.** Show per-case versus cohort calls, native actors versus scripted prior choices, opportunities versus roots, and observed versus planned outcomes. Compare dollars with dollars; shared-prefix standalone alternatives cannot be summed as actual collection spend.
- **Validate the delivered contract.** Compare declared split/seed ranges with generated assignments and inspect effective requests after adapters. An upstream log containing a field does not prove the model received it. Include nested action/value schemas; define literal equality versus acceptable operational equivalence before grading.
- **Disclose baseline fitting.** A parser fitted after inspecting test templates is a development result. Retain that useful ceiling reference, freeze selection before fresh evaluation, and test on appropriate held-out families before generalizing. Zero new model calls does not mean zero total resource cost.

[Revision evidence and study applications](../../studies/vishesh/external-study-review-2026-10-04/REVISION-2.md) distinguish saved-data checks from source-reported claims.
