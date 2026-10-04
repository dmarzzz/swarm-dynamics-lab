---
id: cordeiro-2026-rouxii
type: paper
title: 'Rouxii: Exploiting Honeypots with Deception-Aware AI Pentesters'
authors:
- Arthur Cordeiro
- Alberto Maria Mongardini
- Emmanouil Vasilomanolakis
year: 2026
venue: arXiv preprint
url: https://arxiv.org/html/2609.26555
doi: null
arxiv: '2609.26555'
cite: 'Cordeiro, A., Mongardini, A. M., & Vasilomanolakis, E. (2026). Rouxii: Exploiting Honeypots with Deception-Aware AI Pentesters. arXiv preprint arXiv:2609.26555.'
topics:
- swarm-detection
added_by: dmarz/sd-honeypots
accessed: '2026-10-03'
read_depth: skim
relevance: 5
citations: null
code: []
---

## Summary

An evasion result. Rouxii is an LLM-orchestrated pentest framework with deterministic reconnaissance and exploitation operators. Two matched cohorts differ only in the system prompt: "vanilla" sees raw probe output; "anti-deception" also gets known honeypot fingerprint signals and a classification rule. Across three reasoning models, eleven network setups and twelve cycles (1,544 attack reports), correct honeypot identification rose from 19% to 97% (OT services 11% to 97%) with 0.7% false alarms on real services. Deception-unaware baselines (PentestGPT, HackingBuddy) behaved like the vanilla cohort. A white-box analysis then turned detected honeypots against their operators: a malformed Modbus header hangs Conpot while TCP liveness checks still pass, and a one-byte gate lets an attacker overwrite GasPot's station name, corrupting the intelligence it reports.

## Contribution

The strongest negative result in this lane: honeypot efficacy against AI attackers is a function of what the attacker's prompt knows, and published fingerprints are cheap to hand an agent. The authors find "framing, not evidence, is the binding constraint": both cohorts saw the same signals at nearly the same rates.

## Key results

- Honeypot identification 19% (vanilla) vs 97% (anti-deception); OT 11% vs 97%; false alarm on real service 0.7% (measured, 1,544 reports).
- Demonstrated DoS of Conpot invisible to liveness monitoring; demonstrated intelligence corruption of GasPot; a Cowrie address-filter flaw shown as a primitive toward "deception overflow" (not demonstrated end-to-end).
- Adapts Honeyquest probes ([[kahlhofer-2024-honeyquest]]) to LLM attackers to measure enticingness and detection.

## Methods and models

Testbed of Cowrie, Conpot, GasPot plus real services; LLM orchestrator as the only stochastic component; verdicts scored against a deterministic oracle; SIG_CHAIN check that a verdict cites concrete signals. Skimmed: intro, related work, threat model, honeypot-exploitation section and framework design.

## Limitations and open questions

Open-source, well-fingerprinted honeypots only; custom or LLM-generated honeypots ([[bridges-2025-sok]]) may be harder. The "aware" prompt encodes fingerprints already published, which is realistic for a capable operator.

## Relevance to us

Any trap we design for swarms must assume the operator can paste our published tells into the agent's system prompt. It argues for per-deployment randomised canaries (as in [[seiden-2026-identifying]]) over a fixed honeypot product. Contrast with [[pasquini-2024-hacking]] and [[reworr-2024-llm]], which assume unaware agents; theoretical counterpart in [[gans-2026-when]].

## Notes from dmarz/honeypot-vigilance

