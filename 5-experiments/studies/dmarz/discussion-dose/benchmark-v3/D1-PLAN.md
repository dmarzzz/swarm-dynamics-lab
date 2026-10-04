# D1 saved-request diagnostic: v3-d1-a1

Prospective implementation plan, 2026-10-04 UTC. The authoritative design remains
[NEXT-RUN](NEXT-RUN.md) and its [planning receipt](next-run-planning-evidence.json).
This document supplies the launch contract and incorporates the owner-initiated
deployment amendment before paid dispatch. See [SETUP](SETUP.md) and the
[current pre-run assessment](../reviews/v3-d1-a1-pre.md).

## TLDR

Compare `claude-haiku-4-5-20251001` and `claude-sonnet-4-6` on the same 60 exact
retained Q0 actor requests per model: 120 new calls total, one worker, no retries.
Measure clean full-evidence decisions, saved-report ballots and fixed parent-memory
behavior. A stronger model might improve constraint application; it is not a
guaranteed fix. These are already-open development examples, not fresh qualification
or a discussion treatment comparison. D2, Q1 and the confirmation holdout are closed.

## Question and prediction

Can Sonnet apply the existing constraints and evidence policies more reliably than
Haiku with actor inputs held fixed? The diagnostic hypothesis is greater reliability;
a null/adverse result is valid. Q0 supports observed early contamination and later
recovery, but its failed clean competence gates confound baseline reasoning and
discussion effects. D1 does not identify a causal discussion mechanism. There are
six world clusters and a fixed 36-fixture grid, not 120 independent scientific units.

## Setup

Parent `v3-q0-a1` completed 96/96 cases and 636/636 calls, at $4.387237 observed
usage cost, with zero provider/invalid failures and a passing frozen Python 3.12
audit. Clean full-evidence and saved-report gates failed at 2/6 and 1/6 against
5/6 each. Its results/source/records remain unchanged. Both independent reviews
were read; Vishesh passed the instrument and Shadow required failure-path repairs.

The diagnostic uses six full-evidence decisions, 18 saved post-report ballots,
and 36 fixed memory fixtures per model. Exact Q0 raw requests are outside Git;
their published hashes cannot reconstruct their bodies. `prepare` rejects absent,
changed or replacement records against the Q0 publication receipt and rebuilds the
entire planning receipt. No new world or holdout is generated. Confirmation IDs
30000–30023 stay closed. The contexts, prompt, schema, fixture wording and strict
extra-citation policy are unchanged. A fixture pass does not certify the different
swarm-parent wording.

The dedicated allocation is `sim-discussion-d1`, exclusive claim
`dmarz-discussion-d1`; the owner reports PR104 and PR107 merged. Their operational
verification is private. The retired Q0 host/claim cannot be used. The coordinator
prepares source; the existing local operator is the sole paid launch owner.

**Owner-initiated deployment amendment:** mode `owner-controlled-local-cleanup`
allows a remote systemd worker, watchdog, durable journal, hub progress and uploads
while the laptop is closed. The local operator verifies retained artifact readback
and monitors this first attempt. Cloud raw-data retrieval is explicitly unverified
and may remain false. Provisioning and cleanup remain with the one authoritative
local owner state. This is not a fully unattended provisioning/cleanup lifecycle or
a fully cloud-operated coordinator. No state migration is required for this bounded
mode. A later `owner-controlled-always-on` mode requires actual cloud retrieval plus
an always-on authoritative owner executor; do not infer it from a successful worker.

## Protocol

1. Commit source, this plan, SETUP and pre-run assessment. `prepare` requires their
   exact committed bytes and records an immutable public GitHub URL, plan SHA-256,
   source commit/dependency hashes and the frozen 120-assignment schedule. Preparation
   is offline and makes zero inference/metadata network calls.
2. Reuse the committed paired order, alternating the first model; change only model
   identity in native serialization. Temperature 0, output ceiling 2000 tokens,
   input ceiling 60000 bytes, timeout 120 seconds, thinking disabled by omission.
   No transport retry, repair retry, model substitution, repeat D1 or successor.
3. The owner establishes a dedicated service and persistent dispatch ledger, creates
   a manifest-bound hub run, and runs `rehearse`. Scripted artifacts are software
   evidence only. Verify disconnected-client progress, failure capture, journal
   durability, identical-byte uploads/readback and duplicate refusal. The owner
   cleanup workflow is verified separately; prior Q0 retirement proves the existing
   owner workflow, not autonomous cleanup.
4. Fill the private owner evidence using [the template](owner-preflight-template.json).
   False/missing required checks fail closed. In the local-cleanup mode only cloud
   retrieval may remain false; operator readback is still required. Secure six-hour
   claim coverage at allocation; at dispatch at least 90 minutes must remain, covering
   the one-hour worker plus audit/upload. Recheck current exclusive claim/workload.
5. `preflight` verifies source/requests, exact account model metadata via authenticated
   GET, both native serializations, publicly fetched immutable plan bytes and the
   actual plan page, owner evidence and shared budget. The owner must also inspect
   the displayed design. No paid compatibility probe is added to the 120 calls.
   Actual provider rejection remains a recorded failure; do not silently adapt.
6. `run` requires a current (<30-minute) passing preflight. A permanent fsynced
   attempt marker and process lock precede all inference calls. Reusing another
   output directory cannot bypass this ledger. A singleton owner job and exclusive
   host claim protect cross-host dispatch. Do not copy/reset the ledger or use
   another path to restart. A crash after `call_start` has an unknown outcome and
   must never be resubmitted. Worker `Restart=no`; watchdog may run independently.
