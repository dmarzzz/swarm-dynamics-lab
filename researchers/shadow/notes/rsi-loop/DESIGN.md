# Trace-backed improvement for the research swarm

**Decision:** improve the lab's research procedure, not its ability to produce more confident prose. Start with short versioned worker briefs and executable preflight checks. Learn from actual failed work, test a candidate against an unchanged baseline on fresh assignments, and let a separate reviewer decide whether it is better. No weight training, unrestricted self-modification or automatic spending.

**Status, 2026-10-04:** an offline, privacy-minimized collector and one trace-observability repair are implemented here. The collector normalized ten explicitly selected research sessions. A frozen four-lane replay improved recognition of explicit nonzero command exits from **0/40 to 40/40**, with **0/702** new flags on clean zero exits. This is a real improvement to the measurement pipeline, **not evidence that the research agents became better researchers**. No model calls, paid or otherwise, were launched by these scripts. Independent research evaluation and policy promotion remain blocked.

## 1. What we actually have

The inspection used swarm-lab source `6e116dce` initially, then refreshed main. All references below describe the inspected snapshots, not live guarantees.

- **OpenClaw lane transcripts are the best starting point.** They retain user briefs, assistant messages, tool arguments/results, usage metadata and lane-local order. The export here projects *only typed numeric metadata* from ten explicitly approved hackathon lanes: 1,902 assistant messages, 1,962 tool-result observations, 1,246 explicit exit-status observations and seven compaction events. We do not export prompts, arguments, results, local paths, session IDs or error text. An assistant message is not necessarily one physical provider call; a tool-result observation is not necessarily a unique command.
- **Pool traces exist**, including October 3-4 files, but the observed gateway label does not identify a particular research lane. Requests and responses are strings clipped at **200 x 1024 characters per field**, not a 200k-token context limit. They have usage/status/latency, but no reliable run/span join key. Main conversations and unrelated work are mixed in. We do not keyword-search their bodies into a public dataset or assign them to lanes by timestamp proximity. None are exported here.
- **Codex proxy capture is incomplete, not necessarily absent everywhere.** `codex-proxy.js` logs status, token totals and elapsed time, but has no durable transcript sink. The pool service *does* have a pooled Codex trace path, so traffic routed through it may be captured. Direct proxy traffic lacks that path. Verify the route before saying all Astra calls are lost. OpenClaw sessions can still retain the assistant/tool transcript regardless of provider. Our ten-lane export is not an Astra coverage census.
- **Direct experiment calls bypass gateway traces.** Capture-memory's model adapter maintains a usage/spend ledger, but those totals alone cannot reconstruct per-call causal order, request/response associations, failure classes or retries. Hub events and run artifacts are useful evidence, not a substitute for a unified call journal. Other experiment packages may already have richer journals; reuse them rather than modifying active harnesses.
- **Public artifacts already supply research labels, if independently adjudicated.** The [discussion benchmark review](../review-discussion-benchmark-v3.md) found a quorum-scoring defect and a dropped failure reason. The [next-experiments plan](../../../dmarz/notes/next-experiments-2026-10-04/README.md) distinguishes failed qualification, valid adverse results and unrun successors. The [existing run-review cycle](../../../../tooling/agent-experiments/RUN-REVIEW.md) already says plan, freeze, execute, reconcile, repair, qualify. This design makes that cycle learn across tasks; it does not replace it.
- **dmarz's trace collector landed during this work.** Agentops commit [`35abdc1`](https://github.com/dmarzzz/swarm-labs-agentops/commit/35abdc1) adds `scripts/traces.py` and `docs/TRACES.md`, collecting Claude Code and Codex rollouts to `traces/<handle>` branches with sanitization and human review. On refresh to `87790d1`, no remote `traces/*` heads were advertised. The collector code being present does not mean anyone's traces were uploaded. It does not yet cover OpenClaw. We have not run that collector on mixed private sessions or fetched anyone's transcript payloads.

Library slop pass rates, commit volume and test counts are diagnostics, not interchangeable measurements of research quality. The selected session sample is not all lab activity. Historical task outcomes are development evidence, not an unbiased treatment effect.

## 2. Capture three layers, with a privacy boundary

### Layer A: private source evidence

Owners retain raw transcripts and provider bodies on their own machines. Access is explicit and limited to the research cohort. Never send mixed main-session or pool bodies to the improvement agent. Do not assume a secret regex removes personal material or third-party DMs. Do not export hidden reasoning or global instruction/memory attachments.

