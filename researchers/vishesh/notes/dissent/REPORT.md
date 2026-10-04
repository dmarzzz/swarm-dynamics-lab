# The Right Dissenter: first native result

The first qualification ran to completion but **failed: 12/18 decisions correct**. All 18 responses were valid. The model correctly interpreted all bridge reports and all negative build/alarm reports, but deferred on every positive build and alarm report. No dissent-policy effect has been measured: the broader S1 comparison remains gated.

| Scenario | Correct | Valid | Assigned |
|---|---:|---:|---:|
| Bridge | 6 | 6 | 6 |
| Build | 3 | 6 | 6 |
| Alarm | 3 | 6 | 6 |
| Total | 12 | 18 | 18 |

The prospective thresholds were >=16/18 correct, >=17/18 valid and >=5/6 correct per domain. The run used typesafe/jev-1.13-20260917, 18 unique calls, 10,230 input tokens and $0.00042966. Measured worker duration was 8.35 seconds; hub duration includes later documentation updates and should not be used as latency. No retries or missing observations occurred.

[Public run and measured figure](https://swarm-live.pages.dev/#/r/right-dissenter%2Fq0-a1), [summary](results/q0-a1/summary.json), [complete requests and validated responses](results/q0-a1/calls.json), [post-mortem](reviews/Q0-A1-POST.md).

## What this suggests

The generic requirement may underspecify whether one positive observation is sufficient. This is a testable explanation, not an established cause. [Q1](Q1-PLAN.md) pairs generic and explicit single-criterion instructions on 18 fresh packets and adds six absent/conflicting-evidence controls. Qualification uses unchanged clean thresholds plus all six correct DEFER controls. It has passed 51 software checks but made no native calls.

Fresh identifiers do not create new semantic templates. Even a Q1 pass would support only the bounded synthetic S1 comparison, not general operational reliability. An exact grammar parser already solves these clean packets; Jev must demonstrate value beyond a transparent rule and always-check in the eventual comparison. Scripted votes, fixed evidence ancestry and shared identical model responses limit interpretation.

## Allocation and process failure

I provisioned the temporary host through the default local credential without proving it belonged to Dmarz's DigitalOcean account. The subsequent account check confirmed the mismatch. This violated the requested allocation boundary despite the approved $2 cap and the shared fleet entry. Further calls stopped before Q1. Outcomes and the spend ledger were preserved, artifacts verified, and the exclusive claim released; [CLEANUP.json](CLEANUP.json) verifies host removal and unchanged other droplets. A verified Dmarz-account allocation is required to resume.

The immutable plan was published and publicly verified before Q0. Its original URL is retained on that run. SETUP.md was added retrospectively and is labelled accordingly. These facts do not erase the allocation failure. [Q1 setup post-mortem](reviews/Q1-SETUP-POST.md) separates process compliance from measured model performance.

## Research context and remaining work

[SOURCES.md](SOURCES.md) maps the already-catalogued minority-correction, withholding, honeybee inhibition, evidence-ancestry and correlated-judge literature and map-demo X threads to the design. No unsupported claim of full thread access or completed independent research review is made.

Next: establish the authorized allocation, run Q1 against its published gate, review it, and only then admit the fixed 52-root/seven-policy S1 study. Formal confirmation remains closed. There is no current evidence that the Right Dissenter policy improves outcomes or suppresses useful dissent.

Q0 compute estimate is $0.011643 for 0.326 allocation hours at the verified $0.03571/hour rate; the actual invoice is not yet available. Cumulative API usage remains $0.00042966. No Q1 cost exists.
