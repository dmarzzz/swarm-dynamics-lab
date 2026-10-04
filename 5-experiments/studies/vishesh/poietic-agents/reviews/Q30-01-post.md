# Q30-01 native closeout

**Reviewed; both candidate configurations failed readiness.** Frozen source `e91876daafb66a4521f70f78cc68a517a611a702`. Execution and accounting completed; qualification failed; no30-member swarm comparison occurred. All96assignments retained:25started and71unstarted. Researcher review not required by owner direction.

| Candidate | Started /48 | Full contract valid /48 | Exact correct and executed /48 | Decision |
|---|---:|---:|---:|---|
| GPT-6 Luna / OpenAI |19|18|16|Failed: invalidJSON at case4step2|
| Mistral Nemo / DeepInfra FP8 |6|5|4|Failed: wrong answer value type at case1step1|

The first invalid response correctly stopped each role. Luna returned two identical fetch objects separated by stray non-JSON text. This is not an admissible single-fence wrapper and was not repaired. Nemo returned a combined object containing three task answers instead of the current inventory task's required list. The entire list/object contract was present in its effective input. Missing nested schema no longer explains that failure, though unnecessary cross-task instructions are a plausible contributor, not a verified cause.

Three additional valid but wrong answers remain: Luna calculated delivery shortfall6instead of7 and included an inventory entity that did not meet the threshold; Nemo chose a more expensive eligible supplier. These are semantic errors, not transport or JSON errors. Other reviewed operations included successful retrieval, source-version refresh, tool restoration, service registration/delivery and program installation/execution. These successes do not qualify either model. No protected access was observed. No transport failure or uncertain new charge occurred.

## Trace, accounting and process audit

The owning agent inspected all25effective requests and visible responses, reconstructed their contexts/expected actions, replayed24parseable actions and independently reproduced theJSONfailure. All25billing receipts replay. All96aggregate outcomes recompute. This is same-author review, not independent replication or access to hidden reasoning. Private raw responses stay in the study archive; [trace coverage](../results/Q30-01/trace-review.json) and [artifact manifest](../results/Q30-01/artifact-manifest.json) preserve provenance.

The prospective plan was immutable, publicly registered and visibly verified before dispatch; deployed138tests passed, current account/host/trust/claim checks passed, and the preexisting54ledger rows remained unchanged. All six public aggregate artifact readbacks match; the final figure was inspected and shows the48assigned denominator and unstarted count per role. Worker/children, relay and tunnel are stopped. Claim419 was released by424; existing machine retained.

Native run elapsed46.80seconds. NewAPIcostUSD0.002548557 is fully settled. Claim354seconds addsUSD0.00702395 infrastructure. Original ledger79calls, totalAPIexposureUSD0.499330521, cumulative infrastructureUSD0.10087503333333334; conservative totalUSD0.6002055543333333 of ownerUSD10. All38historical uncertain calls remain in the bound. [Cost closeout](../results/Q30-01/cost-closeout.json).

## Interpretation and next decision

These exact cheap-model configurations are unsuitable for the admitted main comparison under its unchanged gate. There is no evidence here about swarm differentiation, service emergence or efficiency.12dependent lifecycle cases were assigned per model; early stopping prevents an unbiased comparative model ranking or broad error-rate estimate.

A fresh GPT-OSS120B/20B qualification is a useful bounded readiness test because neither has been measured on this contract, both are inexpensive enough for the requested30-member scope, and a different reasoning-model family can succeed or fail without modifying old answers or relaxing gates. [Q30-02](../Q30-02-PLAN.md) keeps task/prompt/schema/threshold unchanged, uses disjoint fresh roots and explicitly changes model/configuration together. Passing would permit main-run preparation; failure blocks that pair. Noautomatic main launch or open-ended retry.

The closed-loop30-member scheduler has also been implemented offline with five tests: balanced paired assignments/6360call ceiling, hand-authored public-data controller, actual backend-role switching, capability-floor missingness and transport/deadline stops. This is scripted mechanism evidence only; main budget authority amendment, instrument controls and runtime admission remain incomplete.
