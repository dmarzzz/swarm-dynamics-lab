# Poietic Agents first qualification assessment

2026-10-04 UTC · prospective assessment v0.1 · author vishesh/codex-heterogeneous

**Decision: blocked for execution; design prepared for review.** This is an author assessment, not independent approval. No attempt has started and no post-mortem is implied. There is no preceding Poietic attempt to read.

## Question and decision value

Can each proposed model execute its exact assigned contract on clean, fresh, independently scored probes? The generalist must interpret the tasks and tools; the cheaper generative model must do its allowed subset; Jev must choose among supplied typed options. Qualification decides which executor contracts may enter the first swarm pilot. It does not test swarm advantage or spontaneous differentiation.

The strongest check is an independently calculated reference answer with positive and negative fixtures: correct fresh evidence, stale-but-numerically-correct evidence, an unavailable provider, changed schema, no eligible result and attempted denied access. A model that merely emits valid JSON has not passed task competence.

## Planned assignment and acceptance

Forty-eight unique probes per candidate contract; 144 logical requests, at most 288 physical requests with one eligible transport retry. At least 44/48 correct and 48/48 schema-valid outputs per contract; zero protected-access violations. Probe families are balanced before dispatch and kept disjoint from prompt-development fixtures. A transport retry is attached to its original probe. Malformed outputs remain failures. Any model/adapter change requires fresh qualification inputs before calling it qualified.

Exact model identities, revisions/settings, prompt templates, data generator, pricing, contract assignments, evaluator and code hashes are not yet resolved. They must be added in a new version before dispatch; this assessment cannot stand in for that freeze. The [design](../design.yaml) fixes intended stage ceilings and split namespaces, not a runnable backend configuration.

## Design risks and required checks

- Validate independently hand-derived answers and stale-but-correct rejection; ensure protected labels never enter request bodies.
- Verify each contract is actually implemented by its designated backend. Jev receives typed choices; no hidden generative fallback.
- Meter all usage and retries with atomic reservation; stop rather than exceed the shared allowance.
- Record initialization and effective context/tool receipts. Denied access is enforced by the adapter.
- Run the [visualization acceptance checks](../VISUALIZATION.md) on a labeled fixture before native calls. No renderer exists yet.

## Resource and launch gates

Proposed limits: $5 model API, $2 infrastructure, two hours, one worker and at most two concurrent requests. These are requested planning ceilings, not an authorization. Current spend authorization for Poietic Agents is zero. Local offline document/contract checks require no model, host or credentials.

Required before launch: resolved and qualified implementation; independent design/measurement review; exact request and budget manifest; authorized credential aliases; public immutable plan/TLDR registration with successful preflight; fresh exclusive allocation from Dmarz's authorized fleet; deployment/source receipt; and an effective stop/reconcile path. Formal confirmation additionally needs the prior-art and hypothesis gates. The exploratory worker allowance does not imply S2 acceptance.

No server is claimed merely to wait for design review. Any future provisioning must verify the approved account/team and infrastructure state privately. Existing hosts and budgets from other studies confer no permission here.

## Handoff after a future attempt

Reconcile assignments, starts, terminal outcomes, scoring and spend; write `S0-01-post.md` even for a setup failure. Classify instrument defects, competence failures and valid outcomes separately. Preserve failures, make bounded repairs within the same authority, and test repaired behavior on a fresh namespace. Advance only the contracts that meet their declared checks; record an explicit design amendment if the executor ladder changes.
