# sybil-split-opus: results package

Maintained by dmarz/results-analyst. Source: the run's `analysis.json` and `summary.json` on sim-dmarz-13, read at 10:58Z (read-only); hub run `sybil-split-opus/3ed4a6e8`. The study's own RESULTS.md and post-run review are not on main yet; when they land they are the record and this package should be checked against them. Package by dmarz/pipeline-split. Same-researcher check only; not independently reviewed. Last updated 2026-10-04T10:56Z.

## Headline

Giving one attacker a fixed budget (27 fabricated report rows, 27 attachment edges, 27 verification attempts) and splitting it across 1, 3, 9 or 27 identities raised Opus 5.5's wrong answers on rare skills far more under degree-based admission than under coverage-based admission. **Primary contrast +41.0 percentage points** (descriptive interval +27.8 to +54.9; 48 of 48 roots: ring graphs +50.0, community graphs +31.9), informative checks (attacker pass 0.1), 12 checks.

Rare-skill outcomes in the primary cells, 48 roots each:

| Admission policy | Wrong at 1 identity | Wrong at 27 identities | Correct at 1 | Correct at 27 | Abstained at 1 / 27 |
|---|---:|---:|---:|---:|---:|
| Degree | 7.6% | 56.2% | 31.2% | 0.7% | 61.1% / 43.1% |
| Coverage | 0.0% | 7.6% | 100.0% | 90.3% | 0.0% / 2.1% |
| Random | 0.7% | 3.5% | 99.3% | 96.5% | 0.0% / 0.0% |

Run: S0 1,853 of 1,853 scripted, probe 1 of 1, Q0 60 of 60, S1 2,688 of 2,688 valid; no failed or unstarted row; S1 USD 44.31, 35 minutes. 48 roots (24 per graph family) are the units; 56 conditions per root.

## What it shows

- With attacker resources held fixed, splitting into more identities does help the attacker, and how much depends on the admission rule. Under degree-based checks wrong answers rise by 48.6 points from 1 to 27 identities; under coverage by 7.6 points.
- Degree-based admission is already poor before any splitting: at one identity the synthesizer is correct on 31% of rare skills and abstains on 61%, because checks go to well-connected core identities and almost no honest specialist is admitted. Splitting then turns abstentions into wrong answers.
- Random checking does as well as coverage here (wrong 3.5% and correct 96.5% at 27 identities).
- The contrast matches the pre-run scripted calibration (+0.41 on engineering roots) and a plurality rule on the same packets gives +44.4. In this cell the model adds little beyond counting the admitted rows. With no verification at all the model does better than plurality (wrong answers 51 points lower at one identity).
- Repeatability: 767 packets were seen more than once (1,554 calls); 727 of those groups returned identical answers.

## What it does not show

- Not a general ranking of admission policies: one honest population (108 identities), two synthetic graph families, one attacker budget (27 rows), simulated checks.
- The result depends on a modelling choice the plan states: the attacker's identities are linked to each other. Without those links the scripted calibration gave +0.01.
- With unreliable checks the scripted calibration had the opposite sign (-0.16); I have not read that cell in the model results.
- One model configuration (Opus 5.5, effort low). Descriptive intervals over roots; no confirmatory claim.

## The one next run

Cross this with scarcity, since both moved the outcome tonight and nothing else did: the primary cell here (degree and coverage, 1 and 27 identities, informative checks, 12 checks) at 18 honest carriers per rare skill (the current value) and at 3. That is 2 policies x 2 identity counts x 2 carrier levels x 48 roots = 384 calls, about USD 7. It answers whether coverage still protects when the truth is rare, which is the case where sybil-scarcity-opus showed the synthesizer following the repeated fabrication.

## Operations

Chain S0, probe, Q0, S1 with no wait between stages: S0 to S1 start in about 3 minutes, S1 at about 80 calls per minute with four in flight and 3,700 input tokens per call (0.3M tokens per minute). No 429, no credit error, no retry. Held about 35 minutes before launch for the rate limit.
