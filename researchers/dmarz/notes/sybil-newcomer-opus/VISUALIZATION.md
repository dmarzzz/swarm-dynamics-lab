# Visualization mapping v1 (inherited)

This study uses [sybil-newcomer-api mapping v1](../sybil-newcomer-api/VISUALIZATION.md) unchanged: same recorded fields, encodings, colors (random gold, reputation violet, renewal teal), logical-round cursor, eight-frame S0/S1 replay, nine-frame Q0 completion-prefix GIF, 1800×1200 final PNG, at most one live progress upload per twenty seconds, and the same missing/failed-observation rules. The renderer is copied byte for byte apart from the banner, which reads `OPUS 5.5`.

## Run bindings

Each attempt binds the mapping to experiment `sybil-newcomer-opus`, design v1, its recorded `source_hash` and code commit, the hub run ID, and the world/identity/strategy/arm keys of every assignment, recorded in [DEPLOYMENT.md](DEPLOYMENT.md) and in each run's `summary.json` (`visualization.mapping = v1`, frame count). The probe has no image; its JSON record is its receipt.

## Cross-model view

After S1, a comparison built only from saved records of all three cohorts shows Haiku, Sonnet and Opus specialist accuracy per policy at the primary cell, with the available-truth diagnostic as a reference line and the paired world count on each bar. Pending or failed observations stay explicit.
