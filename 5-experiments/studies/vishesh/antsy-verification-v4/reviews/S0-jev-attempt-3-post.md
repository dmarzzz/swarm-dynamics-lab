# Jev S0 attempt 3 post-mortem

Source cd04c38. Qualification completed all 10 receipts and 70 arm outcomes with zero new failures. It replayed 68 recorded responses, including one locally revalidated rounded vector with explicit provenance, and made the remaining 52 calls. All 120 reconstructed invocations are valid under the documented representation rule. Both previous failed attempts remain preserved; this is not a claim that the entire qualification history was error-free.

No valid action was rerolled or changed. All budgets, labels, route and usage checks passed. PNGs and six measured replays uploaded. The renderer now identifies each voting role rather than showing an unlabeled vote list; this is a presentation change only. There is no fabricated agent movement or hidden score in the pre-commit frames.

The screen is scientifically sobering: Jev adaptive and fixed committees both recover 0.4693 annotated-token recall, below confidence-only 0.5025 and random checks 0.5139. Single-agent scores 0.4056. Every model arm spends both checks. The committee helps relative to this single-agent policy but not the strongest cheap controls. Ten receipts do not establish a general ranking. Do not tune the policies to reverse this observation.

Decision: proceed once to the frozen 70-receipt Jev S1 comparison under cd04c38, maximum 840 new requests, same calibration, controls, corpus SHA and shared budget. Publish its condition TLDR first. The endpoint's returned probability precision is now handled without normalization; probabilities remain uncalibrated decision scores. Future API changes may still cause an honest stop rather than a silent fallback.
