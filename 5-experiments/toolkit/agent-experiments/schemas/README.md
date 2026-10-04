# Machine-readable contracts

JSON Schema draft 2020-12 files describe agent definitions, context/access manifests, production-oriented run templates, offline toy configurations, events and outcomes. Template validation establishes structural shape only: `REPLACE_...` values are deliberate and require resolution and semantic preflight. The production-oriented run template sets a zero-dollar cap and disables paid execution.

The included validator checks the subset used here (`type`, `const`, `enum`, `required`, `properties`, `additionalProperties`, `items`, bounds, `minItems`, `pattern`). It is not a general JSON Schema implementation. For production, validate with a full draft-2020-12 implementation and additional study-specific semantic checks. The event/outcome schemas describe the toy's narrower contract, not a complete production telemetry system. Extend them with attempt lineage, wall and monotonic time, usage, terminal reasons and safe provider identifiers before real execution.

| Field | Meaning |
| --- | --- |
| study_id | Frozen protocol/configuration identity, independent of individual execution directories |
| run_id | Scenario × replicate × treatment identity; retries retain this identity in a production extension |
| scenario_id, replicate | Scenario cluster and within-scenario paired repetition |
| condition | Prespecified treatment label |
| initial_sha256 | Hash of canonical public synthetic world, including hidden truth held by evaluator |
| seq, parent_seq | Monotonic event index within run and previous event link; richer message causal links require an extension |
| agent_id | Local identity or null for controller/evaluator events |
| payload | Public synthetic event data in the example; never credentials or unfiltered provider output |
| prev_hash, event_hash | SHA-256 chain over canonical JSON; integrity checking, not digital signatures or proof of authenticity |
| status | Execution terminal state, separate from task accuracy |
| score | Fraction of five final decisions correct, range [0,1]; null if not measurable |
| group_correct | Whether majority final decision matches truth; secondary outcome |
| decisions, api_calls, api_cost_usd | Logical policy decisions and separately measured provider usage; toy provider usage is exactly zero |

The toy writes these generated outputs to the chosen directory under git-ignored `data/`: `planned-runs.json`, `events.jsonl`, `outcomes.jsonl`, `summary.json`, `manifest.json`, and `config.resolved.json`. It records an independent planned ledger so missing runs are detectable. Canonical JSON uses UTF-8, sorted keys and compact separators; file formatting is not part of the event hash. Inputs and code are hashed by bytes. A local manifest cannot establish an independent timestamp or prevent an attacker who can rewrite both logs and the manifest.
