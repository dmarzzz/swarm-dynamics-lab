# A practical research guide to experiments with AI agents

Research cutoff: **3 October 2026 (UTC)**. Reusable methods and offline tooling for swarm-lab research. This is a reusable methods package, not a gate-passing survey, accepted hypothesis, or executed LLM experiment. Read [swarm-lab integration](INTEGRATION.md) before adapting it to a research project.

For new studies, start with [the setup runbook](EXPERIMENT-SETUP.md) and copy [the setup record](templates/experiment-setup.md). Then use [the main guide](GUIDE.md), copy [the preregistration template](templates/protocol.md), and adapt [the worked collective-sensing example](examples/collective-sensing/PROTOCOL.md). The [literature review](LITERATURE.md) distinguishes verified research findings, authors' proposals, and this guide's recommendations. [Search notes](SEARCH-LOG.md) document coverage and limits.

For existing studies, use [experiment operations](OPERATIONS.md): `python3 scripts/experiment.py list` from the repository root locates the ten named research areas, their setup/post-mortem references and adapter coverage. Inspection is offline. The first native adapter covers Theseus v2 only; registry membership and prepared packets do not establish current launch readiness.

| Artifact | Purpose |
| --- | --- |
| [OPERATIONS.md](OPERATIONS.md) and [operations.json](operations.json) | Command entry point, study discovery, iteration lineage, implemented boundaries and missing launch evidence |
| [RUN-REVIEW.md](RUN-REVIEW.md) | Required pre-run assessment, post-mortem and repair/rerun cycle |
| [Experiment evidence metadata](../../experiments/EVIDENCE-METADATA.md) | Defined 0–4 evidence-confidence scale, independent sample-size summaries and update workflow |
| [GUIDE.md](GUIDE.md) | Definitions, study lifecycle, statistical design, reliability, and replication |
| [AGENT-LIFECYCLE.md](AGENT-LIFECYCLE.md) | Agent identity, actual initialization receipts, context, memory, reset and fork semantics; recommended production contract |
| [AGENT-LIFECYCLE-RESEARCH.md](AGENT-LIFECYCLE-RESEARCH.md) | 29 annotated research/practitioner entries and access limits |
| [HARNESS.md](HARNESS.md) | Framework choices, architecture, isolation, deterministic startup, execution and replay |
| [LITERATURE.md](LITERATURE.md) | Evidence synthesis and annotated bibliography |
| [templates/protocol.md](templates/protocol.md) | Reusable protocol and preregistration |
| [templates/agent-definition.json](templates/agent-definition.json) | Immutable agent definition template |
| [templates/context-access.json](templates/context-access.json) | Context, data provenance, permissions and retrieval template |
| [templates/run-config.json](templates/run-config.json) | Experiment scheduling and execution policy template |
| [schemas/README.md](schemas/README.md) | Schema contract and field semantics |
| [CHECKLISTS.md](CHECKLISTS.md) | Implementation, analysis, reporting and independent replication checks |
| [examples/collective-sensing/PROTOCOL.md](examples/collective-sensing/PROTOCOL.md) | Concrete swarm experiment, sample-size calculation and interpretation |
| [examples/collective-sensing/RESULTS.md](examples/collective-sensing/RESULTS.md) | Executed scripted demonstration and linked raw artifacts |
| [scripts/toy_harness.py](scripts/toy_harness.py) | Offline, standard-library demonstrator; no network or model calls |
| [scripts/validate.py](scripts/validate.py) | Artifact/schema, pairing, replay and integrity checks |
| [VALIDATION.md](VALIDATION.md) | Actual checks performed and remaining limitations |

The historical demonstration used the commands below with Python 3.10 or newer. Before a new Swarm Lab run, follow the public-plan registration and launch gates in [the lifecycle runbook](AGENT-LIFECYCLE.md). The default validator executes the demonstration twice; it is not a read-only audit command:

```sh
python3 scripts/toy_harness.py --config examples/collective-sensing/config.json --out ../../data/agent-study-demo
python3 scripts/validate.py
```

Choose a new output directory for each execution. The harness refuses to overwrite an existing directory. It simulates explicitly programmed policies and demonstrates experiment bookkeeping; its output cannot support claims about LLMs, human groups, or real scientific discovery. No third-party packages or credentials are required. The configuration templates contain deliberate `REPLACE_...` placeholders and are **not ready for paid execution**.

Source records belong to the shared library; this toolkit provides methodology and conservative reading annotations. The [integration guide](INTEGRATION.md) maps the package to the lab workflow and its research gates.
