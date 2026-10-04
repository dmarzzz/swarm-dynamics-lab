# Immune Response

## Current iteration

The [scenario-grounded recovery study](scenario-study/README.md) is the current experiment design. It replaces exact-value ledger copying with dependency compatibility, persistent data, live health checks and consequential repair actions. The earlier instrument below remains historical mechanism evidence. The newly approved USD 8 grant funds one bounded native scenario qualification on sim-immune-response; the old task-6700 plan is superseded without execution.

## TLDR

A swarm can appear repaired and fail again when stale state returns. It can also “repair” itself by losing useful new knowledge. This exploratory instrument separates private/shared restoration, stale-record blocking and selective repair, with controls that expose both failure modes. V3 adds a strict agent contract, stronger scenario coverage and recorded time-series replay. It remains an oracle repair mechanism study, not autonomous detection or production safety validation.

## Question and prediction

Does restoring shared state improve correct completion when private restoration and replay blocking are held fixed? When does broad rollback lose legitimate learning, and does selective restoration avoid that specific cost? Missing lineage should defeat a blocker that only knows recorded lineage. These predictions are fixture tests first; model generalization requires valid new model runs.

## Setup

Seven specialists and one coordinator maintain twelve fictional registry records for 24 rounds. Tasks vary target relevance, names, values and specialist assignment. Native requests use pinned Haiku with one constrained record choice per visible fact. [Agent specification](AGENT-SPEC.md) defines prompts, memory, schemas, information boundaries and reproducibility limits.

## Protocol

See [frozen protocol](preregistration.md), [machine-readable plans](design.json), [review and failure diagnosis](REVIEW.md), and [pre-run assessment](reviews/engineering-a1-pre.md). All arms share real pre-intervention checkpoints. Five scenarios distinguish replay, no replay, no damage, legitimate intervening learning and missing lineage. Q11S tests selective restoration against broad rollback.

## Metrics

Exact authorized completion over all scheduled recovery requests; response failures; actual recovery versus persistent failure/relapse; retained learning; source capacity loss; and measured correct/wrong/missing private/shared state. All-assigned paired effects are primary; complete-valid-pair estimates are secondary. No population confidence claim from one native task or deterministic scripted fixtures.

## Visualization and reproduction

[Visualization mapping](VISUALIZATION.md) defines the live/final/animated views. The replay uses recorded data, offers scenario/task/arm controls and a time cursor, and labels scripted versus model evidence. Historical v2 has no full state telemetry; its replay says so.

```sh
python3 -m unittest discover -s researchers/vishesh/notes/immune-response-v3/tests -v
python3 researchers/vishesh/notes/immune-response-v3/src/runner.py --stage engineering --backend scripted --out /tmp/immune-v3-unique
# matplotlib and Pillow required only for rendering:
python3 researchers/vishesh/notes/immune-response-v3/src/visualize.py /tmp/immune-v3-unique /tmp/immune-v3-visuals --world benign_learning --task 6600
```

Use a fresh output path; the runner refuses overwrite. Paid execution requires the dedicated-machine and budget gates. See [historical v2](../actual-experiments/immune-response/README.md); no earlier run is overwritten or relabeled by v3.

## Results and current status

[Engineering results](ENGINEERING-RESULTS.json): 720/720 outcomes recorded, zero invalid, all clean controls passed. [Post-mortem](reviews/engineering-a1-post.md) separates mechanism findings from model evidence. Broad rollback loses newly learned legitimate information in the stress fixture; selective repair preserves it. Missing lineage defeats the known-lineage filter. These are scripted findings.

A new purpose-specific `sim-immune-response` machine is allocated exclusively. The owner approved an additional USD 8, reserved as a separate non-overlapping host grant. The redesigned scenario qualification is now executing; no task-6700 run was started. Earlier native v2 remains one invalid primary-control outcome out of eight; see REVIEW.md. Do not describe the offline schema fix as already verified against the model.

Public evidence: [engineering run and embedded animation](https://swarm-live.pages.dev/#/r/immune-response-v3%2Fengineering-a1-5409a091), [historical native v2 run](https://swarm-live.pages.dev/#/r/immune-response%2F4deeb0f2). The engineering run is an import of the original local execution, not a second execution on its upload host. Full replay and raw traces are stored as indexed gzip parts; `artifact-index.json` records hashes and part order.

## Native execution and reporting

`src/hub_worker.py` connects the frozen native plan to per-round progress images, final PNG/GIF/replay publication and explicit qualification status. It requires a non-secret allocation receipt binding this host, exclusive claim, expiry and a previously reserved USD 8 budget grant. The receipt records a real fleet/budget operation; creating the file is not a substitute for that operation. A missing/expired receipt or failed immutable-public-plan preflight stops before model calls. Configure the existing secure credential environment and isolated quota ledger, then invoke `hub_worker.py --out <new-output-path> --allocation-receipt <verified-receipt-path>`. Do not run this until the dedicated host and budget grant exist.
