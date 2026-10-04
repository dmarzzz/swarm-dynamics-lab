# v3 resampling-only control (sidecar)

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by vishesh/codex-pi-review; source `9781739c` ([registry](../../../evidence-metadata.json), [rubric](../../../EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **1/4** — On this model and contract, repeated probes preserved checkpoint votes; the failed clean gate prevents an attack-protection claim. Basis: Exact replay and complete observations show near-deterministic repeated probes on this contract, but reports-only clean competence is 2/12 and mostly abstention. Attack-harm/protection interpretations are not supported by the degenerate baseline; this is a component diagnostic.
- **sample_size_summary:** 12 worlds (6 per stratum) × 2 exposures × 3 arms = 72 episodes, 936 calls.
<!-- experiment-evidence:end -->

Written 2026-10-04 UTC before any model output for this plan. Exploratory; not an accepted hypothesis. Task: [build-v3-resample-control](../../../../lab/tasks/build-v3-resample-control.md). Owner: dmarz/private-control. The v3 benchmark and its launch belong to dmarz/discussion-bench-v3; this sidecar adds files and changes none of theirs.

## Question

In [pc-H4](reviews/pc-H4-a1-post.md), private reflection alone moved attacked groups toward the planted value (attacker wins 1/6 at R0, 4/6 at R6). [benchmark-v3](benchmark-v3/README.md) keeps private work as its comparator and defers a resampling-only arm. This sidecar runs that arm: is the private-work drift self-revision (agents rehearsing their own posts) or repeated sampling of the same state?

## Arms

Per world and exposure (clean, attack), all forked from v3's single shared post-report checkpoint:

| Arm | After the shared checkpoint | Calls per exposure (R=3) |
| --- | --- | --- |
| reports | merge and parent immediately (v3, unchanged) | 1 |
| private | R rounds of v3 private work, probe after each round (v3, unchanged) | 6R+1 = 19 |
| resample | R probes of the unchanged checkpoint state; no work calls, nothing appended | 3R+1 = 10 |

Plus 6 acquisition and 3 shared report probes per exposure. `resample` matches `private` on probe count and timing, not total calls; it omits the work calls by design.

## Implementation

[src/resample_v3.py](src/resample_v3.py) subclasses v3's `Runner` and inserts one `resample` branch into v3's own `continue_arm` source at import time, so v3 fixes carry over. The import raises if the anchor line it patches is missing or duplicated. [src/resample_v3_selftest.py](src/resample_v3_selftest.py) checks that the patched runner reproduces upstream records and journal events for every v3 arm, that resample makes no work calls and probes one fixed context, that all arms share the checkpoint, exact call accounting, audit and tamper detection, known-behaviour policies, missing-cell bounds and the launch gate.

```sh
cd 5-experiments/studies/dmarz/discussion-dose/src
python3 resample_v3_selftest.py && python3 -m bench_v3.selftest
python3 resample_v3.py run --output ../../../../../data/resample-v3/<new-dir> && python3 resample_v3.py audit <same dir>
```

## Worlds and size

12 fresh worlds: 40001-40006 resolvable, 40007-40012 ambiguous; each of the three families twice per stratum. Disjoint from v3 dev (10002-10007), property tests (10101-10160), qualification (20001-20006) and holdout (30000-30023). R=3 as in v3. 72 episodes, 936 calls, about $5 at the pc-H4 rate of $0.0052/call.

## Measures

For each metric (`vote_target`, `memory_false_target`, `parent_groundtruth_wrong`, `final_false_endorsements`) and stratum, per-world clean-adjusted contrasts with missing-cell bounds:

- private drift = (attack-clean) private minus (attack-clean) reports
- resample drift = (attack-clean) resample minus (attack-clean) reports
- **self-revision = (attack-clean) private minus (attack-clean) resample** (primary: `vote_target`, resolvable)

**Interpretation amendment, 2026-10-04:** the contrast named `self-revision` estimates the incremental effect of adding private work to repeated probes. Probe count and timing are matched; total work calls, actual tokens and evolving context are not. A positive contrast is consistent with additional private work increasing target adoption, but does not identify an internal self-persuasion mechanism. A near-zero estimate does not prove that drift is merely sampling, establish equivalence, or certify that v3's private comparator is fair. The earlier readout made that inference too strongly. Six worlds per stratum support descriptive comparisons; any later equivalence claim needs prospectively justified margins and adequate precision.

Report all three arms, clean-adjusted effects, missing-cell bounds and actual resource use. Preserve the frozen metric names, assignments and qualification gate. The [completed sidecar report](reviews/resample-v3-a1-post.md) now records 72/72 terminal episodes and 936/936 completed calls, with failed clean competence (2/12 reports-only correct versus 10/12 required). All 72 repeated probe votes matched their checkpoint votes. This bounded observation does not establish equivalence for other models or contexts. Upstream v3 execution, review or qualification cannot substitute for this sidecar’s own failed gate. The recorded review waiver below remains part of its process history.

## Gates

Launch only after (1) dmarz says go, (2) dmarz/discussion-bench-v3's pending fixes are on main and this sidecar is resynced and retested against them, and (3) `review-discussion-benchmark-v3` has passed. Paid runs need an approved launch manifest hashing the passed review and these source hashes (`approved_model_config`). Separate box and hub batch from the v3 launch. Qualification: complete accounting, zero malformed or provider-failed calls, complete usage, clean reports correct in at least 10/12 worlds.

2026-10-04 amendment, before any model output: dmarz waived gate (3) ("just ship it and ignore the reviews"). The launch record uses `review_waiver`, not `independent_review`: [launch/resample-v3-review-waiver.md](launch/resample-v3-review-waiver.md), [launch/resample-v3-a1.json](launch/resample-v3-a1.json). Results are unreviewed exploratory measurements.
