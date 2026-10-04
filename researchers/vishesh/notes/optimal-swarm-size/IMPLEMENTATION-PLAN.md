# Qualification implementation plan

Written 2026-10-04 UTC before generator implementation. Owner: vishesh/codex-idea-scores.

## TLDR

Build and audit deterministic evidence and bounded repository-repair task generators for the planned N=1,2,4,8,16 qualification. Compare roster sizes only in the later matched-budget core study; the first 80 episodes are engineering qualification. Metrics are verified submission, grounding/behavioral quality, on-time delivery, usage and failure class. Synthetic fixtures establish software correctness, not model performance or a hardware-optimal swarm size.

## Question and prediction

Can the qualification tasks distinguish valid repairs and supported answers from plausible but invalid outputs while giving every roster the same task and tool access? Correct reference fixtures should pass, injected defects should fail, and generated inputs must be invariant to N. Those are software invariants, not predictions of which team size wins.

## Setup

Implement under this owned notes directory while the research gates remain incomplete. Standard-library Python only for the generator/evaluator unit tests. No model calls, external task data or fleet execution for these tests. Separate public task material from evaluator truth and never pass the latter into actor interfaces. Leave transfer roots ungenerated.

Two generated families: inventory reconciliation using integer arithmetic and source provenance; bounded Python arithmetic-module repair with independent or chained functions. For the repair pilot, use an explicitly published restricted expression language (integer constants, x, arithmetic and named prior functions) and a bounded AST interpreter instead of executing returned Python. This narrows the earlier generic repository-repair proposal and must be reported: it is a small repair benchmark, not evidence of production software-engineering ability. Accept equivalent expressions within that grammar using held-out input checks. No imports, filesystem access, subprocesses or arbitrary execution are permitted by the evaluator.

## Protocol

Use SHA-256-derived root seeds with version, split, family, structure and root index. Size is never part of task generation. The 16 qualification roots cover two families, two structures and four roots per cell; the manifest expands to 80 assignments by roster. Q-A contains the 16 N=1 screening episodes; Q-B contains 64 N>1 assignments after calibration. Keep fit, validation and transfer namespaces disjoint. Do not generate transfer examples during development.

Store source records/file snapshots in the actor-facing object; store expected values, proof sets and hidden inputs separately. Reject duplicate JSON keys, unknown fields, boolean-as-integer answers, non-finite timing/usage and oversized payloads. Repository tests must exercise alternative equivalent valid expressions, not only the reference repair. Trace accounting and the credential-consuming runner are separately reviewed components before model launch. The implemented small-fixture protocol places the full public input in each context, charges replication, and hands each actor only its declared prerequisite ledger entries. The bounded worker turn returns one partial artifact; context 0 integrates all recorded artifacts. These fixtures do not yet test large-corpus retrieval.

## Metrics

Offline checks cover deterministic regeneration, root separation, roster-invariant task hashes, parallel/chain contrasts, correct and incorrect evidence, missing/extra citations, malformed outputs, forbidden repair syntax, wrong repairs, equivalent repairs and outcome boundary conditions. No offline unit test is uploaded as a model experiment. All genuine runs require a frozen source, complete model/runtime/limits, public-plan registration, condition-specific TLDR and dedicated allocation. Spending authorization is pending an explicit amount.

## Visualization mapping

The generator exports public item IDs and declared dependencies. Real replay frames will consume recorded actor work/queue/integration events, with labels for failed/missing observations. No simulated time or generated fixture is to be presented as measured model latency. The renderer/runner must be qualified before launch. The implemented fallback is live textual item progress plus an uploaded standalone service-interval replay and raw events; no unsupported flock visualization is substituted.
