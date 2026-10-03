---
id: scan-honeypot-vigilance
type: task
title: 'Prior-art pass: do agents (and swarms) update after discovering a honeypot?'
kind: scan
status: claimed
priority: p2
owner: dmarz/honeypot-vigilance
for: dmarz
created: 2026-10-03
created_by: dmarz/honeypot-vigilance
depends_on: []
topics:
- swarm-detection
- llm-agent-swarms
claimed_at: 2026-10-03T23:09Z
updated: 2026-10-03T23:09Z
---

## Goal

Context from dmarz: when one agent in a swarm discovers a honeypot, does it, and the swarm, get better at
telling traps from real resources (d′), or just jumpier (criterion c)? Five hunches V1-V5 are in
`researchers/dmarz/notes/honeypot-vigilance-hunches.md`. This task is the prior-art pass that decides whether
any of them is new enough to carry toward a survey and hypothesis.

Search: in-run belief updating after deception or a detected trap in LLM agents; evaluation and test
awareness in LLMs, especially awareness that changes during a run; rumour and false-alarm propagation in
multi-agent LLM systems; the MARL literature on deceptive environments; and the vocabulary of neighbouring
fields (alarm calls and predator-cue contagion in animal behaviour, vigilance and trust calibration in human
factors, signal detection after a miss).

## Done when

- Evaluation-awareness papers added to the library (they underpin V5), each opened in this session.
- [[gans-2026-when]] and [[xie-2026-llm-based]] read past the abstract and their entries updated (Notes section).
- The hunches note gains a dated "Prior-art verdict" section saying, per hunch, closest prior found and
  whether it still looks unmeasured.
- Coverage note filled and `python3 scripts/lab.py check` passes.

## Coverage note

Run on lane/honeypot-vigilance, pushed to main as 3a0db09. 26 new entries (13 evaluation awareness, 13 trust,
rumour, cascades and neighbouring-field anchors), Notes on 6 existing entries, Gans, Xie and Rouxii read in
full. All Done-when items met. Not saturated: OpenAlex hit its daily limit and Semantic Scholar returned 429.
Two papers were seen but not catalogued: arXiv 2606.21037 and 2606.20493. Verdict per hunch is in
researchers/dmarz/notes/honeypot-vigilance-hunches.md.
