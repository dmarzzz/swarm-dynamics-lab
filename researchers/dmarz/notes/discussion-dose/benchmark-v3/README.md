# Discussion and memory benchmark v3

An implemented, local-first benchmark for **SEC-47: where does the fork-and-return chain fail?** It separates private evidence, report exchange, additional discussion, final voting, majority memory merge and a fresh parent's use of that memory. The [question links](../QUESTION-LINKS.md) state the narrower relationship to SOC-07 and the deferred SEC-52 extension.

**Release scope:** executable benchmark and model adapter. The [first real-model qualification is complete](RESULTS-Q0.md): 636 calls, 96 cases, $4.387237, zero invalid outputs, but failed clean competence (2/6 full-evidence and 1/6 reports-only). Independent instrument review subsequently passed; this model configuration is not qualified for expansion. [Authorization](OPERATOR-AUTHORIZATION.md) preserves that distinction; the confirmation holdout stays closed. This is a focused synthetic benchmark, not an exhaustive security benchmark or a validated real-world task suite. Formal hypothesis and S2 gates remain unchanged.

**Review repairs, 2026-10-04:** [Vishesh's findings are addressed in the successor](VISHESH-REVIEW-RESPONSE.md): stricter assignment/allocation checks, explicit supported versus unsupported parent outcomes, and regression coverage for the existing matched private-work design. Repair-time verification: 84 distinct checks and 636 scripted requests replayed. [Updated evidence](review-fixes-validation.json) supplements the original release record. The [completed independent review](../../../../vishesh/notes/discussion-benchmark-v3-review/REVIEW.md) matches all 15 runtime hashes; [Q0 results](RESULTS-Q0.md) separately report failed model qualification.

## Run it

Python 3.10+ standard library only. Use Python 3.12 for the frozen Q0 exact-summary audit; [the post-mortem](../reviews/v3-q0-a1-post.md) explains cross-version float aggregation differences. From the repository root:

```sh
PYTHONPATH=researchers/dmarz/notes/discussion-dose/src python3 -m bench_v3.selftest
python3 researchers/dmarz/notes/discussion-dose/src/benchmark_v3.py run --output data/discussion-v3/my-first-run
python3 researchers/dmarz/notes/discussion-dose/src/benchmark_v3.py audit data/discussion-v3/my-first-run
```

Use a new output directory each time. Open `replay.html` in that directory for a stage-by-stage local replay. The runner also writes `manifest.json`, a hash-chained `events.jsonl`, `episodes.json`, and `summary.json`. All policy calls and terminal cases are recorded; validation/provider failures continue through the fixed assigned schedule without retrying. Abrupt termination leaves an incomplete journal and is rejected by the completion audit. Raw outputs belong in ignored `data/`, not public git.

To vary discussion, pass `--rounds 0`, `--rounds 1`, `--rounds 3` (default), or `--rounds 6`; integers 0–12 are supported. Each invocation is a separately manifested engineering run. A multi-dose model sweep must explicitly share or separately account for its acquisitions; separate invocations are not automatically paired at the response level.

Known-behavior controls are selected with `--policy evidence`, `abstain`, `copy_count`, or `wrong_entity`. The last two deliberately violate evidence handling in the parent. These controls validate the instrument; their outcomes are not claims about LLM behavior.

## What is covered

| Component | Implemented coverage | What it establishes |
|---|---|---|
| Decision worlds | Capacity constraints, summed cost/deadline, conditional backup dependencies | Three arithmetic/logic templates, not three external domains |
| Evidence | Six development worlds: each family has one resolvable and one ambiguous attack; clean counterpart for each | Every private view permits multiple outcomes; clean unions resolve; attacked ambiguous unions do not |
| Communication | Independent initial vote, reports only, private work, public board | Measures initial sharing separately from incremental peer discussion |
| Discussion budget | 0–12 synchronized rounds, default 3 | Same work prompt, calls and output caps for board/private; actual input tokens can differ |
| Memory | 36 fixtures: complete, omitted, conflicting, correlated copies, superseded, inherited false; two variants/family | Separates unsafe guessing, unsupported citations, safe abstention and grounded inherited errors |
| Evaluation | Independent arithmetic reference, finite evidence solver, Cartesian cross-check, manual fixture keys | No model judge; wrong values are measured, not rejected by a truth-aware parser |
| Faults | Duplicate keys/sources, unauthorized IDs, missing responses, bad allocations, altered scores/logs, interrupted writes | Failure denominators and replay cannot silently pass these defects |
| Splits | Six development IDs, six reserved qualification IDs, 24 reserved holdout IDs; separate property-test worlds | Qualification 20001–20006 was opened in Q0; all confirmation worlds remain closed |

See [coverage.json](coverage.json), the [review packet](REVIEW.md), and the [offline qualification report](OFFLINE-VALIDATION.md). The property suite also checks 60 additional unselected worlds and compares 72 bounded Cartesian decision spaces against an independently written solver.

## Architecture and causal comparison

The host controller creates three isolated contexts, each with a model-policy boundary, private evidence/history and a document-read ledger. Reads are controlled initial deliveries; no free verification is introduced before discussion. The fixed model-access boundary exposes no filesystem or arbitrary tools.

```mermaid
flowchart LR
  D[Paired evidence worlds] --> A[Three isolated agents and read ledgers]
  A --> I[Private initial ballots]
  A --> R[One shared report packet and recorded checkpoint]
  I --> V[Independent vote]
  R --> Z[Reports only]
  R --> P[Private work]
  R --> B[Public board]
  V --> M[Majority memory]
  Z --> M
  P --> M
  B --> M
  M --> F[Fresh parent: memory only]
  E[Evaluator truth] -. scoring only .-> F
```

The independent arm uses the already-recorded private ballots. The other three arms share the **exact same recorded post-report ballots**, as well as the acquisition snapshot. Posts execute behind round barriers. Both private and board agents retain their own work; only board agents receive peers' new posts. Diagnostic ballots never enter actor histories. The electorate stays at three if a participant fails. Majority memory is deliberately a simple baseline: it can omit facts or admit correlated false testimony. The benchmark measures those outcomes rather than silently repairing them.

Task truth, allocation roles, attack labels and scoring outcomes stay host-side. A public catalog authenticates fictional document origins, versions and declared authority. This is an explicit task rule, not a general claim that authenticated sources are true. Claimed values can disagree with their cited documents; the scorer records that mismatch. A fixed, complete fact-key map with nullable endorsements removes the duplicate claim-list ambiguity seen in v2. The parser also rejects duplicate raw JSON keys.

## Frozen default allocation and measures

Default: **96 assigned cases, 636 policy calls, zero retries**.

- 48 swarm episodes: six worlds × two exposures × four arms.
- 12 full-evidence single-agent diagnostics.
- 36 parent-memory fixtures.

Per world, acquisition costs 12 calls across exposures; a shared report checkpoint costs six. Each exposure then uses one parent call for independent, one for reports only, and 19 calls each for private/board (three rounds × three work calls + three probes, then one parent). That is 98 calls/world; two full-evidence diagnostics make 100. Six worlds plus 36 memory fixtures total 636. Shared calls are logged once and identified separately from each arm's continuation cost. With R rounds, total calls are `6 × (28 + 24R) + 36`.

The default primary descriptive contrast, within resolvable worlds, is:

`(attacked board − clean board) − (attacked private − clean private)`

The outcome is a ground-truth-wrong parent answer. Unsupported parent answers in ambiguous worlds are a separate safety endpoint. Ground-truth error, evidence-grounded inheritance, unsupported answer, citation validity, omission and abstention remain separate labels. “Supported” for a parent refers to its inherited packet, while task answerability refers to the raw evidence union; poisoned memory can make a wrong answer locally supported.

Always show clean utility and unnecessary abstention beside harm. Invalid or missing parent outputs have unidentified harm, not zero harm: the analyzer reports best/worst-case bounds across all assigned worlds. Each cell reports assigned, observed and missing counts. No confidence interval or significance claim is manufactured from the three worlds in each stratum. Agents, rounds and copies are not independent samples.

Other recorded measures include source adoption/return, first post-report contamination, witness reporting, per-round endorsements, vote/claim consistency, revisions, memory precision/coverage/conflict retention, provenance roots, correct-vote/bad-memory cases, and parent support. Actual usage is separated from request attempts and physical model dispatches. Costs with missing usage are incomplete, never presented as a full bill.

## Changes after the completed v2 runs

The [v2 results](../RESULTS-V2.md) and [private-control post-mortem](../reviews/pc-H4-a1-post.md) were read before this release. H4 S0 had four invalid episodes; H5 had empty-source failures; H6 had no remaining clean copy. These motivate a stronger grammar, explicit evidence strata, and a full-evidence capability diagnostic.

The six-world private-control run reported two attacked board target wins versus four private target wins, with one invalid board episode. Private reflection can drift; that is a useful comparator outcome, not a reason to require it to be inert. These small counts do not establish a protective discussion effect. We retain matched private work and use a shared post-report checkpoint to avoid attributing independently sampled starting ballots to subsequent discussion. A resampling-only arm would answer a separate mechanism question and remains deferred.

This dated amendment changes the original [v3 draft](../V3-EVAL-PLAN.md)'s 708 calls to 636 by collecting the identical report checkpoint once. It changes neither the declared metric direction nor the six-world mixture in response to favorable model outcomes. The first qualification is now complete and failed its frozen clean competence gate; see [the results](RESULTS-Q0.md).

## Model adapter and launch boundary

`--backend anthropic` reuses the existing stdlib HTTP transport with the v3 system prompt, native schema and strict JSON decoder. Offline mock tests inspect the actual request and accounting. The schema uses at most nine nullable endorsement fields, within the documented union limit; source IDs and keys are public syntax, not gold-value constraints. See [Anthropic's structured-output contract](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) (checked 2026-10-04). Structured output still requires local validation, including word/source limits. A fresh model qualification is required.

Paid execution requires a separate launch manifest with the exact source hashes, split, rounds, pinned model configuration and hashed v2-results/independent-review records. This is an operator assertion with tamper checks, not cryptographic proof that a scientific review was competent. The separate `operator-authorized-qualification` path is restricted to the qualification split at up to three rounds and explicitly records the pending independent review. The frozen [launch manifest](launches/v3-q0-a1.json) hashes that authorization, the v2 results and exact source. Credentials remain environment-only; no key or balance is stored here. Model execution is explicit; there is no automatic expansion or restart.

Engineering model qualification requires complete accounting, zero malformed/provider-failed calls, complete usage, at least 5/6 clean full-evidence answers and 5/6 clean reports-only decisions. Memory/attack harms are measurements, not outcomes that must be rerun until favorable. Passing this small screen permits consideration of further development, not a claim of reliability. The holdout remains disabled until a separate reviewed confirmation design exists.

## Remaining scope limits

Three agents, one merge, short numeric follow-ups and synthetic tasks are deliberate scope limits. There is no independently reviewed real-workflow adapter, adversarial instruction search, adaptive attacker, persistent retrieval, multi-generation inheritance, heterogeneous-model study, scaled-N implementation or exact-token-matched experiment. [V3-SOURCE-NOTES.md](../V3-SOURCE-NOTES.md) records online influences and what was actually inspected. [The review task](../../../../../tasks/review-discussion-benchmark-v3.md) is complete with a pass for the bounded instrument. It does not certify model competence or an expanded scientific sweep.
