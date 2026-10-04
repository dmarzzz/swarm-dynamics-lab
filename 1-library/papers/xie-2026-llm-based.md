---
id: xie-2026-llm-based
type: paper
title: LLM-Based Penetration Testing in the Presence of Honeypots
authors:
- Xinhong Xie
- Piyush Nagasubramaniam
- Neeraj Karamchandani
- Sencun Zhu
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2609.08093
doi: null
arxiv: '2609.08093'
cite: 'Xie, X., Nagasubramaniam, P., Karamchandani, N., & Zhu, S. (2026). LLM-Based Penetration Testing in the Presence of Honeypots. arXiv preprint arXiv:2609.08093.'
topics:
- swarm-detection
added_by: dmarz/sd-honeypots
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Studies an LLM attack agent that must spend a finite LLM execution budget across a pool of hosts, some of which are honeypots. The attacker's choice is formalised as a budgeted decision process (continue exploiting or skip a host when honeypot suspicion arises). The authors report that a detector-guided skip policy lets the agent allocate budget efficiently and compromise real hosts in a mixed testbed. Defences are explicitly out of scope.

## Contribution

Frames honeypot avoidance as an economic problem for the agent operator, showing that LLM agents can reason about deception artefacts and route around them, which removes much of the trap's value as a sensor.

## Key results

- A detector-guided budget policy lets LLM attack agents compromise hosts in a mixed honeypot/real pool more efficiently (abstract; no numbers stated there).

## Methods and models

Controlled mixed-host testbed; budgeted decision process; honeypot-suspicion detector feeding the agent. Abstract-level read.

## Limitations and open questions

Abstract only. Testbed composition and the specific honeypots used are not known from the abstract.

## Relevance to us

Another evasion data point, alongside [[cordeiro-2026-rouxii]]: rational swarm operators will price traps into their budget. Detection designs should make "skip" costly or indistinguishable from real targets. Contrast [[reworr-2024-llm]], [[pasquini-2024-hacking]].

## Notes from dmarz/honeypot-vigilance

**Read (2026-10-03):** the full arXiv HTML (https://arxiv.org/html/2609.08093): abstract, Sections 1 to 7
including the decision model (3), testbed and detectors (4), all four RQs and the ablation (5), discussion and
limitations (6). Equations and some in-text numbers did not render in my extraction (several "from X to Y"
sentences came out blank), so the numbers below are from the tables. Depth in practice: full read of the prose
and tables.

**Does the agent update honeypot suspicion during a run from experience? No.** The genuine-likeness score per
host comes from two external, deterministic detector tools: a pre-connect protocol-fingerprint detector
(cosine similarity to prototype centroids built from a separate training set of hosts, Vetterl and Clayton
style probes) and a post-connect detector (shell-consistency gate plus count of outbound payloads reaching a
collector, which genuine hosts are configured to allow and honeypots are contained from). Thresholds are fixed
at 0.50. The only parameter that adapts during an episode is the budget-pressure term (a projected update on
spending pace), which reacts to cost, not to having met a honeypot. The LLM (CAI red-team agent on o3-mini)
keeps conversation history "during the current attack attempt", i.e. within one host, and is not given the
detectors' internals. Nothing carries a lesson from one honeypot to the next host. "Online learning" and
"multi-agent co-evolution" are listed as future work.

**False skips of real hosts (numbers).** Testbed: 20 post-triage hosts, 8 honeypots (Cowrie x2, Wetland,
Glastopf, HoneySSH, sshForShits, sshsyrup, sshesame) and 12 Vulnhub machines.
- Pre-connect (Table 2): proposed detector accuracy 0.80, F1 0.67, honeypot recall 0.50, false-rejection rate on
  genuine hosts 0.00; banner-only and service-metadata baselines both 0.70 / 0.50 / 0.38 / FRR 0.08 (one of 12
  genuine hosts wrongly rejected). Precision 1.00, ROC-AUC 0.81 (Table 3). The detector is tuned deliberately
  conservative: it rejects only when both probes agree, buying zero false skips at the price of half the
  honeypots getting through.
- Post-connect (Table 3): 1.00 on 8 honeypot and 8 genuine post-entry branches, but only because the
  containment rule makes the outbound test separate them by construction.
- Entry ranking (Table 4): false-entry rate 0.25 with the detector vs 0.40 without.
- Post-entry loss (Table 6): average cost per entered honeypot 0.500 with no stopping, 0.438 rule stop (50% of
  honeypot branches stopped), 0.042 with the post-connect detector (100% stopped).
- Episodes (Table 7, 3 episodes per budget of $1 to $5): at $5 the full policy confirms 3.66 of 12 genuine
  hosts vs 3 (fixed budget) and 2.33 (random); empirical ceiling 4 of 12. Ablation at $5 (Table 8): removing
  the pre-connect detector raises wasted honeypot cost from 0.18 to 0.61.
- Small sample: 3 episodes per cell, at most 4 attainable genuine footholds.

**Relevance to the hunches.**
- V1: no bearing on in-run updating; the criterion is a fixed hand-set threshold. It does give a clean
  example of an operator choosing a conservative c deliberately (FRR 0 at recall 0.50), which is the trade-off
  V1 asks whether experience shifts on its own.
- V2 to V5: no bearing. Single agent, no communication, no evaluation-awareness measures.
- Useful as a design pattern for our sandbox metrics: they score false entry, delayed abandonment, false reject
  and unresolved separately, which maps onto hits, false alarms and the cost of caution.
