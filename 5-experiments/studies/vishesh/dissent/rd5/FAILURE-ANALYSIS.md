# What explains the RD4 accuracy difference

Retrospective saved-data analysis, 2026-10-04. No new native calls, rewritten outcomes or counterfactual model answers. The [reproducible decomposition](analysis/decompose_rd4.py) reads RD4 records and accounts for all 288 decisions in the three checking arms, including all 26 noncorrect outcomes. Input hashes and row-level evidence are in [the audit JSON](analysis/rd4-failure-decomposition.json).

**The observed one-point gap is a specific admission failure, not an unexplained aggregate.** Original and symmetric both missed a recovery that always-check handled. The transport-affected trajectory contributes four noncorrect opportunities to each checking arm. It does not numerically create the observed gap, but its unobserved counterfactual answers still limit a failure-free performance ranking.

| Noncorrect outcome group | Original gate | Symmetric gate | Always-check |
| --- | ---: | ---: | ---: |
| Transport failures and their budget descendants | 4 | 4 | 4 |
| Unresolved alarm interpretation and its budget descendants | 4 | 3 | 4 |
| Fresh recovery not admitted | 1 | 1 | 0 |
| Initial required-build challenge deferred | 0 | 1 | 0 |
| Total noncorrect / 96 | 9 | 9 | 8 |
| Correct / 96 | 87 | 87 | 88 |

Groups are a descriptive attribution from observed traces, not estimates of how many points a proposed repair will recover. A changed policy can create new states, inputs and errors. Four roots account for the checking arms' noncorrect outcomes, so broad behavior claims would be especially weak.

## One genuine admission miss

Alarm root `294ed0f1b3dc` correctly stopped, retained the stop across repeats, then received a fresh tick-4 reading of 20 inside the allowed interval 10–30. The old majority records were from tick 0. Both gate arms chose KEEP, retaining HOLD; always-check inspected and chose PROCEED. This is the only correctness difference between original-gate and always-check.

The original gate assigned KEEP 0.54 and CHECK 0.42; symmetric assigned KEEP 0.61 and CHECK 0.35. These are saved choice scores, not calibrated error probabilities. The stronger recovery wording did not change the choice. The proposed repair is to make eligibility explicit and mechanical, then test allocation separately—not to fit a threshold to this single error.

## A shared interpretation failure with a downstream cost

Alarm root `6dd7a1db979b` supplied a current verifier receipt saying that 40 is not inside the allowed interval. Despite the explicit numeric requirement, all checking arms returned DEFER. The same challenge was checked again, yielding another DEFER and spending the second check. When genuinely new evidence later permitted recovery, the check budget was exhausted.

This creates four noncorrect opportunities in original and always-check, but three in symmetric. At the alias epoch, symmetric selected KEEP and retained the old HOLD, which happened to be the correct action. There was no fresh verification establishing a new resolution at that epoch. That one point should not be described as stronger interpretation or a successful recovery mechanism.

This motivates two separate changes: clearer actor-visible evidence representation, and a ledger that remembers an unresolved interpretation without repeatedly purchasing the same observation. It also motivates making current authorization distinct from historical last-known action. A corrected state contract could remove the symmetric arm's fortunate point while being more faithful about uncertainty.

## A new admission error offset the symmetric arm's point

Build root `a1424d89c5a1` had a relevant required-test contradiction and an available verifier. Original and always-check inspected and correctly held the release. Symmetric deferred instead of checking at the initial epoch, then handled the remaining epochs correctly. Its saved DEFER score was 0.41, CHECK 0.31 and KEEP 0.28. No calibration or reliable ambiguity threshold follows from these values.

Thus symmetric versus always-check is exactly three differing rows: missed recovery −1, retained old HOLD +1, initial build DEFER −1. The result is −1 overall. Symmetric versus original is +1/−1 and ties. Native admission adds a fallible decision before the useful check; the small successor will retain a structural baseline rather than assume a better wording fixes this.

## The operational uncertainty remains real

Transport root `13e56b8640a7` produced four direct failures in each learned gate. Always-check instead recorded two interpreter transport failures after spending checks, then two budget-exhausted decisions. Both mechanisms produce four noncorrect rows. The saved physical-check charge must not be refunded merely because the model failed later.

The existing sensitivity bounds remain: original 87–91, symmetric 87–91, always-check 88–92 if each affected row can be correct or incorrect. The one-point observed gap is located in unaffected data, but a hypothetical successful transport path could alter the overall ranking. We cannot claim that repairing the network will equalize or improve model accuracy by a known amount. The C2 probe addressed readiness and completed the remaining work; future fault tests must cover the race between a passed probe and dispatch.

## What to carry into the next plan

Retain the successful alias identity and persistent resolved-memory repairs: 59 native retained closures used zero extra checks/calls and preserved the correct action. Prioritize observation/inference accounting, explicit unresolved status, mechanical eligibility and paired representation qualification. Test repeated-uncertainty memory before adding a reserve, and evaluate the reserve against useful early checking. Keep all fixed denominators, transport descendants and time costs visible.

[Improvement contracts](IMPROVEMENTS.md) specify what would close each issue. [Prospective plan](PLAN.md) defines the next bounded comparison. None of the proposed fixes is claimed to have recovered an RD4 point.
