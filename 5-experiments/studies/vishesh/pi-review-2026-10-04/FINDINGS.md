# PI findings and recommendations

57 findings from the two original frozen audit snapshots. Later study designs and evidence are reviewed separately in [the scientific review](SCIENTIFIC-REVIEW.md). These are internal PI-style assessments, not formal cross-researcher gate approvals.

## GUIDE-001 P1 Bring launch instructions and contracts into compliance with required public registration

**Project:** agent-experiment-guide

**Impact:** Following the original documented command would launch unregistered worlds under the current owner requirement. This is a present launch-process gap; the historical demonstration explicitly disclaims LLM preregistration, and the reviewed artifacts do not establish when the owner requirement applied to that execution.

**Recommendation:** Before any new Swarm Lab run, publish and verify the readable plan, register its immutable URL and condition-specific question/treatment/comparator/metrics/limitations TLDR, and fail closed through the existing project preflight or equivalent. Separate read-only validation from fresh execution. Keep historical compliance and execution results separate; do not retroactively call a plan preregistered.

**Status:** documentation partially addressed in this review; executable gate remains absent

**Evidence:**

- `agent-experiment-guide/GUIDE.md:60`: Original step 7 allowed a local immutable protocol or registry when authorized; no mandatory public-plan registration.
- `agent-experiment-guide/scripts/toy_harness.py:103`: run() validates only toy configuration and immediately creates output and schedule; no public-plan/TLDR gate.
- `agent-experiment-guide/scripts/validate.py:101`: Default validator launches two complete 960-world executions.
- `agent-experiment-guide/templates/run-config.json:4`: Only protocol_sha256 is present; no immutable public URL, condition-specific TLDR or verified registration receipt.

## AV-01 P1 Avalon can still launch every condition without the required public design registration

**Project:** avalon-swarm

**Impact:** Future launches violate the owner's explicit requirement. Existing JSON plans establish assignments, but cannot establish public preregistration; no saved immutable-plan receipt exists in these run folders.

**Recommendation:** Use the existing small public-plan helper (after fixing REG-01), require condition-specific registered descriptions, and fail before any world initialization. Mark historical registration status unknown/not evidenced separately from the 45 completed executions; do not relabel them as preregistered.

**Status:** Open recommendation

**Evidence:**

- `avalon-swarm/benchmark.py:496`: CLI proceeds directly to directory creation, config plan, and measure(); it has no public_plan import, immutable plan URL, run TLDR, registration receipt, or preflight.
- `avalon-swarm/README.md:13`: The documented runnable commands launch unregistered worlds.

## AV-02 P1 Interrupted or invalid-action runs have no terminal assignment ledger and freeze provenance too late

**Project:** avalon-swarm

**Impact:** A partial future study can lack both source identity and terminal failure counts, inviting survivor-only reporting and making exact reconstruction harder. Current45 archived outcomes are complete and source hashes match.

**Recommendation:** Freeze code/config/agent-spec and environment metadata before world initialization. Wrap each assigned world in a small terminal-outcome recorder for completed, failed, timeout, canceled and not_run; record reason and preserve partial event-chain tail. Keep execution failure separate from consensus benchmark failure.

**Status:** Open recommendation

**Evidence:**

- `avalon-swarm/benchmark.py:523`: Assignments are saved before execution, but source.sha256 is written only after every world finishes.
- `avalon-swarm/benchmark.py:525`: measure() exceptions propagate out of the sweep with no failed/not_run outcome for the remaining assignments.
- `avalon-swarm/PROTOCOL.md:79`: The limitations acknowledge incomplete plans on invalid actions; this is an implemented gap rather than an undisclosed historical failure.

## EP-01 P1 Validate the entire response before committing agent memory

**Project:** immune-response-review

**Impact:** A syntactically malformed coordinator response can alter private state and remain validity.ok=true / execution_qualified=true. A direct isolated scorer probe returning valid choices plus plan=[] was accepted and cleared memory; no model calls or episodes were run. Structured provider output reduces likelihood but does not replace local validation.

**Recommendation:** Validate the full role-specific schema and semantic domains before any memory mutation. Keep a valid but wrong integer plan as a scientific failure; classify malformed keys/types/actions as response-contract failure with old memory preserved. Add one malformed coordinator regression and one valid-wrong-answer regression.

**Status:** Open recommendation

**Evidence:**

- `https://github.com/dmarzzz/swarm-lab/blob/e3c40b027313ccc6985f36fa63bab6ff221cc1c1/researchers/vishesh/notes/immune-response-v3/src/immune.py:94`: act() validates only choices, then mutates memory; it does not validate the coordinator plan, constraints, action or extra fields.
- `https://github.com/dmarzzz/swarm-lab/blob/e3c40b027313ccc6985f36fa63bab6ff221cc1c1/researchers/vishesh/notes/immune-response-v3/src/immune.py:227`: Validity is determined from exceptions/failed slots; malformed coordinator plans handled as zero utility are not counted as response failures.
- `immune-response-review/AGENT-SPEC.md:11`: The specification promises atomic choice validation, but broader native acceptance requires zero malformed outputs.

## EP-05 P1 Make public-plan verification unavoidable at the execution boundary

**Project:** immune-response-review

**Impact:** The core launcher can bypass the owner-required public plan gate if invoked directly; receipts are absent from the engineering export. This establishes a bypass and unverified process compliance, not proof that the historical engineering execution was unregistered. Its 720 scripted execution outcomes remain valid as recorded engineering evidence.

**Recommendation:** Require an already-verified plan receipt at execute() before policy creation and bind it to protocol/source hashes. Route every public named run through that same check; keep ordinary unit/scorer tests separately labeled. Record process_compliance independently from execution_qualified, and label any later public plan retrospective.

**Status:** Open recommendation

**Evidence:**

- `https://github.com/dmarzzz/swarm-lab/blob/e3c40b027313ccc6985f36fa63bab6ff221cc1c1/researchers/vishesh/notes/immune-response-v3/src/runner.py:10`: The pinned execution function directly creates a scripted/native policy with no public-plan receipt or allocation preflight.
- `https://github.com/dmarzzz/swarm-lab/blob/e3c40b027313ccc6985f36fa63bab6ff221cc1c1/researchers/vishesh/notes/immune-response-v3/src/runner.py:48`: A direct native-repair CLI path exists.
- `immune-response-review/README.md:46`: Later documentation describes a gated hub wrapper, but the wrapper is not in this exported evidence bundle.

## REG-01 P1 Preflight validates a page shape, not registration of the actual planned worlds

**Project:** regrowth-200

**Impact:** A retrospective page or unrelated immutable page can authorize a new altered experiment, while individual worlds still lack the required condition-specific account of question/treatment/comparator/metrics/limits. This is not evidence that the existing numeric pilot was modified.

**Recommendation:** Keep a compact plan schema with experiment/version, prospective/retrospective status, protocol hash, assignment IDs, required per-assignment TLDR fields, and endpoints/limits. Validate those exact assignments before launch and attach their receipt to every terminal record. Rendered public-page verification should be a recorded publication step, not inferred from raw Markdown fetch.

**Status:** Open recommendation

**Evidence:**

- `regrowth-200/src/public_plan.py:5`: validate() checks URL shape, TLDR prefix, 40-character run text, and five nonempty headings; it requires no limitations section, condition assignments, execution hash, plan classification, or protocol identity.
- `regrowth-200/src/run.py:65`: One receipt is checked before assignments are constructed; the same run_tldr authorizes all six arm×damage worlds.
- `review-2026-10-04/regrowth-avalon-review.json:1`: Offline validation accepted headings containing only x and a run TLDR of forty x characters.

## REG-02 P1 Laya provider failures bypass the documented three-error stop rule

**Project:** regrowth-200

**Impact:** A broken hybrid head can be silently converted into persistent WAIT actions while the experiment appears to exercise the intended model. Provider malfunction is mixed with policy behavior.

**Recommendation:** Track provider-specific failure streaks and terminal causes, including qualification. Separate invalid model choices, provider errors and defaults; halt according to the frozen rule. Cache successful decisions or explicitly label cached failure defaults. Add the isolated failure-injection regression test; no live model test is necessary.

**Status:** Open recommendation

**Evidence:**

