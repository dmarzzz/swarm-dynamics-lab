# Protocol / preregistration template

Status: DRAFT — replace every bracketed field before freezing. Record amendments separately rather than overwriting the registered version.

## Identity and scope

- Study ID, title, owner, date, version, preregistration timestamp/location/hash: [fill]
- Instrument, agent-behavior study, human-system simulation or agent-builder evaluation: [choose]
- Research question and target population: [fill]
- Prior evidence, competing explanations and proposed novelty: [citations]
- Primary estimand in one sentence, including population and failure treatment: [fill]
- Claim boundaries: [models, tasks, time, resource constraints, domains not represented]
- Evidence metadata: [evidence_confidence score or unassessed, scoped claim/rationale, assessment date/source; sample_size_summary separating observed from planned independent units and outcomes; use the shared experiments/EVIDENCE-METADATA.md rubric]

## Hypotheses and design

- Primary contrast and directional/two-sided hypothesis: [fill]
- Smallest effect of practical interest and justification: [fill]
- Co-required utility/safety guardrails, justified margins and joint decision/multiplicity rule: [fill]
- Secondary, mechanism and exploratory hypotheses: [separate lists]
- Experimental unit and assignment unit: [fill]
- Dependence/interference diagram, scenario families and persistent-state boundaries: [fill]
- Treatments and explicit configuration differences: [table]
- Controls: scripted, single agent, independent ensemble, relevant ablations: [fill]
- Budget matching estimand and baseline tuning allowance: [fill]
- Resource regime: [fixed total or per agent; evidence, attacker, verification and compute allowances; actual-use ledger]
- Scenario sampling, inclusion criteria and target weighting: [fill]
- Development/pilot/test/replication splits and contamination controls: [fill]
- Randomization, block variables, treatment order and seed schedule: [fill]

## Fixed system and inputs

- Agent definitions, prompts, model revisions, tools and orchestrator hashes: [paths/hashes]
- Context/access manifest, source snapshots, indexes and licenses: [paths/hashes]
- Environment/container, dependency lock, hardware and evaluator version: [fill]
- Initialization, reset, isolation, memory and communication schedule: [fill]
- Aggregate budgets, concurrency, retries, timeouts and stopping conditions: [fill]
- Credential aliases only; secret values are prohibited: [aliases or none]

## Measurement and quality assurance

- Primary endpoint, units, range, direction, denominator and timing: [fill]
- Terminal success, failure, abstention, censored and missing definitions: [fill]
- Reliability, severity, efficiency and process metrics: [fill]
- Scorer independence, protected truth, rubric and calibration: [fill]
- Human/LLM judge blinding, agreement, audit sample and disagreement rule: [fill]
- Instrumentation checks, positive/negative controls and fault-injection gate: [fill]

## Sample size and analysis

- Pilot dataset separate from confirmation; variance components and uncertainty: [fill]
- Agent count as a design factor; scenarios, repetitions and total runs by cell: [fill]
- N population/counting rule, G replacement waves or incidents, S independent roots, R stochastic repeats: [values or not applicable; distinguish identities, stateful agents and worker slots]
- Target effect or CI width, alpha/power, formula/simulation and sensitivity: [fill]
- Resource constraints and detectable-effect limits: [fill]
- Primary estimator, task weights, pairing, clustering/model and assumptions: [fill]
- Root-level paired interaction if claiming treatment-specific scaling; joint precision for primary effect and guardrails: [fill or not applicable]
- Effect sizes, intervals, diagnostics, subgroup/interaction plan: [fill]
- Multiple-testing family and correction: [fill]
- Fixed stopping or valid sequential boundaries; operational stops: [fill]
- Failed/missing runs, retry accounting, exclusions and sensitivity bounds: [fill]
- All-assigned operational endpoint and missing-outcome bounds; complete-case and conditional-on-acquisition sensitivity denominators: [fill]
- Analysis source/hash and synthetic-data validation: [fill]

## Execution, oversight and release

- Pilot go/no-go criteria; accountable human and permitted intervention: [fill]
- Instrument-defect versus competence-gate failure versus valid null/harm; uncertainty-based decision rule: [fill]
- Safety stops, restricted actions, incident handling and resume policy: [fill]
- Data minimization, retention, authorized access and export review: [fill]
- Planned ledger and monitoring policy; treatment effects hidden during execution: [fill]
- Launch-readiness references: [verified immutable public plan/TLDR; pre-run assessment; required independent review; assignment manifest; exact call/spend reservation; authorized allocation and applicable account-verification status; visualization mapping; keep private allocation details private]
- Cost/compute/human-assistance ledger and accounting scope: [fill]
- Replication package, licensing, unavailable assets and acceptance tolerances: [fill]
- Amendment table: date, trigger, previous hash, change, affected units, confirmatory/exploratory consequence: [fill]

Registration does not establish validity by itself. An unfilled template is not a preregistration. A local content hash establishes identity but not an independent public timestamp.
