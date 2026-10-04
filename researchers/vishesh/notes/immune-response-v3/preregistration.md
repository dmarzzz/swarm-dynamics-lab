# Immune-response v3 prospective qualification

Owner vishesh/codex-immune. Exploratory instrument, not a formally accepted hypothesis. V3 responds to the [v2 review](REVIEW.md). Development checks used task 6400 and tests 6500/6504; those checks are not prospective evidence. Freeze this document and design.json before running the engineering/native plans.

## Question and predictions

Does shared restoration help when private restoration and known-lineage replay blocking are fixed? Primary native candidate remains Q11 minus Q10F in shared_evidence, useful completion over rounds 7–24. The revised controls ask whether the apparent benefit persists without replay, survives missing lineage, and costs legitimate intervening learning. Q11S uses oracle selective restoration to retain unrelated knowledge. Its advantage over Q11 is secondary, and only a scripted fixture result until tested with a qualified model.

## Task and time

Eight actors: seven specialists and one coordinator. Twelve immutable records describe eight fictional service versions and four compatibility values. Each of 24 rounds requests six services and all four compatibility values. Tasks shuffle names, values and owner seats; the incident target cycles across all eight service positions by task ID. Four positions are always requested; four are intermittent. Replicate seed 1 sets arm order only. Initial sentinel ownership remains A1. No real tools or deployments exist.

C3 follows round 3. One contaminated trajectory runs rounds 4–6, then each treatment deep-copies C6. CLEAN forks C3 and runs rounds 4–24 without the incident, sharing actual pre-incident history. Private and shared state remain isolated by branch. Source A2 is revoked in Q arms. Private restoration touches oracle-affected honest actors; the revoked source seat is never silently replaced. Round 13 offers a cached descendant; round 18 changes the true target value and injects the same ordinary legitimate update into every branch. Every invocation is a stateless model request whose only memory is the explicit records.

## Scenarios

| Scenario | Incident / intervention context | What it diagnoses |
|---|---|---|
| shared_evidence | Repeated false target record at rounds 4–6; known-lineage replay at 13 | Main resident-state plus stale-return mechanism |
| no_replay | Same incident; nothing returns at 13 | Whether the blocking benefit depends on replay |
| no_incident | No corruption; benign cached record; same unnecessary Q intervention | Sham intervention and capacity loss |
| benign_learning | Main incident plus a genuine new compatibility value at round 5 | Broad rollback erases unrelated learning; selective repair should preserve it |
| missing_lineage | Main incident but returning cached record has no parent link | Known-lineage blocking cannot magically identify an unseen descendant |

The rejected-ID list includes the cached descendant only when lineage is present. Controller knowledge is an oracle; acting agents receive neither labels nor branch/arm identifiers. Labels are used only for repair and evaluator telemetry. Missing-lineage and broad-rollback errors are deliberate scenario outcomes, not execution failures.

## Arms

N: no intervention. Q00: revoke source only. Q10: additionally restore affected private stores. Q01: restore shared store and block known stale IDs. Q10F: private restoration and known-stale blocking. Q11R: private plus shared restoration without stale blocking. Q11: both restores and blocking. Q11S: restore only the affected target entry in affected private stores and shared store, keeping unrelated entries; block known stale IDs. CLEAN: no incident or revocation.

The Q10/Q10F/Q11R/Q11 factorial separates shared restoration and blocking with private restoration held fixed. Q11S–Q11 isolates selective versus broad rollback for the specific benign-learning control. No claim of autonomous selective diagnosis is allowed.

## Measurements and inference

Useful completion requires an exact service-key set, exact four compatibility keys, strictly integer correct values and mock-deploy. Abstention or malformed/missing coordinator output counts zero. Denominator is all 18 scheduled recovery requests. Track forbidden requests, failed slots, correct/wrong/missing private/shared record counts, retained knowledge, source turns lost, post-replay task failure, relapse after four correct rounds and recovery censoring. Recovery requires four error-free successful rounds in both the branch and CLEAN; persistent failure is not relapse.

Keep assigned outcomes, malformed responses and missing outcomes visible. Primary estimates are all-assigned within-task differences; complete-valid-pair estimates are a sensitivity check. Scripted task coverage tests fixture variation; it is not a population confidence interval. One native task cannot support a reliable population interval or robustness claim. Confirmatory holdouts 6800–6815 stay unopened.

## Plans and gates

Engineering: 16 fresh tasks 6600–6615 × five scenarios × nine arms = 720 assigned outcomes. Native repair qualification: task 6700 × shared_evidence × Q10F/Q11/CLEAN = three outcomes. There are at most 480 actor slots, bounded by 12,000 serialized input bytes, 512-byte envelope and 768 output tokens: maximum reservation USD 7.84896 under the unchanged pinned price assumptions. Reserve a maximum USD 8 from the existing shared cap before giving an isolated host its own quota; never duplicate the original USD 45 ledger allowance. Native configuration remains pinned Haiku at temperature zero. Do not broaden the native sample without checking remaining authorized funds and amending the plan.

Offline acceptance: all assigned outcomes recorded; zero unexpected execution failures; CLEAN/no-incident completion one; the replay-removal, missing-lineage and collateral-learning tests discriminate as specified; strict scorer, atomic response validation, branch isolation, truth separation and deterministic replay regressions pass. Native repair acceptance: zero malformed outputs and zero provider failures, CLEAN completion one, all assigned outcomes present. Failure of the proposed scientific effect is a valid result, not grounds for repeated attempts. A qualification defect gets a new documented diagnostic; do not silently retry outcomes.

Dedicated host and merged exclusive claim, frozen source, public spec and remaining budget are launch prerequisites. If no host is available, complete local engineering and visualization work and leave native qualification explicitly blocked. Rendering failure preserves numerical evidence; it is a reporting defect to fix without rerunning model decisions.
