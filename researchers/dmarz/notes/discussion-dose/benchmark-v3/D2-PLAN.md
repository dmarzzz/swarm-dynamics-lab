# D2 proposal: isolate the remaining constraint failures

2026-10-04 UTC. Parent `v3-d1-a1`. **Plan only. Do not launch.** The user requested
the results, analysis and post-mortem in GitHub, followed by a proposed experiment
plan that remains unstarted. No D2 server, hub job, executable manifest or model
call has been created. Q1 and confirmation remain closed.

Read [D1 results](RESULTS-D1.md), [D1 post-mortem](../reviews/v3-d1-a1-post.md),
[original successor design](NEXT-RUN.md), [SETUP](SETUP.md) and the
[experiment setup runbook](../../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md).

## Question and decision

Both models extracted all full-evidence facts correctly yet selected infeasible
options: Haiku 4/6, Sonnet 3/6. Sonnet failed both declared clean gates at 3/6.
Before changing another model or repeating a swarm, determine whether the error
persists when the same decision is presented as a compact canonical fact table,
and whether each individual option's feasibility can be classified correctly.

This is a diagnostic subquestion of [SEC-47](../QUESTION-LINKS.md): baseline
decision errors must be separated from failures caused by corrupted child returns
or merge behavior. It does not test SOC-07 disclosure, discussion dose, a merge
defense or the multi-generation SEC-52 extension. No new formal hypothesis or
duplicate atlas question is needed.

Prediction to examine: explicit complete facts and a small response contract will
reduce the decision failures seen in D1. Alternative outcomes include remaining
atomic constraint errors, correct atomic judgments with faulty option selection,
or model-specific regressions. All are reportable. A success would nominate a
representation/contract repair for later testing, not establish a causal reason
for D1's failures or qualify a swarm.

## Fixed design: 48 calls, if later authorized

Use only open worlds 20001–20006; retain all six, including worlds each model got
right. Two worlds per capacity, total-cost and dependency family. No new tuning
world, confirmation ID or fresh qualification outcome is inspected.

| Probe | Items/model | Both models | Input and response |
|---|---:|---:|---|
| Canonical full decision | 6 | 12 | Public rule/instruction, A/B/C options and all canonical facts; strict `{vote: A/B/C/ABSTAIN}` |
| Single-option feasibility | 18 | 36 | Same rule and only that option's facts; strict `{feasible: boolean}` |
| Total | 24 | **48** | One response per model/item; no repeats or adaptation |

Canonical facts are an explicitly advantaged complete-evidence ceiling, derived
from the audited clean Q0 facts. They contain values, not the expected winner,
feasibility label, attack target, previous model response or evaluator verdict.
Check all values against retained clean records before freezing. Include all
three options in every full-decision probe and every option exactly once in the
atomic set. Atomic labels have six feasible and twelve infeasible options/model;
an always-infeasible policy would achieve 12/18, so accuracy alone needs that baseline.

The compact inputs omit catalogs, finite completion domains, peer report wrappers
and claim-extraction output. This deliberately changes evidence packaging and the
response contract together. **It is not an isolated response-order or wording
experiment.** D1 outputs cannot be pooled with D2 as interchangeable trials, and
an improvement cannot be attributed to any one removed component. The rules,
numeric facts, objective and tie-break stay identical. The six current worlds each
have exactly one feasible option; this does not test multiple-feasible tie-breaking.

## Models, ordering and architecture

Keep D1's exact two model IDs, temperature 0, optional thinking disabled, 2,000
maximum output tokens, 60,000 input-byte ceiling and 120-second request timeout.
Native structured output validates syntax only; an incorrect boolean/vote is a
measured outcome. No fallback, retry or corrective feedback. Verify current account
availability without adding an inference probe.

A single stdlib coordinator builds 24 paired item IDs, freezes their input hashes
and seeded order, and alternates first model 12/12. Each request is an isolated
stateless agent call: one LLM, its supplied private task context, no tools, no
shared memory and no public board. No model sees another request or answer.
This minimal architecture isolates baseline decisions before adding swarm state.

If authorized later, use one dedicated server and exclusive claim, one permanent
dispatch ledger, an fsynced raw-response journal, native provider adapter, independent
watchdog, hub counters and hash-indexed artifact uploads. Reuse the D1 infrastructure
pattern without introducing a large orchestration library. Do not reuse the D1
attempt ID, consumed ledger or retired server. D2 needs its own tested implementation,
source commit, pre-run assessment and immutable public-plan receipt.

The input/output limits, 48-call allocation and one-hour execution bound are fixed;
derive and reserve serialized worst-case cost within the then-current shared $500
pool at admission. D1's reservation is not a new budget grant for this proposal.
Keep actual model tokens/cost and any unknown usage separate from infrastructure
and orchestration costs. No provisioning or budget-consuming action is authorized now.

## Measures and predeclared interpretation

Report all 48 assigned calls: started, terminal, valid, failed, unstarted/unresolved,
returned model, usage completeness, latency, tokens and observed cost. Unknown
usage is not zero; missing/invalid labels do not count as correct. Preserve paired
item scores and world-level results; six worlds are the development clusters.

- Canonical decisions: correct, wrong and abstain out of six/model; feasible choice,
  violations and per-family results. These are fully specified tasks, so abstention
  is unnecessary. Require 6/6 for the diagnostic candidate screen.
- Atomic checks: correct out of 18/model, true-positive 6-way and true-negative
  12-way counts, each world's three-option vector and each family's six checks.
  Require 18/18 for the candidate screen; show the 12/18 trivial baseline.
- Composition: derive a choice from the **observed** atomic booleans using the
  unchanged objective/tie-break; no extra model call. Report no/multiple feasible
  predictions and disagreement with the canonical full-decision answer. An invalid
  atomic response makes that derived decision missing, not an abstention or pass.

If atomic and canonical screens both pass with complete valid usage, propose a
separate test of the candidate contract followed by fresh qualification under the
unchanged readiness thresholds. Do not retroactively promote D1. If atomic checks
pass but canonical selection fails, focus the next proposal on decision composition.
If atomic checks fail, inspect predicate/task/interface semantics before another
model or swarm expansion. If canonical decisions pass but atomic checks fail,
report inconsistency and do not nominate the configuration as repaired.

There are no population confidence intervals, significance claims, automatic
model selection or automatic successors. Q1 IDs 50001–50006, confirmation IDs
30000–30023 and the sidecar namespace remain untouched by this proposal.

## Implementation acceptance and later launch boundary

Before any later launch: read the current post-mortem; commit exact actor text and
schemas; verify the 24 pairs, 12/12 first-model order and 48-call allocation;
exclude all evaluator labels/prior responses from inputs; independently check the
18 option predicates; test always-feasible/always-infeasible/wrong-vote controls,
invalid/missing answers, accounting, timeout preservation and duplicate refusal.
Do not relax schemas or scores in response to a failure. A pre-run assessment must
explain the deliberately bundled representation change and fixed denominators.

Counter/time/cost/invalid/missing-usage series form the live view. Publish a paired
six-world decision table and an 18-option feasibility table, backed by raw hashes.
After execution, if separately authorized, audit all saved responses, verify durable
readback, write results and post-mortem, then retire the dedicated worker. The next
action today is **publish this plan and stop before implementation/dispatch**.
