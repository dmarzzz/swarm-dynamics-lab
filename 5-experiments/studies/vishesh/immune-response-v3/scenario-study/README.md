# Immune Response

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by vishesh/codex-pi-review; source `9781739c` ([registry](../../../../evidence-metadata.json), [rubric](../../../../EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **1/4** — The small scenario diagnostics exposed failed team recovery and healthy-service damage by the solo baseline; they do not identify a causal team-versus-solo advantage. Basis: Healthy control failed in A1; A2 often failed repair; solo repaired incidents but damaged healthy control. All are valid adverse decisions, not provider failures. Sequential architecture runs are not a randomized causal team-versus-solo estimate.
- **sample_size_summary:** Native:4 related scenarios; team A1/A2 each12/12 episodes (3 arms), solo4/4;240 calls. A2 engineering192 episodes includes16 name variants, not192 independent situations.
<!-- experiment-evidence:end -->

## TLDR

The service is down. Yesterday's recovery note says to roll back everything. Today a data migration may have made that advice unsafe. Three agent reviewers and an incident commander must recover a small deployment using live compatibility checks, a version catalog and imperfect handoff memory. We compare retaining that memory, clearing it once, and filtering it against an observed control revision. The question is whether memory repair improves decisions beyond what ordinary tool-assisted diagnosis already achieves.

This is an exploratory executable incident exercise, not a production deployment, accepted hypothesis, incident recreation or demonstration of autonomous immunity. Earlier ledger results remain preserved. Their twelve records were facts, not twelve realistic tasks. This scenario pilot prospectively replaces the not-yet-run task-6700 qualification; the owner's additional USD 8 authorization covers this bounded pilot and any separately documented repair, not USD 8 per retry.

## Results and disposition

[Full assessment and bad-decision analysis](ASSESSMENT.md) reports all three native attempts. The redesigned team preserved a healthy system but often failed to repair an unhealthy one; removing reviewers improved incident recovery but harmed the healthy control. Neither architecture establishes robust immunity. The deterministic contract solver remains the reliable baseline for this fully specified exercise. Total native API cost was USD 0.441259, with 240 calls and no response/provider failures. [Execution record and public runs](EXECUTION.md) links failed and completed attempts. No holdout was opened.

## Dated amendment: scenario a2

A1 (runtime 18fcd22) finished all 12 episodes and 108 calls with no invalid responses for USD 0.169049, but failed the healthy-system control. It remains in NATIVE-A1-RESULTS.json and its public run. Native explanations repeatedly conflated feature number, data format and RPC version, sometimes contradicting live checks. This is observed decision error; representation/prompt causation is an inference, not proven by those explanations.

Before a2, replace overloaded integer protocol/schema/feature labels with distinct named domains and use service names consistent with their roles. Keep binary versions numeric. Ask reviewers to assess whether a problem exists; allow no action needed explicitly. No evaluator health rule, feasible bundle, treatment rule or intervention outcome is changed. A2 combines presentation changes, so improvement cannot identify which change helped. All arms receive the same clarification. The old numeric rendering and source remain immutable in Git. New a2 native seed 9101 and engineering seeds 9020–9035 were unopened before this amendment; they change only service suffixes. This is a bounded competence repair, not an independent operational replication or a favorable-result retry. A second competence failure stops escalation for redesign rather than indefinite retries.

## Question and prediction

When stored operational advice conflicts with current dependency and data constraints, does revising memory improve recovery without damaging an already healthy system? Predictable engineering facts establish what is feasible; whether the agents notice them, use tools, or follow an obsolete handoff is the empirical uncertainty.

The primary exploratory contrast is revision_check minus retain in healthy customer ticks, separately for each scenario. Reset is a practical baseline. No pooled significance or population effect is claimed from four constructed cases. Equal performance is informative: explicit contracts and live probes may make a special memory mechanism unnecessary. A higher final success rate bought with more unsafe changes is not an unqualified win.

## Why run this

Restarting a process does not necessarily remove obsolete advice from the team. Conversely, erasing every handoff can discard a useful bridge-version hint. An operationally meaningful repair must restore service, respect persisted data, resist a delayed old recommendation and avoid disturbing a healthy system. An exact-value copying task could not distinguish those goals.

## Grounding and limits

[Kubernetes API concepts](https://kubernetes.io/docs/reference/using-api/api-concepts/) documents cache resynchronization when watch history is lost. [AWS's rollback-safety discussion](https://aws.amazon.com/builders-library/ensuring-rollback-safety-during-deployments/) motivates considering compatibility across forward and backward deployments. These sources motivate failure mechanisms; they do not supply these invented service versions, an observed incident distribution or evidence that revision filtering works. Our integer control revision is a fictional application epoch, not an implementation of Kubernetes resourceVersion semantics.

We model compatibility and irreversible persisted format with executable constraints. We do not model real Kubernetes, networking, throughput, attackers, continuous migration, noisy metrics, or authenticated provenance. Revision metadata is assumed reliable. There is no adversarial falsification of that metadata. Dropping all earlier notes can remove still-valid advice; this pilot does not establish its general safety.

## Setup

Three services form a dependency chain: gateway → worker → store. Gateway versions require named RPC protocols (`rpc-classic` or `rpc-batch`); worker versions can read named data schemas (`schema-legacy` or `schema-expanded`). Features are independent capability names (`checkout`, `bulk_checkout`), not numeric format requirements. Version 2 of the worker bridges both formats. Store binaries must match persisted data. A requested feature can forbid an otherwise compatible old gateway. Several bundles may be feasible: there is no single answer string.

The catalog and current health checks are available to every arm. The team has three advisory roles (compatibility, data safety, customer impact) and one commander. Advisors make one recommendation each, not eight repetitive endorsements every round. The commander makes six consequential tool choices: deploy one component, fetch the operator recommendation, or wait. Bookkeeping and evaluation are deterministic. Tools are simulated; no real service is modified.

## Protocol

Four cases: stale_advice starts with an incompatible worker but permits multiple safe recovery bundles; migrated_data makes the old snapshot incompatible with the expanded persistent schema; false_alarm starts healthy and requires bulk_checkout, exposing unnecessary repair; registry_partition denies refresh for the first three ticks while local compatibility contracts remain available. The commander does not receive case or arm labels. It does receive the operational evidence needed to solve the task; uncertainty is in decision behavior, not intentionally impossible information access.

All arms start from exactly the same deployment, catalog, handoff and schedule. Retain keeps both notes. Reset clears notes once before advice, but can learn again. Revision_check exposes only notes matching the observed epoch; this rule uses public metadata, not evaluator damage labels. At tick 4 an obsolete note returns in all arms, including reset. No memory arm secretly repairs the actual deployment. Advice is fixed after the initial consultation; later tool observations can contradict it. This tests a small team architecture, not the causal advantage of a swarm over a single agent.

Development tests use seeds 8900–8903. A2 engineering uses 9020–9035: four scenarios × three arms × 16 service-name suffixes = 192 episodes. These names test presentation consistency, not 192 independent operational situations. A2 native qualification uses seed 9101 in all four cases and all three arms: 12 episodes × (three advisory calls + six commander calls) = 108 calls maximum. No automatic retries or fallback-to-scripted native decisions. A model error is preserved and consumes its scheduled slot. Holdout seeds 9200–9215 stay unopened.

## Metrics

Report all six scheduled customer ticks in every assigned episode. Primary: healthy ticks, requiring all four independently computed checks (RPC, reader compatibility, stored format, requested feature). Also report final health, unsafe changes, deployment count, response failures, refresh timeouts, API cost and full action/tool traces. A store/data mismatch is rejected by a safety gate and counted unsafe. Other harmful deployments execute and can reduce service health. An unavailable simulated registry is a scenario outcome, not a provider failure. A model/schema error is an execution failure, not a scientific null result.

Qualification requires all 12 assignments, no invalid responses, no missing usage, and no regression in false_alarm. The reference solver must recover every scenario using only visible contracts. Its success establishes feasibility, not model ability or a treatment effect. Native clean competence is the healthy false-alarm control, a limited check; a separate no-contamination damaged-task baseline and independent scenario authorship are required before stronger causal claims. Do not silently discard failed episodes.

## Bad decisions we corrected

- Replaced copied fact equality with executable dependency/data/feature constraints and multiple acceptable bundles.
- Removed oracle affected-agent lists and known-bad record IDs from treatment decisions.
- Replaced a guaranteed broad-rollback-versus-selective result with memory treatments that can tie, hurt or be unnecessary.
- Reduced repetitive model calls from over a thousand to at most 108; each paid call reviews a risk or chooses a tool action.
- Kept a healthy-system case, registry unavailability and a migration trap so “repair everything” is not automatically rewarded.
- Stopped describing alias permutations as scenario diversity or scripted success as model evidence.

## Visualization mapping

Bind case, seed, arm, source hash and backend in every view. Show six measured ticks as a health timeline with tool-action annotations; highlight unsafe changes and provider errors separately. Pair it with a dependency diagram and the deployed version at each tick, and display the short decision justification plus observed tool result. Compare healthy ticks, changes and unsafe attempts across arms within each case. Animate recorded ticks only, preserving failed and missing steps. Publish final PNG, GIF and a self-contained replay. A single selected-case animation must say which case/seed it shows; full JSONL is the record of all outcomes.

## Reproduction and launch

Run `python3 -m unittest discover -s 5-experiments/studies/vishesh/immune-response-v3/scenario-study -p 'test_*.py' -v`, then `python3 5-experiments/studies/vishesh/immune-response-v3/scenario-study/study.py --backend scripted --out <new-path>`. Freeze this source and protocol before the engineering suite. Native execution requires the dedicated sim-immune-response claim, immutable public-plan check, the real USD 8 budget grant, pinned Haiku config and secure credential environment. The runner refuses an existing output directory. Record the exact source and protocol hashes, model, Python, assignments, call counts and actual costs; never overwrite a prior attempt.

## Architecture control

The separately frozen [single-commander baseline](SOLO-BASELINE.md) compares the same retained-memory cases with the three advisory calls removed. It is conditional on a2 passing the clean-control gate and uses the same cumulative USD 8 grant.
