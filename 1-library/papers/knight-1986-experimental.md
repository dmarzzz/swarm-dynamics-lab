---
id: knight-1986-experimental
type: paper
title: An Experimental Evaluation of the Assumption of Independence in Multiversion Programming
authors:
- John C. Knight
- Nancy G. Leveson
year: 1986
venue: IEEE Transactions on Software Engineering
url: https://web.archive.org/web/2020/http://sunnyday.mit.edu/papers/nver-tse.pdf
doi: 10.1109/TSE.1986.6312924
arxiv: null
cite: 'Knight, J. C., & Leveson, N. G. (1986). An experimental evaluation of the assumption of independence in multiversion programming. IEEE Transactions on Software Engineering, SE-12(1), 96-109.'
topics:
- fork-merge-security
- collective-decision
added_by: dmarz/fm-bft-aggregation
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: 543 (Crossref, 2026-10-03)
code: []
---

## Summary

The classic test of whether independently built versions of a program fail independently, which is the axiom behind majority voting over N versions. Students at two universities (9 at UVA, 18 at UCI) each wrote a Pascal "launch interceptor" program from one carefully debugged specification; all 27 passed a 200-case acceptance test and were then run on one million random inputs against a gold program. Individual versions were very reliable (6 never failed, 23 of 27 succeeded on more than 99.9 percent of inputs), yet 1255 inputs made two or more versions fail at once, and one input made 8 of 27 fail. Under an independence model this gives z = 100.51, so independence is rejected at 99 percent confidence. About half of the 45 faults found were shared by two or more versions, and every common fault crossed the two universities.

## Contribution

First statistically designed test of the failure-independence assumption in design diversity. It shows that k-of-n voting reliability computed from per-version failure rates can be badly optimistic, because hard parts of a problem attract the same mistakes from independent developers.

## Key results

- Measured: 27 versions, 10^6 tests, K = 1255 coincident failures (2 versions: 551; 3: 343; 4: 242; 5: 73; 6: 32; 7: 12; 8: 2). z = 100.51 against independence.
- Measured: per-version failure counts range from 0 to 9656 per million.
- Measured: correlated faults were "far more obscure" than unique ones: comparing cosines instead of angles under limited precision (4 of 27 versions), and missing the 180-degree collinear case. Several survived the acceptance test.
- Observed: no shared faults were traceable to the specification; the authors attribute them to intrinsically hard parts of the problem (numerical analysis, geometry case analysis).
- Interpretation by the authors: common faults may be the ones testing is least likely to catch, so filtering by acceptance test may enrich for correlated faults.

## Methods and models

Independence model: with per-version failure probabilities p_i, P_more = 1 - P_0 - P_1 is the probability that two or more versions fail on an input; the count of such inputs is binomial, and a normal approximation gives the z statistic. Failure is any of 241 Boolean outputs differing from the gold program, or an exception.

## Limitations and open questions

Student programmers, small programs (327 to 1004 lines), one problem domain. The authors stress the result may not generalise and that N-version programming can still help if reliability is computed with a coincident-error model. A 2026 replication with AI coding agents on the same specification found the same rejection [[ron-2026-n-version]].

## Relevance to us

Q2, directly. A k-of-n merge rule for forked sub-agents only forces an attacker to corrupt k parts if the parts fail independently. This paper is the empirical baseline showing that independently produced parts share failure modes when they face the same hard inputs. For LLM sub-agents the shared cause is stronger: same base model, same prompts, and, in the fork-merge threat, the same hostile information domain. The LLM analogues are [[kim-2025-correlated]], [[goel-2025-great]], [[nogueira-2026-systematic]] and [[ron-2026-n-version]]. The design-diversity proposal it tests is [[avizienis-1985-n-version]].
