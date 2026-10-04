# Antsy v7 setup and evidence record

Owner/operator/design assessor: vishesh/codex-methods. Same-author review, not independent. Exploratory instrument; no accepted-hypothesis or LLM-swarm efficacy claim. Researcher review is optional under the current Vishesh owner directive. [Setup runbook](../../../toolkit/agent-experiments/EXPERIMENT-SETUP.md).

## Gates and intended decision

Does a different OCR engine reduce shared wrong totals, and does dissent protection help beyond abstention? [PLAN.md](PLAN.md) defines the primary paired contrasts, competence thresholds, tradeoff criterion and claim boundaries. [v6 post-mortem](../antsy-receipt-v6/reviews/S1-post.md) motivates the shared-wrong-majority test.

| Gate | Status at implementation freeze | Evidence / next requirement |
|---|---|---|
| G0 Question and applicable research gates | pass | Exploratory owned notes, no formal registration claim; prior failure and primary sources in PLAN |
| G1 Plan before implementation | pass | PLAN published before src/ existed; initial plan commit0192a983, subsequent task-claim rebase preserves content |
| G2 Instrument and offline checks | pass | 23 tests cover extraction, duplicates, missingness, truth separation, agreement metrics, source/admission mismatch, corrupt-summary detection and deterministic chart generation |
| G3 Current attempt admission | pending | Fresh exclusive allocation PR175 merged; immutable public plan, browser verification and deployment receipt required per attempt |
| G4 Qualification before escalation | pending | S0 train20–39; >=16 scorable, best worker >=50% correct, each family >=2 correct, zero execution failures |
| G5 Reconciliation and closeout | pending | Preserve every attempt; post-mortem, artifact readback and release after completion |

Assessor: vishesh/codex-methods, 2026-10-04. Pending gates are not launch authorization.

## Frozen design, agents and reset

Five workers, all on the same receipt pixels: T0/T1/T2 use Tesseract ind+eng with PSM3/6/11; R0 uses RapidOCR original pixels; R1 uses the same RapidOCR model with grayscale/autocontrast/2x preprocessing. Every call runs in a fresh subprocess, without messages, memory, previous receipts or labels. No prompts or hosted models. All share the same numeric extractor. This explicitly tests tool-worker differences, not interpersonal or LLM diversity. [Worker profiles](spec/worker-profiles.json), [requirements](requirements.txt), [model hashes](spec/model-hashes.json), [measurement runner](src/study.py).

Each public record contains original/transformed input hashes, exact configuration and computation-origin hashes, model/extractor identifiers, region hashes, candidate, validity and timing. Raw OCR and images remain private. The evaluator attaches reference only after all five worker subprocesses return; policy payload excludes reference. Tesseract language model hashes, RapidOCR config/model hashes, package/Python versions and source fingerprint appear in each manifest. The fingerprint includes the plan, all source and tests, requirements, model manifest and inherited v6 reference parser. S1 must match qualification fingerprint and runtime exactly.

20 S0 receipts (train20–39), 20 reserved bounded-repair receipts (train40–59), 50 S1 receipts (test50–99). Previous v4/v6 images are hash-excluded. Receipt is the paired unit; 11 replayed policies do not create 11 independent observations. This pilot estimates differences with wide uncertainty; no vendor-disjoint or unknown-training-overlap claim. Unknown reference, invalid calls and referrals are separate denominators. Source/read-depth limitations and controls are in PLAN.

## Operations and admission

Manual native workflow; shared operations adapter is null. Commands run from a clean checkout at the admitted SHA. Paths below are runtime placeholders, not credentials.

| Operation | Command or limit |
|---|---|
| Inspect / offline validation | `python -m unittest discover -s 5-experiments/studies/vishesh/antsy-diversity-v7/src -p 'test_*.py'` |
| Prepare | Register experiment and condition TLDR plus immutable PLAN URL via team reporter; verify actual dashboard page; write private admission receipt from fresh exclusive fleet and deployment evidence |
| Dispatch S0 | `python 5-experiments/studies/vishesh/antsy-diversity-v7/src/study.py --stage S0 --out "$RUN_ROOT/S0-attempt-1" --admission "$ADMISSION" --cache "$TRAIN_CACHE" --report` |
| Dispatch S1 | Same runner with `--stage S1 --out "$RUN_ROOT/S1-attempt-1" --qualification "$RUN_ROOT/S0-attempt-1" --admission "$ADMISSION" --cache "$TEST_CACHE" --report`, only after qualification pass |
| Resume | Unsupported: existing output directory is refused; preserve partial run and create a prospectively admitted named repair |
| Analyze | `core.evaluate`, `core.diversity`, `study.audit`, `visuals.render` consume saved numeric records; analysis must not call workers |
| Stop | Terminate only this study process; retain partial manifest/records; fail/report attempt, audit uploads, release exclusive claim |

