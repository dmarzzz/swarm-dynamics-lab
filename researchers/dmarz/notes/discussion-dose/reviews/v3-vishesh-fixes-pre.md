# Pre-run assessment: v3 review repairs

- Owner/stage: dmarz/discussion-bench-v3; offline instrument regression, 2026-10-04 UTC.
- Parent attempt: [v3 offline release](v3-offline-post.md), runtime `0f5044a`.
- Status: diagnostic-only. The user requested implementation of Vishesh's fixes. No model execution, fleet deployment or new scientific result is authorized by this attempt.
- Decision: whether the v3 successor satisfies the acceptance checks in [Vishesh's retrospective review](../../../../vishesh/notes/independent-reviews-2026-10-04/discussion-dose.md). This is an author response; Shadow's independent review remains separate.

## Design and changes

Keep the existing six development worlds, 36 memory fixtures, three agents, independent/reports/private/board arms, three rounds, exact shared report checkpoint and 636-call allocation. Do not generate reserved qualification or holdout worlds. Board/private calls and output ceilings match; input tokens need not match. Diagnostic ballots remain outside actor histories. Ground truth remains evaluator-only.

| Finding | Implementation or retained control | Acceptance check |
|---|---|---|
| Entire world absent from standalone analysis | Require manifest assignment metadata in summaries and assignment ledger in contrasts; validate rows before aggregation | Delete all ten records of one world: retain 96 assigned cases, report ten missing, keep three primary worlds and bounds; all missing gives [-2,2] |
| Relabeled or duplicated records | Compare all assignment fields and reject unexpected grouping fields | Duplicate, unassigned, wrong-arm/stratum/world/type rows raise before aggregation |
| Allocation changed | Check full plan before dispatch and reproduce frozen partition/roles | All-document, rotated-but-still-ambiguous partition, duplicate/missing assignment and bad final world all fail with zero provider calls |
| Lucky parent guesses hide missing evidence | Add required-key coverage and explicit supported, unsupported-correct and unsupported-wrong outcomes | Correct guess from wrong-entity memory is unsupported; inherited false value is supported and wrong; invalid is not abstention |
| Discussion versus extra private work | Retain matched private-work arm, exact starting checkpoints, clean full-evidence diagnostics and initial contamination measurements | Match phase/agent/round schedules; inspect checkpoint reuse and visibility barriers |

## Frozen execution plan

Commit code and this assessment before the separate full saved-output check. The run manifest freezes source hashes. Run the extended v3 selftest and existing v1/v2 regression suite, then:

```sh
python3 researchers/dmarz/notes/discussion-dose/src/benchmark_v3.py run --output data/discussion-v3/vishesh-fixes-a1
python3 researchers/dmarz/notes/discussion-dose/src/benchmark_v3.py audit data/discussion-v3/vishesh-fixes-a1
```

One local worker, scripted evidence policy, maximum 636 policy calls for the separate run, zero network/model calls or spend, zero retries. Unit tests also use bounded scripted fixtures and mocked HTTP only. Stop if invariants fail, preserve output and document any repair before another attempt. No original results or reviews will be overwritten. Successful replay requires all 96 assigned cases, 636 matching requests, complete hash chains and recomputed scores/summary. Passing software tests does not set model-qualified or independently reviewed.

## Visualization mapping

Reuse `v3-stage-ledger-1` from [the original assessment](v3-offline-pre.md), bound to `vishesh-fixes-a1`, six development world IDs, all four arms and 36 memory fixtures. Logical event order, acquisition/report/round/merge/parent markers and full retained journal are unchanged. The local HTML replay and terminal metric table remain the supported artifacts; no live-site upload. This patch changes validation and adds score fields, not rendering. Check the generated payload against saved terminal metrics and test escaping; the prior browser playback check is retained as historical evidence, not claimed as repeated here.

## Remaining gates

Independent successor review and a separately planned real-model qualification are still pending. Historical v1/v2 scoring stays reproducible at its recorded commits; this amendment makes no retrospective scientific claim and does not revive the retired pilot.