- `regrowth-200/src/run.py:35`: Qwen success resets the single error counter; Laya exceptions at line42 increment invalid but never the failure streak.
- `review-2026-10-04/regrowth-runner-faults.json:1`: Dummy-policy unit injection produced20 consecutive Laya ConnectionErrors without provider_failure_streak; execution stopped only at a synthetic wall deadline.

## REG-03 P1 Claimed hard resource bounds are not enforced per dispatch

**Project:** regrowth-200

**Impact:** A future run can exceed the promised call/wall limits. The Qwen expression calls+len(jobs) also counts already-started jobs twice and may stop early; failures during dispatch leave already-submitted calls without event receipts.

**Recommendation:** Reserve each call in a single synchronized ledger before dispatch, pass remaining deadline to each request, stop/cancel pending work on exhaustion, and write an attempted-call receipt even when the round aborts. A few functions and unit fault tests suffice; no scheduler service is needed.

**Status:** Open recommendation

**Evidence:**

- `regrowth-200/src/run.py:19`: Wall and Laya budgets are checked only at round boundaries; a round can dispatch199 Qwen calls, whose90-second request timeout is independent of remaining pilot time.
- `regrowth-200/src/run.py:41`: Every sentinel is allowed to call Laya without a remaining-cap reservation.
- `regrowth-200/src/models.py:12`: Qwen timeout is fixed90s; ThreadPoolExecutor waits for submitted work when leaving its context.
- `review-2026-10-04/regrowth-runner-faults.json:1`: Starting the dummy Laya counter at3999 executes20 calls and fails at4019, overshooting the4000 cap by19.

## REG-04 P1 Publisher reuses historical pilot-v4 run IDs for any output directory

**Project:** regrowth-200

**Impact:** Publishing a later experiment through this helper can replace artifacts/progress attached to the original six pilot records, contradicting historical preservation and making provenance ambiguous.

**Recommendation:** Derive immutable run IDs from a manifest run ID, require a matching manifest digest when resuming, and refuse writes to a completed record with different source/input hashes. Build and validate a sanitized publication payload locally before upload. Do not run the existing publisher on new results.

**Status:** Open recommendation

**Evidence:**

- `regrowth-200/src/publish_hub.py:4`: The command accepts an arbitrary output directory.
- `regrowth-200/src/publish_hub.py:21`: Every uploaded world is named regrowth-200/pilot-v4-<world.id>.
- `regrowth-200/src/publish_hub.py:23`: Existing IDs are reopened and artifacts/progress are written even when the existing run is already done.

## EP-02 P1 Bind the actual runtime model configuration to the qualified agent

**Project:** swarm-of-theseus

**Impact:** Changing SWARM_MODEL_CONFIG_FILE can change model, context/output limits or pricing while the manifest still declares the qualified pinned agent. There is no evidence that the archived runs did this; the launcher permits it and undermines reliable repeatable spin-up.

**Recommendation:** Resolve the approved config once, compare its canonical hash to qualification, pass that object directly into the provider, and write that same hash/config into the manifest. Record served model when available and reject unapproved routing changes. Apply the same pattern to immune v3, whose config is also environment-selected.

**Status:** Open recommendation

**Evidence:**

- `https://github.com/dmarzzz/swarm-lab/blob/a773ff5410442fcf351cfc817550b3fc92a88994/researchers/vishesh/notes/swarm-of-theseus/src/provider.py:23`: Provider loads an arbitrary environment-selected config.
- `https://github.com/dmarzzz/swarm-lab/blob/a773ff5410442fcf351cfc817550b3fc92a88994/researchers/vishesh/notes/swarm-of-theseus/src/runner.py:41`: Manifest hardcodes the declared model and hashes ROOT/model-config.json rather than the actual resolved provider config.
- `https://github.com/dmarzzz/swarm-lab/blob/a773ff5410442fcf351cfc817550b3fc92a88994/researchers/vishesh/notes/swarm-of-theseus/src/runner.py:26`: S1 checks local study/provider/model-config hashes, which do not constrain a different environment-selected config file.

## EP-03 P1 Reporting failures can invalidate valid numerical runs

**Project:** swarm-of-theseus

**Impact:** A temporary image dependency, disk/report error or hub outage can change the reported scientific denominator and stop other terminal records from being written, despite completed decisions. This contradicts the documented separation between rendering failure and numerical evidence.

**Recommendation:** Write numeric events/outcomes first. Catch and record rendering/upload/progress failures separately as reporting_status; retry publication from recorded traces, never model decisions. Ensure each submitted assignment gets a terminal execution record even if reporting fails. A fake failing reporter is a meaningful regression test.

**Status:** Open recommendation

**Evidence:**

- `https://github.com/dmarzzz/swarm-lab/blob/a773ff5410442fcf351cfc817550b3fc92a88994/researchers/vishesh/notes/swarm-of-theseus/src/runner.py:56`: Rendering and hub progress/artifact uploads execute synchronously inside the event callback called by run_world.
- `https://github.com/dmarzzz/swarm-lab/blob/a773ff5410442fcf351cfc817550b3fc92a88994/researchers/vishesh/notes/swarm-of-theseus/src/runner.py:63`: An exception from that callback is caught as failed experimental execution; later final rendering/upload exceptions can escape the worker and prevent aggregate completion.
- `https://github.com/dmarzzz/swarm-lab/blob/e3c40b027313ccc6985f36fa63bab6ff221cc1c1/researchers/vishesh/notes/immune-response-v3/src/runner.py:25`: The immune progress callback is likewise inside scientific execution; a callback failure can replace the entire task/world batch with zero-utility error outcomes.

## GUIDE-002 P2 The default validator does not audit the retained evidence or verify the package/source inventory

**Project:** agent-experiment-guide

**Impact:** Saved evidence or code can diverge while the advertised command still passes its new-run tests. An audit-only command is also needed to avoid treating validation as an unregistered launch. All 30 original inventory entries and five source entries do match in this audit; this finding is a detection gap, not observed corruption.

**Recommendation:** Add a read-only mode that verifies retained output, exact manifest membership and every source/package hash, then performs semantic reconciliation. Keep rerun/reproducibility tests as a separate explicit registered execution mode. Disposable-copy probe changing source_sha256 to all zeroes was accepted by the current verifier.

**Status:** open

**Evidence:**

- `agent-experiment-guide/scripts/validate.py:75`: main() merely parses *.json files and only calls verify_output for freshly generated temporary directories at lines 103-105. Retained events.jsonl/outcomes.jsonl are not parsed here.
- `agent-experiment-guide/scripts/validate.py:26`: verify_output only checks the output_sha256 entries supplied by the manifest; it never checks source_sha256 or requires a complete inventory.
- `agent-experiment-guide/VALIDATION.md:17`: Package manifest is described as local integrity checking, but the documented validation command never enforces it.

## GUIDE-003 P2 Reconcile the planned cell and terminal ledger against actual outcomes

**Project:** agent-experiment-guide

**Impact:** Ledger mismatches can survive validation and inflate completed denominators. Mutation tests accepted a planned condition changed to an unknown condition and an outcome marked failed with decisions=999 while run_end retained completed/5. Current saved outputs are consistent.

**Recommendation:** Construct the expected scenario × replicate × condition keys from the frozen config; require exactly one unit per key, join planned metadata to outcomes/events, and reconcile terminal status and counts. Count completions by status while keeping failed/unscored assigned units visible.

**Status:** open

**Evidence:**

- `agent-experiment-guide/scripts/validate.py:29`: Only the set of planned run IDs and total outcome count are compared; planned scenario/condition metadata are not joined field by field.
- `agent-experiment-guide/scripts/validate.py:65`: Outcome provider usage is checked, but outcome status/decisions are not reconciled with run_end; all required condition cells are not enforced independently of summarize().
- `agent-experiment-guide/scripts/toy_harness.py:91`: completed_runs is len(outcomes), regardless of terminal status if externally supplied outcomes contain failures.

## GUIDE-004 P2 Bind event semantics and scoring truth to the initialized world

**Project:** agent-experiment-guide

**Impact:** A self-consistent but wrong evaluator truth or identity/routing bug can pass the hash and score checks. Rehashing a copy with swapped evaluation truth and coherent changed scores, or all decision agent IDs set to a0, was accepted. These probes target missing invariants, not cryptographic forgery; the retained original traces passed a stronger independent check.

