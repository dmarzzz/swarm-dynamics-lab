# S0/S1 pre-run assessment

Written before evaluation outcome inspection. E0 calibration has real routing headroom: fixed B 0.6023 versus oracle 0.6683, gap 0.0660; first 20 only. The full E0 instrument must finish with zero OCR failures before S0. Calibration headroom is a reason to run, not evidence for a swarm.

## Plan and hypotheses under test

Use the frozen README/SPEC and policy implementation. Exploratory hunch: limited reference checks can improve configuration selection; a five-role adaptive committee may preserve useful quality while saving checks relative to a fixed committee. The primary challenge is beating best-fixed and decision-focused, not just saving against mandatory checking. Same-checkpoint agreement is not independent evidence. Source provenance and limitations are in SOURCES.md. Survey gates remain in force; no S2 launch.

S0: four explicit option-following probes and ten instrument receipts20–29, all seven arms. S1:70 receipt-paired blocks30–99. S0 must have ten complete blocks, no encoding/schema/tool faults, exact budgets and renderable PNG/GIF artifacts. Probe misses are disclosed semantic limitations, not suppressed. If all four probes fail, stop for adapter diagnosis. Do not tune policies using S0 success/failure scores; instrumentation repairs must be versioned and requalified. S1 uses identical frozen policy code.

Budget: exclusive sim-test-01 claim vishesh-antsy-verification-v4 through 2026-10-04T03:58:07Z; verify merged/exclusive before launch and extend if needed. CPU 2, one worker, no paid APIs. Maximum124 physical model calls in S0 and 840 in S1; enforce per-process1100 cap and 30-minute wall timeout. Dataset OCR measurement is a separate300-call E0. Exact model revisions in SPEC, package versions recorded at runtime. No competing processes are stopped.

## Measurement assessment

Independent units are receipts. The external corpus removes engineered policy winners but narrows scope to Indonesian retail images and a reference-derived score. QA is ideal, regional and purchased. The confidence correction is learned only from 20 calibration items. Report whole-receipt recall, per-receipt regret, checks, total-price token exactness, physical/logical calls and actual model latency. Use receipt-paired bootstrap95% intervals with seed 2026,2000 draws for differences; exploratory descriptive intervals, no multiple-testing or population-superiority claims. Report utility over check costs0,.01,.02,.05 alongside raw quality/cost.

Bad decisions are evaluated counterfactually: choice regret>2 pp; QA helps/hurts compared with confidence-only; adaptive stopping loses quality/saves checks compared with the same fixed tape. Do not rewrite poor outcomes as infrastructure faults. Invalid runs remain archived and block escalation.

## Visualization mapping v1

Bindings: antsy-verification-v4/S0-attempt-1 and /S1-attempt-1; seed 71; all arms. Observation time is QA step0,1,2, not model wall time. Preserve every board, vote vector, paid response and final decision. Overview bars encode mean measured quality; adjacent values report regret and checks. Oracle-headroom plot pairs fixed actual recall with best measured recall per receipt.

Replay first three assigned receipts of each stage, for single-agent and swarm-adaptive (six GIFs), regardless of outcome. Confidence/estimated-quality bars precede commitment; actual-score values appear only after commitment. Text shows votes, purchased mode/region, remaining credits and final regret. There are no simulated coordinates or movement. Renderer uses1600x960 PNG/GIF, checked by decoding actual frames before launch. Static E0 has no meaningful temporal actor behavior; show a calibration progress/summary view instead. The main run reports receipt progress live; replays upload after durable results. This fallback is honest about not streaming model internals.

## Acceptance / stop rules

Ten offline scorer/policy tests, plus actual render/decode check; lab validator and secret scan before push. Require complete E0 and relevance gate. S0 errors trigger a recorded repair, not an S1 launch. All-four-probe failure triggers semantic adapter diagnosis. S1 completion means70 blocks and 490 arm outcomes, budgets respected, no lost call receipts, visible artifacts and a post-mortem. Zero execution errors does not mean scientifically successful. Preserve negative/no-benefit results. Review publication independently of computation; a rendering/upload failure must resume from durable outcomes, not rerun decisions.
