# How to win agents and influence swarms

## Follow-up design

The [scenario redesign and candid assessment](../influence-swarms/scenario/README.md) replace the planned scalar-score follow-up with deeper procurement cases, a cheaper generalist baseline and model decision authority. Historical results below remain unchanged.

## TLDR

**Completed pilot, audited:** 50/50 valid outcomes, 750 model calls, USD 2.002637. Verification evidence often failed to govern the final choice. This is an exploratory result with one fixture per domain, not a robustness estimate. See the [quality assessment](reviews/quality-post.md), [visualization mapping](reviews/visualization-mapping.md), and [prospective repair](../influence-swarms/README.md). The repaired architecture has not yet been qualified live.


Can nine agents choose correctly when an outsider edits the evidence they read? Compare private review, discussion, random checks, targeted checks and source-lineage handling at matched call slots. Procurement is primary; dependency selection and travel are transfer probes. Measure harmful choices, correctness and regret on fictional fixtures. Qualification and scripted runs do not establish attack resistance.

A working nine-agent, three-application exploratory experiment. Procurement is the main test; software dependency selection and travel planning are transfer probes. The outside attacker edits evidence, while every team member retains the legitimate user goal. All candidates, documents, quotes and scores are fictional fixtures.

The original [v1 instrument](../actual-experiments/external-influence/) tested invoice-provider selection. Its first live run was only a clean qualification: seven valid/correct outcomes from 67 calls, approximately USD 0.1649 reported usage. It did not measure live attack resistance. V2 has a new experiment ID and does not rewrite those results.

Nine agents comprise six analysts, two check interpreters and one chair. Each arm uses 15 calls. Private review, peer discussion, random independent checks, targeted independent checks and explicit source lineage are compared with the same objective. Five-agent variants are also executable in engineering tests; paid scenarios use nine agents.

Read [the protocol](preregistration.md), [research basis](RESEARCH.md), [executable assignments](design.yaml) and [deployment record](DEPLOYMENT.md). The protocol gives controls, variable/fixed factors, denominators, failure policy and what the sample cannot establish.

```sh
python3 -m unittest discover -s researchers/vishesh/notes/external-influence-v2/tests -v
python3 researchers/vishesh/notes/external-influence-v2/src/runner.py plan --stage S0 --backend anthropic
python3 researchers/vishesh/notes/external-influence-v2/src/runner.py local --stage engineering --out /tmp/influence-v2-new-output
```

Use a new output directory; overwrites are refused. Model workers use an in-memory credential supplied by the approved credential store, the pinned model-config.json, and the existing shared spending ledger. The native S1 gate requires an exact-source valid S0. Scripted outputs are engineering checks, never LLM results. S2 is unavailable.

[Live experiment](https://swarm-live.pages.dev/#/x/external-influence-v2). Source and preregistration are committed before model execution. Raw synthetic calls, private commitments, citations, verification selections and outcomes are uploaded as compressed artifacts with a checksum index. No organization ID, workspace ID, API key or private infrastructure address belongs in this public directory.

## Question and prediction

Does decision-focused independent checking reduce harmful choices more than discussion or random checking? Treat any directional prediction and qualification gate as specified in the linked preregistration; this summary adds no new preregistered claim.

## Setup

Nine agents comprise six analysts, two check interpreters and one chair. Fictional procurement is the main application; dependency and travel tasks probe transfer.

## Protocol

Hold the underlying task and external evidence exposure fixed across policies. Compare private review, discussion, random verification, targeted verification and source lineage with 15 call slots per arm. S0 qualifies clean task competence before S1. See design.yaml for exact assignments.

## Metrics

Report harmful target selection, correct legitimate choice, utility regret, invalid outcomes and actual cost. Keep procurement primary and transfer results separate; count tasks rather than agents as independent units.

## Running a version with local agents

A prospective local-model variant replaces historical Haiku calls with shared local Qwen3 0.6B weights while retaining the same nine-agent teams and task protocol. It starts with six clean/superior competence screens across all three domains; a passing model can repeat the original 50 assignments (450 episode-local identities). Qwen3 1.7B is a declared fallback if 0.6B fails qualification. Four simultaneous calls bound the desktop load. See the [local experimental plan](local-agents/PLAN.md) for qualification gates, historical comparators, metrics, diagnostics and limitations. No result is claimed yet; registration and competence gates precede inference.