**Recommendation:** Compare evaluator truth to the frozen initialized world; require each agent exactly once; validate observed source values and permitted topology; enforce binary actions and event order; independently recompute final endpoints. Keep event hash integrity and scientific semantic validity separate.

**Status:** open

**Evidence:**

- `agent-experiment-guide/scripts/validate.py:55`: Initialization is checked only by its hash; the reconstructed world truth is not compared with evaluation.truth.
- `agent-experiment-guide/scripts/validate.py:57`: Actions are a value list, so five decisions with the same agent_id pass; binary domains, unique agent coverage, event alternation and observation-to-decision binding are not checked.
- `agent-experiment-guide/scripts/validate.py:66`: Only no_communication source visibility is checked in saved traces; ring/global topology, source values and policy consistency are not independently validated.
- `agent-experiment-guide/schemas/event.schema.json:52`: Event payload is an unconstrained object; semantic invariants therefore need explicit validation.

## GUIDE-005 P2 A one-resample configuration can emit a zero-width 95 percent interval

**Project:** agent-experiment-guide

**Impact:** The advertised configurable toy can produce a falsely precise interval labeled 95 percent for a valid schema input. The saved 2000-resample configuration is unaffected.

**Recommendation:** Prespecify a sensible supported resample count and reject inadequate values for interval reporting, or explicitly disable CIs when too few resamples are requested. Freeze the quantile convention and describe Monte Carlo resolution separately from inferential coverage.

**Status:** open

**Evidence:**

- `agent-experiment-guide/schemas/toy-config.schema.json:67`: bootstrap_samples accepts every integer >=1.
- `agent-experiment-guide/scripts/toy_harness.py:78`: The percentile interval indexes one resampled vector without guarding statistical adequacy; at bootstrap_samples=1 both bounds equal the single bootstrap draw.

## GUIDE-006 P2 Complete operational identity with an observed initialization receipt before live use

**Project:** agent-experiment-guide

**Impact:** The same template IDs do not establish that each instance received the same intended policy, inputs, tools and memory. This is an acknowledged extension gap in the illustrative package, rather than a claim that the toy already offers production identity guarantees.

**Recommendation:** Keep the existing three specifications, add a versioned initialization receipt and ledger extension with loaded hashes, requested/returned model metadata, context assembly, actual delivered observations, memory snapshot/namespace/reset facts, effective permissions, role/order assignments and lifecycle lineage. Distinguish frozen specification, fresh state and repeatable output.

**Status:** conceptual remedy authored in AGENT-LIFECYCLE.md; implementation remains intentionally absent

**Evidence:**

- `agent-experiment-guide/templates/agent-definition.json:5`: The template records requested model and policy but has no observed returned model/snapshot record or fully assembled per-agent context.
- `agent-experiment-guide/templates/context-access.json:21`: Visibility and retrieval manifests describe allowed access; delivered content, ordering, token truncation and actual permission checks are not recorded.
- `agent-experiment-guide/templates/run-config.json:13`: Fresh-world reset is prose; no run-level namespace proof, inherited state receipt or checkpoint/fork dependency record is represented.

## AV-03 P2 Discussion randomness changes later decisions even when beliefs are unchanged

**Project:** avalon-swarm

**Impact:** Audit/repair and topology comparisons include changes to tie-breaking random streams caused by memory length. This is a legitimate total intervention effect, but a tiny mission-success change cannot be attributed specifically to improved belief correction without separating this mechanism; pairing is weaker than scenario_hash equality suggests.

**Recommendation:** Key independent random streams by world, identity, phase, mission and attempt; use deterministic/keyed random priorities for candidate items. Keep this change versioned. Add a unit test that irrelevant memory changes do not perturb proposal tie-breaking randomness when the legal options and scores are identical.

**Status:** Open recommendation

**Evidence:**

- `avalon-swarm/benchmark.py:158`: One mutable RNG is shared by every policy phase.
- `avalon-swarm/benchmark.py:200`: Discussion shuffles a treatment-dependent memory candidate list.
- `avalon-swarm/benchmark.py:210`: Proposals shuffle with the same RNG; random votes and assassination also consume it.
- `review-2026-10-04/regrowth-avalon-review.json:1`: Isolated policy test: deleting one audited contradiction leaves all beliefs equal, but after discuss() the RNG states and next tied proposals differ.

## AV-04 P2 Topology comparisons change access to task-relevant evidence, degree and RNG behavior together

**Project:** avalon-swarm

**Impact:** Federated versus local estimates the combined effect of making useful evidence available, increasing communication and changing random-policy trajectories. Local versus none cannot deliver useful initial role evidence under these rules. At random source-role mixture, sent signal correctness is only.6×.8+.4×.2=.56; relays create repetition, not independent corroboration.

**Recommendation:** Present the existing results as a channel-access/mechanics check. For an information-topology claim, hold relevant evidence and delivered budget fixed, compare degree-matched overlays, vary independent source count/reliability and explicitly measure reach, delay, retained evidence and mission utility. Avoid interpreting more claims as more independent evidence.

**Status:** Open recommendation

**Evidence:**

- `avalon-swarm/benchmark.py:282`: Every private signal targets the same seat in the next council; none targets the owner's own council.
- `avalon-swarm/benchmark.py:180`: Belief computation ignores every nonlocal target.
- `avalon-swarm/benchmark.py:329`: Local topology never moves evidence across councils; federated adds two useful cross-council links and increases degree9→11.
- `avalon-swarm/PROTOCOL.md:25`: Each target has only one initial evidence source; adversaries reverse their80%-correct signal.

## AV-05 P2 Consensus gate has a floor effect and measures acquisition failure as well as collapse

**Project:** avalon-swarm

**Impact:** These outcomes validate the mechanics of a chosen threshold, not a general law that swarms collapse. The same label conflates never acquiring knowledge, losing established knowledge and delayed recovery. Class thresholds and finite observer counts create additional asymmetric difficulty.

**Recommendation:** Calibrate on development cases with attainable oracle, unaided, single-agent, Bayesian/exact local and confidently wrong controls. Report continuous truth/agreement coverage and distinguish acquisition latency from loss after a predeclared stable baseline. Freeze thresholds on development seeds; retain the original15 failures unchanged. A post-audit window is a separate registered endpoint, not an after-the-fact rescue.

**Status:** Open recommendation

**Evidence:**

- `avalon-swarm/results/consensus-v02/outcomes.jsonl:1`: All15 conditions fail signal_loss at round5; none passes.
- `avalon-swarm/benchmark.py:176`: Uninformed prior=.4 and one positive.8 signal averages to.6, below confidence=.7 before mission/audit evidence. Provenance does not accumulate repeated signals.
- `avalon-swarm/benchmark.py:90`: Self-exclusion leaves4 observers for ordinary-good targets; ceil(.8×4)=4 requires unanimity, versus4/5 for other targets.
- `avalon-swarm/PROTOCOL.md:85`: The failure clock starts at the first discussion round; it does not require previously achieved truth consensus.

## AV-06 P2 Current recovery evidence is driven by one additional successful mission

**Project:** avalon-swarm

**Impact:** The cautious published prose is appropriate. The table alone can visually overstate a reproducible performance gain, and thousands of claim deliveries must not substitute for five independent worlds.

**Recommendation:** Add the five paired differences beside means and identify one extra mission explicitly. For a confirmatory continuation choose a minimum useful world-level improvement, pilot variance, held-out seed count and paired interval/analysis before launch. Report normalized exposure rate and eligible-source denominators, alongside raw counts. Do not claim significance from five-seed bootstrap behavior.

**Status:** Open recommendation

**Evidence:**

- `avalon-swarm/RESULTS.md:27`: Mean later-mission success is37.3% audit versus38.0% repair.
- `review-2026-10-04/regrowth-avalon-verification.json:1`: Paired repair−audit mission differences across seeds0–4 are0,0,1/30,0,0; the pooled gain is one additional success in150 opportunities. Council win differences averagezero.
- `avalon-swarm/report.py:48`: Report emits treatment means without paired world estimates or uncertainty; eligible-origin denominators remain unavailable.