Our implementation uses a local explicit file manifest, not automatic inclusion by a `swarm-` prefix. Approved sources are snapshotted locally; source hashes and the alias-to-session mapping stay private. Output is an allowlisted projection of counts, enumerated model/provider categories and numeric usage. Unknown strings become `other`; content and tool names are never copied. A regex scan is defense in depth, not the privacy boundary.

Raw local snapshots are 0600 in a 0700 directory. Keep them only for the agreed verification window, then have the owner decide retention/deletion. Public derived artifacts contain no recoverable private source identifiers. A Git branch deletion is not guaranteed erasure from clones, caches or hosted retention; never use that promise to justify uploading sensitive material.

### Layer B: normalized research trace

One `study_id` groups a study; `task_root_id` groups genuinely independent tasks; `run_id` is a specific assigned attempt; `span_id` is a logical model/tool call; `attempt_id` identifies each physical dispatch. Assign these **before execution**. Child lanes get explicit `parent_run_id`, not an inferred parent based on overlapping timestamps.

The event envelope proposed for v1 is:

```json
{
  "schema_version": "research-trace/1.0",
  "event_id": "public-event-0001",
  "study_id": "rsi-review-checklist",
  "task_root_id": "root-017",
  "run_id": "assignment-017-candidate",
  "parent_run_id": null,
  "span_id": "call-004",
  "parent_span_id": null,
  "attempt_id": "attempt-001",
  "seq": 12,
  "event_type": "call_terminal",
  "actor_role": "research-worker",
  "source_type": "experiment-journal",
  "status": "failed",
  "error_class": "provider_rate_limit",
  "dispatched": true,
  "usage": {"input": 120, "output": null, "cost_usd": null},
  "coverage": {"usage": "partial", "body": "omitted", "join": "exact"},
  "artifact_ref": null,
  "source_commit": "EXAMPLE_NOT_A_REAL_COMMIT",
  "brief_sha256": "EXAMPLE_NOT_A_REAL_HASH",
  "manifest_sha256": "EXAMPLE_NOT_A_REAL_HASH"
}
```

This is an illustrative future envelope, not a fabricated observed event. In production, validate hash/ID formats and reject arbitrary free-text payloads at the export boundary.

Required event types: assignment, run_start, model/tool call_start, call_terminal, artifact_produced, review_received, run_terminal, lesson_proposed and policy_decision. Review and policy-decision records come only from the reviewer/controller, not the worker. Use source-native IDs locally for exact joins and approved opaque IDs publicly. Preserve requested and served model, provider revision if supplied, prompt/brief version, source/scorer/assignment hashes, resource regime, UTC times and durations in the private normalized layer. Public time precision and identifiers require owner approval.

- Terminal outcomes distinguish completed, failed, timeout, cancelled, not_started and unknown. A success-looking final message is not a grade.
- Every retry has a new attempt ID; idempotent ingestion keys off owner/source/event ID. Never deduplicate by matching prompt text. A retry can spend real money.
- Unknown usage/cost stays null, with observed-count coverage. Do not add provider and gateway totals for the same span. Prefer the provider receipt as billing evidence and the gateway as a cross-check. Cache tokens, estimated cost and billed cost stay separate.
- Every assignment gets a terminal reconciliation entry, including never-started and missing-result cases. Late corrections are appended with `supersedes`, never silent rewrites.
- A hash chain detects accidental mutation but does not stop its writer recomputing the chain. Anchor assignment and artifact digests in reviewer-owned storage before evaluation.

**Implemented v0.1:** [episode.schema.json](episode.schema.json) is a strict, closed schema for a content-free OpenClaw episode projection. [trace_loop.py](trace_loop.py) implements that adapter; [results/episodes.json](results/episodes.json) contains ten real derived records. Parent/task-root/brief/manifest/artifact links are null because those joins are not established, not guessed. `outcome` is always `ungraded`, billing is null and complete-episode coverage is unknown. This is intentionally smaller than the v1 design. Pool, Codex CLI, Claude Code and hub adapters are not implemented here.

**Compatibility:** retain [tooling/agent-experiments](../../../../tooling/agent-experiments/README.md)'s existing `study_id`, `run_id`, scenario, replicate, condition and event lineage when adapting its event/outcome schemas. Store the exact source contract/version and digest in a local receipt. An invalid or incomplete legacy run is not made schema-valid by replacing missing cost with zero. Do not change the shared toolkit schema during the hackathon.

