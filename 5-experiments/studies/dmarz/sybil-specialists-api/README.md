# Sybil resistance: model synthesis and verification badges

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by vishesh/codex-pi-review; source `9781739c` ([registry](../../../evidence-metadata.json), [rubric](../../../EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **2/4** — The completed controlled comparison describes verifier/admission effects on synthesis within one constructed graph family. Basis: Qualified, complete 12-world pilot supports the bounded strong-check/weak-check tradeoff; a single model, graph family and fixed fabrication do not generalize. The badge interval spans harm and benefit, so badge efficacy remains unresolved.
- **sample_size_summary:** 12 paired worlds × 16 conditions = 192 valid S1 answers; 24 Q0 packets; 36 simulated identities and 1 model synthesizer.
<!-- experiment-evidence:end -->

Exploratory SEC-19 / SEC-43 follow-up. The previous scripted study found that coverage verification recovered useful specialists while also admitting more attackers. This study tests whether that tradeoff persists when an LLM combines reports, and whether showing imperfect verification badges changes the model's answers.

## Question

Can graph admission preserve useful specialist knowledge for a model without letting many identities owned by one attacker dominate its answers? Do passed verification badges become misleading authority when an attacker can pass the check?

## Setup

The 36-identity synthetic environment, four admission policies and evaluator are inherited unchanged from [sybil-specialists](../sybil-specialists). Core skills 0–2; specialist skills 3–5. The actor sees 18 admitted reports, shuffled independently of truth. Badges are visible or removed, with all other evidence matched. Only downstream synthesis is model-backed; reporters, verification and admission remain scripted. No API-based identity proof or autonomous swarm is claimed.

Pinned Claude Haiku 4.5, a six-field structured answer, temperature zero. Existing encrypted credential alias `SWARM_MODEL_API_KEY`; no secrets enter this public repository. [Provider model and prices](https://platform.claude.com/docs/en/models/haiku-4-5/overview) and [structured output contract](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) checked 2026-10-04 UTC.

## Protocol

[design.yaml](design.yaml) and [frozen protocol](preregistration.md) define all assignments. S0 replays all 216 inputs with a scripted solver. Q0 makes 24 fresh clean competence calls, including missing-evidence abstention. Once Q0 passes, S1 makes 192 calls on 12 paired attack worlds, crossing four admission policies, two verifier reliabilities and two badge treatments. The primary development contrast is coverage minus degree at attacker pass .10 with visible badges. The badge contrast at pass .90 is secondary. Full matrix and scripted reference are always retained.

One worker. No automatic API retries. A persistent, nonrefundable reservation ledger enforces a $5 aggregate cap across qualification, pilot and any repairs, with 300 attempted calls maximum. Run source, prompt, config, assignment list, usage and failures are recorded. API calls use only synthetic data. S2 remains blocked by formal research gates.

## Metrics

Rare-skill and all-skill accuracy; missing-evidence abstention; whole-packet correctness on clean controls; malicious admission and specialist rejection; model minus scripted accuracy; valid/invalid/not-started denominators; actual token charges and conservative reserved spend. Confidence intervals resample worlds, not calls. Small exploratory results cannot establish a deployable Sybil defense.

## Visualization

The [mapping](VISUALIZATION.md) defines live measured progress, a final comparison and a GIF replay. Each cell compares all four policies with fixed axes. The cursor counts completed calls, so a model answer is never shown before its response arrives. Missing cells display pending; failed observations are counted explicitly. These views appear on the [live experiment](https://swarm-live.pages.dev/#/x/sybil-specialists-api).

## Results

The model-backed qualification and pilot completed on 2026-10-04 UTC. Q0 passed 24/24 exact packets, including 36/36 missing-evidence abstentions. S1 completed 192/192 valid calls across 12 paired worlds; no missing or repeated observations. Total 216 API calls, 266,342 input tokens and 8,692 output tokens: **USD 0.309802** computed from reported usage, within the USD 5 aggregate cap. No automatic retries. Scripted S0 adds 216 engineering observations with zero API calls.

With informative checks (attackers pass 10%), coverage verification yielded **94.4% rare-skill accuracy**, versus 8.3% for degree, 47.2% for random and 0% with no checks. Coverage-minus-degree is +86.1 percentage points; the 12-world descriptive bootstrap interval is [72.2,97.2]. Coverage admitted 7.4% of attacker identities versus 3.7% for degree: useful recovery still has a security cost.

When attackers pass 90% of checks, coverage admits**80.6% of attacker identities**. Rare-skill accuracy drops to 25.0% with badges hidden and 33.3% with badges shown. The paired badge effect is +8.3 points, with a descriptive interval [-2.8,19.4]; **this pilot does not establish that badges help or harm**. The broad collapse under weak checks persists with a real model synthesizer. The scripted reference is 33.3% in both high-pass coverage cells. Full 16-cell results, paired world differences and denominators are in [results-summary.json](results-summary.json).

Only report synthesis uses an LLM. Graph admission, identity ownership, verifier reliability and fabricated reporter values remain simulated. This is a single model, one symmetric graph family, a fixed attack offset and 12 toy worlds, not evidence of a deployable general Sybil defense. The next scientific extension should vary topology and attack generation and compare faithful published defenses after the formal research gates. No further paid batch is automatically queued.

The generic pilot usage time series originally mixed stage and study totals; saved per-call accounting and all scientific values are unchanged. The separate analysis replay corrects initial carried spend and explains that reporting amendment. Original observations and artifacts remain available. See [reviews](reviews), [deployment record](deployment.json), and the [analysis view](https://swarm-live.pages.dev/#/r/sybil-specialists-api%2Fanalysis-api-001).