## AV-07 P2 Deterministic scripted initialization is strong but not yet a reusable real-agent lifecycle

**Project:** avalon-swarm

**Impact:** Identical scripted agents can be recreated today, and all13 tests pass. Replacing policies with LLMs without a frozen spec would introduce uncontrolled context exposure, memory selection, call scheduling and within-run adaptation. The trusted Python object boundary cannot enforce model/tool isolation.

**Recommendation:** Keep the current baseline lightweight. Before model execution add declarative initial agent specs and identity/role assignments; version an observation serializer, context budget/truncation and eviction policy, permitted tools, update/repair rules, allowed phase transitions and event-keyed randomness. Snapshot initial hashes, then log state/context deltas and policy-version changes. Make heterogeneity a preassigned treatment; learned changes must be named interventions. Verify identical initialization without requiring identical stochastic outputs.

**Status:** Open recommendation

**Evidence:**

- `avalon-swarm/benchmark.py:28`: Roles, signals and policies are keyed by SCENARIO_VERSION, seed and identity; source snapshot preserves prior scenario streams.
- `avalon-swarm/benchmark.py:291`: Observation explicitly constrains role knowledge, council membership, inbox, audited labels and mission history.
- `avalon-swarm/benchmark.py:161`: Memory is a32-claim deque whose eviction order follows global sender ordering; context contains no individual vote history.
- `avalon-swarm/ADAPTER.md:7`: Real structured provider adapter, context handling, isolation and cost reservation are described but not implemented.

## EP-06 P2 The local evidence bundle is not yet self-contained

**Project:** cross-project

**Impact:** A reviewer can reconstruct much of the evidence, but cannot reproduce all runs from this checkout. Pilot-03 was actively being copied during review: incomplete export is not an execution failure and cannot establish missing registration. Its aggregate summary is lower-confidence evidence until the export finishes.

**Recommendation:** Complete a small immutable evidence export with the matching manifest, plan receipt, recorded tapes, outcomes and a pinned source archive or exact external source links. Fix local links or replace them with immutable external URLs. Add a single completeness manifest; no new workflow service is needed.

**Status:** partially resolved in late export: Theseus source and complete Healing pilot03 now reviewed; immune reproducibility gaps remain. See dated addendum.

**Evidence:**

- `immune-response-review/README.md:17`: Five local documentation links are missing: design.json, two engineering reviews, VISUALIZATION.md, and historical README. Reproduction commands reference source paths outside this workspace.
- `swarm-of-theseus/RESULTS.md:71`: Local result prose references missing deployment/source materials; pinned external source can be fetched but is not packaged.
- `healing-helping-hands/results/pilot-03/summary.json:1`: Snapshot summary contains 72 completed worlds but 48 lack raw world files; only 61 total world files are present (24 completed/37 not-run). Manifest, plan receipt and call journal are absent.

## ROOT-01 P2 Project cards combine different experiments under one apparent proposal

**Project:** dossier

**Impact:** A reader cannot tell which intervention, outcome and minimum deliverable to execute. Good ideas lose falsifiability when observational discovery and causal testing are presented as one design.

**Recommendation:** Give each card one primary question, unit, manipulation, comparator, endpoint and stop/go criterion. Label any observational precursor or follow-on separately. Use the proposal decisions in this review to select a canonical version; generate all card sections from that one record.

**Status:** open

**Evidence:**

- `dossier-src/original-build.py:58`: Commons tests a publication gate; its later contribution paragraph tests attribution/incentives.
- `dossier-src/research.py:16`: Research overlays add new prospective mechanisms to cards whose original design remains observational; this also affects Memory, Leadership, Culture and Coordination.
- `dossier-src/build.py:12`: Both sets of fields are rendered in one card.

## ADD-H-01 P2 Replay ZIP fails its recorded integrity hash

**Project:** healing-helping-hands

**Impact:** A consumer validating the published bundle against its manifest must reject the archive. Including the manifest inside the archive while the manifest also hashes that archive creates a circular packaging dependency, or preserves a stale prior archive hash. This is a packaging defect, not a numerical-result mismatch.

**Recommendation:** Keep the inner content manifest limited to payload files; build the ZIP afterward; record the archive hash in a separate outer checksum record that is not included inside that ZIP. Rebuild from recorded evidence without rerunning decisions.

**Status:** Open recommendation

**Evidence:**

- `healing-helping-hands/site/artifact-manifest.json:48`: Manifest claims f35fa6e7… for replay.zip; actual archive SHA256 is 7d6514db…. All six ZIP member CRCs pass and each member matches the site counterpart, including artifact-manifest.json itself.

## ADD-H-02 P2 The checked-in renderer cannot reproduce the new Jev site

**Project:** healing-helping-hands

**Impact:** Running the available local renderer on the now-complete pilot-03 export would omit Jev from effects and overwrite the new Jev UI/plots with the older exact-control presentation. The record is externally recoverable via pinned source, but the workspace build is not reproducible.

**Recommendation:** Import the exact matching renderer/template from the recorded source revision or make the renderer data-driven over manifest arms and the predeclared illustrative-pair rule. Record the renderer/template hash and H2 mapping. Verify the rebuilt site against the unchanged 180-world dataset.

**Status:** Open recommendation

**Evidence:**

- `healing-helping-hands/visualization/render.py:21`: Unchanged local renderer enumerates exact/Qwen/Qwen+Qwen/Qwen+Laya, fixes the illustrative pair and plots to exact, and copies the older visualization/index.html.
- `healing-helping-hands/site/data.js:1`: New site contains pilot-03, five arms including Jev, defaultArm=jev and pre-exchange event snapshots.
- `healing-helping-hands/site/artifact-manifest.json:3`: Manifest still labels mapping H1-retrospective-recorded, whereas the frozen pilot-03 plan specifies H2.

## ADD-H-03 P2 Recovery zero now hides a real damage-and-exchange interval

**Project:** healing-helping-hands

**Impact:** The established metric defines zero as first qualifying post-exchange frame at round10, not zero exchanges or no damage. The new telemetry makes that distinction observable. Without a phase label, the recovery number can be mistaken for instantaneous/no-loss recovery. The remaining task perturbation is small: only0.357 percentage points additional integrated atlas error relative to no event.

**Recommendation:** Preserve the historical metric, label it first qualifying recorded round offset, and additionally report event-phase loss plus recovery_exchanges (first exchange=1). Include pre-exchange and post-exchange phase names wherever the recovery result is displayed.

**Status:** Open recommendation

**Evidence:**

- `healing-helping-hands/results/pilot-03/8701-jev-evidence-only-erasure.json:1`: All three erasure-only sharing trajectories report recovery_rounds=0. New snapshots show 40 empty memories, pre-exchange atlas accuracy85%/coverage84%; the first exchange raises atlas accuracy to95% and coverage93–94%.

## EP-09 P2 Memory-erasure controls barely perturb the measured task

**Project:** healing-helping-hands

**Impact:** Those runs demonstrate notice propagation and redundant storage, but cannot support a strong recovery-from-memory-loss claim when the measured task never loses accuracy. The later diagnostic review recognizes this, and partial pilot-03 introduces event_snapshot telemetry, so this is a historical limitation with repair underway.

**Recommendation:** Preserve original outcomes. Require a measurable pre-exchange damage check and report absolute post-erasure loss before recovery speed. Preregister one contiguous erasure block and one irreversible-source-loss negative control; use a small severity sweep only after the basic manipulation has measurable impact.

**Status:** historical limitation preserved; pilot03 now measures immediate erasure, with a small integrated effect. See ADD-H findings.

**Evidence:**

- `https://github.com/dmarzzz/swarm-lab/blob/8be7fece2b16035609fde1d4832c1320aab5f0a0/researchers/vishesh/notes/healing-helping-hands/src/sim.py:51`: Erasure occurs before the same round neighbor exchange, and only the post-exchange state is recorded in pilot-01/02.
- `https://github.com/dmarzzz/swarm-lab/blob/8be7fece2b16035609fde1d4832c1320aab5f0a0/researchers/vishesh/notes/healing-helping-hands/src/corpus.py:22`: Forty scattered identities lose memory after evidence has already spread redundantly.
- `healing-helping-hands/results/pilot-02/summary.json:1`: Across both pilot-01 and pilot-02, all 12 paired sharing-policy comparisons of erasure versus no-event have exactly zero additional integrated atlas error.

