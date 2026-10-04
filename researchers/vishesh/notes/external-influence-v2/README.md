# External influence v2

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
