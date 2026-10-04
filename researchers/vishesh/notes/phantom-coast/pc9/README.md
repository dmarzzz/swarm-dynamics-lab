# PC9: population exploration instrument

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by vishesh/codex-phantom-coast; source `4dc45cfc` ([registry](../../../../../experiments/evidence-metadata.json), [rubric](../../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **0/4** — Population misinformation spread and acquisition feedback remain untested on native models; only the offline instrument is validated. Basis: 47 offline software tests pass. Original four-arm fixture plus three added four-arm scenarios audit successfully. Eight reachable development snapshots and metered Q0 adapter are prepared; none is native evidence.
- **sample_size_summary:** Native:0 worlds,0 requests. Four scripted fixture families ×4 arms ×5 actors ×3 times; all dependent software fixtures. Eight inspected development qualification snapshots; reserved native Q0 and pilot remain unmaterialized/unrun.
<!-- experiment-evidence:end -->

**Native Q0 completed; qualification failed.** Eight valid calls,32/32 correct map labels,4/6 optimal inspections. No pilot. [Scientific post-mortem](reviews/Q0-A1-POST.md), [quality assessment](reviews/Q0-A1-QUALITY.json) and [saved native records](results/Q0-A1/summary.json). The population fixtures below remain scripted. Five separate actor contexts map four locations, share optional prior-round interpretations and choose two collective inspections. The four paired conditions cross honest/false initial evidence with peer communication on/off. No location is made inaccessible because of a belief. [Prospective implementation contract](PLAN.md).

This refocuses Phantom on whether a seeded false map spreads and prevents its own correction. Spread, acquired evidence, post-receipt error, uncertainty and task loss are separate outputs. The engine is capable of recording a resilience/null result; neither avoidance nor contamination is baked into its scheduler.

## What is implemented

- Strict actor packets with one privately seeded report, common direct receipts, explicit own history and masked/delivered peer slots. All packets in a round are constructed before any response is exposed.
- An injectable actor interface, choice-request builder and strict answer decoder. The added Q0 native adapter has pinned routing, safe traces, durable reservations and fail-closed admission; it is offline-tested, not live-qualified. Full native population/S1 orchestration is not implemented.
- Plurality inspection with deterministic ties, a three-valid-proposal minimum, costly repeats and failed slots with no silent substitute.
- Evidence-only and uniform/no-replacement references, exact finite-horizon Bayesian **per-actor** acquisition, and a pooled evidence-only endpoint diagnostic. The per-actor optimum is not claimed to optimize a decentralized team's joint policy; pooled access is explicitly greater than an unexposed actor's access.
- Full saved packets, hash-bound decisions, receipt/message delivery ancestry, metrics with missingness bounds, and replay recomputation that rejects tampering even when the outer artifact hash is rewritten.
- A self-contained [interactive replay](results/acceptance-fixture/replay.html), with all four conditions and all three time points. Download/open HTML or serve it locally; GitHub shows source. This is a **deliberately credulous scripted fault fixture, not a native poisoning result**.

## Run offline

From the repository root, using Python3 and the standard library only:

```sh
python3 -m unittest discover -s researchers/vishesh/notes/phantom-coast/pc9/tests -v
python3 researchers/vishesh/notes/phantom-coast/pc9/instrument.py fixture --output /tmp/phantom-pc9-fixture
python3 researchers/vishesh/notes/phantom-coast/pc9/instrument.py audit /tmp/phantom-pc9-fixture/fixture.json
```

The fixture command requires a new output directory and cannot dispatch a model. The included fixture exercises a known bad policy and known recovery response. Its positive effect is deliberately engineered to verify scoring/routing; it is not research evidence. The evidence-only control's null and exact-controller reference witnesses are separate unit tests. The public tie order supplies the no-replacement schedule; a future cohort must randomize that order independently of hidden truth before dispatch.

[Validation receipt](results/validation.json) records30 passing tests; [case-quality assessment](reviews/CASE-QUALITY.json) evaluates the twelve dimensions; [build review](reviews/BUILD-POST.md) states scientific limits; [authoritative setup](SETUP.md) records next action. These are same-author checks, not independent review. Prior [six mechanism cases](../reopening/CASEBOOK.md) remain inspected development fixtures and are not new native samples.

## Added scenarios and Q0 preparation

The [scenario browser](results/native-preparation/index.html) adds three audited, deliberately scripted witnesses: false-positive diversion, correction after wrong peer consensus, and repeated inspection leaving evidence missing. Each retains four matched conditions. These supplement the development casebook, not the held-out empirical cohort.

[NATIVE-PLAN](NATIVE-PLAN.md) freezes eight reachable clean-competence snapshots. Expected gate:8/8 valid responses,32/32 correct map labels,6/6 optimal inspections (all tied optima accepted). Qualification does not require poisonability. Tests check reachable histories and time boundaries, and reject malformed outputs, excess spending and tampered saved grades. [Native preparation validation](results/native-preparation/validation.json) records47 passing tests,12 additional replay audits and zero native calls; the original30-test receipt above is historical. [Preparation review](reviews/NATIVE-PREP-POST.md) and [updated twelve-dimension assessment](reviews/NATIVE-CASE-QUALITY.json) separate software readiness from native qualification.

## Current disposition

**HOLD pilot; repair the acquisition objective offline.** The owner-approved Q0 ran once under the frozen plan. Both misses chose to verify the private reported site instead of inspecting an untouched site. All correction/uncertainty maps were correct. This is a narrow snapshot result, not a native population poisoning effect.

The exact reference minimizes individual posterior loss, while the action prompt also describes collective plurality. That objective ambiguity limits diagnosis; it does not retroactively change the failed frozen gate. Clarify individual versus collective acquisition and establish the corresponding reference before proposing fresh native cases. These eight released packets are now development evidence. No retry or successor is queued. Researcher review remains not required.

The four-location world is a minimal causal sandbox with sixteen physical maps and one effective post-peer acquisition decision. No population rollout, realistic geography, long-run persistence or population of independently trained models was tested. The earlier candidate S1 remains undispatched.

New API cost .000492912; cumulative known .846725754; conservative exposure .858821754, including unchanged historical uncertainty .012096. Original cap5/API4/infra1. No new VM or incremental infrastructure; worker stopped and ledger backed up. [Closeout](results/Q0-A1/CLOSEOUT.json) records reporting and allocation release.