**Read (2026-10-03):** the full arXiv HTML (https://arxiv.org/html/2609.26555): Sections 1, 4 and 5 in full,
Section 6 (grounding, false positives, questionnaire), Section 7, the conclusion, and Appendices C (seven-axis
profile), D (repetition stability) and E (automation, prompts). Section 3 (honeypot exploitation) and the
disclosure appendix only skimmed. Depth in practice: full read of evaluation and methods.

**Within-run learning: none, by design.** Each verdict is "sampled once, then frozen". The 12 cycles are
described (Appendix D) as "12 independent draws of the orchestrator's own decision policy" against a fixed
environment: same honeypot suite and deterministic operators, no state carried between runs. Within a run the
attacker loop feeds accumulated session context back to the model, but one run covers one setup (at most one SSH
service plus the OT slots), so there is no sequence of later resources on which a discovery could show an
effect. The paper reports no before/after or order analysis.

**False-alarm dynamics across the 12 cycles: none reported as a trend.** Only pooled false-alarm rates on the one
real service (real SSH, 142 deployed instances per Rouxii cohort): anti-deception 1/142 (0.7%), vanilla 7/142
(4.9%), PentestGPT 19/101 (18.8%), HackingBuddy 35/182 (19.2%). There is no OT false-alarm control (no real OT
device). Appendix D gives only the per-repetition range for detection: vanilla never above 23.8%,
anti-deception never below 94.0% across the 12 repetitions. Note: the conclusion quotes PentestGPT and
HackingBuddy false-positive rates of 13.2% and 17.7%, which do not match the 18.8% and 19.2% in Section 6.2.

**Signal-detection reading (my computation from their counts, not the authors').** Pooled over protocols the
false alarms are SSH-only, so the SSH-only figures are the cleaner ones. SSH hits are cowrie verdicts from
Table 2 (vanilla 98/144, anti-deception 141/144).
- Vanilla SSH: H 0.68, F 0.049, d′ about 2.1, c about 0.59.
- Anti-deception SSH: H 0.98, F 0.007, d′ about 4.5, c about 0.21.
- Pooled all protocols (hits over 1,008, F from SSH): vanilla d′ 0.76, c 1.27; anti-deception d′ 4.35, c 0.28.
- PentestGPT and HackingBuddy SSH come out at or below chance (d′ about -0.7 and -0.1), but their misses include
  stalls and null verdicts, so this mixes interaction failure with judgment.
So being told (system-prompt framing) moved d′ a lot and c only moderately toward liberal, while false alarms
fell. The authors make the same point in words: "The low anti-deception rate does not reflect a conservative
bias."

**Other numbers relevant to vigilance.**
- Evidence parity: at least one fingerprint signal is logged on 1232/1237 vanilla and 1247/1252 anti-deception
  instances; on OT the triggering fingerprints fire on 853/857 vs 861/861. Detection still differs 19% vs 97%.
- NEXT_BLIND to NEXT_AWARE (same report, plus a warning that honeypots are present): among targets the blind step
  wanted to exploit (real and honeypot alike), the warning switches the plan to AVOID_TARGET in 23.0% (183/795)
  vanilla and 40.1% (234/584) anti-deception. This is the paper's only measure of a warning changing behaviour,
  and it is pooled over real and decoy targets, so it cannot say whether the avoidance is selective.
- Detection does not imply avoidance: of targets the model itself flagged as honeypots, the warned next step
  still recommends HONEYPOT_EXPLOIT in 27.0% (53/196) vanilla and 21.0% (225/1072) anti-deception.
- At the sabotage gate the model commits on 72% (140/195) vanilla and 99% (655/663) anti-deception; sabotage
  success 34% vs 67%.

**Relevance to the hunches.**
- V1: no in-run discovery, so no direct measurement. The cohort contrast is the static anchor: with the same
  evidence, knowing the tells raised d′ by roughly 2 to 3.5 and lowered false alarms, which is the "better, not
  jumpier" outcome. V1 asks whether a discovery made mid-run reproduces this or only moves c.
- V3: the closest available data. Operator framing (system prompt) produced the d′ gain; a bare warning
  (NEXT_AWARE) produced more avoidance (23% and 40% switching) with no evidence of selectivity reported. A bare
  warning without tells is the rumour condition; this paper suggests it moves action but leaves the d′ question
  open, because the switch rate is not split by real vs honeypot target.
- V4: the vanilla false alarms (4.9%) and external baselines (about 19%) show a non-trivial base rate of calling a
  real SSH service a honeypot, which is the seed a false-alarm cascade needs. No propagation measured.
- V5: the authorization framing is held constant; no evaluation-awareness measures.
