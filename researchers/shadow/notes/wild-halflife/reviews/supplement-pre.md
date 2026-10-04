# Saved-data supplement assessment, 2026-10-04

Owner/operator: shadow/sol-halflife. Status: ready for offline saved-data checks only, not model dispatch. This assessment is written after reading the baseline aggregate outputs and before executing supplement.py. It is not retrospective preregistration of the baseline or its existing post-hoc exclusions.

## Previous evidence and concerns

The baseline and first post-hoc sensitivity were recovered from two earlier sessions interrupted by provider outages in the operating assistant. The analysis itself made zero provider calls. Baseline [PLAN.md](../PLAN.md) was committed before analysis at 2cb859a5. The draft results have been published on main at 48bc8a76. No earlier scientific post-mortem was present; this assessment explicitly records that documentation gap rather than inventing one.

Saved results show a stronger pooled URL slope on wiki than git, but the early-transition slope among eventual popular units is flat/negative. The plan's suggestion that this restriction removes popularity selection is incorrect; it conditions on a future outcome. The draft discloses that limitation. Line slopes differ substantially from URL slopes and include code/process boilerplate. The existing first post-hoc exclusions are retained as sensitivity, not promoted to prospective analysis.

The paper's population differs from our all-revision corpus. Directly opened arXiv 2609.09150 HTML on 2026-10-04: the paper excludes agents that never wrote on a task page, predominantly a June 18 link-poster swarm. No task-engagement filter has yet been reconstructed here.

## Exact supplement scope

1. Add 1,000 origin-page bootstrap resamples to the existing wiki visible-pages URL rates, seed 20261004. The point estimates must agree exactly with saved summary.json. Moderator deletion events remain ignored; URL removal by revisions is included.
2. Report the primary wiki URL metrics after excluding the whole UTC day June 18. This is explicitly post-hoc, deliberately coarse, and not the paper's actual task-engagement restriction. Do not choose another filter based on whether the result is favorable.
3. Use askswarm.adapters.json_rows read-only to report schema key counts for local pages/labels/events files. No source rows or label/IP values emitted.
4. Rebuild the one figure from the unchanged baseline plus visible-pages bootstrap endpoints, width >1,600px. Add pointwise KM intervals, clearly not simultaneous bands.

No new causal hypothesis, new corpus, paid request, model, host provisioning or fleet allocation. Compute: nice 10, one process, BLAS one thread, shad0wbot; source data stay local, outputs aggregates only. Existing 1,000-resample plan is used, not a precision stopping rule. Cost cap and actual model calls: zero.

## Acceptance checks and visualization mapping

- Existing six synthetic tests pass; add a known-answer visible-pages rate fixture and bootstrap reproducibility test.
- Supplement preserves all baseline visibility event/exposure/rate estimates exactly.
- Assert strict JSON serializability for supplemental outputs; unavailable values must be null, not manufactured results.
- Figure A: recorded elapsed activity to second identity mapped to x / KM adoption fraction to y. Figure B: prior identities mapped to x / pooled rate to y. Figure C: latest-known page count bins mapped to x / new-label rate to y. Bootstrap endpoints shown from aggregates.
- Static final frame is the supported fallback. This is a retrospective, frozen-data census, not a live execution; source history is not redistributed and a replay animation would add no new observations.
- Preserve baseline outputs and disclose any measurement/reporting defects instead of silently replacing them. Close with a scientific post-mortem and FINDING.md status update.
