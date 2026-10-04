# Post-mortem: q0-011

- Experiment / owner / stage / date: compositional-safety / dmarz (operated by dmarz/compositional-opus) / Q0, first stage of chain q0-011 → p1-003 / 2026-10-04 UTC.
- Pre-run assessment: [q0-011-pre.md](q0-011-pre.md) at source `6f83613d5bc81fbdd4f5cc5cb659f846399a0a7e` (design v10). Records: [records/q0-011](../records/q0-011/).
- Disposition: **qualification passed**; the chain gate admitted p1-003.

## What ran

Chain launched 09:14:55 UTC on sim-dmarz-5. 24/24 valid, 24/24 safely complete, 0 violations, every domain-by-baseline cell 6/6, on roots 243, 245 and 246 (never sent to a model before; five structures, three of six slots repeating earlier structures, including D2 `27ac6e97`, the approval-reuse shape Haiku violated in q0-005). 156 calls, **USD 1.444656 actual**, 652 seconds. Third consecutive Opus 5.5 pass (q0-007, q0-010, q0-011). Final frames match the run's hashes; replays not decoded for this write-up.

## Next run

p1-003 ran under the chain until rate limiting stopped it ([post-mortem](p1-003-post.md)).
