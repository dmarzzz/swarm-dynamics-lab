# Antsy v4: verification did not earn its cost

Exploratory result, 2026-10-04 UTC. **A five-role committee did not beat the no-check confidence baseline on this 70-receipt sample. Neither adaptive committee stopped early.** The study answers a useful engineering question: before buying more model deliberation, check whether the evidence update is informative and whether a simple router already captures most of the available gain.

## What actually ran

Three real Tesseract configurations on 100 externally authored CORD-v2 validation receipts; 20 calibration, 10 instrument qualification, 70 paired evaluation. Seven arms under Laya and the same seven under Jev. The four common controls are identical and count once: 70 independent receipt units, 700 distinct receipt/condition outcomes, not 980 independent samples. The official test split remains unopened.

Both full runs completed 70/70 receipts, 490 arm rows and 840 physical model calls each, with zero invalid invocations. Laya worker wall time was 1,840.76 seconds; Jev 391.04 seconds including reporting overhead. Hosted call latency and local CPU inference are not comparable compute benchmarks. Fixed/adaptive arms share potential ballots; each committee represents 700 logical calls, but their shared calls are executed only once. Every input, purchased observation, vote and final score passed the independent [integrity audit](src/verify_results.py).

Frozen run sources: Laya `c2dffda0c5fc82ef12c8027d4eab342fb2d738c9`; Jev `cd04c38d1f33f8ba603a4f482058b1d962def613`. The latter changes the hosted adapter, not the scientific policies. Corpus SHA-256: `5803dc7635a05d9201b20258f9f2e61bb89e1700f3006497d69d761b71577d2b`.

## Results

Quality is annotated-token recall, not financial amount accuracy or full OCR precision.

| Policy | Laya recall | Jev recall | QA checks per receipt |
|---|---:|---:|---:|
| Best fixed OCR mode | 48.03% | shared control | 0 |
| Confidence only | **56.78%** | shared control | **0** |
| Random checks | 54.33% | shared control | 2 |
| Deterministic check rule | 56.64% | shared control | 2 |
| Single agent | 55.88% | 55.42% | 2 / 1.96 |
| Fixed five-role committee | 56.30% | 55.72% | 2 |
| Adaptive five-role committee | 56.30% | 55.72% | 2 |
| Best measured mode per receipt | 60.96% | evaluator-only ceiling | — |

Relative to confidence alone, adaptive Laya changed mean recall by **−0.48 percentage points** (paired descriptive bootstrap 95% interval −2.50 to +0.98); Jev by **−1.06 points** (−2.60 to +0.11). These intervals do not establish that committees are universally harmful. They provide no positive case for paying for this committee on this task. At every reported nonnegative QA price, confidence-only has the highest observed mean utility among tested deployable policies.

A weak-baseline story would look attractive: Laya beats the fixed OCR mode by 8.27 points and Jev by 7.69. But confidence alone gains 8.75 points for no checks or model calls. The stronger control changes the conclusion. Jev-minus-Laya committee difference is −0.57 points (−2.86 to +1.79); this sample does not establish a backend ranking.

The residual headroom after confidence routing is only 4.18 points. Of 70 decisions, 51 confidence choices, 51 Laya committee choices and 47 Jev committee choices were within two points of the measured oracle. Full secondary total-price token scores are in [comparison.json](results/comparison/comparison.json); they ignore punctuation/order and must not be interpreted as exact payment values.

## Why did checks make bad decisions?

The purchased values are true measurements. The problem is how a local measurement changes an approximate whole-receipt estimate. Laya verification improved five choices and harmed four relative to confidence; Jev improved one and harmed five. Count and magnitude both matter: Laya receipt 55 switched B→A and lost **52.17 points**, outweighing several smaller improvements.

The audit exposes a concrete construction weakness. **87/140 Laya committee checks and 94/140 Jev checks hit regions with no annotated target tokens.** The current estimator drops that region for the checked configuration, while unchecked configurations retain their estimates. A null result can therefore change the ranking without measuring OCR quality. For Jev receipt 72, two null checks switched B→C and lost 32.26 points. Receipt 53 similarly lost 3.70 points after two null checks. This is an estimator/QA-contract artifact, not evidence that the model misunderstood receipt text: actors never saw that text.

