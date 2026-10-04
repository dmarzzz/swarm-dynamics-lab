# Frozen exploratory protocol v1

## Question and prediction

Can continuing to check established reputations while investigating little-audited identities preserve rare truthful information after a coordinated sleeper attack? The directional prediction is that renewal improves round-8 specialist accuracy over reputation auditing by at least 10 percentage points in the 16-identity sleeper condition. Zero, negative, or uncertain effects are valid outcomes. An apparently strong result accompanied by high harmful-report admission or honest-specialist rejection must be reported with that tradeoff.

## Assignment and information

See `design.yaml` and README for the complete fixed matrix. Tasks 7100–7123 are 24 paired world clusters. Engineering tasks 6900–6901 and qualification tasks 7000–7005 are separate. Formal S2 tasks 12000–12999 remain unused. World truth depends on task and round, not policy or strategy. Common random numbers determine report labels/order, audits, tie breaking, and truth across paired policies/strategies. Identity-count comparisons share truth but not an identical set of identities or audit opportunities.

The comparison policies are deterministic functions of observable reports and selected audit history. No policy receives world truth or ownership. The model sees a current-round packet only. Before the switch, all controller and honest messages are true and external audit accuracy is role-independent. Half the controller identities are new in round 4 at 4/16 identities. The same 16 controller messages are redistributed over active identities every round. All arms have four checks and twelve report slots. All methods use the same post-check admission rule.

## Outcome definitions

- Specialist accuracy: number of exactly correct outputs for current skills 3, 4, and 5 divided by three. Wrong values and null both count as incorrect.
- Task accuracy: exactly correct outputs over all six skills.
- Wrong specialist output share: non-null incorrect specialist values divided by three.
- Harmful seat share: admitted reports with a false current claim divided by twelve.
- Controller/attacker seat share: admitted reports owned by the common controller divided by twelve, even when it tells the truth. Ownership share is not itself harm in clean rounds.
- Honest specialist newcomer retention: admitted rare honest messages divided by three after round 4; unavailable before round 4.
- Available-truth diagnostic: fraction of rare fields whose true value appears at least once in the admitted packet, evaluated with hidden truth. Not fed to the model; not a strict bound on guessing.
- Unique contributors, cumulative audits per active controller identity, newcomer/veteran audit split, and round-3 reputation show the identity/reputation mechanism.

## Analysis and sample size

Primary: the paired world difference renewal minus reputation, sleeper strategy, sixteen controller identities, round eight, specialist accuracy. Report its mean and 95% descriptive bootstrap interval, resampling whole worlds 10,000 times with seed 20261004. This is an exploratory 24-world study, not power-qualified or confirmatory. All 81 cells (identity × strategy × arm × sampled round) and renewal-minus-random contrasts are secondary. Multiple comparisons are exploratory without significance claims. No individual actor or round is an independent replicate. Failures remain in planned denominators; valid-completion means and assigned-denominator accuracy are both reported. Any paired contrast reports its actual number of complete world pairs.

Prespecified secondary identity contrasts compare 16 minus 1 controller identities within each policy, strategy, and sampled round for specialist accuracy, harmful seat share, and newcomer retention. Also report the paired world interaction (renewal minus reputation at 16) minus (renewal minus reputation at 1). Duplicate assignment IDs are rejected. Assigned-denominator accuracy bounds put missing outcomes at zero and one, while complete-case paired contrasts retain their actual pair count.

Noattack/clean controls have the same controller identities and messages, so only attack behavior is removed. A plurality synthesizer on the exact same packets is diagnostic. Relapse is defined before execution as a stress test; its code may be structurally self-tested, so it is not described as unknown to the design team or a formal holdout. There is no tuning on S1 outcomes.

## Qualification and runtime

Model `claude-haiku-4-5-20251001`, temperature zero, native structured JSON, six fields, max output 500 tokens, no tools, no thinking, no caching, no retries. Q0: 36 packets, full/common-only/sparse coverage, with one or two agreeing reports per present field; each shape requires at least 95% field accuracy, 90% exact packets, and 100% absent-field abstention. S0: 198 scripted observations, all structurally valid and qualification thresholds passed. A failed Q0 blocks S1 pending a preserved diagnostic/repair attempt using fresh competence fixtures.

Every assignment is saved before calls; every terminal record includes packet hash, source hash, code commit, actual usage when provided, evaluation, completion time, and failure status. Any invalid API observation stops new dispatch and drains at most two in-flight calls, marking undispatched rows not_started. A fresh attempt never silently replaces a failed result. Provider reservations are durable and nonrefundable in the study ledger. Budget: 2,050 attempted calls, $75 local conservative ceiling, plus the parent's shared $60 bundle actual-plus-outstanding limit for both experiments. The owner-wide total remains $500; parent launch reconciliation is required. Q0+S1 plan is 1,980 calls. Two concurrent workers per study run alongside the other study; stage timeout is four hours. No secrets enter packets, reports, artifacts, or Git.

## Visualization and provenance

`VISUALIZATION.md` v1 maps saved logical history to an eight-frame replay, current-completion progress PNG, and final tradeoff image. The renderer has no effect on scientific random draws. The runtime source hash includes configuration, requirements, and every Python module under src. Runtime changes invalidate exact-source qualification gates; documentation-only post-mortems do not.

## Allocation correction — 2026-10-04 UTC

The owner's updated inbox requires a dedicated host for each experiment. S0 and Q0 historically completed on sim-dmarz-4 under dmarz-sybil-followups; those completed results and runtime fingerprints are preserved. Before S1, this study moves to the dedicated host sim-dmarz-sybil-newcomer under claim dmarz-sybil-newcomer. Provisioning, claim exclusivity, migration and ledger continuity remain pending the parent operator's verification. S1 is not launched by this correction. No simulator, assignment, model, evaluator or source/configuration fingerprint changes.

Across the separate hosts, the existing $60 bundle cap is partitioned into at most $50 total for sybil-budget-api and $10 total for sybil-newcomer-api. Both hosts retain the same settled 52-call checkpoint ($0.366548). The budget host permanently reserves the $10 peer allocation; the newcomer host permanently reserves the $50 peer allocation. Historical charges are not reset. Duplicating the settled checkpoint in both guard copies makes the aggregate bound stricter, rather than creating extra spending authority.

These permanent peer reservations are inter-host allocations, not API charges, model calls or unknown-billing failures. Do not count them as actual experiment spending. Final actual cost is the sum of the separate per-study usage ledgers. Existing per-study conservative reservation/call limits still apply, with the new partition providing the tighter real-spend limit. The parent must verify the guard state and exclusive allocation before launch; this document does not claim that provisioning or migration is complete.
