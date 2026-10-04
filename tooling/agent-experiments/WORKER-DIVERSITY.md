# What must differ between swarm members?

A different name, persona or random seed is not sufficient. A useful difference changes the information or reasoning path enough to correct failures of another member, while retaining task competence. Whether a difference is useful is task-dependent and must be measured on held-out cases.

## Record before launch

Keep the dimensions separate; do not turn them into an arbitrary universal distance score.

| Dimension | Reproducible record | Main confound |
|---|---|---|
| Model / engine | exact revision, weights hash, provider, numerical settings | capability can change along with diversity |
| Instructions / role | effective prompt hash and tool contract, not a persona label | different wording may produce the same behavior |
| Evidence | source roots, retrieval results, image/input hashes, transformation lineage | multiple copies of one source are not independent evidence |
| Tools / preprocessing | implementation/config hashes, available actions | a shared parser can erase differences or create common errors |
| Context / memory | inherited context, memory and peer-message hashes; reset policy | common anchoring can dominate model differences |
| Sampling | seed when available, temperature, repeat index, ordering | stochastic instability can masquerade as systematic complementarity |

Antsy v7 varies engine family, segmentation and preprocessing while holding pixels, extraction, memory and communication fixed. It cannot establish evidence-source independence or LLM-agent diversity. Its five workers have two engine families, not five independent experts.

## Measure after launch

1. **Competence first.** Per-worker correct, wrong, missing/invalid and cost with the same assigned denominator. A useless contrarian is not a beneficial diverse worker.
2. **Behavior.** Agreement among co-answering pairs, answerability/missingness separately, and denominators. Separate “both found no answer” from “both verified an answer.”
3. **Shared failure.** Both-wrong, exactly-same-wrong, joint non-correct, and correctness correlation. Report undefined correlations as undefined; difficulty confounds raw correlation.
4. **Complementarity.** Directed rescue (A correct when B is wrong or missing), unique-correct contribution, and candidate-oracle headroom. Oracle is an upper bound using labels, never an operational policy.
5. **Decision value.** Paired difference in wrong acceptance, correct completion, referral and measured cost against the strongest singleton and a related-worker team. Extra abstention alone is not an improvement.

Use receipt/task roots as the unit for uncertainty, not worker outputs, messages or policy replays. Stratify by predeclared difficulty proxies and report sparse denominators; do not treat strata as eliminating all confounding. When repeated stochastic calls are introduced, separate within-worker variability from between-worker differences on the same tasks.

## Prevent confident correlated mistakes

Collect private initial judgments before peer discussion. Track evidence lineage and deduplicate repeated computations/sources. Preserve a credible contrary answer as a reason to obtain a genuinely new observation or refer; do not merely add identical voters until a quorum appears. Evaluate this protection against both naive majority and cheap single-worker baselines. Do not let evaluator labels select the “credible” dissenter.

The operational target is conditional complementarity: among cases where the existing team fails, how often does the new member supply a correct usable answer, and what does the policy actually do with it? A later routing rule must be fit on development data, frozen, and evaluated on new cases. It cannot use the held-out rescue matrix to pick workers for those same held-out cases.

## Next LLM study, once admitted

Add exact model/prompt/context manifests, independent initial judgments, repeated identical-input calls, and a matched-call same-model control. Compare same model/same evidence; different model/same evidence; same model/different evidence; and different model/different evidence. Hold budget and available task information fixed where the contrast requires it. Label model-capability effects separately from source-diversity effects. Jev can replace a decision backend when securely configured and prospectively budgeted; it is not part of this OCR run.

Worked implementation: [Antsy v7](../../researchers/vishesh/notes/antsy-diversity-v7/README.md). Qualification and result status are recorded there; this methods document is not evidence of an efficacy result.
