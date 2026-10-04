# Controller schema repair after A7

Prospective offline implementation plan,2026-10-04. Owner requested fixing the controller schema after the A7 diagnostic. This is implementation authorization, not a new model run.

Replace dependent action/service/version constraints with one string enum `action_id` and a separate required string `reason`, in a closed object. IDs expose their meaning: `inspect`, `refresh`, `wait`, and `deploy:<service>:<version>`. Build the exact legal catalog from each fixture, including same-version restarts; maintain a one-to-one strict mapping to the unchanged simulator action. Invalid IDs, extra keys, wrong types and legacy action objects must fail closed without fuzzy parsing or default actions. Decoding preserves reason verbatim.

Show the ID-to-action mapping in the controller observation, not in advisor inputs. Preserve the raw response before decoding and record the decoded action before execution. Add a contract version and module hash to manifests. Keep previous commits and native results immutable. Existing A5/A6 live entry points must refuse to execute the new contract without a newly admitted plan; scripted checks remain available. No paid calls or allocation for this repair.

Validate all legal/illegal combinations against the previous exact schema and actual simulator across every scenario; test unknown IDs, wrong types and extra fields, same-version restart and complete scripted qualification/reconciliation. Retain the A5 invalid inspect regression. The two-field enum avoids the rejected composition, but offline validation is not hosted acceptance. Native interface and semantic qualification remain outstanding; do not claim that this fixes the advisors' catalog errors.

## Implemented and verified

The flat two-field contract is integrated in both controller paths.34tests pass: exact legal-action equivalence across all six scenarios, malformed-response rejection, simulator equivalence, untouched advisor observation and six-episode scripted qualification with raw/decoded replay. [Evidence](reviews/controller-schema-repair.json). No model calls, allocation or extra spend. Hosted acceptance and native semantic qualification remain untested. Existing native entry points refuse the changed contract before creating output or calling a provider; historical commits remain replayable.