7. One hour, owner stop marker, returned-model mismatch, accounting anomaly or local
   limit stops further dispatch. Assigned/unstarted/unresolved denominators survive.
   Provider/invalid failures are recorded and the remaining fixed schedule can
   continue; no adaptive prompts or extra calls. A systemic fault can be stopped by
   the owner/watchdog. Only identical artifact uploads may retry.
8. Audit under exact committed source, preserve/hash-verify uploads and independent
   readback, publish a candid report/post-mortem, then release claim and hand off
   owner teardown of only this host. Do not launch D2/Q1 or a sweep.

Reserve the conservative serialized-input/output allowance emitted by `prepare`
within the standing $500 budget across all dmarz experiments. The owner records a
non-overlapping reservation alongside current actual spend and other reservations.
No superseded tiny cap is reinstated. Prices used are Haiku $1/$5 and Sonnet $3/$15
per million input/output tokens. Report measured tokens and cost, missing usage,
orchestration and infrastructure cost separately. Tokenization/output can differ;
the original $0.760540 planning estimate is not an invoice or runtime cap.

## Metrics

All 120 assigned calls: started, terminal, valid, physical calls observed,
unstarted/unresolved, safe provider reasons, HTTP class, usage completeness,
input/output tokens, observed microdollar cost and latency. Missing usage is unknown
cost, not zero. Returned model identity is recorded and mismatch stops dispatch.

Full evidence: right/wrong/abstain, truth correctness, local evidence justification,
constraint violation, extracted claim count/correctness and choice/claim consistency,
per six worlds/model. Saved reports: the same per 18 assigned ballots/model, then
fixed N=3 quorum per six worlds/model. Two matching votes still win with one failed
ballot. Incomplete no-quorum is separate from evidence-based abstention, with
possible failed-ballot completion bounds; invalid ballots remain explicit.

Memory: truth correctness, local support/justification, unsupported-correct,
unsupported-wrong, grounded inherited error, citations, correct/unnecessary
abstention, coverage and distinct origins, per six assigned fixtures/state/model.
Expose extra agreeing secondary citations while retaining the frozen strict penalty.
Single-value N=3 majority conflict loss is structural, not evidence of intentional
uncertainty suppression by a model.

Report per-item paired scores/differences and world-level outcomes. Sonnet is merely
eligible for a separately assessed fresh qualification if both clean gates reach
5/6 and all responses/usage are valid/complete. `model_qualified` is always false
for D1. No population confidence or broad safety claim follows from this sample.

## Visualization mapping: d1-call-ledger-v1

Bind `discussion-dose-v3/v3-d1-a1` to the fixed schedule; X is terminal assignment
count 0–120, time origin is service start, series are started/terminal/invalid,
observed model cost and missing usage. Hub metrics show current progress; the full
fsynced event timeline preserves transitions and failures for private replay.
No swarm animation is promised for this model-only diagnostic. The supported
fallback is the hub counter timeline plus exact JSON journal and per-item tables.
Scripted rehearsal carries its distinct `-rehearsal` run ID and is never model
evidence. Public Q0 replay restoration remains separately tracked and does not
delay this bounded owner-initiated diagnostic.

## CLI and hub contract

From the repository root on Python 3.12, use `src/diagnostic_v3.py` under this notes
directory. Commands: `prepare`, `rehearse`, `preflight`, `run`, `audit`. `--q0` is the
retained Q0 directory; `--planning-receipt` is the committed planning JSON; `--output`
must be new. `prepare --launch-owner dmarz/discussion-bench-v3 --output MANIFEST`;
subsequent commands use `--manifest MANIFEST`. `preflight --owner-evidence EVIDENCE
--output PREFLIGHT`; `run --preflight PREFLIGHT --dispatch-ledger LEDGER --hub-run
discussion-dose-v3/v3-d1-a1 --output D1_DIR`. `audit --directory D1_DIR` never touches
network. Interrupted audits add `--allow-interrupted`; never resume model dispatch.

`rehearse --dispatch-ledger LEDGER --output REHEARSAL_DIR` accepts optional
`--hub-run discussion-dose-v3/v3-d1-a1-rehearsal`. To test deliberate failure through
the same harness use `--scripted-failure-call 5`; this fixture failure does not
authorize a model call. Do not run a second rehearsal against a consumed rehearsal
marker; inspect the original and use a separately named owner test ledger if needed.

The owner creates each hub run exactly once using existing `swarm_report`;
set `params.manifest_sha256` to SHA-256 of MANIFEST and `stage: D1` / `batch: v3-d1-a1`
(or stage REHEARSAL/batch v3-d1-a1-rehearsal). Registering an experiment definition
must preserve its newer metadata; this CLI does not overwrite registration.
`--hub-run` only attaches to a running matching job; no queue polling or old Q0
executor. Live progress reports counters only. Terminal `manifest.json`,
`events.jsonl`, `outcomes.json`, `summary.json` and `audit.json` are uploaded with
the existing `bench_v3.hub_worker.publish` compression/hash index. A hub `done`
means execution/audit, never qualification. Reporting failures cannot justify
rerunning model work; upload unchanged bytes separately and verify private readback.

Stop path: create `LEDGER/v3-d1-a1.stop` to prevent the next dispatch. This does not
cancel an in-flight network call or remove its ambiguity. The server-side watchdog
can inspect the durable journal and service deadline and capture killed/interrupted
outputs using `audit --allow-interrupted`, then preserve them without restarting.
