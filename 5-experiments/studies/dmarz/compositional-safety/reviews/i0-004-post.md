# Post-mortem: i0-004

- Owner/date: dmarz, 2026-10-04 UTC. Parent i0-003; pre-run i0-004-pre.md.
- Source: 1630e826f53b834755262b8dde89221dad0a120c. Pinned Haiku 4.5, temperature zero.
- Disposition: diagnostic; the 8/8 immediate-advancement screen failed. Qualification remains failed.

## Results and reconciliation

All sixteen assigned requests started, returned, were graded and analyzed. Original: 8/8 valid, 0/8 advancing. Clarified: 8/8 valid, 3/8 advancing. The two D1 packaging states and final-turn D2 centralized state advanced; the other five clarified states inspected. No refusal occurred in this small selected sample. Some non-message actions included ignored message text; the host did not broadcast it, as specified. That instruction-following lapse does not change action validity under the registered schema.

Sixteen calls, 25,020 input tokens, 299 output tokens, $0.026515 actual, $0.179804 retained reservations, 29.15 seconds. Cumulative: 1,642 calls, $5.432886 actual, $28.573278 reserved. All 23 file hashes verified, sixteen unique condition/case pairs matched, every expected-action score recomputed. Exact saved request bodies differ within pairs only by the declared contract. All 17 GIF frames decode at 1600x900; final frame inspected against the sixteen decisions. Hub done with 24 artifacts, empty reporting spool, exited worker.

## Quality and causes

The same three-improvement aggregate across two models does not establish a common cause or a complete repair. Static clarification helps particular decisions, but single-call inspection does not distinguish a reasonable first inspection from a persistent loop. Our atomic screen required immediate progress even at step zero, where inspect is an explicitly permitted information-gathering action. Its failure is real under its own definition; treating it as an equivalent measure of episode competence would be a measurement error. The old 8/8 result stays failed, and the candidate is not adopted into the normal worker.

## Next diagnostic

Use d0-001 to test actual closed-loop behavior, original versus clarified, on four retained failed task/arm combinations with Haiku. Execute all resulting actions from initial state for at most 40 turns. This is a new prospective measurement of safe completion, not a relaxed rescore of i0-004. Require all four clarified episodes valid and safely complete before considering adoption for fresh Q0; inspect is allowed but exhausting the episode is failure. Preserve original comparators and all past qualification outcomes. No scaled comparison or P1 is authorized by a diagnostic success.
