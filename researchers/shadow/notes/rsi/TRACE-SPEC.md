# Swarm Trace and Bundle Protocol

**Version:** `swarm-trace/0.2.0`

**Status:** draft specification plus an offline reference example, not deployed infrastructure.

**Headline:** a privacy-preserving agent trace interface on which other agents can compete to add useful next steps, repairs, reviews and replications, with explicit originator credit and independently verified value.

**Default for an explicitly enrolled research cohort:** **public envelope, sealed content**. Unenrolled work remains private. No raw trace export without a separate explicit owner approval.

This is the MEV-facing extension of the [trace-backed improvement design](../rsi-loop/DESIGN.md), not a replacement for its privacy, preregistration or independent-review rules. The previous `research-trace/0.1` episode rollup remains a separate legacy format. It is not silently reinterpreted as a signed span/event stream.

## 0. Deliverables and nonclaims

- [trace.schema.json](trace.schema.json): JSON Schema 2020-12 for the public/offline profile, with event, content-projection and bundle records. All objects are closed to unknown fields. [build_schema.py](build_schema.py) generates it reproducibly.
- [pool_to_spec.py](pool_to_spec.py): converts an explicitly selected, locally scope-verified pool cohort without copying body content into public output.
- [examples/pool-events.jsonl](examples/pool-events.jsonl): **three real historical pool records**, with derived envelopes and salted content commitments.
- [examples/pool-content-public.jsonl](examples/pool-content-public.jsonl): separate redacted content projections. Every body is a fixed `[SEALED]` or `[OMITTED]` marker, not a text excerpt.
- [examples/worked-bundle.json](examples/worked-bundle.json): a fully worked offline bundle, competitor, evaluator fixture, selection and hypothetical allocation.
- [protocol.py](protocol.py), [demo.py](demo.py), [test_protocol.py](test_protocol.py): canonicalization, commitments, schema/semantic checks, an offline one-slot selector, payment arithmetic and adversarial tests.

No provider service, experiment harness, hub, live task queue or payment system was changed. No model call, raw disclosure, auction deployment, actual payment or scientific policy promotion was performed. Imported records are explicitly **ineligible for live orderflow auctions**. Cryptographic signatures, identity enrollment, funded escrow and isolated execution are required production components, not features this prototype pretends to implement.

## 1. What the mempool analogy means

**Orderflow** is an originator-authorized opportunity to contribute to an agent workflow. A trace describes observations; it is not itself an executable order. Completed results are immutable observations. Pending assignments and possible next steps form the opportunity stream, with explicit permits, resource caps and inclusion windows. Calling this a mempool does not make past inference calls reorderable.

Use the Flashbots terms narrowly:

- **Originator/orderflow provider:** the human/research principal whose authorized agent produced the work. A proxy operator recording it is not automatically its intellectual author or economic owner.
- **Hints:** selected envelope facts, such as operation class, model, usage, completion class, permitted task category and commitment. They are a policy-controlled partial view, not an implicit license to the content.
- **Searcher:** an agent or service that consumes permitted hints and proposes a bundle. Searchers can be repair specialists, reviewers, replicators, hypothesis generators or routing optimizers.
- **Bundle:** an ordered, dependency-bound proposal plus inclusion predicates, resource limits, evidence requirements and value-sharing terms. It is not permission to execute arbitrary code or spend money.
- **Builder:** constructs a feasible ordered set of bundles from the permitted orderflow, checks versions/conflicts, obtains authorized simulations/evaluations and proposes a plan. Multiple builders may compete.
- **Proposer/controller:** owns the task queue and execution authority. It chooses a valid builder plan and commits assignments under the owner's budget. It is separate from the builder. This is the **PBS** analogy; it is not Ethereum consensus, validator blockspace or MEV-Boost wire compatibility.
- **Backrunning:** adding work after an originator-authorized result/artifact becomes available, for example independent replication, a review or a successor hypothesis. It never means publishing someone else's unreleased conclusion first.
- **Orderflow auction (OFA):** a funded competition for inclusion/access to an authorized workflow opportunity, with proceeds rebated to the originator according to agreed terms. The selected searcher's bid must be backed by escrow if it promises money. A claimed score increase is not a funded bid.
- **MEV-Share analogy:** originators choose hints and permitted builders, searchers submit partial proposals against opaque source commitments, and successful contributions can share value with originators. The allowed builder set is the **intersection** of all source policies and the bundle policy, not their union.

Ethereum bundles can have atomic transaction inclusion. Agent work consumes time and often has irreversible side effects. Here only **assignment reservation and candidate artifact publication** can be atomic; model/tool execution and consumed budget cannot be rolled back. Failed work remains recorded. The v0.2 prototype permits offline, no-network, zero-paid-call work only.

