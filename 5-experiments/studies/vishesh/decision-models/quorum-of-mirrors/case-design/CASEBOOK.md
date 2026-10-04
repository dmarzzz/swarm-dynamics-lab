# Paired development casebook

24 cases / 12 authored scenario roots. Synthetic and inspected; not a native trial or holdout. Authentication and dependency labels are stipulated. Every packet and controller outcome is retained in cases.json and outcomes.json.

Source mapping does not verify report content. A forwarded false statement can still have a known origin. NEW_GROUP refers only to supplied registry constraints, not statistical independence.

## CD-00-A: Loading bay / paraphrase

Report: The vehicle entrance was clear at first light.

Claimed reference: none (untrusted). Authenticated edges: report → r-3.

Receipts: r-4: At sunrise the loading-bay barrier was unobstructed. [acquisition event-00-b; dependency other]; r-3: At sunrise the loading-bay barrier was unobstructed. [acquisition event-00-a; dependency new]

Known group: shared. Expected origin: r-3; admission: NEW_GROUP.

A verified link establishes origin despite different wording; without a link, similarity cannot establish which acquisition generated the report.

Pair change: Remove the only authenticated origin edge; wording stays unchanged.

## CD-00-B: Loading bay / paraphrase

Report: The vehicle entrance was clear at first light.

Claimed reference: none (untrusted). Authenticated edges: (none).

Receipts: r-4: At sunrise the loading-bay barrier was unobstructed. [acquisition event-00-b; dependency other]; r-3: At sunrise the loading-bay barrier was unobstructed. [acquisition event-00-a; dependency new]

Known group: shared. Expected origin: DEFER; admission: DEFER.

A verified link establishes origin despite different wording; without a link, similarity cannot establish which acquisition generated the report.

Pair change: Remove the only authenticated origin edge; wording stays unchanged.

## CD-01-A: Reservoir / paraphrase

Report: No liquid remained after the drain cycle.

Claimed reference: none (untrusted). Authenticated edges: report → r-10.

Receipts: r-10: The tank was empty when draining finished. [acquisition event-01-a; dependency new]; r-11: The tank was empty when draining finished. [acquisition event-01-b; dependency other]

Known group: shared. Expected origin: r-10; admission: NEW_GROUP.

A verified link establishes origin despite different wording; without a link, similarity cannot establish which acquisition generated the report.

Pair change: Remove the only authenticated origin edge; wording stays unchanged.

## CD-01-B: Reservoir / paraphrase

Report: No liquid remained after the drain cycle.

Claimed reference: none (untrusted). Authenticated edges: (none).

Receipts: r-10: The tank was empty when draining finished. [acquisition event-01-a; dependency new]; r-11: The tank was empty when draining finished. [acquisition event-01-b; dependency other]

Known group: shared. Expected origin: DEFER; admission: DEFER.

A verified link establishes origin despite different wording; without a link, similarity cannot establish which acquisition generated the report.

Pair change: Remove the only authenticated origin edge; wording stays unchanged.

## CD-02-A: Archive room / identical

Report: Humidity was 45 percent at 10:00.

Claimed reference: none (untrusted). Authenticated edges: report → r-18.

Receipts: r-17: Humidity was 45 percent at 10:00. [acquisition event-02-a; dependency new]; r-18: Humidity was 45 percent at 10:00. [acquisition event-02-b; dependency other]

Known group: shared. Expected origin: r-18; admission: NEW_GROUP.

Two distinct acquisitions have identical text. Only the authenticated binding distinguishes them; both remain visible in both variants.

Pair change: Remove the acquisition binding between otherwise identical receipts.

## CD-02-B: Archive room / identical

Report: Humidity was 45 percent at 10:00.

Claimed reference: none (untrusted). Authenticated edges: (none).

Receipts: r-17: Humidity was 45 percent at 10:00. [acquisition event-02-a; dependency new]; r-18: Humidity was 45 percent at 10:00. [acquisition event-02-b; dependency other]

