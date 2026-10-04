# Post-mortem: fleet-s0-001

Experiment sybil-budget-api / owner dmarz / scripted S0 / 2026-10-04. Parent: [committed fleet pre-run assessment](fleet-s0-001-pre.md). Run `sybil-budget-api/4346fc36`, attempt 1. **Disposition: complete valid engineering qualification; advance to Q0.** The owner explicitly waived independent review and authorized the two follow-ups in parallel. This is the operator's own assessment, not an independent research approval. Q0 and S1 are pending; formal S2 remains disabled.

## Execution and reconciliation

The fleet ran committed revision `106d1082db3152af5bcf5e4539bca81adc13d57d` with frozen runtime hash `66ea4fe1465678ff66d099eec14ea11dbf5bc69063c00e3cc57249e06db98f08`, matching the completed local engineering qualification. Host `sim-dmarz-4`, exclusive allocation `dmarz-sybil-followups`.

All 256 assignments were started, terminal, graded and analyzed. There were zero invalid or not-started records and one recorded attempt, with no retries. The 120 scientific engineering cells each contain exactly two valid worlds, accounting for 240 outputs. The remaining 16 outputs are clean fixtures: eight at N=324 and eight at N=972. Each size achieved 100% field correctness, 100% exact packets and 100% required missing-fact abstention. The qualification gate passed. Preparation and collection took 84.47 seconds; rendering was additional.

No model API calls were made: zero input tokens, output tokens and model spend. The verification receipt also showed zero shared-ledger reservations, unsettled commitments or actual spend, with the joint $60 cap intact. The finite budget-study worker was no longer active when verified. The claim is retained for the authorized subsequent stages.

## Visualization and durable evidence

The operator verification receipt confirms ten durable artifacts: assignment, episode and world histories; summary and analysis; initial, progress, final and retention images; and replay. The initial and final images are 1920×1440. All 25 replay frames decoded at the same dimensions. The summary records no reporting errors. Mapping v1 labels this stage SCRIPTED, shows collection-completion order, preserves counts and uses a static final fallback. It does not depict model performance or autonomous identity interaction.

The same frozen renderer's main and retention layouts were already inspected during local qualification, and the retained local assignments, packet hashes, check counts, graph metrics, grades and analysis were independently recomputed there. This fleet receipt verifies the deployed stage's completion, artifact integrity and image decoding. Public browser playback remains a publication check; it is not inferred from successful decoding.

## Quality and next action

The full engineered grid, all clean controls and exact-runtime prerequisite passed without a material defect. Scripted differences between policies are instrument outputs, not evidence of model superiority, and do not justify retuning or selecting cells. The 24 fresh scientific worlds remain uncollected. Holdout 10000–19999 remains untouched.

The Q0 preassessment was committed in the executed revision and is ready now that its S0 prerequisite has passed. Q0 will make 16 bounded clean API calls on separate worlds, with two concurrent requests, no retries, the persistent study ledger and the joint actual-plus-unsettled spending guard. The exact planned Q0 reservation is $1.018967; actual cost is unknown. Only successful exact-runtime Q0 permits S1. The root operator refreshes the claim and shared allowance before launch and records Q0's actual results in its own post-mortem.

There is no open S0 repair item. Next action: **advance to Q0**, while preserving this run and all original artifacts. See [deployment record](../DEPLOYMENT.md).
