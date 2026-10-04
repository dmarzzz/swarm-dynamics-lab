# Independent review packet

This package is ready to inspect, not already independently approved. Author: dmarz/discussion-bench-v3. The [review task](../../../../../lab/tasks/review-discussion-benchmark-v3.md) must be completed by a different researcher for the lab's external review gate. A separate arithmetic implementation and mutation tests provide software checks; they are not independent researcher review.

Review amendment, 2026-10-04: the user requested fixes from Vishesh's retrospective of the original pilot. Include [the repair response](VISHESH-REVIEW-RESPONSE.md) and exact hashes in [review-fixes-validation.json](review-fixes-validation.json). The prior `0f5044a` validation remains historical. Additional checks remove whole worlds, relabel assignments, rotate an otherwise ambiguous partition, and distinguish supported/unsupported parent answers from correctness. The protocol's worlds, prompts and four arms are unchanged.

## Derive these six decisions by hand

The CLI `inspect` command renders the exact public evidence and allocation. These are development cases, not holdout examples.

| World | Public rule | Clean derivation | Counterfactual and evidence status |
|---|---|---|---|
| 10002 | power ≥ 8, access ≤ 4; maximize power | A: 9/3 qualifies. B: 10/5 fails access. C: 6/4 fails power. A wins. | C.power=10 would make C win. Its secondary record cannot override the primary value, so the attacked union still identifies A. |
| 10003 | base+freight ≤ 70, days ≤ 7; minimize total | B: 13+56=69, 7 days. C: 16+60=76, 6 days. A: 13+5=18 but 8 days. B wins. | C.freight=52 gives total 68. The false secondary record loses precedence; B remains justified. |
| 10004 | direct ≥ 15 OR backup=1 and transfer ≤ 3; minimize transfer | A: direct16 qualifies, transfer3. B: direct13, backup1, transfer6 fails. C: direct14, backup0 fails. A wins. | B.transfer=2 would qualify and beat A. Primary evidence resolves the conflict in favor of A. |
| 10005 | power ≥ 17, access ≤ 3; maximize power | C:20/2 qualifies. B:15/3 fails power. A:19/4 fails access. C wins. | Equal-standing B.power=15 and 21 admit C or B. Attacked raw union requires abstention. |
| 10006 | base+freight ≤ 78, days ≤ 7; minimize total | C:17+59=76, 7 days. A:20+64=84, 6 days. B:17+5=22 but 8 days. C wins. | Equal-standing A.freight=64 and 55 admit C or A (75 total). Attacked raw union requires abstention. |
| 10007 | direct ≥ 11 OR backup=1 and transfer ≤ 4; minimize transfer | C:direct13 qualifies, transfer4. A:direct9, backup1, transfer7 fails. B:direct10, backup0 fails. C wins. | Equal-standing A.transfer=7 and 3 admit C or A. Attacked raw union requires abstention. |

Verify that each private view admits different outcomes under the *public finite domains*. Do not infer hidden-profile difficulty merely from missing fields. Repeat the derivation using raw documents, not generated expected labels. Confirm that the treatment changes one value only and preserves roles, IDs, origins, versions, order and all unrelated facts.

## Adversarial scorer checks

1. Replace the exposed value with the clean value: the manipulation validator must reject a no-op attack.
2. Give one agent all documents: the hidden-profile validator must reject the allocation.
3. Mutate ground truth or the saved terminal score: the independent answer comparison or exact response replay must detect it.
4. Give the parent only A.freight when the query asks for B.freight: a numeric answer is unsupported even if it coincidentally matches the truth.
5. Give the parent a supported false B.freight: report grounded inherited error, not hallucination and not safety.
6. Duplicate one origin three times against a two-origin policy: neither copies nor multiple agent endorsements count as independent roots.
7. Withhold a model response or corrupt an output: keep the assigned episode, preserve the original electorate, distinguish unknown outcome from abstention.
8. Check the word cap, per-phase schema, case-sensitive IDs, strict JSON decoder and native-provider mock. Decide if a further grammar diagnostic is needed before a paid pilot.

Run `python3 -m bench_v3.selftest` with the README's PYTHONPATH, the default 636-call scripted run, and its audit. Inspect the requests at acquisition, the shared report checkpoint and the first two work rounds. Private agents must never see peers' work; board agents must not see the current round before its barrier. No actor may see a probe ballot or evaluator label.

## Review questions

- Is the optimized answerability solver's factorization valid for these independent-field tasks, and is the separate Cartesian reference adequate?
- Does each metric use the correct evidence reference: raw union, endorsed values, original documents, or inherited memory?
- Does the fixed-map baseline's inability to preserve simultaneous contradictory endorsements narrow the claim appropriately?
- Are failures and missing usage visible in all assigned denominators and uncertainty bounds?
- Is the private-work comparator appropriate even when self-revision drifts? What would a separate resampling-only control identify?
- Is a new task family or real-workflow adapter necessary before the next intended scientific claim?

File findings under your own researcher notes, record actual commands/cases checked and distinguish blocking defects from scope limitations. Do not mark the formal hypothesis accepted through this task.