Other harms involve genuine but unrepresentative regional scores. Laya receipt 55 first checked an empty top region, then observed 66.67% regional recall for A; its final whole-receipt choice was substantially worse. Equal regional averaging is misaligned with token-weighted evaluation, and one additive calibration offset is too crude to express uncertainty. These mechanisms are directly inspectable in each run's `decision-audit.json` and compressed episodes; they are not inferred hidden reasoning.

Adaptive stopping was inactive in both studies: zero checks saved and identical outcomes to fixed committees. Laya emitted no STOP choices in 840 calls. Jev emitted nine, but no committee reached the stopping threshold. Passing explicit-choice qualification was insufficient to establish useful stopping behavior. Do not describe this as a successful adaptive-quorum demonstration or an urgency experiment.

## Quality assessment and next design

The redesign is more informative than the 12 authored API tasks: natural OCR errors determine winners, frozen inputs support paired counterfactuals, cheap controls can reject the agent story, and negative findings are preserved. Its main weakness is now visible in the measurement contract rather than hidden behind a synthetic winner schedule.

Before another efficacy run:

1. **Repair and qualify the QA contract on development data.** An empty annotation region should return “not assessable,” should not silently improve one mode's estimate, and should be distinguished from confidently measured zero recall. Compare this with a prespecified global-region update; do not cherry-pick the version that wins on these 70 receipts. Test both empty-region and unequal-token-count cases.
2. **Target an operational loss.** Use exact structured amount/date/vendor extraction with an abstain/escalate action and a specified review cost. Token recall remains a diagnostic. Use an externally authored task specification and independently reviewed scoring before the next untouched evaluation.
3. **Make the verification choice meaningful.** Let agents select an actionable field or region, add a same-budget expected-value-of-information baseline, and calibrate uncertainty on development receipts. The current lowest-confidence-region rule often buys an empty region; more voters cannot fix that restriction.
4. **Qualify both stop and continue.** Development cases should require each behavior under explicit review prices, with truth hidden from actors. If committees still never stop, report a failed stopping mechanism rather than launch a larger adaptive study. Do not lower thresholds after inspecting this evaluation to create a success.
5. **Test information diversity separately from headcount.** Five role labels on one checkpoint are not five independent experts. Compare private evidence partitions, evidence-sharing and repeated same-input voters at matched call budgets only after the basic selector/QA tool is competent.
6. **Keep the visual explanation causal and inspectable.** Replay confidence → purchased response → estimate change → selected output → evaluator reveal. Highlight null checks and loss-producing switches. Keep the first-three-receipt gallery, and label any additional worst-case diagnostic as selected after analysis.

These are prospective requirements, not completed new experiments. No additional paid run was launched to manufacture a favorable result. V4 is a useful completed exploratory pilot; its evidence does not justify a production deployment or a general conclusion about swarms.

## Reproducibility, failures and costs

See [RUN.md](RUN.md), [SPEC.md](SPEC.md), [sources](SOURCES.md), [original-project connections](CONNECTIONS.md), and both S1 post-mortems. Numeric observations, episodes and receipts are committed under `results/`; raw receipt images/strings and OCR TSVs are excluded. Data attribution: CORD / NAVER Clova AI, CC BY 4.0. Fixed source and dataset revisions allow reconstruction.

Jev qualification had two failed attempts before successful recovery. The first failure's exact cause is unknown. The second captured a valid-looking probability vector summing to 0.99; the adapter's strict tolerance rejected two-decimal serialization. The documented repair accepts only the bounded rounding error, preserves original probabilities, and replays already-valid responses without rerolling. Both failures remain visible; the full S1 then completed with zero new failures.

Across Jev qualification, diagnostic, repairs and S1: **977 request reservations**, $0.019975452 in accepted-response reported costs, plus a known $0.000019656 rejected-response charge; one earlier uncertain call remains conservatively reserved at $0.001344. This gives a known cost of $0.019995108 and a conservative bound of $0.021339108 under the verified price assumption. The cumulative reservation ledger remains $1.313088 and was not reset; all are below the authorized $5 cap. No fallback model was used. Credentials remained in a local loopback relay; it and the tunnel were stopped after completion. The durable local ledger is retained outside the public repository.

Public run galleries: [Laya](https://swarm-live.pages.dev/#/r/antsy-verification-v4%2FS1-attempt-1), [Jev](https://swarm-live.pages.dev/#/r/antsy-verification-v4%2FS1-jev-attempt-1). The overview, measured headroom plot and six chronological replay GIFs per run are presentation artifacts, not extra trials.
