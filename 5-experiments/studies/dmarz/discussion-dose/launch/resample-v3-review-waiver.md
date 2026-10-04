# Review waiver: v3 resampling-only sidecar, attempt resample-v3-a1

Date: 2026-10-04 UTC. Decision by dmarz (owner), relayed by dmarz/private-control.

dmarz instructed: "just ship it and ignore the reviews." This launch therefore proceeds **without** a passed independent review of benchmark v3 or of this sidecar. At the time of launch, shadow/sol-rev's review (`review-discussion-benchmark-v3`) was in progress with no verdict, and vishesh's targeted static note (`researchers/vishesh/notes/independent-reviews-2026-10-04/v3-followthrough.md`) explicitly did not approve paid launch.

Consequences recorded here so no later reader mistakes this for a reviewed run:

- Results are exploratory engineering measurements. They are not reviewed evidence and must not be cited as such.
- If shadow's review later finds a blocking defect in v3 code this sidecar imports, this attempt's results are suspect and the post-mortem must say so.
- The software gate still checks source hashes, call allowance and this file's digest.
