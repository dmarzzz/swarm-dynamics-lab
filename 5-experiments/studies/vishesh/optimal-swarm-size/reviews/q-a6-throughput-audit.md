# Q-A6 saved-data quality-adjusted throughput audit

2026-10-04 UTC; retrospective derived analysis, no new model calls. The prior post-mortem is retained. Correct throughput is final verified correct items / episode elapsed seconds; it is not an observed per-item correctness timeline. Same-author arithmetic, no independent validation.

| Root | Structure | Correct items/s N1 | Correct items/s N2 | Relative change | Correct items/USD N1 | Correct items/USD N2 |
|---|---|---:|---:|---:|---:|---:|
| 4 | parallel | 0.4417 | 0.6829 | +54.6% | 314.50 | 311.37 |
| 4 | chain | 0.0245 | 0.0257 | +5.0% | 13.26 | 16.55 |
| 5 | parallel | 0.4371 | 0.2938 | -32.8% | 266.11 | 142.13 |
| 5 | chain | 0.0000 | 0.0000 | undefined (both zero) | 0.00 | 0.00 |

The parallel throughput contrast reverses across the two roots. Chain throughput is limited by failed competence. Two task roots cannot estimate an optimal size, and item/call counts are not independent n. Full-task on-time success remains zero in all eight episodes. No changes to the original scorer, responses or denominators.

Accept DESIGN-TRANSFER advice to separate task correctness, actual total resources and concurrent capacity. Defer a broad N sweep and use Q-A7 to discriminate a worker input-binding failure at fixed N1. Adding many roots to the same competence floor is not justified; nor is switching models before testing a simpler interface explanation. The original public source and readback receipts are linked from [Q-A6 post-mortem](q-a6-post.md).
