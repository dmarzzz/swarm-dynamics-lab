# D8: matrix contract repaired; typed request rejected

Retrospective closeout,2026-10-04. [Native run](https://swarm-live.pages.dev/#/r/influence-swarms%2F1004-190842-cd6b82), [immutable plan](https://github.com/dmarzzz/swarm-lab/blob/682429057a8d77f527d88b10d02bcac5610152f4/researchers/vishesh/notes/influence-swarms/scenario/ITERATION-08-PREP.md), [audit](D8-audit.json), [saved response and summary](native-D8-01/summary.json).

| Assigned contract | Acquisition | Contract outcome | Reported cost |
|---|---|---|---|
| Matrix reviewer | Complete Haiku4.5/Anthropic response | Valid JSON and usage | $0.008518 |
| Typed reviewer | HTTP400 | No answer; cause unresolved | Unknown |

## What this establishes

The corrected wire delivered the original schema through OpenRouter response_format, with a JSON-only instruction. The first matrix request completed, passed the original strict validator and retained complete usage. This is a successful operational repair of D7's schema omission. The second typed request returned400. Both requests retain exact bytes/hashes; no retry, substitute model or third request occurred. Overall qualification fails because both contracts were required. OpenRouter acquisition works for the matrix; the direct Anthropic credential's earlier429 remains unexplained and was not tested again.

The typed400 cannot yet be attributed to schema complexity, a specific unsupported keyword, billing or another provider condition. The relay applied an Anthropic-only error-envelope classifier and produced a generic malformed label. That classifier cannot recognize a valid OpenRouter envelope. It deliberately discarded raw text, so the actual body's shape and retrospective cause classification are unavailable. This telemetry defect is owned by the instrument. [Post-D8 offline repair](../POST-D8-REPAIR.md) adds bounded recognition of outer and nested OpenRouter errors with fixed reason labels, never raw error retention.99 offline tests now pass; the historical D8 source is unchanged and this helper is not yet deployed into a new admitted relay.

Both schemas have zero optional parameters and zero union parameters. They do not violate Anthropic's documented24/16 explicit limits on those dimensions. Its [documentation](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) also describes internal grammar-size limits that can produce400; that remains a hypothesis here, not a diagnosed cause. Do not call a local schema check proof of provider acceptance or simplify the schema to obtain a favorable run without a prospective decision.

## What the matrix answer reveals, retrospectively

[Source arithmetic and field audit](D8-matrix-retrospective.json) score13/15 classifications correct. Cobalt's software-only cost is below the budget and buyer-weighted coverage exceeds the minimum, but the answer marks both FAIL while discussing total operating cost. This is the same cross-field contamination the typed-fact architecture was intended to address. It is a concrete failure mode worth investigating; typed collection is still missing, so there is no architecture comparison.

The reviewer selects Birch while marking deployment scope UNKNOWN for all three candidates. The source-based purchase choice is DEFER; applying the existing shadow action guard to the raw checklist also yields DEFER. No chair or purchase execution occurred in this diagnostic. A provisional reviewer preference is not an executed purchase, and the guard's refusal does not repair the reasoning. Report these distinctions rather than calling schema validity safe decision-making.

This secondary audit is retrospective on one previously inspected case. Fifteen dependent fields are not fifteen independent samples. It supports neither a fresh generalization estimate nor a causal effect of schema formatting. The two-row status table is the appropriate visualization for this short acquisition diagnostic; animation would imply an unmeasured interaction.

## Execution, accounting and closeout

Source `682429057a8d77f527d88b10d02bcac5610152f4`,96 tests passed in the actual pinned runtime. Public packet bytes were verified anonymously; both native wire hashes match. The immutable plan and both condition-specific TLDRs were registered and read back before dispatch. Dedicated existing capacity matched the approved account and current exclusive claim. The key remained in the local relay. No new machine was created.

Two pre-dispatch operator problems were contained without model calls: a stage-name text replacement corrupted the deployment helper's source hash, which was corrected against the published commit; an initial check-only refusal was followed by a clean credential-free preflight on the unchanged source. The initial refusal's detailed cause was not retained. Neither was a model attempt or a reason to reset the ledger. The launch itself passed current admission and normal platform review.

D8 addedUSD0.097280 conservative reservation for two calls. Original ledger capUSD8, cumulative reservationUSD5.063392, physical calls250, unreservedUSD2.936608. Known D8 subtotalUSD0.008518; total actual charge remains unknown because the rejected typed request supplied no usage. Preserve that reservation and all earlier uncertain charges. No failure is counted as free.

Worker exited, zero blocking model processes remained, local relay and remote forwarding ports closed, six native hub artifacts were verified and collected, and the allocation was released. Operational finalization and the separate eleven-dimension scientific assessment are complete. No successor is running. The next decision should resolve the typed acquisition failure with correct telemetry before any broader behavioral cohort; this closeout authorizes no further call.
