# Trace review: observed failures, causal limits and revised scope

**Audited all 96 assigned slots across four attempts, not just the failed choices.** There were 49 starts, 48 retained valid answers, one discarded rejected response, and 47 unstarted slots. These counts include setup failure and repeated/repair assignments; they are not independent tasks. [Complete trace index](traces.json), [request/response browser view](traces.html).

## Guidance and evidence boundary

Dmarz's [pipeline lessons, section 6](../../../../../dmarz/notes/pipeline/LESSONS.md) calls for reading the rendered request and returned answer for every qualification miss. Its working-fields discussion and [verify-cost Qwen post-mortem](../../../../../dmarz/notes/verify-cost-qwen/reviews/chain-002-post.md) show how observable intermediate outputs can localize an error without fixing it. They do not establish that adding such fields improves Quorum. The [completion audit](../../../../../dmarz/notes/completion-audit-2026-10-04/README.md) additionally distinguishes saved actor packets and parsed responses from unavailable complete HTTP envelopes, and refuses to infer provider refusal from missing data. Its historical Quorum inventory includes S0; this review adds the later Q1 failures rather than treating the earlier passed screen as current qualification. No newer universal logging change was established beyond these published sources.

Private agentops operator-session collection is a separate workflow. No operator transcripts, owner prompts, credentials or private configuration were collected or copied. Quorum's experimental contract exposes typed choice outputs, not a conversational trace or tool-using agent. The retained local request is frozen and receipt-bound; it is not a provider rendering echo. Hidden reasoning and experimental tool actions were not available and are not invented here.

## Full assigned denominator

| Attempt | Assigned | Started | Valid answer retained | Correct / graded | Other outcomes |
|---|---:|---:|---:|---:|---|
| S0-01 | 32 | 0 | 0 | Not evaluated | Missing output parent; 32 unstarted |
| S0-02 | 32 | 32 | 32 | 29/32 | 2 wrong, 1 DEFER |
| Q1-01 | 16 | 1 | 0 | Not evaluated | Rejected response discarded; 15 unstarted |
| Q1-02 | 16 | 16 | 16 | 0/8 | 8 wrong full-lineage; 8 partial-lineage ungraded |

Every retained answer validates against the historical typed response contract. The joined audit rehashes every request and retains all response fields already in the public experimental artifacts, including scores, usage and latency. Generation IDs are retained for Q1-02 via its separate accounting journal; their absence elsewhere is a retention limit, not evidence that no provider call occurred. Q1-01's original output count, answer and exact charge cannot be recovered from these files. The prior conservative cost bound is not a reconstructed bill.

## What the actual answers establish

**S0 varies on identical inputs.** Fourteen of 16 exact-request pairs agree. For `q65-011`, the two answers are ZERO (scores ZERO .41, ONE .37, DEFER .22) and DEFER (approximately .40, with ONE .32/ZERO .28); the source-MAP target is ONE. For `q80-100`, one answer is correct ZERO (.49), the other wrong ONE (approximately .34 versus .33 for each other choice). All three S0 non-correct responses lie in the copied-report conflict stratum. These are returned choice scores, not calibrated world probabilities or evidence of internal reasoning.

**Q1 confidently makes the wrong graded choices in the retained score sense.** Its eight full-lineage chosen scores span .69–.88, all against root-MAP. All 16 choices, including the ungraded partial cases, match report majority. In the graded cases report majority and misleading prior majority coincide. The peer context includes one correct focal choice and three wrong peer choices; the self context contains one wrong prior. The self instruction also says to reconsider using only the prior-decision slot while the general instruction says to use available evidence. That is an observable ambiguity; its causal effect was not isolated.

**The S0-to-Q1 comparison changes more than prior context.** S0 reports use `bit` and `report_id`; Q1 uses `value` and `id`. Source aliases, report ordering and instructions also change. Consequently 29/32 versus 0/8 cannot identify the effect of prior choices, repetition, wording, schema or ordering separately. We have not diagnosed the exact cognitive cause from the absence of a reasoning trace.

**Known operational causes remain known.** S0-01 failed before calls because the output parent directory did not exist. Q1-01 rejected a response under an erroneous zero-output-token assertion; the repaired Q1-02 retained 39 output tokens for every valid answer. These are implementation failures already repaired, not a reason to retry valid negative Q1-02 results.

## Concrete revisions and offline development

Following the focused research refresh, this cycle constructs **24 explicitly synthetic development bundles**, six per provenance family. Exact mapping and downstream new-dependency-group admission are separate. Same wording does not imply the same acquisition; distinct acquisition IDs do not prove independence. Missing and ambiguous receipts are abstention cases. [Bundles](development-bundles.json), [all baseline outcomes](baseline-results.json).

| Controller | Correct resolved / 15 resolvable | Correct mapping or abstention / 24 | Incorrect admissions | False new-group admissions |
|---|---:|---:|---:|---:|
| Explicit receipt reference | 6 | 15 | 0 | 0 |
| Normalized text plus event/capture metadata | 9 | 18 | 0 | 0 |
| Token Jaccard, score >=.5 and margin >=.2 | 8 | 17 | 0 | 0 |
| Conservative reference/text/synonym hybrid | 15 | 24 | 0 | 0 |

The hybrid is intentionally a strong simple control and uses a dictionary written from these templates. Its result is in-sample software fit, not validated generalization. However, reporting only the weaker controllers would manufacture a model opportunity. This development set has no demonstrated residual headroom and is not an evaluation holdout. Nine new tests verify trace completeness, missingness, repeat disagreements, target isolation, order invariance, ambiguous/missing abstention and common-cause handling.

The [revised conditional proposal](PROPOSAL.md) specifies a decision-changing task, eight qualification plus 24 event-family-separated evaluation calls, strong matched controls, all-assigned metrics, precision limits, exact trace retention, strict stops and unchanged cumulative budget. It first requires a corpus that genuinely defeats the frozen hybrid while remaining answerable from authenticated evidence. That gate is unmet. No model, machine, qualification retry or native adapter was dispatched under this offline review.

## Run-quality and decision

Question/usefulness is improved by mapping evidence rather than paying a model to do solved arithmetic. Scenario realism and generalization remain gaps: four authored families do not replace a provenance corpus. Controls now include the strongest feasible simple controller. Capability remains failed for the historical Q1 contract; the proposed resolver is unqualified. Measurement, missingness, trace coverage and cumulative accounting are explicit; no cohort pooling or native claim is made from software fixtures. Source hashes, deterministic generators, full-case trace view and all baseline outputs provide reproducibility and visualization. No purported statistical precision is gained from 96 repeated/repair slots or 24 dependent development bundles.

**PI decision: keep native arithmetic parked; stop this template-only resolver proposal at the corpus/headroom gate.** Reopen only if development exposes a useful, identifiable residual problem. Direct provisioning authorization does not remove that scientific prerequisite. A materially changed ready scope would then receive one concrete owner decision; no generic spending/researcher approval is requested now.

No new calls or allocation. Cumulative historical API exposure remains **49 calls / $0.065856 reserved**, **$0.00171696 known actual + $0.001344 bounded unknown**. The conditional proposal's 32 calls would reserve $0.043008 additional and reach 81/$0.108864 cumulatively, but none are reserved or spent by this review.
