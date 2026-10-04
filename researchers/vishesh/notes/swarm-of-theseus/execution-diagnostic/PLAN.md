# Swarm of Theseus: targeted execution diagnostic D1

Status: prospective diagnostic; owner has now authorized admission work and D1 execution after its gates pass. Original v2 gates, failures and outcomes remain unchanged. Owner requested targeted repairs built, committed and pushed before the next useful run.

## TLDR

Question: which controlled interface repairs improve explicit-rule execution? Compare a fixed ladder of five interfaces on matched balanced cases: legacy learner-framed instructions, clean executor instructions, keyed evidence, no notebook, and one case per call. Measure exact correctness, false holds/ships, equivalent-input consistency, invalid/missing outputs and command semantics. Three independent worlds, four task/console contexts; 144 calls maximum, 480 assigned decisions, USD5 proposed cap, two hours, one worker, zero retries. This is a small diagnostic, not a culture-preservation experiment or causal study of model internals.

## Question and prediction

The prior13 repaired ceiling errors include seven false evidence statements, one correct-evidence/wrong-action, one notebook/command disagreement and four nonspecific errors. Clean executor wording removes a verified instruction mismatch. Keyed rows may reduce evidence-column confusion; omitting a notebook may remove conflicting output representations; atomic calls may reduce cross-case interference. These are predictions, not proven fixes. Adjacent paired contrasts isolate one interface change at a time; the ladder cannot identify interactions or establish a universally optimal combination.

## Setup

D1 uses three fresh world seeds610/611/612 (development seeds10/11/12; no model qualification or pilot seeds reused). World index rotates the ordered governing sources (probe/ledger, ledger/canary, canary/probe), ensuring every source governs each class once. Worlds share a finite task family, so even three worlds are not broad generalization evidence.

Each world has eight cases: for each of two classes, every governing signal/freshness pair00,01,10,11 occurs once. Independently permuted irrelevant-source bit pairs are balanced within class. Opaque case IDs derive from a separate seeded random stream, not class/index/bits. Row order is independently shuffled. Validate coverage and identity/ordering invariance before any dispatch. Release and incident use the same observations; incident ignores freshness. Migration is the release task in old versus renamed consoles on the identical cases. Four contexts per world: release, incident, migration-old, migration-new. Contexts and arms are not independent worlds.

## Protocol

Freeze five arms: A legacy/table/batch/notebook; B executor/table/batch/notebook; C executor/keyed/batch/notebook; D executor/keyed/batch/decisions-only; E executor/keyed/atomic/decisions-only. All receive the exact current class mapping and command documentation, no history, no feedback, no inherited notes and no answers. A deliberately retains old learner framing solely as comparator; it is never treated as the clean ceiling. B changes only instructions. C changes only evidence presentation. D changes only notebook request/schema. E changes only case batching. All source evidence remains visible in every arm; keyed presentation does not select the governing source for the agent.

Eight cases per context, four batch calls plus eight atomic calls:12 calls/context x4 contexts x3 worlds=144 calls. Each arm has96 assigned decisions across contexts. Release and old migration are matched duplicate semantics with different task labels, a diagnostic check rather than independent replication. Randomize call order reproducibly; atomic calls remain stateless. No within-run adaptations, selection, feedback, revision retries or agent replacement. A deterministic executor is an offline scoring fixture, never a model substitute. Do not add a second correction call or silently rewrite commands from the notebook.

Pinned model claude-haiku-4-5-20251001, temperature0, max1200 output tokens, maximum18000 encoded input bytes, fixed provider schema by notebook condition. Same output cap across arms. Calls/latency/token usage differ across batch and atomic arms; comparisons match assigned cases and worlds, NOT compute. Record those costs. No model-family claim. Pricing and authorized non-overlapping allocation must be freshly verified before launch; USD5 is a proposed maximum, not newly created authority. Never reset or reuse the stopped v2 deadline/ledger.

## Metrics

Primary descriptive contrasts B-A, C-B, D-C, E-D: per-world assigned accuracy difference, separately for release and incident, plus all three individual world differences. No significance claim or winner selection. Migration old/new semantic accuracy and command-validity differences are secondary paired diagnostics, not culture transfer. Report all arms and contexts even if worse.

Strict per-decision scoring: malformed schema, duplicate/unknown/missing ID, invalid command or provider failure retained in assigned denominators; no fallback answers. Record raw schema and transport errors separately; valid partial decisions may be separately described but strict headline accuracy marks an invalid response incorrect. Independently decode commands and recompute truth from visible evidence; verify primary score agreement. Report wrong-source-compatible signatures only descriptively.

Coverage invariance: for incident, cases with identical class/signal but differing freshness should match; for release, compare matched rule-equivalent cases across contexts and arms as descriptive agreement, not independent replication. Notebook contradictions are qualitative annotations preserving exact text; do not claim automatic free-text parsing measures them reliably. The old13 cases are regression/inspection fixtures only, excluded from new outcomes and qualification denominators.

No arm is automatically promoted to the culture pilot. A candidate for separately planned confirmation must have >=90% assigned accuracy in EACH world/context, 100% valid responses, no systematic omitted bit stratum and no console-translation failures. With eight cases per world/context,90% effectively means8/8; this is an explicit small-screen requirement, not a confidence bound. If no candidate qualifies, stop and preserve failures. If one does, freeze it and qualify on fresh held-out worlds before a new acquisition/turnover design. No unplanned repair in D1.

## Launch gates

Owner authorization update 2026-10-04T05:00Z: the owner explicitly verified the USD5 allocation and instructed independent review, a fresh host, plan update and then execution. No extra budget confirmation is required. The allocation must still be reserved once and verified operationally. Before D1: resolve applicable research/design review, publish immutable plan and current diagnostic-only pre-review; register exact URL and readable experiment/condition TLDRs; verify hash AND actual public page; obtain fresh exclusive fleet allocation and verify live workload; bind source/instrument/assignment hashes and fresh dependency/credential status; reserve non-overlapping approved USD5/144-call authority with current pricing and two-hour deadline. Native runner must reject blocked/stale/mismatched admissions, changed source, missing registration, duplicate output namespace and exhausted quotas. A local receipt or copied ledger cannot create spending authority. Review independence must be stated honestly.

## Visualization mapping

Live measured progress shows completed/assigned calls and cases, errors and conservative spend. Final report shows all five arms, paired world/context accuracy, coverage matrices and cost per assigned case. Saved calls support replay in dispatch order with arm, world, visible evidence, emitted action and viewer-only truth; atomic call order is not a cultural timeline. Missing/invalid rows remain visible. Offline examples say SCRIPTED SOFTWARE FIXTURE, NOT MODEL EVIDENCE. Full decision records are durable before reporting; reporting failures cannot trigger a model retry.

## Operational authorization update

The owner authorized D1 at USD5/144 calls/two hours, with one worker and no retries. This supersedes the build-only status but does not waive review or runtime gates. Since the fleet now routes new launches through orbital-one, dispatch will use the private agentops run queue, not a laptop launch. A fresh exclusive existing idle fleet allocation is sufficient; no new infrastructure purchase is included. Original scientific contrasts, seeds, assignments, metrics and stop rules are unchanged.