**Economic distinction:** a sponsor-funded review/repair bounty is a procurement mechanism, not proof that financial MEV was extracted. Actual OFA proceeds and sponsor bounties have separate accounts. There is no token issuance, transferable reputation or monetary reward minted from a model's self-reported score.

## 2. Trace format

### 2.1 Envelope

Each UTF-8 JSONL line contains one record. `schema_version` is exact, not a permissive version range. Unknown major/minor profiles must be rejected or explicitly adapted. Field absence in OTel attributes means unknown/not captured; explicit nullable application fields preserve missingness.

An `event` has these groups:

1. **Identity:** `event_id`, `stream_id`, `stream_seq`, `producer_id`, `owner_id`, `agent_id`, `run_id`, `task_id`, `attempt_id`. Owner, producer and agent are distinct. Stable agents are registered to a human/research principal; aliases are not independent identities. Missing native identifiers remain null.
2. **Causality:** W3C-compatible nonzero 128-bit `trace_id`, nonzero 64-bit `span_id`, nullable `parent_span_id`, `step_id`, `parent_step_id`, and explicit `links` with `depends_on`, `follows`, `derived_from`, `reviews` or `supersedes`. An agent step can contain several spans. DAG relationships are not inferred from wall-clock proximity. Parent links are same-trace; cross-trace dependencies use links.
3. **Lifecycle:** `event_type` is `assignment_created`, `span_started`, `span_ended`, `span_snapshot`, `step_committed`, `artifact_published`, `review_recorded` or `run_cancelled`. Live producers record start before dispatch and terminal state on every exit path. Historical adapters use `span_snapshot` rather than inventing missing starts or terminal confirmations.
4. **Timing:** `timing.observed_at`, declared `precision_ms`, nullable `start_time`/`end_time`, `duration_ms` and `ttfb_ms`. An ingestion/observation time is not necessarily operation start. Durations should use a monotonic clock. The public projection may coarsen or suppress absolute time. Clock uncertainty and unjoined legacy spans cannot be used to establish priority.
5. **Model/operation:** named OTel attributes under `attributes`, including operation, provider, requested model, served model when independently observed, stable agent ID, stream flag, total input/output and cache token counts. Do not infer a served revision from the request alias.
6. **Tool calls:** nullable `tool_calls`. Each known call has an opaque call ID, registered safe tool name, parent model span, argument/result commitments and state. A model proposing a tool is not proof the tool executed. `null` means not captured, `[]` means positively observed absence. Arguments, shell commands, URLs, paths, definitions and results belong in the content layer, never a free-form envelope field.
7. **Transport and outcome:** HTTP status and transport state are separate from scientific outcome. HTTP 200 is not an accepted artifact, valid completion or stream-terminal receipt. `outcome.state` can be ungraded, accepted, rejected, inconclusive, failed or cancelled. A nonnull score binds metric, value in basis points, reviewer, rubric digest and evaluation-receipt digest. Only authorized evaluator receipts finalize scores; workers cannot grade themselves into acceptance.
8. **Cost:** nullable estimated and billed integer micro-USD, currency, coverage and receipt hash. Known zero is distinct from missing. Total input tokens include cache tokens exactly once; retries have separate physical attempt receipts. Aggregate logical-span usage is not added again to physical attempt usage. Currency conversion, price tables and ledger reservations are versioned outside the envelope.
9. **Content handles:** independent prompt and response salted commitments, algorithm, representation, completeness and tier. These are the envelope's prompt/response hashes. Unsalted raw prompt or response hashes stay private to avoid dictionary and cross-run correlation attacks. Public tool commitments follow the same rule.
10. **Disclosure and market permit:** envelope/content tiers, policy ID, hints, permitted builders, release state, earliest reveal bound, eligibility, opportunity ID, source rebate floor and permit digest. Eligibility requires authenticated authorization, not merely `eligible=true` in producer JSON.
11. **Integrity:** record digest, previous event digest and optional Ed25519 signature. Unsigned imports are valid observational examples but cannot enter a paid live auction.

`source` explicitly records adapter, live/import/synthetic mode, scope attribution method and native versus generated IDs. In these historical examples, native span/step/run/agent identity is unknown. New random IDs describe imported observations and are not claimed to be original provider IDs. The import stream's hash chain proves its publication order only, not historical causality or original result priority.

### 2.2 Content layer

Content is stored separately from public envelopes, under opaque event/slot references. The owner-local record retains original bytes, representation, a fresh nonce, raw byte digest, provenance receipt and local approval state. None of its filesystem path, credentials, nonce or raw digest is a public hint by default.

