# RD6 replacement qualification post mortem

**Q0-A2 completed all 18 native requests but failed qualification at 15/18 correct. D0 was not run.** All 12 source-only controls and all three current-conflict controls were correct. All three expired-evidence controls incorrectly selected PROCEED. This is a valid negative qualification result, not a provider outage or a failed startup. The owning agent reviewed every request and visible response and completed all eleven run-quality dimensions; no independent audit is claimed.

## Prospective contract and execution

The owner directly approved the published zero-dispatch replacement contract. Its original predecessor Q0-A1 remains stopped with zero calls; the original ledger was not reset. Source `ab7a92c944f882e85c70abd28feea87602bbd324` passed 88 offline checks locally and on the exclusively allocated approved-account host. The immutable plan and condition TLDRs were verified before launch. Exact receipt-byte binding and the remote no-provider startup acknowledgment passed before local relay creation.

One early readiness check ran before deployment finished and failed closed without a relay, reservation or worker. It was repeated only after deployment and remote tests had completed; no native attempt or stage fence was consumed by that read-only check. The actual admitted Q0-A2 ran once, with no retries, fallback, missing answer or new unknown charge. The model/provider receipt was `typesafe/jev-1.13-20260917` / TypeSafe for all 18 responses. Worker loop elapsed 10.487 seconds; it and the relay stopped and all artifacts were collected and reconciled.

## Native trace findings

| Control group | Correct | Required behavior | Observed behavior |
| --- | --- | --- | --- |
| Source only | 12/12 | Apply an explicit current process, load or required-test rule | All six PROCEED and six HOLD targets correct |
| Conflicting current evidence with history and ballots | 3/3 | DEFER on equally current contradictory observations | All three correctly DEFER |
| Expired evidence with history and ballots | 0/3 | DEFER when age 9 exceeds TTL 7 | All three incorrectly PROCEED |

The three failures span process reading 23 within 10–30, bridge capacity 26 against required 20, and a passed required compatibility test. Each positive observation was from time 91 while now=100 and TTL=7. The payload explicitly required current evidence; copied evidence cards retained the same observed_at=91. Historical action and four of five ballots said HOLD, so the selected PROCEED is not simple conformity to their majority. Reported choice probabilities were 0.86, 0.86 and 0.90; those numbers are model outputs, not established calibration.

The first observable divergence is the final action violating the freshness requirement. Stale favorable content apparently influenced the action, but internal reasoning is unavailable. The qualification controls change evidence structure as well as contextual fields; they do not causally separate temporal interpretation, history, ballots, duplicated evidence cards or output variability. Three inspected authored cases do not establish a field failure rate. D0's matched matrix and repeated-input contrast remain unmeasured.

## Process defect and offline correction plan

The convenience `native.py finalize` hook passed an absolute results path to a shared CLI that accepts repository-relative paths. It failed before writing the closeout. The documented explicit shared offline finalize command succeeded, with no recollection or ledger mutation. Before editing the helper, this post-mortem records the bounded correction: pass the canonical repository-relative result path, reject a foreign directory and test against the actual shared path validator. The correction is now implemented: all 88 tests pass, the real shared path validator accepts the relative path and rejects a foreign directory, and the corrected saved-data hook completed successfully without model calls. The frozen run source and native bundle remain unchanged; this repair is for closeout tooling only and does not authorize another model attempt.

## Decision and practical meaning

Select **complete_valid_result** for this qualification attempt; native capability has a documented gap and D0 remains blocked by the original 18/18 criterion. Do not soften the threshold or run the 144 comparison requests to obtain an effect. The simple actor-visible literal reference still labels all 18 correctly. For these finite tasks, freshness and conflict eligibility can be checked explicitly before asking a model to authorize action; any proposed modified interface would need its own prospective comparison and admission under the applicable owner authority. This record makes no claim that such a model repair has been demonstrated.

Operational completion, qualification failure, scientific review, artifact delivery, cumulative cost and allocation release remain separate records. The source-only and conflict successes are preserved alongside all three harmful stale commitments. Read the companion eleven-dimension review, trace audit and resource ledger before considering a separate question.

## Final accounting and delivery

[Resources](../results/q0-a2/resources.json) retain 506 lifetime calls and USD 0.023434447 committed API, including the historical USD 0.004032 unknown reservation. Q0-A2 added 18 settled calls costing USD 0.000735378. Its 399-second exclusive allocation added an estimated USD 0.007916825; combined lifetime API exposure plus infrastructure estimate is USD 0.778524856, within the original USD 2 split cap. Estimates are not invoice settlements. No new unknown dispatch or reservation remains.

Workers and relay are verified stopped, the allocation is released, and hub delivery completed for the seven native bundle artifacts. Public repository byte readback is recorded separately. The original A1 stopped row remains; the append-only A2 row records completed execution. D0 has zero calls. The operational handoff is `a5493a765b57b14270a6e3a4ea893162fe5809e5cbcf6f12bc79fbf4c90316a9`; the [owning quality review](Q0-A2-QUALITY.json) supplies the scientific assessment that the automatic handoff cannot.

[Reader report and verified static figure](../REPORT.md) · [Complete trace audit](../results/q0-a2/trace-audit.json).
