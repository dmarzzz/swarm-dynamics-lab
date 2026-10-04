# Review waiver: SOC-07 v2 (soc07-private-judgments-v2), S0 to S1-L

Date: 2026-10-04 UTC. Carried over from the v1 waiver (`../soc07-private-judgments/launch/review-waiver.md`) by dmarz/orbital-orchestrator under dmarz's instruction, relayed by dmarz/fleet-monitor, to prepare this successor.

dmarz waived cross-researcher review by vishesh and shadow for SOC-07. This design version therefore proceeds **without** independent cross-researcher approval, without a reviewed survey for the question and without an accepted hypothesis.

Recorded here so that no later reader mistakes this for a reviewed run:

- Everything produced under this waiver is an exploratory development measurement. It is not reviewed evidence and must not be cited as such.
- dmarz/fleet-monitor reads the package (`reviews/chain-001-pre.md`) before it is queued. That is a same-researcher check, not the cross-researcher review that AGENTS.md asks for.
- The go for paid stages is dmarz's, recorded in `launch/s1-approval.json` only when he gives it. No approval record exists at the commit that adds this file.
- S2, the confirmation stage, is closed and is not authorized by this waiver.
- The software gate still applies: P0, S1-Q, S1-R and S1-L refuse to start unless `launch/s1-approval.json` is committed with the runtime fingerprint, the hash of the pre-run assessment and the hash of this file.
- If a later independent review finds a defect in this code or design, the affected results are suspect and the post-run review must say so.
