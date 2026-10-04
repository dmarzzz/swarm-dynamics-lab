# Quorum D1: distinguish copied evidence from prior-choice anchoring

Status: prospective material-update proposal; owner decision pending. Written before implementation. Parent: QM-Q1-02, whose valid 0/8 result is retained. Researcher review is not required. No allocation or new model call is authorized by this file.

## TLDR

Test whether explicit source deduplication or removal of misleading prior choices improves the pinned Jev model's handling of copied binary evidence. Cross raw repeated reports versus one report per source with no prior choice, correct/wrong self choice, and correct/wrong peer choices. First run eight clean qualification calls; only if they pass, run 160 fixed diagnostic calls covering eight structural fixtures, ten arms and two identical-request repetitions. Score exact source-MAP accuracy, prior-following, per-fixture effects and cost. These are synthetic finite fixtures, not 168 independent tasks, real swarms or population evidence.

## Question and prediction

Primary: among conflict fixtures with no prior decisions, does presenting each independent source once improve correctness over presenting seven copies of one source and one of each other source? This directly informs whether source normalization should happen in code before model access. Predict a nonnegative effect; the minimum useful observed gain is 0.50 on the four equally weighted conflict structures, with no structure harmed and nonnegative gain in both repetition blocks. Failure to meet this rule is reported, not repaired into success.

Secondary: within each representation, how much do wrong self or peer decisions reduce accuracy compared with no prior decision? Correct-prior controls distinguish misleading value from mere context presence. The qualification-floor alternative is that the model cannot execute even the clean three-source task. Another alternative is that the old ambiguous self-review instruction drove the earlier result; this design removes that ambiguity uniformly, so it cannot isolate the historical wording effect. No comparison against Q1-02 is treated as a randomized contrast.

## Setup

Pinned model typesafe/jev-1.13, expected snapshot typesafe/jev-1.13-20260917, TypeSafe only, no fallback. One stateless decision call per assignment, no tools, retrieval, memory inheritance or communication between real agents. The prior choices are scripted context, not measured first-pass model decisions. Exact truth is the MAP decision under equal truth priors and three independent binary acquisitions with equal q>.5. Distinct visible_root labels identify sources; copies never add information.

Qualification QM-D1-Q0-01: all eight binary root patterns at q=.72, one record per source, no prior choices, one call each. Require 8/8 valid, >=7/8 correct, and both unanimous patterns correct. This is an eight-call clean capability gate; it is not a swarm or intervention result.

Diagnostic QM-D1-01: four patterns (100,011,000,111) at q=.65 and .80 = eight fixed structural fixtures. Conflict stratum is 100/011; agreement-control stratum is 000/111. Within each fixture cross two representations (one-per-source or 7/1/1 copied reports) and five contexts (none, self-correct, self-wrong, peers-correct, peers-wrong). Self context contains one prior decision; peer context contains three scripted unanimous prior decisions. Every available prior uses .80 selected, .15 opposite and .05 DEFER scores. Correct/wrong labels exist only in the evaluator. All arms receive the same instructions; none says to use only a prior decision. All ancestry is explicit; partial ancestry is excluded because it cannot resolve this causal question.

Each of the 80 unique requests is called twice, byte-identically, with separate assignment IDs. Eight structural fixtures (four conflict, four agreement) are dependent handcrafted support points, not independent sampled worlds. Two repetitions measure limited provider variability, not two new task populations. Qualification and diagnostic IDs/reliability differ, but the bit grammar is reused and explicitly not a fresh scientific holdout. Existing reserved C1 worlds/seeds 41000–41003 remain unopened. No new real-world/generalization claim.

Neutral source/report IDs and record order derive from fixture identity independently of labels/answers; matched arms preserve sources and values. Assignment order is frozen by a deterministic shuffle (seed 20261004); repetition blocks are each balanced over all arms. Source labels are complemented/order-mixed, and evaluator target, arm alignment, stratum and fixture names never enter requests. Request sizes are checked offline. Treatments intentionally change context length; report input tokens and cost, and do not call this an equal-token causal comparison. Exact source-MAP and naive report-majority are saved-input deterministic references, not extra model arms.

## Protocol

