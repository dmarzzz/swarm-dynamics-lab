# Direct launch and native-trace review cycle

2026-10-04. Work in progress. The owner removed the central-acknowledgment wait for eight prepared Vishesh scopes; direct dispatch still requires the original budget, verified Dmarz account/state, an exclusive allocation, public plan and qualified runtime. No blanket budget increase or deletion of other researchers’ machines is authorized.

## What is implemented

- The exact scope is recorded in [AGENTS.md](../../../../AGENTS.md#direct-execution-for-the-current-vishesh-study-cycle). Each owning task is the sole dispatcher; old central requests are fenced first.
- [Native trace review](../../../../tooling/agent-experiments/RUN-REVIEW.md#review-the-native-traces-before-choosing-a-repair), the quality rubric and post-mortem template now require trace coverage, every qualification miss, the first observable divergence, competing explanations and a discriminating repair. No universal new logger/service was imposed.
- Quorum and Phantom completed saved-record audits and implemented concrete scenario/baseline revisions. Neither revision yet establishes a useful role for another native model run.

## Verified source updates

| Source | Revision | Lesson retained | Boundary |
|---|---|---|---|
| [Completion audit](../../../dmarz/notes/completion-audit-2026-10-04/README.md) |6e4e879da3f4fe7d3a3186675306249d3506f9a3| Separate execution, validity, completion, refusal and qualification; inspect actual packets/returns | Historical baseline/supplement, not current live status |
| [Pipeline lessons](../../../dmarz/notes/pipeline/LESSONS.md) |466fe9310aa09a33ecdf598dd1aad9cd7cfa49bc| Read each failed answer before changing models; intermediate fields diagnose without necessarily repairing | Different fixture batches do not identify a paired format effect |
| [Per-row worked review](../../../dmarz/notes/verify-cost-qwen/reviews/chain-002-post.md) |88e9455c9e745444f93ed8287ea6a5380363ffbe| Join assignments, rendered requests and returned objects; distinguish cost formation from selected action | Written answers are not access to hidden reasoning |
| [Trace transport](../../../dmarz/notes/discussion-dose/src/artifacts.py) |cf872ef669c7451261bf8d0538c2661bf1607a58| Compressed/chunked artifact index, payload/raw hashes, recovery without rerunning | Study-local implementation; not a new global logger |

Private operator-session transcript collection is a separate workflow. It is not required to analyze these native experiment traces and was not invoked here. Exact owner prompts, secrets and private resources are excluded from this public note.

## Current coordination

Direct dispatch has been exercised. Seven studies reached native execution. Right Dissenter passed its bounded Q5 qualification; the other six attempts did not establish uncontaminated qualification. Released machines have been assigned sequentially. The approved account is at its current droplet quota, so a working credential alone cannot create another machine. No other researcher's claim was released or worker deleted to make room.

Snapshot: **2026-10-04 17:17 UTC**. Counts below are observed, not planned. See [structured status](status.json) for provenance and source-file hashes; an operational report can be newer than its published scientific review.

| Study | Execution / sample observed | Assessment | Next action |
|---|---|---|---|
| Antsy | 5 valid OCR outputs, 1 timeout, 34 unstarted; 2 complete pairs | Reviewed; qualification incomplete | Timing/timeout retention repair tested; bounded latency plan prepared |
| Theseus | 1 HTTP429, 203 unstarted; no valid learner or executor outcome | Reviewed; transport failure, cause unresolved | Error observability repaired; retain unresolved reservation |
| Influence | 24 failed logical requests / 48 transport attempts; no returned answers | Reviewed; transport failure, exact codes lost | Tested error retention/circuit breaker; bounded two-contract proposal |
| Poietic | 1 returned answer rejected by parser, 143 unstarted | Reviewed; action-contract failure before environment execution | Explicit prompt, billing retention and diagnostic runner repaired;106 offline tests reported |
| Healing | 60 reports / 180 calls; Jev60/60, Qwen40/60 each | Reviewed; instrument invalid: expected labels leaked in names | S1 stopped; metadata-blind repair tested and qualification plan prepared |
| Immune | 1 HTTP429; no response or completed controller episode | Reviewed; transport failure, cause unresolved | Error observability repaired; no repeated probe or A5 |
| Right Dissenter | Q5:24 valid responses; raw and card12/12 correct | Qualification reviewed and passed; no card advantage at ceiling | H5 has started under the unchanged conditional scope; result pending |
| Optimal Size | No Q-A7 calls or claim; original ledger preserved | Operational hold: repeated direct-route failures | Resume on relevant recovery evidence; first-failure handling fixed offline |
| Quorum | 48 retained valid historical answers; all 11 graded misses inspected | Old context comparison confounded; simple control solves development set | Acquire a defensible residual task before proposing native evaluation |
| Phantom | 140 retained request/output pairs; 6 manually inspected S1 cases | Revised decision problem solved by exact Bayes | Define an application-specific model role before spending |

Execution failures are not adverse scientific effects. A failed qualification does not demonstrate that a swarm idea is false, and a completed post-mortem does not turn it into a successful experiment.

### What the new traces change

| Observation | Supported repair | Unsupported inference |
|---|---|---|
| Antsy's larger third image timed out; phase timing and timeout streams were absent | Retain phases and timeout diagnostics; specify cold versus persistent-worker timing | Larger images are proven to cause the timeout; a longer limit will fix it |
| Theseus returned HTTP429; Influence retained only `PolicyError` across failed transport attempts | Preserve allowlisted status/category/retry metadata and stop futile dispatch sooner in a prospective version | Billing exhaustion is proven; all failures had the same code |
| Poietic got HTTP200 through OpenRouter, then failed strict parsing | Audit formatting and action-schema errors separately using the saved answer | Direct Anthropic has recovered; stripping fences alone makes the action valid |
| Healing's method names contained expected labels; both Qwen variants made the same20 errors | Remove evaluator metadata and test the complete actor-visible contract before new qualification | Jev60/60 establishes uncontaminated competence; two agreeing Qwen agents add independent evidence |
| Quorum changed schema, order and instructions alongside context | Separate those interventions in any future comparison | Context or priors alone caused the observed accuracy drop |
| Phantom's exact controller solves the specified contract | Strengthen the task's application rationale and comparator | More model calls will establish a useful model contribution |

Changing a model, timeout, parser tolerance, prompt, stopping rule or sample produces a new execution contract. Prepare and validate that change offline first, retain the failed cohort, and seek the applicable next-run decision rather than silently restarting it. Original ledgers retain uncertain costs even when no usage receipt was returned.

## Trace-grounded revisions delivered

- [Quorum](../decision-models/quorum-of-mirrors/trace-review/RESULTS.md): full historical denominator and all graded misses reviewed; schema/instruction/order changes confound the old context comparison.24development bundles now test source resolution/common causes against four deterministic controls. Strongest template-tuned control solves the development set; an independently sourced residual task is still missing. Nine checks rerun here.
- [Phantom](../phantom-coast/pc7/README.md):140retained pairs reconcile, with missing raw-body/confidence fields disclosed and manual inspection coverage explicitly bounded. New finite-history/shift model and information-value controller are implemented offline; exhaustive policy enumeration agrees. Eight checks and full portable readback rerun here. A native model role beyond exact Bayes is still unjustified.

These are implemented scenario/baseline improvements and revised conditional plans, not additional model outcomes. A receiver, claim or successful credential handoff alone is not evidence that a model request was sent.

## Implemented repairs and next decisions

| Study | Published review / repair | Validation and boundary |
|---|---|---|
| Antsy | [Post-mortem](../antsy-targeted-v8/reviews/Q0-attempt-1-post.md) · [versioned repair and D1 plan](../antsy-targeted-v8/execution-repair-v1/README.md) |13 fault tests rerun here; proposed6 cold calls on3 reused receipts. Native latency remains unknown. |
| Theseus | [Actual trace review](../swarm-of-theseus/execution-diagnostic/results/A1/TRACE-REVIEW.md) · [safe error diagnostics](../swarm-of-theseus/execution-diagnostic/A1-DIAGNOSTICS-REPAIR-PLAN.md) |23 checks rerun here with resource warnings treated as errors; no new provider request. |
| Influence | [D5 post-mortem](../influence-swarms/scenario/reviews/D5-post.md) · [D6 preparation](../influence-swarms/scenario/ITERATION-06-PREP.md) |10 acquisition tests rerun here; exact rejected response bodies now survive validation. Proposed two-contract maximum USD0.097280, no dispatch. |
| Poietic | [S0-02 post-mortem](../poietic-agents/reviews/S0-02-post.md) · [D0-01 diagnostic](../poietic-agents/reviews/S0-02-repair-plan.md) |106 offline checks reported, including full worker fault rehearsals. Proposed36 decisions on3 paired generator roots; no diagnostic dispatch. |
| Healing | [C4 post-mortem](../healing-helping-hands/c4/S0-POST.md) · [C5 proposal](../healing-helping-hands/c5/PLAN.md) |5 complete-context checks rerun here. Proposed60 instances from12 authored templates,180 calls; no claim of60 independent semantic problems or automatic main stage. |
| Immune | [A4 post-mortem](../immune-response-v3/freshness-study/reviews/a4-post.md) · [diagnostic checks](../immune-response-v3/freshness-study/reviews/http-diagnostics-validation.json) |13 checks reported; full new USD0.006006 reservation retained because actual charge is unknown. |
| Optimal Size | [Route assessment and repair](../optimal-swarm-size/reviews/q-a7-route-assessment.md) |65 checks reported; HTTP failure during work now stops scheduling as promised. No Q-A7 model call. |

Tests verify the repaired software behavior; they do not establish provider recovery, model capability or scientific efficacy. A material diagnostic or qualification successor remains a concrete owner decision, with the original cumulative budget and unresolved costs carried forward.
