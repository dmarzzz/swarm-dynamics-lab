# Pre-run assessment: jev-qualification-01

- Experiment / owner / stage: Healing Helping Hands / vishesh/codex-regrowth-docs / S0 candidate-head qualification, 2026-10-04 UTC.
- Parent evidence: pilot-02-post.md and diagnostic-03-post.md; diagnostic-04 is separate ongoing local-model repair.
- Status: ready after adapter tests, immutable source registration, public-page verification and dedicated-host check. No model call precedes those checks.
- User authorized adding Jev as a separate model condition. It does not replace Laya's history or repair Qwen's base-agent failure.

## Design and assessment

Question: can Jev classify the narrow report/claim relation reliably enough to be considered as an independent decision head? Sixty new fictional reports, 20 per label, five new phrasings per class with four named methods; seed 8600 shuffles cases. Reused semantic concepts but previously unexecuted text, not a real-world benchmark. Model sees only claim and report. Rotated label order, same source-balanced three-way definition. Gate: >=85% overall, >=70% for every class, zero schema/provider errors. No tuning on these outcomes. Compare qualification descriptively, acknowledging different language fixtures; do not call it a paired model ranking.

The head receives no first-Qwen answer. Its typed choice and probability vector are validated for allowed labels, finite normalized probabilities and argmax consistency. Confidence is recorded, not treated as calibrated correctness. A pass only makes Jev eligible for a separately planned Qwen+Jev condition; Qwen must independently qualify. No autonomous swarm efficacy or heterogeneous superiority is inferred from this run.

## Changes and unresolved issues

| Issue | Change | Acceptance | Owner |
|---|---|---|---|
| Candidate head competence | Add Jev as distinct qualification, preserve Laya | Same unchanged class/overall gates | vishesh/codex-regrowth-docs |
| Route reproducibility | Pin model family, TypeSafe-only route, dated response snapshot | Refuse another provider/snapshot, no fallbacks | same |
| Shared credential safety | Local credential relay over private SSH tunnel | Key stays in local credential file; never in transcript, remote worker, artifact or journal | same |
| Spend | Single durable reservation ledger on credential relay | Reserve worst-case charge before dispatch; enforce call and dollar cap, no retries | same |

## Frozen execution plan

Verified public metadata on 2026-10-04: model `typesafe/jev-1.13`, only provider `TypeSafe` (route tag `typesafe`), served snapshot `typesafe/jev-1.13-20260917`; context 32,000; input $0.042/million tokens, output free. Use `POST https://openrouter.ai/api/alpha/decisions`, not chat completions or the latest/router aliases. Request provider `only: ["typesafe"]`, `allow_fallbacks: false`; reject a different response snapshot/provider. Re-read public endpoint pricing before launch and abort if higher or route unavailable.

Sources: [official model listing](https://openrouter.ai/typesafe/jev-1.13/), [Decisions API](https://openrouter.ai/docs/api/api-reference/alphadecisions/submit-a-decisions-request), [public endpoint metadata](https://openrouter.ai/api/v1/models/typesafe/jev-1.13/endpoints). These establish API semantics and quoted prices, not competence or actual authentication. Authentication has not yet been tested.

Maximum 60 attempted calls, 30 seconds each, 10 minutes total, no retries or fallback. This separately authorized Jev qualification has a conservative $0.10 ceiling (60 full-context requests would cost $0.08064 at the verified rate; expected spend much lower). Keep a single persistent local ledger, reserve $0.001344 before every call, and preserve uncertain/failed reservations. Do not clone this ledger or reuse this allowance for another experiment. Existing study/API caps remain unchanged.

Execution stays on exclusive sim-vishesh allocation `vishesh-healing-helping-hands`; same experiment, sequential requests. The local relay only supplies the authorized credential and forwards this frozen set of synthetic payloads; it performs no model computation. Restrict both ends to loopback over SSH, reject unknown or repeated payloads, cap payload bytes, stop after the attempt, and never log headers or raw exception bodies. Credential alias: local OpenRouter key file; its contents never leave the local forwarding process except in the authenticated HTTPS request to OpenRouter.

Source, prompt, fixtures, adapter and renderer must be committed before registration. Entry point `src/qualify_jev.py --out <new directory> --run-tldr <purpose>`. Plan receipt and source hashes precede calls. Journal request start/completed/failed with safe error types. Every assigned case has a terminal status; unresolved provider failure makes remaining cases not-run. Stop on a changed route, invalid usage/cost or schema; retain the failure.

## Visualization mapping

Mapping D1-J: a 3 × 3 count confusion matrix with explicit 20-case row denominators, model/served snapshot, gate status, 0–60 progress, latency and input token/cost totals. Cases use shuffled order; no swarm round or animation is implied. Expected labels are evaluator-only. Live progress JSON + hub start/final qualification record; PNG final fallback. Retain full safe call journal privately and public class counts. Check all matrix counts against terminal records; failures remain visible rather than substituted with decisions. A failed renderer does not rerun inference.