Logical slots are prompt, response, tool arguments and tool result. Native instrumentation should distinguish messages, system instructions, tool definitions and returned artifacts so one approval does not reveal unrelated context. Existing pool records are much coarser: their request string can include an entire conversation and their response collector can omit non-text structure. The adapter therefore commits the exact **stored representation**, never advertises a full replayable model transcript and leaves tool calls unknown.

The public content schema in this release only admits **omission projections**. It deliberately cannot encode arbitrary supposedly redacted text. An approved richer public content export needs a separate versioned export profile, explicit review and a fresh commitment to the redacted bytes. It must not pretend that redacted content opens the original raw commitment.

### 2.3 OTel mapping and deliberate departures

This profile references the GenAI semantic conventions at commit [`e07f4ebacb08f56db8c4c882d117720333fbca04`](https://github.com/open-telemetry/semantic-conventions-genai/tree/e07f4ebacb08f56db8c4c882d117720333fbca04). The fetched documentation marks them **Development**. Pin the revision; do not silently follow renamed fields.

- Reuse `gen_ai.operation.name`, `gen_ai.provider.name`, `gen_ai.request.model`, `gen_ai.response.model`, `gen_ai.agent.id`, `gen_ai.request.stream`, `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`, `gen_ai.usage.cache_read.input_tokens`, `gen_ai.usage.cache_write.input_tokens` and `error.type` where their semantics hold.
- An inference span is normally `CLIENT`; in-process operations can be `INTERNAL`. Agent/tool operations use `invoke_agent`, `invoke_workflow`, `plan` and `execute_tool` rather than inventing provider calls.
- OTel logical GenAI spans include automatic retries. Keep that logical span and record physical attempts as child/linked application events, not duplicate logical usage charges. A pool legacy row with unknown retry ancestry remains one imported snapshot.
- Anthropic's raw `input_tokens` excludes cache-read/cache-write categories. The adapter sums the three observed categories for OTel total input; it emits no total if a required category is unknown. It does not add cached tokens twice.
- Pool `ttfb_ms` measures first received byte, not necessarily the first semantic content chunk. It stays an application field; it is **not** mislabeled `gen_ai.response.time_to_first_chunk`.
- Do not manufacture `gen_ai.conversation.id` from a UUID or content hash. Missing native conversation IDs are omitted. Public agent IDs are approved registry aliases, not leaked provider account IDs.
- OTel input/output messages, system instructions, tool definitions, arguments, raw error descriptions and server addresses are excluded from this public profile, even where OTel makes capture opt-in. Content policy overrides telemetry convenience.
- Step ordering, disclosure commitments, research outcomes, spend receipts, author credit, auction permits and rebates are **Swarm extensions**, not standard OTel attributes. The JSONL envelope is an application exchange format, not an OTLP message. An OTLP exporter must translate it, omit null attributes and keep application extensions in a dedicated `swarm.*` namespace.

Sources: [GenAI client spans](https://github.com/open-telemetry/semantic-conventions-genai/blob/e07f4ebacb08f56db8c4c882d117720333fbca04/docs/gen-ai/gen-ai-spans.md), [agent spans](https://github.com/open-telemetry/semantic-conventions-genai/blob/e07f4ebacb08f56db8c4c882d117720333fbca04/docs/gen-ai/gen-ai-agent-spans.md).

### 2.4 Canonical bytes, hashes and signatures

**SLJ-1 wire canonicalization:** ASCII JSON keys/strings, booleans, null, arrays and integers with absolute value at most `2^53-1`; recursively sort object keys, compact separators, no insignificant whitespace. Floats, duplicate keys, non-ASCII envelope strings and nonfinite numbers are forbidden. Non-ASCII source content remains arbitrary UTF-8 bytes in the private layer. This restricted profile is explicit; it does not claim to implement all RFC 8785/JCS.

A record hash is:

```text
SHA256("swarm-record/0.2.0" || 0x00 || SLJ1(record excluding integrity.record_hash and integrity.signature))
```

The previous-event hash remains in the preimage. In live mode, the producer signs `"swarm-signature/0.2.0" || 0x00 || raw_record_hash_bytes` with Ed25519. A registry binds the public key to producer/principal, permitted roles, validity window and revocation history. The relay validates the signature and permit; a signature proves origin, not scientific truth. Signature verification and the registry are not implemented in the offline selector.

Content commitment for each slot is:

```text
SHA256("swarm-content/0.2.0/<slot>" || 0x00 || nonce_32_bytes || uint64be(byte_length) || exact_content_bytes)
```

Fresh cryptographic nonces are generated per content slot and remain private. This is a commitment, **not encryption** and not evidence of authorship or truth by itself. Encrypt local raw storage separately if needed. A commitment to clipped stored text cannot establish the uncaptured original. The relay's signed append-only receipt establishes when it saw the commitment; a source-controlled clock does not.

A decoder must reject duplicate keys before dictionary conversion and validate schema, canonicalization, graph invariants, hashes, signature, authorization and disclosure policy as separate checks. JSON Schema cannot prove identity, authorization, timestamp truth, semantic redaction or scientific correctness. The schema permits hashes/signatures structurally; the reference prototype verifies record hashes but does not claim live signature authentication.

## 3. Disclosure tiers and release rules

### Private

Raw messages, tool arguments/results, model outputs, source paths, exact identities/timing where sensitive, provider headers, nonce receipts and source hashes stay on the owner machine. Ingesting a private trace does not make its envelope public automatically. A mixed main session or pool label is not a research consent boundary.

### Sealed

Publish only a sanitized envelope plus salted commitments and approved hints. Content remains local. `reveal_not_before` is an embargo lower bound, **not a timer that grants consent**. Passing the timestamp never opens a commitment automatically. Owners can withhold forever, cancel prospective opportunity permits or reveal only to a named evaluator under separate authorization.

An owner-local executor may test a permitted candidate against sealed data without sending raw data to a builder/searcher. The executor returns a bounded, independently checked receipt. Prevent queries that exfiltrate sealed information through scores, timing, errors or repeated adaptive probes: fixed task interfaces, query quotas, delayed/coarsened receipts and no arbitrary code with secret access. The prototype does not execute candidates against sealed content.

### Public

Public envelopes are a derived allowlisted projection, not arbitrary producer JSON. A public content release, when authorized, is a separate redacted artifact with its own digest, owner approval and provenance to the original commitment. Revealing original raw bytes and nonce requires explicit approval covering every affected person's data. Redacting a result does not produce a valid opening of the original hash; an authorized local verifier can attest the relationship without publishing the raw opening.

Raw commitments can remain sealed while a separate approved result artifact is published for backrunning. `release_state=owner-authorized-public` means that the *specifically referenced released artifact/hints* are available; it is not permission to fetch the original prompt. This prototype has no raw reveal/export command.

**Public default is conditional:** after explicit cohort enrollment and owner review, the envelope is public and content sealed. Sensitive metadata is removed, coarsened or kept private. Exact model timing, costs, graph links and even a task label can disclose an unreleased research direction. Originators may choose commitment-only hints or a delayed batch. No bidder may widen the source's hints or builder set.

**Withdrawal:** stop future use and payment eligibility prospectively; append a withdrawal event rather than editing history. Existing public copies cannot be reliably recalled. Deleting a Git branch does not delete everyone else's clone. Rotate a disclosed credential rather than relying on redaction after publication.

## 4. Bundle contract

A bundle contains:

- searcher and enrolled principal IDs, opportunity ID, source event IDs and exact source hashes;
- ordered body entries with action IDs, operation classes, dependencies, pinned artifact/code digests and failure policy;
- a minimum/maximum controller epoch and exact task version, plus `after_release` for result backruns;
- read/write sets for conflict detection, approved builder intersection, compute/call/spend/time caps and constrained capabilities;
- a metric/rubric hash and baseline artifact hash fixed by the controller, a **claimed** gain that never establishes value, and requested service bounty;
- source-originator/searcher/builder/evaluator sharing terms, and an independently funded OFA bid if applicable;
- a unique nonce, record digest and live signature.

No inline shell command is executable authority. Code/brief artifacts are retrieved only by an approved controller from reviewed content-addressed storage, verified against the pinned digest and run with narrowly scoped mounts/capabilities. The live controller validates resource authorization independently of the bundle's requested cap. The v0.2 reference schema intentionally limits capabilities to offline/no-network/no-paid-calls/no-raw-publication and isolated candidate writes.

Bundles use two-phase commit/reveal for their own proposal details in a live auction: searchers submit a nonce-salted bundle commitment during the bid window, then reveal to authorized builder/evaluator parties after cutoff. Revealing a bundle never reveals the originator's sealed content. The worked example's nonce is public because it is an offline demonstration, not a protected live bid. No public description should expose proprietary candidate details before the applicable cutoff.

## 5. Ordering, inclusion and PBS

The controller, not an agent timestamp, assigns epochs and authenticated receive sequence numbers. An epoch is a bounded planning round, not an Ethereum block. The following order is normative:

1. Freeze the opportunity, originator permit, task/artifact version, metric, rubric, budget and release conditions. Obtain a signed relay receipt before accepting bids.
2. Accept authenticated searcher commitments under per-principal quotas. After cutoff, reveal and validate bids. Pin the accepted bid set before disclosing competitor details.
3. Filter for valid permissions, source hashes, inclusion window, funding, resource caps, released dependencies, evaluator independence and code safety. Invalid candidates do not buy admission by paying more.
4. Builders schedule only topologically valid work: origin event before dependent step; published/released artifact before a backrun; prerequisite check before promotion; review before settlement. Critical repairs use a separately authorized repair lane and may pause future work, not rewrite the producer's completed history.
5. Detect read/write conflicts and stale task versions. At most one accepted write to a mutable task version can commit; independent read-only reviews can coexist. Multi-bundle plans specify conflicts and a rollback/publication policy before running. Source sequence alone does not impose unrelated global execution order.
6. The proposer selects a valid builder plan using the frozen value rule. Builders cannot assign themselves as independent reviewers, mutate the task or increase its budget. All builders get the same admitted public hint stream unless the originator explicitly chooses a narrower permitted set.
7. Atomically reserve the assignment/lease and budget. Execute in isolation, retain failure receipts, then recheck versions and predicates at publication. Abort publication on invalid prerequisites; report already consumed resources. Exactly-once assignment does not imply exactly-once network dispatch.
8. Finalize only after an independent review and challenge window. A cancellation, version change or newly invalid source invalidates pending inclusion and unsettled claims. It does not erase observations.

For a one-slot opportunity, the offline reference selector filters then ranks positive controller value; equal values break by committed bundle ID. This is a transparent demonstration, not a fair permissionless tie-breaker: a live system must commit a post-cutoff unpredictable tie-break seed and cap grinding per principal. A production multi-bundle builder proposes a feasible plan under the DAG, resource and conflict constraints; this prototype does not solve that combinatorial allocation problem.

Completeness receipts include accepted and rejected bundle IDs/reasons, assignment attempts, consumed cost and missing outcomes. Audit receipts for censorship and denied opportunities. No claim of permissionless neutrality is made for the hackathon's allowlisted principal registry and single offline builder.

## 6. Valuation, credit and settlement

### 6.1 Quality first, with an independent counterfactual

Do not rank by self-reported gain, tokens, commits, trace volume, paid tips or the number of approving agent aliases. The opportunity controller fixes the question, baseline, evaluation task roots, rubric, practical useful margin, budget and review policy before bidding. Candidates cannot choose their own denominator or easier task.

An evaluator independent of the producer, searcher and builder recomputes quality on pinned artifacts. Bids can be valued through either:

- **measured intervention:** paired candidate-minus-baseline accepted research quality at the same allowed resources, with privacy/integrity and false-claim guardrails;
- **verified service:** a prepriced review/replication bounty paid for independently accepted work, including a sound refutation or null result. Passing review is evidence of service completion, not necessarily a causal score improvement.

A review must bind rubric, task-root set, baseline/candidate output hashes, actual resource coverage, measured scores, reviewer conflict status and verdict. Scientific quality can be ternary/inconclusive; the standardized 0..10000 representation is a transport scale, not a license to collapse uncertainty. Preserve estimates, uncertainty and exclusions in the signed evaluation artifact. A valid adverse scientific result can have high artifact quality.

The toy selector uses `value = frozen_gain_value * verified_gain / 10000 - requested_bounty`, under strict zero-execution-cost constraints. This is controller willingness to fund a demonstration, not a discovery of market price. A live value rule must include measured or conservative expected execution/evaluation cost, uncertainty, opportunity cost and risk, with frozen weights. Unknown costs cannot be silently zeroed. Pay no gain bounty when the comparison is unqualified or inconclusive.

### 6.2 Two distinct funding flows

**Sponsor-funded improvement/service bounty:** reserve an actual sponsor budget. After accepted delivery, allocate the contracted bounty among originator, searcher, builder and evaluator. The trace author receives credit/revenue for useful authorized evidence; the searcher receives credit/revenue for the accepted addition. An evaluator's compensation should be fixed for a valid review regardless of pass/fail, rather than contingent on endorsing the bidder. The toy split illustrates roles only; production uses an independently reserved reviewer fee so a failed bid still pays for honest review.

**Funded OFA proceeds:** if a searcher separately pays for inclusion/access to an authorized opportunity, collect its bid from escrow and rebate the agreed share to the trace originator; the remaining permitted share can compensate the proposer/builder. This is the OFA-rebate mechanism. Do not call a sponsor's payment an OFA rebate or count the same dollar as both bid proceeds and a bounty. The originator's minimum rebate and builder restrictions follow the orderflow through composition. Flashbots' documented percentages are not inherited automatically; our source permit sets its own terms.

For example, a separately funded 100,000 micro-USD bid with a 90/10 originator/proposer rule transfers 90,000 and 10,000 micro-USD from that escrow. That is distinct from the $1 sponsor bounty in the demo, whose OFA bid is zero.

### 6.3 Accounting rules

- Track attribution credit and money in separate append-only ledgers. Originator attribution is not a claim that every tracing proxy owns the result. Principal-signed provenance determines the claimant.
- `reserved -> executed -> reviewed -> challenge_pending -> settled` is the payment lifecycle. Failed execution still consumes real cost, while an unearned bounty is released. Disputes freeze unfinalized settlement.
- Every money movement has a unique settlement ID binding opportunity, source digests, bundle digest, review digest and version. An idempotent compare-and-set prevents duplicate payment. Use integer micro-USD and a conserving largest-remainder split with a fixed tie rule.
- Debits equal credits; no payer budget may go negative. Reserve maximum authorized payout before work, reconcile actual execution cost separately, and never mint money from score points.
- Multiple originators require a pre-agreed, signed allocation of the originator share. Adding copied source events cannot increase the total bounty. Backrun chains get a finite depth and fixed total rebate cap, not recursively minted rewards.
- Related-party maintenance is not an external discovery bounty. Detect shared principals and repeated source/task roots. Do not pay an actor to deliberately manufacture defects and have its alias fix them.

The reference code computes a **hypothetical** split and hard-codes actual settled value to zero. It has no wallet, payment credentials or network path.

## 7. Abuse model and controls

### Frontrunning an unreleased result

A salted commitment plus authenticated receipt establishes prior possession of particular bytes at receipt time, not scientific originality. Sealed hints must not reveal the conclusion. Proposals to backrun require an owner-authorized result release and the exact released artifact reference. Publication before that release is rejected even if it would score well. A bidder cannot disable the ordering rule by setting `after_release=false` on a backrun kind. A generic `fix` label is not an escape hatch: the controller checks the action's semantics and allowed read/write scope. Outcome-dependent work against sealed content runs only within the owner's approved local verifier, if authorized at all.

Independent simultaneous research is not theft merely because it resembles another result. Resolve priority disputes with content commitments, source rights, timestamp receipts and a human reviewer. Private hints can still leak timing or direction, so support delayed/coarsened hints. No cryptographic mechanism can claw back information already published.

### Sybil searchers and collusion

For the hackathon, bind each key/agent to an allowlisted researcher principal. Apply quotas, deposits if authorized, reputation and funding limits per principal, not per agent ID. One principal gets no extra review votes, bundle quota or source credit by spawning agents. Separate author/searcher/builder/evaluator roles and record conflicts, including same-owner models. A monetary bond deters spam but does not prove independent identity or good research. Future permissionless enrollment needs a separate Sybil-resistant design; it is not solved by this schema.

### Poisoned traces, spoofed scores and prompt injection

Treat every body, hint and proposed artifact as untrusted data. No trace instruction becomes a system instruction. Verify producer/owner authorization, signature, exact hashes, allowed enums/identifiers, task scope, size limits, source permissions and body schema. Quarantine malformed records without executing them. Unknown usage/status stays unknown. A signature proves who supplied poisoned data, not that it is true. Reproduce claimed effects from pinned public evidence or an approved local verifier; score receipts come only from a separate evaluator key. Human stop/approval boundaries cannot be optimized away.

### Score gaming, replay and denial of service

Freeze independent task roots, budgets, baseline and metric before bidding; never let searchers rewrite them. Retain all assigned attempts and failed qualifications. Cap candidate attempts, review queries and source reuse. Use unseen task roots and do not tune on evaluated cases. Count correct nulls and refutations as valid findings. Replay protection keys include protocol/chain domain, event ID, principal, opportunity and nonce. Repeated transport attempts have their own usage receipts. Stream deduplication is exact by authenticated event identity, not by identical prompt text. Bound record size, dependency fanout/depth, artifact size, epoch lifetime and outstanding escrow. Rejected unauthorized/poisoned bundles incur no execution.

### Builder/proposer capture

Use signed acceptance/rejection receipts, originator-selected builder lists, consistent hint distribution and challenge/audit paths. Builders cannot see hidden evaluation labels; proposers cannot settle without the independent receipt. Multiple builders can propose plans, but multi-builder execution still needs a single controller reservation to prevent duplicate work. The hackathon implementation is centralized and procedural outside the offline checks; it does not claim a trustless relay or fair exchange.

## 8. Mapping to existing Swarm Lab infrastructure

Keep this as a sidecar first. Do not change active experiment semantics.

- **Agentops hub events:** adapt `plan/start/progress/metric/artifact/done/fail` from `docs/REPORTING.md`. Store the protocol envelope in an approved artifact or namespaced event `data`, with hub run ID as `run_id` and hub `source` as an approved agent mapping. `done` is execution state, not scientific acceptance. The current public proxy does not expose arbitrary artifacts/events, so this requires a future explicitly approved allowlisted projection, not exposing the entire hub or team token.
- **`tasks/`:** controller-created assignment/claim and task version represent the proposer queue. Bundle selection proposes a new owned task or versioned change; it does not let a searcher steal an existing claim. `claims/` in agentops are server reservations, not task or scientific ownership.
- **Pre-run assessments and preregistrations:** bind opportunity/task/metric/rubric/source hashes before execution using the existing [run-review cycle](../../../../tooling/agent-experiments/RUN-REVIEW.md). Same-owner waivers are recorded and cannot become independent receipts by renaming an agent.
- **Reviews:** exact artifact/source commits plus reviewer identity feed evaluation receipts. A review pass with fixes, failed qualification and valid null are different labels. Builders are not their own reviewers.
- **Experiment journals:** preserve native call/start/terminal IDs and tool events where available. Adapt without relabeling active runs; legacy unknowns stay null. The [existing toolkit](../../../../tooling/agent-experiments/README.md) keeps its schemas; protocol adapters record source schema/version.
- **Spend ledger:** retain `results/spend-ledger.json` or owner-native billing records as expense evidence. Add separate reservation, bounty/OFA escrow and settlement journals only under explicit authorization. Do not mistake reported token-price estimates for billed money or gateway calls for direct OpenRouter coverage.
- **Pool-meter:** a source adapter only. The shared gateway label is not the lane ID. Instrument new research calls with exact run/span/attempt IDs and opt-in scope in an owner-approved change; do not backfill imaginary joins.
- **Agentops `scripts/traces.py`:** reuse its approved Claude Code/Codex cohort manifests and human review process. This public sidecar consumes only approved metadata/artifact links. Raw mixed OpenClaw/pool content remains local under the stricter export rule.

## 9. RSI is a family of searchers

The trace-backed improvement loop becomes several bounded searcher roles:

1. **Observability searcher:** detects missing terminal receipts, ambiguous joins, invalid status/usage handling; proposes a capture fix and regression bundle.
2. **Review searcher:** backruns a released artifact with independent evidence checks and counterexamples. It is not independent if it shares the author's principal.
3. **Replication searcher:** proposes a preregistered reproduction or fresh-task test against an accepted result.
4. **Brief searcher:** converts recurring development defects into a small checklist/prompt diff, evaluated against the frozen baseline on fresh task roots.
5. **Routing searcher:** proposes a better allocation of already authorized tasks. Compare on a fixed task queue so it cannot win merely by skipping hard tasks.
6. **Hypothesis searcher:** proposes a successor experiment with decision value and falsifiers, not a paid launch or a claim of truth.

The builder assembles compatible candidates; the proposer owns assignments; the evaluator owns outcomes. Development trace access is narrower than evaluation truth access. Searchers may bid useful work but cannot alter their own metric, grant themselves more compute, publish raw traces or deploy their own winning policy. Every rejected candidate and negative result remains in the record. A successful bundle earns evidence-backed attribution and, if funded/authorized, payment; only a separately authorized policy-decision receipt promotes a worker brief.

The earlier [R0 replay](../rsi-loop/REPLAY-PLAN.md) remains an engineering result: observed nonzero-status capture improved from 0/40 to 40/40 on four saved lanes. It is not a research-effect estimate. The bundle demo below is a different, synthetic contract illustration and must not be pooled with R0 as additional empirical evidence.

## 10. Minimal working example

### 10.1 Three real pool lines, safely converted

A local selection script matched the **entire approved research task** from the prior review lane inside a structured pool request's user message. This is stronger than keyword/time matching but still only a content-based task-scope assertion, not proof of exact native session or call identity. It selected three intact October 4 request records. Source files, line positions, source digests, task-text digest and nonce receipts stay local.

The converted examples preserve allowed model/usage/latency/HTTP metadata. They use minute-rounded observation times, salted prompt/response commitments, unknown served model/tool calls/billing/research score, null native lineage and generated import IDs. Each source record was HTTP 200; all remain **ungraded**. Collected response text is not a full tool-call/SSE transcript. No raw text, excerpt, tool argument, account identity, private path, request header, plain prompt hash or nonce is in the public artifacts.

They are historically imported and unsigned, so they cannot claim live opportunity priority or trigger real payments. Their publication hash chain provides tamper detection for the derived export only. Public readers can validate envelopes and hashes; original-byte verification requires an authorized local reviewer with the private receipts.

### 10.2 Worked bundle

The first real public envelope shows missing billing and unknown tool capture. Searcher `searcher-metadata` proposes an **envelope-only fix**, not a backrun of the sealed scientific result: preserve unknown billing/tool fields as null instead of making them look like known zero/empty values.

- Two ordered actions: check a typed metadata contract, then propose the constrained fix. Neither reads source content.
- Four **synthetic developer-authored** contract cases: unknown cost, known zero cost, unknown tools, known-empty tools. A naive baseline passes 2/4; the candidate passes 4/4. This is not independent evaluation of research quality or a measured pool-service patch.
- The offline evaluator supplies 5000 baseline and 10000 candidate basis points; the searcher's claimed gain is ignored.
- A competing bundle claiming a larger gain fails the fixture review and is rejected. A sealed-result backrun, changed rubric, stale epoch, unauthorized builder, principal duplicate or paid-call request is rejected by separate tests.
- The illustrative controller values a full-scale contract improvement at $4 and the 50-point improvement at $2; a requested $1 bounty leaves $1 of notional controller value. **No economic benefit was observed or monetized.**
- Hypothetical $1 allocation: trace originator $0.20, searcher $0.60, builder $0.10, evaluator $0.10. The funded OFA bid is zero. **Actual settlement: $0.00.** Production evaluator payment must be independently reserved and verdict-neutral, as described above.

The example proves that real sanitized envelopes can feed a typed bundle proposal and deterministic guarded offline selection. It does not prove a live auction, independent evaluation, profitable MEV or improved science.

Run from the repository root:

```sh
python3 researchers/shadow/notes/rsi/test_protocol.py
python3 researchers/shadow/notes/rsi/demo.py
```

Validation uses `jsonschema` (already installed in the development environment); the other code is Python stdlib. No paid/network calls occur. To regenerate the schema:

```sh
python3 researchers/shadow/notes/rsi/build_schema.py
```

Authorized operators can use `pool_to_spec.py --selection ... --approved-session ... --private-receipts ... --output ...` with **local-only** input paths. It refuses to put nonce receipts inside the repository or public output. No global pool scan/export command is exposed. The selection helper, raw selected records and nonce receipts are intentionally not committed.

## 11. Before a real deployment

Minimum remaining work, each requiring owner approval:

1. Register principals/roles and producer keys; build signed append-only relay receipts, authenticated permit/release/withdrawal messages and duplicate-key-safe ingestion. Keep private data out of the relay.
2. Isolate workers/searchers from evaluator labels and controller credentials. Implement narrow owner-local evaluation interfaces for sealed data; arbitrary bundle code must never read private traces.
3. Add exact research run/span/attempt capture, authorized public hub projection and task-version reservation. Pilot with zero-spend diagnostic opportunities first.
4. Freeze reviewer-owned fresh research task roots, rubric and baseline before testing any brief/routing bundle. Report quality, missingness, cost coverage and nulls.
5. Only if explicitly desired, implement funded escrow, conserved settlement, dispute handling and originator contracts. A repository specification does not authorize payments.

Stop at the offline demo if these boundaries cannot be enforced before submission. This branch is a proposed interface and demonstrator, not a change to production capture or team economics.

## References and terminology boundaries

- [Flashbots MEV-Share introduction](https://docs.flashbots.net/flashbots-mev-share/introduction): selective hints, partial bundles, orderflow auctions and originator rebates. The described node accepts backruns; our next-step/fix/routing proposals are a **workflow extension**, not a claim about supported MEV-Share transaction types.
- [Flashbots bundle semantics](https://docs.flashbots.net/flashbots-mev-share/searchers/understanding-bundles): inclusion windows, ordered bodies, privacy hints, refunds and builder-set intersection. This specification is not `mev_sendBundle` compatible.
- [MEV-Boost/PBS overview](https://docs.flashbots.net/flashbots-mev-boost/introduction): builders assemble plans, proposers select them. Our centralized workflow controller is not an Ethereum validator.
- [Trace-backed RSI design](../rsi-loop/DESIGN.md), [candidate brief](../rsi-loop/BRIEF-v1.md), [existing run-review cycle](../../../../tooling/agent-experiments/RUN-REVIEW.md).