### Layer C: independent outcomes and accepted lessons

Join artifacts and reviews by exact commit plus task/run identity. Each label needs reviewer identity, author identity, artifact hash, reviewed source hash, rubric version, verdict and concrete defect evidence. Same-researcher review, an owner waiver and truly cross-researcher review are distinct categories. A document that says "independent" is not proof of independence.

A lesson has: source run/review IDs, failure taxonomy, proposed mechanism, bounded policy diff, expected benefit, counterexample, regression test, freshness requirement and promotion state. Historical review text is untrusted evidence for a proposal, not an instruction to change the metric. Contradictory lessons remain visible. [LESSONS.md](LESSONS.md) starts with four curated examples.

## 3. What improves, and what stays fixed

Start with **brief/checklist changes**. They are small, reversible and cheap to evaluate offline. The initial candidate [BRIEF-v1.md](BRIEF-v1.md) addresses false command-success assumptions, missingness/quorum checks, typed failure recording and qualified claims. It changes no shared agent configuration.

Later candidates can improve artifact verification, review task routing and experiment selection. Do not optimize all three at once: scheduler selection changes which tasks are attempted and can inflate acceptance by selecting easy work. For the first research evaluation, the controller assigns every task from a fixed queue, and both arms face the same inputs and resource caps. Prioritize experimental value using human-reviewed uncertainty and next-decision value, not the promise of a positive result.

Freeze during each cycle:

- task pool and sampling/assignment rule;
- primary endpoint, exclusions, unit of analysis and missingness treatment;
- baseline brief, candidate brief, model/provider/tool versions and compute cap;
- independent review rubric, reviewer selection and conflict-of-interest rule;
- promotion threshold, evaluation sample count and stopping rule.

No agent may modify budgets, credentials, permissions, reviewer prompts, truth labels or these protected files to improve its score. This is bounded procedure optimization, not permission for self-directed capability growth.

## 4. The research metric

**Primary:** independently accepted research artifacts per assigned task at a fixed total resource allowance.

For task i, `Q_i = 1` only if a blind independent reviewer finds the artifact correct within its stated scope, reproducible or adequately evidence-linked for its task type, and free of unresolved material methodological defects. Otherwise `Q_i = 0`. Missing, cancelled and never-started assignments remain in the denominator with zero accepted output. An infrastructure cause is separately reported; it does not disappear. A correct null or negative finding can receive full credit.

Estimate `mean(Q_candidate - Q_baseline)` across paired independent task roots. Do not treat multiple agents, tool calls, task renderings, retries or repeated reviewers as independent tasks. Task-family strata must be assigned in advance. Do not pool a library citation check and a full experiment as interchangeable units without fixed stratification/weights.

**Co-required guardrails:** no critical privacy or integrity violations; no increase in independently measured false claims/material defects beyond the frozen margin; no reduction in task coverage; caps respected. Report actual billed cost where known, estimated cost separately, wall time, number of artifacts independently checked and reviewer disagreement. The initial replay has no adequate billing data, so it cannot support an efficiency claim.

**Secondary:** first-pass acceptance, verified defect recall and false alarms on reviewer-authored seeded audits, repeat-defect rate, cost per accepted artifact, and avoidable human repair turns. Human approval/access/safety decisions are a separate category, not a nuisance objective. Never reward bypassing them. Fewer human turns is valuable only at matched task quality and oversight requirements.

**Before-Sunday research pilot, proposed not run:** the controller chooses twelve fresh task roots across at least three task families, pairs baseline/candidate work on identical frozen evidence, randomizes execution order and output labels, and allows one attempt per arm under equal caps. Replays must be offline on saved or synthetic public evidence for this task's authorization. Twelve pairs are a feasibility pilot, not evidence of broad improvement. Publish all pairs and a paired interval or exact randomization analysis only if the assignment design justifies it. Call uncertainty inconclusive. A confirmatory sample size and practical margin require a separate independent precision plan, not picking a threshold after seeing these twelve results.

**Promotion:** pilot results permit, at most, an explicitly labeled human-approved canary. Full promotion requires an independently frozen larger test whose lower confidence bound exceeds the predeclared useful margin and whose safety/quality guardrails pass. If no independent reviewer or genuinely fresh task set is available before the deadline, ship the collector and replay, with the research-effect claim still unproven.

