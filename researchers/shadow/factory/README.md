# Shadow's small experiment factory

**Launch hold (PI review follow-up):** the legacy execution boundary is disabled in the accompanying containment patch, pending janitor review/merge. It lacks the full required registration, per-transport reservation, initialization-receipt and immutable-outcome contract. Do not use the historical resume commands below or refresh old source pins. Read [PI review response](PI-REVIEW-RESPONSE.md). Analysis of saved data is unaffected.

**Handoff: tool built, scientific execution blocked.** No model jobs remain running. 152 attempted assignments,100 valid,52 failures; no completed treatment finding. The native recovery screen returned HTTP503, and the paid key exhausted its shared daily allowance. See [operator handoff](HANDOFF.md), [honest result overview](FINDING.md), and [reporting corrections](CORRECTIONS.md). Twelve offline tests and652 internal recomputation checks pass. The five scientific questions have separate archived operational attempts, not20 independent experiments.

**Current launcher:** `pool_structured.py queue`, [native-pool amendment](AMENDMENT-NATIVE.md). The shared OpenRouter key exhausted its externally enforced USD5 daily limit after 100 valid structured calls, leaving only two complete main roots. Paid dispatch stopped; no key limit or credential was changed. New zero-paid native-schema cohorts use bounded HTTP429 backoff and complete-root scheduling. The authorized USD20 factory ceiling does not override the provider key's lower limit.

**Previous launcher:** `structured.py queue --watch`. The first paid route produced 20 prose-wrapped, schema-invalid answers; all are retained. The [prospective structured-output repair](AMENDMENT-STRUCTURED.md) adds native JSON-schema output and fresh clean-screen roots in separate `-or-json` cohorts, without increasing the aggregate budget. It stops the whole queue on a failed qualification rather than repeating an interface defect.

**Route update:** the five initial pool attempts returned 8 HTTP429 and 12 HTTP503 failures before any model answer (20 failed requests total). The [prospective paid-route amendment](AMENDMENT-PAID.md) adds separately committed `-or` attempts with a locked USD4/spec, USD20 aggregate ledger. Original attempts and the original runner remain unchanged. Use `paid.py queue --watch` for the amended queue. The original design/route description below is retained for lineage, not a claim the pool runs succeeded.

A queue of five one-file prospective exploratory studies, one resumable runner, one automatic closeout. Built under Shadow's 2026-10-04 Wave 4 instruction. This is a tool for closing small experiments, not another proposal queue. It never launches or modifies Dmarz's or Vishesh's studies.

## The operating change

Keep scientific safeguards, reduce repeated operational setup. Put the question, credit to parent, packet generator pin, assignment population, qualification, directional prediction, stop rules, cost cap, estimator and missing-data policy in **one committed JSON spec**. One command carries that spec through calls, checkpointing, analysis and a FINDING. Do not equate commit count, library size, native calls or a passing engineering test with findings.

These are authorized **exploratory replications/sensitivity checks**, not accepted formal hypotheses. No independent review is claimed. The general repository's survey and hypothesis gates still apply to formal promotion. This implementation does not change those rules.

## First queue

1. Sonnet 4.6, informative checks, 12 checks, parent's linked attacker.
2. Sonnet 4.6, unreliable checks, 12 checks, parent's linked attacker.
3. Sonnet 4.6, informative checks, 12 checks, no attacker-internal links.
4. Sonnet 4.6, unreliable checks, 12 checks, no attacker-internal links.
5. Sonnet 4.6, informative checks, four checks, parent's linked attacker.

