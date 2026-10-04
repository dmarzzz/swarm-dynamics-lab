---
id: hu-2026-when
type: paper
title: "When Local Monitors Miss Compositional Harm: Diagnosing Distributed Backdoors in Multi-Agent Systems"
authors: [Yibo Hu, Ren Wang]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2607.11751
doi: null
arxiv: '2607.11751'
cite: "Hu, Y., & Wang, R. (2026). When Local Monitors Miss Compositional Harm: Diagnosing Distributed Backdoors in Multi-Agent Systems. arXiv:2607.11751."
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-identity-hijack
accessed: 2026-10-03
read_depth: skim
relevance: 5
citations: null
code: []
---

## Summary

A distributed backdoor splits a harmful payload across several agents' outputs so that each message passes a per-message monitor while the assembled result (for example, code that exfiltrates credentials) is the attack. The authors build a testbed with one dial, how much of the attack is visible in any single fragment, and compare local, taint-style, trained, marker-based and assembly-level monitors on the same fragments, plus an external prompt-injection benchmark and end-to-end agent runs.

## Contribution

Formalises an "observability boundary": once fragments are indistinguishable from benign traffic in a monitor's view, no detector on that view can catch them, however strong. Detection returns only when the monitor observes the assembled object in a representation where the payload is exposed.

## Key results

- Proved (under their definitions): local benignness of fragments implies no local detector can separate attack from benign traffic.
- Measured: across the testbed, an external benchmark and agent runs, local monitors lose signal exactly as local evidence is removed, and recover only when shown the assembled object.
- Measured: a monitor trained only on benign traffic recovers the attack's code structure across held-out encodings with 0.874 mean AUROC; a decoded-view gate that knows the encoding family blocks every tested attack.
- Measured: full-trace monitors and decoders still fail unless they reach the representation where the payload is exposed.

## Methods and models

Controlled fragment-visibility testbed; comparison of monitor families; end-to-end multi-agent runs. Skimmed: abstract and introduction.

## Limitations and open questions

Attack payloads are structured (code); open question named by the authors is how to find the exposing representation in general.

## Relevance to us

Q2, and the coordinated form of Q3. This is the strongest published reason why per-part checking at merge is insufficient: if an adversary corrupts several parts, it can split its payload so that each returning part's contribution is benign and only the merged state is harmful. A k-of-n threshold applied part by part does not bound this; the check must run on the merged object, in the right representation. It is the multi-agent counterpart of [[liu-2026-safe]] (fragments assembled by a summariser) and connects to [[ding-2026-colluding]] (components safe alone, unsafe composed) and [[makins-2026-multi]], [[hills-2026-distributed]] (distributed attacks against per-instance monitors).