1. Complete the parent operational closeout and eleven-dimension scientific review. Preserve its valid negative outcome and all costs. Publish this plan before implementing its contract.
2. Compile qualification and diagnostic manifests, agent/context definitions, source hashes and request hashes. Offline check paired sources, unchanged instructions, target isolation, known-answer controls, duplicate/unknown receipt rejection, malformed usage, missingness, qualification refusal and budget continuity. Render a clearly scripted preview with wrong, failed and unstarted rows.
3. Complete the concrete update and request the owner's design decision under the current runbook. No machine claim while this remains pending. Existing $1 API/$1 infrastructure approval is reused, never reset.
4. After that decision, bind the approved plan/contract digest to a private provenance record; obtain a fresh dedicated approved-account claim and verify actual host workload, source/runtime, original ledger and credential procedure. Publish/register the immutable stage plan and condition TLDR; verify the public page before calls.
5. Admit only QM-D1-Q0-01, maximum eight native calls. Stop at first provider/schema/accounting failure; preserve unstarted cases. A valid wrong choice is retained. If the clean gate fails, do not start the diagnostic. No repair namespace or automatic retry is proposed.
6. If clean qualification passes on the exact same instrument, repeat live stage admission and register QM-D1-01, maximum 160 native calls, sequential and no retries. Recheck public/source/allocation/budget constraints before each request; retain bounded usage before answer validation and one terminal outcome per dispatch. No tuning, model substitution or favorable stopping based on intermediate effects.
7. Recompute from saved evidence, complete the operational finalize hook and scientific post-mortem, verify artifact downloads/hashes and visual mappings, stop only these workers, close memory credentials and release the claim. No automatic M1/C1 or new material successor.

## Metrics

Qualification: validity /8, exact source-MAP correctness /8, unanimous control correctness /2. Main primary: per-conflict-fixture mean correctness over two repeats for deduplicated minus copied representation under no priors; average the four fixture differences equally. A >=.50 observed gain, no negative fixture difference and nonnegative gain in each repetition block is an engineering signal for source normalization within this finite support, not a statistical significance test. Report all eight paired observations and their four structural clusters.

Secondary: each arm's all-assigned correctness, wrong, DEFER, invalid and unstarted counts; wrong-prior accuracy minus no-prior accuracy within representation and conflict/agreement strata; correct-prior effects; choices matching prior and report majority; duplicate-request agreement across the two repetitions; input/output tokens, latency and native cost. Do not pool partial lineage, historical S0 or Q1 into this cohort.

Missing/invalid/unstarted assignments count as zero correctness in the conservative all-assigned endpoint and are separately named. Report best/worst bounds for unresolved responses and withhold directional decision labels unless every diagnostic assignment is valid and both clean no-prior unanimous-control arms are correct on all 16 corresponding calls. DEFER is valid but not correct on these unambiguous inputs. No fixed favorable outcome is required to finish a valid diagnostic.

The primary effect has resolution .125 with eight paired draws, and only four distinct conflict structures. There is no credible population confidence interval or power claim. The two repeats expose gross instability but cannot estimate hosted-model variance precisely. Report exact fixture effects and the two repetition-block effects; do not manufacture binomial n=160 or bootstrap a broad population from this finite support. A wider sample must follow a separately justified target population, not increase n to reverse the current finding.

## Visualization mapping

Mapping D1-v1 uses a complete fixture-by-arm table with both repeat IDs, and per-dispatch progress (valid, correct, failed, unstarted and reserved/actual cost). Initial, partial and final views render absent answers explicitly. All truth/stratum values are evaluator-only. Save a replay JSON of accumulated observed counts in dispatch order, and a standalone HTML table that allows stepping through saved receipts. Scripted previews are labelled NOT MODEL EVIDENCE. Because calls are stateless rather than interacting swarms, no physical motion or collective-time animation is implied. Read back uploaded bytes and verify table denominators and replay final counts against the journal.

## Cumulative resources and stopping

Maximum eight qualification plus 160 diagnostic calls = 168 new calls; no retries or separate provider probes. Maximum input 32,000 per call; output price must be zero; reserve $0.001344 before every call. Maximum new API reservation $0.225792; cumulative 49+168=217 calls and $0.291648 reserved. Historical known actual $0.00171696 plus one conservatively bounded $0.001344 parent charge remains separate from measured actual. Canonical ledger remains on sim-shadow until an authorized single migration; no new database or duplicated authority.

One small CPU host (at least 1 CPU, 1GB RAM, 100MB result storage), no GPU, sequential calls, maximum 45 minutes for both stages; at the previously verified $0.07143/hour rate allocated time would be <=$0.0535725. That rate must be rechecked; accept only an allocation within the remaining $1 infrastructure/six-hour cumulative limits. Actual former allocations and original S0 resource records carry forward; no personal/default-account provisioning. Dedicated model key follows existing verified-SSH memory-only delivery; no key in documents or reports. Stop on stale admission, deadline, conflicting claim, unknown accounting, model/price drift or any failed call. A stage that cannot complete remains fully reported.

## Owner decision and launch status

This material diagnostic changes prompts, arms and sample allocation. Current state: approval-ready after offline checks, owner decision pending, zero new native calls and no machine claimed. The requested decision is this bounded two-stage design, not a budget increase. Approval of qualification and conditional diagnostic does not permit any other run. The manual D1 adapter must enforce exact plan/source/manifest, approved update, passing clean qualification, original ledger and current public/runtime evidence; the shared operations wrapper has no native Quorum run adapter.
