---
id: karami-2026-deterrence
type: paper
title: "Deterrence Effects of Social Media Interventions on Health Misinformation Dissemination by Bots and Humans"
authors: [Amir Karami, Nima Kordzadeh, Serena Harn]
year: 2026
venue: "European Journal of Information Systems"
url: https://arxiv.org/abs/2607.18248
doi: null
arxiv: "2607.18248"
cite: "Karami, A., Kordzadeh, N., & Harn, S. (2026). Deterrence Effects of Social Media Interventions on Health Misinformation Dissemination by Bots and Humans. European Journal of Information Systems, 1-28. arXiv:2607.18248"
topics: [swarm-detection]
added_by: shadow/sol-w5
accessed: 2026-10-03
read_depth: skim
relevance: 2
citations: null
code: []
---

## Summary

Interrupted time-series study of whether Twitter's three misinformation interventions (removal from Feb 2017, reduction from Jun 2018, informing labels from Sep 2020; dated from Twitter blog posts) had lasting effects on bots versus humans spreading cancer misinformation. Pipeline: 81 false cancer claims from the Google Fact Check API; 268,280 tweets matching them (2011-2021); a classifier trained on 2,000 hand-coded tweets labelled 68% as supportive; Botometer scores for the 96,836 supporting accounts (66.9% scorable, the rest suspended, deleted or protected), with results averaged over thresholds 2.5 to 4 in 0.1 steps; seasonal ARIMA intervention models on monthly counts. Reported: about 48.5% of supporting accounts were bots, producing 59.1% of activity. All three interventions cut the number of bot accounts (coefficients -0.804, -0.892, -0.554, i.e. about 84%, 87% and 72% drops); removal and reduction cut bot activity (98% and 86%), informing did not; no intervention had a significant sustained effect on humans.

## Contribution

Long-horizon (ten-year) quasi-experimental evidence, split by bots and humans, that platform enforcement changes automated accounts' behaviour persistently while human spreaders are largely undeterred.

## Key results

- Bot accounts: removal -84%, reduction -87%, informing -72% (all p < 0.05).
- Bot activity: removal -98%, reduction -86%, informing not significant (p = 0.62).
- Humans: no significant sustained effect of any intervention.
- Post hoc: pooling bots and humans hides the difference.

## Methods and models

Fact-check-seeded keyword collection, supervised tweet classification, Botometer bot scores with a threshold sweep, seasonal ARIMA interrupted time series with step-change terms, Ljung-Box residual checks, Google Trends as a control for third-party interest.

## Limitations and open questions

Bot labels rest on Botometer scores applied retroactively; the threshold sweep reduces but does not remove the base-rate problems in [[gallwitz-2022-investigating]] and [[rauchfleisch-2020-false]]. A third of accounts were unscorable, and suspended accounts (likely bots, likely removed by the intervention itself) drop out, which biases the "after" bot counts. Intervention dates are blog-post dates, not rollout data. English only, Twitter only, data ends before the X era.

## Relevance to us

Weak as a bot-prevalence source, but the design is relevant: interventions that hit bots and not humans are themselves a behavioural signal, i.e. response to platform pressure could separate automated swarms from organic users. Related detection-validity critiques: [[gallwitz-2022-investigating]], [[rauchfleisch-2020-false]]; coordination methods: [[pacheco-2021-uncovering]].
