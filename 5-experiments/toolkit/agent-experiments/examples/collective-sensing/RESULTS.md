# Executed offline demonstration

Executed 2026-10-03 using Python 3.14.5. **These are results of programmed majority rules on generated binary signals, not LLM research findings.** No provider calls were made. This is a reproducible analysis example, not confirmation of the prospective LLM hypothesis.

| Scripted condition | Mean fraction of agents correct |
| --- | ---: |
| Naive global message counting | 0.8042 |
| Global counting of unique sources | 0.8667 |
| No communication | 0.7333 |
| Ring with unique-source counting | 0.8108 |

The primary paired difference is **0.0625** (6.25 percentage points). The illustrative scenario-cluster percentile-bootstrap interval is **[0.0125, 0.1125]**, based on 2,000 resamples. This interval reflects the toy's scenario sampling and configured repetition scheme; it is not an estimate of any LLM effect. Comparisons with ring and no-communication conditions are exploratory and have different evidence reach.

Run accounting: 60 scenario clusters × 4 fresh repetitions × 4 conditions = 960 completed worlds, with five final decisions each. There are 4,800 agent decisions and 12,480 event records. Counting those decisions as 4,800 independent experimental units would be incorrect. All runs completed under the scripted mechanism; this provides no evidence about real provider failure rates.

The mechanism is explicit: repeated source 0 can change the unweighted message majority. Deduplication restores majority across independent source observations. The validity test includes a concrete case with observations `[0,0,1,1,1]`, where tripling source 0 flips the naive decision but not the unique-source decision.

The compact [reference summary](expected-summary.json) is included. Regenerate full logs under the git-ignored `data/` directory using the command in the protocol. Generated traces and machine-specific manifests are intentionally not committed. Exact rerun equality is checked within the executing Python runtime; hash chains establish internal consistency rather than protection against an adversary who can rewrite every artifact.

No current API prices, compute-energy estimate, LLM judge, persistent autonomous agents or real-world side effects are involved. Local CPU time and preparation time were not metered. To collect scientific LLM evidence, resolve and preregister the prospective protocol, replace the toy control with a competent baseline, complete provider and isolation checks, and run a separate pilot and confirmatory study with explicit authorization for cost.
