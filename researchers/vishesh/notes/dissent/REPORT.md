# The Right Dissenter: evidence gates can block recovery

**The tested gate saved checks but did not improve decisions.** In 52 synthetic root cases with 60 decision opportunities per policy, Jev evidence-gated dissent got 24 correct on time, compared with 30 for always-check and 24 for majority alone. It saved nine checks versus always-check, but used almost twice as many logical model calls. This bounded exploratory result does not support deploying the current gate.

[Public comparison and replay](https://swarm-live.pages.dev/#/r/right-dissenter%2Fs1-a1) · [Experimental plan](LIVE-PLAN.md) · [Prospective clarification amendment](Q1-PLAN.md) · [Sources and X threads](SOURCES.md).

## Results

| Policy | Correct / 60 | Checks | Harmful reversals / 24 initially correct | Logical model calls |
|---|---:|---:|---:|---:|
| Majority | 24 | 0 | 0 | 0 |
| Blind veto | 28 | 0 | 20 | 0 |
| Always-check | 30 | 40 | 4 | 32 |
| Evidence gate | 24 | 31 | 4 | 63 |
| Fixed 50% random allocation | 28 | 19 | 2 | 15 |
| Pooled evidence | 32 | 0 | 15 | 60 |
| Exact grammar rule | 32 | 40 | 4 | 0 |

All 420 opportunities remain in the denominators. Abstention is not correct completion; harmful reversals count wrong completed actions and exclude abstentions. Always-check and evidence-gate each deferred on ten opportunities, including two failed calls. The random policy's allocation is fixed at 26/52 roots, not matched to the gate's realized expense. Checks are simulated observations; model calls are a separate resource.

The exact grammar rule and pooled evidence tie in accuracy but differ sharply in harmful reversals. Blind veto corrects 24 initially wrong decisions while corrupting 20 initially right ones. Reporting only corrections would hide that damage. The fixed random arm beats the evidence gate on this sample with fewer checks and calls; repeated templates and small numbers prevent a broad dominance claim.

## What makes the result interesting

The gate's six lost decisions versus always-check have two mechanisms. Four follow semantically unsupported objections: the objection requests reversal while its own cited evidence agrees with the majority. The gate usually rejects these, saving seven checks across eight such cases. But when the majority happens to be wrong, always-check can still discover the truth through a lucky extra measurement. Evidence-consistent admission sacrifices some of those rescues.

The other two losses expose a more useful research question: **does a dissenter have the right to announce recovery?** The gate correctly withdrew all four false alarms and suppressed their four unchanged repetitions. When genuinely new evidence arrived, it reopened correctly for both worsening cases but rejected both favorable changes and stayed on HOLD. Always-check handled all 12 temporal opportunities correctly; the gate handled ten. A mechanism that can stop a group also needs a tested path to restart it.

This is an observed action pattern, not access to the model's reasoning. Directional recovery tests, an explicit transition rule, and a separate right to obtain evidence versus right to change action are promising next design questions. They are proposals; no redesigned policy is credited with these results.

## Qualification and validation history

| Attempt | Outcome | Interpretation |
|---|---|---|
| Q0 | 12/18 correct, all 18 valid | Failed clean-task qualification; positive build/alarm reports elicited DEFER |
| Q1 | Generic 11/18; clarified 18/18; uncertainty controls 6/6 | Explicit sufficient-evidence wording qualified this synthetic grammar before S1 |
| S1 | 420/420 decisions; 129/132 unique calls valid | Adverse gate comparison; three rejected responses retained |
| D1 | All nine responses valid; six fresh controls correct | Three exact failing inputs did not reproduce; historical rejection subtype remains unknown |

Q1 used matched packets with identical answer order and changed only task instructions. Seven pairs improved and none worsened. Fresh IDs do not create new semantic templates. Clean qualification is not evidence of good dissent admission.

S1's three validation rejections affected six policy decisions through deliberately shared saved responses. The same two checked failures affected both always-check and evidence-gate on the same cases, so their six-decision paired gap is invariant to any common replacement answer for those two failures. Absolute accuracies retain the failures; D1 answers are never substituted. Logging now exposes safe fixed validation predicates without relaxing the response contract.

## Evidence and limits

[All S1 requests](results/s1-a1/calls.json), [all assigned outcomes](results/s1-a1/records.json), [summary](results/s1-a1/summary.json), and [reconciled analysis](results/s1-a1/analysis.json) are retained. Replaying saved decisions and failures exactly reproduced all 420 records without provider calls. The analysis reports each domain and condition, temporal events, paired contrasts, counterfactual API usage and sensitivity to the published illustrative loss weights. Those weights are preferences, not measured operational utilities.

Votes and challenges were scripted, evidence ancestry fixed, and equal inputs shared one response within S1. There were 52 root cases, not 420 independent experiments. No population-level significance or operational reliability claim is supported. The deterministic parser's success on this grammar limits the case for using a learned judge. Formal prior-art and independent research review are incomplete; S2 remains unopened.

The research hub already contains the relevant papers and map-demo X threads. [SOURCES.md](SOURCES.md) links their canonical entries and states reading limits, including the blocked X refresh. Biological inhibition motivates the construction but does not establish equivalence to honeybee decision mechanisms.

## Budget, machines and process compliance

The owner approved $2 total. Across Q0, Q1, S1 and D1, the ledger contains 201 unique calls: 198 validated and three failed. Settled recorded API usage is $0.00739767; retaining full uncertain reservations raises the committed amount to $0.01142967. No retries reset the allowance.

I initially provisioned a host with the local default DigitalOcean credential without proving it belonged to Dmarz's account. That was an allocation error. The host and its dedicated resources were deleted, all other droplets were verified unchanged, and the Q0 evidence was preserved. Estimated compute for that temporary host was $0.011643; its actual invoice is not yet available. This failure is documented in Q1-SETUP-POST.md and CLEANUP.json.

The experiment then borrowed the newly released, idle sim-shadow machine from Dmarz's established fleet under an exclusive claim. Q1, S1 and D1 ran there with actual-host, source, public-plan and claim checks. No replacement droplet was purchased. All artifacts were read back and hash-verified. Workers, relay and tunnel are stopped; the existing host is released and preserved. Public-plan compliance does not erase the earlier allocation failure. SETUP.md's retrospective creation for Q0 is also labelled explicitly.

## Reproduction and closeout

Every run's configuration records source, model, assignments, immutable plan and per-run TLDR. [Q0 post-mortem](reviews/Q0-A1-POST.md), [Q1 post-mortem](reviews/Q1-A1-POST.md), [S1 post-mortem](reviews/S1-A1-POST.md), [D1 post-mortem](reviews/D1-A1-POST.md), and [setup record](SETUP.md) preserve the complete sequence. Fifty-three software checks pass. The 1800px policy figure and 23-second measured replay show actual saved events, with evaluator truth labelled and excluded from model inputs.

This exploratory cycle is complete. It leaves a concrete negative result for the current gate and a sharper next question about recovery after dissent, without retuning the comparison until it looks favorable.
