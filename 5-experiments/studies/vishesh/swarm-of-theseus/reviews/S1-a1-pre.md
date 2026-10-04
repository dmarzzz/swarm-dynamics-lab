# Pre-run assessment: S1-a1

- Experiment / owner / stage: swarm-of-theseus / vishesh/codex-theseus / exploratory S1.
- Parent and previous post-mortem: S0-a4, read S0-a4-post.md; earlier qualification failures retained.
- Status: ready, conditional on fail-closed public/claim/source/budget checks.
- Question: can seeded useful procedure survive replacement through notes, mentoring, both, or neither?
- Expected: both exceeds neither after all founders leave; plausible null is equal scores, or arbitrary convention persistence without usefulness. A failed verbatim control or missing outcomes weakens inference and must be reported.

## Design and assessment

Same scenarios, generator, model, prompts, evaluator, population and channel caps as qualified source 586c476892c442c29fc290358ce21a75cbcc07fe. Study/provider/model hashes must match its manifest. The prior 12/12 outcomes and 72 frames passed independent audit; verbatim controls 1.0 accuracy/convention in every scenario. Eleven local regression tests pass, including case-ID ordering and duplicate rejection. No S1 cases have been opened.

36 world-arm outcomes: three scenarios × seeds 200/201 × six arms. Six paired worlds are the units, not 108 agents, 216 frames or 864 actor calls. Counterbalanced labels/conventions; arm order seeded at 244. All six arms receive the same call/output ceilings; actual tokens and inherited information differ and will be reported. Inherited procedure is intended information; future cases/labels remain inaccessible during onboarding. New case IDs do not establish novel feature combinations.

Primary: paired within-world both-minus-neither collective accuracy, steps 4–5, averaged equally across scenarios; useful threshold 0.10 points, descriptive. 2,000 stratified world bootstrap draws; six worlds yield weak precision and no confirmatory p-value. Report all six arms, scenario effects, convention separately, behavioral mutation, turnover and actual use. Missing final outcomes score zero in conservative analysis, with complete-case sensitivity and denominators. Observatory repeated-root adversarial cases distinguish proper evidence use from vote counting. Repair bulletin reaches every arm at steps 4 and 5; this tests following an update, not discovery.

## Changes and unresolved issues

| Issue | Change / decision | Acceptance | Owner |
|---|---|---|---|
| Earlier model/schema failures | frozen v3 source-ID work schema | exact-source S0 passed | codex-theseus |
| Tiny scenario coverage | retain as exploratory, no enlarged claim | per-scenario denominators and raw paired effects | codex-theseus |
| Source drift after qualification | compare study/provider/model hashes and audit | runner rejects mismatch | codex-theseus |
| Earlier plans could follow latest registration | per-run original URL report | immutable link retained | codex-theseus |

## Frozen execution plan

Commit this review and summary-figure/complete-case reporting before execution. Manifest freezes hashes and assignments. Native model claude-haiku-4-5-20251001, temperature 0, max 1,024 output tokens / 8,000 input bytes / 60-second timeout. Three workers, two-hour wall ceiling, at most 864 further calls; shared allocation total USD 15 / 1,728 calls, 833 already used. Dedicated sim-shadow claim vishesh-swarm-theseus, expiry 2026-10-04T05:28:09Z; refresh exclusivity before launch. No additional infrastructure or API cap. Credential alias only: approved Keychain service swarm-lab-anthropic / account vishesh; worker receives it through secure local process and SSH memory.

Command: `python src/runner.py --stage S1 --attempt S1-a1 --out /srv/swarm/theseus-results/S1-a1 --qualification /srv/swarm/theseus-results/S0-a4/summary.json`. New output directory; zero semantic/transport retries. Every scheduled assignment gets a terminal record; failures remain visible. Stop at quota/claim/runtime limits. A valid negative finding ends the cycle; a material defect needs preserved evidence and explicit repair planning, never silent substitution. S2 stays disabled.

## Visualization mapping

Mapping v1 unchanged, bound to `swarm-of-theseus/S1-a1-<scenario>-<arm>-<seed>`. 216 scored frames maximum, latest PNG after every step, 36 final PNGs, full event histories, per-world and aggregate HTML replay. Accuracy /4 cases, convention /3 actors and turnover /3 members in separate panels. Seed/world/arm filters and case-ID lineage prevent mixing trajectories. Steps 1–3 mark replacements, repair-only step 4 marks the update. Missing states use grey gaps; no imputation in plots. Final aggregate figure shows arm/scenario means and exploratory contrast interval; all task weights equal. Public hub images plus downloadable replay fallback; no claim of native custom embedding. Audit every recorded frame against raw events, verify initial/turnover/final states and actual replay controls. Rendering defects are reporting defects, separate from scientific outcomes.
