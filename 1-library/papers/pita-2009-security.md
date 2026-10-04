---
id: pita-2009-security
type: paper
title: Security applications
authors:
- James Pita
- Harish Bellamane
- Manish Jain
- Chris Kiekintveld
- Jason Tsai
- Fernando Ordóñez
- Milind Tambe
year: 2009
venue: ACM SIGecom Exchanges, 8(2), 1-4
url: https://www.sigecom.org/exchanges/volume_8/2/pita.pdf
doi: 10.1145/1980522.1980527
arxiv: null
cite: 'Pita, J., Bellamane, H., Jain, M., Kiekintveld, C., Tsai, J., Ordóñez, F., & Tambe, M. (2009). Security applications: Lessons of real-world deployment. ACM SIGecom Exchanges, 8(2), 1-4.'
topics:
- fork-merge-security
- collective-decision
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: full
relevance: 3
citations: 18 (Crossref, 2026-10-03)
code: []
---

## Summary

Crossref records the title as "Security applications"; the PDF headline is "Security Applications: Lessons of Real-World Deployment". Short note on three deployed Stackelberg-game systems: ARMOR at Los Angeles airport (in use since August 2007, randomising road checkpoints and canine patrols), IRIS for the Federal Air Marshals (pilot since October 2009) and GUARDS for the TSA (in testing). The premise is that the defender commits to a randomised policy and the attacker observes it through surveillance. Lessons: solvers must scale, deployed systems are hard to evaluate, eliciting the game model is laborious, and users need to override schedules.

## Contribution

Practitioner account of committed randomisation in operation. Opened in place of the 2008 AAMAS ARMOR paper, which I did not reach.

## Key results

- Only qualitative outcome evidence: police reported more arrests for drug and firearm offences after ARMOR. No counts or control.
- Evaluation obstacles: security data cannot be published, controlled trials are unethical, external variables cannot be controlled.
- User overrides change the equilibrium outcome; flagged as open.

## Methods and models

Bayesian Stackelberg games, structured solvers, decomposed preference elicitation, mixed-initiative interfaces.

## Limitations and open questions

Demonstration of deployability, not a measurement of security.

## Relevance to us

- Q1: shows that publishing the distribution and hiding the draw has been operated at scale, and warns that deterrence is hard to measure. Hand-picking which sub-agent to merge is the analogue of an override and breaks the commitment.
Related: [[tambe-2011-security]], [[korzhyk-2011-stackelberg]], [[burianova-2025-secret]].
