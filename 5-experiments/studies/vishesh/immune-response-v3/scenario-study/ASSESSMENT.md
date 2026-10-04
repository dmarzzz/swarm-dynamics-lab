# What the redesigned experiment can tell us

The useful question is no longer whether a programmed rollback restores a programmed ledger. It is whether an agent team can distinguish an actual deployment incompatibility from obsolete recovery advice, select a safe feasible repair, and leave a healthy system alone. Customer checks, not agreement with a preferred policy, determine success.

## What improved

The service catalog now defines relational constraints: protocol compatibility, schema readability, persisted-data safety and customer features. Several recovery bundles are valid. A higher software version is not inherently better. The healthy-system control exposes unnecessary intervention; the migrated-data case makes yesterday's rollback recipe unsafe; registry unavailability tests whether agents can use available local contracts. Every action has a measured result and consumes a finite slot.

The memory treatments use observed revision metadata rather than hidden affected-agent or bad-record lists. Reset clears once and can learn again. Delayed obsolete advice can return. The reference solver uses the same visible contracts and succeeds across all arms: the treatment effect is not embedded in the scoring rule. However, a fully visible three-service catalog is still a constructed exercise; it is not a production workload or a realistic incident distribution.

Model work is limited to consequential choices: three one-time reviews plus six commander actions per episode. Deterministic code handles bookkeeping, the dependency checks and visualization. The explicit solo control tests whether the three reviews earn their extra cost. No claim about benefits of larger swarms or small local models follows from this study.

## Bad decisions and the failed first attempt

A1 recorded 12 episodes with no provider/format failures, but all three treatments damaged an initially healthy system. Reviewers and commander conflated version numbers, feature requirements and schema formats. The revision-check treatment even asserted all checks passed while its recorded data-readability check was false. The full failed run and its trace-backed replay remain public. A valid API response is not a competent decision.

The a2 amendment separates those concepts by name and permits reviewers to conclude no change is needed. An exhaustive check of all 48 case/configuration combinations confirms that this presentation amendment did not change the evaluator's health outcomes. It changes several presentation factors at once, so any behavior difference is not a causal estimate of one wording fix.

## A2 result: safety improved, recovery did not

A2 recorded every assignment, made 108 calls, had zero invalid responses and zero missing usage, and cost USD 0.221422. All three arms preserved the healthy control for six ticks with no deployments or unsafe attempts. It therefore passed the narrow prespecified execution/healthy-control gate.

| Scenario | Retain healthy ticks | Reset | Revision check |
|---|---:|---:|---:|
| Stale advice | 0/6 | 0/6 | 0/6 |
| Migrated data | 0/6 | 5/6 | 0/6 |
| Healthy false alarm | 6/6 | 6/6 | 6/6 |
| Registry partition | 0/6 | 0/6 | 0/6 |

That gate is insufficient to establish recovery competence. In stale_advice, reviewers explicitly described a failing data-readability probe as healthy; the commander repeated that description and waited for all six ticks. In the retained and revision-filtered arms the short justification repeatedly invoked team consensus. These are recorded claims, not proof of the commander's internal causal reasoning. Revision filtering cannot correct a new false conclusion made from current evidence. Do not call A2 a successful immunity demonstration merely because the hub run completed.

## Single commander: better incident recovery, insufficient restraint

The prespecified retain-memory solo control used the same four fixtures and six action slots, with the initial three advisory calls removed. All four episodes and 24 calls completed with no invalid responses or missing usage, costing USD 0.050788. It recovered each incident but failed the healthy-control gate.

| Case | Team retain healthy ticks | Solo retain healthy ticks | Solo unsafe attempts |
|---|---:|---:|---:|
| Stale advice | 0/6 | 5/6 | 0 |
| Migrated data | 0/6 | 5/6 | 0 |
| Healthy false alarm | 6/6 | 3/6 | 1 |
| Registry partition | 0/6 | 5/6 | 0 |

All four solo episodes ended healthy. Final health alone would therefore hide the damage it caused during the healthy control. Removing reviewers reduced calls per episode from nine to six; measured recovery improved in the three incident cases, but healthy-system preservation worsened. This is a small exploratory architecture comparison with single samples, fixed order and provider nondeterminism, not proof that reviewers caused the failures. It does not test a local model or a larger swarm.

The current narrow exercise is solved reliably by the deterministic contract solver. Adding model decisions and advisory consensus did not justify their cost or risk here. The useful engineering recommendation is to keep objective compatibility checking deterministic and demand stronger evidence before delegating recovery decisions or scaling the team. Memory reset and revision filtering alone do not fix false interpretations of current evidence.

## Evidence and cost

Native A1: 12 episodes, 108 calls, USD 0.169049, healthy-control failure. Native A2: 12 episodes, 108 calls, USD 0.221422, narrow execution/healthy-control gate passed but poor incident recovery. Solo A1: four episodes, 24 calls, USD 0.050788, healthy-control failure. Total actual API cost: USD 0.441259; 240 calls; 28 assigned/recorded episodes; zero response/provider failures and zero missing usage. The one USD 8 ledger was not reset. Conservative reservations are USD 1.815067, which are not actual charges and are not refunded automatically.

Both offline suites recorded 192 outcomes each, with zero invalid. They cover four constructed scenarios and presentation variants, not hundreds of independent incidents. Ten scenario regressions pass; the older instrument's 13 regressions remain separate. All 48 configuration checks were identical across the a1→a2 presentation amendment. Final frames, six-tick animations, per-action replays, full JSONL and immutable manifests are retained for successful and failed runs. No further model calls are warranted just to obtain a positive outcome.

## What must precede a stronger claim

1. Require both preservation of a healthy system and recovery on a matched damaged scenario with no misleading memory. The original a2 gate checked only the first; its weakness is now explicit rather than retroactively changed.
2. Separate interpretation errors, harmful proposals, rejected unsafe actions and actual service damage. Cite the exact observed check behind each recommendation. Test that interface on fresh development cases before spending on another qualification.
3. Compare independent proposals with evidence-carrying proposals, where a stated predicate can be checked against the actual tool result. Measure whether checking reduces repeated false assertions and whether its extra queries delay recovery. Do not give an arm oracle repairs.
4. Add independent scenario authorship and a held-out service graph before a confirmatory comparison. Vary topology, feasible repair count, partial observability, registry latency and genuine uncertainty one factor at a time. Names and suffixes are not operational diversity.
5. Only after basic competence holds, compare Haiku with a pinned local model at fixed team size; vary agent count separately. More models repeating an incorrect interpretation is not evidence of greater resilience.

These are gates for a subsequent study, not unperformed work presented as results. No holdout was opened and no run was repeated to make the scientific contrast favorable. Existing failures are part of the conclusion.
