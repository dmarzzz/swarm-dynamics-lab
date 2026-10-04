# Immune response v3: durable repair without erasing good knowledge

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
