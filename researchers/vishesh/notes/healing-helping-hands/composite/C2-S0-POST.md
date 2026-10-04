# C2-S0 post-mortem and cycle closure

2026-10-04 UTC. Source `33a71ee5c7291cebe8aae468b3c8393ad4b4992f`. Decision: **blocked for scientific comparison; bounded cycle closed, no further automatic attempt**.

Assigned 60: zero complete, one failed, 59 not run. One Qwen response completed; the first Jev relay connection failed locally after 0.002713 seconds with URLError. Total worker runtime 4.719 seconds. The SSH tunnel had terminated with a server-not-responding timeout. Original ledger has zero C2 slots and remains at 859 entries: no C2 request reached the provider and no C2 API charge occurred. The Qwen response is retained and is not a successful composite qualification.

The original preflight checked host, workload, source, budget and public registration but omitted end-to-end relay readiness. That is an admission defect. The repair adds a GET /health endpoint and checks live attempt, stage and remaining relay lifetime before creating a run or calling Qwen. Nineteen offline composite tests pass, including disconnected/wrong-stage/wrong-attempt/stale-relay refusal, uncertain-spend retention and diagnostics that exclude exception text. Twenty-two practical-engine tests also pass. The new health guard has not been qualified by another native run, and does not guarantee that a connection cannot drop during a run. A future attempt needs a new prospective admission and a supervised transport design; it must preserve this lineage and ledger.

Public C2 registration was verified from the worker and rendered in the browser through a temporary GET-only view of the public site, because local DNS for the public hostname failed. The site's documented ?api mode was used; example data were explicitly rejected. No private hub endpoint or credential was proxied. This workaround verified the public page but did not cure the model relay.

C1-S0 remains valid and separately published: Qwen+Jev 60/60, Jev-only 60/60, Qwen-only 36/60. C1-S1 and C2-S0 remain failed. There is no completed 200-curator composite comparison, no demonstrated incremental Qwen benefit and no claim of reliable end-to-end operation.
