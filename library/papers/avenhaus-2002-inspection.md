---
id: avenhaus-2002-inspection
type: paper
title: Chapter 51 Inspection games
authors:
- Rudolf Avenhaus
- Bernhard von Stengel
- Shmuel Zamir
year: 2002
venue: Handbook of Game Theory with Economic Applications, Vol. 3, Chapter 51 (Elsevier)
url: http://www.maths.lse.ac.uk/personal/stengel/TEXTE/insp.pdf
doi: 10.1016/S1574-0005(02)03014-X
arxiv: null
cite: Avenhaus, R., von Stengel, B., & Zamir, S. (2002). Inspection games. In R. J. Aumann & S. Hart (Eds.), Handbook of Game Theory with Economic Applications (Vol. 3, Chapter 51, pp. 1947-1987). Elsevier.
topics:
- fork-merge-security
- collective-decision
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: skim
relevance: 5
citations: 68 (Crossref, 2026-10-03)
code: []
---

## Summary

Survey chapter on inspection games, in which an inspector with limited resources checks that an inspectee keeps an agreement it has an incentive to break. It covers applications (arms control, IAEA safeguards, auditing, tax, environment), a statistical framework where the inspector chooses a test and false-alarm rate, sequential inspection games (Dresher 1962: n stages, m inspections), and inspector leadership, where the inspector announces and commits to a mixed strategy. I read sections 1, 2.2, part of 4.1, 5 and 6 of the authors' 2001 preprint; section 3 was skimmed.

## Contribution

The standard reference linking inspection to equilibrium analysis and stating the leadership (commitment) principle; the operations-research root of Stackelberg security games ([[korzhyk-2011-stackelberg]], [[tambe-2011-security]]).

## Key results

- Leadership: in zero-sum games announcing a mixed strategy changes nothing; in non-zero-sum inspection games the inspector gains by committing. In the chapter's 2x2 example the inspector announces the same probability (1/3) as in the simultaneous equilibrium, and the inspectee switches to legal behaviour, raising the inspector's payoff from -2/3 to -1/3.
- In the Dresher game with an announced strategy, the inspectee acts legally while inspections remain and violates once they are used up (stated for general n and m).
- With uncertain inspectee payoffs, the recommended announced probability is slightly above the equilibrium value (Avenhaus, Okada and Zamir 1991, as summarised).
- Applied finding: splitting a plant into many balance areas does not raise overall detection probability against a strategic violator.

## Methods and models

Zero-sum and non-zero-sum games in normal and extensive form, embedded hypothesis tests, recursive games, leadership versions solved for subgame-perfect equilibria. Theory and application descriptions; no new data.

## Limitations and open questions

Mostly one inspector, one inspectee and a single violation. Assumes the inspectee knows the distribution but not the realised schedule. Authors list sequential leadership games and links to principal-agent theory as open.

## Relevance to us

- Q1: the formal answer to whether a parent should hide its reintegration policy. Publish the distribution of which children are audited before merge; keep only the draw secret. Commitment can make honest behaviour the best response. The Dresher result predicts the empirical failure in [[kutasov-2025-evaluating]] and [[bhatt-2025-ctrl]]: once the schedule or remaining budget is known, the protection disappears.
- Q2: gives a closed-form trade-off between merge rounds and audit budget for one attacker; k-of-n corruption is not covered (see [[leslie-2015-threshold]]).
Related: [[gans-2026-when-does]], [[blocki-2013-audit]], [[becker-1968-crime]].
