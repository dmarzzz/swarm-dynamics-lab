# V2 execution record

Published protocol: bcba39e. Isolated deployed revision: 810cc177199d95ef45f4fcd451aecc3553485333. The existing v1 process and checkout were left untouched. Deployment tests: 17 passed. Repository validation: zero errors, five pre-existing missing-library-link warnings.

Completed scripted runs were imported with their original manifests, event journals and outcomes; they were not rerun on the server. The hub import timestamps identify publication time, while manifest started_unix records execution time.

- immune-response/v2-scripted-s0-072061fe: 32 outcomes, zero invalid.
- immune-response/v2-scripted-s1-072061fe: 256 outcomes, zero invalid.
- immune-response/4deeb0f2: native Haiku S0, task 6200, shared_evidence, eight arms; launched 2026-10-04 00:43 UTC on research-01. Running at handoff; no model-result claim yet.

Native execution uses the existing shared USD 45 API ledger. Remaining conservative reservations before launch: USD 39.757886, above the USD 36.980736 maximum v2 reservation bound. No server was provisioned. Credentials were consumed from the authorized local Keychain via SSH stdin and process memory, never written into these records.

Native artifacts upload through the worker on completion. A finite postprocessing step also attaches factorial-analysis.json and the all-assigned primary contrast to the same hub run; it does not retry outcomes or launch S1. Generic summary bootstrap intervals are not meaningful for this one-world native qualification. The postprocessor waits up to three hours, then exits without changing original outcomes if completion artifacts never arrive.

Local orchestration checkout: /private/tmp/swarm-immune-v2. Server checkout: /srv/swarm/vishesh-immune-v2. Worker log: native-s0.log. Postprocessing log: postprocess-native.log. The logs must be inspected with narrow filtering, not dumped, because future provider diagnostics may contain sensitive context.
