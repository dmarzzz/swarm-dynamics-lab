# Connecting real agents

The reference `Policy` interface exposes `ingest`, `discuss`, `propose`, `vote`, `sabotage`, `assassinate`, and `beliefs`. `World.policies` currently contains trusted in-process scripted implementations. There is no provider integration or paid execution path in this version.

An `Observation` contains the caller's identity and role, council member IDs, role-authorized local evil membership or null, one private noisy signal, mission and proposal indexes, proposed team, local mission history, received claims, and local verified audit labels. It contains no complete role table. The evaluator owns roles and objective scores. Do not pass `World`, controller files, event archives, or debugger access into an agent sandbox.

Use a phase-tagged JSON request and a strict response schema. Discussion output is up to four bounded claims, proposals are the exact required number of unique local IDs, ballots and sabotage choices are booleans, assassination is one local ID, and beliefs are finite probabilities for the permitted local targets. Any natural-language expansion needs a byte and token limit in addition to the number-of-claims limit. Never execute agent-supplied code as a parser.

Move relay authorization into the controller's own delivered-message ledger before allowing arbitrary policies: checking a policy's mutable memory is only acceptable for trusted baseline code. Corrections should refer to auditable source IDs. Store environment-signed verified evidence separately from agent assertions; merely writing “verified” in a message cannot grant verification status.

The reference harness calls decisions sequentially within a synchronous logical stage. A production worker pool should collect same-phase outputs from a frozen snapshot, apply them in deterministic agent-ID order, and only then advance. Queue timing must not leak another agent's response into a supposedly simultaneous ballot. Cap provider concurrency independently from population size, and preserve private state per world and identity.

Reserve worst-case call cost before dispatch. Include probes, retries, summaries, and cached token categories in accounting. Use strict deadlines and declared defaults for missing actions; record invalid output separately from provider failures. A timeout must not become a silent strategy retry. Every planned world needs one terminal outcome, including failure, cancellation, timeout, or budget exhaustion. A retry is not a new scientific replicate.

Credentials must enter through a local credential store or provider-native secure setup. Local authorized processes may consume them, but tool output must contain only allowlisted status metadata. Never ask for keys in chat or log headers, environment dumps, or raw authentication errors.

Record model identifier, model settings, prompt and schema hashes, source hash, context cap, memory policy, provider concurrency, usage, wall and queue time, and treatment assignment. Keep the controller's complete role table and diagnostic origin classifications inaccessible to agents. Publish sanitized synthetic traces with the final run manifest.

Version 0.2 also probes ordinary-good agents after each discussion tick for truth-consensus scoring. Keep these read-only probes separate from agent memory and communication; the probe reveals no role labels. Charge their usage explicitly. `belief_probe_calls` counts these consensus probes; the existing Brier calculations are additional diagnostics. Never expose the global consensus report or its protected classifications to agent policies unless a later protocol explicitly defines that feedback treatment.
