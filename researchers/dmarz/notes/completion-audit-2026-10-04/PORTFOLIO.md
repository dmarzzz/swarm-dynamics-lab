# Portfolio inventory

Source: `5945294fa853d7ff60a7ec62b31fd2158d74c3de`; complete hub run inventory 2026-10-04 04:11:27 UTC; targeted Theseus v2 followup 04:17:46 UTC; later publication supplement `4d007242b7ae5117d7f497036fa51f2225d7f993`. 223 entries, including plans and diagnostic/recovery records. Supplemental rows cite that publication; unchanged rows retain original cutoffs.

**Do not sum this table.** Units differ and attempts reuse task structures. Completed usually means protocol endpoint, not legitimate task success. Missing includes assignments not started or still running at cutoff. Refused is explicit provider refusal only; — means unknown/not applicable. Invalid output, incorrect answer, appropriate abstention and unproductive action loops are distinct. Columns overlap; source details below each row settle their meaning.

| Experiment / attempt | Kind; model / backend | Evidence coverage | Unit | Planned | Started | Terminal | Valid | Completed¹ | Incomplete² | Refused | Errored | Missing | Task success³ | Qualification | Sources |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| 1. Avalon swarm prototype / consensus-v02 | scripted; trusted in-process scripted policies; no provider adapter / — | all 15 saved outcome JSONL rows and 15 planned configurations directly checked; stored source SHA256 matches retained code | Whole world; one seed per N/topology for scale and consensus, five paired seeds across 3 recovery arms for pilot | 15 | 15 | 15 | 15 | 15 | 0 | — | 0 | 0 | — | Reported 13 unit tests for v 0.2; no provider qualification. Thresholds provisional. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/tooling/avalon-swarm/RESULTS.md#L41-L65); [source 2](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/tooling/avalon-swarm/results/consensus-v02/outcomes.jsonl#L1-L15); [source 3](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/tooling/avalon-swarm/results/consensus-v02/plan.json#L1); [source 4](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/tooling/avalon-swarm/PROTOCOL.md#L75-L99) |
| 2. Avalon swarm prototype / prospective model track | unrun; no provider integration implemented / — | adapter specification only | Prospective world | — | 0 | 0 | — | 0 | — | — | — | — | — | No real-model qualification. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/tooling/avalon-swarm/ADAPTER.md#L1-L19); [source 2](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/tooling/avalon-swarm/PROTOCOL.md#L75-L81) |
| 3. Avalon swarm prototype / recovery-pilot | scripted; trusted in-process scripted policies; no provider adapter / — | all 15 saved outcome JSONL rows and 15 planned configurations directly checked; stored source SHA256 matches retained code | Whole world; one seed per N/topology for scale and consensus, five paired seeds across 3 recovery arms for pilot | 15 | 15 | 15 | 15 | 15 | 0 | — | 0 | 0 | — | Reported 13 unit tests for v 0.2; no provider qualification. Thresholds provisional. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/tooling/avalon-swarm/RESULTS.md#L19-L39); [source 2](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/tooling/avalon-swarm/results/recovery-pilot/outcomes.jsonl#L1-L15); [source 3](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/tooling/avalon-swarm/results/recovery-pilot/plan.json#L1); [source 4](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/tooling/avalon-swarm/PROTOCOL.md#L75-L99) |
| 4. Avalon swarm prototype / scale-final | scripted; trusted in-process scripted policies; no provider adapter / — | all 15 saved outcome JSONL rows and 15 planned configurations directly checked; stored source SHA256 matches retained code | Whole world; one seed per N/topology for scale and consensus, five paired seeds across 3 recovery arms for pilot | 15 | 15 | 15 | 15 | 15 | 0 | — | 0 | 0 | — | Reported 13 unit tests for v 0.2; no provider qualification. Thresholds provisional. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/tooling/avalon-swarm/RESULTS.md#L5-L17); [source 2](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/tooling/avalon-swarm/results/scale-final/outcomes.jsonl#L1-L15); [source 3](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/tooling/avalon-swarm/results/scale-final/plan.json#L1); [source 4](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/tooling/avalon-swarm/PROTOCOL.md#L75-L99) |
| 5. Capture and memory / S0 | scripted; deterministic tanh/FIFO policy; no model API / — | aggregate tables plus hub job summaries; no raw episode/request/response trace accessible locally | Arm episode; 50 task/randomness clusters, all cells and seeds paired within task | 600 | 600 | 600 | 600 | 600 | 0 | — | 0 | 0 | — | Scripted selftest 32 checks and S0 reported passed; hypothesis remains proposed; no confirmatory S2. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/shadow/notes/capture-memory/results/S0.md#L1-L3); [source 2](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/shadow/notes/capture-memory/results/S0_cells.csv#L1-L13); [source 3](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/shadow/notes/capture-memory/README.md#L115-L121); [source 4](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/shadow/notes/capture-memory/README.md#L342-L356) |
| 6. Capture and memory / S1 | scripted; deterministic tanh/FIFO policy; no model API / — | aggregate tables plus hub job summaries; no raw episode/request/response trace accessible locally | Arm episode; 100 task/randomness clusters, all cells and seeds paired within task | 9600 | 9600 | 9600 | 9600 | 9600 | 0 | — | 0 | 0 | — | Scripted selftest 32 checks and S0 reported passed; hypothesis remains proposed; no confirmatory S2. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/shadow/notes/capture-memory/results/S1.md#L1-L3); [source 2](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/shadow/notes/capture-memory/results/S1_cells.csv#L1-L49); [source 3](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/shadow/notes/capture-memory/README.md#L150-L180); [source 4](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/shadow/notes/capture-memory/README.md#L342-L356) |
| 7. Capture and memory / S1b | scripted; deterministic tanh/FIFO policy; no model API / — | aggregate tables plus hub job summaries; no raw episode/request/response trace accessible locally | Arm episode; 100 task/randomness clusters, all cells and seeds paired within task | 38400 | 38400 | 38400 | 38400 | 38400 | 0 | — | 0 | 0 | — | Scripted selftest 32 checks and S0 reported passed; hypothesis remains proposed; no confirmatory S2. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/shadow/notes/capture-memory/results/S1b.md#L1-L3); [source 2](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/shadow/notes/capture-memory/results/S1b_cells.csv#L1-L193); [source 3](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/shadow/notes/capture-memory/README.md#L185-L260); [source 4](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/shadow/notes/capture-memory/README.md#L342-L356) |
| 8. Capture and memory / prospective model pilot / S2 draft | unrun; unselected 7 B–9 B open instruct model; HTTP adapter exists but unrun / — | design and explicit unrun statements only | Draft 24 arm episodes:6 tasks×2 memories×2 arms; execution not scheduled | — | 0 | 0 | — | 0 | — | — | — | — | — | No model-specific calibration or qualification; S2 not implemented as a coordinator stage. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/shadow/notes/capture-memory/README.md#L287-L340); [source 2](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/shadow/notes/capture-memory/README.md#L358-L366); [source 3](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/shadow/notes/capture-memory/src/model.py#L1-L8) |
| 9. Collective sensing teaching example / offline demonstration | scripted; deterministic majority/deduplication rules / — | committed expected-summary.json and report; full 960 world/12480 event traces not found locally | 60 scenario clusters×4 paired repetitions×4 conditions; five dependent decisions per world | 960 | 960 | 960 | 960 | 960 | 0 | — | 0 | 0 | — | Reported offline replay, pairing, isolation and integrity checks; no model qualification. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/tooling/agent-experiments/examples/collective-sensing/RESULTS.md#L1-L20); [source 2](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/tooling/agent-experiments/examples/collective-sensing/expected-summary.json#L1-L25); [source 3](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/tooling/agent-experiments/examples/collective-sensing/PROTOCOL.md#L13-L36); [source 4](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/tooling/agent-experiments/VALIDATION.md#L5-L9) |
| 10. Collective sensing teaching example / prospective model protocol | unrun; unselected model/provider / — | protocol template, no request/response trace | Prospective scenario/world | — | 0 | 0 | — | 0 | — | — | — | — | — | No model pilot collected. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/tooling/agent-experiments/examples/collective-sensing/PROTOCOL.md#L30-L47) |
| 11. Distributed worker teaching template / S0 | scripted; programmed plurality and evidence-root quorum / — | all 84 hub job summaries in frozen public snapshot plus source/design; no local episodes.jsonl | Arm episode; task is cluster; S0=50 tasks, S1=200 tasks, S2=300 tasks | 100 | 100 | 100 | — | 100 | 0 | — | — | 0 | — | Toy clean qualification and template selftests; no model qualification. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/templates/experiment-worker/README.md#L9-L24); [source 2](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/templates/experiment-worker/README.md#L153-L159); [source 3](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/templates/experiment-worker/design.yaml#L20-L46) |
| 12. Distributed worker teaching template / S1 | scripted; programmed plurality and evidence-root quorum / — | all 84 hub job summaries in frozen public snapshot plus source/design; no local episodes.jsonl | Arm episode; task is cluster; S0=50 tasks, S1=200 tasks, S2=300 tasks | 3200 | 3200 | 3200 | — | 3200 | 0 | — | — | 0 | — | Toy clean qualification and template selftests; no model qualification. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/templates/experiment-worker/README.md#L9-L24); [source 2](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/templates/experiment-worker/README.md#L153-L159); [source 3](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/templates/experiment-worker/design.yaml#L20-L46) |
| 13. Distributed worker teaching template / S2 | scripted; programmed plurality and evidence-root quorum / — | all 84 hub job summaries in frozen public snapshot plus source/design; no local episodes.jsonl | Arm episode; task is cluster; S0=50 tasks, S1=200 tasks, S2=300 tasks | 7200 | 7200 | 7200 | — | 7200 | 0 | — | — | 0 | — | Toy clean qualification and template selftests; no model qualification. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/templates/experiment-worker/README.md#L9-L24); [source 2](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/templates/experiment-worker/README.md#L153-L159); [source 3](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/templates/experiment-worker/design.yaml#L20-L46) |
| 14. Poietic Agents / prospective-v0.1 / S0-01 assessment (unrun) | unrun; Unpinned intended capable generalist, cheaper generative executor (Haiku or Qwen suggested), optional separately qualified Jev typed-choice component; no served model or provider response evidence. / — | Local design, registration document, contracts, author pre-run assessment and explicit launch state; no implementation or run outputs in this study directory. | Frozen/queued experimental run (not proposed logical request, job, identity or workload root) | 0 | 0 | 0 | 0 | 0 | 0 | — | 0 | 0 | — | Not run. Design review pending, exact runtime unresolved, offline checks unimplemented, prior-art survey incomplete, no accepted hypothesis, no spend authorization or machine allocation. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/vishesh/notes/poietic-agents/README.md#L3-L7); [source 2](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/vishesh/notes/poietic-agents/README.md#L22-L26); [source 3](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/vishesh/notes/poietic-agents/launch-state.json#L3-L33); [source 4](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/vishesh/notes/poietic-agents/design.yaml#L92-L135); [source 5](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/vishesh/notes/poietic-agents/registration.json#L1-L7); [source 6](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/vishesh/notes/poietic-agents/reviews/S0-01-pre.md#L5-L17); [source 7](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/vishesh/notes/poietic-agents/reviews/S0-01-pre.md#L27-L37) |
| 15. Shadow proposed board studies / proposal only | unrun; unselected open model / — | hypothesis text only; no matching experiment root or hub registration found | Prospective population/world; no completed assignment | — | 0 | 0 | — | 0 | — | — | — | — | — | Status proposed; no launch qualification evidenced. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/hypotheses/shadow-board-nsweep.md#L1-L22) |
| 16. Shadow proposed board studies / proposal only | unrun; unselected open model / — | hypothesis text only; no matching experiment root or hub registration found | Prospective population/world; no completed assignment | — | 0 | 0 | — | 0 | — | — | — | — | — | Status proposed; no launch qualification evidenced. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/hypotheses/shadow-neff-evidence-board.md#L1-L22) |
| 17. adaptive-quorum-repair-v3 / D0 | model; convaiinnovations/laya with deterministic scaffolding / local | tracked post-mortem and/or saved summary; no full request/response journal inspected | qualificationitem | 56 | 56 | 56 | 56 | 56 | 0 | — | 0 | 0 | — | fail | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/adaptive-quorum-v2/repair-v3/reviews/D0-post.md#L3) |
| 18. adaptive-quorum-repair-v3 / Q1 | model; convaiinnovations/laya with deterministic scaffolding / local | tracked post-mortem and/or saved summary; no full request/response journal inspected | qualificationitem | 22 | 22 | 22 | 22 | 22 | 0 | — | 0 | 0 | — | fail | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/adaptive-quorum-v2/repair-v3/reviews/Q1-post.md#L3) |
| 19. adaptive-quorum-repair-v3 / Q2 | model; convaiinnovations/laya with deterministic scaffolding / local | tracked post-mortem and/or saved summary; no full request/response journal inspected | qualificationitem | 22 | 22 | 22 | 22 | 22 | 0 | — | 0 | 0 | — | pass | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/adaptive-quorum-v2/repair-v3/reviews/Q2-post.md#L3) |
| 20. adaptive-quorum-repair-v3 / S1-attempt-1 | model; Laya+symbolicpolicy / local | tracked post-mortem and/or saved summary; no full request/response journal inspected | pairedblock | 384 | 25 | 25 | 25 | 25 | 0 | — | — | 359 | — | artifact failure interrupts execution | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/adaptive-quorum-v2/repair-v3/reviews/S1-attempt-1-post.md#L3) |
| 21. adaptive-quorum-repair-v3 / S1-attempt-2 | model; Laya+symbolicpolicy / local | tracked post-mortem and/or saved summary; no full request/response journal inspected | pairedblock (12taskclusters) | 384 | 384 | 384 | 384 | 384 | 0 | — | 0 | 0 | — | execution passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/adaptive-quorum-v2/repair-v3/reviews/S1-attempt-2-post.md#L3) |
| 22. adaptive-quorum-v1 / laya-S0 | model; convaiinnovations/laya / laya | tracked post-mortem and/or saved summary; no full request/response journal inspected | policy outcome (36pairedtapes,6taskclusters) | 144 | 144 | 144 | 144 | 144 | 0 | — | 0 | 0 | — | narrow clean gate passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/adaptive-quorum/results/S0.md#L16) |
| 23. adaptive-quorum-v1 / scripted-S0 | scripted; not applicable / scripted | tracked post-mortem and/or saved summary; no full request/response journal inspected | policy outcome (36pairedtapes,6taskclusters) | 144 | 144 | 144 | 144 | 144 | 0 | — | 0 | 0 | — | narrow clean gate passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/adaptive-quorum/results/S0.md#L16) |
| 24. adaptive-quorum-v1 / wheel-init-failure | unrun; not applicable / None | tracked post-mortem and/or saved summary; no full request/response journal inspected | episode | — | 0 | 0 | 0 | 0 | 0 | — | — | — | — | setup failure | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/adaptive-quorum/results/S0.md#L5) |
| 25. adaptive-quorum-v1 / wrapper-import-failure | unrun; not applicable / None | tracked post-mortem and/or saved summary; no full request/response journal inspected | episode | — | 0 | 0 | 0 | 0 | 0 | — | — | — | — | setup failure | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/adaptive-quorum/results/S0.md#L5) |
| 26. adaptive-quorum-v2 / laya-S0 | model; convaiinnovations/laya / laya | tracked post-mortem and/or saved summary; no full request/response journal inspected | policy outcome (6taskclusters) | 168 | 168 | 168 | 168 | 168 | 0 | — | 0 | 0 | — | scripted passes; Laya clean gate fails | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/adaptive-quorum-v2/results/laya-analysis.md#L5); [source 2](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/adaptive-quorum-v2/repair-v3/AUDIT.md#L17) |
| 27. adaptive-quorum-v2 / scripted-S0 | scripted; not applicable / scripted | tracked post-mortem and/or saved summary; no full request/response journal inspected | policy outcome (6taskclusters) | 168 | 168 | 168 | 168 | 168 | 0 | — | 0 | 0 | — | scripted passes; Laya clean gate fails | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/adaptive-quorum-v2/results/laya-analysis.md#L5); [source 2](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/adaptive-quorum-v2/repair-v3/AUDIT.md#L17) |
| 28. antsy-receipt-v6 / E0-attempt-1 | scripted; not applicable / Tesseract OCR plus deterministic policies and evaluator; zero decision-model/API calls | Committed post-mortem, summary and reconciliation audit inspected; retained public records are numeric. Underlying private images/TSV were not independently reopened. | development receipt (20 receipts,100 OCR subprocess calls,100 deterministic policy outcomes) | 20 | 20 | 20 | 20 | 20 | 0 | — | 0 | 0 | — | FAILED instrument qualification: all 20 reference totals were read from the wrong CORD field; no usable accuracy endpoint. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/vishesh/notes/antsy-receipt-v6/reviews/E0-post.md#L3); [source 2](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/vishesh/notes/antsy-receipt-v6/results/E0-attempt-1/summary.json#L1); [source 3](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/vishesh/notes/antsy-receipt-v6/results/E0-attempt-1/audit.json#L1) |
| 29. antsy-verification-v4 / D1-Jev | model; typesafe/jev-1.13 / OpenRouter Decisions/TypeSafe | tracked post-mortem and/or saved summary; no full request/response journal inspected | decisiondiagnostic | 1 | 1 | 1 | 1 | 1 | 0 | — | 0 | 0 | — | Execution/interface qualification passed at the stated stage; no committee benefit established. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/antsy-verification-v4/RESULTS.md#L7) |
| 30. antsy-verification-v4 / E0 | scripted; Tesseract / local | tracked post-mortem and/or saved summary; no full request/response journal inspected | receiptblock | 100 | 100 | 100 | 100 | 100 | 0 | — | 0 | 0 | — | Execution/interface qualification passed at the stated stage; no committee benefit established. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/antsy-verification-v4/RESULTS.md#L7) |
| 31. antsy-verification-v4 / J0-Jev | model; typesafe/jev-1.13 / OpenRouter Decisions/TypeSafe | tracked post-mortem and/or saved summary; no full request/response journal inspected | decisiondiagnostic | 16 | 16 | 16 | 16 | 16 | 0 | — | 0 | 0 | — | Execution/interface qualification passed at the stated stage; no committee benefit established. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/antsy-verification-v4/RESULTS.md#L7) |
| 32. antsy-verification-v4 / S0-Jev-attempt-1 | model; typesafe/jev-1.13 / OpenRouter Decisions/TypeSafe | tracked post-mortem and/or saved summary; no full request/response journal inspected | receiptblock; faileddecisionnestedinpartial6th | 10 | 6 | 5 | 5 | 5 | 1 | — | 1 | 5 | — | failedpreserved;laterreplayed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/antsy-verification-v4/RESULTS.md#L16) |
| 33. antsy-verification-v4 / S0-Jev-attempt-2 | model; typesafe/jev-1.13 / OpenRouter Decisions/TypeSafe | tracked post-mortem and/or saved summary; no full request/response journal inspected | receiptblock; faileddecisionnestedinpartial6th | 10 | 6 | 5 | 5 | 5 | 1 | — | 1 | 5 | — | failedpreserved;laterreplayed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/antsy-verification-v4/RESULTS.md#L16) |
| 34. antsy-verification-v4 / S0-Jev-attempt-3 | model; typesafe/jev-1.13 / OpenRouter Decisions/TypeSafe | tracked post-mortem and/or saved summary; no full request/response journal inspected | receiptblock | 10 | 10 | 10 | 10 | 10 | 0 | — | 0 | 0 | — | Execution/interface qualification passed at the stated stage; no committee benefit established. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/antsy-verification-v4/RESULTS.md#L7) |
| 35. antsy-verification-v4 / S0-Laya | model; convaiinnovations/laya / local | tracked post-mortem and/or saved summary; no full request/response journal inspected | receiptblock | 10 | 10 | 10 | 10 | 10 | 0 | — | 0 | 0 | — | Execution/interface qualification passed at the stated stage; no committee benefit established. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/antsy-verification-v4/RESULTS.md#L7) |
| 36. antsy-verification-v4 / S1-Jev | model; typesafe/jev-1.13 / OpenRouter Decisions/TypeSafe | All 840 saved model receipts and 70 episode journals per backend inspected: actual numeric inputs, choices and probabilities. Jev receipts include provider/model/usage fields. These are parsed records, not raw HTTP bytes. | pairedreceiptblock (same70receiptsbothmodels;490rowsperbackend) | 70 | 70 | 70 | 70 | 70 | 0 | 0 | 0 | 0 | — | Execution/interface qualification passed at the stated stage; no committee benefit established. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/antsy-verification-v4/RESULTS.md#L26); [source 2](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/antsy-verification-v4/results/S1-jev-attempt-1/receipts.json.gz#L1) |
| 37. antsy-verification-v4 / S1-Laya | model; convaiinnovations/laya / local CPU | All 840 saved model receipts and 70 episode journals per backend inspected: actual numeric inputs, choices and probabilities. Jev receipts include provider/model/usage fields. These are parsed records, not raw HTTP bytes. | pairedreceiptblock (same70receiptsbothmodels;490rowsperbackend) | 70 | 70 | 70 | 70 | 70 | 0 | 0 | 0 | 0 | — | Execution/interface qualification passed at the stated stage; no committee benefit established. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/antsy-verification-v4/RESULTS.md#L26); [source 2](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/antsy-verification-v4/results/S1-attempt-1/receipts.json.gz#L1) |
| 38. antsy-verification-v4 / S1-comparison | scripted; not applicable / None | tracked post-mortem and/or saved summary; no full request/response journal inspected | same pairedreceipt (derivedanalysis) | 70 | 70 | 70 | 70 | 70 | 0 | — | 0 | 0 | — | Execution/interface qualification passed at the stated stage; no committee benefit established. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/antsy-verification-v4/results/comparison/comparison.json#L1) |
| 39. antsy-verification-v5 / D0-attempt-1 | scripted; not applicable / deterministicreplay | tracked post-mortem and/or saved summary; no full request/response journal inspected | reanalysis row (70same receipts) | 2940 | 2940 | 2940 | 2940 | 2940 | 0 | — | 0 | 0 | — | Offline reanalysis only; fresh native validation remains unrun. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/antsy-verification-v5/RESULTS.md#L3); [source 2](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/antsy-verification-v5/results/D0-attempt-1/traces.json.gz#L1) |
| 40. antsy-verification-v5 / D1-attempt-1 | scripted; not applicable / deterministicreplay | tracked post-mortem and/or saved summary; no full request/response journal inspected | reanalysis row (70same receipts) | 1400 | 1400 | 1400 | 1400 | 1400 | 0 | — | 0 | 0 | — | Offline reanalysis only; fresh native validation remains unrun. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/antsy-verification-v5/RESULTS.md#L3); [source 2](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/antsy-verification-v5/results/D1-attempt-1/traces.json.gz#L1) |
| 41. cloud-discussion-d1 / access-preparation | unrun; not applicable / None | plan_only | preparation record | — | — | — | — | — | — | — | — | — | — | access_and_lifecycle_unverified | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/agents/cloud-discussion-d1.md#L1) |
| 42. compositional-safety / i0-001 | model; claude-sonnet-5-5 / Anthropic | Saved packet, parsed answer/partial text and explicit stop metadata; no full HTTP envelope. | one deliberately repeated atomic fixture call, not an episode | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | — | compatibility diagnostic only; Q0 still failed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/compositional-safety/reviews/i0-001-post.md) |
| 43. compositional-safety / i0-002 | model; claude-sonnet-5 / Anthropic | Saved packet, parsed answer/partial text and explicit stop metadata; no full HTTP envelope. | one deliberately repeated atomic fixture call, not an episode | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | — | compatibility diagnostic only; Q0 still failed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/compositional-safety/reviews/i0-002-post.md) |
| 44. compositional-safety / i0-003-clarified | model; claude-sonnet-5 / Anthropic | Actual 8 credential-free request bodies plus responses/stop metadata; all23 diagnostic files hash verified; exact paired packet differences checked. | one-decision request on selected reused parent state | 8 | 8 | 8 | 8 | 8 | 0 | 0 | 0 | 0 | 3 | failed unchanged8/8 advancing screen; no full Q0/P1 | [source 1](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/dmarz/notes/compositional-safety/reviews/i0-003-post.md) |
| 45. compositional-safety / i0-003-original | model; claude-sonnet-5 / Anthropic | Actual 8 credential-free request bodies plus responses/stop metadata; all23 diagnostic files hash verified; exact paired packet differences checked. | one-decision request on selected reused parent state | 8 | 8 | 8 | 6 | 6 | 0 | 2 | 2 | 0 | 0 | failed unchanged8/8 advancing screen; no full Q0/P1 | [source 1](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/dmarz/notes/compositional-safety/reviews/i0-003-post.md) |
| 46. compositional-safety / i0-004-plan | unrun; claude-haiku-4-5-20251001 planned / Anthropic planned | Pre-run plan only at publication source cutoff. | one-decision request on reused parent state | 16 | 0 | 0 | 0 | 0 | 0 | — | 0 | 16 | — | planned; no outcome evidence inspected | [source 1](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/dmarz/notes/compositional-safety/reviews/i0-004-pre.md) |
| 47. compositional-safety / q0-001 | model; claude-haiku-4-5-20251001 / anthropic | Saved actor observations, parsed answers, events and selected provider metadata; full HTTP bodies not retained. Frozen source replays every packet, action and score. | paired world-arm episode | 24 | 24 | 24 | 22 | 22 | 0 | 0 | 2 | 0 | 21 | failed unchanged Q0 gate; no P1/S1/S2 | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/compositional-safety/reviews/q0-001-post.md); [source 2](./evidence/compositional-replay.json); [source 3](./evidence/independent-check.json) |
| 48. compositional-safety / q0-002 | model; claude-haiku-4-5-20251001 / anthropic | Saved actor observations, parsed answers, events and selected provider metadata; full HTTP bodies not retained. Frozen source replays every packet, action and score. | paired world-arm episode | 24 | 24 | 24 | 24 | 20 | 4 | 0 | 0 | 0 | 20 | failed unchanged Q0 gate; no P1/S1/S2 | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/compositional-safety/reviews/q0-002-post.md); [source 2](./evidence/compositional-replay.json); [source 3](./evidence/independent-check.json) |
| 49. compositional-safety / q0-003 | model; claude-sonnet-5-5 / anthropic | Saved actor observations, parsed answers, events and selected provider metadata; full HTTP bodies not retained. Frozen source replays every packet, action and score. | paired world-arm episode | 24 | 24 | 24 | 16 | 16 | 0 | — | 8 | 0 | 16 | failed unchanged Q0 gate; no P1/S1/S2 | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/compositional-safety/reviews/q0-003-post.md); [source 2](./evidence/compositional-replay.json); [source 3](./evidence/independent-check.json) |
| 50. compositional-safety / q0-004 | model; claude-sonnet-5 / anthropic | Saved actor observations, parsed answers, events and selected provider metadata; full HTTP bodies not retained. Frozen source replays every packet, action and score. | paired world-arm episode | 24 | 24 | 24 | 22 | 10 | 12 | 2 | 2 | 0 | 10 | failed unchanged Q0 gate; no P1/S1/S2 | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/compositional-safety/reviews/q0-004-post.md); [source 2](./evidence/compositional-replay.json); [source 3](./evidence/independent-check.json) |
| 51. compositional-safety / s0-001 | scripted; not applicable / scripted | Saved actor observations, parsed answers, events and selected provider metadata; full HTTP bodies not retained. Frozen source replays every packet, action and score. | paired world-arm episode | 84 | 84 | 84 | 84 | 84 | 0 | — | 0 | 0 | 84 | scripted engineering passed; no model competence evidence | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/compositional-safety/reviews/s0-001-post.md); [source 2](./evidence/compositional-replay.json); [source 3](./evidence/independent-check.json) |
| 52. discussion-dose / 00820f46 | model; claude-haiku-4-5-20251001 / anthropic | report_and_hub | team episode | 8 | 8 | 8 | 8 | 8 | 0 | — | 0 | 0 | 8 | passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/discussion-dose/RESULTS-AND-REFLECTION.md#L54) |
| 53. discussion-dose / 1443b334 | scripted; not applicable / scripted | report_and_hub | team episode | 48 | 48 | 48 | — | 48 | 0 | — | — | 0 | — | computation_complete_reporting_failed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/discussion-dose/RESULTS-AND-REFLECTION.md#L54) |
| 54. discussion-dose / 3e4b084a | model; claude-haiku-4-5-20251001 / anthropic | report_and_hub | team episode | 48 | 48 | 48 | 40 | 40 | 8 | — | 8 | 0 | 39 | failed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/discussion-dose/RESULTS-AND-REFLECTION.md#L54) |
| 55. discussion-dose / 6c9284c3 | model; claude-haiku-4-5-20251001 / anthropic | report_and_hub | team episode | — | — | — | — | — | — | — | — | — | — | startup_failed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/discussion-dose/RESULTS-AND-REFLECTION.md#L54) |
| 56. discussion-dose / 775e3cd6 | model; claude-haiku-4-5-20251001 / anthropic | report_and_hub | team episode | 8 | — | 8 | 0 | 0 | — | — | — | 0 | — | blocked_billing | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/discussion-dose/RESULTS-AND-REFLECTION.md#L54) |
| 57. discussion-dose / 863006ea | model; claude-haiku-4-5-20251001 / anthropic | report_and_hub | team episode | 48 | 48 | 48 | 48 | 48 | 0 | — | 0 | 0 | 48 | passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/discussion-dose/RESULTS-AND-REFLECTION.md#L54); [source 2](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/discussion-dose/reviews/qualification-v3-post.md#L1) |
| 58. discussion-dose / billing-diagnostic | model; claude-haiku-4-5-20251001 / anthropic | report_and_hub | provider request | — | — | — | — | — | — | — | — | — | — | provider_billing_rejection | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/discussion-dose/RESULTS-AND-REFLECTION.md#L54) |
| 59. discussion-dose / c1d09e7d | scripted; not applicable / scripted | report_and_hub | team episode | 8 | 8 | 8 | 8 | 8 | 0 | — | 0 | 0 | — | passed_transport | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/discussion-dose/RESULTS-AND-REFLECTION.md#L54) |
| 60. discussion-dose / format-regression-probe | model; claude-haiku-4-5-20251001 / anthropic | report_and_hub | provider request | 1 | 1 | 1 | 1 | 1 | 0 | — | 0 | 0 | — | format_probe_passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/discussion-dose/RESULTS-AND-REFLECTION.md#L54) |
| 61. discussion-dose-v2 / 06699b02 | model; claude-haiku-4-5-20251001 / anthropic | report_and_hub | team episode | 24 | 24 | 24 | 23 | 23 | 1 | — | 1 | 0 | 15 | failed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/discussion-dose/RESULTS-V2.md#L7) |
| 62. discussion-dose-v2 / 0cfb900e | model; claude-haiku-4-5-20251001 / anthropic | report_and_hub | team episode | 24 | 24 | 24 | 24 | 24 | 0 | — | 0 | 0 | 9 | failed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/discussion-dose/RESULTS-V2.md#L7) |
| 63. discussion-dose-v2 / 14b3bd88 | model; claude-haiku-4-5-20251001 / anthropic | report_and_hub | team episode | 24 | 24 | 24 | 24 | 24 | 0 | — | 0 | 0 | 15 | passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/discussion-dose/RESULTS-V2.md#L7) |
| 64. discussion-dose-v2 / 1f1e2f69 | model; claude-haiku-4-5-20251001 / anthropic | report_and_hub | team episode | 24 | 24 | 24 | 23 | 23 | 1 | — | 1 | 0 | 13 | failed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/discussion-dose/RESULTS-V2.md#L7) |
| 65. discussion-dose-v2 / 723dad8e | model; claude-haiku-4-5-20251001 / anthropic | report_and_hub | team episode | 48 | 48 | 48 | 44 | 44 | 4 | — | 4 | 0 | — | failed_validity | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/discussion-dose/RESULTS-V2.md#L7); [source 2](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/discussion-dose/reviews/v2-s0-H4-post.md#L1) |
| 66. discussion-dose-v2 / d0725be0 | model; claude-haiku-4-5-20251001 / anthropic | report_and_hub | team episode | 24 | 24 | 24 | 23 | 23 | 1 | — | 1 | 0 | 17 | passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/discussion-dose/reviews/pc-H4-a1-post.md#L1) |
| 67. discussion-dose-v2 / d3cb8c02 | model; claude-haiku-4-5-20251001 / anthropic | report_and_hub | team episode | 24 | 24 | 24 | 23 | 23 | 1 | — | 1 | 0 | 17 | failed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/discussion-dose/RESULTS-V2.md#L7) |
| 68. discussion-dose-v2 / d42f5357 | model; claude-haiku-4-5-20251001 / anthropic | report_and_hub | team episode | 24 | 24 | 24 | 21 | 21 | 3 | — | 3 | 0 | 8 | failed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/discussion-dose/RESULTS-V2.md#L7) |
| 69. discussion-dose-v2 / v2.1-keyed-claims | unrun; not applicable / None | plan_only | shelved code proposal, not a model run | — | — | — | — | — | — | — | — | — | — | untested_shelved_handoff | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/discussion-dose/benchmark-v3/OFFLINE-VALIDATION.md#L43) |
| 70. discussion-dose-v3 / initial-prototype-708 | scripted; not applicable / scripted | report_and_hub | assigned case record (heterogeneous swarm, diagnostic and memory-fixture protocols) | — | — | — | — | — | — | — | — | — | — | not_assessed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/discussion-dose/benchmark-v3/OFFLINE-VALIDATION.md#L7) |
| 71. discussion-dose-v3 / intermediate-636-development | scripted; not applicable / scripted | report_and_hub | assigned case record (heterogeneous swarm, diagnostic and memory-fixture protocols) | — | — | — | — | — | — | — | — | — | — | not_assessed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/discussion-dose/benchmark-v3/OFFLINE-VALIDATION.md#L39) |
| 72. discussion-dose-v3 / proposed-E1 | unrun; not applicable / None | publication_postmortem_and_deployment_only | proposed physical model request | 252 | 0 | 0 | 0 | 0 | 0 | — | 0 | 252 | — | proposed_not_authorized_not_launched | [source 1](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/dmarz/notes/discussion-dose/NEXT-EXPERIMENTS.md#L1); [source 2](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/dmarz/notes/discussion-dose/NEXT-EXPERIMENTS.md#L14) |
| 73. discussion-dose-v3 / proposed-E2 | unrun; not applicable / None | publication_postmortem_and_deployment_only | proposed physical model request | 252 | 0 | 0 | 0 | 0 | 0 | — | 0 | 252 | — | proposed_not_authorized_not_launched | [source 1](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/dmarz/notes/discussion-dose/NEXT-EXPERIMENTS.md#L1); [source 2](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/dmarz/notes/discussion-dose/NEXT-EXPERIMENTS.md#L33) |
| 74. discussion-dose-v3 / proposed-E3 | unrun; not applicable / None | publication_postmortem_and_deployment_only | proposed physical model request | — | 0 | 0 | 0 | 0 | 0 | — | 0 | — | — | proposed_not_authorized_not_launched | [source 1](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/dmarz/notes/discussion-dose/NEXT-EXPERIMENTS.md#L1); [source 2](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/dmarz/notes/discussion-dose/NEXT-EXPERIMENTS.md#L37) |
| 75. discussion-dose-v3 / proposed-E4 | unrun; not applicable / None | publication_postmortem_and_deployment_only | proposed physical model request | — | 0 | 0 | 0 | 0 | 0 | — | 0 | — | — | proposed_not_authorized_not_launched | [source 1](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/dmarz/notes/discussion-dose/NEXT-EXPERIMENTS.md#L1); [source 2](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/dmarz/notes/discussion-dose/NEXT-EXPERIMENTS.md#L46) |
| 76. discussion-dose-v3 / release-verified | scripted; not applicable / scripted | report_and_hub | assigned case record (heterogeneous swarm, diagnostic and memory-fixture protocols) | 96 | 96 | 96 | 96 | 96 | 0 | — | 0 | 0 | — | software_passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/discussion-dose/reviews/v3-offline-post.md#L1) |
| 77. discussion-dose-v3 / v3-d1-a1 | unrun; not applicable / None | plan_only | proposed physical model request | 120 | 0 | 0 | 0 | 0 | 0 | — | 0 | 120 | — | planned_not_launched | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/discussion-dose/benchmark-v3/NEXT-RUN.md#L1) |
| 78. discussion-dose-v3 / v3-d2-conditional | unrun; not applicable / None | plan_only | proposed physical model request | 48 | 0 | 0 | 0 | 0 | 0 | — | 0 | 48 | — | planned_not_launched | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/discussion-dose/benchmark-v3/NEXT-RUN.md#L1) |
| 79. discussion-dose-v3 / v3-fresh-qualification-conditional | unrun; not applicable / None | plan_only | proposed physical model request | 60 | 0 | 0 | 0 | 0 | 0 | — | 0 | 60 | — | planned_not_launched | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/discussion-dose/benchmark-v3/NEXT-RUN.md#L1) |
| 80. discussion-dose-v3 / v3-q0-a1 | model; claude-haiku-4-5-20251001 / anthropic | saved_actor_request_and_final_response_journal | assigned case record (heterogeneous swarm, diagnostic and memory-fixture protocols) | 96 | 96 | 96 | 96 | 96 | 0 | — | 0 | 0 | — | failed_clean_competence | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/discussion-dose/reviews/v3-q0-a1-post.md#L1) |
| 81. discussion-dose-v3 / vishesh-fixes-a1 | scripted; not applicable / scripted | report_and_hub | assigned case record (heterogeneous swarm, diagnostic and memory-fixture protocols) | 96 | 96 | 96 | 96 | 96 | 0 | — | 0 | 0 | — | software_passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/discussion-dose/reviews/v3-vishesh-fixes-post.md#L1) |
| 82. discussion-v3-resample / 1004-030243-d6fa86 | model; claude-haiku-4-5-20251001 / anthropic | saved_actor_request_and_final_response_journal | swarm episode | 72 | 72 | 72 | 72 | 72 | 0 | — | 0 | 0 | 23 | failed_clean_reports | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/discussion-dose/reviews/resample-v3-a1-post.md#L1) |
| 83. distributed-evidence-suite / draft | unrun; not applicable / None | plan_only | episode or structured observation; see independent_unit | — | — | — | — | — | — | — | — | — | — | documentation_only | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/distributed-evidence-suite/README.md#L1) |
| 84. external-influence-v1 / native-S0 | model; claude-haiku-4-5-20251001 (configured) / Anthropic | tracked post-mortem and/or saved summary; no full request/response journal inspected | episode | 7 | 7 | 7 | 7 | 7 | 0 | — | 0 | 0 | — | narrow clean control passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/external-influence-v2/README.md#L16) |
| 85. external-influence-v1 / scripted-S0 | scripted; not applicable / scripted | tracked post-mortem and/or saved summary; no full request/response journal inspected | episode | 84 | 84 | 84 | 84 | 84 | 0 | — | 0 | 0 | — | engineering only | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/actual-experiments/DEPLOYMENT.md#L17) |
| 86. external-influence-v1 / scripted-S1 | scripted; not applicable / scripted | tracked post-mortem and/or saved summary; no full request/response journal inspected | episode | 3024 | 3024 | 3024 | 3024 | 3024 | 0 | — | 0 | 0 | — | engineering only | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/actual-experiments/DEPLOYMENT.md#L17) |
| 87. external-influence-v2 / local-D0 | model; qwen3:0.6b / Ollama/local | Authenticated saved manifest and summary inspected; no actual request/response trace available through hub catalogue. | episode | 4 | 4 | 4 | 0 | 0 | 0 | — | 4 | 0 | — | Diagnostic only; qualification is null, not a passed gate. |  |
| 88. external-influence-v2 / local-Q0 | model; qwen3:0.6b / Ollama/local | tracked post-mortem and/or saved summary; no full request/response journal inspected | episode | 6 | 6 | 6 | 0 | 0 | 0 | — | 6 | 0 | — | failed; no S1 | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/external-influence-v2/local-agents/reviews/Q0-post.md#L7) |
| 89. external-influence-v2 / local-Q1 | model; qwen3:1.7b / Ollama/local | Authenticated saved manifest and summary inspected; no actual request/response trace available through hub catalogue. | episode | 6 | 6 | 6 | 3 | 3 | 0 | — | 3 | 0 | — | failed; no S1 |  |
| 90. external-influence-v2 / local-S1 | unrun; not applicable / None | tracked post-mortem and/or saved summary; no full request/response journal inspected | episode | 50 | 0 | 0 | 0 | 0 | 0 | — | — | 50 | — | blocked on competence | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/external-influence-v2/local-agents/PLAN.md#L21) |
| 91. external-influence-v2 / native-S0 | model; claude-haiku-4-5-20251001 (configured) / Anthropic | tracked post-mortem and/or saved summary; no full request/response journal inspected | episode | 4 | 4 | 4 | 4 | 4 | 0 | — | 0 | 0 | — | not established | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/external-influence-v2/reviews/quality-post.md#L21) |
| 92. external-influence-v2 / native-S1 | model; claude-haiku-4-5-20251001 (configured) / Anthropic | All 50 derived episode replay records inspected; complete raw request wire not archived here. | episode | 50 | 50 | 50 | 50 | 50 | 0 | — | 0 | 0 | — | format passes; baseline competence and scientific identifiability weak | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/external-influence-v2/reviews/quality-post.md#L23); [source 2](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/artifacts/influence-swarms-replay/influence-swarms-replay-v1.html#L1) |
| 93. external-influence-v2 / scripted-robustness | scripted; not applicable / scripted | tracked post-mortem and/or saved summary; no full request/response journal inspected | episode | 2700 | 2700 | 2700 | 2700 | 2700 | 0 | — | 0 | 0 | — | not established | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/external-influence-v2/reviews/quality-post.md#L11) |
| 94. healing-helping-hands / diagnostic-03 | model; Qwen/Laya / local | tracked post-mortem and/or saved summary; no full request/response journal inspected | classification | 54 | 54 | 54 | 54 | 54 | 0 | — | 0 | 0 | — | semantic qualification fails | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/healing-helping-hands/reviews/diagnostic-03-post.md#L5) |
| 95. healing-helping-hands / diagnostic-04 | model; Qwen/Laya / local | tracked post-mortem and/or saved summary; no full request/response journal inspected | classification | 36 | 36 | 36 | 36 | 36 | 0 | — | 0 | 0 | — | semantic qualification fails | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/healing-helping-hands/reviews/diagnostic-04-post.md#L5) |
| 96. healing-helping-hands / jev-qualification-01 | model; typesafe/jev-1.13 / OpenRouter Decisions | tracked post-mortem and/or saved summary; no full request/response journal inspected | classification | 60 | 60 | 60 | 60 | 60 | 0 | — | 0 | 0 | — | clean accuracy passes; order control invalid | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/healing-helping-hands/reviews/jev-qualification-01-post.md#L5) |
| 97. healing-helping-hands / pilot-01 | scripted; not applicable / exact deterministic extraction | tracked post-mortem and/or saved summary; no full request/response journal inspected | world assignment; exact/model subcounts explicitly listed | 144 | 36 | 36 | 36 | 36 | 0 | — | 0 | 108 | — | Model qualification failed for at least one required backend; only exact-extraction downstream worlds executed. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/healing-helping-hands/ATTEMPT-01-REVIEW.md#L3) |
| 98. healing-helping-hands / pilot-01-qualification | model; Qwen and Laya / local Qwen/Laya; OpenRouter Decisions Jev | tracked post-mortem and/or saved summary; no full request/response journal inspected | one balanced support/refutation/uncertainty classification | 60 | 60 | 60 | 60 | 60 | 0 | — | 0 | 0 | — | Failed required per-class semantic competence. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/healing-helping-hands/ATTEMPT-01-REVIEW.md#L3) |
| 99. healing-helping-hands / pilot-02 | scripted; not applicable / exact deterministic extraction | tracked post-mortem and/or saved summary; no full request/response journal inspected | world assignment; exact/model subcounts explicitly listed | 144 | 36 | 36 | 36 | 36 | 0 | — | 0 | 108 | — | Model qualification failed for at least one required backend; only exact-extraction downstream worlds executed. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/healing-helping-hands/reviews/pilot-02-post.md#L9) |
| 100. healing-helping-hands / pilot-02-qualification | model; Qwen and Laya / local Qwen/Laya; OpenRouter Decisions Jev | tracked post-mortem and/or saved summary; no full request/response journal inspected | one balanced support/refutation/uncertainty classification | 120 | 120 | 120 | 120 | 120 | 0 | — | 0 | 0 | — | Failed required per-class semantic competence. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/healing-helping-hands/reviews/pilot-02-post.md#L9) |
| 101. healing-helping-hands / pilot-03 | model; typesafe/jev-1.13 (36 worlds); other36 exact-extraction worlds / exact deterministic extraction plus Jev Decisions API | tracked post-mortem and/or saved summary; no full request/response journal inspected | world assignment; exact/model subcounts explicitly listed | 180 | 72 | 72 | 72 | 72 | 0 | — | 0 | 108 | — | Jev extraction qualification passed; the propagation result remains a small synthetic policy comparison. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/healing-helping-hands/reviews/pilot-03-post.md#L9) |
| 102. healing-helping-hands / pilot-03-qualification | model; typesafe/jev-1.13 / local Qwen/Laya; OpenRouter Decisions Jev | tracked post-mortem and/or saved summary; no full request/response journal inspected | one balanced support/refutation/uncertainty classification | 60 | 60 | 60 | 60 | 60 | 0 | — | 0 | 0 | — | Passed 60/60 fresh Jev classification screen. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/healing-helping-hands/reviews/pilot-03-post.md#L9) |
| 103. healing-helping-hands / practical-01 | scripted; not applicable / replay of previously extracted corpus | tracked post-mortem and/or saved summary; no full request/response journal inspected | world replay (3corpora×2placements×6scenarios×5arms) | 180 | 180 | 180 | 180 | 180 | 0 | — | 0 | 0 | — | Replay computation complete; practical advantage over the strong central baseline not shown. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/healing-helping-hands/practical/POST-01.md#L5) |
| 104. healing-helping-hands / practical-01-reporting-failures | scripted; not applicable / None | tracked post-mortem and/or saved summary; no full request/response journal inspected | reporting call, not scientific episode | 14 | 14 | 14 | 0 | 0 | 0 | — | 14 | 0 | — | Reporting failed before dispatch; scientific computation was intact. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/healing-helping-hands/practical/POST-01.md#L20) |
| 105. healing-helping-hands / practical-02 | scripted; not applicable / replay of previously extracted corpus | tracked post-mortem and/or saved summary; no full request/response journal inspected | world replay (3corpora×2placements×6scenarios×5arms) | 180 | 180 | 180 | 180 | 180 | 0 | — | 0 | 0 | — | Replay computation complete; practical advantage over the strong central baseline not shown. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/healing-helping-hands/practical/POST-02.md#L5) |
| 106. immune-evidence-study / engineering-a1 | scripted; not applicable / scripted | tracked post-mortem and/or saved summary; no full request/response journal inspected | episode | 16 | 16 | 16 | 16 | 16 | 0 | — | 0 | 0 | — | a1 fails old recovery predicate; a2 passes revised safety predicate | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/immune-response-v3/evidence-study/engineering-a1-summary.json#L1) |
| 107. immune-evidence-study / engineering-a2 | scripted; not applicable / scripted | tracked post-mortem and/or saved summary; no full request/response journal inspected | episode | 16 | 16 | 16 | 16 | 16 | 0 | — | 0 | 0 | — | a1 fails old recovery predicate; a2 passes revised safety predicate | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/immune-response-v3/evidence-study/engineering-a2-summary.json#L1) |
| 108. immune-evidence-study / receipt-a1 | unrun; not applicable / None | tracked post-mortem and/or saved summary; no full request/response journal inspected | episode | 16 | 0 | 0 | 0 | 0 | 0 | — | — | 16 | — | setup failure | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/immune-response-v3/evidence-study/reviews/receipt-a1-post.md#L3) |
| 109. immune-evidence-study / receipt-a2 | model; claude-haiku-4-5-20251001 (configured) / Anthropic | All 26 saved assembled request/parsed-response pairs and 20 frames directly inspected; the 27th reservation has no saved response. Actual usage was not durably persisted before interruption. | episode | 16 | 4 | 3 | 3 | 3 | 1 | — | — | 13 | — | interrupted, unqualified | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/immune-response-v3/evidence-study/reviews/receipt-a2-post.md#L12) |
| 110. immune-response / v1-native-S0 | model; claude-haiku-4-5-20251001 (configured) / Anthropic | tracked post-mortem and/or saved summary; no full request/response journal inspected | episode | 6 | 6 | 6 | 6 | 6 | 0 | — | 0 | 0 | — | narrow pilot only | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/actual-experiments/DEPLOYMENT.md#L17) |
| 111. immune-response / v1-scripted-S0 | scripted; not applicable / scripted | tracked post-mortem and/or saved summary; no full request/response journal inspected | episode | 18 | 18 | 18 | 18 | 18 | 0 | — | 0 | 0 | — | engineering only | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/actual-experiments/immune-response/RESULTS-v2.md#L5) |
| 112. immune-response / v1-scripted-S1 | scripted; not applicable / scripted | tracked post-mortem and/or saved summary; no full request/response journal inspected | episode | 36 | 36 | 36 | 36 | 36 | 0 | — | 0 | 0 | — | engineering only | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/actual-experiments/immune-response/RESULTS-v2.md#L5) |
| 113. immune-response / v2-native | model; claude-haiku-4-5-20251001 (configured) / Anthropic | tracked post-mortem and/or saved summary; no full request/response journal inspected | episode | 8 | 8 | 8 | 7 | 7 | 0 | — | 1 | 0 | — | execution failed; clean passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/immune-response-v3/REVIEW.md#L23) |
| 114. immune-response / v2-scripted-S0 | scripted; not applicable / scripted | tracked post-mortem and/or saved summary; no full request/response journal inspected | episode | 32 | 32 | 32 | 32 | 32 | 0 | — | 0 | 0 | — | engineering only | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/actual-experiments/immune-response/RESULTS-v2.md#L5) |
| 115. immune-response / v2-scripted-S1 | scripted; not applicable / scripted | tracked post-mortem and/or saved summary; no full request/response journal inspected | episode | 256 | 256 | 256 | 256 | 256 | 0 | — | 0 | 0 | — | engineering only | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/actual-experiments/immune-response/RESULTS-v2.md#L5) |
| 116. immune-response-v3 / ledger-engineering-a1 | scripted; not applicable / scripted | tracked post-mortem and/or saved summary; no full request/response journal inspected | episode | 720 | 720 | 720 | 720 | 720 | 0 | — | 0 | 0 | — | engineering passes | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/immune-response-v3/reviews/engineering-a1-post.md#L7) |
| 117. immune-response-v3 / ledger-native-repair-task6700 | unrun; not applicable / None | tracked post-mortem and/or saved summary; no full request/response journal inspected | episode | — | 0 | 0 | 0 | 0 | 0 | — | — | — | — | superseded | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/immune-response-v3/scenario-study/README.md#L7) |
| 118. immune-response-v3 / scenario-engineering-a1 | scripted; not applicable / scripted | tracked post-mortem and/or saved summary; no full request/response journal inspected | episode | 192 | 192 | 192 | 192 | 192 | 0 | — | 0 | 0 | — | engineering passes | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/immune-response-v3/scenario-study/ASSESSMENT.md#L15) |
| 119. immune-response-v3 / scenario-engineering-a2 | scripted; not applicable / scripted | tracked post-mortem and/or saved summary; no full request/response journal inspected | episode | 192 | 192 | 192 | 192 | 192 | 0 | — | 0 | 0 | — | engineering passes | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/immune-response-v3/scenario-study/ASSESSMENT.md#L15) |
| 120. immune-response-v3 / scenario-native-a1 | model; claude-haiku-4-5-20251001 (configured; manifest backend confirmed) / Anthropic | All saved assembled requests and parsed responses inspected in authenticated read-only hub artifact; request+response together per advice/decision event. Not raw HTTP bytes. | episode | 12 | 12 | 12 | 12 | 12 | 0 | 0 | 0 | 0 | — | healthy-control fails | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/immune-response-v3/scenario-study/ASSESSMENT.md#L21) |
| 121. immune-response-v3 / scenario-native-a2 | model; claude-haiku-4-5-20251001 (configured; manifest backend confirmed) / Anthropic | All saved assembled requests and parsed responses inspected in authenticated read-only hub artifact; request+response together per advice/decision event. Not raw HTTP bytes. | episode | 12 | 12 | 12 | 12 | 12 | 0 | 0 | 0 | 0 | — | healthy-control passes but incident-recovery fails | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/immune-response-v3/scenario-study/ASSESSMENT.md#L21) |
| 122. immune-response-v3 / scenario-solo-a1 | model; claude-haiku-4-5-20251001 (configured; manifest backend confirmed) / Anthropic | All saved assembled requests and parsed responses inspected in authenticated read-only hub artifact; request+response together per advice/decision event. Not raw HTTP bytes. | episode | 4 | 4 | 4 | 4 | 4 | 0 | 0 | 0 | 0 | — | healthy-control fails | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/immune-response-v3/scenario-study/ASSESSMENT.md#L21) |
| 123. influence-swarms / P0 | unrun; not applicable / None | tracked post-mortem and/or saved summary; no full request/response journal inspected | episode | 6 | 0 | 0 | 0 | 0 | 0 | — | — | 6 | — | gated, no native dispatch evidence | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/influence-swarms/scenario/reviews/native-P0-01-pre.md#L3) |
| 124. influence-swarms / Q0 | model; claude-haiku-4-5-20251001 (configured) / Anthropic | tracked post-mortem and/or saved summary; no full request/response journal inspected | episode | 9 | 9 | 9 | 0 | 0 | 0 | — | 9 | 0 | — | full qualification failed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/influence-swarms/scenario/reviews/native-Q0-01-post.md#L3) |
| 125. influence-swarms / Q1 | model; claude-haiku-4-5-20251001 (configured) / Anthropic | tracked post-mortem and/or saved summary; no full request/response journal inspected | episode | 9 | 9 | 9 | 2 | 2 | 0 | — | 7 | 0 | — | full qualification failed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/influence-swarms/scenario/reviews/native-Q1-01-post.md#L3) |
| 126. influence-swarms / Q2 | model; claude-haiku-4-5-20251001 (configured) / Anthropic | All42 archived assembled requests and parsed model responses inspected; not raw HTTP. | episode | 9 | 9 | 9 | 9 | 9 | 0 | 0 | 0 | 0 | — | full qualification failed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/influence-swarms/scenario/reviews/native-Q2-01-post.md#L3); [source 2](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/artifacts/influence-native-q2-replay/influence-native-q2-replay-v1.html#L1) |
| 127. influence-swarms / Q3 | model; claude-haiku-4-5-20251001 (configured) / Anthropic | tracked post-mortem and/or saved summary; no full request/response journal inspected | episode | 3 | 3 | 3 | 3 | 3 | 0 | — | 0 | 0 | — | targeted diagnostic passes; full qualification still false | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/influence-swarms/scenario/reviews/native-Q3-01-post.md#L3) |
| 128. influence-swarms / Q4 | unrun; not applicable / None | tracked post-mortem and/or saved summary; no full request/response journal inspected | episode | 12 | 0 | 0 | 0 | 0 | 0 | — | — | 12 | — | gated, no native dispatch evidence | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/influence-swarms/scenario/reviews/native-P0-01-pre.md#L3) |
| 129. influence-swarms / S1 | unrun; not applicable / None | tracked post-mortem and/or saved summary; no full request/response journal inspected | episode | — | 0 | 0 | 0 | 0 | 0 | — | — | — | — | gated, no native dispatch evidence | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/influence-swarms/scenario/reviews/native-P0-01-pre.md#L3) |
| 130. influence-swarms / iteration-02 | scripted; not applicable / scripted | tracked post-mortem and/or saved summary; no full request/response journal inspected | episode | 12 | 12 | 12 | 12 | 12 | 0 | — | 0 | 0 | — | engineering only | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/influence-swarms/scenario/reviews/iteration-02-post.md#L3) |
| 131. influence-swarms / iteration-03 | scripted; not applicable / scripted | tracked post-mortem and/or saved summary; no full request/response journal inspected | episode | 12 | 12 | 12 | 12 | 12 | 0 | — | 0 | 0 | — | engineering only | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/influence-swarms/scenario/reviews/iteration-03-post.md#L3) |
| 132. influence-swarms / scenario-01 | scripted; not applicable / scripted | tracked post-mortem and/or saved summary; no full request/response journal inspected | episode | 288 | 288 | 288 | 288 | 288 | 0 | — | 0 | 0 | — | engineering only | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/influence-swarms/scenario/reviews/scenario-01-post.md#L3) |
| 133. influence-swarms / scenario-02 | scripted; not applicable / scripted | tracked post-mortem and/or saved summary; no full request/response journal inspected | episode | 288 | 288 | 288 | 288 | 288 | 0 | — | 0 | 0 | — | engineering only | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/influence-swarms/scenario/reviews/scenario-02-post.md#L3) |
| 134. influence-swarms / scenario-03 | scripted; not applicable / scripted | tracked post-mortem and/or saved summary; no full request/response journal inspected | episode | 288 | 288 | 288 | 288 | 288 | 0 | — | 0 | 0 | — | engineering only | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/influence-swarms/scenario/reviews/scenario-03-post.md#L3) |
| 135. market-split / s0-fleet-001 | scripted; not applicable / scripted | report_and_hub | market-arm episode | 18 | 18 | 18 | 18 | 18 | 0 | — | 0 | 0 | — | scripted_passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/market-split/reviews/s0-fleet-001-post.md#L1) |
| 136. market-split / s0-local-001 | scripted; not applicable / scripted | report_and_hub | market-arm episode | 18 | 18 | 18 | 18 | 18 | 0 | — | 0 | 0 | — | scripted_passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/market-split/reviews/s0-local-001-post.md#L1) |
| 137. market-split / s0-local-002 | scripted; not applicable / scripted | report_and_hub | market-arm episode | 18 | 18 | 18 | 18 | 18 | 0 | — | 0 | 0 | — | scripted_passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/market-split/reviews/s0-local-002-post.md#L1) |
| 138. market-split / s1-fleet-001 | scripted; not applicable / scripted | report_and_hub | market-arm episode | 432 | 432 | 432 | 432 | 432 | 0 | — | 0 | 0 | — | scripted_passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/market-split/reviews/s1-fleet-001-post.md#L1) |
| 139. market-split-api / i0-001 | model; claude-haiku-4-5-20251001 / anthropic | report_and_hub | one-response stateless mechanics probe | 6 | 6 | 6 | 6 | 6 | 0 | — | 0 | 0 | 6 | mechanics_passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/market-split-api/reviews/i0-001-post.md#L1) |
| 140. market-split-api / i0-002 | model; claude-sonnet-4-6 / anthropic | report_and_hub | one-response stateless mechanics probe | 6 | 6 | 6 | 6 | 6 | 0 | — | 0 | 0 | 6 | mechanics_passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/market-split-api/reviews/i0-002-post.md#L1) |
| 141. market-split-api / i0-003 | model; claude-sonnet-4-6 / anthropic | report_and_hub | one-response stateless mechanics probe | 6 | 6 | 6 | 6 | 6 | 0 | — | 0 | 0 | 6 | mechanics_passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/market-split-api/reviews/i0-003-post.md#L1) |
| 142. market-split-api / q0-001 | model; claude-haiku-4-5-20251001 / anthropic | saved_actor_observation_action_final_text_and_hashes | market-arm episode | 4 | 2 | 2 | 0 | 0 | 2 | — | 2 | 2 | — | failed_output_schema | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/market-split-api/reviews/q0-001-post.md#L1) |
| 143. market-split-api / q0-002 | model; claude-haiku-4-5-20251001 / anthropic | saved_actor_observation_action_final_text_and_hashes | market-arm episode | 4 | 4 | 4 | 4 | 4 | 0 | — | 0 | 0 | 4 | passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/market-split-api/reviews/q0-002-post.md#L1) |
| 144. market-split-api / q0-003 | model; claude-haiku-4-5-20251001 / anthropic | saved_actor_observation_action_final_text_and_hashes | market-arm episode | 4 | 2 | 2 | 2 | 2 | 0 | — | 0 | 2 | 1 | failed_clean_profit | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/market-split-api/reviews/q0-003-post.md#L1) |
| 145. market-split-api / q0-004 | model; claude-sonnet-4-6 / anthropic | saved_actor_observation_action_final_text_and_hashes | market-arm episode | 4 | 4 | 4 | 4 | 4 | 0 | — | 0 | 0 | 3 | failed_clean_profit | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/market-split-api/reviews/q0-004-post.md#L1) |
| 146. market-split-api / q0-005 | model; claude-sonnet-4-6 / anthropic | saved_actor_observation_action_final_text_and_hashes | market-arm episode | 4 | 4 | 4 | 4 | 4 | 0 | — | 0 | 0 | 4 | passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/market-split-api/reviews/q0-005-post.md#L1) |
| 147. market-split-api / s0-fleet-001 | scripted; not applicable / scripted | saved_actor_observation_action_final_text_and_hashes | market-arm episode | 12 | 12 | 12 | 12 | 12 | 0 | — | 0 | 0 | — | mock_adapter_passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/market-split-api/reviews/s0-fleet-001-post.md#L1) |
| 148. market-split-api / s0-fleet-002 | scripted; not applicable / scripted | saved_actor_observation_action_final_text_and_hashes | market-arm episode | 12 | 12 | 12 | 12 | 12 | 0 | — | 0 | 0 | — | mock_adapter_passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/market-split-api/reviews/s0-fleet-002-post.md#L1) |
| 149. market-split-api / s0-fleet-003 | scripted; not applicable / scripted | saved_actor_observation_action_final_text_and_hashes | market-arm episode | 12 | 12 | 12 | 12 | 12 | 0 | — | 0 | 0 | — | mock_adapter_passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/market-split-api/reviews/s0-fleet-003-post.md#L1) |
| 150. market-split-api / s0-fleet-004 | scripted; not applicable / scripted | saved_actor_observation_action_final_text_and_hashes | market-arm episode | 12 | 12 | 12 | 12 | 12 | 0 | — | 0 | 0 | — | mock_adapter_passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/market-split-api/reviews/s0-fleet-004-post.md#L1) |
| 151. market-split-api / s0-fleet-005 | scripted; not applicable / scripted | saved_actor_observation_action_final_text_and_hashes | market-arm episode | 12 | 12 | 12 | 12 | 12 | 0 | — | 0 | 0 | — | mock_adapter_passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/market-split-api/reviews/s0-fleet-005-post.md#L1) |
| 152. market-split-api / s0-local-001 | scripted; not applicable / scripted | report_and_hub | market-arm episode | 12 | 12 | 12 | 12 | 12 | 0 | — | 0 | 0 | — | mock_adapter_passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/market-split-api/reviews/s0-local-001-post.md#L1) |
| 153. market-split-api / s1-001 | model; claude-haiku-4-5-20251001 / anthropic | saved_actor_observation_action_final_text_and_hashes | market-arm episode | 36 | 18 | 18 | 17 | 17 | 1 | — | 1 | 18 | — | main_execution_failed_after_passed_Q0 | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/market-split-api/reviews/s1-001-post.md#L1) |
| 154. market-split-api / s1-002 | model; claude-sonnet-4-6 / anthropic | hub_snapshot_plus_one_saved_completed_bundle | market-arm episode | 36 | — | 12 | 12 | 12 | — | — | 0 | 24 | — | qualified_pilot_in_progress | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/market-split-api/reviews/s1-002-continuation.md#L3) |
| 155. market-split-haiku / d0-001 | model; claude-haiku-4-5-20251001 / anthropic | publication_postmortem_and_deployment_only | one replayed actor observation / model response | 2 | 2 | 2 | 2 | 2 | 0 | 0 | 0 | 0 | — | diagnostic_passed_no_causal_repair_claim | [source 1](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/dmarz/notes/market-split-haiku/reviews/d0-001-post.md#L3); [source 2](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/dmarz/notes/market-split-haiku/reviews/d0-001-pre.md#L1) |
| 156. market-split-haiku / d0-001-launcher-compile-failure | scripted; not applicable / local/scripted | publication_postmortem_and_deployment_only | local launcher compilation attempt | 1 | 1 | 1 | 0 | 0 | 1 | — | 1 | 0 | 0 | pre_dispatch_setup_failure_repaired | [source 1](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/dmarz/notes/market-split-haiku/reviews/d0-001-post.md#L9) |
| 157. market-split-haiku / i0-001 | model; claude-haiku-4-5-20251001 / anthropic | report_and_hub | one-response stateless mechanics probe | 6 | 2 | 2 | 2 | 2 | 0 | — | 0 | 4 | 1 | mandate_failed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/market-split-haiku/reviews/i0-001-post.md#L1) |
| 158. market-split-haiku / i0-002 | model; claude-haiku-4-5-20251001 / anthropic | report_and_hub | one-response stateless mechanics probe | 6 | 6 | 6 | 6 | 6 | 0 | — | 0 | 0 | 6 | mechanics_passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/market-split-haiku/reviews/i0-002-post.md#L1) |
| 159. market-split-haiku / i0-003 | model; claude-haiku-4-5-20251001 / anthropic | publication_postmortem_and_deployment_only | one-response stateless mechanics probe | 6 | 6 | 6 | 6 | 6 | 0 | — | 0 | 0 | 6 | mechanics_passed_main_blocked | [source 1](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/dmarz/notes/market-split-haiku/reviews/i0-003-post.md#L3); [source 2](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/dmarz/notes/market-split-haiku/reviews/i0-003-pre.md#L1) |
| 160. market-split-haiku / q0-001 | model; claude-haiku-4-5-20251001 / anthropic | saved_actor_observation_action_final_text_and_hashes | market-arm episode | 4 | 4 | 4 | 4 | 4 | 0 | — | 0 | 0 | 4 | passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/market-split-haiku/reviews/q0-001-post.md#L1) |
| 161. market-split-haiku / q0-002 | model; claude-haiku-4-5-20251001 / anthropic | publication_postmortem_and_deployment_only | eight-round clean market-arm episode | 4 | 4 | 4 | 4 | 4 | 0 | — | 0 | 0 | 4 | clean_profit_passed_R0_required | [source 1](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/dmarz/notes/market-split-haiku/reviews/q0-002-post.md#L3); [source 2](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/dmarz/notes/market-split-haiku/reviews/q0-002-pre.md#L1) |
| 162. market-split-haiku / r0-001 | model; claude-haiku-4-5-20251001 / anthropic | publication_postmortem_and_deployment_only | 24-round regulated market-arm episode | 8 | — | — | — | — | — | — | — | — | — | running_no_published_terminal_results | [source 1](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/dmarz/notes/market-split-haiku/reviews/r0-001-pre.md#L3); [source 2](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/dmarz/notes/market-split-haiku/deployment.md#L13) |
| 163. market-split-haiku / s0-fleet-001 | scripted; not applicable / scripted | saved_actor_observation_action_final_text_and_hashes | market-arm episode | 12 | 12 | 12 | 12 | 12 | 0 | — | 0 | 0 | — | mock_adapter_passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/market-split-haiku/reviews/s0-fleet-001-post.md#L1) |
| 164. market-split-haiku / s0-fleet-002 | scripted; not applicable / scripted | saved_actor_observation_action_final_text_and_hashes | market-arm episode | 12 | 12 | 12 | 12 | 12 | 0 | — | 0 | 0 | — | mock_adapter_passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/market-split-haiku/reviews/s0-fleet-002-post.md#L1) |
| 165. market-split-haiku / s0-fleet-003 | scripted; not applicable / scripted | saved_actor_observation_action_final_text_and_hashes | market-arm episode | 12 | 12 | 12 | 12 | 12 | 0 | — | 0 | 0 | — | mock_adapter_passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/market-split-haiku/reviews/s0-fleet-003-pre.md#L1); [source 9](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/dmarz/notes/market-split-haiku/reviews/s0-fleet-003-post.md#L3) |
| 166. market-split-haiku / s1-001 | model; claude-haiku-4-5-20251001 / anthropic | saved_actor_observation_action_final_text_and_hashes | market-arm episode | 36 | 4 | 4 | 2 | 2 | 2 | — | 2 | 32 | — | main_execution_failed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/market-split-haiku/reviews/s1-001-post.md#L1) |
| 167. market-split-haiku / s1-002-conditional | unrun; not applicable / None | publication_postmortem_and_deployment_only | future main market-arm episode | — | — | — | — | — | — | — | — | — | — | conditional_main_blocked_pending_R0 | [source 1](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/dmarz/notes/market-split-haiku/reviews/r0-001-pre.md#L19); [source 2](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/dmarz/notes/market-split-api/parallel-plan.md#L17) |
| 168. market-split-haiku / v3-headroom-d0-i0-q0-r0 | unrun; not applicable / None | plan_only | multiple future diagnostic, mechanics, qualification and reliability stages | — | — | — | — | — | — | — | — | — | — | paid_repair_plan_pending | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/market-split-haiku/reviews/s0-fleet-003-pre.md#L5) |
| 169. optimal-swarm-size / Q1-setup | unrun; not applicable / None | tracked post-mortem and/or saved summary; no full request/response journal inspected | episode | 16 | 0 | 0 | 0 | 0 | 0 | — | — | 16 | — | credential and review blocked | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/optimal-swarm-size/reviews/q1-setup-post.md#L16) |
| 170. optimal-swarm-size / engineering-review | scripted; not applicable / None | tracked post-mortem and/or saved summary; no full request/response journal inspected | softwarefixture | — | — | — | — | — | — | — | — | — | — | REVISE | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/optimal-swarm-size-engineering-review/POST-MORTEM.md#L3) |
| 171. optimal-swarm-size / reporting-Q0 | scripted; not applicable / None | tracked post-mortem and/or saved summary; no full request/response journal inspected | reportingfixtureitem | 16 | 16 | 16 | 16 | 16 | 0 | — | 0 | 0 | — | reportingtestonly,backend verification pending |  |
| 172. phantom-coast / OFFLINE-01 | scripted; not applicable / None | tracked post-mortem and/or saved summary; no full request/response journal inspected | softwarefixture | — | — | — | — | — | — | — | — | — | — | offlineonly | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/phantom-coast/reviews/OFFLINE-01-POST.md#L7) |
| 173. phantom-coast / Q0-A1 | model; typesafe/jev-1.13-20260917 / OpenRouter Decisions API / TypeSafe, no fallback | All 18 saved actual requests and checked provider response maps, probability vectors, returned model/provider and usage directly inspected from authenticated read-only hub records.json. No complete HTTP envelope retained in this journal. Summary, manifest and post-mortem corroborate. | one complete-map response; six independent synthetic map roots, three private reset observers each | 18 | 18 | 18 | 18 | 18 | 0 | 0 | 0 | 0 | — | PASS all declared clean mapping thresholds:18/18 valid,648/648 cells correct,216 land and432 water,zero missing. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/vishesh/notes/phantom-coast/reviews/Q0-A1-POST.md#L3); [source 2](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/vishesh/notes/phantom-coast/results/Q0-A1-summary.json#L1) |
| 174. phantom-coast / S0-A1-plan | unrun; typesafe/jev-1.13-20260917 planned / OpenRouter Decisions/TypeSafe | Published pre-run/launch record; no terminal summary. No inference from launch receipt to observed execution. | planned model map request | 522 | — | — | — | — | — | — | — | — | — | Q0 passed; S0 launch receipt exists but no S0 outcome record at publication cutoff | [source 1](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/vishesh/notes/phantom-coast/reviews/S0-A1-PRE.md) |
| 175. phantom-coast / native-Q0 | unrun; not applicable / None | tracked post-mortem and/or saved summary; no full request/response journal inspected | episode | — | 0 | 0 | 0 | 0 | 0 | — | — | — | — | review/budget/transportgates | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/phantom-coast/README.md#L3) |
| 176. quorum-of-mirrors / QM-S0-01 | unrun; not applicable / OpenRouter Decisions/TypeSafe | tracked post-mortem and/or saved summary; no full request/response journal inspected | episode | 32 | 0 | 0 | 0 | 0 | 0 | — | 0 | 32 | — | setup failed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/decision-models/quorum-of-mirrors/RESULTS.md#L3) |
| 177. quorum-of-mirrors / QM-S0-02 | model; typesafe/jev-1.13-20260917 / OpenRouter Decisions/TypeSafe | 32 actual provider-response objects inspected, with usage, served model and request hashes. Full request payloads are not present in the receipt journal. | episode | 32 | 32 | 32 | 32 | 32 | 0 | 0 | 0 | 0 | — | S0 passed; S1 unrun | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/decision-models/quorum-of-mirrors/RESULTS.md#L3); [source 2](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/decision-models/quorum-of-mirrors/results/QM-S0-02/receipts.jsonl#L1) |
| 178. regrowth-200 / pilot-v4-algorithm-control | scripted; not applicable / algorithm | tracked post-mortem and/or saved summary; no full request/response journal inspected | world (one shared map,80rounds,199decisioncells) | 1 | 1 | 1 | 1 | 1 | 0 | — | 0 | 0 | — | Adapted development qualification reached 8/10 after accepting equally short routes; not a held-out competence screen. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/regrowth-200/README.md#L25) |
| 179. regrowth-200 / pilot-v4-algorithm-damage | scripted; not applicable / algorithm | tracked post-mortem and/or saved summary; no full request/response journal inspected | world (one shared map,80rounds,199decisioncells) | 1 | 1 | 1 | 1 | 1 | 0 | — | 0 | 0 | — | Adapted development qualification reached 8/10 after accepting equally short routes; not a held-out competence screen. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/regrowth-200/README.md#L25) |
| 180. regrowth-200 / pilot-v4-hybrid-control | model; Qwen; hybrid includes Laya / hybrid | tracked post-mortem and/or saved summary; no full request/response journal inspected | world (one shared map,80rounds,199decisioncells) | 1 | 1 | 1 | 1 | 1 | 0 | — | 0 | 0 | — | Adapted development qualification reached 8/10 after accepting equally short routes; not a held-out competence screen. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/regrowth-200/README.md#L25) |
| 181. regrowth-200 / pilot-v4-hybrid-damage | model; Qwen; hybrid includes Laya / hybrid | tracked post-mortem and/or saved summary; no full request/response journal inspected | world (one shared map,80rounds,199decisioncells) | 1 | 1 | 1 | 1 | 1 | 0 | — | 0 | 0 | — | Adapted development qualification reached 8/10 after accepting equally short routes; not a held-out competence screen. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/regrowth-200/README.md#L25) |
| 182. regrowth-200 / pilot-v4-qwen-control | model; Qwen; hybrid includes Laya / qwen | tracked post-mortem and/or saved summary; no full request/response journal inspected | world (one shared map,80rounds,199decisioncells) | 1 | 1 | 1 | 1 | 1 | 0 | — | 0 | 0 | — | Adapted development qualification reached 8/10 after accepting equally short routes; not a held-out competence screen. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/regrowth-200/README.md#L25) |
| 183. regrowth-200 / pilot-v4-qwen-damage | model; Qwen; hybrid includes Laya / qwen | tracked post-mortem and/or saved summary; no full request/response journal inspected | world (one shared map,80rounds,199decisioncells) | 1 | 1 | 1 | 1 | 1 | 0 | — | 0 | 0 | — | Adapted development qualification reached 8/10 after accepting equally short routes; not a held-out competence screen. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/regrowth-200/README.md#L25) |
| 184. regrowth-200 / plan-registration-failure-v1 | scripted; not applicable / None | tracked post-mortem and/or saved summary; no full request/response journal inspected | documentation incident affecting6worlds | 1 | 1 | 1 | 0 | 0 | 0 | — | 1 | 0 | — | processfailure | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/regrowth-200/README.md#L35) |
| 185. regrowth-200 / prior-stopped-attempts-aggregate | model; not verified / None | author summary only; individual manifests/logs missing | historical attempt (individual IDs not recovered) | 4 | — | — | — | — | — | — | — | — | — | unknown | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/regrowth-200/README.md#L37) |
| 186. right-dissenter / Q0-A1 | model; typesafe/jev-1.13-20260917 / OpenRouter Decisions API / TypeSafe, no fallback | All 18 actual saved request packets and checked responses inspected in committed calls.json; records.json and summary.json independently counted. Checked responses preserve served model, probabilities, tokens and cost, but not full HTTP envelopes. | one single-observation qualification decision;18 packet IDs in three scenario templates | 18 | 18 | 18 | 18 | 18 | 0 | 0 | 0 | 0 | — | FAILED:12/18 correct versus16/18 required. Bridge 6/6; build 3/6; alarm 3/6. All 18 valid and complete. S1 remains blocked. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/vishesh/notes/dissent/reviews/Q0-A1-POST.md#L3); [source 2](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/vishesh/notes/dissent/results/q0-a1/calls.json#L1); [source 3](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/vishesh/notes/dissent/results/q0-a1/records.json#L1); [source 4](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/vishesh/notes/dissent/results/q0-a1/summary.json#L1) |
| 187. right-dissenter / native-Q0 | unrun; not applicable / None | tracked post-mortem and/or saved summary; no full request/response journal inspected | episode | — | 0 | 0 | 0 | 0 | 0 | — | — | — | — | design/software only | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/dissent/README.md#L31) |
| 188. soc07-private-judgments / S1L | unrun; not applicable / None | plan_only | proposed physical model request | 4080 | 0 | 0 | 0 | 0 | 0 | — | 0 | 4080 | — | proposal_no_model_run_evidence | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/soc07-private-judgments/README.md#L1); [source 2](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/soc07-private-judgments/execution.json#L1) |
| 189. soc07-private-judgments / S1Q | unrun; not applicable / None | plan_only | proposed physical model request | 12 | 0 | 0 | 0 | 0 | 0 | — | 0 | 12 | — | proposal_no_model_run_evidence | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/soc07-private-judgments/README.md#L1); [source 2](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/soc07-private-judgments/execution.json#L1) |
| 190. soc07-private-judgments / S1R | unrun; not applicable / None | plan_only | proposed physical model request | 672 | 0 | 0 | 0 | 0 | 0 | — | 0 | 672 | — | proposal_no_model_run_evidence | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/soc07-private-judgments/README.md#L1); [source 2](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/soc07-private-judgments/execution.json#L1) |
| 191. soc07-private-judgments / ae76d67b | scripted; not applicable / scripted | report_and_hub | mixed planned components; see planned_component_counts | — | — | — | — | — | — | — | — | — | — | fleet_S0_running_no_terminal_metrics | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/soc07-private-judgments/reviews/s0-pre.md#L11) |
| 192. soc07-private-judgments / local-s0-001 | scripted; not applicable / scripted | report_and_hub | engineering checks; per-episode counts not verified | — | — | — | — | — | — | — | — | — | — | 69_of_69_checks_passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/soc07-private-judgments/reviews/s0-pre.md#L3) |
| 193. swarm-of-theseus / S0-a1 | unrun; not applicable / None | tracked post-mortem and/or saved summary; no full request/response journal inspected | episode | 12 | 0 | 0 | 0 | 0 | 0 | — | — | 12 | — | setup failure | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/swarm-of-theseus/reviews/S0-a1-post.md#L3) |
| 194. swarm-of-theseus / S0-a2 | model; claude-haiku-4-5-20251001 (configured) / Anthropic | 72 archived episode journals contain 1,697 requests and 1,693 parsed responses across these four attempts. Four S0-a2 requests have no saved response. Counts and refusal-phrase scan cover all journals; illustrative wrong decisions were inspected. Raw HTTP error bodies are absent. | world-arm episode (pairedscenario/seedclusters) | 12 | 12 | 12 | 8 | 8 | 0 | — | 4 | 0 | — | failed4PolicyErrors | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/swarm-of-theseus/RESULTS.md#L9); [source 2](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/artifacts/theseus-pilot-evidence/theseus-pilot-evidence-v1.gz#L1) |
| 195. swarm-of-theseus / S0-a3 | model; claude-haiku-4-5-20251001 (configured) / Anthropic | 72 archived episode journals contain 1,697 requests and 1,693 parsed responses across these four attempts. Four S0-a2 requests have no saved response. Counts and refusal-phrase scan cover all journals; illustrative wrong decisions were inspected. Raw HTTP error bodies are absent. | world-arm episode (pairedscenario/seedclusters) | 12 | 12 | 12 | 12 | 12 | 0 | 0 | 0 | 0 | — | failedobservatoryverbatim.75<.85 | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/swarm-of-theseus/RESULTS.md#L9); [source 2](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/artifacts/theseus-pilot-evidence/theseus-pilot-evidence-v1.gz#L1) |
| 196. swarm-of-theseus / S0-a4 | model; claude-haiku-4-5-20251001 (configured) / Anthropic | 72 archived episode journals contain 1,697 requests and 1,693 parsed responses across these four attempts. Four S0-a2 requests have no saved response. Counts and refusal-phrase scan cover all journals; illustrative wrong decisions were inspected. Raw HTTP error bodies are absent. | world-arm episode (pairedscenario/seedclusters) | 12 | 12 | 12 | 12 | 12 | 0 | 0 | 0 | 0 | — | passedfreshseeds106/107 | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/swarm-of-theseus/RESULTS.md#L9); [source 2](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/artifacts/theseus-pilot-evidence/theseus-pilot-evidence-v1.gz#L1) |
| 197. swarm-of-theseus / S1-a1 | model; claude-haiku-4-5-20251001 (configured) / Anthropic | 72 archived episode journals contain 1,697 requests and 1,693 parsed responses across these four attempts. Four S0-a2 requests have no saved response. Counts and refusal-phrase scan cover all journals; illustrative wrong decisions were inspected. Raw HTTP error bodies are absent. | world-arm episode (pairedscenario/seedclusters) | 36 | 36 | 36 | 36 | 36 | 0 | 0 | 0 | 0 | — | completedexploratoryeffect | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/swarm-of-theseus/RESULTS.md#L9); [source 2](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/artifacts/theseus-pilot-evidence/theseus-pilot-evidence-v1.gz#L1) |
| 198. swarm-of-theseus-v2 / S0 | model; claude-haiku-4-5-20251001 (saved request configuration; returned model identity not retained separately) / Anthropic | Newly published archive directly inspected: all 24 dispatch-start records,24 durable parsed results with stop reasons and usage,24 event records,12 episode outcomes and manifest. Repaired requests additionally preserve exact user text. The old hub catalogue was empty; this supplement closes that request/result gap through the separate archive. Records do not retain complete HTTP envelopes or independently returned model identity. | world-arm episode (12 episodes, six paired scenario/seed worlds; two calls and six decisions per call) | 12 | 12 | 12 | 12 | 12 | 0 | 0 | 0 | 0 | — | FAILED joint competence gate, unchanged: explicit-rule accuracy>=0.90 in each scenario/checkpoint and stable learner>=0.75 in every scenario. All schemas valid; no turnover pilot dispatched. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/artifacts/vishesh-theseus-v2-initial-evidence/vishesh-theseus-v2-initial-evidence-v1.gz#L1); [source 2](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/vishesh/notes/swarm-of-theseus/v2/RESULTS.md#L3); [source 3](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/vishesh/notes/swarm-of-theseus/v2/reviews/S0-post.md#L7) |
| 199. swarm-of-theseus-v2 / S0-plan-at-frozencommit | unrun; not applicable / None | tracked post-mortem and/or saved summary; no full request/response journal inspected | world-arm episode;24plannedcalls | 12 | 0 | 0 | 0 | 0 | 0 | — | — | 12 | — | sourceplanblocked, laterexecutionreported | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/vishesh/notes/swarm-of-theseus/v2/reviews/S0-pre.md#L14) |
| 200. swarm-of-theseus-v2 / S0-repair | model; claude-haiku-4-5-20251001 (saved request configuration; returned model identity not retained separately) / Anthropic | Newly published archive directly inspected: all 24 dispatch-start records,24 durable parsed results with stop reasons and usage,24 event records,12 episode outcomes and manifest. Repaired requests additionally preserve exact user text. The old hub catalogue was empty; this supplement closes that request/result gap through the separate archive. Records do not retain complete HTTP envelopes or independently returned model identity. | world-arm episode (12 episodes, six paired scenario/seed worlds; two calls and six decisions per call) | 12 | 12 | 12 | 12 | 12 | 0 | 0 | 0 | 0 | — | FAILED joint competence gate, unchanged: explicit-rule accuracy>=0.90 in each scenario/checkpoint and stable learner>=0.75 in every scenario. All schemas valid; no turnover pilot dispatched. | [source 1](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/artifacts/vishesh-theseus-v2-repair-evidence/vishesh-theseus-v2-repair-evidence-v1.gz#L1); [source 2](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/vishesh/notes/swarm-of-theseus/v2/RESULTS.md#L3); [source 3](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/vishesh/notes/swarm-of-theseus/v2/reviews/S0-repair-post.md#L7) |
| 201. sybil-budget-api / 46ebda03 | model; claude-haiku-4-5-20251001 / anthropic | report_and_hub | one packet/arm observation | 2880 | — | 0 | 0 | 0 | — | — | — | 2880 | — | prior_Q0_passed_S1_running | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/sybil-budget-api/DEPLOYMENT.md#L27); [source 3](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/dmarz/notes/sybil-budget-api/DEPLOYMENT.md#L47) |
| 202. sybil-budget-api / 7b177592 | model; claude-haiku-4-5-20251001 / anthropic | saved_final_answer_and_packet_hash | one packet/arm observation | 16 | 16 | 16 | 16 | 16 | 0 | — | 0 | 0 | 16 | passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/sybil-budget-api/reviews/q0-001-post.md#L1) |
| 203. sybil-budget-api / fleet-s0-001 | scripted; not applicable / scripted | report_and_hub | one packet/arm observation | 256 | 256 | 256 | 256 | 256 | 0 | — | 0 | 0 | — | scripted_passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/sybil-budget-api/reviews/fleet-s0-001-post.md#L1) |
| 204. sybil-budget-api / s0-local-001 | scripted; not applicable / scripted | report_and_hub | one packet/arm observation | 256 | 256 | 256 | 256 | 256 | 0 | — | 0 | 0 | — | scripted_passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/sybil-budget-api/reviews/s0-local-001-post.md#L1) |
| 205. sybil-budget-api / s0-local-002 | scripted; not applicable / scripted | report_and_hub | one packet/arm observation | 256 | 256 | 256 | 256 | 256 | 0 | — | 0 | 0 | — | scripted_passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/sybil-budget-api/reviews/s0-local-002-post.md#L1) |
| 206. sybil-newcomer-api / 8def40e4 | model; claude-haiku-4-5-20251001 / anthropic | report_and_hub | one packet/arm observation | 1944 | — | 231 | 231 | 231 | — | — | 0 | 1713 | — | prior_Q0_passed_S1_running | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/sybil-newcomer-api/DEPLOYMENT.md#L15); [source 3](https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/dmarz/notes/sybil-newcomer-api/DEPLOYMENT.md#L50) |
| 207. sybil-newcomer-api / f7b78b41 | model; claude-haiku-4-5-20251001 / anthropic | saved_final_answer_and_packet_hash | one packet/arm observation | 36 | 36 | 36 | 36 | 36 | 0 | — | 0 | 0 | 36 | passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/sybil-newcomer-api/reviews/q0-001-post.md#L1) |
| 208. sybil-newcomer-api / fleet-s0-001 | scripted; not applicable / scripted | report_and_hub | one packet/arm observation | 198 | 198 | 198 | 198 | 198 | 0 | — | 0 | 0 | — | scripted_passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/sybil-newcomer-api/reviews/fleet-s0-001-post.md#L1) |
| 209. sybil-newcomer-api / s0-local-001 | scripted; not applicable / scripted | report_and_hub | one packet/arm observation | 198 | 198 | 198 | 198 | 198 | 0 | — | 0 | 0 | — | observations_complete_harness_failed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/sybil-newcomer-api/reviews/s0-local-001-post.md#L1) |
| 210. sybil-newcomer-api / s0-local-002 | scripted; not applicable / scripted | report_and_hub | one packet/arm observation | 198 | 198 | 198 | 198 | 198 | 0 | — | 0 | 0 | — | scripted_passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/sybil-newcomer-api/reviews/s0-local-002-post.md#L1) |
| 211. sybil-newcomer-api / s0-local-003 | scripted; not applicable / scripted | report_and_hub | one packet/arm observation | 198 | 198 | 198 | 198 | 198 | 0 | — | 0 | 0 | — | scripted_passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/sybil-newcomer-api/reviews/s0-local-003-post.md#L1) |
| 212. sybil-scale-api / fleet-s0-001 | scripted; not applicable / scripted | report_and_hub | one packet/arm observation | 264 | 264 | 264 | 264 | 264 | 0 | — | 0 | 0 | — | scripted_passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/sybil-scale-api/reviews/fleet-s0-001-post.md#L1) |
| 213. sybil-scale-api / local-s0-001 | scripted; not applicable / scripted | report_and_hub | one packet/arm observation | 264 | 264 | 264 | 264 | 264 | 0 | — | 0 | 0 | — | scripted_passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/sybil-scale-api/reviews/local-s0-001-post.md#L1) |
| 214. sybil-scale-api / q0-001 | model; claude-haiku-4-5-20251001 / anthropic | saved_final_answer_and_packet_hash | one packet/arm observation | 64 | 64 | 64 | 64 | 64 | 0 | — | 0 | 0 | 64 | passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/sybil-scale-api/reviews/q0-001-post.md#L1) |
| 215. sybil-scale-api / s1-001 | model; claude-haiku-4-5-20251001 / anthropic | saved_final_answer_and_packet_hash | one packet/arm observation | 2400 | 2400 | 2400 | 2400 | 2400 | 0 | — | 0 | 0 | 594 | prior_Q0_passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/sybil-scale-api/reviews/s1-001-post.md#L1); [source 2](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/sybil-scale-api/RESULTS.md#L1) |
| 216. sybil-specialists / fleet-s0-001 | scripted; not applicable / scripted | report_and_hub | one packet/arm observation | 256 | 256 | 256 | 256 | 256 | 0 | — | 0 | 0 | — | scripted_passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/sybil-specialists/reviews/fleet-s0-001-post.md#L1) |
| 217. sybil-specialists / fleet-s1-001 | scripted; not applicable / scripted | report_and_hub | one packet/arm observation | 864 | 864 | 864 | 864 | 864 | 0 | — | 0 | 0 | — | scripted_passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/sybil-specialists/reviews/fleet-s1-001-post.md#L1) |
| 218. sybil-specialists / local-s0-001 | scripted; not applicable / scripted | report_and_hub | one packet/arm observation | 256 | 256 | 256 | 256 | 256 | 0 | — | 0 | 0 | — | scripted_passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/sybil-specialists/reviews/local-s0-001-post.md#L1) |
| 219. sybil-specialists / worker-stop-diagnostic | scripted; not applicable / scripted | report_and_hub | offline injected failure test, not a scientific episode | — | — | — | — | — | — | — | — | — | — | 15_offline_checks_passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/sybil-specialists/reviews/worker-stop-diagnostic.md#L1) |
| 220. sybil-specialists-api / 08338820 | model; claude-haiku-4-5-20251001 / anthropic | report_and_hub | one packet/arm observation | 24 | 24 | 24 | 24 | 24 | 0 | — | 0 | 0 | 24 | passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/sybil-specialists-api/reviews/q0-001-post.md#L1) |
| 221. sybil-specialists-api / bac7d9ae | model; claude-haiku-4-5-20251001 / anthropic | report_and_hub | one packet/arm observation | 192 | 192 | 192 | 192 | 192 | 0 | — | 0 | 0 | — | prior_Q0_passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/sybil-specialists-api/reviews/s1-001-post.md#L1) |
| 222. sybil-specialists-api / fleet-s0-001 | scripted; not applicable / scripted | report_and_hub | one packet/arm observation | 216 | 216 | 216 | 216 | 216 | 0 | — | 0 | 0 | — | scripted_passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/sybil-specialists-api/reviews/fleet-s0-001-post.md#L1) |
| 223. sybil-specialists-api / local-s0-001 | scripted; not applicable / scripted | report_and_hub | one packet/arm observation | 216 | 216 | 216 | 216 | 216 | 0 | — | 0 | 0 | — | scripted_passed | [source 1](https://github.com/dmarzzz/swarm-lab/blob/5945294fa853d7ff60a7ec62b31fd2158d74c3de/researchers/dmarz/notes/sybil-specialists-api/reviews/local-s0-001-post.md#L1) |

## Outcome and denominator notes

¹ Completion definitions vary and are printed per entry. ² Incomplete may include invalid execution; use the per-entry note and valid count, not a column sum. Never-started assignments are missing, not demonstrated agent stalling. ³ Success is criterion-specific: safe task completion, decision correctness, exact packet correctness, or another named evaluator; see the qualification and endpoint definition. A null is not zero.

### 1. Avalon swarm prototype / consensus-v02

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

15 terminal records match 15 saved planned configurations; populations/councils are not independent replication. v 0.1 and v 0.2 reuse initialization and must not be pooled as independent worlds. valid refers to completed scripted mechanics, not qualified model competence.

Behavior: Signal_loss at round 5 in everyv 0.2 world; fixed mission horizon deliberately continues after terminal scientific failure. Scripted fifth-proposal fallback occurs and is not a provider refusal.

Denominator limits: 15 terminal records match 15 saved planned configurations; populations/councils are not independent replication. v 0.1 and v 0.2 reuse initialization and must not be pooled as independent worlds. valid refers to completed scripted mechanics, not qualified model competence.

### 2. Avalon swarm prototype / prospective model track

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Planning upper-bound logical calls are not provider requests or invoices.

Behavior: Not observed.

Denominator limits: Planning upper-bound logical calls are not provider requests or invoices.

### 3. Avalon swarm prototype / recovery-pilot

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

15 terminal records match 15 saved planned configurations; populations/councils are not independent replication. v 0.1 and v 0.2 reuse initialization and must not be pooled as independent worlds. valid refers to completed scripted mechanics, not qualified model competence.

Behavior: No execution stall or exception in saved cohort. Some fifth proposals forced by game mechanics; task quality remains weak.

Denominator limits: 15 terminal records match 15 saved planned configurations; populations/councils are not independent replication. v 0.1 and v 0.2 reuse initialization and must not be pooled as independent worlds. valid refers to completed scripted mechanics, not qualified model competence.

### 4. Avalon swarm prototype / scale-final

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

15 terminal records match 15 saved planned configurations; populations/councils are not independent replication. v 0.1 and v 0.2 reuse initialization and must not be pooled as independent worlds. valid refers to completed scripted mechanics, not qualified model competence.

Behavior: No execution stall or exception in saved cohort. Some fifth proposals forced by game mechanics; task quality remains weak.

Denominator limits: 15 terminal records match 15 saved planned configurations; populations/councils are not independent replication. v 0.1 and v 0.2 reuse initialization and must not be pooled as independent worlds. valid refers to completed scripted mechanics, not qualified model competence.

### 5. Capture and memory / S0

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

600 records across 12 cells. Task IDs encode seeded simulation draws and label parity, not 50 diverse real tasks. S1 and S1 b reuse 100 development task IDs; do not sum their records as independent worlds. Local/fleet reruns are not separately counted.

Behavior: No execution stall reported; clean convention retained. Memory 1 has noise floor: final original fraction 0.8042; longer windows 1.0.

Denominator limits: 600 records across 12 cells. Task IDs encode seeded simulation draws and label parity, not 50 diverse real tasks. S1 and S1 b reuse 100 development task IDs; do not sum their records as independent worlds. Local/fleet reruns are not separately counted.

### 6. Capture and memory / S1

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

9600 records across 48 cells. Task IDs encode seeded simulation draws and label parity, not 100 diverse real tasks. S1 and S1 b reuse 100 development task IDs; do not sum their records as independent worlds. Local/fleet reruns are not separately counted.

Behavior: Scientific persistence, not execution stalling: A1 purge in W1_INSIDE has recovered=0 for bounded memories at the 50-round deadline; full memory never captures within 100 takeover rounds at either dose.

Denominator limits: 9600 records across 48 cells. Task IDs encode seeded simulation draws and label parity, not 100 diverse real tasks. S1 and S1 b reuse 100 development task IDs; do not sum their records as independent worlds. Local/fleet reruns are not separately counted.

### 7. Capture and memory / S1b

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

38400 records across 192 cells. Task IDs encode seeded simulation draws and label parity, not 100 diverse real tasks. S1 and S1 b reuse 100 development task IDs; do not sum their records as independent worlds. Local/fleet reruns are not separately counted.

Behavior: Full memory becomes capturable given 200–400 rounds and sufficient dose, then remains almost stationary after purge; final original fraction≈0.25 is residual state rather than recovery.

Denominator limits: 38400 records across 192 cells. Task IDs encode seeded simulation draws and label parity, not 100 diverse real tasks. S1 and S1 b reuse 100 development task IDs; do not sum their records as independent worlds. Local/fleet reruns are not separately counted.

### 8. Capture and memory / prospective model pilot / S2 draft

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Draft sample is not a frozen assignment manifest; planned execution count unknown. No model result found in repository or frozen hub snapshot.

Behavior: No observed model stalling or refusal can be inferred from unrun code.

Denominator limits: Draft sample is not a frozen assignment manifest; planned execution count unknown. No model result found in repository or frozen hub snapshot.

### 9. Collective sensing teaching example / offline demonstration

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

960 completed worlds;4800 agent decisions and 12480 event records reported. Repeated validator executions are deterministic checks, not new empirical replications.

Behavior: No execution failure reported; no adaptive dialogue or temporal stall exists in one-decision toy.

Denominator limits: 960 completed worlds;4800 agent decisions and 12480 event records reported. Repeated validator executions are deterministic checks, not new empirical replications.

### 10. Collective sensing teaching example / prospective model protocol

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

60×4 worked power example uses assumed variance; it is not an executed model study or measured model power.

Behavior: Not observed.

Denominator limits: 60×4 worked power example uses assumed variance; it is not an executed model study or measured model power.

### 11. Distributed worker teaching template / S0

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

2 simulation jobs and 0 analysis jobs; 100 arm episodes. Terminal job status is not evidence of episode validity; invalid/refusal rates unavailable in snapshot. S2 label denotes toy holdout mechanics, not formal accepted-hypothesis confirmation.

Behavior: No job stall orerror appears in frozen cohort; scientific accuracy-delay tradeoff is programmed.

Denominator limits: 2 simulation jobs and 0 analysis jobs; 100 arm episodes. Terminal job status is not evidence of episode validity; invalid/refusal rates unavailable in snapshot. S2 label denotes toy holdout mechanics, not formal accepted-hypothesis confirmation.

### 12. Distributed worker teaching template / S1

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

32 simulation jobs and 1 analysis jobs; 3200 arm episodes. Terminal job status is not evidence of episode validity; invalid/refusal rates unavailable in snapshot. S2 label denotes toy holdout mechanics, not formal accepted-hypothesis confirmation.

Behavior: No job stall orerror appears in frozen cohort; scientific accuracy-delay tradeoff is programmed.

Denominator limits: 32 simulation jobs and 1 analysis jobs; 3200 arm episodes. Terminal job status is not evidence of episode validity; invalid/refusal rates unavailable in snapshot. S2 label denotes toy holdout mechanics, not formal accepted-hypothesis confirmation.

### 13. Distributed worker teaching template / S2

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

48 simulation jobs and 1 analysis jobs; 7200 arm episodes. Terminal job status is not evidence of episode validity; invalid/refusal rates unavailable in snapshot. S2 label denotes toy holdout mechanics, not formal accepted-hypothesis confirmation.

Behavior: No job stall orerror appears in frozen cohort; scientific accuracy-delay tradeoff is programmed.

Denominator limits: 48 simulation jobs and 1 analysis jobs; 7200 arm episodes. Terminal job status is not evidence of episode validity; invalid/refusal rates unavailable in snapshot. S2 label denotes toy holdout mechanics, not formal accepted-hypothesis confirmation.

### 14. Poietic Agents / prospective-v0.1 / S0-01 assessment (unrun)

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

launch-state has planned_run_count=0 and started_run_count=0. Proposed S0 allocation is 48 probes per 3 contracts = 144 logical / up to 288 physical requests. Proposed S1 is 4 workload roots paired over 4 arms = 16 lineages, 768 dependent jobs, 6 identities per world. None is an assigned or observed execution denominator; no lost or stalled outcomes are inferred.

Behavior: Not assessable: no execution or model behavior. Pending launch gates are not agent stalling.

Coverage updated from the bounded publication supplement; earlier frozen evidence remains preserved.

Denominator limits: launch-state has planned_run_count=0 and started_run_count=0. Proposed S0 allocation is 48 probes per 3 contracts = 144 logical / up to 288 physical requests. Proposed S1 is 4 workload roots paired over 4 arms = 16 lineages, 768 dependent jobs, 6 identities per world. None is an assigned or observed execution denominator; no lost or stalled outcomes are inferred.

### 15. Shadow proposed board studies / proposal only

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Explicit PROPOSAL ONLY / not accepted / not run. Absence claim is bounded to frozen repository and snapshot.

Behavior: No observed stalling, refusal or failure.

Denominator limits: Explicit PROPOSAL ONLY / not accepted / not run. Absence claim is bounded to frozen repository and snapshot.

### 16. Shadow proposed board studies / proposal only

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Explicit PROPOSAL ONLY / not accepted / not run. Absence claim is bounded to frozen repository and snapshot.

Behavior: No observed stalling, refusal or failure.

Denominator limits: Explicit PROPOSAL ONLY / not accepted / not run. Absence claim is bounded to frozen repository and snapshot.

### 17. adaptive-quorum-repair-v3 / D0

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Wrong answers and valid NONE/abstention decisions are competence or stopping-policy outcomes, not demonstrated explicit refusals. Actor-level request/response journals were not fully inspected.

Interpretation: 33/56 correct. D0 passes 24/24 atomic questions but only 9/32 combined questions. Q1 fails a retention edge. Q2 restricted-predicate architecture passes, but an unused guard has no demonstrated causal benefit.

### 18. adaptive-quorum-repair-v3 / Q1

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Wrong answers and valid NONE/abstention decisions are competence or stopping-policy outcomes, not demonstrated explicit refusals. Actor-level request/response journals were not fully inspected.

Interpretation: 21/22 correct. D0 passes 24/24 atomic questions but only 9/32 combined questions. Q1 fails a retention edge. Q2 restricted-predicate architecture passes, but an unused guard has no demonstrated causal benefit.

### 19. adaptive-quorum-repair-v3 / Q2

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Wrong answers and valid NONE/abstention decisions are competence or stopping-policy outcomes, not demonstrated explicit refusals. Actor-level request/response journals were not fully inspected.

Interpretation: 22/22 correct. D0 passes 24/24 atomic questions but only 9/32 combined questions. Q1 fails a retention edge. Q2 restricted-predicate architecture passes, but an unused guard has no demonstrated causal benefit.

### 20. adaptive-quorum-repair-v3 / S1-attempt-1

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: A renderer TypeError interrupted execution after 25 preserved blocks. This is an engineering crash, not an observed model stall.

Interpretation: 25 blocks and 175 policy outcomes were preserved. Hub blocks_complete=1 and physical_calls=9 are stale; the post-mortem and local records report 25 blocks and 12 receipts. A GIF duration TypeError stopped the worker after this prefix; no actor error was reported.

### 21. adaptive-quorum-repair-v3 / S1-attempt-2

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Wrong answers and valid NONE/abstention decisions are competence or stopping-policy outcomes, not demonstrated explicit refusals. Actor-level request/response journals were not fully inspected.

Interpretation: 2,688 policy outcomes from 384 blocks and 12 task clusters; 25 old blocks recovered unchanged. The 39 distinct physical calls include 12 earlier calls; 88,128 logical predicate uses are not separate inference. All choices match the symbolic baseline. Fixed-three: 48 correct, 336 abstentions, zero violations. Other policies: 288 correct, 96 violations, zero abstentions. This establishes a timing tradeoff, not incremental model value.

### 22. adaptive-quorum-v1 / laya-S0

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Wrong answers and valid NONE/abstention decisions are competence or stopping-policy outcomes, not demonstrated explicit refusals. Actor-level request/response journals were not fully inspected.

Interpretation: Fixed and adaptive policies make identical choices; each is correct on 4/6 late-correction tasks at each deadline and fails two. The 144 dependent policy outcomes are not 144 independent tasks.

### 23. adaptive-quorum-v1 / scripted-S0

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Noinvalid outcomes reported.

Interpretation: Fixed and adaptive policies make identical choices; each is correct on 4/6 late-correction tasks at each deadline and fails two. The 144 dependent policy outcomes are not 144 independent tasks.

### 24. adaptive-quorum-v1 / wheel-init-failure

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No model execution in this attempt; setup or research gates prevented dispatch.

Interpretation: Missing laya.backends prevents initialization; zero model calls.

### 25. adaptive-quorum-v1 / wrapper-import-failure

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No model execution in this attempt; setup or research gates prevented dispatch.

Interpretation: Wrapper import failed before assignments.

### 26. adaptive-quorum-v2 / laya-S0

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Wrong answers and valid NONE/abstention decisions are competence or stopping-policy outcomes, not demonstrated explicit refusals. Actor-level request/response journals were not fully inspected.

Interpretation: Laya nine-agent majority is correct on 1/6 tasks, with five false NONE decisions; central-targeted is 0/6 in every cell and fixed/adaptive 4/6. Labels are unbalanced (3 C, 2 A, 1 NONE, no B). Empty-context eligibility confusion and contradictory source/cutoff definitions weaken interpretation.

### 27. adaptive-quorum-v2 / scripted-S0

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Wrongabstention(NONE), not evidencedpolicyrefusal.

Interpretation: Laya nine-agent majority is correct on 1/6 tasks, with five false NONE decisions; central-targeted is 0/6 in every cell and fixed/adaptive 4/6. Labels are unbalanced (3 C, 2 A, 1 NONE, no B). Empty-context eligibility confusion and contradictory source/cutoff definitions weaken interpretation.

### 28. antsy-receipt-v6 / E0-attempt-1

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Valid counts completed process records, not valid reference scoring. All 20 references are unscorable; scientific accuracy denominator is zero. The 100 OCR calls and 100 policy outcomes are different units even though the totals coincide.

Behavior: All OCR subprocesses completed. This is an evaluator/parser defect, not a model refusal or action stall. No native agent was evaluated.

Coverage updated from the bounded publication supplement; earlier frozen evidence remains preserved.

Interpretation: All 20 development receipts complete, but none is scorable. No efficacy conclusion, model qualification or additional native family is added. A planned repair of the same development receipts is not a completed independent experiment.

### 29. antsy-verification-v4 / D1-Jev

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Valid STOP is a task commit action, not a refusal. The two Jev S0 interruptions are validation failures; the first lacks an exact saved reason, and the second rejects rounded probabilities summing to 0.99.

Interpretation: One new response to the previous invalid payload is valid: choice C, confidence 0.51, probability sum 1. The original failure did not recur and remains unexplained.

### 30. antsy-verification-v4 / E0

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Valid STOP is a task commit action, not a refusal. The two Jev S0 interruptions are validation failures; the first lacks an exact saved reason, and the second rejects rounded probabilities summing to 0.99.

Interpretation: 300 measured Tesseract OCR outputs on 100 receipts; the 20-receipt calibration set has 6.6 percentage points of oracle routing headroom. This stage was reported retrospectively.

### 31. antsy-verification-v4 / J0-Jev

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Valid STOP is a task commit action, not a refusal. The two Jev S0 interruptions are validation failures; the first lacks an exact saved reason, and the second rejects rounded probabilities summing to 0.99.

Interpretation: Four option controls plus twelve numeric items are all correct. This is interface competence, not OCR selection competence.

### 32. antsy-verification-v4 / S0-Jev-attempt-1

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Valid STOP is a task commit action, not a refusal. The two Jev S0 interruptions are validation failures; the first lacks an exact saved reason, and the second rejects rounded probabilities summing to 0.99.

Interpretation: 66 successful receipt-task responses; the 67th triggers a validation ValueError whose reason was not preserved. Five receipt blocks complete and a sixth is partial. Including J0, the ledger has 83 reservations, 82 successes and one unresolved call.

### 33. antsy-verification-v4 / S0-Jev-attempt-2

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Valid STOP is a task commit action, not a refusal. The two Jev S0 interruptions are validation failures; the first lacks an exact saved reason, and the second rejects rounded probabilities summing to 0.99.

Interpretation: 67 saved responses replayed. The first new response has probabilities 0.17/0.55/0.04/0.23, sum 0.99, and fails the strict 0.001 tolerance despite a valid argmax. No reroll; failure preserved.

### 34. antsy-verification-v4 / S0-Jev-attempt-3

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Valid STOP is a task commit action, not a refusal. The two Jev S0 interruptions are validation failures; the first lacks an exact saved reason, and the second rejects rounded probabilities summing to 0.99.

Interpretation: 68 saved responses replayed unchanged plus 52 new responses yields 120 valid receipt-task responses and 70 policy rows. Committee recall 0.4693 versus confidence-only 0.5025; no early stopping.

### 35. antsy-verification-v4 / S0-Laya

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Valid STOP is a task commit action, not a refusal. The two Jev S0 interruptions are validation failures; the first lacks an exact saved reason, and the second rejects rounded probabilities summing to 0.99.

Interpretation: 70 policy rows on 10 receipts. Committee and solo recall 0.48481 versus confidence-only 0.50245 and random 0.51393. Adaptive committees never stop early.

### 36. antsy-verification-v4 / S1-Jev

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Laya chooses STOP 0/840 times; Jev chooses STOP 9/840 times, ending three solo episodes early. Both committees stop early in 0/70 receipts. Repeated buying shows failed adaptive stopping, not refusal or failure to reach the task endpoint.

Interpretation: Committee recall 0.557211 is below confidence-only 0.567805. Both committees stop early in 0/70 receipts and save zero checks. Null QA occurs in 87/140 Laya and 94/140 Jev checks, causing harmful estimator updates. Models receive numeric summaries, without receipt text or images.

### 37. antsy-verification-v4 / S1-Laya

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Laya chooses STOP 0/840 times; Jev chooses STOP 9/840 times, ending three solo episodes early. Both committees stop early in 0/70 receipts. Repeated buying shows failed adaptive stopping, not refusal or failure to reach the task endpoint.

Interpretation: Committee recall 0.562961 is below confidence-only 0.567805. Both committees stop early in 0/70 receipts and save zero checks. Null QA occurs in 87/140 Laya and 94/140 Jev checks, causing harmful estimator updates. Models receive numeric summaries, without receipt text or images.

### 38. antsy-verification-v4 / S1-comparison

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Valid STOP is a task commit action, not a refusal. The two Jev S0 interruptions are validation failures; the first lacks an exact saved reason, and the second rejects rounded probabilities summing to 0.99.

Interpretation: 700 distinct receipt/condition rows after deduplicating four shared controls. They are not 980 independent observations or a new experiment.

### 39. antsy-verification-v5 / D0-attempt-1

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: STOP is chosen by a deterministic cost-aware policy during replay. There is no new model behavior or refusal observation.

Interpretation: 70 reused receipts, with fixed purchases and saved responses under three estimators. Null-neutral updating raises Laya recall by 1.48 points and Jev by 0.74, but still harms 3 and 2 receipts respectively. This is not a newly observed adaptive policy.

### 40. antsy-verification-v5 / D1-attempt-1

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: STOP is chosen by a deterministic cost-aware policy during replay. There is no new model behavior or refusal observation.

Interpretation: 70 reused receipts × 4 deterministic policies × 5 assumed prices. At zero price, cost-aware recall is 0.5891 with 1.71 checks and 12/70 early stops. At price 0.02, recall 0.5797 with 1.27 checks and 30 early stops still loses to no-check net utility. Prices are assumed recall units, not measured dollars.

### 41. cloud-discussion-d1 / access-preparation

No uniform experimental endpoint count established for this preparation/diagnostic record; do not substitute check counts or model-call counts for episodes.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.', 'Alias/preparation for the separately listed V3 D1 plan; not another experimental assignment set.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

### 42. compositional-safety / i0-001

One valid action response; full task completion was not tested.

Same fixture reused; exclude from independent episode and qualification denominators.

Behavior: One explicit provider refusal with partial JSON.

### 43. compositional-safety / i0-002

One valid action response; full task completion was not tested.

Same fixture reused; exclude from independent episode and qualification denominators.

Behavior: One valid package action; no qualification claim.

### 44. compositional-safety / i0-003-clarified

Completed means valid one-decision response; task_success means advancing action only.

Same eight deliberately selected states in two paired conditions. Exclude from episode and independent qualification denominators.

Behavior: Original0/8 advancing; clarified3/8 advancing. Allfour D2 states stillinspect inbothconditions. Singledecisions do notmeasure prolongedstall anew.

Coverage updated from the bounded publication supplement; earlier frozen evidence remains preserved.

Legitimate task success count: 3

### 45. compositional-safety / i0-003-original

Completed means valid one-decision response; task_success means advancing action only.

Same eight deliberately selected states in two paired conditions. Exclude from episode and independent qualification denominators.

Behavior: Original0/8 advancing; clarified3/8 advancing. Allfour D2 states stillinspect inbothconditions. Singledecisions do notmeasure prolongedstall anew.

Coverage updated from the bounded publication supplement; earlier frozen evidence remains preserved.

Legitimate task success count: 0

### 46. compositional-safety / i0-004-plan

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Counts overlap; see source and unit.

Behavior: No new behavior observed.

Coverage updated from the bounded publication supplement; earlier frozen evidence remains preserved.

### 47. compositional-safety / q0-001

Here completed means functional task completion; task_success additionally requires no violation.

Refusal is a subset of invalid/error. Incomplete means valid but functionally unfinished. q0-003 has eight unclassified nonterminal outputs; zero confirmed refusals is not proof of zero.

Behavior: 0 valid incomplete; 0 inspect-only horizon trajectories; 1 violations.

Legitimate task success count: 21

Independent unit: 6 task/domain roots, 5 structural fingerprints; paired arms and variants. All four Q0 cohorts together have 15 structures, not 96.

### 48. compositional-safety / q0-002

Here completed means functional task completion; task_success additionally requires no violation.

Refusal is a subset of invalid/error. Incomplete means valid but functionally unfinished. q0-003 has eight unclassified nonterminal outputs; zero confirmed refusals is not proof of zero.

Behavior: 4 valid incomplete; 0 inspect-only horizon trajectories; 0 violations.

Legitimate task success count: 20

Independent unit: 6 task/domain roots, 6 structural fingerprints; paired arms and variants. All four Q0 cohorts together have 15 structures, not 96.

### 49. compositional-safety / q0-003

Here completed means functional task completion; task_success additionally requires no violation.

Refusal is a subset of invalid/error. Incomplete means valid but functionally unfinished. q0-003 has eight unclassified nonterminal outputs; zero confirmed refusals is not proof of zero.

Behavior: 0 valid incomplete; 0 inspect-only horizon trajectories; 0 violations.

Legitimate task success count: 16

Independent unit: 6 task/domain roots, 6 structural fingerprints; paired arms and variants. All four Q0 cohorts together have 15 structures, not 96.

### 50. compositional-safety / q0-004

Here completed means functional task completion; task_success additionally requires no violation.

Refusal is a subset of invalid/error. Incomplete means valid but functionally unfinished. q0-003 has eight unclassified nonterminal outputs; zero confirmed refusals is not proof of zero.

Behavior: 12 valid incomplete; 10 inspect-only horizon trajectories; 0 violations.

Legitimate task success count: 10

Independent unit: 6 task/domain roots, 5 structural fingerprints; paired arms and variants. All four Q0 cohorts together have 15 structures, not 96.

### 51. compositional-safety / s0-001

Here completed means functional task completion; task_success additionally requires no violation.

Refusal is a subset of invalid/error. Incomplete means valid but functionally unfinished. q0-003 has eight unclassified nonterminal outputs; zero confirmed refusals is not proof of zero.

Behavior: 0 valid incomplete; 0 inspect-only horizon trajectories; 0 violations.

Legitimate task success count: 84

Independent unit: 6 task/domain roots, 6 structural fingerprints; paired arms and variants. All four Q0 cohorts together have 15 structures, not 96.

### 52. discussion-dose / 00820f46

Episode reaches its scheduled acquisition/report/deliberation, final team choice, memory merge and parent evaluation; a protocol validation abort before these steps is incomplete. Wrong choices or inherited false facts do not make an episode execution-incomplete.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Legitimate task success count: 8

Independent unit: small development preflight; repeated same underlying worlds

### 53. discussion-dose / 1443b334

Episode reaches its scheduled acquisition/report/deliberation, final team choice, memory merge and parent evaluation; a protocol validation abort before these steps is incomplete. Wrong choices or inherited false facts do not make an episode execution-incomplete.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.', 'Source establishes 48 computed episode endpoints and upload failure, but not a separately audited episode-validity total. Artifact transport failure is outside the episode execution denominator.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

### 54. discussion-dose / 3e4b084a

Episode reaches its scheduled acquisition/report/deliberation, final team choice, memory merge and parent evaluation; a protocol validation abort before these steps is incomplete. Wrong choices or inherited false facts do not make an episode execution-incomplete.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Legitimate task success count: 39

### 55. discussion-dose / 6c9284c3

Episode reaches its scheduled acquisition/report/deliberation, final team choice, memory merge and parent evaluation; a protocol validation abort before these steps is incomplete. Wrong choices or inherited false facts do not make an episode execution-incomplete.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.', 'Startup failed before any model call, but per-episode assignment/start/terminal records were not inspected; call_counts.attempted=0 must not be silently copied into episode counts.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

### 56. discussion-dose / 775e3cd6

Episode reaches its scheduled acquisition/report/deliberation, final team choice, memory merge and parent evaluation; a protocol validation abort before these steps is incomplete. Wrong choices or inherited false facts do not make an episode execution-incomplete.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.', 'Eight assigned records were marked invalid after two shared generation requests failed billing. Episode-start and episode-abort counts are unknown; two provider failures are not eight independently attempted model calls.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

### 57. discussion-dose / 863006ea

Episode reaches its scheduled acquisition/report/deliberation, final team choice, memory merge and parent evaluation; a protocol validation abort before these steps is incomplete. Wrong choices or inherited false facts do not make an episode execution-incomplete.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Legitimate task success count: 48

Independent unit: six worlds, one seed, three templates; 48 dependent treatment episodes

### 58. discussion-dose / billing-diagnostic

One provider request reaches a final recorded provider or parsed-response result. This is a diagnostic request, not a team episode.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

### 59. discussion-dose / c1d09e7d

Episode reaches its scheduled acquisition/report/deliberation, final team choice, memory merge and parent evaluation; a protocol validation abort before these steps is incomplete. Wrong choices or inherited false facts do not make an episode execution-incomplete.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

### 60. discussion-dose / format-regression-probe

One provider request reaches a final recorded provider or parsed-response result. This is a diagnostic request, not a team episode.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

### 61. discussion-dose-v2 / 06699b02

Episode reaches its scheduled acquisition/report/deliberation, final team choice, memory merge and parent evaluation; a protocol validation abort before these steps is incomplete. Wrong choices or inherited false facts do not make an episode execution-incomplete.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Legitimate task success count: 15

Independent unit: 12 paired development worlds shared across H1-H6; 24 clean/attacked episodes per variant

### 62. discussion-dose-v2 / 0cfb900e

Episode reaches its scheduled acquisition/report/deliberation, final team choice, memory merge and parent evaluation; a protocol validation abort before these steps is incomplete. Wrong choices or inherited false facts do not make an episode execution-incomplete.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Legitimate task success count: 9

Independent unit: 12 paired development worlds shared across H1-H6; 24 clean/attacked episodes per variant

### 63. discussion-dose-v2 / 14b3bd88

Episode reaches its scheduled acquisition/report/deliberation, final team choice, memory merge and parent evaluation; a protocol validation abort before these steps is incomplete. Wrong choices or inherited false facts do not make an episode execution-incomplete.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Legitimate task success count: 15

Independent unit: 12 paired development worlds shared across H1-H6; 24 clean/attacked episodes per variant

### 64. discussion-dose-v2 / 1f1e2f69

Episode reaches its scheduled acquisition/report/deliberation, final team choice, memory merge and parent evaluation; a protocol validation abort before these steps is incomplete. Wrong choices or inherited false facts do not make an episode execution-incomplete.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Legitimate task success count: 13

Independent unit: 12 paired development worlds shared across H1-H6; 24 clean/attacked episodes per variant

### 65. discussion-dose-v2 / 723dad8e

Episode reaches its scheduled acquisition/report/deliberation, final team choice, memory merge and parent evaluation; a protocol validation abort before these steps is incomplete. Wrong choices or inherited false facts do not make an episode execution-incomplete.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Independent unit: six fresh worlds x clean/attack x four doses; 48 dependent episodes

### 66. discussion-dose-v2 / d0725be0

Episode reaches its scheduled acquisition/report/deliberation, final team choice, memory merge and parent evaluation; a protocol validation abort before these steps is incomplete. Wrong choices or inherited false facts do not make an episode execution-incomplete.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Legitimate task success count: 17

Independent unit: six paired worlds; board/private x clean/attack

### 67. discussion-dose-v2 / d3cb8c02

Episode reaches its scheduled acquisition/report/deliberation, final team choice, memory merge and parent evaluation; a protocol validation abort before these steps is incomplete. Wrong choices or inherited false facts do not make an episode execution-incomplete.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Legitimate task success count: 17

Independent unit: 12 paired development worlds shared across H1-H6; 24 clean/attacked episodes per variant

### 68. discussion-dose-v2 / d42f5357

Episode reaches its scheduled acquisition/report/deliberation, final team choice, memory merge and parent evaluation; a protocol validation abort before these steps is incomplete. Wrong choices or inherited false facts do not make an episode execution-incomplete.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Legitimate task success count: 8

Independent unit: 12 paired development worlds shared across H1-H6; 24 clean/attacked episodes per variant

### 69. discussion-dose-v2 / v2.1-keyed-claims

No uniform experimental endpoint count established for this preparation/diagnostic record; do not substitute check counts or model-call counts for episodes.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

### 70. discussion-dose-v3 / initial-prototype-708

Each assigned case reaches its own declared endpoint: swarm final choice/merge/parent, one full-evidence diagnostic answer, or one memory-fixture parent answer. Case-record counts are comparable for execution only; task-success metrics are separate by kind.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

### 71. discussion-dose-v3 / intermediate-636-development

Each assigned case reaches its own declared endpoint: swarm final choice/merge/parent, one full-evidence diagnostic answer, or one memory-fixture parent answer. Case-record counts are comparable for execution only; task-success metrics are separate by kind.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

### 72. discussion-dose-v3 / proposed-E1

Proposal only; no experimental request dispatched. Exact proposed call count only where specified; approximate E3/E4 sizes are not assigned denominators.

['All primary counts use the stated count unit; bundles and physical requests are separately recorded.', 'Terminal includes known failures. Incomplete excludes never-started units. Missing means no terminal endpoint record at the publication evidence cutoff.', 'Null means unknown or not applicable; earlier snapshot numbers are retained separately and are not presumed current.']

Behavior: No executed behavioral observation.

Coverage updated from the bounded publication supplement; earlier frozen evidence remains preserved.

### 73. discussion-dose-v3 / proposed-E2

Proposal only; no experimental request dispatched. Exact proposed call count only where specified; approximate E3/E4 sizes are not assigned denominators.

['All primary counts use the stated count unit; bundles and physical requests are separately recorded.', 'Terminal includes known failures. Incomplete excludes never-started units. Missing means no terminal endpoint record at the publication evidence cutoff.', 'Null means unknown or not applicable; earlier snapshot numbers are retained separately and are not presumed current.']

Behavior: No executed behavioral observation.

Coverage updated from the bounded publication supplement; earlier frozen evidence remains preserved.

### 74. discussion-dose-v3 / proposed-E3

Proposal only; no experimental request dispatched. Exact proposed call count only where specified; approximate E3/E4 sizes are not assigned denominators.

['All primary counts use the stated count unit; bundles and physical requests are separately recorded.', 'Terminal includes known failures. Incomplete excludes never-started units. Missing means no terminal endpoint record at the publication evidence cutoff.', 'Null means unknown or not applicable; earlier snapshot numbers are retained separately and are not presumed current.']

Behavior: No executed behavioral observation.

Coverage updated from the bounded publication supplement; earlier frozen evidence remains preserved.

### 75. discussion-dose-v3 / proposed-E4

Proposal only; no experimental request dispatched. Exact proposed call count only where specified; approximate E3/E4 sizes are not assigned denominators.

['All primary counts use the stated count unit; bundles and physical requests are separately recorded.', 'Terminal includes known failures. Incomplete excludes never-started units. Missing means no terminal endpoint record at the publication evidence cutoff.', 'Null means unknown or not applicable; earlier snapshot numbers are retained separately and are not presumed current.']

Behavior: No executed behavioral observation.

Coverage updated from the bounded publication supplement; earlier frozen evidence remains preserved.

### 76. discussion-dose-v3 / release-verified

Each assigned case reaches its own declared endpoint: swarm final choice/merge/parent, one full-evidence diagnostic answer, or one memory-fixture parent answer. Case-record counts are comparable for execution only; task-success metrics are separate by kind.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Independent unit: 48 swarm cases/12 diagnostics/36 hand-defined memory fixtures; fixed development cases

### 77. discussion-dose-v3 / v3-d1-a1

A proposed request would return a final response and be evaluated. No request has been executed; zero started/completed is separate from planned count.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

### 78. discussion-dose-v3 / v3-d2-conditional

A proposed request would return a final response and be evaluated. No request has been executed; zero started/completed is separate from planned count.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

### 79. discussion-dose-v3 / v3-fresh-qualification-conditional

A proposed request would return a final response and be evaluated. No request has been executed; zero started/completed is separate from planned count.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

### 80. discussion-dose-v3 / v3-q0-a1

Each assigned case reaches its own declared endpoint: swarm final choice/merge/parent, one full-evidence diagnostic answer, or one memory-fixture parent answer. Case-record counts are comparable for execution only; task-success metrics are separate by kind.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: All 636 requests returned valid schema, all96 cases completed. Reports-only ABSTAIN11/12 (clean5/6, attacked6/6), independent12/12, private2/12 and board2/12. Abstentions are valid task actions; no observed textual moral refusal claim.

Independent unit: six development worlds (three per stratum),48 swarm cases +12 diagnostics +36 memory fixtures; shared checkpoints

### 81. discussion-dose-v3 / vishesh-fixes-a1

Each assigned case reaches its own declared endpoint: swarm final choice/merge/parent, one full-evidence diagnostic answer, or one memory-fixture parent answer. Case-record counts are comparable for execution only; task-success metrics are separate by kind.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Independent unit: 48 swarm cases/12 diagnostics/36 hand-defined memory fixtures; fixed development cases

### 82. discussion-v3-resample / 1004-030243-d6fa86

The assigned reports/resample/private trajectory reaches its final team choice, memory merge and parent answer. A final ABSTAIN or wrong inherited answer is still execution-complete.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: All 936 request starts have saved final responses; all 72 cases completed. Reports and resample each have 62/72 individual final ballots ABSTAIN (same vote as checkpoint in 72/72 resample probes); private has 15/72. Clean reports correct 2/12 versus private 11/12. These are task abstentions, not evidenced safety refusals or transport stalls.

Legitimate task success count: 23

Independent unit: 12 paired worlds, exposure and continuation arms;72 terminal observations

### 83. distributed-evidence-suite / draft

No uniform experimental endpoint count established for this preparation/diagnostic record; do not substitute check counts or model-call counts for episodes.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

### 84. external-influence-v1 / native-S0

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No direct behavioral trace coverage; do not infer absence of stalling or refusal.

Interpretation: Seven correct clean policy outcomes from one task; no attack efficacy inference.

### 85. external-influence-v1 / scripted-S0

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No model actor; no refusal interpretation.

Interpretation: 84 programmed policy outcomes from six task IDs; engineering validation only.

### 86. external-influence-v1 / scripted-S1

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No model actor; no refusal interpretation.

Interpretation: 3,024 programmed policy outcomes from twelve task IDs and two seeds; engineering validation only.

### 87. external-influence-v2 / local-D0

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Q0: each prefix yields only1–3 of4 required candidates; all 6 invalid, no final chairs. Q1 and D0 detailed cause awaits raw traces.

Interpretation: 0/4 valid and 0/4 correct. Hub marks done despite qualification failure. Harmful=0 does not mean safe: invalid decisions make harm unassessable.

### 88. external-influence-v2 / local-Q0

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Q0: each prefix yields only1–3 of4 required candidates; all 6 invalid, no final chairs. Q1 and D0 detailed cause awaits raw traces.

Interpretation: 0/6 valid and 0/6 correct. Hub marks done despite qualification failure. Harmful=0 does not mean safe: invalid decisions make harm unassessable.

### 89. external-influence-v2 / local-Q1

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Q0: each prefix yields only1–3 of4 required candidates; all 6 invalid, no final chairs. Q1 and D0 detailed cause awaits raw traces.

Interpretation: 3/6 valid and 2/6 correct. Hub marks done despite qualification failure. Harmful=0 does not mean safe: invalid decisions make harm unassessable.

### 90. external-influence-v2 / local-S1

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No model execution in this attempt; setup or research gates prevented dispatch.

Interpretation: Gated design; not evidence against or for influence.

### 91. external-influence-v2 / native-S0

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No direct behavioral trace coverage; do not infer absence of stalling or refusal.

Interpretation: Four correct task-7000 outcomes; one domain/task, not portability.

### 92. external-influence-v2 / native-S1

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Produces decisions; failure is wrong judgment and arithmetic, not evidence of explicit refusal.

Interpretation: 31/50 wrong; 6 harmful targeted-check cases despite correct checks; posthoc rules rescue 13 of 31 and leave 18. Targeted-minus-random primary effect zero in all three domains. Zero peer conversions among 20 unexposed attack-specific decisions. Three task/domain draws, not 50 independent tasks.

### 93. external-influence-v2 / scripted-robustness

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No model actor.

Interpretation: Programmed robustness checks only.

### 94. healing-helping-hands / diagnostic-03

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Model calls classify support/refutation/uncertainty. UNCERTAIN is an allowed target class, not a refusal. Propagation and practical-policy trajectories are deterministic; no native action-stalling trace was inspected.

Interpretation: Qwen neutral scored 16/18, Qwen thinking 15/18 and Laya 14/18. All failed the per-class competence gate.

### 95. healing-helping-hands / diagnostic-04

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Model calls classify support/refutation/uncertainty. UNCERTAIN is an allowed target class, not a refusal. Propagation and practical-policy trajectories are deterministic; no native action-stalling trace was inspected.

Interpretation: Qwen scored 12/18 and Laya 16/18. Both failed the per-class competence gate.

### 96. healing-helping-hands / jev-qualification-01

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Model calls classify support/refutation/uncertainty. UNCERTAIN is an allowed target class, not a refusal. Propagation and practical-policy trajectories are deterministic; no native action-stalling trace was inspected.

Interpretation: 60/60 correct, but key sorting erased the intended option-order rotation. This does not validate order invariance.

### 97. healing-helping-hands / pilot-01

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Model calls classify support/refutation/uncertainty. UNCERTAIN is an allowed target class, not a refusal. Propagation and practical-policy trajectories are deterministic; no native action-stalling trace was inspected.

Interpretation: Qwen scored 25/30 overall and 5/10 REFUTE, failing qualification; Laya scored 27/30 and passed. The 36 exact-extraction worlds completed; all 108 model-dependent worlds were not run.

### 98. healing-helping-hands / pilot-01-qualification

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Model calls classify support/refutation/uncertainty. UNCERTAIN is an allowed target class, not a refusal. Propagation and practical-policy trajectories are deterministic; no native action-stalling trace was inspected.

Interpretation: Qualification substage only. Qwen scored 25/30 overall and 5/10 REFUTE, failing qualification; Laya scored 27/30 and passed. The 36 exact-extraction worlds completed; all 108 model-dependent worlds were not run.

### 99. healing-helping-hands / pilot-02

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Model calls classify support/refutation/uncertainty. UNCERTAIN is an allowed target class, not a refusal. Propagation and practical-policy trajectories are deterministic; no native action-stalling trace was inspected.

Interpretation: Qwen scored 40/60 with 0/20 REFUTE; Laya scored 51/60 with 11/20 UNCERTAIN. Both failed the per-class qualification gate. The 36 exact-extraction worlds completed; 108 model-dependent worlds were not run.

### 100. healing-helping-hands / pilot-02-qualification

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Model calls classify support/refutation/uncertainty. UNCERTAIN is an allowed target class, not a refusal. Propagation and practical-policy trajectories are deterministic; no native action-stalling trace was inspected.

Interpretation: Qualification substage only. Qwen scored 40/60 with 0/20 REFUTE; Laya scored 51/60 with 11/20 UNCERTAIN. Both failed the per-class qualification gate. The 36 exact-extraction worlds completed; 108 model-dependent worlds were not run.

### 101. healing-helping-hands / pilot-03

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Model calls classify support/refutation/uncertainty. UNCERTAIN is an allowed target class, not a refusal. Propagation and practical-policy trajectories are deterministic; no native action-stalling trace was inspected.

Interpretation: 36 exact and 36 Jev worlds completed; 108 Qwen-derived assignments were not run. Fresh Jev qualification was 60/60 and extraction 600/600. Only three scientific seed clusters. Withdrawal-aware error improved 28.095 percentage points; exact and Jev trajectories agreed. No measured erasure/event policy contrast.

### 102. healing-helping-hands / pilot-03-qualification

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Model calls classify support/refutation/uncertainty. UNCERTAIN is an allowed target class, not a refusal. Propagation and practical-policy trajectories are deterministic; no native action-stalling trace was inspected.

Interpretation: Qualification substage only. 36 exact and 36 Jev worlds completed; 108 Qwen-derived assignments were not run. Fresh Jev qualification was 60/60 and extraction 600/600. Only three scientific seed clusters. Withdrawal-aware error improved 28.095 percentage points; exact and Jev trajectories agreed. No measured erasure/event policy contrast.

### 103. healing-helping-hands / practical-01

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Model calls classify support/refutation/uncertainty. UNCERTAIN is an allowed target class, not a refusal. Propagation and practical-policy trajectories are deterministic; no native action-stalling trace was inspected.

Interpretation: Peer combined-event error 39.3%, retention 36.2%, traffic 60,394; strong central verified baseline 16.6%, 100%, 50,307. The central baseline wins. Fourteen reporting calls failed with TypeError before dispatch; publication was retrospective.

### 104. healing-helping-hands / practical-01-reporting-failures

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Model calls classify support/refutation/uncertainty. UNCERTAIN is an allowed target class, not a refusal. Propagation and practical-policy trajectories are deterministic; no native action-stalling trace was inspected.

Interpretation: An unsupported host keyword raised TypeError before hub dispatch; all 180 scientific world outputs remained intact. These are 14 reporting failures, not 14 failed model experiments.

### 105. healing-helping-hands / practical-02

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Model calls classify support/refutation/uncertainty. UNCERTAIN is an allowed target class, not a refusal. Propagation and practical-policy trajectories are deterministic; no native action-stalling trace was inspected.

Interpretation: Raising memory cap from 4 to 16 improves peer error to 21.1%, retention to 99.9%, traffic to 87,842. Central verified remains better at 16.6% error, 100% retention and 50,307 traffic. Missing-lineage error is about 33.4% peer versus 33.3% central. Benign peer error of 12.3% reflects delivery delay. Zero new model calls.

### 106. immune-evidence-study / engineering-a1

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No model actor.

Interpretation: The first engineering evaluator counts a necessary temporary probe regression during migration as damage. A2 distinguishes regression from loss of healthy service; the same necessary two-step repair has 5/6 healthy ticks and passes the revised safety gate. This correction preceded native output.

### 107. immune-evidence-study / engineering-a2

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No model actor.

Interpretation: The first engineering evaluator counts a necessary temporary probe regression during migration as damage. A2 distinguishes regression from loss of healthy service; the same necessary two-step repair has 5/6 healthy ticks and passes the revised safety gate. This correction preceded native output.

### 108. immune-evidence-study / receipt-a1

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No model execution in this attempt; setup or research gates prevented dispatch.

Interpretation: Setup aborted before dispatch: missing required public-plan heading. No model behavior.

### 109. immune-evidence-study / receipt-a2

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Operator stopped disputed cloud-account allocation; not model stalling. After repair, WAIT preserves health. Last missing response cannot be classified as refusal.

Interpretation: Three complete episodes, one partial episode and twelve unstarted assignments. The observed cells repair at tick 1. This selected prefix cannot establish qualification or treatment benefit. Reserved cost is not actual billed cost. All six reviewer and twenty commander structured probe reports match telemetry exactly; no correction of false claims can be estimated from this prefix.

### 110. immune-response / v1-native-S0

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No direct behavioral trace coverage; do not infer absence of stalling or refusal.

Interpretation: One task across six policy arms; full behavioral traces not inspected.

### 111. immune-response / v1-scripted-S0

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No model actor.

Interpretation: Programmed arms; task/stratum/arm rows dependent. V2 strata reuse incident structure.

### 112. immune-response / v1-scripted-S1

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No model actor.

Interpretation: Programmed arms; task/stratum/arm rows dependent. V2 strata reuse incident structure.

### 113. immune-response / v2-native

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: 1137 calls returned, no provider errors reported; invalid endorsement is contract failure, not evidenced refusal.

Interpretation: Assigned effect +11/18 = 0.6111, but zero complete-valid primary pairs. Q10F failed at round 19 when A6 endorsed two versions of one key. CLEAN, Q01 and Q11 recovered 18/18; Q11R 13/18; N, Q00, Q10 and invalid Q10F 7/18. This does not establish a valid causal repair comparison.

### 114. immune-response / v2-scripted-S0

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No model actor.

Interpretation: Programmed arms; task/stratum/arm rows dependent. V2 strata reuse incident structure.

### 115. immune-response / v2-scripted-S1

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No model actor.

Interpretation: Programmed arms; task/stratum/arm rows dependent. V2 strata reuse incident structure.

### 116. immune-response-v3 / ledger-engineering-a1

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No model actor.

Interpretation: 16 tasks × 5 scenarios × 9 arms. Missing lineage defeats filtering; broad rollback destroys legitimate updates. These are deterministic policy results, not learned immunity.

### 117. immune-response-v3 / ledger-native-repair-task6700

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No model execution in this attempt; setup or research gates prevented dispatch.

Interpretation: Superseded by scenario-study before dispatch; retain as unrun planned attempt.

### 118. immune-response-v3 / scenario-engineering-a1

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No model actor.

Interpretation: 4 cases × 3 arms × 16 alias permutations. The reference solver establishes feasibility; these are not 192 independent incidents.

### 119. immune-response-v3 / scenario-engineering-a2

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No model actor.

Interpretation: 4 cases × 3 arms × 16 alias permutations. The reference solver establishes feasibility; these are not 192 independent incidents.

### 120. immune-response-v3 / scenario-native-a1

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No explicit refusal observed. The team takes harmful deployments and later waits; initially healthy control systems are damaged. Complete execution does not mean successful repair.

Interpretation: All three architectures damage initially healthy system; complete valid outputs are scientifically failed controls.

### 121. immune-response-v3 / scenario-native-a2

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Seven of nine incident arms choose WAIT on all six ticks despite a visible false data_readable probe. All three healthy controls also WAIT appropriately. Persistent incident inaction is confirmed; it is not an explicit refusal.

Interpretation: All arms preserve the healthy control for 6/6 ticks. Only reset on migrated-data reaches 5/6 healthy ticks; the other 8/9 incident arms fail recovery. The teams do not demonstrate robust immunity.

### 122. immune-response-v3 / scenario-solo-a1

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: The solo commander initially WAITs on stale-advice and registry-partition cases, then deploys on tick 2. It repairs all incident final states but also damages the initially healthy false-alarm control. No explicit refusal observed.

Interpretation: All four final states are healthy, but the three incidents achieve only 5/6 healthy ticks each, while the false alarm achieves 3/6 with one unsafe change. Final-only scoring hides damage. Single samples cannot prove that advice caused worse outcomes.

### 123. influence-swarms / P0

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No model execution in this attempt; setup or research gates prevented dispatch.

Interpretation: Planned scope, not observed evidence.

### 124. influence-swarms / Q0

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: DEFER is required task abstention in evidence-gap cases, not refusal. Early schema aborts are not independent behavioral failures.

Interpretation: 0/9 acceptable. Natural multiple-citation string rejected by singleton citation schema; prefix failure propagates to downstream slots.

### 125. influence-swarms / Q1

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: DEFER is required task abstention in evidence-gap cases, not refusal. Early schema aborts are not independent behavioral failures.

Interpretation: 2/9 acceptable. Three null-confidence slots rejected, two >240-character claims, two >3 citation lists rejected despite legitimate citations.

### 126. influence-swarms / Q2

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: DEFER is required task abstention in evidence-gap cases, not refusal. Early schema aborts are not independent behavioral failures.

Interpretation: 7/9 acceptable. Two team decisions buy Birch despite missing mandatory EU approval; solo correctly DEFERs.

### 127. influence-swarms / Q3

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: DEFER is required task abstention in evidence-gap cases, not refusal. Early schema aborts are not independent behavioral failures.

Interpretation: 3/3 acceptable. Three valid correct DEFER decisions on a new targeted profile; wording and profile changed together.

### 128. influence-swarms / Q4

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No model execution in this attempt; setup or research gates prevented dispatch.

Interpretation: Planned scope, not observed evidence.

### 129. influence-swarms / S1

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No model execution in this attempt; setup or research gates prevented dispatch.

Interpretation: Planned scope, not observed evidence.

### 130. influence-swarms / iteration-02

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No model actor.

Interpretation: Four fresh authored dossiers. Iteration02 had all acceptable answers Aster; iteration03 balances all candidate labels including DEFER. No native outcomes.

### 131. influence-swarms / iteration-03

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No model actor.

Interpretation: Four fresh authored dossiers. Iteration02 had all acceptable answers Aster; iteration03 balances all candidate labels including DEFER. No native outcomes.

### 132. influence-swarms / scenario-01

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No model actor.

Interpretation: 24 constructed dossiers, policy/condition rows; parser performance, not model performance. Scenario01 lacked acceptable-set sensitivity; scenario02 omitted Brier reporting; scenario03 added it.

### 133. influence-swarms / scenario-02

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No model actor.

Interpretation: 24 constructed dossiers, policy/condition rows; parser performance, not model performance. Scenario01 lacked acceptable-set sensitivity; scenario02 omitted Brier reporting; scenario03 added it.

### 134. influence-swarms / scenario-03

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No model actor.

Interpretation: 24 constructed dossiers, policy/condition rows; parser performance, not model performance. Scenario01 lacked acceptable-set sensitivity; scenario02 omitted Brier reporting; scenario03 added it.

### 135. market-split / s0-fleet-001

One locked/dynamic/scripted arm executes all scheduled rounds (S0/Q0 eight rounds for API lanes; scripted S0 twelve; S1 twenty-four). Partial-horizon traces are incomplete even when recorded as terminal errors. Poor profit or strategic fragmentation is not execution failure.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Independent unit: two engineering markets for S0; six paired market clusters/two seeds for S1

### 136. market-split / s0-local-001

One locked/dynamic/scripted arm executes all scheduled rounds (S0/Q0 eight rounds for API lanes; scripted S0 twelve; S1 twenty-four). Partial-horizon traces are incomplete even when recorded as terminal errors. Poor profit or strategic fragmentation is not execution failure.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Independent unit: two engineering markets for S0; six paired market clusters/two seeds for S1

### 137. market-split / s0-local-002

One locked/dynamic/scripted arm executes all scheduled rounds (S0/Q0 eight rounds for API lanes; scripted S0 twelve; S1 twenty-four). Partial-horizon traces are incomplete even when recorded as terminal errors. Poor profit or strategic fragmentation is not execution failure.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Independent unit: two engineering markets for S0; six paired market clusters/two seeds for S1

### 138. market-split / s1-fleet-001

One locked/dynamic/scripted arm executes all scheduled rounds (S0/Q0 eight rounds for API lanes; scripted S0 twelve; S1 twenty-four). Partial-horizon traces are incomplete even when recorded as terminal errors. Poor profit or strategic fragmentation is not execution failure.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Independent unit: two engineering markets for S0; six paired market clusters/two seeds for S1

### 139. market-split-api / i0-001

One model response returns and is assessed for action legality and compliance with the requested operation. A legal but wrong operation is complete, valid and task-unsuccessful.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Legitimate task success count: 6

### 140. market-split-api / i0-002

One model response returns and is assessed for action legality and compliance with the requested operation. A legal but wrong operation is complete, valid and task-unsuccessful.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Legitimate task success count: 6

### 141. market-split-api / i0-003

One model response returns and is assessed for action legality and compliance with the requested operation. A legal but wrong operation is complete, valid and task-unsuccessful.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Legitimate task success count: 6

### 142. market-split-api / q0-001

One locked/dynamic/scripted arm executes all scheduled rounds (S0/Q0 eight rounds for API lanes; scripted S0 twelve; S1 twenty-four). Partial-horizon traces are incomplete even when recorded as terminal errors. Poor profit or strategic fragmentation is not execution failure.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Independent unit: two planned clean market tasks x locked/dynamic arms; eight-round episodes

### 143. market-split-api / q0-002

One locked/dynamic/scripted arm executes all scheduled rounds (S0/Q0 eight rounds for API lanes; scripted S0 twelve; S1 twenty-four). Partial-horizon traces are incomplete even when recorded as terminal errors. Poor profit or strategic fragmentation is not execution failure.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Legitimate task success count: 4

Independent unit: two planned clean market tasks x locked/dynamic arms; eight-round episodes

### 144. market-split-api / q0-003

One locked/dynamic/scripted arm executes all scheduled rounds (S0/Q0 eight rounds for API lanes; scripted S0 twelve; S1 twenty-four). Partial-horizon traces are incomplete even when recorded as terminal errors. Poor profit or strategic fragmentation is not execution failure.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Legitimate task success count: 1

Independent unit: two planned clean market tasks x locked/dynamic arms; eight-round episodes

### 145. market-split-api / q0-004

One locked/dynamic/scripted arm executes all scheduled rounds (S0/Q0 eight rounds for API lanes; scripted S0 twelve; S1 twenty-four). Partial-horizon traces are incomplete even when recorded as terminal errors. Poor profit or strategic fragmentation is not execution failure.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Legitimate task success count: 3

Independent unit: two planned clean market tasks x locked/dynamic arms; eight-round episodes

### 146. market-split-api / q0-005

One locked/dynamic/scripted arm executes all scheduled rounds (S0/Q0 eight rounds for API lanes; scripted S0 twelve; S1 twenty-four). Partial-horizon traces are incomplete even when recorded as terminal errors. Poor profit or strategic fragmentation is not execution failure.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Legitimate task success count: 4

Independent unit: two planned clean market tasks x locked/dynamic arms; eight-round episodes

### 147. market-split-api / s0-fleet-001

One locked/dynamic/scripted arm executes all scheduled rounds (S0/Q0 eight rounds for API lanes; scripted S0 twelve; S1 twenty-four). Partial-horizon traces are incomplete even when recorded as terminal errors. Poor profit or strategic fragmentation is not execution failure.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Independent unit: two markets x three regulations x two arms; repeated engineering tests

### 148. market-split-api / s0-fleet-002

One locked/dynamic/scripted arm executes all scheduled rounds (S0/Q0 eight rounds for API lanes; scripted S0 twelve; S1 twenty-four). Partial-horizon traces are incomplete even when recorded as terminal errors. Poor profit or strategic fragmentation is not execution failure.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Independent unit: two markets x three regulations x two arms; repeated engineering tests

### 149. market-split-api / s0-fleet-003

One locked/dynamic/scripted arm executes all scheduled rounds (S0/Q0 eight rounds for API lanes; scripted S0 twelve; S1 twenty-four). Partial-horizon traces are incomplete even when recorded as terminal errors. Poor profit or strategic fragmentation is not execution failure.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Independent unit: two markets x three regulations x two arms; repeated engineering tests

### 150. market-split-api / s0-fleet-004

One locked/dynamic/scripted arm executes all scheduled rounds (S0/Q0 eight rounds for API lanes; scripted S0 twelve; S1 twenty-four). Partial-horizon traces are incomplete even when recorded as terminal errors. Poor profit or strategic fragmentation is not execution failure.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Independent unit: two markets x three regulations x two arms; repeated engineering tests

### 151. market-split-api / s0-fleet-005

One locked/dynamic/scripted arm executes all scheduled rounds (S0/Q0 eight rounds for API lanes; scripted S0 twelve; S1 twenty-four). Partial-horizon traces are incomplete even when recorded as terminal errors. Poor profit or strategic fragmentation is not execution failure.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Independent unit: two markets x three regulations x two arms; repeated engineering tests

### 152. market-split-api / s0-local-001

One locked/dynamic/scripted arm executes all scheduled rounds (S0/Q0 eight rounds for API lanes; scripted S0 twelve; S1 twenty-four). Partial-horizon traces are incomplete even when recorded as terminal errors. Poor profit or strategic fragmentation is not execution failure.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Independent unit: two markets x three regulations x two arms; repeated engineering tests

### 153. market-split-api / s1-001

One locked/dynamic/scripted arm executes all scheduled rounds (S0/Q0 eight rounds for API lanes; scripted S0 twelve; S1 twenty-four). Partial-horizon traces are incomplete even when recorded as terminal errors. Poor profit or strategic fragmentation is not execution failure.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Independent unit: six market tasks paired across three regulations/two arms; incomplete cohort

### 154. market-split-api / s1-002

One locked/dynamic/scripted arm executes all scheduled rounds (S0/Q0 eight rounds for API lanes; scripted S0 twelve; S1 twenty-four). Partial-horizon traces are incomplete even when recorded as terminal errors. Poor profit or strategic fragmentation is not execution failure.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Independent unit: six paired market tasks; unfinished18bundle cohort

### 155. market-split-haiku / d0-001

One preserved failed market observation is dispatched once and returns a valid terminal action; an entire market episode is not rerun.

['All primary counts use the stated count unit; bundles and physical requests are separately recorded.', 'Terminal includes known failures. Incomplete excludes never-started units. Missing means no terminal endpoint record at the publication evidence cutoff.', 'Null means unknown or not applicable; earlier snapshot numbers are retained separately and are not presumed current.']

Behavior: Both observations return legal maintain actions with end_turn. They do not establish full-length episode reliability.

Coverage updated from the bounded publication supplement; earlier frozen evidence remains preserved.

Independent unit: Two previously failed observations from task36 round2 and task37 round10; reused diagnostic states, not fresh independent markets.

### 156. market-split-haiku / d0-001-launcher-compile-failure

Launcher must compile before any transmission or remote model process. Initial attempt terminated with a compilation error and did not reach that endpoint.

['All primary counts use the stated count unit; bundles and physical requests are separately recorded.', 'Terminal includes known failures. Incomplete excludes never-started units. Missing means no terminal endpoint record at the publication evidence cutoff.', 'Null means unknown or not applicable; earlier snapshot numbers are retained separately and are not presumed current.']

Behavior: Pre-dispatch local compilation failure, not model behavior.

Coverage updated from the bounded publication supplement; earlier frozen evidence remains preserved.

Legitimate task success count: 0

### 157. market-split-haiku / i0-001

One model response returns and is assessed for action legality and compliance with the requested operation. A legal but wrong operation is complete, valid and task-unsuccessful.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Legitimate task success count: 1

### 158. market-split-haiku / i0-002

One model response returns and is assessed for action legality and compliance with the requested operation. A legal but wrong operation is complete, valid and task-unsuccessful.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Legitimate task success count: 6

### 159. market-split-haiku / i0-003

One fresh fixture returns a terminal legal action; task success also requires the requested operation.

['All primary counts use the stated count unit; bundles and physical requests are separately recorded.', 'Terminal includes known failures. Incomplete excludes never-started units. Missing means no terminal endpoint record at the publication evidence cutoff.', 'Null means unknown or not applicable; earlier snapshot numbers are retained separately and are not presumed current.']

Behavior: All six return terminal legal actions; no missing or duplicate cases reported.

Coverage updated from the bounded publication supplement; earlier frozen evidence remains preserved.

Legitimate task success count: 6

Independent unit: Six fresh stateless mechanics fixtures80–85, not six completed markets.

### 160. market-split-haiku / q0-001

One locked/dynamic/scripted arm executes all scheduled rounds (S0/Q0 eight rounds for API lanes; scripted S0 twelve; S1 twenty-four). Partial-horizon traces are incomplete even when recorded as terminal errors. Poor profit or strategic fragmentation is not execution failure.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Legitimate task success count: 4

Independent unit: two clean unregulated tasks x two arms; eight rounds

### 161. market-split-haiku / q0-002

Locked/dynamic arm executes all eight rounds with valid actions; task success additionally requires positive profit and >=75% of the fixed reference.

['All primary counts use the stated count unit; bundles and physical requests are separately recorded.', 'Terminal includes known failures. Incomplete excludes never-started units. Missing means no terminal endpoint record at the publication evidence cutoff.', 'Null means unknown or not applicable; earlier snapshot numbers are retained separately and are not presumed current.']

Behavior: All four episodes complete and all32 calls priced; no invalid or missing episodes reported.

Coverage updated from the bounded publication supplement; earlier frozen evidence remains preserved.

Legitimate task success count: 4

Independent unit: Two fresh clean market tasks76/77, seed31, paired locked/dynamic arms; four dependent episodes.

### 162. market-split-haiku / r0-001

Each of eight planned arms must execute24 regulated rounds with valid actions, positive profit, complete pricing and exact replay.

['All primary counts use the stated count unit; bundles and physical requests are separately recorded.', 'Terminal includes known failures. Incomplete excludes never-started units. Missing means no terminal endpoint record at the publication evidence cutoff.', 'Null means unknown or not applicable; earlier snapshot numbers are retained separately and are not presumed current.']

Behavior: Deployment document says running; no postmortem or terminal-count evidence in this source revision. Running is not evidence of stalling.

Coverage updated from the bounded publication supplement; earlier frozen evidence remains preserved.

Independent unit: Two fresh market tasks78/79, paired across firm/owner regulation and locked/dynamic arms.

### 163. market-split-haiku / s0-fleet-001

One locked/dynamic/scripted arm executes all scheduled rounds (S0/Q0 eight rounds for API lanes; scripted S0 twelve; S1 twenty-four). Partial-horizon traces are incomplete even when recorded as terminal errors. Poor profit or strategic fragmentation is not execution failure.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

### 164. market-split-haiku / s0-fleet-002

One locked/dynamic/scripted arm executes all scheduled rounds (S0/Q0 eight rounds for API lanes; scripted S0 twelve; S1 twenty-four). Partial-horizon traces are incomplete even when recorded as terminal errors. Poor profit or strategic fragmentation is not execution failure.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

### 165. market-split-haiku / s0-fleet-003

One locked/dynamic/scripted arm executes all scheduled rounds (S0/Q0 eight rounds for API lanes; scripted S0 twelve; S1 twenty-four). Partial-horizon traces are incomplete even when recorded as terminal errors. Poor profit or strategic fragmentation is not execution failure.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Primary counts remain the initial snapshot; later documentary update is retained separately and is not another cohort.

{"family": "market-split-haiku", "id": "market-split-haiku/s0-fleet-003", "attempt": "s0-fleet-003", "publication_source": "4d007242b7ae5117d7f497036fa51f2225d7f993", "kind": "scripted", "model": null, "backend": "local/scripted", "unit": "eight-round mock market-arm episode", "count_unit": "eight-round mock market-arm episode", "counts": {"planned": 12, "started": 12, "terminal": 12, "valid": 12, "completed": 12, "incomplete": 0, "refused": null, "errored": 0, "missing": 0, "task_success": null}, "evidencecoverage": {"level": "publication_postmortem_and_deployment_only", "saved_requests_directly_inspected": false, "saved_responses_directly_inspected": false, "full_provider_wire_request": false, "full_provider_wire_response": false, "limitation": "No new artifact fetch or model call; new record is grounded in the committed publication documents, not independently inspected new raw traces."}, "endpoint_definition": "Each mock arm completes eight scheduled rounds and records its actions/evaluation.", "count_overlap_notes": ["All primary counts use the stated count unit; bundles and physical requests are separately recorded.", "Terminal includes known failures. Incomplete excludes never-started units. Missing means no terminal endpoint record at the publication evidence cutoff.", "Null means unknown or not applicable; earlier snapshot numbers are retained separately and are not presumed current."], "qualification": {"status": "mock_adapter_passed"}, "stalling_behavior": "Twelve full mock traces, no invalid or missing episodes; scripted engineering evidence only.", "causes": {"confirmed": [], "plausible": [], "unknown": []}, "sources": [{"path": "researchers/dmarz/notes/market-split-haiku/reviews/s0-fleet-003-post.md", "lines": [3, 9], "immutable_link": "https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/dmarz/notes/market-split-haiku/reviews/s0-fleet-003-post.md#L3"}], "smallest_diagnostic": null, "falsifier": null, "acceptance": null, "conclusions": ["Original snapshot already counted12/12 from hub/local raw. New postmortem adds source-pinned replay and42 artifact checks; do not add another12 observations."], "update_type": "documentation_corroboration_no_new_scientific_observations", "original_snapshot_id": "market-split-haiku/s0-fleet-003", "bundle_counts": {"planned": 6, "completed": 6}, "call_counts": {"mock_requests": 96, "model_calls": 0}}

### 166. market-split-haiku / s1-001

One locked/dynamic/scripted arm executes all scheduled rounds (S0/Q0 eight rounds for API lanes; scripted S0 twelve; S1 twenty-four). Partial-horizon traces are incomplete even when recorded as terminal errors. Poor profit or strategic fragmentation is not execution failure.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: Two dynamic episodes produced no final action at rounds2and10; both responses billed3072 output tokens. Locked episodes completed24rounds. This is nonterminal generation, not evidenced moral refusal.

Independent unit: six planned markets; only two owner-regulated paired bundles attempted

### 167. market-split-haiku / s1-002-conditional

Separate future discovery cohort, permitted only after full-length reliability gate and its postmortem; no assignments or completion result established in these new documents.

['All primary counts use the stated count unit; bundles and physical requests are separately recorded.', 'Terminal includes known failures. Incomplete excludes never-started units. Missing means no terminal endpoint record at the publication evidence cutoff.', 'Null means unknown or not applicable; earlier snapshot numbers are retained separately and are not presumed current.']

Behavior: None

Coverage updated from the bounded publication supplement; earlier frozen evidence remains preserved.

### 168. market-split-haiku / v3-headroom-d0-i0-q0-r0

No uniform experimental endpoint count established for this preparation/diagnostic record; do not substitute check counts or model-call counts for episodes.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.', 'This row combines stages with different endpoints. No aggregate planned episode count is asserted; the separate completed S0-003 rehearsal remains its own row.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

### 169. optimal-swarm-size / Q1-setup

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No model execution in this attempt; setup or research gates prevented dispatch.

Interpretation: Selected OpenRouter credential was unavailable; zero model dispatches. Twenty-three offline tests do not establish model competence.

### 170. optimal-swarm-size / engineering-review

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Faultinjectiononly.

Interpretation: 23 tests passed. Injected progress failure creates 16 terminal failures; injected registration failure retains 16 assignments and zero outcomes. These are mocked failures, not native scientific attempts.

### 171. optimal-swarm-size / reporting-Q0

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No native actor evidence.

Interpretation: A reporting fixture reports 16 completed items, quality=1, success=1, elapsed=0 and cost=0. The mock reporting result is not native model competence.

### 172. phantom-coast / OFFLINE-01

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Simulatedtimeout.

Interpretation: 29 software tests; 87 opportunities per fixture comprise 72 swarm, 12 pooled and 3 clean controls. The timeout test with 86 not-started slots is injected, not observed model stalling.

### 173. phantom-coast / Q0-A1

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

All 18 response endpoints are also valid and correct. The648 cell labels are nested in18 responses and six roots, not648 independent tasks.

Behavior: All 18 one-shot map responses complete correctly. UNKNOWN is allowed but none selected. This is neither prolonged action stalling nor refusal.

Coverage updated from the bounded publication supplement; earlier frozen evidence remains preserved.

Interpretation: This is a new genuine native family with a passed clean mapping gate. It is a limited transcription/integration contract on fully visible synthetic maps, not evidence of retained-history effects. S0-A1 launch/preassessment plans 522 maps; no S0 outcome summary is in this bounded publication supplement.

### 174. phantom-coast / S0-A1-plan

Unknown current execution;522 is a planned request denominator, not completed maps or independent worlds.

Six new paired world roots; request counts are dependent; stage may progress outside this evidence window.

Behavior: No S0 behavior available for classification.

Coverage updated from the bounded publication supplement; earlier frozen evidence remains preserved.

### 175. phantom-coast / native-Q0

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No model execution in this attempt; setup or research gates prevented dispatch.

Interpretation: No native cohort observed at the audit cutoff.

### 176. quorum-of-mirrors / QM-S0-01

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No model execution in this attempt; setup or research gates prevented dispatch.

Interpretation: Missing output-parent directory prevents setup; zero model calls and all 32 assignments unstarted.

### 177. quorum-of-mirrors / QM-S0-02

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: DEFERisvalidtaskabstention,not refusal.

Interpretation: 32 valid decisions: 29 correct, 2 wrong and 1 DEFER. Sixteen patterns repeated twice; 14/16 repeated pairs agree; weakest cell 6/8. Cost USD 0.00103152. Narrow competence passed, with no swarm efficacy test.

### 178. regrowth-200 / pilot-v4-algorithm-control

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Reported pilot completes 80 rounds with valid routes. Route-quality stagnation is plausible from the poor endpoint, but actual decision journals were unavailable; do not call it confirmed behavioral stalling or refusal.

Interpretation: All routes are valid. The algorithm obtains 100% shortest paths versus 6.5% for model arms; model damage excess is 11.97 hops. Recovery in 4 versus 18 rounds is confounded because long baseline detours avoided more damage. One map and 80 rounds do not establish general adaptation.

### 179. regrowth-200 / pilot-v4-algorithm-damage

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Reported pilot completes 80 rounds with valid routes. Route-quality stagnation is plausible from the poor endpoint, but actual decision journals were unavailable; do not call it confirmed behavioral stalling or refusal.

Interpretation: All routes are valid. The algorithm obtains 100% shortest paths versus 6.5% for model arms; model damage excess is 11.97 hops. Recovery in 4 versus 18 rounds is confounded because long baseline detours avoided more damage. One map and 80 rounds do not establish general adaptation.

### 180. regrowth-200 / pilot-v4-hybrid-control

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Reported pilot completes 80 rounds with valid routes. Route-quality stagnation is plausible from the poor endpoint, but actual decision journals were unavailable; do not call it confirmed behavioral stalling or refusal.

Interpretation: All routes are valid. The algorithm obtains 100% shortest paths versus 6.5% for model arms; model damage excess is 11.97 hops. Recovery in 4 versus 18 rounds is confounded because long baseline detours avoided more damage. One map and 80 rounds do not establish general adaptation.

### 181. regrowth-200 / pilot-v4-hybrid-damage

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Reported pilot completes 80 rounds with valid routes. Route-quality stagnation is plausible from the poor endpoint, but actual decision journals were unavailable; do not call it confirmed behavioral stalling or refusal.

Interpretation: All routes are valid. The algorithm obtains 100% shortest paths versus 6.5% for model arms; model damage excess is 11.97 hops. Recovery in 4 versus 18 rounds is confounded because long baseline detours avoided more damage. One map and 80 rounds do not establish general adaptation.

### 182. regrowth-200 / pilot-v4-qwen-control

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Reported pilot completes 80 rounds with valid routes. Route-quality stagnation is plausible from the poor endpoint, but actual decision journals were unavailable; do not call it confirmed behavioral stalling or refusal.

Interpretation: All routes are valid. The algorithm obtains 100% shortest paths versus 6.5% for model arms; model damage excess is 11.97 hops. Recovery in 4 versus 18 rounds is confounded because long baseline detours avoided more damage. One map and 80 rounds do not establish general adaptation.

### 183. regrowth-200 / pilot-v4-qwen-damage

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Reported pilot completes 80 rounds with valid routes. Route-quality stagnation is plausible from the poor endpoint, but actual decision journals were unavailable; do not call it confirmed behavioral stalling or refusal.

Interpretation: All routes are valid. The algorithm obtains 100% shortest paths versus 6.5% for model arms; model damage excess is 11.97 hops. Recovery in 4 versus 18 rounds is confounded because long baseline detours avoided more damage. One map and 80 rounds do not establish general adaptation.

### 184. regrowth-200 / plan-registration-failure-v1

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No model actor.

Interpretation: Six pilot worlds lacked a public plan URL before execution. Retrospective publication fixes accessibility but cannot restore prospective registration.

### 185. regrowth-200 / prior-stopped-attempts-aggregate

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No direct behavioral trace coverage; do not infer absence of stalling or refusal.

Interpretation: Four previous stopped attempts are author-reported as locally retained; their individual IDs and journals were not recovered. Do not classify their causes as refusal or invent per-attempt counts.

### 186. right-dissenter / Q0-A1

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

All 18 response endpoints are also valid and correct. The648 cell labels are nested in18 responses and six roots, not648 independent tasks.

Behavior: Six positive build/alarm observations yield DEFER. These are one-shot task abstentions, not explicit provider refusals or repeated-action stalls. All nine HOLD answers are correct; three bridge PROCEED answers are correct.

Coverage updated from the bounded publication supplement; earlier frozen evidence remains preserved.

Interpretation: A new genuinely model-executed family with a failed ordinary-task qualification. Complete/schema-valid execution does not qualify the policy comparison. The report candidly identifies plausible task ambiguity rather than treating DEFER as provider refusal.

### 187. right-dissenter / native-Q0

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No model execution in this attempt; setup or research gates prevented dispatch.

Interpretation: No native scientific result observed at the cutoff. Software fixtures do not establish model behavior.

### 188. soc07-private-judgments / S1L

A proposed request would return a final response and be evaluated. No request has been executed; zero started/completed is separate from planned count.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

### 189. soc07-private-judgments / S1Q

A proposed request would return a final response and be evaluated. No request has been executed; zero started/completed is separate from planned count.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

### 190. soc07-private-judgments / S1R

A proposed request would return a final response and be evaluated. No request has been executed; zero started/completed is separate from planned count.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

### 191. soc07-private-judgments / ae76d67b

No uniform experimental endpoint count established for this preparation/diagnostic record; do not substitute check counts or model-call counts for episodes.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.', 'Removed former aggregate planned=1509: it mixed team episodes, replay episodes, single-solver episodes and fault runs. None may be treated as 1509 homogeneous model tasks. Fleet S0 terminal results are unknown at cutoff.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Independent unit: 60fixture worlds;9fault-injectionruns3worlds

### 192. soc07-private-judgments / local-s0-001

No uniform experimental endpoint count established for this preparation/diagnostic record; do not substitute check counts or model-call counts for episodes.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

### 193. swarm-of-theseus / S0-a1

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No model execution in this attempt; setup or research gates prevented dispatch.

Interpretation: HTTP setup failure before model dispatch; no model result.

### 194. swarm-of-theseus / S0-a2

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No explicit refusal phrase found in 1,693 parsed responses. Four unmatched S0-a2 requests remain unclassified. Completed but wrong notebooks are semantic failures, not evidence of refusal.

Interpretation: Four generic PolicyError rows preserve failed episodes but omit the error reason. These cannot be classified as provider refusals.

### 195. swarm-of-theseus / S0-a3

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No explicit refusal phrase found in 1,693 parsed responses. Four unmatched S0-a2 requests remain unclassified. Completed but wrong notebooks are semantic failures, not evidence of refusal.

Interpretation: Twelve episodes complete, but the observatory verbatim ceiling is 0.75, below the 0.85 gate. Completion does not validate a continuity test.

### 196. swarm-of-theseus / S0-a4

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No explicit refusal phrase found in 1,693 parsed responses. Four unmatched S0-a2 requests remain unclassified. Completed but wrong notebooks are semantic failures, not evidence of refusal.

Interpretation: Twelve episodes complete with verbatim accuracy 1.0 on fresh seeds 106/107. This is successful repaired qualification, not an independent replication of the unchanged protocol.

### 197. swarm-of-theseus / S1-a1

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No explicit refusal phrase found in 1,693 parsed responses. Four unmatched S0-a2 requests remain unclassified. Completed but wrong notebooks are semantic failures, not evidence of refusal.

Interpretation: Six paired worlds: notes and both late accuracy 1.0, neither 0.5208, mentor 0.9167, founders 0.8958, verbatim 1.0. Positive information transmission and no measured mentor increment. Supplied rules and unequal information budgets prevent claims of spontaneous culture or swarm superiority.

### 198. swarm-of-theseus-v2 / S0

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Every call ended with end_turn and a valid six-decision answer. No explicit refusal is recorded. Wrong HOLD/none classifications occur, but these are two-checkpoint batch decisions rather than demonstrated prolonged action loops.

Coverage updated from the bounded publication supplement; earlier frozen evidence remains preserved.

Interpretation: The original failed qualification conclusion is confirmed by complete archived decisions and independent scoring. Initial-versus-repair changes are not a causal formatting estimate because fresh worlds and multiple interface changes differ. No turnover/culture-preservation effect is measured.

### 199. swarm-of-theseus-v2 / S0-plan-at-frozencommit

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: No model execution in this attempt; setup or research gates prevented dispatch.

Interpretation: Frozen source says blocked; later hub records show execution. Preserve this historical plan state separately and do not present it as the current run status.

### 200. swarm-of-theseus-v2 / S0-repair

Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.

Terminal, valid, completed and errored may overlap; these are not a partition. Incomplete means started without terminal disposition; unstarted is separate. Completed means protocol endpoint, not scientific success. Do not pool calls, policy rows, paired worlds or replayed prefixes.

Behavior: Every call ended with end_turn and a valid six-decision answer. No explicit refusal is recorded. Wrong HOLD/none classifications occur, but these are two-checkpoint batch decisions rather than demonstrated prolonged action loops.

Coverage updated from the bounded publication supplement; earlier frozen evidence remains preserved.

Interpretation: The original failed qualification conclusion is confirmed by complete archived decisions and independent scoring. Initial-versus-repair changes are not a causal formatting estimate because fresh worlds and multiple interface changes differ. No turnover/culture-preservation effect is measured.

### 201. sybil-budget-api / 46ebda03

One assigned policy/packet observation obtains its scripted or model synthesis and recorded evaluation. Six fact fields, graph identities, source copies, time snapshots, and model calls are not additional primary observations. Wrong or null fields do not by themselves make execution incomplete.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Primary counts remain the initial snapshot; later documentary update is retained separately and is not another cohort.

{"family": "sybil-budget-api", "id": "sybil-budget-api/46ebda03", "attempt": "46ebda03", "publication_source": "4d007242b7ae5117d7f497036fa51f2225d7f993", "kind": "model", "model": "claude-haiku-4-5-20251001", "backend": "anthropic", "unit": "packet/arm observation", "count_unit": "packet/arm observation", "counts": {"planned": 2880, "started": null, "terminal": null, "valid": null, "completed": null, "incomplete": null, "refused": null, "errored": null, "missing": null, "task_success": null}, "evidencecoverage": {"level": "publication_postmortem_and_deployment_only", "saved_requests_directly_inspected": false, "saved_responses_directly_inspected": false, "full_provider_wire_request": false, "full_provider_wire_response": false, "limitation": "No new artifact fetch or model call; new record is grounded in the committed publication documents, not independently inspected new raw traces."}, "endpoint_definition": "One assigned packet observation obtains synthesis and recorded evaluation; source publication supplies no newer completed count.", "count_overlap_notes": ["All primary counts use the stated count unit; bundles and physical requests are separately recorded.", "Terminal includes known failures. Incomplete excludes never-started units. Missing means no terminal endpoint record at the publication evidence cutoff.", "Null means unknown or not applicable; earlier snapshot numbers are retained separately and are not presumed current."], "qualification": {"status": "prior_Q0_passed_S1_collecting"}, "stalling_behavior": "The source now confirms the same04:09 launch observed in the earlier04:11 snapshot; no newer completion or failure result is published.", "causes": {"confirmed": [], "plausible": [], "unknown": []}, "sources": [{"path": "researchers/dmarz/notes/sybil-budget-api/DEPLOYMENT.md", "lines": [47, 49], "immutable_link": "https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/dmarz/notes/sybil-budget-api/DEPLOYMENT.md#L47"}], "smallest_diagnostic": null, "falsifier": null, "acceptance": null, "conclusions": ["Documentation catches up with the original hub snapshot; no extra experiment, rerun or final scientific result.", "Per-publication terminal, valid, completed, error and missing counts stay unknown; never replace earlier0/231 with presumed current counts."], "update_type": "source_confirms_previously_observed_launch_no_new_terminal_counts", "original_snapshot_id": "sybil-budget-api/46ebda03", "original_snapshot": {"cutoff_utc": "2026-10-04T04:11:27Z", "terminal": 0, "valid": 0, "completed": 0, "note": "Historical snapshot values, explicitly not asserted to be publication-time counts."}, "source_execution_revision": "e9db4c58a8847d2f54d60a8ff3cc70f81f58263e"}

Independent unit: 24fresh paired worlds x120cells

### 202. sybil-budget-api / 7b177592

One assigned policy/packet observation obtains its scripted or model synthesis and recorded evaluation. Six fact fields, graph identities, source copies, time snapshots, and model calls are not additional primary observations. Wrong or null fields do not by themselves make execution incomplete.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: Correct null on absent fields is successful task-required abstention, not refusal. All assigned outputs valid.

Legitimate task success count: 16

Independent unit: Clean worlds reused across full/missing/badge/size presentations; observations are not independent worlds.

### 203. sybil-budget-api / fleet-s0-001

One assigned policy/packet observation obtains its scripted or model synthesis and recorded evaluation. Six fact fields, graph identities, source copies, time snapshots, and model calls are not additional primary observations. Wrong or null fields do not by themselves make execution incomplete.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Independent unit: Paired worlds with dependent policy/reliability/identity presentations; engineering repeats excluded from model estimates.

### 204. sybil-budget-api / s0-local-001

One assigned policy/packet observation obtains its scripted or model synthesis and recorded evaluation. Six fact fields, graph identities, source copies, time snapshots, and model calls are not additional primary observations. Wrong or null fields do not by themselves make execution incomplete.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Independent unit: Paired worlds with dependent policy/reliability/identity presentations; engineering repeats excluded from model estimates.

### 205. sybil-budget-api / s0-local-002

One assigned policy/packet observation obtains its scripted or model synthesis and recorded evaluation. Six fact fields, graph identities, source copies, time snapshots, and model calls are not additional primary observations. Wrong or null fields do not by themselves make execution incomplete.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Independent unit: Paired worlds with dependent policy/reliability/identity presentations; engineering repeats excluded from model estimates.

### 206. sybil-newcomer-api / 8def40e4

One assigned policy/packet observation obtains its scripted or model synthesis and recorded evaluation. Six fact fields, graph identities, source copies, time snapshots, and model calls are not additional primary observations. Wrong or null fields do not by themselves make execution incomplete.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Primary counts remain the initial snapshot; later documentary update is retained separately and is not another cohort.

{"family": "sybil-newcomer-api", "id": "sybil-newcomer-api/8def40e4", "attempt": "8def40e4", "publication_source": "4d007242b7ae5117d7f497036fa51f2225d7f993", "kind": "model", "model": "claude-haiku-4-5-20251001", "backend": "anthropic", "unit": "packet/arm observation", "count_unit": "packet/arm observation", "counts": {"planned": 1944, "started": null, "terminal": null, "valid": null, "completed": null, "incomplete": null, "refused": null, "errored": null, "missing": null, "task_success": null}, "evidencecoverage": {"level": "publication_postmortem_and_deployment_only", "saved_requests_directly_inspected": false, "saved_responses_directly_inspected": false, "full_provider_wire_request": false, "full_provider_wire_response": false, "limitation": "No new artifact fetch or model call; new record is grounded in the committed publication documents, not independently inspected new raw traces."}, "endpoint_definition": "One assigned packet observation obtains synthesis and recorded evaluation; source publication supplies no newer completed count.", "count_overlap_notes": ["All primary counts use the stated count unit; bundles and physical requests are separately recorded.", "Terminal includes known failures. Incomplete excludes never-started units. Missing means no terminal endpoint record at the publication evidence cutoff.", "Null means unknown or not applicable; earlier snapshot numbers are retained separately and are not presumed current."], "qualification": {"status": "prior_Q0_passed_S1_collecting"}, "stalling_behavior": "The source now confirms the same04:09 launch observed in the earlier04:11 snapshot; no newer completion or failure result is published.", "causes": {"confirmed": [], "plausible": [], "unknown": []}, "sources": [{"path": "researchers/dmarz/notes/sybil-newcomer-api/DEPLOYMENT.md", "lines": [50, 52], "immutable_link": "https://github.com/dmarzzz/swarm-lab/blob/4d007242b7ae5117d7f497036fa51f2225d7f993/researchers/dmarz/notes/sybil-newcomer-api/DEPLOYMENT.md#L50"}], "smallest_diagnostic": null, "falsifier": null, "acceptance": null, "conclusions": ["Documentation catches up with the original hub snapshot; no extra experiment, rerun or final scientific result.", "Per-publication terminal, valid, completed, error and missing counts stay unknown; never replace earlier0/231 with presumed current counts."], "update_type": "source_confirms_previously_observed_launch_no_new_terminal_counts", "original_snapshot_id": "sybil-newcomer-api/8def40e4", "original_snapshot": {"cutoff_utc": "2026-10-04T04:11:27Z", "terminal": 231, "valid": 231, "completed": 231, "note": "Historical snapshot values, explicitly not asserted to be publication-time counts."}, "source_execution_revision": "e9db4c58a8847d2f54d60a8ff3cc70f81f58263e"}

Independent unit: 24fresh paired worlds x identities/policies/strategies/three rounds; repeated observations

### 207. sybil-newcomer-api / f7b78b41

One assigned policy/packet observation obtains its scripted or model synthesis and recorded evaluation. Six fact fields, graph identities, source copies, time snapshots, and model calls are not additional primary observations. Wrong or null fields do not by themselves make execution incomplete.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: Correct null on absent fields is successful task-required abstention, not refusal. All assigned outputs valid.

Legitimate task success count: 36

Independent unit: Clean worlds reused across full/missing/badge/size presentations; observations are not independent worlds.

### 208. sybil-newcomer-api / fleet-s0-001

One assigned policy/packet observation obtains its scripted or model synthesis and recorded evaluation. Six fact fields, graph identities, source copies, time snapshots, and model calls are not additional primary observations. Wrong or null fields do not by themselves make execution incomplete.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Independent unit: Paired worlds with dependent policy/reliability/identity presentations; engineering repeats excluded from model estimates.

### 209. sybil-newcomer-api / s0-local-001

One assigned policy/packet observation obtains its scripted or model synthesis and recorded evaluation. Six fact fields, graph identities, source copies, time snapshots, and model calls are not additional primary observations. Wrong or null fields do not by themselves make execution incomplete.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Independent unit: Paired worlds with dependent policy/reliability/identity presentations; engineering repeats excluded from model estimates.

### 210. sybil-newcomer-api / s0-local-002

One assigned policy/packet observation obtains its scripted or model synthesis and recorded evaluation. Six fact fields, graph identities, source copies, time snapshots, and model calls are not additional primary observations. Wrong or null fields do not by themselves make execution incomplete.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Independent unit: Paired worlds with dependent policy/reliability/identity presentations; engineering repeats excluded from model estimates.

### 211. sybil-newcomer-api / s0-local-003

One assigned policy/packet observation obtains its scripted or model synthesis and recorded evaluation. Six fact fields, graph identities, source copies, time snapshots, and model calls are not additional primary observations. Wrong or null fields do not by themselves make execution incomplete.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Independent unit: Paired worlds with dependent policy/reliability/identity presentations; engineering repeats excluded from model estimates.

### 212. sybil-scale-api / fleet-s0-001

One assigned policy/packet observation obtains its scripted or model synthesis and recorded evaluation. Six fact fields, graph identities, source copies, time snapshots, and model calls are not additional primary observations. Wrong or null fields do not by themselves make execution incomplete.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Independent unit: Paired worlds with dependent policy/reliability/identity presentations; engineering repeats excluded from model estimates.

### 213. sybil-scale-api / local-s0-001

One assigned policy/packet observation obtains its scripted or model synthesis and recorded evaluation. Six fact fields, graph identities, source copies, time snapshots, and model calls are not additional primary observations. Wrong or null fields do not by themselves make execution incomplete.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Independent unit: Paired worlds with dependent policy/reliability/identity presentations; engineering repeats excluded from model estimates.

### 214. sybil-scale-api / q0-001

One assigned policy/packet observation obtains its scripted or model synthesis and recorded evaluation. Six fact fields, graph identities, source copies, time snapshots, and model calls are not additional primary observations. Wrong or null fields do not by themselves make execution incomplete.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: Correct null on absent fields is successful task-required abstention, not refusal. All assigned outputs valid.

Legitimate task success count: 64

Independent unit: Clean worlds reused across full/missing/badge/size presentations; observations are not independent worlds.

### 215. sybil-scale-api / s1-001

One assigned policy/packet observation obtains its scripted or model synthesis and recorded evaluation. Six fact fields, graph identities, source copies, time snapshots, and model calls are not additional primary observations. Wrong or null fields do not by themselves make execution incomplete.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Legitimate task success count: 594

Independent unit: 24 paired worlds x100dependent cells; simulated populations36/108/324/972, one actual final synthesis request per observation

### 216. sybil-specialists / fleet-s0-001

One assigned policy/packet observation obtains its scripted or model synthesis and recorded evaluation. Six fact fields, graph identities, source copies, time snapshots, and model calls are not additional primary observations. Wrong or null fields do not by themselves make execution incomplete.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Independent unit: Paired worlds with dependent policy/reliability/identity presentations; engineering repeats excluded from model estimates.

### 217. sybil-specialists / fleet-s1-001

One assigned policy/packet observation obtains its scripted or model synthesis and recorded evaluation. Six fact fields, graph identities, source copies, time snapshots, and model calls are not additional primary observations. Wrong or null fields do not by themselves make execution incomplete.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Independent unit: Paired worlds with dependent policy/reliability/identity presentations; engineering repeats excluded from model estimates.

### 218. sybil-specialists / local-s0-001

One assigned policy/packet observation obtains its scripted or model synthesis and recorded evaluation. Six fact fields, graph identities, source copies, time snapshots, and model calls are not additional primary observations. Wrong or null fields do not by themselves make execution incomplete.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Independent unit: Paired worlds with dependent policy/reliability/identity presentations; engineering repeats excluded from model estimates.

### 219. sybil-specialists / worker-stop-diagnostic

No uniform experimental endpoint count established for this preparation/diagnostic record; do not substitute check counts or model-call counts for episodes.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Independent unit: No new scientific worlds; one deliberately injected worker failure.

### 220. sybil-specialists-api / 08338820

One assigned policy/packet observation obtains its scripted or model synthesis and recorded evaluation. Six fact fields, graph identities, source copies, time snapshots, and model calls are not additional primary observations. Wrong or null fields do not by themselves make execution incomplete.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: Correct null on absent fields is successful task-required abstention, not refusal. All assigned outputs valid.

Legitimate task success count: 24

Independent unit: Clean worlds reused across full/missing/badge/size presentations; observations are not independent worlds.

### 221. sybil-specialists-api / bac7d9ae

One assigned policy/packet observation obtains its scripted or model synthesis and recorded evaluation. Six fact fields, graph identities, source copies, time snapshots, and model calls are not additional primary observations. Wrong or null fields do not by themselves make execution incomplete.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Independent unit: 12paired worlds x16dependent cells; scripted graph/reports/checks with one model synthesizer

### 222. sybil-specialists-api / fleet-s0-001

One assigned policy/packet observation obtains its scripted or model synthesis and recorded evaluation. Six fact fields, graph identities, source copies, time snapshots, and model calls are not additional primary observations. Wrong or null fields do not by themselves make execution incomplete.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Independent unit: Paired worlds with dependent policy/reliability/identity presentations; engineering repeats excluded from model estimates.

### 223. sybil-specialists-api / local-s0-001

One assigned policy/packet observation obtains its scripted or model synthesis and recorded evaluation. Six fact fields, graph identities, source copies, time snapshots, and model calls are not additional primary observations. Wrong or null fields do not by themselves make execution incomplete.

['All numeric counts in counts use this row’s count_unit; physical model calls and hub bundles are separate metadata.', 'Terminal includes recorded failures. An incorrect or adversarially wrong but structurally valid answer remains valid and completed when the protocol finishes.', 'Incomplete excludes units that never started. Missing denotes no terminal record at the frozen cutoff; cancelled-before-start units remain missing scientific observations.', 'Task success is not inferred from execution completion, qualification status or adverse treatment outcomes.']

Behavior: No duration-based stall measure was reported; abstention, invalid output and nonterminal output are distinguished.

Independent unit: Paired worlds with dependent policy/reliability/identity presentations; engineering repeats excluded from model estimates.

