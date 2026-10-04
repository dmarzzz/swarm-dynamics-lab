# Process failure: missing public plan registration

Detected and reported by the owner after the pilot; documented 2026-10-04 UTC.

**Failure:** `regrowth-200` had a null hub plan URL. Readers could see run metrics but could not inspect a linked experimental design. A local protocol and hashed run manifest existed, but they did not satisfy public registration. The original source/evidence archive was not published; this repair publishes only the newly requested reader-facing design documentation.

**Cause:** the registration helper supplied title, description, parameters and metrics but omitted `url`. There was no mandatory check that the public plan resolved before model launch. The launch and hub-reporting paths were separate, so reporting success was mistaken for complete experiment registration. Responsibility lies with the experiment setup, not the models.

**Impact:** all six pilot worlds were executed without a publicly registered plan. Their numeric records remain intact, but they must be described as exploratory and retrospectively documented. The repair must not be called preregistration, backdated, or used to promote the pilot to confirmatory evidence.

**Record:** a separate failed process-audit run under `regrowth-200` records `missing_plan_url=1`. Its documentation-failure label distinguishes it from the six completed computational worlds. The audit identifies all six original runs, and the linked plan provides a condition-specific TLDR for each. Original run records, outcomes and execution timestamps are not changed.

**Correction:** publish the retrospective plan, register its immutable GitHub URL on the experiment, add a visible TLDR and link the incident. Check both the public API and the rendered page. Preserve the failed process record after remediation.

**Prevention:** future launches require a published plan URL, a TLDR explaining question/intervention/comparator/metrics/limits, a per-run question and an immutable plan revision. The shared documentation helper fails closed if the public registration or required README sections are missing. The Regrowth runner uses that helper before model initialization. This is a workflow requirement for all of this owner's experiments; it is not a claim that every existing third-party runner has been retrofitted.