Each is 12 clean qualification fixtures then 192 comparison calls over **48 paired roots**, not 192 independent observations. Total maximum 1,020 calls. The parent is [Dmarz's completed identity-splitting study](../../dmarz/notes/sybil-split-opus/RESULTS.md), credited without changes. Its frozen simulator, world seeds and public packet construction are reused; no source data or ledgers are copied over or edited. This is a **same-model-family** follow-up, not cross-family replication. Dmarz already owns Qwen/GPT cross-family follow-ups, which we do not duplicate.

The most informative added comparison removes the free attacker-internal links, a confound explicitly named in the parent's review. The parent already reported scripted attenuation without those links; the native Sonnet sensitivity check is incremental evidence, not a new conceptual discovery.

## Run

From repository root, Python 3 plus PyYAML:

```sh
python3 researchers/shadow/factory/test_factory.py
python3 scripts/lab.py check
# Specs and runner MUST be committed before the following command:
nice -n 10 python3 researchers/shadow/factory/factory.py queue --watch
# Or one fixed spec:
python3 researchers/shadow/factory/factory.py run --spec split-sonnet-linked-strong
# Deterministic re-analysis, no model calls:
python3 researchers/shadow/factory/factory.py analyze --spec split-sonnet-linked-strong
```

`--watch` sleeps 60 seconds when the finite queue is done. It does not generate new studies or repeat terminal studies. New prospective specs may be added only after committing them. The dispatcher refuses new calls at **2026-10-04 22:00Z**, even if restarted; in-flight requests have a 90-second timeout. This implementation runs on shad0wbot, four concurrent HTTP requests and negligible CPU, `nice 10`. No nyx-node dependency or production-container operation is needed.

### Credential and spend policy

Native Claude Messages API through the established local pool at `127.0.0.1:18811`. The key is read from `~/.moltbot/secrets/pool-keys.json`, never saved or printed. Paid routes are **disabled in code**. Each spec has a hard USD0 external-paid cap, so aggregate paid spend is bounded by USD0, strictly below the authorized **USD20 factory ceiling**. No OpenRouter key is read and no automatic paid fallback exists. If someone wants paid fallback later, that requires a new budget-reserving adapter with tests and prospective spec amendment; a command-line model override cannot enable it. Pool token usage is recorded and is not described as zero compute cost.

### Minimal safeguards, not zero safeguards

- Pin runner and parent generator/scorer/prompt/design SHA-256. Dirty/uncommitted specs and source drift fail before calls.
- Strict JSON schema, exact returned model, usage and stop-reason validation.
- Qualification is 12/12 exact clean fixtures; any failure blocks comparison calls. This is narrower than the parent's 60-fixture qualification.
- Journal a dispatch before the request, fsync terminal outcomes, exclusive per-spec lock. A crash leaves an `interrupted_unknown` result, never a silent answer retry.
- No retries. All attempted, failed, unstarted, and valid denominators remain explicit. Three failed calls stop new batches, up to four requests may already be in flight.
- Resume checks the spec, source and full assignment digest; no last-valid-outcome selection.
- Signed missing-outcome bounds and within-family root bootstrap. The family means are equally weighted.
- Five dependent exploratory contrasts, no multiplicity correction. `finding` is only a within-spec descriptive label requiring complete data, competence and a directional CI beyond 10 points; `negative` means that criterion was not met, not equivalence; incomplete results are `lead`.

## Outputs and closeout

Every spec gets `results/<id>/records.jsonl`, `dispatch.jsonl`, `provenance.json`, `summary.json`, `cells.csv`, `FINDING.md`, and terminal status. The packet itself is deterministically reconstructed from pinned source; answer text and usage are saved. The CLI analysis recreates the tables from terminal rows. Hub registration and evidence metadata are handled by the companion closeout script; they do not authorize calls or promote a hypothesis.

## Diagnosis: why many commits do not imply many findings

This is a qualitative diagnosis from a small operational sample, **not a causal audit of every team commit**. Read at base `66fa0aa6` and subsequent task-claim rebase.

1. **The scan pipeline optimizes a different output.** `PIPELINE.md` explicitly feeds scan only: collectors -> batches -> claimable catalogue issues. It does not promise experiment throughput. `STATUS.md` has hundreds of entries per topic while multiple experiment tasks still await qualification or review. Stop treating catalogue throughput as evidence throughput. Credit: deduplication and ownership made a large literature base tractable.
2. **Every small experiment repeats a large operational package.** The [split pre-run assessment](../../dmarz/notes/sybil-split-opus/reviews/chain-001-pre.md) describes four stages, source/manifest pins, separate launcher, hub gates, 55 selftests, mutation tests, review, fleet reservation and full artifact replay. These safeguards caught genuine risks and its [post-run review](../../dmarz/notes/sybil-split-opus/reviews/chain-001-post.md) reconciles 2,749/2,749 valid calls with saved records. Keep that rigor for large runs, reuse tested infrastructure for small extensions instead of rebuilding it.
3. **Large all-or-nothing grids are operationally fragile.** The parent pre-run plan halted S1 on its first failed call; subsequent studies added transport retries and missing bounds. Small predeclared contrasts and checkpointed terminal outcomes produce interpretable partial evidence without selecting only successful reruns.
4. **Design and model-route churn can precede the first observation.** The [program v5 methods review](../../dmarz/notes/overnight-program-2026-10-04/methods-review-v5.json) explicitly calls seven-hour viability conditional on a new instrument. [Scale Opus](../../dmarz/notes/sybil-scale-opus/README.md) documents deferral and resumption around queue/load priorities. Do one clean probe/qualification and a small primary contrast first, then decide whether a larger new design fits the clock.
5. **Closeout, not launch, is the unit of progress.** Our capture-memory-mix reporting defects (retry lineage, denominators and captions) show why automatic tables must remain linked to immutable attempts. Here the same persisted records drive the table, CI, generated finding and registry summary. A failed qualification is a completed diagnostic report, not something to hide or keep tuning against.

### Five concrete actions before the deadline

- **Us:** run the five bounded contrasts, prioritize the no-internal-link sensitivity, and ship every terminal outcome. Payoff: a reusable execution tool plus a directly scoped robustness check.
- **Us:** make saved raw answers -> analysis -> finding -> evidence entry a single closeout. Payoff: fewer stale headlines and denominator disagreements.
- **Dmarz, optional adoption:** wrap already-reviewed packet generators in a short spec rather than duplicate another large package for each model/configuration. Payoff: lower setup time without discarding scientific gates.
- **Vishesh, optional adoption:** terminate a failed capability screen with a diagnostic artifact and require a new dated spec for repairs. Payoff: honest submission-ready negative results instead of apparently endless qualification.
- **Us:** reserve the final two hours for recomputation and submission integration, not new grids. Payoff: results the judges can inspect and reproduce rather than READY files.