Runtime preflight verifies clean tracked source, exact source/run/stage, private receipt freshness <30min, unexpired dedicated allocation, zero hosted-model budget, fixed call cap, and public immutable plan bytes/hash before runtime/model loading. It does not independently query the fleet service: operator fleet/page attestations must come from actual contemporaneous checks. Public admission receipt contains only non-secret metadata. No credential transfer is needed; existing host reporter consumes the approved store locally. Host identity is checked using established SSH trust.

Dedicated allocation: `vishesh-antsy-diversity-v7`, sim-vishesh, approved team account, exclusive two-hour lease via agentops PR175. No provisioning, new billable infrastructure or API calls authorized for this stage. Existing Antsy budget is cumulative, never reset. Native OCR caps100/S0 and250/S1; one worker at a time, one inference thread,45s hard timeout/call. Stop admitting new receipts after25min, bounding the stage below30min. No outcome-dependent expansion or automatic S2. One repair only for an identified implementation defect; genuine weak competence blocks S1.

Each attempt records exact immutable source/PLAN URL and hash, verified time, source/runtime, assigned IDs, private cache hashes, allocation expiry and admission. Reporter registration precedes native measurement. Visual artifacts map directly to numeric outcomes: all-arm outcomes/cost, all-receipt decision matrix, pairwise same-wrong/answer agreement with denominators, and first-three-receipt measured replay (normalized timing). No visual RNG affects measurements. GIF is not a live parallel trace.

## Attempt history and closeout

No native v7 measurements at implementation freeze. S0 pre-review: the second engine's actual total-extraction competence is unknown. Proceed only after G3; retain failures and apply qualification thresholds without relaxation. Record assigned/started/terminal/graded/analyzed counts, software defects separately from wrong answers, costs, deviations, readback and post-mortem after each attempt. Allocation release follows uploads and worker termination. S1 remains blocked until G4 passes.

## 2026-10-04 qualification update

S0-attempt-1 at source8112123d was interrupted for missing host `libGL.so.1`. Ten complete receipt records preserve30 valid Tesseract and20 invalid RapidOCR calls; exact total started is unknown due to an unjournaled partial receipt. See [post-mortem](reviews/S0-post.md). This did not qualify the experiment.

The single bounded repair uses sourcef0be4c82, train40–59, unchanged policies/thresholds, installed official system dependencies, import-only preflight and immediate call journals. Host offline checks:24 passing. [Prospective repair assessment](reviews/S0-repair-pre.md). Public immutable GitHub PLAN was browser-verified at both source revisions, and the hub confirmed planned status. Local live-dashboard DNS resolution failed; no dashboard-view success is claimed. Runtime separately matched public plan bytes before measurement.

At this intermediate checkpoint S0-repair-1 was running; the terminal disposition below supersedes its pending status. The original attempt is retained, not overwritten. System dependency repair and journal code are included in the qualified source fingerprint if this attempt passes. The [reusable diversity protocol](DIVERSITY-PROTOCOL.md) explains how these measurements extend to later LLM workflows without claiming an LLM result here.


## Terminal disposition — S0-repair-1

G3 passed for the named repair at sourcef0be4c82; G4 **failed** the unchanged per-family competence threshold. No S1 was launched. G5 arithmetic, call and visual reconciliation pass; all14 original public artifacts were downloaded from the hub and SHA256-matched. [Readback receipt](results/S0-repair-1/readback.json). Hub status is failed, correctly reflecting qualification failure, despite successful execution.

| Field | Terminal assessment |
|---|---|
| Execution / response validity |100 started /100 valid /0 invalid native OCR invocations |
| Assigned / terminal / graded / analyzed |20/20/19/20 receipts;1 unknown reference retained;220 policy outcomes |
| Qualification |Failed: best Tesseract variant1 correct, below2 required per family; RapidOCR R0 11/19 |
| Scientific conclusion |Competence mismatch and conservative quorum dominate; no established diversity benefit |
| Tests and audit |24 offline tests; all220 policies and10 pair counts independently reconstructed in a separate same-author script |
| Runtime and cost |501.0s;0 hosted-LLM/API calls or new provisioning; measured worker costs include cold starts |
| Public artifacts |14 original files hash-verified through hub readback; charts and18 GIF frames decoded |
| Missingness and deviation |1 unknown reference; interrupted initial attempt preserved with uncertain partial-call count; local dashboard DNS failure documented |
| Next action |Develop/qualify competent perception controls under a new plan; leave test50–99 unopened |

[Final assessment](RESULTS.md) and [post-mortem](reviews/S0-repair-post.md) distinguish repaired execution from failed competence. Raw OCR and receipt images remain private. No credential values were read or published. Fleet release is recorded below after final upload.

Closeout verified2026-10-04T06:28:39Z: final assessment and audits uploaded;0 experiment worker processes remained. Dedicated allocation released and agentops release PR187 merged. Existing server retained under owner lifecycle control; no teardown or replacement provisioning. Public RESULTS page rendered correctly in the browser at commit5114250e. This iteration is closed with failed qualification and no S1 launch.
