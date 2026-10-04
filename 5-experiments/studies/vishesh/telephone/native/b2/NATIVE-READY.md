# B2 native packet readiness — 2026-10-04

**Named delegated PI funding received for the unchanged B2 scope; live admission pending, no paid calls made.** The scope remains two qualification calls, followed conditionally by twelve roots × two policies × three hops × two fresh blocks. Sol50 is not included.

## Implemented and tested

The native entry point is `src/native.py`. It verifies every prepared manifest hash; opens only an existing original ledger; validates the finite admission receipt and transport hash; atomically reserves all 146 calls before qualification; and preserves every request, start marker, raw return, parent hash and usage receipt. A process interruption cannot silently free a started request. No retries, provider fallback or automatic successor exist.

The private admitted transport implements `post_json(request)`, declares `MAX_ATTEMPTS=1` and `TIMEOUT_SECONDS<=55`, and supplies the existing authorized bridge. The native worker discovers no credentials. Its CLI consumes a private admission receipt containing the named PI decision, portfolio reservation, immutable public plan/TLDR checks, verified runtime/account/claim/idle-host checks, deadline, existing infrastructure reservation and actual transport-source hash. Those operator attestations require real current evidence; this module does not itself query cloud accounts or create approvals. No admission receipt or bridge credential is checked into the repository.

`qualify` collects only the two frozen qualification packets. `main` requires saved response hashes plus an assessor's documented decision-rule/uncertainty review and checks actual GO/HOLD correctness. It verifies the same packet as qualification and writes an exclusive main-start marker, preventing a duplicate main dispatch. Changed source, invalid route/output/usage, expired deadline or absent parent stops the packet. Drift is recorded without intervention.

`src/report.py` replays all effective request/parent bindings and provider-generation identities, separates correctness/false GO/false HOLD/UNKNOWN/invalid/missing, computes paired terminal contrasts by block and root with missingness bounds, reports direct-source competence and repeat disagreement, and emits all 1008 semantic annotation slots. It does not mark semantic review or scientific reproducibility passed. The annotation validator rejects incomplete or unscored available responses, stale hashes and invented scores for missing outputs. Assertions outside target labels still require the frozen manual review.

## Offline acceptance

Run `python3 src/prepare.py` then `python3 -m unittest discover -s tests -v` from this B2 directory. There are **21 passing tests**, including the earlier thirteen packet checks and eight native/replay checks. Simulated full execution covers all 146 distinct requests; route failure stops with 143 main descendants unstarted; a bad semantic answer is retained for all planned hops; false qualification prevents main; packet reservation is atomic; modified parent context is detected; missing admission is rejected; and a crash start marker retains its reservation. These are local synthetic transport tests, not native model evidence. The full simulation uses a source controller and does not count toward fresh-run replication.

## Operator sequence after funding

1. Refresh original ledger/portfolio and obtain the exclusive approved-account allocation; reserve its full lifetime within the envelope. Publish and verify immutable plan and condition-specific summaries. Hash the actual private bridge and deployed source. Preserve all prior exposure.
2. Invoke `python3 src/native.py qualify --ledger ORIGINAL --admission PRIVATE_RECEIPT --transport PRIVATE_BRIDGE --out NEW_ATTEMPT`. No new ledger is accepted. The bridge must be the reviewed bounded OpenRouter consumer.
3. Inspect both saved native qualification responses and costs; write the hash-bound semantic review privately. On failure, stop and close out. No blind retry.
4. After refreshing current admission, invoke the same entry point with `main` and `--review PRIVATE_REVIEW`. Do not change the frozen packet between phases. Only this owning task dispatches.
5. Stop/verify the worker, replay and score saved data, and call `release_unstarted` only with verified worker-stopped evidence. Started/ambiguous requests retain exposure pending reconciliation. Settle infrastructure, complete operational finalize and scientific post-mortem, publish/read back safe evidence, and release the claim.

## Exact finite envelope and remaining gates

146 calls × USD 0.031744001 = **USD 4.634624146** maximum model exposure; infrastructure <= **USD 0.250000000**; total new exposure <= **USD 4.884624146**. Including historical **USD 0.113744701**, Telephone cumulative upper is **USD 4.998368847**. This fits the existing USD 5 study slice but must also receive a named reservation within the USD 200 project ceiling. No tier increase or new allocation is asserted. Input/output limits remain 8192 conservative input and 1536 output tokens; no capacity reduction was made to fit the cap.

Outstanding live gates: fresh original-ledger/portfolio reconciliation; real exclusive approved-account allocation and runtime/transport evidence; immutable public registration; two native qualification responses and semantic review. No further scientific proposal is needed unless an actual gate failure changes scope. Source and cases are ready for this bounded benchmark; stable useful native results remain unobserved.

## Delegated funding and anchor preservation

The PI approved the unchanged B2 scientific packet anchored at de3653d1763a40d3cbfb60ef0a29e7e4bbd12bdf, allowing routine dispatcher implementation under the exact finite envelope above. The anchor manifest hash was checked against the private decision; actor packets, gold, assignment order and SCORING.md remain byte-identical. This records delegated PI authority, not a new direct owner instruction. Implementation/source and live admission are refreshed before any paid dispatch. No Sol50, AI Village, extra attempts, fallback or new virtual machine is included.