## 5. Anti-gaming and enforcement

Four roles, different write access:

1. **Curator:** gets approved development projections and public outcomes. Proposes lessons and a brief diff. Cannot access evaluation task answers or the review store.
2. **Worker:** gets one assigned task, frozen public evidence and one brief. Writes only its output directory. No repo-push credentials, no writable evaluator mount, no peer outputs or reviewer state.
3. **Evaluator:** a different researcher/account owns task truth, blind grading, final reconciliation and signed verdicts. Fresh cases are outside the worker's filesystem and context. It cannot retrospectively alter the preregistered endpoint without invalidating the cycle.
4. **Controller/human:** freezes the assignment before dispatch, controls budgets, reserves run IDs, verifies exact artifact hashes and reviewer identity, and alone promotes or rolls back the policy.

**Concrete minimum enforcement for the next real cycle:** workers run in isolated processes/containers with read-only brief/task input, writable run output, no evaluation directory and no repository push credential. The reviewer stores the task key, rubric and frozen manifest in a separate account/worktree outside the worker mount. Publish a timestamped digest before dispatch; the evaluator signs a receipt binding the manifest, both brief hashes, output hashes and rubric. Only a controller with an evaluator public key and separate deployment credential can apply an approved candidate. Pin expected hashes rather than trusting filenames or a worker's `passed=true`. Human retains stop authority.

**Current limitation:** these controls are a deployment requirement, not something a shared writable Git repository or this document magically enforces. Existing lab agents often share a Unix account and repository credentials. A "reviewer agent" under that same authority is not a security boundary. We did not change those credentials or deploy isolation. This implementation never auto-promotes anything; R0 explicitly writes `scientific_promotion: blocked-no-independent-evaluation`.

Other protections:

- Development and evaluation split by root/family/time, not by rows of one transcript. Once inspected for tuning, an evaluation root becomes development material forever.
- Independently derive labels; rerunning the author's scorer is reproducibility, not independent correctness. Reviewers get the artifact/evidence, not the worker's confidence pitch or treatment label.
- Include healthy controls, missingness, valid adverse outcomes and abstention costs. Don't reward all-block/all-abstain policies.
- Freeze a modest candidate budget. Log every candidate and rejected/failed cycle; no best-of-many score shopping. Keep baseline and shadow-mode rollback available.
- Label manipulation attempts and privacy events separately; do not minimize them into an average quality score.
- Signed records prove who wrote a verdict, not that it is correct. Use cross-researcher audit and disagreement resolution for material claims.

## 6. The one implemented loop

1. **Collect:** explicitly selected research-session metadata. No pool bodies exported.
2. **Diagnose:** the slop-audit development lane had seven nonzero process exits but zero wrapper errors. The naive wrapper-only detector misses command statuses.
3. **Freeze:** [REPLAY-PLAN.md](REPLAY-PLAN.md) was pushed as commit `d16dc8a6` before the four evaluation-session snapshots were inspected for this endpoint. Development examples had already been inspected and are disclosed.
4. **Change:** B1 adds a typed nonzero-exit detector and preserves B0's wrapper flags. L0 becomes a brief/checklist instruction with counterexamples. This is a manually curated improvement, not autonomous lesson mining.
5. **Next run:** execute the offline normalizer on four different saved lanes, with no new model run. B0 recognizes 0/40 explicit nonzero status observations; B1 recognizes 40/40. Neither flags the 702 clean zero observations; the one wrapper error is retained.
6. **Report, do not overclaim:** all four lanes are included. No research-defect labels, success claims, confidence intervals or dollars-saved estimate are inferred from shell exit statuses. The evaluator was written by the developer, so the result is a parser-contract test, not independent research evaluation. The new brief has not been tested on a subsequent agent task.

Public [histograms](results/replay-input.json) are sufficient to recompute this narrow endpoint without raw transcripts. [Saved result](results/replay-result.json) pins the parser's source hash. Ten episode records validate against the strict schema. Unit tests cover content exclusion, incomplete lines, malformed records, unknown usage, boolean/string exit statuses, duplicate inputs and secret scanning.

From the repository root:

```sh
python3 researchers/shadow/notes/rsi-loop/test_trace_loop.py
python3 researchers/shadow/notes/rsi-loop/demo.py
```

