# What a good experimental run establishes

Use this rubric in every [post-mortem](templates/post-mortem.md) and before proposing the next run. A good run answers a defined question with interpretable evidence, complete accounting and reproducible records. It can return a null, adverse or inconclusive result. A favorable effect does not compensate for a broken instrument.

Assess the declared scope: a diagnostic need not support population inference, and a scripted mechanism test need not demonstrate model competence. State that limit rather than silently awarding a broader pass. Assessment is the owning agent's scientific work; automatically generated counts cannot perform it.

## Record evidence rather than a score

Each dimension records `dimension`, `status`, `finding` and `evidence` references. In the structured review, an evidence reference contains a path and its SHA-256. Use one of:

| Status | Meaning |
|---|---|
| `pass` | Relevant acceptance evidence supports the stated requirement within this run's scope. At least one evidence reference is required. |
| `gap` | Evidence demonstrates a missing requirement or a defect. Name the affected inference or next stage. |
| `unknown` | Available records do not resolve the requirement. Missing evidence is not a pass or a numerical zero. |
| `not_applicable` | The requirement does not apply to this scoped question; explain why in `finding`. |

Every `gap` or `unknown` needs a `next_action` and an `acceptance_check`. Distinguish directly observed facts, plausible causes and verified causes. Record the assessor, date, attempt and evidence revision. A count of green cells is not an experiment-quality score or launch authorization. Keep the existing [evidence confidence and independent sample-size metadata](../../experiments/EVIDENCE-METADATA.md) current after analysis; these dimension checks complement those fields rather than replacing them.

## Eleven checks

| Dimension | What a pass must establish | Typical gap or unknown |
|---|---|---|
| `question` | A primary question, empirical unknown, outcome-dependent decision, contrast and claim boundary are explicit; explain why existing evidence or a simpler method is insufficient. | Several mechanisms bundled into one headline; an observed result replaces the original prediction. |
| `scenarios` | Tasks exercise the proposed mechanism with meaningful challenge, useful baselines, relevant strata and disclosed realism limits. | Ceiling/floor tasks, copied semantic templates, artificial costs presented as real, or difficulty created only by unusable instructions. |
| `controls` | Manipulation occurred; clean and adverse controls discriminate; comparator information/resources support the estimand. For collective claims, isolate the relevant interaction from re-evaluation/resampling and use a strong simple-controller reference. | More evidence/compute changes with treatment, impossible baseline, ineffective intervention, or hidden oracle assistance. |
| `capability` | Required agents, tools and interfaces meet the prespecified clean-task and response-contract criteria on appropriate qualification inputs. | Schema validity mistaken for competence; healthy restraint without repair ability; diagnostic success used as broad qualification. |
| `measurement` | Endpoint, denominator, scorer and uncertainty match the question; saved decisions support recomputation and relevant sensitivity checks. | Wrong truth/version, label leakage, invalid-versus-wrong confusion, selective exclusions or an interval interpreted beyond its sample. |
| `sample_size` | Independent units, pairing/clustering, allocation and missingness are explicit; sample size fits a precision/effect objective or a candid feasibility scope. | Agent/call/branch counts treated as independent n; arbitrary enlargement; rare failures absent from a tiny pilot. |
| `agent_context` | Effective model/prompt/tool/context and memory initialization match the specification; changes, resets and lineage are recorded. | Environment-selected model drift, undeclared fallback, cross-arm memory, uncontrolled truncation or context leakage. |
| `data_integrity` | Every assignment reconciles through started, terminal, graded and analyzed; failed/partial attempts, raw decisions and call receipts remain recoverable. | Missing cells disappear, duplicate attempts enter the denominator, uncertain calls are retried invisibly, or reporting changes outcomes. |
| `resources` | Actual and reserved cost, calls, tokens, runtime, concurrency and allocations remain within cumulative authority; uncertain exposure is retained. | New ledger treated as new funds, supporting-agent costs omitted, claimed caps unenforced, or account identity unverified. |
| `reproducibility` | Source/configuration/input/runtime provenance and exact commands reconstruct the instrument; retained evidence replays within its stated boundary. | Unresolvable hashes, overwritten outputs, unpinned effective dependencies, or identical seeds claimed to guarantee hosted answers. |
| `visualization` | Tables/plots/replays agree with recorded evidence, expose uncertainty and missingness, and separate scripted from native outcomes. | Selected frames imply complete history, missing values appear as zero, denominators vanish, or decoration suggests an unmeasured mechanism. |

