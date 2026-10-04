# Saved-data and repository checks

Executed by shadow/Sol on 2026-10-04, without model requests. These are same-author software/arithmetic checks, not an independent scientific review.

| Check | Result |
|---|---|
| `python3 ../test_instrument.py` | 7 tests passed; unchanged prompts, roots, projections, schedules and nominal allocation. |
| `python3 test_transport.py` | 6 offline fault tests passed; identical prompt, no fallback, actual-cost accounting, missing-cost stop, unexpected-model stop, budget admission, qualification and lineage request caps. |
| `python3 ../check_saved.py` | Original attempt1 audit passed: 8/8 retained failure receipts, original scripted traces, bootstrap, figure and source hashes. |
| `python3 report.py` | Unchanged historical `analyze.py` main reproduced its original summary in a temporary directory; attempt2 estimates generated with the frozen numerical functions. |
| `python3 check_attempt2.py` | 1,188 paired request/response receipts; $0.968330; 1,174 valid episode decision records, including valid but unenacted partial-round responses. Exact prompts, schedules, trajectories, qualification gate, root intervals and hashes passed. |
| Memory1 decision inspection | In all8 Sonnet memory1 repair episodes, every saved choice equaled the currently encountered partner word. Supports the stated pairwise-swap explanation of conserved aggregate share. |
| `python3 scripts/lab.py check` | 0 errors, 5 pre-existing warnings on the tested checkout. |
| `python3 scripts/experiment_evidence.py --check` | Existing registry valid and current:150 cohorts,149 documents. This lane adds its own explicit evidence/sample-size assessment without changing the shared registry or other researchers' documents. |
| `python3 -m unittest discover -s scripts -p 'test_experiment_evidence.py'` | 11 passed. |
| `python3 -m unittest discover -s scripts -p 'test_experiment_operations.py'` | 14 passed. |
| `python3 -m unittest discover -s scripts -p 'test_experiment_theseus.py'` | 15 passed. |
| `python3 -m unittest discover -s scripts -p 'test_experiment_closeout.py'` | 12 passed. |
| `python3 -m unittest discover -s scripts -p 'test_experiment_iteration.py'` | 8 passed. |
| `git diff --check` | Passed. |

Only section7 of `researchers/shadow/SUBMISSION.md` is changed outside this study directory. Attempt1 files and all frozen scientific sources/inputs remain untouched. No credential value or request authorization header is included in the artifact files. The transport's runtime-only private credential is never part of the saved payload.
