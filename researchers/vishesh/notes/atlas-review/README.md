# Research question review and project connections

Reviewer: **vishesh/codex-methods**, 2026-10-03. This contribution reviews all **214 atlas candidates** (the original 143 plus 71 additions), adds **40 reviewer-authored questions, refinements and cross-connections**, and maps them to **all 16 original project briefs**. It incorporates the experimental-design hunch bundle published in `45b363a` and the newly published simulation-environment survey. These are research-context notes, not registered hypotheses, a completed survey, or approval to run experiments.

The strongest immediate opportunity is a small evidence-and-memory testbed that distinguishes independent observations from repeated claims, useful dissent from extra computation, and correction from apparent recovery. Several projects can share that infrastructure. The broad bank preserves other directions without pretending they are equally ready or novel.

The final reconciliation uses atlas Update 2 from main `25a7575`. It rechecks 36 revised original cards, comments on all 71 additions, and marks four substantially overlapping extensions as refinements of existing cards. The forty entries are not forty independently novel projects. The [canonical dashboard](https://swarm-research.pages.dev/#/questions) now hosts the 214-question bank.

## Read the contribution

| Artifact | Purpose |
| --- | --- |
| [Candidate review](candidate-review.md) | Individual judgments and actionable controls for all 214 existing questions |
| [Extension bank](extension-bank.md) | Forty reviewed cross-connections with comparisons, confounds, feasibility and decision value |
| [Sixteen project crosswalk](project-crosswalk.md) | Every original brief linked to existing candidates and new extensions |
| [Research area context](area-context.md) | All 15 current atlas areas, including agent budgets |
| [Experimental design review](design-review.md) | Concrete findings in the new bundle and boundaries between fork/merge setups |
| [UI review](ui-review.md) | Browser observations separated from scientific findings |
| [Source checks](source-checks.md) | Fresh primary-source access, inherited metadata and unresolved checks |
| [Atlas review JSON](atlas-review.json) | Importable reviewer comments in Dan's existing review interface |
| [Extensions JSON](extensions.json) and [crosswalk JSON](project-crosswalk.json) | Structured context for downstream tooling |

## Prioritized next comparisons

This is the reviewer's design/prior-art shortlist, not a team selection or a claim of statistical significance. Ordering favors diagnostic value, shared infrastructure and a small first test. Model access, annotation and runtime costs have not been measured for these proposed comparisons.

| Priority | Comparison | Why do it next | What would change the decision |
| --- | --- | --- | --- |
| 1 | [VX-03](extension-bank.md#vx-03), reachable correct commits | The current Scheme C rejects unanimous evidence for every finite positive evidence count and coefficient. This can be checked without inference calls. | Fix the specification before implementation or reject the confidence-ceiling design. |
| 2 | [VX-01](extension-bank.md#vx-01) and [VX-02](extension-bank.md#vx-02), roots and provenance errors | Quorum, diversity and external influence all depend on what counts as independent evidence. | Prefer a simpler rule if gains vanish under observable, imperfect provenance. |
| 3 | [VX-04](extension-bank.md#vx-04), dissent versus new evidence | Separates a role effect from buying another useful observation. | Remove the critic role if a neutral evidence delivery achieves the same frontier. |
| 4 | [VX-06](extension-bank.md#vx-06) and [VX-07](extension-bank.md#vx-07), correction and genuine loss | Memory and regrowth need stronger baselines than plausible reconstructed text. | Use ordinary backups if selective repair or reacquisition adds no retained-function benefit. |
| 5 | [VX-12](extension-bank.md#vx-12), faithful retelling of a false source | Telephone can become useful general tooling without promising truth detection. | Keep lineage tooling if it improves error localization and investigator decisions at matched effort. |
| 6 | [VX-25](extension-bank.md#vx-25), stale expertise directories | A specific routing extension beyond another topology leaderboard. | Prefer broadcast or periodic refresh if learned routing loses its advantage under directory drift. |
| 7 | [VX-30](extension-bank.md#vx-30), selective loss of verifier logs | Makes casefile and discovery claims auditable. | Restrict reported comparisons if missingness can reverse policy rankings. |
| 8 | [VX-18](extension-bank.md#vx-18) and [VX-19](extension-bank.md#vx-19), NCA function and schedule | A separate, checkpoint-dependent observatory track with explicit existing prior work. | Stop at a replication if the proposed lesion/schedule tests already exist or no compatible checkpoint is available. |

The eight original atlas candidates marked **Shortlist** are SOC-01, SOC-04, SOC-08, SOC-09, SOC-23, SOC-31, SEC-03 and SEC-06. Methodology candidates MTH-01 through MTH-06 and simulator checks are controls for those choices, not six more projects to implement immediately.

## Minimal shared infrastructure

Reuse [the agent experiment toolkit](../../../../tooling/agent-experiments/README.md) for protocol discipline and artifact conventions. Its existing deterministic examples are not evidence that a full provider/retrieval environment already exists. Consult [the simulation survey](../../../../surveys/sim-environments.md) before choosing an engine; teammates' smoke runs are not reproduced by this review.

The first fixture should expose task truth only to the evaluator, immutable upstream observation IDs, observable versus oracle provenance, versioned claims, source access, an event schedule, and total resource accounting. Preserve initial private answers, delivered evidence, final actions, timeouts and false interventions. A central evidence-union solver, independent solvers, simple voting, fixed rounds and reset/checkpoint recovery cover much of the baseline surface. Add components only for a selected question.

Before promotion, choose one discriminating comparison, finish the question-specific prior-art survey, satisfy the repository's gate, and obtain the required independent review. A large bank of plausible ideas is not evidence of novelty. Reserve a separate confirmation set before trying many configurations.

## Review import and scope

Open [Dan's review UI](../../../dmarz/notes/question-atlas/review.html), set the reviewer name to `vishesh/codex-methods`, and import `atlas-review.json`. The interface stores review choices in that browser; it does not publish changes to the team. Import merges by candidate ID and replaces overlapping local choices, so export any existing review first. This file uses atlas hash `221d012538054f1770caadee9b63c7681504ec970cb390328e0ad52b345e4fe1`.

The review covers the cards, their design/falsifier fields, original briefs, selected research context and design-critical sections of the new bundle. It is **not** a fresh audit of every catalogue entry or every numbered citation in that bundle. No model experiment, paid evaluation or live external influence attempt was launched. The primary-source ledger states the reading depth of this session rather than inheriting somebody else's `full` label.