## EP-10 P2 Qualification cases are mostly repeated templates, not broad semantic coverage

**Project:** healing-helping-hands

**Impact:** Passing 60/60 shows narrow interface competence, not 60 independent semantic successes or model superiority. Small models repeatedly fail negation/unknown cases; exact/qualifying decisions should not hide this. The current docs mostly state these limits accurately.

**Recommendation:** Freeze a shared small evaluation panel for every candidate, split by linguistic template family rather than method name, and include scope negation, no significant gain, unavailable measurement, contradictory sentences, and changed claims. Report per-family errors and paired case differences. Select one frozen model/interface before downstream comparison.

**Status:** Open recommendation

**Evidence:**

- `https://github.com/dmarzzz/swarm-lab/blob/8be7fece2b16035609fde1d4832c1320aab5f0a0/researchers/vishesh/notes/healing-helping-hands/src/corpus.py:31`: The 60-case pilot-02 screen has four phrasings per label repeated across method names.
- `https://github.com/dmarzzz/swarm-lab/blob/8be7fece2b16035609fde1d4832c1320aab5f0a0/researchers/vishesh/notes/healing-helping-hands/src/jev.py:17`: Jev has five phrasings per class repeated with renamed methods: 15 semantic templates, 60 text instances.
- `healing-helping-hands/results/jev-qualification-01/qualification.json:1`: Jev 60/60 is correctly recorded, but other model screens used different fixtures.

## EP-13 P2 Head blindness should not be described as independent errors

**Project:** healing-helping-hands

**Impact:** The implemented blinding is valuable. It does not by itself make the second head an independent error source, and agreement can replicate systematic misclassification. No heterogeneous-head efficacy estimate exists in pilot-01/02 because Qwen failed qualification; pilot-03 appears to be Jev-only plus exact, not the originally proposed heterogeneous treatment.

**Recommendation:** Use the term blinded second assessment. Preregister conditional error correlation, accuracy among first-head errors, and abstention/cost changes on identical cases. Compare Qwen repeat and heterogeneous head with matched extra call slots while reporting tokens separately. Keep new base-model conditions explicitly separate from the original heterogeneity question.

**Status:** Open recommendation

**Evidence:**

- `https://github.com/dmarzzz/swarm-lab/blob/8be7fece2b16035609fde1d4832c1320aab5f0a0/researchers/vishesh/notes/healing-helping-hands/src/run.py:74`: The repeated Qwen check changes option order/seed on the same report with the same model at temperature zero; both heads are blind to the other answer.
- `https://github.com/dmarzzz/swarm-lab/blob/8be7fece2b16035609fde1d4832c1320aab5f0a0/researchers/vishesh/notes/healing-helping-hands/src/providers.py:25`: Shared deterministic model/weights and highly repeated language do not produce statistically independent error mechanisms.

## ADD-I-01 P2 Finish the redesigned evidence export before claiming independently verified execution provenance

**Project:** immune-response-review

**Impact:** Numeric episode evidence is substantially complete: all five episodes.jsonl provenance hashes can be reproduced from embedded rows. However independent verification of the evaluator, precise initial context, reviewer mechanism, provider usage, amendment equivalence and preregistration remains unavailable within this export. Absence here is not proof that those artifacts or registrations never existed elsewhere.

**Recommendation:** Add the small pinned scenario source/fixture/config/protocol bundle, reviewer/call records, equivalence-check result and public-plan receipts or exact immutable links. Fix renamed local links. Root should reconcile separate local-run-records before drawing any process-compliance conclusion.

**Status:** open

**Evidence:**

- `immune-response-review/SCENARIO-SPEC.md:11`: Links ASSESSMENT.md and EXECUTION.md are absent from the frozen export; assessment is actually exported as SCENARIO-ASSESSMENT.md.
- `immune-response-review/SCENARIO-SPEC.md:74`: SOLO-BASELINE.md is absent, preventing local review of the claimed prospective architecture control.
- `immune-response-review/scenario-native-a2/manifest.json:1`: Includes source/protocol/config hashes and commit but no corresponding source, fixture catalog, frozen protocol bytes, public-plan receipt or provider-call journal in this 38-file delta.
- `immune-response-review/SCENARIO-ASSESSMENT.md:17`: Claims a 48-configuration equivalence check; the check artifact/test source is not included.
- `immune-response-review/SCENARIO-ASSESSMENT.md:30`: Claims about reviewer statements cannot be independently traced because replay rows contain only six commander decisions, not the three reviewer outputs.

## ADD-I-02 P2 Separate proposed deployments, rejected changes and actual damage

**Project:** immune-response-review

**Impact:** A rejected proposal did not modify the deployment. Labels currently conflate policy risk with effective system changes, and unsafe_changes combines several events with different operational meaning. Healthy-tick primary results remain correct.

**Recommendation:** Preserve historical fields; add versioned derived deployment_attempts, rejected_unsafe_attempts, applied_actions, effective_state_changes and harmful_applied_changes. Keep all six customer ticks as the common primary denominator.

**Status:** acknowledged in assessment; derived metric labels not yet corrected

**Evidence:**

- `immune-response-review/SCENARIO-SPEC.md:51`: Metrics list deployment count and unsafe changes; the latter includes safety-gate rejection and executed harm.
- `immune-response-review/scenario-native-a2/replay.html:3`: Embedded data and comparison renderer count every action=deploy as a deployment, even when the result is safety-gate rejection. Across A2, 5 attempted deployments comprise 3 applied actions and 2 rejections.
- `immune-response-review/scenario-native-a1/replay.html:3`: A1 has 32 deployment attempts: 27 applied and 5 rejected. Its 9 unsafe flags mix rejection and applied harmful action.
- `immune-response-review/SCENARIO-ASSESSMENT.md:56`: The assessment already recommends separating harmful proposals, rejected unsafe actions and actual damage.

## ADD-I-03 P2 The qualification gate admits a policy that preserves healthy systems by failing to repair damaged ones

**Project:** immune-response-review

**Impact:** Operationally valid answers and healthy-system restraint do not establish the competence needed to interpret a memory-repair contrast. A wait-dominated policy passes while recovering almost nothing. This is a limitation of the originally chosen gate, not a reason to relabel its observed pass as failure.

**Recommendation:** Keep the historical gate result unchanged, stop escalation, and require both clean damaged-task recovery and healthy-system preservation in the next prespecified gate. Separate model/schema validity, competence, scientific contrast and process compliance.

**Status:** accurately acknowledged; no further launches recommended

**Evidence:**

- `immune-response-review/SCENARIO-SPEC.md:53`: Qualification requires complete/valid execution and no false_alarm regression, but no recovery competence in an uncorrupted damaged control.
- `immune-response-review/SCENARIO-ASSESSMENT.md:21`: A2 is accurately reported as passing this narrow gate.
- `immune-response-review/scenario-native-a2/summary.json:1`: Eight of nine damaged-case episodes end unhealthy; three healthy controls stay healthy. Only reset/migrated_data recovers.
- `immune-response-review/SCENARIO-ASSESSMENT.md:55`: The missing matched damaged, no-misleading-memory baseline is explicitly required for the next study.

## EP-04 P2 Knowledge retention counts obsolete values as desirable

**Project:** immune-response-review

**Impact:** A perfectly updated clean swarm appears to forget useful knowledge. The metric confounds successful revision with damage, and could reward retaining stale copies.

**Recommendation:** Rename the historical field original_value_retention if retained for provenance. Add current_truth_retention and stable_fact_retention excluding facts legitimately updated; evaluate sentinel against current truth or restrict it to unchanged facts. Preserve historical fields and version corrected derived metrics.

**Status:** Open recommendation

**Evidence:**

