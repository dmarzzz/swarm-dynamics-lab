# Sybil resistance as swarms grow

Exploratory follow-up to [sybil-specialists-api](../sybil-specialists-api), addressing SEC-19 and SEC-43. Authorized by dmarz: “great, lets create a follow up experiment plan to the last one to test all of this, then please ship it autonomously and show me the results when youre done”. This is a frozen exploratory scaling study, not an accepted formal hypothesis or a deployable identity defense. S2 remains disabled.

## Question

Does coverage-based verification preserve specialist knowledge as the population grows from 36 to 972 identities, and does scaling the checking budget preserve accuracy better than keeping four checks?

Working prediction: proportional checking preserves more specialist knowledge than four checks at larger sizes when checks are informative. A plausible negative result is that the advantage disappears, or improved accuracy comes with much greater attacker influence. Ten percentage points is a predeclared useful accuracy difference, not a significance threshold.

## Setup

| Identities | Honest core | Honest specialists | One attacker's identities | Admitted seats | Fixed checks | Proportional checks |
|---:|---:|---:|---:|---:|---:|---:|
|36|18|9|9|18|4|4|
|108|54|27|27|54|4|12|
|324|162|81|81|162|4|36|
|972|486|243|243|486|4|108|

Six skills, same integer fact task, +7 attacker fabrication, 90% honest check success, attacker check success 10% or 90%, same pinned Haiku 4.5 snapshot and prompt as the pilot. Badges hidden and visible. Only report synthesis uses a model: identities, check outcomes and graph admission are simulated. One controller owns every malicious identity, but its total reporting capacity grows with population; this tests proportional population scaling, not a fixed-attacker-resource identity-splitting theorem.

The generalized graph uses two core rings of N/4 nodes (degree six inside plus one cross-ring edge) and two outside rings (degree four). Each outside community has N/36 degree-preserving bridge swaps, preserving the bridge-edge fraction. Outside communities remain graph-automorphic; random ownership and shuffled IDs prevent graph labels from revealing the attacker. Two initial trusted core identities remain fixed at every size. We do not quietly add trusted identities as the population grows. Fixed degree means graph distances and mixing can change with N; this is one explicit graph-family scaling rule, not an isolated effect of count across arbitrary networks. At N=36 the generalized generator must exactly reproduce the original.

## Protocol

Start from `templates/experiment-worker`, adapting the owned preceding simulator and API transport. See [preregistration](preregistration.md), [design](design.yaml), [runbook](RUN.md), and [visual mapping](VISUALIZATION.md).

S0 runs full clean qualification fixtures plus two disjoint engineering worlds at all sizes, policies, reliability and badge settings. Q0 evaluates four fresh worlds at each size, with full facts versus missing specialist facts and both badge settings: 64 API calls. Q0 includes up to 972 reports, exceeding the maximum 486 admitted reports in S1. Each size must independently pass the original competence thresholds. S1 compares 24 fresh world clusters (6000–6023) at every size, with degree, random, coverage and no verification. Check-budget duplicates at N=36 and all no-check duplicates are physically deduplicated: 2,400 API assignments. The identical N=36 fixed/proportional condition is one observation, never counted twice. Dispatch is globally shuffled, at most four simultaneous requests in one finite worker. No automatic retries. Any failed call stops new submissions and preserves remaining assignments as not started.

A persistent ledger admits at most 2,600 requests and USD 180 conservative reservations for this study (including qualification and bounded repairs), within the user's USD 500 total dmarz API budget; report actual usage separately. The previous USD 5 cap does not apply to this newly authorized study. Qualification and S1 require exact runtime fingerprints, committed pre-run reviews and completed prerequisite stages. Original holdout 10000–19999 stays untouched.

## Metrics

Rare-skill and all-skill answer accuracy; attacker share of admitted seats; fraction of attacker identities admitted; honest specialist rejection; verification cost; model minus identical-packet plurality; badge contrast; exact clean answers and required abstentions; all assigned/started/valid/failed/missing counts and actual tokens/cost. Report every cell. Resample whole world clusters for descriptive 95% intervals; skills, identities, policies and API calls are not independent samples. Primary exploratory contrast is coverage proportional minus fixed accuracy at N=972, informative checks and visible badges; its N=36 reference difference is exactly zero by deduplication.

## Prior evidence and limits

The prior 12-world API pilot demonstrated the strong-check utility / weak-check admission tradeoff, but could not resolve badges. This study addresses population scale requested by the user, retaining the old model and attack mechanism so changes remain interpretable. It does not test sleeper attackers, autonomous reporters or real identity verification. [[shi-2013-sybilshield]] already addresses multi-community exclusion; [[viswanath-2010-analysis]] studies graph-defense sensitivity to communities. We are not claiming novelty or an improvement over faithful implementations of these defenses. Those comparisons and reviewed survey/hypothesis gates remain necessary for formal promotion.

## Results

Pending execution. Initial and progress frames, final scaling curves and a measured completion replay will appear on [the live experiment](https://swarm-live.pages.dev/#/x/sybil-scale-api). No favorable outcome is required for completion.
