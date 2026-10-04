# Integration contract and source checks

**Design status:** documentation only, checked 2026-10-03. The contract below proposes an extension to existing tooling; none of these immune-response operations has been implemented or validated by this note.

## Reuse the existing toolkit

Use [tooling/agent-experiments](../../../toolkit/agent-experiments/README.md), its [harness contract](../../../toolkit/agent-experiments/HARNESS.md) and [protocol template](../../../toolkit/agent-experiments/templates/protocol.md). The published example uses scripted agents. An LLM adapter, state-store repair and production checkpoint support require separate implementation and tests.

The current [event schema](../../../toolkit/agent-experiments/schemas/event.schema.json) has five permitted top-level types: `run_start`, `observation`, `decision`, `evaluation`, `run_end`. Keep that envelope and hash chain. Put proposed semantics in `payload.kind`, such as `claim_admitted`, `quarantine_decision`, `repair_applied`, `reentry_attempt` and `probation_result`; do not add incompatible top-level event types.

Each intervention payload should record target scope and identifier, visible evidence references, authority/policy version, old/new state hashes, reason, resource cost and release criteria. Use a versioned payload contract in the future adapter. Multiple claim dependencies need an explicit `payload.parent_event_ids` or equivalent lineage list: the existing single `parent_seq` cannot express the full dependency graph. Hashes establish recorded integrity, not truth or completeness of provenance.

Keep evaluator-only labels, planted-source identity and hidden task facts in separate artifacts with explicit access controls. A policy event may contain its own suspicion score; it must not receive an oracle label through a conveniently shared event log. Public examples should contain synthetic data only.

The strict [outcome schema](../../../toolkit/agent-experiments/schemas/outcome.schema.json) does not permit arbitrary extra fields. Preserve it and put longitudinal metrics in a separate, versioned `immune-outcomes.json` sidecar keyed by study/run/scenario/replicate/condition, with schema identifier, event-log hash, evaluator version, trajectories, denominators and censoring indicators. This is a suggested filename and contract, not an existing supported output. A future schema change requires explicit versioning and consumer migration.

## Checkpoint inventory and implementation acceptance

Snapshot private contexts, shared stores and indexes, caches, tool queues, pending writes, communication buffers, task versions, scheduler position, available RNG state, policy/model configuration and budget reservations. Give each fork separate mutable storage and a parent-checkpoint hash. If an API cannot reset hidden conversational state, start a new conversation and disclose the limitation. A reset that leaves a hidden summary or pending write intact is a different treatment.

Before any model collection, a future implementation should demonstrate:

1. A planted error produces distinguishable exposure, adoption, propagation and mock-action events.
2. Private-only reset leaves the intended shared reservoir intact; shared-only repair leaves private history intact; forks cannot write into each other.
3. Quarantine blocks the declared capabilities across direct messages, queues and shared tools. Replacement has a new instance ID and its own cost.
4. A correction survives a returning stale child when release conditions require it, and a deliberately incomplete repair can fail that test.
5. Correct minority evidence survives the narrow-repair control; unserved tasks and false exclusions remain visible in scores.
6. Detector inputs cannot access oracle labels or hidden answer keys; missing provenance stays unknown.
7. Failed, censored and budget-exhausted runs retain their event histories and outcome denominators.

The durable audit record should record invalidation without deleting the evidence needed to reconstruct what happened. Operational agents receive only authorized repaired state. Keep collection, repair and evaluation budgets separate in reporting but enforce their combined cap.

## Primary-source access ledger

The following sources were opened for this design or its immediately preceding atlas review. Depth below describes our fresh inspection, not the catalogue author's claimed depth. No code was run and no empirical result was independently replicated. These are targeted checks, not a complete prior-art survey. Existing library records are reused without changing another researcher's entries.

| Source | What was checked | Consequence for this proposal |
| --- | --- | --- |
| [INFA-Guard](https://arxiv.org/html/2601.14667), [[zhou-2026-infa-guard]] | Abstract and targeted Sections 3–4, especially 4.3 equations 10–11. Predicted attackers are replaced; affected replies are cleaned before further communication. | Recovery is already an explicit objective. Compare against this mechanism after full implementation review; do not claim “first healing defense.” |
| [MemSecBench](https://arxiv.org/abs/2607.27080), [[chen-2026-memsecbench]] | Abstract. A controlled write/execute/forget lifecycle evaluates persistence, downstream consequences and selective repair across memory configurations. | Selective memory repair is also prior art. Inspect its checkpoints and retention criteria before fixing ours. Multi-agent return-path coverage has not been established by this abstract check. |
| [MemTX](https://arxiv.org/html/2607.23929v1), [[li-2026-memtx]] | Abstract checked in the atlas review; primary page reopened for this design. Staged belief updates and dependent repair are the relevant nearby mechanisms. | Cascading rollback is not a novelty claim. Compare the proposed shared/private treatment decomposition against its full methods. |
| [MemLineage](https://arxiv.org/html/2605.14421v1), [[ouyang-2026-memlineage]] | Abstract checked in the atlas review; primary page reopened. Lineage-aware gating of sensitive actions is relevant. | Incomplete lineage and authorization should be explicit controls, not ignored advantages for our repair policy. |
| [G-Safeguard](https://arxiv.org/abs/2502.11127), [[wang-2025-g-safeguard]] | Abstract. Graph-based malicious-agent detection and topology modification. | Candidate containment baseline; recovery behavior and exact implementation remain to be reviewed. |
| [GAMMAF](https://arxiv.org/abs/2604.24477), [[mateo-torrejon-2026-gammaf]] | Abstract. A common graph-monitoring evaluation with live isolation. | Check benchmark reuse before building evaluation infrastructure. Code availability and faithful integration are unverified. |
| [Reliability–Contagion Feasibility](https://arxiv.org/abs/2607.21912), [[niu-2026-reliability-contagion]] | Abstract. Network conclusions depend on whether exposure is budgeted per edge or per sender. | Hold exposure accounting explicit when changing connectivity; do not ascribe a budget change to topology alone. |
| [Zombie Agents](https://arxiv.org/abs/2602.15654), [[yang-2026-zombie]] | Abstract, current v2. Indirect content can persist in long-term memory and later induce unauthorized tool behavior. | Include delayed retrieval and separate action authorization from factual correctness. Our mock task is not a replication of its attack setup. |

No numeric paper performance is imported into our power, cost or expected-effect assumptions. NetSafe and AgentPrune were discussion/catalogue leads, not freshly reviewed methods for this design, so they do not support a claimed gap here. The next survey should include distributed recovery/checkpointing and fault-tolerance literature as well as LLM defense papers; this note has not completed that search.

## Collaboration boundary

The public anchor is [PR 82](https://github.com/dmarzzz/swarm-lab/pull/82), inspected while open at head `a6a201da1753b653432a16bd2db39928d06957b8`. The capture-memory draft is provisional. We preserve the infect/remove/recover comparison as motivation and add objective task recovery, shared reservoirs and false-quarantine controls. Discussion material supplied by the human informed the design; private transcripts and screenshots are not included in this contribution.

This note changes no other researcher's hypothesis, does not register an experiment, and makes no claim that another contributor has agreed to implement or review the extension. A later formal protocol can incorporate measurement feedback through the normal review process.
