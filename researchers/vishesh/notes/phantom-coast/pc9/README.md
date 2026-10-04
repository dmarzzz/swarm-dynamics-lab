# PC9: population exploration instrument

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by vishesh/codex-phantom-coast; source `14504ced` ([registry](../../../../../experiments/evidence-metadata.json), [rubric](../../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **0/4** — Population misinformation spread and acquisition feedback remain untested on native models; only the offline instrument is validated. Basis: Thirty software tests and replay of four conditions on one deliberately scripted development world pass. A positive fault witness and negative evidence-only control validate routing/scoring, not empirical susceptibility.
- **sample_size_summary:** Native:0 worlds,0 requests. Saved unit fixture:1 world ×4 paired conditions ×5 scripted actors ×3 times; these60 decisions are dependent software fixtures. Candidate8-root pilot and8 qualification packets remain ungenerated/unrun.
<!-- experiment-evidence:end -->

**Built and validated offline; no native run.** Five separate actor contexts map four locations, share optional prior-round interpretations and choose two collective inspections. The four paired conditions cross honest/false initial evidence with peer communication on/off. No location is made inaccessible because of a belief. [Prospective implementation contract](PLAN.md).

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

## Readiness and next decision

**DECISION NEEDED for the concrete Q0 scope; preparation complete.** The [runbook](RUNBOOK-Q0.md) documents the private-bootstrap API, current operational evidence and closeout. Public native registration, current route/price, source/runtime and approved exclusive allocation are not yet satisfied. No researcher sign-off is required. Q0 uses8 calls/38 questions; the conservative40-question ceiling is USD0.05376. No retry/fallback, no automatic S1 dispatch. New native packet identities/orders remain unmaterialized; their templates are author-known and do not establish independent language transfer.

The four-location world is a minimal causal sandbox with sixteen physical maps and one effective post-peer acquisition decision. It cannot establish realistic geography, long-run persistence or a population of independently trained models. An exact controller can be rationally misled by false evidence too; a poisoning claim must exceed simple contamination and separate communication from adaptive evidence loss.

Original budget unchanged: cumulative known .846232842, conservative exposure .858328842, total cap5/API4. Zero new model calls, zero infrastructure costs, no machine allocation. The earlier candidate pilot remains unrun; this amendment adds no S1 arms or allowance.