- `https://github.com/dmarzzz/swarm-lab/blob/e3c40b027313ccc6985f36fa63bab6ff221cc1c1/researchers/vishesh/notes/immune-response-v3/src/immune.py:159`: retained compares every private store with fx[facts], the original truth, even after legitimate round-5 learning and round-18 updates.
- `https://github.com/dmarzzz/swarm-lab/blob/e3c40b027313ccc6985f36fa63bab6ff221cc1c1/researchers/vishesh/notes/immune-response-v3/src/immune.py:160`: Sentinel retention uses the original value even when the sentinel is the legitimate update target.
- `immune-response-review/engineering-v3/replay.html:13`: Recomputed embedded engineering data: all 80 CLEAN outcomes have all eight actors at 12/12 current facts, while retained is 11/12 for 64 and 10/12 for 16; sentinel_retained is zero for 10 CLEAN outcomes.

## ROOT-02 P2 Illustrative numbers look more empirical than the explanation they support

**Project:** influence-guide

**Impact:** The disclaimer is honest, but the strongest visual cues compare different endpoints and invite a remembered efficacy claim. None of these counts is evidence of an observed attack.

**Recommendation:** Use one worked route decision as the main illustration. If aggregate invented counts remain, put the same endpoint on both cards, label every value hypothetical, and avoid their reuse in empirical summaries. The current invented figures should not enter a result table.

**Status:** open

**Evidence:**

- `swarm-influence-guide.html:26`: The guide explicitly labels 1,000 tasks and all aggregate counts hypothetical.
- `swarm-influence-guide.html:28`: Large 95.0% display means target selection, whereas the paired 99.0% display means task accuracy; influenced task accuracy is 38.3% in smaller text.

## REG-05 P2 Advertised certificate validity and actual next-hop reachability are different outcomes

**Project:** regrowth-200

**Impact:** The recorded primary metric is correctly implemented for the protocol, but it cannot by itself establish packet delivery or evacuating200 agents. The visualization may draw a route different from the certificate being scored, obscuring transient loops and recovery semantics.

**Recommendation:** Name the endpoint certificate validity throughout. Add a separately defined next-hop delivery metric (static forwarding or time-varying packet execution, explicitly chosen) and display the actual scored certificate on selection. Preserve original metrics; publish any reanalysis as retrospective.

**Status:** Open recommendation

**Evidence:**

- `regrowth-200/src/world.py:39`: score() checks each stored full path from earlier neighbor states against current topology; it does not follow current next-hop pointers.
- `regrowth-200/site/index.html:20`: The selected route overlay follows current f.next pointers, while the displayed validity and hop count describe the stored advertised certificate.
- `review-2026-10-04/regrowth-avalon-verification.json:1`: Reanalysis found31 disagreement frames:15 algorithm-damage,8 qwen-damage,8 hybrid-damage. At round40, Qwen/hybrid certificate validity=.855 but current next-hop reachability=.97. At algorithm round52 the values are.79 and.975.

## REG-06 P2 Development record misreports Laya qualification for pilot-v2

**Project:** regrowth-200

**Impact:** The narrative is inconsistent with preserved raw evidence and the correction changes the apparent effect of prompt revisions, though it does not change gate failure or any swarm outcome.

**Recommendation:** Correct both documents to Qwen5/10, Laya6/10; retain the original result JSON and add an explicit editorial correction note. Generate qualification tables from archived fixture records.

**Status:** fixed in current prose with dated editorial note; original archived evidence unchanged

**Evidence:**

- `regrowth-200/DEVELOPMENT.md:9`: Table says both models scored5/10.
- `regrowth-200/PROTOCOL.md:39`: V3 amendment says the preceding v2 attempt failed at5/10 Qwen and5/10 Laya.
- `regrowth-200/results/pilot-v2/manifest.json:1`: Stored qualification is Qwen5/10 and Laya6/10; independently rescoring all10 fixture records confirms6 under both strict and any-shortest scoring.

## REG-07 P2 Agent identity, context and reproducible model spin-up need an explicit executable contract

**Project:** regrowth-200

**Impact:** The implementation does provide200 independent controller states, but readers cannot infer200 persistent model contexts, and another machine cannot reliably recreate the inference environment from the commands alone. A fixed seed does not make all serving backends bitwise deterministic.

**Recommendation:** Add one small versioned agent spec naming role, model artifact/digest, provider/runtime, initial prompt/schema bytes and hashes, observation allowlist, state ownership, reset/caching policy, context cap, legal actions, and hybrid assignment. Validate resolved model/dependency metadata before qualification. State199 decision agents plus one fixed exit, shared weights and stateless invocations; test initialization/input hashes separately from stochastic output reproducibility.

**Status:** Open recommendation

**Evidence:**

- `regrowth-200/src/models.py:9`: Qwen receives only a stateless route-length instruction; controller observation cell ID is omitted. There is no conversational history or per-identity model session.
- `regrowth-200/src/models.py:24`: Laya likewise receives route sentences and the Qwen proposal, without identity or history; its revision is pinned.
- `regrowth-200/src/run.py:11`: Identity-specific state is path plus memo; it resets per world. The map is hard-coded, not generated from manifest seed4100.
- `regrowth-200/src/run.py:74`: Qwen metadata records a digest for the mutable qwen3:0.6b alias but does not enforce an expected digest or record Ollama/backend/hardware version.
- `regrowth-200/README.md:17`: Runbook requires an existing Laya source/venv/cache via placeholder paths; there is no dependency lock or self-contained resolution step.

## REG-08 P2 Earlier development source hashes cannot be resolved from the retained project or archive

**Project:** regrowth-200

**Impact:** Failed development outcomes remain inspectable, but exact prior prompt/scorer reconstruction requires another version-control artifact. Hashes prove identity only when the corresponding bytes can be retrieved.

**Recommendation:** Locate any existing Git objects matching these hashes before declaring evidence lost. For future runs save a small source bundle or immutable commit link before execution; keep qualification prompts/scorer version and exact inputs with each attempt. Do not rewrite earlier manifests to current hashes.

**Status:** Open recommendation

**Evidence:**

- `regrowth-200/results/pilot-v1/manifest.json:1`: Protocol/models/runner hashes identify prior bytes but those bytes are absent from the checked project and evidence archive.
- `regrowth-200/results/pilot-v2/manifest.json:1`: The same gap affects pilot-v2, pilot-v3 and pilot-v1-attempt2.
- `review-2026-10-04/regrowth-avalon-verification.json:1`: The v4 source is recoverable exactly from evidence.tar.gz. Archive checksum, member list, and71 members verified; all earlier attempts miss three source snapshots locally.

## REG-09 P2 Report regeneration silently erases hand-maintained publication context

**Project:** regrowth-200

**Impact:** Regenerating the report removes relevant provenance and can carry stale facts into future results.

**Recommendation:** Render only a delimited generated table/metrics block or move immutable narrative into a separate linked note. Generate execution facts from the selected manifest and validation receipts; preserve publication/process-compliance status explicitly.

**Status:** Open recommendation

**Evidence:**

- `regrowth-200/src/analyze.py:12`: The generator replaces the entire RESULTS.md.
- `regrowth-200/RESULTS.md:35`: The publication-boundary section explaining what was uploaded is present in the current report but absent from the generator template.
- `regrowth-200/src/analyze.py:11`: Date-specific test, diagnostic and deployment claims are hard-coded and reused for any input run.

## REG-10 P2 The pilot cannot identify a diversity benefit and its stronger result should be surfaced

**Project:** regrowth-200

**Impact:** The record supports a useful negative engineering finding: this hybrid mechanism did not improve measured endpoints, while the exact local algorithm dominates route quality. It does not establish that heterogeneity helps or never helps.

**Recommendation:** Write this negative finding plainly. Before any new model spending, define a mechanism-specific prediction and choose a task where the model contributes more than numeric argmin. For a routing continuation, use held-out maps/damage locations, randomized attachment assignments, blind Laya and second-Qwen controls, matched damage exposure, recovery-area/route-stretch endpoints, and paired world replicates.

**Status:** Open recommendation

**Evidence:**

- `regrowth-200/results/pilot-v4/summary.json:1`: Qwen and hybrid have identical final validity, shortest fraction, excess hops and recovery; hybrid adds476 world Laya calls across two worlds.
- `review-2026-10-04/regrowth-avalon-verification.json:1`: Only two distinct Laya overrides occur, repeated in control/damage. One chooses a tied nonminimum route; the other chooses33 hops instead of25 while23 is available. Neither corrects to minimum. Validity and optimal-fraction trajectories are identical; excess hops differ transiently by at most.23.
- `regrowth-200/PROTOCOL.md:15`: Attachment cells are fixed, Laya sees Qwen, and additional compute is unmatched; the single map is developmental.

