# PC7: trace audit and finite-history verification prototype

**Offline revision complete; no native successor recommended yet.** [Prospective plan](PLAN.md), [trace-grounded review](reviews/TRACE-REVIEW.md), [setup](SETUP.md).

The full PC5 trace audit covers12 qualification and128 scientific choices, including all50 valid-but-suboptimal scientific outcomes. Actual prompts were delivered as specified; missing scoring text and malformed outputs do not explain the reliable-source regression. The [trace viewer](results/native-traces.html) exposes every input and retained checked output, including successes. Raw provider bodies and confidence were not saved; that historical gap is explicit. [Audit and source hashes](results/trace-audit.json), [compressed portable traces](results/native-traces.json.gz).

The proposed finite-calibration scenario was implemented offline with empirical, posterior-greedy and exact Bayesian references. Three noisy calibration bits inform an unknown source regime, which can shift before two subsequent trust/check decisions. Verification both fixes the current report and reveals correctness for learning. In a development fixture, information value changes the action from greedy trust to check: exact expected total loss .70184 versus .77279. Independent policy enumeration verifies it. These are mathematical fixture results, not model samples or real-world estimates.

This gives a useful two-step controller improvement while preserving the prior finding that a model is unnecessary for the fully specified finite-state contract. A native proposal remains conditional on an application-specific role the exact controller cannot already perform. No machine, qualification or additional budget is requested merely to measure minimum selection again.

```sh
python3 -m unittest discover -s researchers/vishesh/notes/phantom-coast/pc7/tests -v
python3 researchers/vishesh/notes/phantom-coast/pc7/reporting/verify_export.py
```

Eight tests passed; all140 exported input/output pairs read back. No secrets/operator transcripts were included, no holdout opened, no model calls or infrastructure spend. Original cumulative API known .845052138; exposure .857148138 within the unchanged USD5 authority. Native proposal:48 roots, exploratory precision only; hypothetical112-call qualification/pilot ceiling .150528 additional, **not admitted**.
