---
id: olson-2001-ten
type: paper
title: "The Ten Commandments of Counterintelligence: A Never-Ending Necessity"
authors: [James M. Olson]
year: 2001
venue: Studies in Intelligence (CIA Center for the Study of Intelligence), Fall-Winter 2001
url: https://www.cia.gov/resources/csi/static/ten-commandments-of-counterintelligence.pdf
doi: null
arxiv: null
cite: "Olson, J. M. (2001). The ten commandments of counterintelligence: A never-ending necessity. Studies in Intelligence, Fall-Winter 2001."
topics: [fork-merge-security]
added_by: dmarz/fm
accessed: 2026-10-03
read_depth: full
relevance: 3
citations: null
code: []
---

## Summary

A practitioner's essay (read in full, about 4,000 words) by a former chief of the CIA Counterintelligence Center setting out ten rules for counterintelligence (CI). It is opinion grounded in experience, not a study. The rules most relevant here: be offensive, with aggressive double-agent operations, because "the key to CI success is penetration"; test even friendly services by sending "an enticing morsel, made to order for that specific target" and seeing whether they take it; CI must not be shoved aside by case officers and managers who "do not want to believe that their operations are controlled or penetrated by the opposition"; and CI officers should not stay too long, because a steady diet of suspicion produces "creeping paranoia", as with James Angleton's mole hunts, which the author regards as among the worst CI disasters.

## Contribution

States, from inside the profession, the operating principles for detecting turned or penetrated agents, including the cost of excessive suspicion.

## Key results

- No measurements; all claims are the author's experience and judgment.
- Cites at least 41 countries spying on the US (from Paul Redmond's 2000 congressional testimony) and lists SVR-handled penetrations (Ames, Nicholson, Pitts, Hanssen) as evidence that insiders, not perimeter failures, did the damage: "Spies have hurt us."
- Recommends tailored test material ("dress up an enticing morsel") to reveal whether a party is working against you.
- Warns that owners of an operation resist outside scrutiny of whether it is controlled, and that sustained paranoia leads to "the wilderness of mirrors".

## Methods and models

Personal essay.

## Limitations and open questions

Single-author opinion with no data; selective anecdotes.

## Relevance to us

Three operating rules that translate to a fork-merge parent. Q1/Q3: the attacker's equivalent of "penetration" is knowing which child will be merged; the defender's equivalent is planting its own controlled children so that an attacker who turns a child cannot tell whether it has turned a real one. Q2: the "enticing morsel" is a canary test, i.e. send each child domain-specific bait whose correct handling is known, and measure same-task reliability before trusting its report, which is the calibration [[numbers-2014-influences]] found necessary in humans. The Angleton warning sets the other side of the threshold trade-off: a merge rule that treats every child as possibly turned will reject honest reports and lose the value of exploring at all, so k must be set against a false-positive cost, not only against the attack. The resistance of operation owners to scrutiny argues that the merge check should be run by a component separate from the one that spawned and relies on the child. Related: [[cowden-2014-pioneering]], [[heuer-1999-psychology]], [[kelly-2025-effect]].