Use small reference calculations, semantic fault tests and artifact replay to resolve instrument questions before further collection. Trace initial evidence through interpretation, advice, action and outcome across the full eligible cohort; label saved-data diagnosis retrospective. Inspect retained effective requests and visible answers for every qualification miss, report per-artifact coverage, locate the first observable divergence and retain alternative explanations using the [native trace review](RUN-REVIEW.md#review-the-native-traces-before-choosing-a-repair). Missing traces and uninspected cases cannot support a verified-cause claim. For memory interventions, separate resistance, persistence, recovery and legitimate knowledge lost. State native actor counts separately from programmed population size. No new service or universal test count is required. Independent authorship or replication can strengthen evidence, but do not claim it for same-agent checks.

## Translate the review into a decision

Choose `advance`, `repair`, `diagnostic`, `complete_valid_result` or `blocked`. Explain which observations justify that decision and which claims remain unsupported. `advance` still requires the next stage's admission. Only `advance`, `repair` and `diagnostic` propose a successor through the operations workflow; a completed result or unresolved external blocker does not queue another run.

A valid null or worse intervention may earn passes on every relevant design dimension and finish as `complete_valid_result`. A wide interval can leave the scientific question unresolved without implying an instrument defect; propose additional sampling only if its expected precision and decision value justify the cost. Never increase n or repair scenarios merely to obtain a preferred effect.

The next session must assess earlier suggestions against this rubric, accepting, revising or rejecting them with reasons. A suggested fix is not a verified cause, and copying the preceding recommendation is not a new assessment. Turn selected work into the [next-run plan](templates/next-run-plan.md), with a specific design, sample allocation, scenarios, telemetry, analysis, resource envelope and acceptance checks. Follow the [owner approval and closeout workflow](RUN-REVIEW.md).

## Lessons from the market and decision studies

[The pinned Dmarz transfer review](../../researchers/vishesh/notes/dmarz-methods-transfer-2026-10-04/README.md) supplies concrete checks for the existing dimensions, not new universal thresholds:

| Check | What to record | Avoid |
|---|---|---|
| Resource conservation (`controls`) | Which capacities, evidence, checks and compute stay fixed when identities/roles change; residual topology changes | Calling an identity effect pure when free links or information also change |
| Evidence bottleneck (`measurement`) | Truth/evidence available → admitted → interpreted → action → verified task outcome; scripted/native label at each step | Spending on a stronger synthesizer when the needed evidence never arrives |
| Semantic qualification (`capability`) | Correct action and component diagnostics on the hardest necessary step, separately from parse success | Valid JSON or a plausible written calculation counted as competence |
| Informative task (`scenarios`) | Development-selected challenge range; prospective floor/ceiling/futility rule for costly escalation | Lowering the clean competence gate or redesigning after outcomes to obtain an effect |
| Harm and service (`measurement`) | Absolute correct/wrong/abstain levels, legitimate work retained, and paired changes | Smaller harm slope presented as safer when absolute harm is worse |
| Variability and n (`sample_size`) | Independent world/task roots; nested same-condition repeats; model/config cohorts separate | Many identities/calls or a degenerate bootstrap interval presented as broad certainty |

Use safe allowlisted failure categories and numeric cost/throughput telemetry. Provider outages remain operational outcomes; preserve uncertain dispatch exposure. A copied retry policy or new subledger must never grant extra calls, erase costs or expose arbitrary provider error bodies.

## Prospective claim scope

Apply [claim-scoping guidance](CLAIM-SCOPE.md) before implementation: identify the intended inference, independent units, comparator and untested boundaries. If the useful claim needs broader evidence, improve the design prospectively; do not rely on a post-hoc caveat.

## Evaluate the cases as well as the run

Use [TEST-CASE-QUALITY.md](TEST-CASE-QUALITY.md) to assess answerability, labels, leakage, causal contrasts, realism, strong comparisons, independent units and holdout integrity. Record evidence and critical failures, not a blanket average score. Case readiness, native capability and run admission are separate determinations.
