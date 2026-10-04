# Visualization mapping v1

Binding: sybil-newcomer-api, design v1, each attempt's recorded source_hash and code commit, world/identity/strategy/arm keys. The primary visual explains how earned reputation responds to an attack and whether unique honest newcomers remain audible. The final view complements accuracy with controller influence.

| Recorded field | Meaning and denominator | Encoding | Visibility |
|---|---|---|---|
| history.metrics.attacker_reputation | mean public Beta audit score across active controller identities | upper-left line, scale 0–1 | Score is public; ownership grouping evaluator-only |
| history.metrics.newcomer_retention | rare honest messages admitted / 3 | upper-right line, scale 0–1, undefined before arrival | Evaluator-only grouping |
| episodes.evaluation.rare_accuracy | exactly correct specialist outputs / 3 | sampled-round table, final tradeoff y-axis | Evaluator-only |
| episodes.evaluation.bad_seat_share | controller-owned admitted reports / 12 | final tradeoff x-axis | Evaluator-only; not labeled harm |
| round, attack_active, join_round | logical time, switch and arrival | time cursor and round-4 event line | Arrival observable; attack truth evaluator-only |
| status, completion_index, elapsed_seconds | actual API execution and missing state | progress text and pending cells | Public-safe accounting |

Colors are stable across all views: random gold, reputation violet, renewal teal. Each panel also uses written names. Lines average recorded worlds at a given logical round, never treating frames as independent samples. The focus trace uses sixteen identities and sleeper strategy; all other cells remain in analysis. Model observations exist only at rounds 4, 5, and 8; other cursor rounds explicitly say model not sampled, with no fabricated accuracy or interpolated model memory.

Live progress uploads are throttled to at most once per twenty seconds. Final frames are 1800×1200 PNG. Logical replay is eight GIF frames at one second each, with a three-second final pause; Q0 uses nine completion-prefix frames because it has no temporal interaction. JSONL history retains every round of every world, policy, identity count, and strategy without downsampling. Its schema distinguishes actor-observable packets/history from evaluator-only diagnostic fields. No additional API calls generate animation.

The public live site supports PNG and GIF images. A labeled round cursor provides time semantics; the final PNG is the static fallback where autoplay is unsupported. No unsupported custom player or arbitrary frame.json schema is assumed. All four panels derive from saved records. The renderer is outside the simulation random stream. On rendering/report failure the raw result is preserved and the failure is logged; post-hoc rendering repairs may use existing history without repeating model calls.

Acceptance: offline synthetic normal/attack transition/failure frame checks; compare initial, round-3, round-4 and round-8 states with history; verify final numeric values against analysis; inspect readability and GIF frame count and actual public playback. Parent operator verifies the deployed UI. Pending/failed observations remain explicit, and denominator counts accompany reported API measurements.
