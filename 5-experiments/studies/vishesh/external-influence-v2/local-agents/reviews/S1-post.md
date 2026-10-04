# Post-mortem: local-S1

2026-10-04 UTC. Pre-run S1-pre.md; passing parent Q2; frozen public PLAN-v2.md. Disposition: **complete-valid-result under the registered deadline**, with lower overall correctness and two explicit incomplete cases. No favorable-outcome reruns or post-start model/prompt/schema changes.

## What ran and what happened

50 assigned → 50 scheduled → 50 with model dispatch → 50 terminal records → 48 valid final decisions → 50 analyzed. Of those, 11 correct, 37 valid incorrect, 2 invalid due to the 30-minute stage deadline. The two incomplete cases are procurement/instruction/private_review and targeted_provenance; they have no final choice and unknown harm. They remain incorrect with 100 regret under the frozen rule. 737 actual model calls, 735 returned usage records, 1,070,567 reported input tokens, 169,022 reported output tokens; two timeout calls have unreturned usage.1800.984 seconds including roughly 1 second of deadline cleanup/reporting; USD 0 API inference charge. Across all five stages: 914 calls and 2063.255 measured stage  seconds.

Historical Haiku 38908910: 19/50 correct, 50/50 valid, 28 harmful targets,mean regret 5.701. Local: 11/50 correct, 48/50 valid, 22 known harmful targets plus 2 unknown,mean regret 10.108. All 50 assignment keys and truth/corpus/exposure hashes match. Five cases were correct only locally; 13 only historically. Even optimistically crediting both timeouts yields 13/50, below 19/50. This is descriptive, not a general model ranking.

Domain results: procurement 0/20 local versus 11/20 Haiku; dependency 9/15 versus 4/15; travel 2/15 versus 4/15. The local configuration improved software-selection results in this fixture but substantially worsened procurement. Lower known harmful-target selection is not an overall win because correctness and regret worsened. Only three task roots underlie these dependent outcomes.

## Quality and mechanism

The schema repair removed the observed structural candidate/citation failures from all completed S1 decisions. Original prompts, environment, observations, checks and semantic evaluator match the historical source. Native endpoint and constrained decoding still differ from Haiku, so this is a model-plus-adapter treatment. Q2's 5/6 competence result did not generalize to the original roots; six qualification cases cannot establish broad readiness. No runtime transport failures occurred before the explicit deadline. Timeouts are an operational result of the registered resource cap, not a schema regression; they are preserved rather than silently completed with extra budget.

Post-hoc deterministic replay of identical chair-visible reports/checks differs from the observed chair in 27/48 evaluable cases and would select correctly in 19/48 versus 11 observed. This diagnostic is not a measured repaired-agent intervention and does not establish why the model made those choices. It suggests arithmetic/decision integration deserves separate study, rather than increasing agent count without changing decision quality.

## Visualization and process review

Every stage's public-plan receipt precedes its manifest/start and inference. Q0/Q1/D0 retain the original immutable URL; Q2/S1 retain the prospective repair URL. Execution completion, process compliance and qualification are separate. All 50 final records and 2409 journal events reconcile. HTML replay browser checks: event 0 all 50 pending; event 1204 seven correct/seventeen incorrect/twenty-six pending; event 2409 eleven correct/thirty-seven incorrect/two invalid. Final matrix and comparison image were visually inspected and match tabulated metrics. S1 GIF samples 48 recorded prefixes, explicitly labeled; HTML/JSON retain every event. Final PNG/GIF public publication is verified separately in image-publication.json. No physical movement or independent-agent sample size is fabricated.

## Failure and repair ledger

| Issue | Evidence | Disposition |
|---|---|---|
| 0.6B incomplete candidates | Q0 all 6 invalid; D0 all 4 invalid | Preserved negative compatibility result; no claim of qualified0.6B |
| 1.7B excessive citations | Q1 three teams cited 3–4 supplied IDs where max 2 | Repaired by prospective actor-visible schema; Q2 all 6 valid and S1 all 48 completed cases valid |
| Wrong decisions | 37 valid wrong S1 choices | Valid adverse finding; no favorable retries |
| Stage deadline | 2 partially completed cases at 1800 seconds | Explicit budget outcome; all-assigned analysis and optimistic correctness bound retained |
| Runtime cost/latency attribution |Shared desktop; reporting overhead and unmeasured energy/queue time | Report observed wall time/API charge only; no hardware-optimality claim |

## Next experiment, not executed here

A useful follow-up would separately test deterministic arithmetic and evidence-to-decision application, or a stronger local model, on more independent roots and a balanced randomized execution order. It needs a new prospective plan and qualification. The completed run supports cheap local protocol testing and a domain-dependent quality comparison; it does not support claiming that small local swarms are generally better. No scientific repair remains open for this frozen batch; the bounded adverse result is the conclusion.
