# PC9: population exploration instrument

**Built and validated offline; no native run.** Five separate actor contexts map four locations, share optional prior-round interpretations and choose two collective inspections. The four paired conditions cross honest/false initial evidence with peer communication on/off. No location is made inaccessible because of a belief. [Prospective implementation contract](PLAN.md).

This refocuses Phantom on whether a seeded false map spreads and prevents its own correction. Spread, acquired evidence, post-receipt error, uncertainty and task loss are separate outputs. The engine is capable of recording a resilience/null result; neither avoidance nor contamination is baked into its scheduler.

## What is implemented

- Strict actor packets with one privately seeded report, common direct receipts, explicit own history and masked/delivered peer slots. All packets in a round are constructed before any response is exposed.
- An injectable actor interface, transport-neutral choice-request builder and strict answer decoder; **no network/credential/native-launch adapter** in this build.
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

## Readiness and next decision

The software is ready for controlled offline instrument work. Native qualification and run admission are **not** satisfied. The candidate eight-root feasibility envelope in PLAN is costed only against the historical conservative rate; fresh qualification packets, model/route/price bounds, exact semantic thresholds, source/public registration and approved allocation remain necessary. The owner approved this build; a paid scope needs its concrete updated-plan decision. No review sign-off is required.

The four-location world is a minimal causal sandbox with only sixteen physical maps and one effective post-peer acquisition decision. It cannot establish realistic geography, long-run persistence or a population of independently trained models. An exact controller can be rationally misled by false evidence too; a poisoning claim must exceed simple contamination and separate communication from adaptive evidence loss.

Original budget unchanged: cumulative known .846232842, conservative exposure .858328842, total cap5/API4. Zero new model calls, zero infrastructure costs, no machine allocation. Candidate native total would reserve3.06432 more API, not spend that amount automatically. No fallback, repair run or top-up is implied.