## ROOT-03 P2 Verification contrast in the numeric surrogate bundles checking with aggregation

**Project:** seo-guide

**Impact:** The existing random-versus-focused comparison isolates allocation under the toy assumptions. Discussion-versus-verification cannot identify the causal effect of checking, and the same-source skeptic is identical by construction.

**Recommendation:** Keep the disclosed limitation beside the visible result bars. In a separately planned surrogate revision, add a mean-score no-check control and hold aggregation fixed. Call the skeptic arm a no-new-information control rather than a simulated language-model critic. Preserve the current version as an illustration.

**Status:** open

**Evidence:**

- `seo-guide-src/simulation.js:29`: Discussion produces score vectors, then uses plurality of agent argmax choices.
- `seo-guide-src/simulation.js:32`: Verification changes two candidate scores and selects the group mean argmax.
- `seo-guide-src/body.html:67`: The detailed assumptions already disclose the aggregation confound.

## ROOT-04 P2 Three discussion iterations do not create evolving propagation in the surrogate

**Project:** seo-guide

**Impact:** Up to floating-point roundoff, the first update is the fixed point; rounds two and three repeat the same state. This is a static averaging demonstration, not a simulation of three rounds of evidence exchange.

**Recommendation:** Describe the current mechanism as one mixing update. If temporal diffusion is the hypothesis, specify an explicit local adjacency/update rule and manipulation check in a new plan before changing the simulator. Do not infer cascade depth or discussion convergence from these rounds.

**Status:** open

**Evidence:**

- `seo-guide-src/simulation.js:29`: Every iteration mixes fixed original bad[i] with mean(discussed). The group mean is invariant under this update.

## ROOT-05 P2 The proposed large factorial should follow mechanism qualification

**Project:** seo-guide

**Impact:** The design has thoughtful controls, but that scale consumes integration and inference before the independent-verification mechanism is established. A nominal 1,000 tasks does not determine precision of paired clustered regret differences.

**Recommendation:** Start with focused checks versus random checks under identical aggregation, plus no-check and clean controls needed to interpret them. Qualify the independent measurement channel and freeze the attacker/evaluator split. Use pilot world-level variance, minimum useful improvement, clean non-inferiority and cost ceiling to size the held-out study. Add additional protocol questions only after this contrast is interpretable.

**Status:** open

**Evidence:**

- `seo-guide-src/body.html:77`: The core proposal is 2 corpora × 6 protocols × 1,000 cases = 12,000 group episodes; the text properly says proposed and requires a pilot.

## ADD-T-01 P2 Action-domain validation permits illegal labels while successful reports hardcode invalid=0

**Project:** swarm-of-theseus

**Impact:** A future model can emit an out-of-domain action that is treated only as incorrect rather than counted as invalid, and its run may still satisfy aggregate competence thresholds. This did not corrupt S1: all 2,592 archived S1 labels independently checked here are legal.

**Recommendation:** Enforce the legal label enum at both schema and local validation; distinguish invalid action from valid-but-wrong action and report actual invalid counts. Validate any work evidence fields only to the declared contract; do not silently correct reasoning. Add a direct validator unit test, no live inference required.

**Status:** Open recommendation

**Evidence:**

- `swarm-of-theseus/src/study.py:62`: validate_solve checks label is a string and case IDs are correct, but never requires label in dax/wug; evidence/result are also not validated locally.
- `swarm-of-theseus/src/provider.py:99`: The generated output schema treats label as a generic string, so provider structured output does not enforce the legal action set.
- `swarm-of-theseus/src/runner.py:70`: Completed reports always publish invalid=0.
- `swarm-of-theseus/README.md:49`: Invalid responses are promised as a secondary endpoint; qualification requires zero invalid records.

## EP-07 P2 Bootstrap precision exceeds the independent variation in the Theseus pilot

**Project:** swarm-of-theseus

**Impact:** The interval is a sensitivity summary over six specific runs, not a calibrated confidence statement about task families, mappings or repeated model draws. The prose already acknowledges weak precision, which should be retained; the prominent 95% label still encourages stronger interpretation.

**Recommendation:** Lead with all six paired differences and their scenario means. Label the existing interval as conditional exploratory bootstrap sensitivity. For a new study, sample distinct task instances within each mapping block and resample whole paired worlds within those blocks; separate scenario generalization from provider variation.

**Status:** Open recommendation

**Evidence:**

- `https://github.com/dmarzzz/swarm-lab/blob/a773ff5410442fcf351cfc817550b3fc92a88994/researchers/vishesh/notes/swarm-of-theseus/src/study.py:18`: Every even seed uses one label mapping/convention, every odd seed the other; the same four binary feature combinations recur every step.
- `https://github.com/dmarzzz/swarm-lab/blob/a773ff5410442fcf351cfc817550b3fc92a88994/researchers/vishesh/notes/swarm-of-theseus/src/analyze.py:21`: Bootstrap resamples the two observed worlds inside each of only three fixed scenarios.
- `swarm-of-theseus/RESULTS.md:26`: The reported +47.92 pp mean and +22.92 to +72.92 interval are arithmetically reproducible, but there is one run per counterbalanced mapping per scenario.

## EP-08 P2 Notes and mentoring vary information amount and access structure together

**Project:** swarm-of-theseus

**Impact:** This is a valid comparison of these implemented packages, but not a clean mechanism estimate for conversation versus written storage. Notes have access to three memories and mentoring one; both also transmits more information.

**Recommendation:** In a new compact study, compare the same outgoing notebook as written handoff, read-only copy, and bounded interactive Q&A with a matched available-information budget. Include a no-inheritance arm and a verbatim competence ceiling. Keep procedure accuracy and arbitrary phrase retention separate; do not turn the current ceiling result into a mentoring claim.

**Status:** Open recommendation

**Evidence:**

- `https://github.com/dmarzzz/swarm-lab/blob/a773ff5410442fcf351cfc817550b3fc92a88994/researchers/vishesh/notes/swarm-of-theseus/src/study.py:95`: Notes provide the entire prior three-agent archive; mentoring gives one outgoing agent message capped at 300 characters.
- `swarm-of-theseus/RESULTS.md:63`: Recorded totals: notes 6,756 bytes, mentor 5,746, both 12,530. Notes/both both reach 100% task accuracy; no added mentoring benefit demonstrated.

## EP-11 P2 The archived S1 receipt points to the previous README revision

**Project:** swarm-of-theseus

**Impact:** Direct comparison of the two pinned READMEs shows only the added qualification-success/S1-ready section, not a changed scientific design. Thus this is a provenance/process ambiguity, not evidence of post hoc treatment changes or invalid numerical results.

**Recommendation:** Record plan_revision and implementation_revision as distinct fields, plus an explicit authorized amendment record when they differ. If the current procedure requires exact source-plan matching, reject mismatch; otherwise document why the prior immutable plan still covers the run instead of claiming an identical registered source.

**Status:** later DEPLOYMENT documentation clarifies separate plan and implementation revisions; no changed scientific design found

**Evidence:**

- `swarm-of-theseus/results/S1-a1/seed-bank-both-200/public-plan-receipt.json:4`: All 36 S1 receipts retain commit 586c4768, while execution source/README is a773ff54.
- `swarm-of-theseus/results/S1-a1/manifest.json:4`: Source manifest differs from receipt source; all 36 plan hashes differ from the current manifest README hash.
- `https://github.com/dmarzzz/swarm-lab/blob/a773ff5410442fcf351cfc817550b3fc92a88994/researchers/vishesh/notes/swarm-of-theseus/src/public_plan.py:24`: Preflight verifies the public page but does not bind it to the running README.

## ADD-T-02 P2 Prospective archive-sufficiency claims need an equivalence criterion

**Project:** swarm-of-theseus/redesign

**Impact:** A small or imprecise pilot can show no detected gap without establishing portable-archive sufficiency or equivalent performance. The draft is unrun and candid about remaining launch blockers, so this is a prospective design clarification rather than a false reported result.

