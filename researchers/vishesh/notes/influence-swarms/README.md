# How to win agents and influence swarms

## TLDR

Outside evidence can mislead a nine-agent team even when its verifiers return correct facts. This prospective repair makes verification update an explicit decision ledger, applies the same final rule in every arm, and records the model chair's proposal separately. Historical results and the measured replay are in [the v2 audit](../external-influence-v2/reviews/quality-post.md). This version is **offline-tested, not live-qualified**; fresh dedicated allocation is required.

## Question and prediction

Does targeted checking reduce harmful choices relative to random checking when both use the same enforced decision rule? Low/high exposure and eligible/ineligible targets probe whether success depends on saturation or trivial feasibility. A valid null or adverse result is retained. This is exploratory S0/S1, not an accepted formal hypothesis.

## Setup

Six analysts, two check interpreters, one model chair. Haiku 4.5, pinned model ID, temperature zero, native structured outputs. Four fictional candidates and twelve fixed-exposure documents. Procurement is primary; dependencies/travel provide competence screens. Every complete arm has 15 logical calls; transient HTTP retries may add billed attempts. See [agent contracts](AGENTS-SPEC.md).

## Protocol

Use the [versioned protocol](preregistration.md), [executable design](design.yaml), [pre-run assessment](reviews/quality-01-pre.md) and [visualization mapping](reviews/visualization-mapping.md). Record private reports, one synchronous peer revision, two scoped check results, normalized scorecard, chair proposal and enforced choice. The observed-document calculator performs only arithmetic; it never certifies evidence truth. No credentials, shell, browser, external writes or evaluator truth are available to agents.

## Metrics

Report committed correctness/harm/regret and chair-proposal correctness/disagreement separately. Confidence calibration applies to the chair's proposal, not the enforced outcome. Track citation support, cost arithmetic errors, unexposed-agent conversion, coverage, unavailable checks, requests/retries/tokens/cost and all failure denominators. Tasks are the independent units; agents/frames are not replicates.

## Reproduce and status

```sh
python3 -m unittest discover -s researchers/vishesh/notes/influence-swarms/tests -v
python3 researchers/vishesh/notes/influence-swarms/src/runner.py local --stage engineering --out /tmp/influence-quality-new
```

Use a fresh directory. Historical v2 is immutable. Paid execution requires an exclusive machine claim, an enforced non-overlapping quota from the existing shared authority and exact-version public plan; it must not copy the old USD 45 ledger to a new host. No additional spending authorization is assumed.
