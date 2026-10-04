# Public plan repair

Published a retrospective Regrowth plan and missing-registration incident, with a TLDR condition guide for all six pilot worlds. Added reviewed TLDRs and parser-compatible design sections to six experiment READMEs; registered immutable commit 938772fc468ac506d3d491a9882cc81dc6938426 on the hub. Created failed analysis record regrowth-200/plan-registration-failure-v1 with missing_plan_url=1 and documentation_remediated=1. Verified that all original execution status, timestamps and metrics remained unchanged.

The public browser shows TLDR, two plan links, retrospective labeling and no missing-plan warning; no browser errors. Six preflight tests and seven environment tests pass. Regrowth local runner now blocks model initialization without a public plan receipt and run-specific TLDR. Standing workspace instructions require a plan before implementation and public registration before any run. No models rerun; no full private source/evidence archive exported.

A concurrent Antsy rename was preserved; one automated sync heartbeat on another task was excluded. Auto-review initially rejected the combined merge/push; a separately inspected documentation-only diff passed. Remaining work is to adopt the shared preflight in other runners before their next launch, as required by the documentation contract.
