# Post-mortem: s1-001

Experiment sybil-specialists-api / dmarz/sybil-specialists / S1 / 2026-10-04 UTC. Parent q0-001. Pre-run s1-001-pre.md. Disposition complete-valid-result.

## What ran and what happened

Run sybil-specialists-api/bac7d9ae, source 2b8895abce333d3e4cdd44a78f8566d3e2608b09, runtime 12ff89f2f54322f07245640708a0c243ad09ab8d933163e71869c3ce08255f6a. All 192 planned → started → terminal → graded → analyzed records. Every16-cell assignment has 12 valid observations; no duplicates, missing records, retries or invalid outputs. Twelve independent world clusters4000–4011; untouched holdout10000–19999 remains closed. The original API runtime was kept fixed for all 216 model calls. Analysis/reporting amendments were deployed only after that worker exited.

S1 used 192 requests, 229,886 input tokens and 7,720 output tokens; computed costUSD0.268486, execution loop241.56s, entire hub run4m22s including rendering/upload. Together with qualification:216 calls, 266,342 input tokens, 8,692 output tokens,USD 0.309802 reported-usage cost. All 216 requests have usage. Nonrefundable aggregate reservationUSD2.133561 remains below theUSD5 cap; no further requests queued. Scripted fleet S0 adds 216 zero-cost engineering cases, local S0 another216 excluded from scientific estimates. Runtime Python 3.12.3, Pillow 11.3.0, PyYAML 6.0.1 on exclusively claimed sim-dmarz-4.

Primary contrast: at attacker pass .10 with visible badges, coverage rare accuracy34/36 (.944444) versus degree3/36 (.083333), paired difference+.861111 across 12 worlds; descriptive cluster interval[.722222,.972222]. Random17/36; no verification0/36. Coverage admits8/108 attacker identities (.074074), degree4/108 (.037037), risk difference+.037037. Badge masking leaves all four low-pass aggregate scores unchanged. These are separate physical calls, not reused model answers.

At attacker pass .90, coverage admits87/108 attacker identities (.805556). Rare accuracy is 9/36 masked (.25) and 12/36 visible (.333333), paired badge difference+.083333 with descriptive interval[-.027778,.194444]. The direction is not robust enough to claim benefit or harm. Per-world differences include both signs. Scripted coverage reference12/36; the masked LLM is worse than plurality on this cell. All 16 cells and individual paired differences appear in results-summary.json. Adverse outcomes were retained unchanged.

## Visualization review

Original S1 produced a25-frame replay and 1800×1180 initial/final/progress images; seven artifacts matched hub SHA256 metadata. The original S0 and Q0 contribute14 more verified artifacts. Each completed evaluation was independently recomputed from saved packets and actor answers before analysis.

Analysis run sybil-specialists-api/analysis-api-001 uses source 7354b31d521e9229c06e2ccd3dcc10db278e7fc9 and the same192 observations, with zero new API calls. Mappingv1.1 fixes carried initial spend; initial state includes Q0'sUSD0.041316 actual andUSD0.255660 reserved, subsequent frames use the saved study totals. Its five artifacts also match hub hashes. All 26 files verified; every GIF frame decodes, image dimensions and final-image-first ordering pass. Browser playback was observed advancing from 0/192 pending to 128/192 with changing values, counts and cost, at full1800×1180 resolution. The final image agrees with all 16 cell means. Public UI embeds measured replay and links the plan; raw synthetic records remain on the hub and dedicated checkout.

## Experiment-quality assessment

Execution complete; clean API qualification passed 24/24 exact packets before attack testing; original and amended regression checks pass. The informative-check manipulation preserves specialists, while uninformative checks admit most of the attacker community and the model cannot recover reliability. This extends the scripted tradeoff to a real model synthesizer. It does not test a fully autonomous swarm or real identity proofs. Badge presentation produced only an uncertain secondary effect.

Limits: one model snapshot, 12 small worlds, one symmetric topology family, privileged honest seeds, fixed +7 fabricated values, scalar facts, externally modeled verification, and no faithful published-defense comparator. The no-check arm is a diagnostic with zero verification cost; the three active policies have equal four-check budgets. The three skill outcomes within a world and repeated conditions are dependent; intervals resample worlds. No confirmatory p-value, novelty claim or deployment recommendation. Valid adverse/null outcomes are not defects and were not tuned away.

## Failure and repair ledger

| ID / kind | Evidence / cause | Repair | Acceptance / status |
|---|---|---|---|
| usage-scope / reporting | Original hub progress counts include previous Q0 while terminal totals describe S1 | Worker now reports stage counts consistently; full original trace retained and documented | Mocked carried-ledger regression passes; corrected analysis replay verified; closed |
| initial-cost / display | Original initial frame defaults to zero despite earlier Q0 spend | Pass explicit pre-stage accounting to renderer | Analysis initial frame visibly shows correct carried cost; closed |
| non-applicable-metric / display | Q0 emitted a zero rare-accuracy placeholder | Future worker omits that field; original Q0 uses qualification_passed and clean chart | Regression asserts absence and Q0 perfect score separately documented; closed |
| analysis-path / reconciliation | Named analysis starts have hub attempts0, unlike leased workers' attempts1 | Private verifier maps the explicitly named analysis directory | All 26 artifact hashes and image checks pass; no observation rerun; closed |
| upstream-artifacts / unrelated validation | Prior project-wide Flight Deck metadata errors | Upstream updates resolved them during the run | Strict check now9 artifacts, 0 errors, 0 warnings; closed |

No authentication, transport, budget, model-schema or scoring failures occurred. The reporting repair used mock responses only, consumed no API budget and did not mutate scientific records. The amended runtime is not retroactively claimed as the generating code; future paid work must qualify its own exact runtime and fresh fixture plan.

## Next run and closure

This exploratory follow-up is complete. Do not rerun for a more favorable badge result. A new scientific study should predeclare a second graph family, vary attack-generation mechanisms and add faithful published comparators; survey/hypothesis review and powered design remain required before formal S2. No additional API batch is authorized or queued by this report. Worker exit was verified before claim release. Results, ledger and artifacts are preserved for audit; reusable hardware returns to the owner's pool.

Closure confirmed: release merged as agentops PR51 at2026-10-04T02:12:37Z; claim status done. All26 artifact checks passed and worker_active was false before release. Agentops launcher PR47 has passing CI. Project validation reports0 errors (five pre-existing unresolved library-link warnings); Flight Deck strict check reports9 artifacts,0 errors,0 warnings.
