# Original development casebook

These are invented, inspected software fixtures. Each root adds “The archive contains three records” and “Review is still pending” as two unchanged obligations. This shared scaffolding further limits independence. No Village record is quoted.

| Family | Source statement | Changed statement at hops 2–3 | Changed field |
|---|---|---|---|
| qualification | A prototype may work; no test has been performed. | The prototype has been tested and works. | modality |
| attribution | Sensor A measured the temperature; sensor B did not measure it. | Sensor B performed the temperature measurement. | attribution |
| scope | Two checked records passed, with no claim about other records. | Every record passed the audit. | scope |
| time | The gate was open at 14:00; later state is not reported. | The gate is open now. | time |
| correction | The count of 12 was corrected to 9; the current count is 9. | The current count is 12 items. | value_unit |
| dependence | Two reports reference one acquisition, so they are one evidence source. | The two reports provide two independent acquisitions. | value_unit |
| unavailable | The linked receipt is unavailable, so approval is unverified. | The missing receipt confirms verified approval. | modality |
| polarity | The recorded deployment failed; the report link resolves to that failure. | The recorded deployment succeeded. | predicate |

Each root has faithful, distorted and omitted trajectories. Hop 1 is faithful in all trajectories. Faithful scores are [1, 1, 1]; distorted and omitted scores are [1, 2/3, 2/3]. Distortion adds one contradicted assertion at hops 2–3; omission adds none. All 24 trajectories and 72 outputs reconcile in [the result file](FIXTURE-RESULTS.json).

Direct copy and exact lookup use only source records and receive all required source IDs. Both preserve all obligations. These baselines do not solve constrained selection or compression because the fixtures impose neither. Future task construction must establish a useful real task under an explicit common information/output budget before a model comparison is warranted.

Fault tests additionally cover annotation tampering, unknown additions, contradictions, duplicates, missing/invalid outputs, source lookup faults, reordering and evaluator metadata changes. Labels and tests are same-author checks, not independent semantic adjudication.
