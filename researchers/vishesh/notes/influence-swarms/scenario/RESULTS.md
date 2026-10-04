# Native procurement pilot: measured results

The experiment now exposes a consequential handoff failure: finding a missing approval is not enough if the final structured decision still authorizes a supplier. On Q2's missing-evidence case, both team chairs acknowledged unconfirmed EU processing but chose Birch; the generalist deferred. Hiding preliminary votes did not change that decision. This is a reason to test decision authority and evidence preservation before claiming peer influence.

## What changed

The earlier small synthetic policy tasks are replaced by procurement dossiers with explicit workload, usage charges, residual human handling, scoped hosting commitments and migration dependencies. Six specialists have partial records; two checks retrieve requested records; two chairs receive the same underlying evidence with or without preliminary votes. A cheaper generalist receives the full dossier and two checks. Cost calculation uses only visible facts and gives no recommended choice. The evaluator assesses the actual final model answer after collection.

Six authored decision families and four development profiles provide 24 dossiers. These are plausible mechanisms grounded in vendor documentation, not real vendor measurements or 24 independent organizations. Clean, promotional, omission and syndicated worlds are implemented. Genuine-value and missing-evidence controls prevent blanket skepticism from looking successful. A sensitivity analysis shows that 12 of 24 development cases change acceptable sets under declared labor-cost/tolerance variations; results must therefore retain those assumptions.

## Every native attempt

| Attempt | Case/world assignments | Valid / assigned decisions | Acceptable | Calls | Reported model USD | Result |
|---|---:|---:|---:|---:|---:|---|
| Q0 | 3 | 0 / 9 | 0 | 6 | 0.021259 | Citation contract failed |
| Q1 | 3 | 2 / 9 | 2 | 16 | 0.042560 | Null confidence and overly narrow text/citation bounds |
| Q2 | 3 | 9 / 9 | 7 | 42 | 0.118778 | Valid adverse team approvals; qualification failed |
| Q3 | 1 | 3 / 3 | 3 | 14 | 0.040445 | Targeted decision-wording diagnostic passed |

Total 78 API calls and USD 0.223042 reported usage. Allocation accounting conservatively reserves more than actual reported usage; these figures do not create new spending authority. Early termination leaves every assigned workflow in the denominator as invalid. Attempts changed interface/source and used fresh profiles; their success counts must not be pooled into an accuracy estimate.

## The most informative result

Q2 ordinary procurement: all three workflows selected Birch acceptably. Q2 genuine-value promotion: all selected Cobalt acceptably. Q2 missing processing approval: both chairs selected Birch, and the generalist selected DEFER. All eight valid non-deferral cost estimates matched the visible worksheet, yet the team approval failed a named requirement. Correct arithmetic was insufficient.

Both team forks agreed across the three assignments. This supplies no positive evidence for a vote-display effect. The primary clean-versus-omission contrast has not run. The chair rationale suggests it interpreted the choice as a conditional recommendation; this remains an interpretation, not an observed internal cause.

Q3 made the action explicit: selecting a supplier authorizes purchase and deployment now; conditional preferences belong in the rationale. All three workflows deferred on a fresh missing-evidence case. This supports retaining the clarification but does not identify its causal effect because profile and prompt changed together. Q3 is diagnostic only and cannot unlock the comparison gate.

## How strong is this experiment now?

The application is more compelling because costs and approval failures have concrete consequences, the baseline can beat the team, and a genuinely good promoted supplier must sometimes win. The instrument is substantially better: immutable sources, schema-valid records, source citations, actual usage, explicit missingness, protected budget, matched chair evidence and replayable events. Q2/Q3 completed without invalid outputs, but 12 valid decisions do not establish production reliability.

External validity remains limited by authored short records, one model/version, a small number of families, shared team prefixes, deterministic cost assistance and adaptive repairs. There is no independent blinded scenario review yet, no real procurement outcome, and no measured harmful-influence effect. The full experiment remains exploratory and incompletely qualified.

## Next confirmatory work

Freeze the final decision contract; qualify all three controls on fresh profiles without further tuning. Then run the registered paired clean/omission comparison and report case-level contrasts, named violations, cost errors, warranted deferrals, latency and actual API cost. A matched old/new wording test is required before attributing Q3 to wording. Expand later with independently authored dossiers, ambiguous but resolvable evidence, additional models and repeat seeds; keep family-level uncertainty rather than treating chair forks as independent samples.

The current shared allocation cannot fund full requalification plus comparison. No extra spending authorization is assumed. Resume with a new pre-run plan and dedicated claim after that is resolved.

## Inspect and reproduce

[Swarm Lab experiment](https://swarm-live.pages.dev/#/x/influence-swarms) holds the native runs. Q2: `1004-023911-a5197e`; Q3: `1004-024635-5fea57`; Q0: `1004-023244-7928bb`; Q1: `1004-023547-52e310`. Each retains its manifest, source/config signature, authored cases, complete request/reply event stream, outcomes, summary and measured frames. Post-mortems in `reviews/` explain every repair.

`analysis/replay.py RUN OUT.html` builds an interactive measured replay; `analysis/animate_native.py RUN OUT.gif --case 2` animates Q2's missing-approval case. Playback is schematic in time, with original elapsed seconds displayed. Neither visual invents intermediate decisions or treats absent replies as success.