The second command uses only checked-in derived histograms. For an authorized local extraction:

```sh
python3 researchers/shadow/notes/rsi-loop/trace_loop.py --manifest /absolute/private/approved-manifest.json --output /absolute/private/derived-output
```

See the script docstring for the local manifest shape. Never commit that manifest or a raw snapshot. Inspect derived outputs before publication. The current extractor is a parser/projection, not a redactor for arbitrary text exports.

## 7. Build and operate before Sunday 5pm PT

**Done now:** verified inventory; local scoped capture; strict episode schema; normalized real metadata; frozen offline replay; content-free reproduction; lessons and candidate brief. Everything is confined to this owned directory and private local working files.

**Next, owner-approved, no shared harness mutation required:**

- Shadow approves exact research lanes for export and a retention window. dmarz/Vishesh use their existing consent/review workflow for their own sources.
- Curator imports sanitized manifests and public review metadata. Keep source-native transcripts local. Add stable task/run/artifact mappings before adding more body data.
- A different researcher selects fresh public offline tasks and owns the grading key. Freeze the twelve-pair feasibility plan, exact rubric, assignments and resource cap. Use the existing run-review templates.
- Run baseline/candidate in read-only isolated workspaces; save every output and final reconciliation. Evaluate blind; show quality/cost/coverage and uncertainty, even if the candidate loses.
- Human decides whether a bounded canary is justified. Until then, do not advertise research improvement or change live agent instructions.

If time is short, the submission demo is two commands plus the observed trace gap and repaired measurement. A complete honest measurement loop is more credible than calling a pile of transcripts RSI.

## 8. Three capture fixes, proposed only

1. **Correlate at dispatch.** In OpenClaw's research-lane call wrapper, allocate `run_id`, `span_id` and `attempt_id` before each dispatch, and attach an allowlisted `x-swarm-run-id`, `x-swarm-span-id`, `x-swarm-attempt-id` plus W3C `traceparent` where supported. At the pool ingress, record these IDs as metadata and strip unneeded headers before external forwarding. Emit request/response original lengths and truncation booleans before clipping. Add explicit run start/end receipts. Without exact IDs, leave old pool calls unjoined. Do not add raw prompt capture or derive scope from a client-supplied label alone; require an operator-approved research scope.
2. **Close the direct Codex path.** Either route sanctioned research Astra calls through the already instrumented pool path after confirming API compatibility, or add a scoped append-only metadata sink in `codex-proxy.js`: IDs, requested/served model, dispatch start/terminal state, status/error enum, usage completeness, latency and retry attempt. Metadata only, 0600 files, explicit research opt-in; no headers, keys, URLs, prompt bodies or raw error text. Count transport retries separately. No service changes were made here.
3. **Journal direct experiment calls and join team runs.** In the next *owner-approved harness version*, write a start receipt before dispatch and a terminal receipt on success/error/cancellation for each OpenRouter call. Link model usage to the immutable assignment and experiment/run/artifact IDs already on the hub. Preserve a vetted `public_reason`/error enum, dispatch uncertainty and all retries. Record partial stream/disconnect and missing usage explicitly. Reconcile started/terminal/unknown against the spend ledger. Do not silently retrofit an active experiment or relabel old aggregate costs as per-call traces.

## 9. What to ask dmarz and Vishesh to push

The collector is already shipped in agentops; do not ask them to build another one. Ask for **one completed, owner-reviewed research cohort** on `traces/<handle>` using their `docs/TRACES.md` process, plus:

- filled `SETUP.md` and manifest with the machine/harness version, session-parent map and explicit included/excluded scope;
- a small join file mapping opaque session/lane IDs to swarm-lab task IDs, run IDs, experiment IDs, artifact commits and brief/prompt hashes;
- failed and cancelled sessions as well as successful ones, model/usage coverage, truncation/redaction counts and which user turns were actual decisions versus repair nudges;
- exact public preregistration and independent review references, with author/reviewer identities and source hashes; preserve waived/same-owner review as such;
- consent for the particular sanitized research content and an export review. No personal instructions, credentials, hidden reasoning, unrelated projects or raw mixed sessions.

Their richer sanitized transcripts should remain access-controlled source evidence. The public RSI package only needs metadata projections, artifact links, accepted lessons and the frozen evaluation receipts. For Shadow's OpenClaw/pool sources, this stricter content-free export remains the rule, regardless of what another collector can sanitize.
