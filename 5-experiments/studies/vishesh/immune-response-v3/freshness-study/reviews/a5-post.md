# Immune Response — A5 native post-mortem

Retrospective owning-agent review,2026-10-04. [Run](https://swarm-live.pages.dev/#/r/immune-response-v3%2F1004-185822-0e77b0). Frozen runtime1873ee1addb07a556928ac75e40d9832dce405f5. [Reconciliation](a5-reconciliation.json), [summary](a5-summary.json), [native frame](a5-final.png), [animation](a5-replay.gif). No independent review claimed.

## Outcome and coverage

OpenRouter with Anthropic-only Haiku4.5 returned17/17 responses with stop finish reasons and complete usage/cost. Four advisor responses and13 controller responses were inspected in full. Twelve controller actions applied; the thirteenth stopped on an internal assertion. Of12 assigned episodes:3 completed,1 started/invalid,8 unstarted. One complete raw/checked pair exists;43 of60 planned calls were not dispatched. No retry or successor. This is better native evidence than A4's empty transport failure, but it is not a completed treatment comparison.

## What the traces establish

In the fresh-crash world, both arms scored0/4 healthy ticks. A same-version worker restart was sufficient according to the visible reference controller. Instead, the configuration advisor falsely described worker v2 as unable to read the persisted legacy schema, despite the provided catalog listing both schemas. The runtime advisor asserted a liveness contradiction absent from the supplied probe. Both controllers inspected and downgraded gateway/worker to v1, losing the required bulk-checkout feature. Incorrect advisor claims recur in controller explanations, but this observational trace cannot isolate advice causality from independent model error.

In the stale-false-alarm checked arm, the service began healthy. The agent refreshed telemetry, then inspected repeatedly while repeating an obsolete contradiction even after every current health check was true. At tick4 its explanation recognized compatibility and concluded that waiting was safest, but the structured action deployed gateway v1. Executing that action broke RPC compatibility and removed the required feature:3/4 healthy ticks, final unhealthy. Grade the actual action, not the prose conclusion. Freshness labels did not prevent these observed mistakes; one completed pair and one unpaired trajectory cannot estimate general treatment harm or benefit.

## Verified instrument defect

The raw stale-alarm arm's first action was inspect with service worker-1 and version0. This is valid under the advertised flat JSON schema, but step() asserts service=none for every non-deploy action. The actor-visible tool description never states that restriction. Replaying the retained action reproduces the assertion. Classify this terminal event as an interface/schema mismatch, not a demonstrated reasoning failure. Preserve all earlier applied actions and their outcomes; do not repair the response retroactively. Instrument feasibility tests missed the gap because the reference controller always supplied the hidden sentinel.

## Integrity, cost and visualization

All17 request/response/usage IDs and request hashes reconcile. Every recorded state/health transition was replayed from saved actions. Actual new costUSD0.027232;17 reservations totalUSD0.123600. Cumulative ledger:405 calls,USD3.309095reserved of originalUSD8. Historical uncertain exposure remains; no allowance reset. No new machine created and shared-machine allocated cost is not separately measured. Correct-account claim343 was released by349 after workers stopped and the SSH listener closed. The exact local relay was stopped by its owning task. Seven hub artifacts were fetched and SHA256-matched; full transport trace and relay evidence remain local, not silently claimed as public raw artifacts.

The five-frame animation shows only the three complete trajectories and labels the12-episode denominator. Empty panels are missing outcomes. The invalid action did not execute and is described in this report rather than drawn as a service transition. Frames are native saved-data renderings; no scripted frame substitutes for missing observations.

## Decision and prospective offline repair

Decision: repair the instrument before proposing further collection. A5 remains failed execution, failed observed capability, and inconclusive treatment efficacy. OpenRouter transport is now demonstrated for these17 calls, not promised indefinitely. The original model/temperature/provider identity and source are recorded; route migration does not make A3/A5 equivalent cohorts.

Before implementation, specify the repair: expose the exact non-deploy service=none/version0 contract in tool descriptions and encode dependent action/service/version combinations in JSON schema; restrict deployment versions to that service's catalog. Add exhaustive offline checks that every admitted combination reaches a defined simulator result and the retained failing action is rejected by the advertised schema. Keep historical A5 untouched, stopping rules and adverse outcomes intact. This is not permission to run A6. A future proposal should first qualify factual catalog reading, useful restart and healthy abstention, then distinguish evidence freshness from evidence truth. Do not respond to the failure simply by increasing swarm size, weakening success thresholds or rerunning until favorable.

## Offline repair outcome

The prospective contract repair above was committed before implementation. Added explicit non-deploy argument requirements and service-specific schema branches. Exhaustive combinations across all six scenarios reach defined simulator results; the retained invalid inspect and nonexistent service/version pairs are rejected by the visible schema.20tests pass, including route/cost fault checks. This offline repair was not deployed into A5 or followed by another model call. Hosted support for the refined dependent schema still needs bounded qualification in a separately approved next attempt.
