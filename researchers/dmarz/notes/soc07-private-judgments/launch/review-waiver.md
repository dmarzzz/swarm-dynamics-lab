# Review waiver: SOC-07 private judgments, S0 and S1

Date: 2026-10-04 UTC. Decision by dmarz (owner), relayed to dmarz/soc07-private by the session that operates as dmarz/fleet-monitor.

dmarz waived cross-researcher review by vishesh and shadow for this experiment. The only reviewer is dmarz/fleet-monitor, an agent of the same researcher who owns the study. This launch therefore proceeds **without** independent cross-researcher approval, without a reviewed survey for the question and without an accepted hypothesis.

Recorded here so that no later reader mistakes this for a reviewed run:

- Everything produced under this waiver is an exploratory engineering and development measurement. It is not reviewed evidence and must not be cited as such.
- dmarz/fleet-monitor reviews the code and the pre-run assessment (`reviews/s1-pre.md`) and sends an explicit go before any model call. That is a same-researcher check, not the cross-researcher review that AGENTS.md asks for.
- S2, the 960-world confirmation, is closed and is not authorized by this waiver. Opening it needs the normal gates: a reviewed survey, an accepted hypothesis, a joint power simulation and a fresh review.
- The software gate still applies: paid stages refuse to start unless `launch/s1-approval.json` is committed with the runtime fingerprint, the hash of the pre-run assessment and the hash of this file.
- If a later independent review finds a defect in this code or design, the affected results are suspect and the post-run review must say so.
