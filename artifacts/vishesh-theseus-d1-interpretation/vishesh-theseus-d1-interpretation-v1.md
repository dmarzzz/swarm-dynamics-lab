# What D1 establishes, and what it does not

D1 identifies a plausible usable executor, not a successful culture experiment. Atomic condition E passed the frozen small-screen gate. The strongest practical finding is that correct execution depends on how we package simultaneous cases. The evidence is too narrow to attribute that difference to a particular internal mechanism or to generalize beyond this model and task family.

## A more honest reading of the headline

| Finding | Supported interpretation | Limitation |
|---|---|---|
| A 40/96 versus B 82/96 | Cleaning the instruction contract improved strict task success | Six A calls used bare action words instead of console commands. A post-hoc alias interpretation gives 83/96 semantic matches, so this does not demonstrate better reasoning. |
| B 82/96 versus C 88/96 | Keyed evidence is a reasonable candidate interface | World changes were +6, +2, -2 correct decisions. It was not uniformly better. |
| C 88/96 versus D 89/96 | Omitting the notebook simplifies execution without an observed large loss | One extra correct decision is weak evidence for a causal notebook effect. |
| D 89/96 versus E 96/96 | Atomic execution merits held-out confirmation | Seven incorrect decisions collapse to three distinct case/family failures. Calls and compute were not matched. |

The atomic arm used eight times as many calls and 2.51 times D's model cost. No response hit the output-token limit. This rules out an observed truncation explanation in D1; it does not establish that batching interfered with attention or memory.

## The seven errors are three failures

The same observations were reused for release, migration-old and migration-new. Two release-case mistakes each recur under all three labels:

- World 611: class B, governing source canary, case at position 8. Canary authorizes release; both distractor sources fail the release rule. D holds instead.
- World 612: class A, governing source canary, case at position 7. Canary authorizes release; both distractor sources fail the release rule. D holds instead.
- World 611 incident: class A, governing source ledger, case at position 5. Ledger's signal is false; both irrelevant signals are true. D selects ledger instead of none.

These patterns are consistent with distractor interference or case-order effects, but do not distinguish them. Source identity, distractor conflict and late position coincide in the release errors. No internal model reasoning is observed.

Giving release and incident one vote each, with the duplicate release contexts removed, gives D **45/48** and E **48/48**. This is a retrospective sensitivity analysis, not a replacement for the frozen 89/96 versus 96/96 result. Even 48 decisions span only three generated worlds and two Boolean task families.

The more important operational metric is missed valid releases: D releases **4 of 6** distinct eligible cases; E releases **6 of 6**. Overall accuracy hides this because only one quarter of release cases should ship. A cautious always-hold policy would score 75% on release while failing the useful action entirely.

## What worked in the instrument

All 144 requests completed, with no provider errors, retries, missing usage or truncated outputs. The source, plan, claim, credentials and spending records are reconciled. The first audit compared decoded per-ID commands with an independently calculated expected command; it did not independently validate the entire response contract.

The additional same-author audit in analysis/reassess_d1.py now checks the complete strict contract directly from archived raw outputs, verifies saved requests and their hashes against the assignment manifest, and reproduces all 480 primary scores with zero mismatches. This is computational agreement, not an independent researcher review. Original outputs and scores are unchanged.

## Improvements before the next run

1. Treat the generated world as the comparison unit; stop counting renamed release contexts as additional evidence.
2. Cover all six ordered class/source mappings. D1 used only three cyclic mappings.
3. Reverse case order within each world, and repeat each exact request twice, so order sensitivity and native response variability can be inspected separately.
4. Keep only D and E. Do not spend the next run re-establishing the legacy format failure or selecting among five interfaces again.
5. Report positive-action recall, false actions, command validity, response presence and strict correctness separately. An invalid command is not a missing API response.
6. Extend the independent scorer to full schema and batch-contract validation. Preserve strict scoring while separately showing collateral losses from an invalid batch.
7. Carry forward the existing ledger, separate actual model cost from infrastructure estimates, and reserve a fixed envelope before dispatch. No hidden qualification probes or retries.

The concrete prospective protocol is [D2-PLAN.md](D2-PLAN.md). No D2 model calls or new infrastructure are authorized by the planning artifact itself.

## Returning to Swarm of Theseus

After execution qualification, the interesting question is selective inheritance: can replacements preserve useful practices while revising obsolete or corrupted ones? Mere access to a persistent note is an insufficient result.

The later culture design should distinguish three mechanisms: adapting an inherited release policy after evidence changes; repairing a confidently wrong inherited incident lesson; and preserving a procedure when a replacement console renames its actions. Each needs frozen founding notes, editable inherited notes, no inheritance, and a single-controller baseline matched for information and resources. Compare all-member context replacement with a no-replacement condition; score novel cases before feedback and adaptation after identical feedback budgets.

Those are conditional design directions, not three new experiments admitted here. Define replacement as loss of the agent's private context, not replacement of model weights. Do not give the true current mapping in the culture probe: that belongs only in the executor ceiling. A useful result would be accurate selective updating after replacement beyond what a static archive or matched controller achieves. D1 supplies no evidence for that claim.
