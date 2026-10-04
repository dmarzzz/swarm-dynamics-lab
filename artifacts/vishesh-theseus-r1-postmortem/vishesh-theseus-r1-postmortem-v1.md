# Theseus R1 postmortem: candidate executor qualified, broad repair advantage not established

Verdict: complete_valid_result. Owning-agent PI assessment; no independent researcher review. R1 is the single native repair after D2. Freeze candidate F and stop this repair line. Acquisition and cultural preservation remain untested.

## Result against the frozen plan

384/384 calls started and completed, 384 assigned decisions graded, zero provider errors, retries, missing usage, truncations, audit disagreements or request-hash mismatches. Six fresh fixed worlds, 96 distinct case/family pairs, two identical native repetitions per arm. Input/output tokens: 211544/11476. Recorded model cost USD0.268924; native interval 544.4 seconds. No incremental machine purchase.

| Metric | E: unchanged atomic | F: repaired atomic |
|---|---:|---:|
| Strict correct | 188/192 (97.92%) | 192/192 (100%) |
| Valid response contracts | 192/192 | 192/192 |
| Release correct | 96/96 | 96/96 |
| Incident correct | 92/96 | 96/96 |
| Valid-release recall | 24/24 | 24/24 |
| False releases | 0 | 0 |
| False incident activations | 4 | 0 |
| Native calls | 192 | 192 |
| Model USD | 0.128541 | 0.140383 |
| Qualified | no | yes |

F passes all prospective gates: 189/192 overall, 92/96 per family, 31/32 per world, 23/24 valid releases, 100% valid contracts and zero false releases or incident activations. It has 32/32 in every world. E fails overall, two world minima and the zero-false-incident gate. Do not reinterpret E as qualified because its rounded percentage is close to 98%.

The primary F-minus-E contrast is +2.083 points. Gains are +6.25 points in worlds 7200 and 7201, zero in the other four. This does **not** meet the prespecified material-benefit criterion (3 points and gains in at least four worlds). Qualification success and comparative effect size answer different questions. Report the candidate selection, not a large general repair advantage.

## Failure diagnosis and limits

E's four errors are two distinct false-signal incident cases, repeated twice. One governs ledger, one probe; each chooses the governing source when the rule requires none. Thus this failure is not exclusively a probe-label problem. Neither arm disagrees between its two identical repetitions on any of the 96 case/family pairs. There are no E identity failures in this fresh cohort.

F combines a supplied-ID enum/minimum-one output constraint with explicit incident conditional wording. The observed cohort supports the package's qualification only. It does not isolate component effects, and E's absence of new ID errors prevents an empirical attribution of an ID-copy benefit here. Original D2 identity errors remain strict failures; no historic scores were repaired.

F cost approximately 9.2% more per call than E. Calls and case information are matched, while extra instructions/schema affect input tokens and attention. Six fixed synthetic worlds, two reused Boolean task families and temperature-zero repetitions do not justify a population reliability guarantee. Perfect performance here is a bounded competence screen, as D1's later failure already illustrated.

## Process and evidence

The plan preceded implementation and all paid calls. The first preparation contained unsupported maxItems. An official API documentation check caught it before dispatch; a prospective clarification retained minItems=1 and exact-ID enums, while strict scoring still required exactly one decision. The old preparation/receipts were preserved as superseded, the new revision was deployed/tested, public registration/page verification refreshed, and only then was one native attempt launched. This was not an excluded live probe or a second repair attempt.

Eight offline checks passed locally and on Python 3.12.3 at pinned source c4c7a87973b0027e70f4bb6bfd44c7fd664bf656. Full raw-text reference scoring agrees on all 384 rows, and all delivered request hashes match the manifest. The model served the pinned Haiku version. Replay/CSV retain every assignment. The static figure was visually checked against summary counts; all correct/invalid/unstarted display states were previously fixture-checked.

The same exclusive sim-dmarz-3 allocation was retained from D2 with current claim and no competing workload. D2 reservations were settled before R1 reserved its own non-overlapping USD3.80 envelope. D1+D2+R1 estimated cumulative cost is USD0.8122310437, leaving approximately USD4.1877689563 of the original USD5. New model spend in this cycle is USD0.626774. Zero ambiguous calls or unresolved model reservations. Claim release follows verified durable uploads; see closeout.json.

## Quality assessment and decisions

| Dimension | Assessment | Evidence / limitation |
|---|---|---|
| question | pass | Fixed F/E contrast, engineering gates and material-benefit threshold kept separate. |
| scenarios | pass within scope | Fresh fixed worlds with all mappings and conflict coverage; finite synthetic realism. |
| controls | pass within scope | Unchanged E and matched case information; bundled F prevents component attribution. |
| capability | pass for F only | All prespecified gates pass; E fails and is not relabeled. |
| measurement | pass | Full raw audit, strict identity semantics, no missing rows or post-hoc threshold change. |
| sample_size | pass for diagnostic scope | Six paired worlds, 96 distinct pairs; no independent-n inflation or reliability bound. |
| agent_context | pass | Request hashes and served model match; stateless, no hidden history or feedback. |
| data_integrity | pass | Assigned = started = terminal = graded = 384; preserved earlier failures. |
| resources | pass | Settled prior allocation, once-only reservation, zero retries, same exclusive host. |
| reproducibility | pass | Source/runtime/manifest pinned, raw evidence and same-author reference audit. |
| visualization | pass | Counts, costs, six world contrasts and false activations agree with raw-derived summary. |

The useful outcome is a candidate execution component, not a culture result. Stop adding prompt repairs or rerunning these Boolean tasks to chase a stronger effect. Next qualify learning from labeled experience with the true mapping withheld, then test selective preservation/correction under full context replacement with frozen notes and a matched single-controller comparator. No second repair or culture run is launched by this postmortem.
