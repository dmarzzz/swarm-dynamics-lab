# Post-mortem: v3 engineering a1

Disposition: engineering qualification passed; native repair qualification blocked on a dedicated host. Execution is complete, model qualification is not. Pre-run: engineering-a1-pre.md. Frozen execution commit e3c40b027313ccc6985f36fa63bab6ff221cc1c1; source/config/protocol hashes and assignment manifest are preserved in ENGINEERING-MANIFEST.json.

## What ran

720 assigned → 720 recorded → 720 scored; zero missing/duplicate outcomes and zero invalid executions. Sixteen tasks × five scenarios × nine arms, 24 rounds. Zero API calls and zero model cost. Clean and no-incident controls complete every request. Thirteen current unit tests pass; nine scientific regressions passed before the suite. Later checks cover missing/duplicate assignment accounting, legacy duplicate-format rejection and unsupported-arm rejection. Later reporting changes and argument validation do not alter the preserved run's source hash or outcomes.

## What it teaches

Across 16 tasks in shared_evidence: Q10F mean completion 54.17%, Q11R 79.17%, Q11 and Q11S 100%. Target relevance now creates genuine fixture variation: Q10F ranges 38.89–72.22%; Q11R ranges 72.22–88.89%. These are programmed-policy mechanism checks, not sampled LLM estimates.

Removing replay raises Q11R to 100%, isolating the replay mechanism. Removing lineage drops Q11/Q11S to 79.17%, demonstrating the known-ID blocker's boundary. With legitimate learning before repair, broad Q11 rollback scores 0% while selective Q11S scores 100%; the retained-learning metric independently shows why. The intervention therefore has a real cost/benefit boundary in the fixture. All of these deliberate task failures are correctly scored outcomes, not reasons to retry until successful.

## Visualization review

Generated a 1600×1000 final frame, 24-frame GIF and self-contained interactive replay for both historical native v2 and v3 engineering. The HTML retains all tasks/scenarios and supports arm selection, scrub and play/pause; GIF is one explicitly labeled task/scenario. Verified the round-7 benign-learning state: Q11 has 11 correct/1 wrong shared facts, Q11S has 12 correct/0 wrong. Timeline cells agree with the preserved request outcomes. V2 shows the recorded response error and labels absent state-count telemetry rather than inventing it. Static frame inspected; interactive controls and animation progression checked in the browser. Full history remains in JSONL.

## Remaining repair work

V2's duplicate-key failure has an offline schema repair and regression coverage but not yet a passing fresh native run. All candidate fleet hosts became exclusively claimed; atomic claim checks rejected collisions and no conflicting host was used. A dedicated or released host is required. Then reserve up to USD 8 from the existing shared budget before installing a separate local quota and run task 6700 only. Public plan and exact runtime tests must pass before that launch. No provider/permission bypass and no extra machine spending occurred.

Native population robustness, real detection and independent replication remain untested. The next result must distinguish execution qualification, clean competence and the scientific contrast; no current document declares model robustness established.