Known group: shared. Expected origin: DEFER; admission: DEFER.

Two distinct acquisitions have identical text. Only the authenticated binding distinguishes them; both remain visible in both variants.

Pair change: Remove the acquisition binding between otherwise identical receipts.

## CD-03-A: Package station / identical

Report: The sealed parcel weighed two kilograms.

Claimed reference: none (untrusted). Authenticated edges: report → r-25.

Receipts: r-25: The sealed parcel weighed two kilograms. [acquisition event-03-b; dependency other]; r-24: The sealed parcel weighed two kilograms. [acquisition event-03-a; dependency new]

Known group: shared. Expected origin: r-25; admission: NEW_GROUP.

Two distinct acquisitions have identical text. Only the authenticated binding distinguishes them; both remain visible in both variants.

Pair change: Remove the acquisition binding between otherwise identical receipts.

## CD-03-B: Package station / identical

Report: The sealed parcel weighed two kilograms.

Claimed reference: none (untrusted). Authenticated edges: (none).

Receipts: r-25: The sealed parcel weighed two kilograms. [acquisition event-03-b; dependency other]; r-24: The sealed parcel weighed two kilograms. [acquisition event-03-a; dependency new]

Known group: shared. Expected origin: DEFER; admission: DEFER.

Two distinct acquisitions have identical text. Only the authenticated binding distinguishes them; both remain visible in both variants.

Pair change: Remove the acquisition binding between otherwise identical receipts.

## CD-04-A: Freezer / forged_ref

Report: The chamber was within its temperature limit.

Claimed reference: r-3 (untrusted). Authenticated edges: report → r-2.

Receipts: r-2: The chamber was within its temperature limit. [acquisition event-04-a; dependency new]; r-3: The chamber was within its temperature limit. [acquisition event-04-b; dependency other]

Known group: shared. Expected origin: r-2; admission: NEW_GROUP.

A claimed receipt ID is not an authenticated edge. The trusted binding, when present, points to the other receipt.

Pair change: Remove trusted binding while retaining the misleading untrusted claimed receipt reference.

## CD-04-B: Freezer / forged_ref

Report: The chamber was within its temperature limit.

Claimed reference: r-3 (untrusted). Authenticated edges: (none).

Receipts: r-2: The chamber was within its temperature limit. [acquisition event-04-a; dependency new]; r-3: The chamber was within its temperature limit. [acquisition event-04-b; dependency other]

Known group: shared. Expected origin: DEFER; admission: DEFER.

A claimed receipt ID is not an authenticated edge. The trusted binding, when present, points to the other receipt.

Pair change: Remove trusted binding while retaining the misleading untrusted claimed receipt reference.

## CD-05-A: Bridge sensor / forged_ref

Report: No displacement was detected during this sample.

Claimed reference: r-10 (untrusted). Authenticated edges: report → r-9.

Receipts: r-9: No displacement was detected during this sample. [acquisition event-05-a; dependency new]; r-10: No displacement was detected during this sample. [acquisition event-05-b; dependency other]

Known group: shared. Expected origin: r-9; admission: NEW_GROUP.

A claimed receipt ID is not an authenticated edge. The trusted binding, when present, points to the other receipt.

Pair change: Remove trusted binding while retaining the misleading untrusted claimed receipt reference.

## CD-05-B: Bridge sensor / forged_ref

Report: No displacement was detected during this sample.

Claimed reference: r-10 (untrusted). Authenticated edges: (none).

Receipts: r-9: No displacement was detected during this sample. [acquisition event-05-a; dependency new]; r-10: No displacement was detected during this sample. [acquisition event-05-b; dependency other]

Known group: shared. Expected origin: DEFER; admission: DEFER.

A claimed receipt ID is not an authenticated edge. The trusted binding, when present, points to the other receipt.

