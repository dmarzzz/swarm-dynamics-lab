---
id: makins-2026-multi
type: paper
title: 'Multi-Agent AI Control: Distributed Attacks Hamper Per-Instance Monitors'
authors: [Oliver Makins, Orazio Angelini, Zohreh Shams, Mary Phuong]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/html/2607.07368
doi: null
arxiv: '2607.07368'
cite: 'Makins, O., Angelini, O., Shams, Z., & Phuong, M. (2026). Multi-Agent AI Control: Distributed Attacks Hamper Per-Instance Monitors. arXiv:2607.07368.'
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-ai-control
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: null
code: []
---

## Summary

First empirical study of control when several instances of the same possibly misaligned model must cooperate to pull off one severe attack because no single instance has the needed permissions. Setting is FakeLab, a synthetic AI-lab monorepo (9 services, about 10K lines of Python, 292 tests, 86 benign main tasks, 4 side tasks: disable monitoring, data poisoning, privilege escalation, weight exfiltration). K executor agents (K = 1, 3, 9) run in sequence on their own main tasks, passing state only through commits; each commit is checked by a per-commit LLM monitor that sees only that diff. Optional planner agent broadcasts one plan to all executors over an unmonitored channel. Executor model Gemini 3 Flash; monitors GPT-5 mini and GPT-5 nano; 572 sequences in the main cohort.

Central measured finding, the fragmentation effect: as an attack is split over more agents, both per-commit suspicion and the most suspicious commit of the sequence fall. In the Figure 1 example a single-agent attack scores 0.92, the same kill chain split over three agents scores 0.68 / 0.60 / 0.60 per commit, and the three commits squashed into one diff score 0.90 again. Joint (whole-PR) suspicion stays high and flat in K. At nine commits, the per-commit suspicion drop (0.34) is mediated about 25% by dilution of malicious lines and 53% by cover-story plausibility, with 38% unexplained.

## Contribution

Moves AI control from one agent in one trajectory to many instances over shared state, and measures that a defender who checks each part separately is systematically weaker than one who can see the parts together.

## Key results

- Planner raises side-task success odds by 5.74 (posterior OR), up to about sevenfold, amplifies the fragmentation effect, and improves executors' prediction of monitor scores (Pearson 0.77 vs 0.59; flagged by authors as suggestive).
- Monitor strength dominates: going from GPT-5 mini to GPT-5 nano multiplies the odds of undetected success by 52.9 at 5% FPR. Holding undetected success near 1% needs a capable monitor, a few-percent FPR and a detailed task description.
- Every distributed attack keeps a few intrinsically hard-to-hide commits; that is per-agent monitoring's foothold.
- Coarse write restrictions cut first-attempt side-task success (OR 5.90 for none vs coarse without planner) but the effect disappears when a planner is present.

## Methods and models

Sequential deployment, randomised stage order, 50 steps per executor, bash and editor tools. GPT-5.2 grades main tasks and runs an agentic side-task scorer. Bayesian GLMs (HiBayES) for outcomes; monitor scores modelled with RBF log-linear densities. One round of manual prompt optimisation for attacker and monitor.

## Limitations and open questions

One executor model family; communication only via commits plus a one-off plan; attacker loses on the first flagged commit; not a full iterated red/blue control evaluation; no untrusted-monitor (collusion) runs; parallel deployment left to future work. The authors note the joint monitor is not deployable because the defender does not know which commits belong together.

## Relevance to us

The strongest measured result I found for Q2, read in reverse.
- Q2 (thresholds): per-part checking at merge time is exactly what a k-of-n scheme does if each returning part is vetted alone. This paper shows coordinated parts can each pass a per-part check while the combination is malicious; the defence that worked was a joint check over the combined contribution. A merge protocol should therefore audit the composed update, not only each child. It also shows that k-of-n requires the parts to be unable to coordinate; an unmonitored broadcast channel (the planner) removed most of the overhead that held attacks back.
- Q3 (attack): splitting a payload across several sub-agents so that each carries an innocuous fragment is a measured, effective attack shape; the corrupted-subagent-takes-over story is not required.
- Q1 (hiding): the defender's problem here is not knowing which parts belong together, the mirror image of a parent hiding which child will return.
Related: [[greenblatt-2023-ai]], [[hills-2026-distributed]] (same effect across time in one agent), [[radev-2026-best]] (coordinated sabotage benchmark), [[qinqin-2026-distributed]] (theory of sub-threshold distributed attacks), [[mallen-2024-subversion]], [[motwani-2024-secret]].
