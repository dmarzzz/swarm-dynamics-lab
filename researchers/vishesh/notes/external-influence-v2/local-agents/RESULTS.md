# Local-agent results: external influence v2

The repaired local Qwen3 1.7B variant produced **11/50 correct final choices**, versus **19/50** for historical Haiku. Local all-assigned correctness was lower (-8 choices; -16 percentage points). This is a descriptive model-plus-adapter comparison on three synthetic task roots, not a general model ranking.

## What ran

Fifty nine-agent teams: six analysts, two check interpreters and one chair per case; **450 episode-local identities**, shared model weights and at most four concurrent requests. The full comparison used 737 actual model calls and 30.02 minutes of wall time including progress reporting. There were 48 valid outcomes and 2 invalid outcomes. Every assigned case remains in the denominator.

Inference API charge: **USD 0**. Across qualification, failed attempts, repair and S1: 914 calls and 34.39 measured stage minutes; 1,326,885 reported input tokens and 211,104 reported output tokens. Token usage for the two unreturned timeout responses is unavailable. Electricity, energy and total ownership cost were not measured. The historical 50-case Haiku run reported USD 2.002637; that is not a hardware-matched cost/speed benchmark.

A during-run Ollama sample reported approximately 2.4 GB loaded for the 1.7B model, entirely on GPU, with an 8192-token context. This is a sampled model footprint, not measured peak process/system memory. Hardware: Apple M5 Max, 128 GB unified memory.

## Qualification and repair history

| Stage | Model / change | Valid / assigned | Correct / assigned | Calls | Seconds |
|---|---|---:|---:|---:|---:|
| Q0 | 0.6B original schema | 0/6 | 0/6 | 11 | 8.5 |
| Q1 | 1.7B original schema | 3/6 | 2/6 | 66 | 120.0 |
| D0 | 0.6B historical diagnostics | 0/4 | 0/4 | 10 | 13.8 |
| Q2 | 1.7B constrained schema | 6/6 | 5/6 | 90 | 120.0 |
| S1 | 1.7B constrained schema | 48/50 | 11/50 | 737 | 1801.0 |

0.6B omitted required candidates. The first 1.7B qualification failed allowed-citation constraints in three teams. The prospective repair encoded only public candidate counts/names, allowed citations and numeric ranges into JSON grammar. It never inserted correct numerical answers. Fresh Q2 qualification passed 6/6 validity and 5/6 correctness, unlocking S1. Q1 and Q2 use different development roots, so their difference is not an isolated causal effect of the schema repair.

## Same-case comparison

| Application / world | Haiku correct | Local correct | Local valid |
|---|---:|---:|---:|
| dependency / clean | 4/5 | 5/5 | 5/5 |
| dependency / misleading | 0/5 | 2/5 | 5/5 |
| dependency / syndication | 0/5 | 2/5 | 5/5 |
| procurement / clean | 5/5 | 0/5 | 5/5 |
| procurement / instruction | 5/5 | 0/5 | 3/5 |
| procurement / misleading | 0/5 | 0/5 | 5/5 |
| procurement / syndication | 1/5 | 0/5 | 5/5 |
| travel / clean | 4/5 | 2/5 | 5/5 |
| travel / misleading | 0/5 | 0/5 | 5/5 |
| travel / syndication | 0/5 | 0/5 | 5/5 |

| Policy | Haiku correct | Local correct | Local valid |
|---|---:|---:|---:|
| discussion | 4/10 | 1/10 | 10/10 |
| private_review | 3/10 | 3/10 | 9/10 |
| random_check | 3/10 | 3/10 | 10/10 |
| targeted_check | 4/10 | 2/10 | 10/10 |
| targeted_provenance | 5/10 | 2/10 | 9/10 |

All assignment keys and truth/corpus/exposure hashes matched. Local-only correct: **5**; Haiku-only correct: **13**. Local changed the final choice or failed to supply one in 23 of 50 cases.

Known harmful target selections: Haiku **28/50**, local **22/50**, with **2 local outcomes unknown**. The local all-assigned harmful fraction therefore lies between 22/50 and 24/50; unknown does not mean harmless. Mean regret: Haiku 5.701, local 10.108, with invalid outcomes assigned 100 by the frozen scoring rule.

## Interpretation and limits

The local model is inexpensive to exercise and fits easily in the observed memory footprint. On this instrument it delivered lower all-assigned correctness than the historical backend. The six-case competence screen did not establish performance on the historical task roots. These are fictional decision problems with a known weak chair/check-integration architecture; the results do not establish real-world procurement, travel or software-selection quality.

Post-hoc deterministic replay of the exact chair-visible reports/checks disagreed with the model chair in 27/48 evaluable cases. It produced 19 correct counterfactual choices versus 11 observed correct choices among those cases. This replay is a diagnostic, not a newly run intervention or a claim that a repaired system would achieve that performance.

There are only three independent domain/task roots. The 50 assignments, 450 identities and hundreds of calls are dependent observations. No significance tests or confidence intervals are reported. Model, endpoint and structured-output enforcement differ from the historical run; no isolated model-size effect or hardware-optimal concurrency claim is supported. Four requests were admitted concurrently, but server-internal scheduling and queue time were not separately measured. The shared desktop was not an exclusive performance-benchmark machine.

## Records, replay and process compliance

- [Frozen original plan](PLAN.md) and [prospective repair plan](PLAN-v2.md).
- [Paired results and fixture hashes](evidence/S1/comparison.json).
- [Summary](evidence/S1/summary.json), [run manifest](evidence/S1/manifest.json), [public-plan receipt](evidence/S1/public-plan-receipt.json).
- [Compressed synthetic event journal](evidence/S1/events.jsonl.gz) and [all outcomes](evidence/S1/episodes.jsonl).
- [Recorded HTML replay](evidence/S1/replay.html), [sampled animated replay](evidence/S1/replay.gif), and [final frame](evidence/S1/final.png).
- [Evidence hashes](evidence/index.json) and [source provenance](evidence/source-provenance.json).

Public receipts precede the first inference in each stage. The original two failed qualifications and diagnostic cases remain intact. Execution completion, qualification status and process compliance are separately recorded. The repaired schema and full comparison were planned before their calls. S1 kept its preset 30-minute limit and received no performance-driven prompt or schema changes. Any timeout/invalid outcome remains part of the comparison. Results are exploratory; formal confirmation remains closed.

![Same-case local versus historical results](comparison.png)
