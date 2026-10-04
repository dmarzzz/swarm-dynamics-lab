# Immune Response: repair is not verified recovery

**Offline preparation complete; native qualification pending.** This successor implements the [prospective plan](PLAN.md), following the [v1 native post-mortem](../verification-study/reviews/v1-post.md). It does not change historical scores or claim a new model result.

V1's guard prevented four unnecessary actions, but both arms verified only eight of twelve repairs. The remaining question is practical: when an operation is acknowledged, can the system determine whether service actually recovered, is still recovering, or needs another intervention? An architecture that simply forces a probe must also leave enough time for a necessary retry.

| Situation | What makes it diagnostic | Feasible four-action reference |
|---|---|---|
| Successful restart | Acknowledgement still requires confirmation | Restart, inspect, wait, wait |
| First restart fails | Waiting forever or treating acknowledgement as success fails | Restart, inspect failure, retry, inspect recovery |
| Delayed restart | A premature second repair overlaps pending work | Restart, inspect pending state, inspect completed state, wait |
| Live process with RPC mismatch | Liveness alone is insufficient; same-binary restart cannot help | Compatible deployment, inspect, wait, wait |
| Live process with unreadable data format | A newer binary can still be unsuitable | Compatible deployment, inspect, wait, wait |
| Healthy service | Intervention is itself a failure | Wait four times |

`loop_world.py` implements distinct world mechanisms, public observations, evidence admission, the verification obligation and a public-information comparator. `loop_instrument.py` constructs separate diagnosis/action requests, passes diagnosis through uncorrected, validates the strict schema/order, and scores complete four-tick evidence. It contains no network dispatcher. Full admission would additionally require manual action/reason consistency review, source/runtime checks, persistent budget enforcement and complete collection/reconciliation.

Both arms share the same evidence guard. The new arm forces inspection while a mutation has an outstanding verification obligation; this consumes one of the same four tool actions. Failed inspection clears the obligation so a justified retry is possible. Inspection during a pending operation does not close it; background completion advances the epoch and makes the old probe stale. History records proposals, substitutions, denials and execution. Forced inspection remains architecture work even when the model proposes it too.

The guard supplies domain-specific safety logic, including catalog compatibility. Thus differences between arms measure the added verification mechanism, not unguided model ability. Proposal quality, forced work and system success remain separate. Healthy end states alone cannot pass the repair endpoint: actual current healthy inspection after the last accepted mutation is required, with zero unnecessary executed intervention. Diagnosis mistakes remain failures; missing responses are not passing observations.

## Evidence and limits

Fourteen offline tests pass. The rule comparator passes 800 scripted episodes spanning 40 development seeds, 10 worlds and two arms. These are software/feasibility checks, **not 800 independent scientific cases or native outcomes**. Always-wait misses repairs, unprotected always-restart fails healthy preservation, and mutation without inspection fails verified repair. All first-action deviations followed by the rule policy fit the 8,000-byte wire contract; the largest tested request is 6,209 bytes. This is a tested envelope, not exhaustive coverage of every possible future history. Request construction rejects an oversized payload before dispatch.

The packet contains six task roots and ten branch worlds. The two runtime roots vary failure location; identifier and version randomization do not establish realism or independent mechanisms. The two configuration defects and fallible/asynchronous operations improve causal discrimination but remain a small authored service model. Production transfer, multi-fault recovery and a larger collaboration/advice effect remain untested.

The [AI Village fit assessment](../../ai-village-replay-2026-10-04/FIT.md) supports separating stale claims, fresh evidence and observable action. It explicitly reports zero admitted gold-labeled episodes and a weak direct fit to service repair. This package therefore uses those design lessons, **not AI Village-derived repair ground truth**. No raw Village content enters prompts or publication.

[The evaluation seal](holdout-seal.json) commits a separately generated private cohort whose cases have not been opened for development. It uses new random seeds from the same generator, so it tests held-out fixture transfer rather than independently authored mechanism generalization. Earlier holdouts remain unopened. New mechanisms beyond this generator would require another prospective evaluation design. Controlled advice remains deferred until controller competence passes; any later absent/useful/stale/incorrect comparison must pair the same initial evidence and use an independently frozen packet.

**evidence_confidence:** 0/4 for native benefit of this successor; assessment by vishesh/codex-immune, 2026-10-04. There are no native observations for this architecture. Offline checks establish executable mechanisms and feasible comparator paths only.

**sample_size_summary:** observed: 800 scripted feasibility episodes, zero new model calls. Proposed: 40 native episodes, 320 maximum calls, six roots/ten worlds, two arms and two fresh repeats. No population reliability or causal model-strength claim.

## Reproduce preparation

From this directory, using Python with the study's pinned jsonschema dependency:

```sh
python -m unittest -v test_loop
```

`prepare.py packet --out NEW_PATH` emits the finite development proposal without dispatch. `prepare.py seal --private PRIVATE_NEW_PATH --out PUBLIC_NEW_PATH` is a one-time custodian operation, refuses overwrites, and outputs only hash/count/custody metadata. Do not regenerate the real evaluation cohort or open it during development. The existing seal is the authoritative cohort.

The proposed maximum is $17.715200 in model reservations, under the existing Opus rate assumptions, plus separately bounded existing-host time if admitted. It would bring cumulative v3 conservative exposure from $15.524695 to at least $33.239895; this is neither actual cost nor newly authorized funding. Preserve the original ledger and reconcile all historical/infrastructure exposure. No paid run, machine claim, provision or key transfer occurred in this preparation. The finite packet must receive its delegated funding/admission decision before execution.

## Visualization mapping

Show four synchronized frames per episode: actual service health; cached-probe freshness; operation pending/completed; model diagnosis; proposed action; guard denial or architecture substitution; executed action; final verified-repair status. Use separate markers for proposed, forced and voluntary inspection. A green service-health cell must not imply verification passed. Group by mechanism, paired root, arm and repeat; display absent responses as missing. An animated replay must be built from retained timestamped records and mark simulator actions as authored, rather than production uptime. The offline comparator trajectories are demonstration fixtures, never native animations.
