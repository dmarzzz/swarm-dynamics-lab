# O1 post-mortem: useful instrument, coordination confound found

All12 episodes completed, with140 native OpenRouter calls, no retries, transport/schema failures or unsafe commits. All4 single-agent qualification mechanisms passed. The small demonstration yielded7/8 recoveries. [Analysis](../results/outage-o1/analysis.json), [full trace audit](../results/outage-o1/trace-audit.json), [48-file authenticated hub readback](../results/outage-o1/verification.json) and [eleven-dimension scientific assessment](../results/outage-o1/scientific-assessment.json). This is the owning agent's scientific review, separate from the automated offline finalize scaffold.

| Strategy | Stable recovery | Changing recovery | Calls across both | Exposure across both |
|---|---|---|---:|---:|
| Single context, four tool slots | yes | yes |16|$0.038129|
| Fixed four contexts | yes |3/4 services|64|$0.166912|
| Deterministic public-state controller | yes |yes|0|$0|
| Four-to-one contraction | yes |yes|28|$0.058728|

The simple controller and single agent are the practical winners on this declared support. The controller uses the same public inspections and safe writes, with no model or evaluator access. Its zero API cost excludes pre-existing shared infrastructure and is not a general production cost claim.

## Native failure diagnosis

The one task miss is the changing fixed-four case. At tick1 all four actors inspect the same first service. Tick2 rejects all four stale patches after failover. They repeat the same inspection at tick3; at tick4 only the first repair commits while three duplicates are rejected. This repeats for the next two services, exhausting tick8 before the fourth is repaired. All32 visible responses and32 exact effective requests are retained for this episode. The final checker identifies only the remaining endpoint mismatch. No hidden transport failure or unsafe write caused the miss.

Contraction fires after tick2 in BOTH stable and changing cases. The stable trigger comes from duplicate writes, without any exogenous event. Thus the observed improvement is consistent with eliminating redundant coordination work; it does not establish useful detection of a parallel-to-coupled phase transition. The interface gave actors IDs and a request to coordinate, but no concrete disjoint ownership protocol. That is a substantive comparator weakness for a general team-size claim, even though the single-agent and deterministic comparisons are strong.

## Scientific decision

Finish this instrument demonstration. It establishes a model-solvable outage task and exposes a concrete coordination failure. It does not identify optimalN, show contraction beats a well-coordinated fixed team, or generalize beyond one demonstration template. Four mechanism qualification cases and140 calls are not140 independent incidents. A better future design would add explicit task ownership/work claims, parallel work that cannot be cheaply batched by one actor, delayed or incomplete telemetry, and distinct incident roots. Those changes need a prospective scoped proposal; none are silently implemented or rerun here.

The separately approved Q-A7 public-input-binding diagnostic may proceed: O1's operational route/accounting/publication checks passed, and its scientific coordination limitation does not invalidate the arithmetic diagnostic. Q-A7 keeps its original roots, arms, futility andUSD2subcap, with an explicit OpenRouter routing amendment and fresh public/source/ledger admission.

## Accounting and process

O1 provider-reported settled costUSD0.314565, additional fee-uncertainty holdUSD0.031519, total exposureUSD0.346084. The original ledger now contains771records, settledUSD2.125405 and total exposureUSD2.377404; historical unknownUSD0.220480 remains untouched. OriginalUSD20cap unchanged. The prior authority was backed up/hash-verified and fenced before a single-writer transfer to the exclusively claimed approved-account worker, after explicit owner approval. No new cloud resources or host credential installation.

Execution source2acfe6cf; immutable public plan and condition TLDRs verified before calls. Public UI lists runs, while raw JSON/HTML artifacts are restricted by its proxy: authenticated hub readback verified all48files; the synthetic raw evidence is also published in this repository. Browser replay verification was on the saved scripted fixture; native scores were independently recomputed from all12 saved terminal states. No independent researcher review was required or claimed.
