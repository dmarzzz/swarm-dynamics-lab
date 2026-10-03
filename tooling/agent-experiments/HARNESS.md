# Harness selection and implementation

The experiment harness owns allocation, resets, observation delivery, action execution, budgets, logs and scoring. Agent orchestration is one component. A workflow library alone does not define the experimental unit or make experiments reproducible.

## Choose the smallest appropriate foundation

Capabilities below were checked against official documentation on 2026-10-03. Pin a tested release; documentation tagged “latest” is not a version lock. No external framework was installed or benchmarked for this package.

| Option | Appropriate use | What the study must add |
| --- | --- | --- |
| Custom Python runner, like this package's toy | Small, discrete, synthetic mechanisms with objective truth | Production isolation, provider adapter, robust storage, monitoring and statistical design |
| [Inspect](https://inspect.aisi.org.uk/) | Model/agent evaluation with datasets, solvers, scorers, tools, logging and sandbox support | Explicit swarm/world unit, topology semantics, scenario pairing and safe trace policy |
| [Mesa](https://mesa.readthedocs.io/latest/) [[gh-mesa-mesa]] | Agent-based spatial/network models and data collection in Python | LLM adapter, immutable prompt/context records and controlled model randomness; stable Mesa 3 versus development Mesa 4 must be selected deliberately |
| [NetLogo BehaviorSpace](https://docs.netlogo.org/behaviorspace.html) [[gh-netlogo-netlogo]] | Classical ABM parameter sweeps, repeated runs and accessible simulation models | Pin NetLogo/model versions; isolate external LLM calls; maintain trace provenance and scheduling semantics |
| [PettingZoo](https://pettingzoo.farama.org/) [[gh-farama-foundation-pettingzoo]] | Multi-agent environments with explicit observations, actions, rewards and termination | Choose sequential AEC versus simultaneous Parallel API to match the scientific model; add language interfaces and evaluator isolation |
| [Melting Pot](https://github.com/google-deepmind/meltingpot) [[gh-google-deepmind-meltingpot]] | Social interaction/generalization in multi-agent RL substrates | Study-specific language interface, population splits and domain validation; it is not a generic social-human simulator |
| [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview) [[gh-langchain-ai-langgraph]] | Stateful workflows, persistence and human interruption | External experimental ledger, condition-specific state namespaces, controlled resumes and protected scoring |
| [SOTOPIA](https://arxiv.org/abs/2310.11667) [[zhou-2023-sotopia]] | Goal-directed social interaction and role-play evaluation | Local evaluator calibration and evidence for any human-population inference |

For a small collective-sensing teaching model, start with a small explicit world model and a pluggable policy interface. Inspect can manage real-model evaluation; Mesa becomes useful when spatial dynamics matter; PettingZoo becomes useful if RL agents and formal multi-agent environment interfaces are central. Keep scheduler and scorer behavior testable without any model.

## Architecture and trust boundaries

```text
Frozen protocol + source/config/data hashes
                    |
          schedule and block allocator
                    |
        disposable world for one run
        | environment + tool executor |
        | agents + local memory       |
        | routing + budget controller |
                    |
        append-only sanitized event sink
                    |
   protected evaluator -> run outcome ledger
                    |
       frozen analysis -> report + archive
```

The host controller can read hidden truth; the agent process receives only its allowed observation. Protect evaluation in a separate permission domain. Prompts are not security boundaries. A hostile agent must not be able to overwrite the task, expected answer, grader, completion marker, budget counter or log. Containers help but require appropriate mounts, network and resource controls; a Python class does not enforce isolation against arbitrary code.

## Deterministic scripted initialization

1. Load schema-validated configuration; reject unknown fields and unresolved placeholders for real execution. Resolve overlays before hashing. Record original and fully resolved definitions.
2. Verify public artifact hashes against a frozen manifest. The absence of an initial Git commit is acceptable if an explicit source archive and content hashes are recorded. A hash proves byte identity, not correctness or a trustworthy timestamp.
3. Start a fresh filesystem, database namespace, tool sandbox, browser profile, memory store and agent process for the run. Establish network and resource policy before agent code runs.
4. Derive named seed streams with a stable cryptographic hash of `(master seed, study version, scenario, replicate, stream, agent ID)`; use an explicit portable RNG implementation if cross-runtime bitwise identity matters. Never use process-randomized language `hash()`.
5. Generate the scenario and exogenous schedule before applying treatment. Save their public-safe hash. Create identical baseline copies across paired conditions. Agents within one world can legitimately have different private observations; it is each corresponding agent's baseline context across treatments that must match.
6. Apply only declared treatment overlays. Compute and record a machine-readable diff. Compare rendered initial prompts, observations, tool schemas, clocks and available data—not only manifest labels.
7. Freeze the initial world, launch the scheduler and write `run_start`. If any preflight check fails, write a sanitized failure to the controller ledger and do not call providers.

For live retrieval, identical manifests do not guarantee identical retrieved results. Prefer frozen documents, index snapshots, embedding revisions, chunk boundaries and ranked-result snapshots. If live retrieval is the subject, log retrieval timestamps and returned content hashes, block in time, and report variability. Distinguish access eligibility, fetched content and actual context visible at each action.

## Scheduling, fairness and failures

For a synchronous round, all agents observe the same pre-round world, actions are collected, then a deterministic transition applies them. A sequential loop that lets later agents see earlier actions is a different mechanism. For asynchronous execution, record send, delivery and processing order with monotonic event IDs and causal parents; replay wall timestamps alone cannot reconstruct races.

Limit both experiment-wide provider concurrency and per-run concurrency. Keep conditions balanced across execution windows. Model rate limits, server batching and queue delays can affect cost and outcomes. If latency is an endpoint, define whether queue time counts and measure it consistently. Reserve resources for a run or report contention as part of the environment.

Use hard controller-enforced caps for aggregate tokens, calls, time and money. Check remaining allocation before dispatch and reserve worst-case per-call cost; reconcile after response. Define what happens when usage metadata is missing. A budget visible only in a prompt is advisory. Track cached and uncached input, output, reasoning tokens when exposed, rejected calls, retries and evaluator consumption. Save price-table date, currency and source or invoice reference; this package makes no current price claims.

Retries require an idempotency key for side effects, a cap, backoff, retriable-error classes and attempt events. If a request may have executed before timing out, reconcile state before retrying. Invalid agent actions and bad answers should not be retried as invisible infrastructure repairs. Model fallback changes the treatment unless explicitly part of its definition. Disable automatic fallback or log and analyze it as prespecified.

A run ends with exactly one terminal ledger outcome: `completed`, `failed`, `timeout`, `budget_exhausted`, `cancelled`, or `unscored`. Record outcome validity separately from execution status. Do not convert unknown scores to numerical zero unless the endpoint defines them that way. Reconcile every planned unit after a controller crash; an absent terminal event must become an auditable incomplete record. Checkpoints retain run identity; fresh restarts receive attempt lineage and do not count as new samples by default.

## Event and outcome contract

See [schemas](schemas/README.md). Events carry study/run/scenario/replicate/treatment/agent identifiers, a sequence number, event type, causal parent, sanitized payload or artifact reference, and a chain hash. Production extensions should include UTC and monotonic timestamps, request IDs safe to disclose, logical round, usage, latency and intervention identifiers. The local demonstrator uses logical sequence only, making its files byte-replayable; it is not a wall-time logger.

Never print raw provider errors or headers. Allowlisted structured metadata should cross the adapter boundary. Store public synthetic traces inline; restricted raw data require a separate protected store and reviewed exports. Hashes and encryption do not themselves anonymize personal information.

Use event sourcing to recompute outcomes and audit trajectories. Maintain a separate planned-run table so missing logs cannot disappear from the denominator. Compare recomputed results to scored outputs. Validate event order, terminal uniqueness, budget accounting, graph permissions, initial-state equivalence and reset isolation. Include fault injection: timeout, partial write, duplicate response, malformed action, unavailable judge and lost worker.

## Three different meanings of replay

- **Trace replay:** feed recorded actions and tool results to the state machine. It tests state transitions and scoring without requerying a model.
- **Fresh execution:** rerun the same frozen configuration with new or recorded seeds and new provider calls. It measures behavioral variability.
- **Independent replication:** a separate team or implementation tests the same claim, with deviations declared.

For hosted LLMs, identical seed, temperature and prompt do not guarantee identical output. Nondeterministic kernels, server batching, request routing, hidden provider updates and unsupported seed semantics can intervene. Temperature zero does not eliminate these sources. Pin available snapshots, record exposed backend metadata and repeat runs; describe determinism as an observed property within a stated boundary. Local models also need weights, tokenizer, runtime, hardware and deterministic settings locked, with numerical tolerance declared.

The demonstration's rerun check is exact for its deterministic scripted policy and recorded Python runtime. Its event replay reconstructs accuracy from recorded decisions independently of the policy. It does not simulate provider nondeterminism, durable distributed storage or hostile-code containment.
