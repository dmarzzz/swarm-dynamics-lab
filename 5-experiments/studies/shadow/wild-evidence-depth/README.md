# Evidence-depth card for incident artifact exports

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by shadow/sol-audit-gap; source `d7301e98` ([registry](../../../evidence-metadata.json), [rubric](../../../EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **1/4** — In this selected release, 7,733/91,037 payload artifacts have a direct response child; response-link coverage varies with artifact length. Basis: Complete corpus census, graph fixtures and separate same-author arithmetic agree. Selection, response semantics and original event independence are unknown; no success rate or causal inference is supported.
- **sample_size_summary:** Observed: one selected incident corpus; 189,579/189,579 rows analyzed, 91,037 payloads, 7,733 response-linked payloads; zero parse failures/exclusions. Rows are dependent artifacts, not independent trials. Zero model calls.
<!-- experiment-evidence:end -->

This standard-library-only tool reports parent-linked response coverage, reconstruction-only coverage, graph integrity and exact released-text duplication. It does not execute/decode payloads or infer success, agents or missing clocks. [FINDING](FINDING.md) is the one-page result; [PLAN](PLAN.md), [SETUP](SETUP.md), [PRE-RUN](PRE-RUN.md) and [POST-MORTEM](POST-MORTEM.md) preserve scope and lineage.

## Reproduce

Download the public export yourself from https://swarmtraces.org/data/final/redacted.jsonl.gz and keep it outside git. From this directory:

```sh
python3 -m unittest -v test_analyze.py
nice -n 10 python3 analyze.py --data /path/to/redacted.jsonl.gz --out results
nice -n 10 python3 reference_check.py --data /path/to/redacted.jsonl.gz --summary results/summary.json --out results/reference-check.json
```

Open `results/index.html` locally. No web server, network requests, models, API key, package install or target access is needed to analyze the export. Measured runtime here: 2.56 seconds, 181,320 KB maximum resident memory, one CPU. Input checksum lives in `results/summary.json`; a changed input is a different release, not a replication of these exact counts.

## Input and output contract

`--data` accepts newline-delimited JSON, optionally gzipped. Each row has unique `id`, `kind` (`payload`, `recovered_text`, `response`), nullable `parent_id`, nullable `time_utc`, and nullable string `text`. Unknown kinds, duplicate ids or cyclic ancestry fail closed. Orphan links are counted and retained. Missing text is not collapsed into one artificial event. Null times remain unavailable.

Outputs: aggregate `summary.json`, `length-strata.csv`, static `coverage.svg`, local `index.html`. No raw source text, URLs embedded in payloads, names or dataset rows are copied into outputs. Parent components are provenance groups, not independent samples. SHA-256 equality applies to the released redacted text only.

The adapter is deliberately narrow and reusable on exports with this artifact schema; it is not a universal swarm detector. AskSwarm owns the broader multi-corpus question interface. This tool can supply its evidence-coverage panel without modifying its package.

## Safe two-minute demo insert

Show the card for 15 seconds: "23,008 response rows does not mean 23,008 observed payloads. Only 7,733 payloads have any response child, 8.49% of the release. We show that missingness before asking what the agents achieved." Then switch to the broader AskSwarm comparison or the team's synthetic provenance experiments. Do not call this an attack-success rate.