Pair change: Remove trusted binding while retaining the misleading untrusted claimed receipt reference.

## CD-06-A: Ventilation / relay

Report: The exhaust fan was running during inspection.

Claimed reference: none (untrusted). Authenticated edges: report → r-16.

Receipts: r-17: The exhaust fan was running during inspection. [acquisition event-06-b; dependency other]; r-16: The exhaust fan was running during inspection. [acquisition event-06-a; dependency new]

Known group: shared. Expected origin: r-16; admission: NEW_GROUP.

Forwarding creates another report, not another acquisition. Direct and relayed paths terminate at the same receipt.

Pair change: Replace direct origin link with a two-hop forwarding chain; origin must stay unchanged.

## CD-06-B: Ventilation / relay

Report: The exhaust fan was running during inspection.

Claimed reference: none (untrusted). Authenticated edges: report → forwarded-note, forwarded-note → r-16.

Receipts: r-17: The exhaust fan was running during inspection. [acquisition event-06-b; dependency other]; r-16: The exhaust fan was running during inspection. [acquisition event-06-a; dependency new]

Known group: shared. Expected origin: r-16; admission: NEW_GROUP.

Forwarding creates another report, not another acquisition. Direct and relayed paths terminate at the same receipt.

Pair change: Replace direct origin link with a two-hop forwarding chain; origin must stay unchanged.

## CD-07-A: Lift / relay

Report: The lift stopped at the requested floor.

Claimed reference: none (untrusted). Authenticated edges: report → r-23.

Receipts: r-23: The lift stopped at the requested floor. [acquisition event-07-a; dependency new]; r-24: The lift stopped at the requested floor. [acquisition event-07-b; dependency other]

Known group: shared. Expected origin: r-23; admission: NEW_GROUP.

Forwarding creates another report, not another acquisition. Direct and relayed paths terminate at the same receipt.

Pair change: Replace direct origin link with a two-hop forwarding chain; origin must stay unchanged.

## CD-07-B: Lift / relay

Report: The lift stopped at the requested floor.

Claimed reference: none (untrusted). Authenticated edges: report → forwarded-note, forwarded-note → r-23.

Receipts: r-23: The lift stopped at the requested floor. [acquisition event-07-a; dependency new]; r-24: The lift stopped at the requested floor. [acquisition event-07-b; dependency other]

Known group: shared. Expected origin: r-23; admission: NEW_GROUP.

Forwarding creates another report, not another acquisition. Direct and relayed paths terminate at the same receipt.

Pair change: Replace direct origin link with a two-hop forwarding chain; origin must stay unchanged.

## CD-08-A: Warehouse probes / dependency

Report: The room temperature measured 18 degrees.

Claimed reference: none (untrusted). Authenticated edges: report → r-1.

Receipts: r-2: The room temperature measured 18 degrees. [acquisition event-08-b; dependency other]; r-1: The room temperature measured 18 degrees. [acquisition event-08-a; dependency shared]

Known group: shared. Expected origin: r-1; admission: KNOWN_GROUP.

Known shared dependence is not new evidence; unknown dependence requires deferral. Distinct receipt identity alone never establishes independence.

Pair change: Change supplied dependency metadata only; source identification must stay unchanged.

## CD-08-B: Warehouse probes / dependency

Report: The room temperature measured 18 degrees.

Claimed reference: none (untrusted). Authenticated edges: report → r-1.

Receipts: r-2: The room temperature measured 18 degrees. [acquisition event-08-b; dependency other]; r-1: The room temperature measured 18 degrees. [acquisition event-08-a; dependency new]

Known group: shared. Expected origin: r-1; admission: NEW_GROUP.

Known shared dependence is not new evidence; unknown dependence requires deferral. Distinct receipt identity alone never establishes independence.

Pair change: Change supplied dependency metadata only; source identification must stay unchanged.

## CD-09-A: Clock monitors / dependency

Report: The clock was within one second of the reference.

