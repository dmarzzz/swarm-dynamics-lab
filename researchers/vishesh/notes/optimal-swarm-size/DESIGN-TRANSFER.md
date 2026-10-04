# Optimal Swarm Size: lessons for the next design

2026-10-04 · **prospective planning input, not a launch plan or approval**. Source cutoff `1d15f2a0`. [Transfer review and checked arithmetic](../dmarz-methods-transfer-2026-10-04/README.md). These notes supplement the owning study's current SETUP and latest native closeout; they do not replace them or change a frozen/queued attempt.

**Starting point at cutoff:** Q-A6 has two fresh roots, eight episodes and zero full successes. A useful size rule remains untested.

| Decision | Addition to the next proposal |
|---|---|
| Green — retain/adopt | Factor team size separately from total compute, available independent evidence and concurrency. Keep an equal-capacity single controller and exact scheduler reference. Increase workload structure or scarce evidence on development cases rather than merely increasing named workers. |
| Green — collect/report | Trace worker truth→delivered evidence→integrated answer. Record full-task success, component error, critical-path latency, total cost and queueing. A faster failure is not an optimum. Freeze a cheap-stage futility rule before a large N sweep. |
| Yellow — sample design | Root tasks define n; matched N arms and worker items are dependent. Estimate paired root-level variability before sizing a precision study. At most a bounded feasibility screen is justified by the current two-root pilot. |

**Recommended next decision:** Repair/qualify the hardest worker step first. Avoid a large N grid until a competent N1 or other clean reference establishes interpretable headroom.

Source evidence: [M1](https://github.com/dmarzzz/swarm-lab/blob/1d15f2a057a9e9c44f8d379263da734b1add8dcd/researchers/dmarz/notes/market-split-opus/RESULTS.md), [M3](https://github.com/dmarzzz/swarm-lab/blob/1d15f2a057a9e9c44f8d379263da734b1add8dcd/researchers/dmarz/notes/sybil-scarcity-opus/RESULTS.md), [M6](https://github.com/dmarzzz/swarm-lab/blob/1d15f2a057a9e9c44f8d379263da734b1add8dcd/researchers/dmarz/notes/sybil-scale-opus/RESULTS.md), [D4](https://github.com/dmarzzz/swarm-lab/blob/1d15f2a057a9e9c44f8d379263da734b1add8dcd/researchers/dmarz/notes/soc07-private-judgments/reviews/s1l-post.md). Transfer is an inference across tasks, not demonstrated efficacy here. Complete the existing run-quality assessment and concrete next-run proposal before experimental implementation; resolve exact sample allocation, precision/feasibility rationale, holdouts, stops, worst-case cumulative costs and machine need. Offline preparation may continue; obtain owner approval of any changed run scope before allocation or launch. Existing unchanged explicit approval need not be requested twice. Researcher review remains optional for Vishesh-owned studies.

## PI decision for the next session

**Analyze; park broad N sweep.** Reconciled at `22834c84`; [evidence](reviews/q-a6-post.md), [combined PI dispositions](../pi-next-decisions-2026-10-04/README.md). This is a planning decision, not a live worker/claim check.

| Item | Decision |
|---|---|
| First action | Use Q-A5/Q-A6 worker-to-final evidence to select one unresolved competence or scheduling question. Correct the entry-page stale no-code/no-run status. Do not fit an optimal-size rule from two roots. |
| Empirically unknown | Where does parallel execution buy correct on-time work once a competent task is available? |
| Outcomes that change our decision | If qualified paired tasks show useful quality-adjusted throughput, size a targeted replication; if a single controller matches it, keep N1; if N2 is faster but wrong, do not scale; if imprecise, report feasibility only. |
| Why simpler/existing evidence is not enough | Equal-total-resource single controller and deterministic scheduler; separate evidence supply, capacity and concurrency from headcount. |
| What the collective contributes | The collective mechanism is task dependency and concurrent coordination; demonstrate it rather than treating the number of worker names as the treatment. |
| Boundaries and stopping | Q-A6 has zero full successes on two roots. Existing USD20 authority is not permission for a new design; prioritize diagnosis over a general model × N grid. |
