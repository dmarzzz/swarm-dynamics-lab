# 2026-10-04, dmarz/pipeline-split

Builder for the pipeline lead dmarz/pipeline. Task: build-sybil-split-opus. Nothing was launched and no model call was made.

- Built `researchers/dmarz/notes/sybil-split-opus/` to launch-ready under the ready-chain contract: plan and frozen design (f3e294c5), code and manifest (88fcf92a, 0b8a444a), pre-run review with status ready (e74378d5 and the documents-only commit after it). Code commit 0b8a444af0b08dfd80c06bc577ae30547ed35343, source hash 95889beafbd40142ea68c52b4a00e2b1dbbbc10794f967cba3e00ca1767f3089.
- Offline evidence on the code commit: 55 selftests pass; scripted S0 1,853 of 1,853 rows valid with no invariant violation; manifest regenerates identically (also under Python 3.12); the rehearsal against a throwaway local hub with a stubbed model endpoint runs all four stages and, with a stub that never abstains, stops at Q0 with nothing queued for S1.
- What surprised me: with attachment edges fixed and no links among the attacker's own identities, a 27-way split is almost never admitted, so one end of the note's primary contrast sits at zero. Harm peaks at an intermediate identity count (9), where each identity is connected enough to be seated and too small to be checked by a degree-first policy. The frozen design links the attacker's identities in a ring (free, as in the parent's attacker); on engineering roots the scripted primary is +0.41 with those links and +0.01 without. That dependence is stated in the README and the setup record.
- Also noted: 1,554 of the 2,688 comparison assignments have a packet identical to another cell of the same root, almost always the same cell at the other check strength, because no attacker identity was checked there. They are kept as a test-retest measure.
- Next, for whoever continues: the lead's review, the fleet monitor's same-researcher check, then the run request. After a run: post-mortem per RUN-REVIEW.md, evidence row and README results from the saved analysis.

## trust-credit-qwen (program v5, line T)

- Built `researchers/dmarz/notes/trust-credit-qwen/` to launch-ready: plan 32f751b0, code baefdb6b (source hash ddc370fd...), then READY.yaml, runbook, visualization mapping and the pre-run review. Nothing launched, no model call.
- Offline evidence on the code commit: 68 selftests (28 are the reference adapter's); scripted S0 216 of 216; rehearsal passes the full chain, a failed-qualification stop and a billing stop with resume in 73 s.
- What surprised me: the primary is positive and large on engineering roots (+23.4 seats), but direct-only credit does not make admission safer in level: at 32 checks it seats about 20 attacker identities where propagated credit seats about 2. The budget escalation and the level are different questions; the README reports both.
- The propagated rule equals the budget study's ranking exactly when no identity is dangling; with a dangling identity the seat sets differ by 6 to 13 seats (attacker seats by at most 1).
- Amendment A1 (before any run): took the revised reference adapter (main 639e9501), reservation margin 10, voided reservations on a billing stop, caps per batch family; new code commit d3219ceb, source hash e24e85f5...; 73 selftests, offline S0 and the rehearsal pass again.
