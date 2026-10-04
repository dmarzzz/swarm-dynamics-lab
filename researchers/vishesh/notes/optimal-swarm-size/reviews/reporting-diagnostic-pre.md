# Reporting diagnostic pre-run assessment

2026-10-04 UTC. Owner vishesh/codex-idea-scores. Attempt reporting-q0-a1, first live check of the repaired child-process reporter. Status: diagnostic-only, gated on exclusive allocation and public registration. Prior assessment: q1-setup-post.md; offline repairs passed independent engineering review AMENDMENT-1.md at 19fa527d. Formal paid-run review and credentials remain unresolved.

## TLDR

Verify the repaired reporting adapter against the installed hub client using one explicitly synthetic episode with no provider or model calls. Compare observed acknowledgments, public TLDR, saved artifacts and terminal state against the exact known synthetic records. Metrics: admission success, acknowledgment completeness, artifact byte identity and terminal visibility. This checks reporting plumbing only; the synthetic score and intervals are not model performance or swarm-size evidence. API spend is zero.

## Question and prediction

Will the bounded spawned reporting processes import the installed client, register an episode publicly, send progress, upload four exact artifacts and acknowledge completion? Predict all acknowledgments and fetched artifact hashes match. Any failure stops this diagnostic, preserves its local evidence and blocks paid execution; do not replace it with an unrecorded success.

## Setup

One freshly verified exclusive machine from the shared fleet; claim must be current and recorded separately before execution. Public code pinned to the immutable commit containing this plan and reporting_diagnostic.py. Python standard library; PYTHONPATH includes /usr/local/lib/swarm. Hub credentials are consumed privately by the installed client; no model credentials are required or read. Experiment optimal-swarm-size-reporting-q0, episode reporting-q0-a1. No qualification, fit, validation or transfer tasks are generated.

## Protocol

Publish/register this immutable plan and its TLDR; run public_plan.py before any episode. Start one synthetic row with a condition-specific TLDR. Reporter verifies the public run before further steps. Write assignment.json, trace.jsonl, outcome.json and replay.html explicitly labeled synthetic. One fabricated 0–1 second service interval is used solely to test preservation of known input bytes and renderer plumbing, never measured model latency. Send one progress update, upload all four files, save publication.json and finish. Verify public terminal state and all four artifacts by downloading them through the authenticated installed client into a separate verification directory; compare SHA-256 hashes locally and output booleans only. Never print authenticated URLs.

Bounded failure diagnostic: a local child that sends no result is tested through the reporting adapter's parent deadline with a short test-only timeout; no hub mutation or model request. The production timeout stays 30 seconds. Maximum one live episode, four uploads, one progress call, one terminal event; no automatic live retry. Thirty-second operation limits plus joins, public reads at 20 seconds, artifact verification bounded separately. Overall process deadline 300 seconds, then operator reconciliation. No paid calls; shared $20 model ledger remains untouched.

## Metrics

Exact known-byte agreement for all four artifacts, initial public condition TLDR match, local publication complete flag, public terminal status and child timeout behavior. Denominator one synthetic live episode; preserve failure and partial publication separately. This says nothing about model accuracy, route pinning, billing or optimal N. Existing 31 offline tests remain software evidence only.

## Visualization mapping

Diagnostic fixture version reporting-q0-a1: a visibly synthetic 0–1 second interval, a static table and replay scrubber. Retain input trace and generated replay. No real actor trajectories exist. Public live progress is labeled synthetic; any success metric is explicitly adapter-test success. Rendering already passed browser fixture inspection; this check tests preservation and delivery of the same format. Arbitrary HTML is a downloadable hub artifact, not embedded by the public proxy.
