# Visualization mapping: influence-replay-v2

Parent mapping: ../../external-influence-v2/reviews/visualization-mapping.md. Bind every run to attempt quality-01, source/design/model hashes and assignment index; task, seed, domain, world, dose and arm remain visible.

Use the same analyst/check/decision layout, now separating **chair proposal** from **committed rule choice** and displaying scoped verified values and rule-disagreement. Initial/revision states come from response call indices; explicit verified_scorecard events mark evidence application. Cost-calculator outputs are observed-document transformations, not truth. Ground-truth coloring is evaluator-only and cannot enter agent contexts.

Logical time is ordered responses and ledger application; monotonic_seconds is available separately, not mixed into equal-step comparisons. Pending responses are gray; unavailable/stale checks show their status; malformed/failed outcomes have explicit error cards. No interpolation across missing responses. All raw events are append-only; complete replay is derivable without fresh model calls.

Live view: a bounded latest progress PNG, refreshed no faster than once per outcome. Final view: all-assigned outcome matrix and measured case replay. Supported public embeds are PNG and GIF; rich HTML player is a separate artifact, not assumed to embed in the live site. Renderer failure is a reporting defect recorded locally; it must not trigger model retries or alter outcomes. Final artifact-only regeneration is permitted.

Before paid launch, verify renderer dependencies on the allocated host, attach the semantic event-to-frame adapter for this version, test normal/pending/invalid transitions, verify stable agent IDs and matrix counts, and check actual public playback. Historical v2 rendering is already implemented; this version's live adapter is tested locally and remains part of deployment qualification, not an inherited capability.