Claimed reference: none (untrusted). Authenticated edges: report → r-8.

Receipts: r-9: The clock was within one second of the reference. [acquisition event-09-b; dependency other]; r-8: The clock was within one second of the reference. [acquisition event-09-a; dependency unknown]

Known group: shared. Expected origin: r-8; admission: DEFER.

Known shared dependence is not new evidence; unknown dependence requires deferral. Distinct receipt identity alone never establishes independence.

Pair change: Change supplied dependency metadata only; source identification must stay unchanged.

## CD-09-B: Clock monitors / dependency

Report: The clock was within one second of the reference.

Claimed reference: none (untrusted). Authenticated edges: report → r-8.

Receipts: r-9: The clock was within one second of the reference. [acquisition event-09-b; dependency other]; r-8: The clock was within one second of the reference. [acquisition event-09-a; dependency new]

Known group: shared. Expected origin: r-8; admission: NEW_GROUP.

Known shared dependence is not new evidence; unknown dependence requires deferral. Distinct receipt identity alone never establishes independence.

Pair change: Change supplied dependency metadata only; source identification must stay unchanged.

## CD-10-A: Pump / path_conflict

Report: The transfer pump was off when sampled.

Claimed reference: none (untrusted). Authenticated edges: report → copy-one, report → copy-two, copy-one → r-15, copy-two → r-15.

Receipts: r-15: The transfer pump was off when sampled. [acquisition event-10-a; dependency new]; r-16: The transfer pump was off when sampled. [acquisition event-10-b; dependency other]

Known group: shared. Expected origin: r-15; admission: NEW_GROUP.

Two paths to one acquisition still resolve uniquely. A packet attributing the report to two distinct acquisitions has no unique origin under this contract.

Pair change: Change one authenticated branch endpoint from the same acquisition to a different acquisition.

## CD-10-B: Pump / path_conflict

Report: The transfer pump was off when sampled.

Claimed reference: none (untrusted). Authenticated edges: report → copy-one, report → copy-two, copy-one → r-15, copy-two → r-16.

Receipts: r-15: The transfer pump was off when sampled. [acquisition event-10-a; dependency new]; r-16: The transfer pump was off when sampled. [acquisition event-10-b; dependency other]

Known group: shared. Expected origin: DEFER; admission: DEFER.

Two paths to one acquisition still resolve uniquely. A packet attributing the report to two distinct acquisitions has no unique origin under this contract.

Pair change: Change one authenticated branch endpoint from the same acquisition to a different acquisition.

## CD-11-A: Valve / path_conflict

Report: The inlet valve was closed during the check.

Claimed reference: none (untrusted). Authenticated edges: report → copy-one, report → copy-two, copy-one → r-22, copy-two → r-22.

Receipts: r-23: The inlet valve was closed during the check. [acquisition event-11-b; dependency other]; r-22: The inlet valve was closed during the check. [acquisition event-11-a; dependency new]

Known group: shared. Expected origin: r-22; admission: NEW_GROUP.

Two paths to one acquisition still resolve uniquely. A packet attributing the report to two distinct acquisitions has no unique origin under this contract.

Pair change: Change one authenticated branch endpoint from the same acquisition to a different acquisition.

## CD-11-B: Valve / path_conflict

Report: The inlet valve was closed during the check.

Claimed reference: none (untrusted). Authenticated edges: report → copy-one, report → copy-two, copy-one → r-22, copy-two → r-23.

Receipts: r-23: The inlet valve was closed during the check. [acquisition event-11-b; dependency other]; r-22: The inlet valve was closed during the check. [acquisition event-11-a; dependency new]

Known group: shared. Expected origin: DEFER; admission: DEFER.

Two paths to one acquisition still resolve uniquely. A packet attributing the report to two distinct acquisitions has no unique origin under this contract.

Pair change: Change one authenticated branch endpoint from the same acquisition to a different acquisition.
