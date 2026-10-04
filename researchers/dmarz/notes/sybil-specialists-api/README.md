# Sybil resistance: model synthesis and verification badges

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

Not run yet. See reviews for stage-specific qualification and post-mortems.