**Recommendation:** Before qualification specify a practically meaningful equivalence/noninferiority margin and interval decision rule for portability/controller comparisons, or label their gaps descriptive and any null result inconclusive. Failure to establish a swarm advantage is already enough to withhold that claim; it does not prove equivalence.

**Status:** Open recommendation

**Evidence:**

- `swarm-of-theseus/redesign/DESIGN.md:60`: If transplant matches continuation, report archive sufficiency; if single controller matches swarm, drop a special swarm advantage claim.
- `swarm-of-theseus/redesign/DESIGN.md:56`: Noninferiority margins are required for stable reward and unaffected-component retention, but matching for portability/single-controller comparisons has no explicit margin or uncertainty criterion.

## GUIDE-007 P3 Correct Co-Scientist reading-depth pagination

**Project:** agent-experiment-guide

**Impact:** Minor bibliography inaccuracy weakens otherwise good reading-depth transparency. It does not alter the scientific interpretation.

**Recommendation:** Replace full 157-page supplement with full paper and 115-page supplement. Supporting primary record: https://arxiv.org/abs/2502.18864v2 .

**Status:** corrected in LITERATURE.md during the review; original snapshot preserved

**Evidence:**

- `agent-experiment-guide/LITERATURE.md:29`: Consulted note calls the supplement 157 pages; the primary arXiv v2 record specifies 157 total pages: 42 main plus 115 supplementary.

## ROOT-06 P3 Duplicate string matching attached the wrong biology caption to project cards

**Project:** dossier

**Impact:** Several cards displayed an unrelated biological analogy, reducing confidence in the project taxonomy despite otherwise polished visuals.

**Recommendation:** Match by project slug, keep one replacement per card, and validate all 16 generated labels against their source brief. Fixed and generated dossier rebuilt in this review.

**Status:** fixed; all 16 mappings verified

**Evidence:**

- `dossier-src/prism.py:16`: Original replacement matched a shared hour-estimate string, so the first replacement changed all cards with that estimate.
- `dossier-src/build.py:19`: Now emits a unique data-project-assessment slug for each card.

## ROOT-09 P3 Editorial fit tags and estimates are weak decision aids

**Project:** dossier

**Impact:** Nearly uniform positive labels do little to prioritize scarce effort. A polished browser demo should not be mistaken for a feasible confirmatory study inside the estimated hours.

**Recommendation:** Rank by identifiable contrast, available evidence, implementation readiness, qualification risk and minimum decisive deliverable. Separate demo completion from research completion. Keep 1–2 active mechanisms and park the rest.

**Status:** open

**Evidence:**

- `dossier-src/research.py:1`: Fifteen of sixteen proposals receive Strong fit; time estimates assume familiar tools and ready data.
- `dossier-src/build.py:43`: Tags are explicitly editorial and estimates qualified, which is good practice.

## ADD-H-04 P3 Pilot03 qualification prose miscounts distinct method names

**Project:** healing-helping-hands

**Impact:** Small reproducibility/writing error; the actual60 balanced cases and15 semantic templates are intact. Renamed entities do not create60 independent semantic templates.

**Recommendation:** Correct in an explicitly dated erratum:20 method names, five phrasings/class,60 items. Keep the frozen preregistration unchanged and linked.

**Status:** Open recommendation

**Evidence:**

- `https://github.com/dmarzzz/swarm-lab/blob/46678b2b99936383d01b268075e0ae2cf8b405fc/researchers/vishesh/notes/healing-helping-hands/reviews/pilot-03-pre.md:12`: Plan describes four new method names; source new_qualification uses i=0..19 and names system K401 through K420, with five phrasings/class repeated across20 names.

## ADD-I-04 P3 Standalone images omit the run identity required by their own visualization specification

**Project:** immune-response-review

**Impact:** Separate final-frame exports can lose their provenance when shared outside the folder. The HTML views do expose backend/source and selectors, and the comparison chart gives appropriate one-episode caveats.

**Recommendation:** Add a compact footer with run/architecture, selected seed or aggregation rule, source prefix and scripted/native label; use stepped state timelines for discrete ticks and distinguish overlapping arms without adding decorative motion.

**Status:** open

**Evidence:**

- `immune-response-review/SCENARIO-SPEC.md:66`: Requires case, seed, arm, source hash and backend in every view.
- `immune-response-review/scenario-solo-a1/final_frame.png:1`: Image title says anthropic but does not identify solo architecture, seed 9101, amendment or source hash.
- `immune-response-review/scenario-engineering-a1/final_frame.png:1`: Same pixels as a2 final_frame despite different seed ranges/source versions; no embedded source/seed label allows standalone identification.

## ROOT-08 P3 Visual test scripts assume the author’s machine

**Project:** presentation-tooling

**Impact:** The HTML is portable and self-contained, but another reviewer cannot readily run the same presentation checks from the checkout alone.

**Recommendation:** Document one local QA command with configurable browser/runtime paths or a small dev dependency manifest. Keep it separate from experimental dependencies; a container or CI service is unnecessary.

**Status:** open

**Evidence:**

- `dossier-src/check-prism.cjs:1`: Browser dependency and output locations are machine-specific.
- `seo-guide-src/check.cjs:1`: Same local Playwright/browser assumptions; no portable package manifest in this presentation source.

## REG-11 P3 Replay emphasizes100% validity while the decisive6.5% shortest-path result is visually secondary

**Project:** regrowth-200

**Impact:** The visual craft is already coherent, but a quick reader can infer model success and fail to notice that the exact algorithm produces optimal routes while model routes are poor. The headline multiplication can imply200 separately loaded models.

**Recommendation:** Use200 states /199 decision cells and shared-weight model labels. Put final validity, shortest fraction, route stretch, cost and registration/exploratory status together; give overlapping curves distinguishable markers/dashes, provide text summaries and keyboard cell selection, and show baseline on equal footing. Keep the existing restrained palette/layout; avoid a full UI rebuild. Make visual QA use resolved dependencies and write review screenshots to temporary output.

**Status:** Open recommendation

**Evidence:**

- `regrowth-200/site/index.html:5`: Headline panels say200×Qwen and show rounded valid percentages.
- `regrowth-200/site/index.html:7`: Main table/chart omit final shortest fraction and excess hops; baseline has no grid panel.
- `regrowth-200/src/check_replay.cjs:3`: A desktop/mobile smoke script exists but depends on a developer-specific absolute Playwright path and changes the screenshot while checking.

## EP-12 P3 Static failure graphics omit the promised visible missing steps

**Project:** swarm-of-theseus

**Impact:** The more polished aggregate graphic is readable, but a failed individual PNG can make a missing observation difficult to distinguish from an omitted axis category. HTML controls also lack explicit labels and canvas has no equivalent numeric table.

**Recommendation:** Render all six scheduled step slots with a grey missing marker, keep numeric values in an accessible table, and label replay selector/slider. Show tiny-n per-world dots next to aggregate means. Preserve the current strong separation of task accuracy and convention retention.

**Status:** Open recommendation

**Evidence:**

- `https://github.com/dmarzzz/swarm-lab/blob/a773ff5410442fcf351cfc817550b3fc92a88994/researchers/vishesh/notes/swarm-of-theseus/src/render.py:16`: Static PNG draws only retained frames; missing steps are blank rather than explicit grey gaps. HTML replay explicitly draws missing markers.
- `swarm-of-theseus/results/S0-a2/audit.json:4`: S0-a2 has 61 of 72 frames, so this affects actual archived failure evidence.

## ROOT-07 P3 Repository entry point does not distinguish the planning snapshot from executed work

**Project:** workspace

**Impact:** New collaborators can confuse historical plans, scripted engineering controls, qualified model pilots and active exports.

**Recommendation:** Add a current repository index with evidence class, scope/cutoff, links to each result and agent lifecycle standard. Preserve the old context as historical rather than rewriting its narrative.

**Status:** fixed with README.md; original handoff preserved

**Evidence:**

- `grove-hackathon-context.md:1`: Historical handoff describes a planning state predating the current experiment folders.
- `AGENTS.md:5`: The current owner requirement needs a visible entry point for future work.

Paths and lines identify reviewed versions; current files may differ. [Recorded inventories](review-2026-10-04/inventory.json) and [source availability](review-2026-10-04/source-map.json) distinguish included, exact-match, related and local-only evidence.
