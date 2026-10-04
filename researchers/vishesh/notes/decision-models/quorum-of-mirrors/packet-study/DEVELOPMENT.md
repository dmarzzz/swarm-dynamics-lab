# Development packet explorer
48 packets / 12 authored roots. Each source set is fixed across four conditions. Exact expected answers below are development labels, not native results.
## development-polarity-0
Query: {"kind": "running", "entity": "workshop-32886", "time": "10:00"}
Source receipts:
- 6b20e5bbb6: At 10:00, workshop-32886 was not running.
- d510e49602: At 10:00, workshop-32886 was not stopped.
- d18aee8ffa: At 10:00, workshop-32886 was not running.
Expected source decision: **ZERO**. Focal source: d510e49602.
| Copies | Inverted | Report-vote | Deduplicated claims | Source-parser |
|---|---|---|---|---|
| 1 | False | ZERO | ZERO | ZERO |
| 1 | True | ZERO | ZERO | ZERO |
| 5 | False | ONE | ZERO | ZERO |
| 5 | True | ZERO | ZERO | ZERO |
## development-polarity-1
Query: {"kind": "running", "entity": "loading-98004", "time": "11:00"}
Source receipts:
- 39eb1961a3: At 11:00, loading-98004 was not stopped.
- 76e62de25e: At 11:00, loading-98004 was running.
- 49d0ba1447: At 11:00, loading-98004 was not running.
Expected source decision: **ONE**. Focal source: 39eb1961a3.
| Copies | Inverted | Report-vote | Deduplicated claims | Source-parser |
|---|---|---|---|---|
| 1 | False | ONE | ONE | ONE |
| 1 | True | ZERO | ZERO | ONE |
| 5 | False | ONE | ONE | ONE |
| 5 | True | ZERO | ZERO | ONE |
## development-time-0
Query: {"kind": "running", "entity": "workshop-37284", "time": "11:00"}
Source receipts:
- 7b8d307f06: At 08:00, workshop-37284 was stopped. / At 11:00, workshop-37284 was running.
- 3bf21f027c: At 08:00, workshop-37284 was running. / At 11:00, workshop-37284 was stopped.
- 78d45919db: At 08:00, workshop-37284 was running. / At 11:00, workshop-37284 was stopped.
Expected source decision: **ZERO**. Focal source: 7b8d307f06.
| Copies | Inverted | Report-vote | Deduplicated claims | Source-parser |
|---|---|---|---|---|
| 1 | False | ZERO | ZERO | ZERO |
| 1 | True | ZERO | ZERO | ZERO |
| 5 | False | ONE | ZERO | ZERO |
| 5 | True | ZERO | ZERO | ZERO |
## development-time-1
Query: {"kind": "running", "entity": "loading-44212", "time": "11:00"}
Source receipts:
- ecfba54343: At 08:00, loading-44212 was running. / At 11:00, loading-44212 was stopped.
- 9214897da7: At 08:00, loading-44212 was stopped. / At 11:00, loading-44212 was running.
- 8c2457aaa5: At 08:00, loading-44212 was stopped. / At 11:00, loading-44212 was running.
Expected source decision: **ONE**. Focal source: 8c2457aaa5.
| Copies | Inverted | Report-vote | Deduplicated claims | Source-parser |
|---|---|---|---|---|
| 1 | False | ONE | ONE | ONE |
| 1 | True | ZERO | ZERO | ONE |
| 5 | False | ONE | ONE | ONE |
| 5 | True | ZERO | ZERO | ONE |
## development-entity-0
Query: {"kind": "running", "entity": "workshop-66025", "time": "11:00"}
Source receipts:
- 13dfacfd00: At 11:00, workshop-66025-other was stopped. / At 11:00, workshop-66025 was not stopped.
- fdaf98da03: At 11:00, workshop-66025-other was running. / At 11:00, workshop-66025 was stopped.
- fa79faa450: At 11:00, workshop-66025-other was running. / At 11:00, workshop-66025 was stopped.
Expected source decision: **ZERO**. Focal source: 13dfacfd00.
| Copies | Inverted | Report-vote | Deduplicated claims | Source-parser |
|---|---|---|---|---|
| 1 | False | ZERO | ZERO | ZERO |
| 1 | True | ZERO | ZERO | ZERO |
| 5 | False | ONE | ZERO | ZERO |
| 5 | True | ZERO | ZERO | ZERO |
## development-entity-1
Query: {"kind": "running", "entity": "loading-58352", "time": "16:00"}
Source receipts:
- cd412c993b: At 16:00, loading-58352-other was stopped. / At 16:00, loading-58352 was not stopped.
- f8d8d4923e: At 16:00, loading-58352-other was stopped. / At 16:00, loading-58352 was not stopped.
- 82f121507b: At 16:00, loading-58352-other was running. / At 16:00, loading-58352 was not running.
Expected source decision: **ONE**. Focal source: f8d8d4923e.
| Copies | Inverted | Report-vote | Deduplicated claims | Source-parser |
|---|---|---|---|---|
| 1 | False | ONE | ONE | ONE |
| 1 | True | ZERO | ZERO | ONE |
| 5 | False | ONE | ONE | ONE |
| 5 | True | ZERO | ZERO | ONE |
## development-units-0
Query: {"kind": "mass", "entity": "workshop-12309", "time": "14:00", "threshold_grams": 5000}
Source receipts:
- aec07478fe: At 14:00, workshop-12309 measured 6 kilograms.
- 2a38ce80a1: At 14:00, workshop-12309 measured 4000 grams.
- ee32e008bb: At 14:00, workshop-12309 measured 4000 grams.
Expected source decision: **ZERO**. Focal source: aec07478fe.
| Copies | Inverted | Report-vote | Deduplicated claims | Source-parser |
|---|---|---|---|---|
| 1 | False | ZERO | ZERO | ZERO |
| 1 | True | ZERO | ZERO | ZERO |
| 5 | False | ONE | ZERO | ZERO |
| 5 | True | ZERO | ZERO | ZERO |
## development-units-1
Query: {"kind": "mass", "entity": "loading-25458", "time": "11:00", "threshold_grams": 5000}
Source receipts:
- 6175992ae6: At 11:00, loading-25458 measured 6000 grams.
- edca602d9f: At 11:00, loading-25458 measured 4 kilograms.
- b1e15f3d50: At 11:00, loading-25458 measured 6 kilograms.
Expected source decision: **ONE**. Focal source: 6175992ae6.
| Copies | Inverted | Report-vote | Deduplicated claims | Source-parser |
|---|---|---|---|---|
| 1 | False | ONE | ONE | ONE |
| 1 | True | ZERO | ZERO | ONE |
| 5 | False | ONE | ONE | ONE |
| 5 | True | ZERO | ZERO | ONE |
## development-modality-0
Query: {"kind": "running", "entity": "workshop-13972", "time": "11:00"}
Source receipts:
- 00e6a74db3: Plan: at 11:00, workshop-13972 will be stopped. / Observation: At 11:00, workshop-13972 was running.
- a0a219b7d1: Plan: at 11:00, workshop-13972 will be running. / Observation: At 11:00, workshop-13972 was not running.
- c5128f83e7: Plan: at 11:00, workshop-13972 will be running. / Observation: At 11:00, workshop-13972 was not running.
Expected source decision: **ZERO**. Focal source: 00e6a74db3.
| Copies | Inverted | Report-vote | Deduplicated claims | Source-parser |
|---|---|---|---|---|
| 1 | False | ZERO | ZERO | ZERO |
| 1 | True | ZERO | ZERO | ZERO |
| 5 | False | ONE | ZERO | ZERO |
| 5 | True | ZERO | ZERO | ZERO |
## development-modality-1
Query: {"kind": "running", "entity": "loading-84734", "time": "13:00"}
Source receipts:
- c5b48cb595: Plan: at 13:00, loading-84734 will be stopped. / Observation: At 13:00, loading-84734 was not stopped.
- cbb1b4ecfb: Plan: at 13:00, loading-84734 will be stopped. / Observation: At 13:00, loading-84734 was not stopped.
- bbae6ee01f: Plan: at 13:00, loading-84734 will be running. / Observation: At 13:00, loading-84734 was not running.
Expected source decision: **ONE**. Focal source: c5b48cb595.
| Copies | Inverted | Report-vote | Deduplicated claims | Source-parser |
|---|---|---|---|---|
| 1 | False | ONE | ONE | ONE |
| 1 | True | ZERO | ZERO | ONE |
| 5 | False | ONE | ONE | ONE |
| 5 | True | ZERO | ZERO | ONE |
## development-correction-0
Query: {"kind": "running", "entity": "workshop-36852", "time": "14:00"}
Source receipts:
- e19c681e98: Initial: at 14:00, workshop-36852 was running. / Correction: At 14:00, workshop-36852 was not running.
- b8d3ea7196: Initial: at 14:00, workshop-36852 was stopped. / Correction: At 14:00, workshop-36852 was not stopped.
- 7b287d87fc: Initial: at 14:00, workshop-36852 was running. / Correction: At 14:00, workshop-36852 was stopped.
Expected source decision: **ZERO**. Focal source: b8d3ea7196.
| Copies | Inverted | Report-vote | Deduplicated claims | Source-parser |
|---|---|---|---|---|
| 1 | False | ZERO | ZERO | ZERO |
| 1 | True | ZERO | ZERO | ZERO |
| 5 | False | ONE | ZERO | ZERO |
| 5 | True | ZERO | ZERO | ZERO |
## development-correction-1
Query: {"kind": "running", "entity": "loading-96385", "time": "15:00"}
Source receipts:
- eacfe71bbd: Initial: at 15:00, loading-96385 was running. / Correction: At 15:00, loading-96385 was not running.
- a8dd86ab42: Initial: at 15:00, loading-96385 was stopped. / Correction: At 15:00, loading-96385 was not stopped.
- 473014fefb: Initial: at 15:00, loading-96385 was stopped. / Correction: At 15:00, loading-96385 was not stopped.
Expected source decision: **ONE**. Focal source: a8dd86ab42.
| Copies | Inverted | Report-vote | Deduplicated claims | Source-parser |
|---|---|---|---|---|
| 1 | False | ONE | ONE | ONE |
| 1 | True | ZERO | ZERO | ONE |
| 5 | False | ONE | ONE | ONE |
| 5 | True | ZERO | ZERO | ONE |
