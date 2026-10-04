# S0-02 post-mortem

2026-10-04 UTC. Assessor: vishesh/codex-heterogeneous. **Executed, qualification failed, scientific review complete. No swarm efficacy result.** Native source: `f3621c649311f4e7a6c110c1b56f97b818927f9e`;81 checks passed on the actual runtime before launch. [Original immutable plan](https://github.com/dmarzzz/swarm-lab/blob/f3621c649311f4e7a6c110c1b56f97b818927f9e/researchers/vishesh/notes/poietic-agents/README.md).

## What happened

One generalist decision started out of144 assignments. The pinned OpenRouter chat route returned HTTP 200 from `anthropic/claude-haiku-4.5`, provider Anthropic,565 input/41 output tokens. The first interface-failure guard stopped collection after strict JSON parsing failed.143 assignments remained unstarted; all144 have terminal records. None of the three roles qualifies. Qwen and Jev received no call. This does not establish a provider outage, weak reasoning, task accuracy or swarm efficiency.

## Inspecting the actual divergence

The private full request, response and provider receipt cover the only started miss; [the manifest](../results/S0-02/manifest.json) records their hashes without publishing payloads. The effective request asked for the endpoint/entity required by its fixture task. Its action-field map described required fields but did not explicitly specify a top-level discriminator.

The visible answer used Markdown fences around a nested action object. In schematic form the returned shape was `{"fetch": {...}}`, while the engine requires `{"type": "fetch", ...}`. These are format illustrations, not a reproduction of the actual task payload.

First divergence: Markdown fences cause `json.loads` to fail. Second, removing only fences still leaves a nested shape with no `type`, rejected by the engine. The response selected the requested endpoint/entity, but no native action was executed or credited. The prompt's underspecified shape is an actionable instrument weakness; its causal contribution to model behavior has not been isolated. The provider's accepted `response_format=json_object` request did not yield bare JSON in this observation; no universal provider claim follows.

Saved-data replay reproduces the parser failure, checks route and usage, joins physical IDs and recomputes every qualification count. [Trace review](../results/S0-02/trace-review.json) distinguishes verified failures from the proposed explanation. No hidden reasoning is inspected or inferred.

## Accounting and process

The owner-approved one-shot direct scope and bounded replacement window were activated only after exclusive allocation, fresh resource matching, public registration and runtime checks. The duplicate dispatch request was fenced. No credentials entered the worker. All12final hub artifacts were downloaded and matched their SHA256 hashes; all3hub runs are failed. The final PNG was visually checked. Worker process group, local relay/tunnel and allocation were stopped/released before offline repairs.

The new actual API charge isUSD 0.00077. The native worker summary conservatively recordedUSD 0.492544 cumulative API exposure because invalid-action parsing preceded its billing settlement. The authoritative relay retained known usage; the mirror was reconciled from that receipt, leaving36 historical uncertain calls untouched. Correct cumulative API exposure isUSD 0.480002. The full250 second allocation costsUSD 0.004960417 at the verified rate; cumulative infrastructure isUSD 0.082184183. **Total conservative cumulative exposure:USD 0.562186183 ofUSD 2.** This is retained accounting, not a provider/infrastructure invoice. [Cost closeout](../results/S0-02/cost-closeout.json) is a separate correction; original worker summary and published artifacts remain byte-identical.

## Quality and next decision

The [eleven-dimension scientific review](S0-02-scientific.json) is complete. Interface capability fails; scenario communication and worker cost measurement need repair; native controls remain unobserved. Complete trace retention, stopping, denominator accounting, source replay and artifact delivery worked. The offline operational finalize hook produced its own immutable handoff; that automatic record alone did not certify this scientific assessment.

The [prospective repair/diagnostic plan](S0-02-repair-plan.md) was written before the new implementation. Main now explicitly describes bare JSON, top-level `type` and sibling fields; strict rejection remains. Worker billing settles validated usage before action parsing.106 offline checks pass, including the observed fenced/nested pattern, known/unknown billing paths and 21diagnostic/renewal checks. These changes are not deployed and have no native qualification result.

Recommend a separately approved36 decision diagnostic on3 fresh roots paired across3 roles, covering all4lifecycle steps and all3structural variants. This smaller screen is not full qualification, a causal prompt comparison or a swarm experiment. Its dedicated manifest/runner is implemented and fault-tested offline; current admission is still required. No S0-03, D0-01 or S1 is launched. The original one-shot S0-02 authorization is consumed; changed successor scope requires the owner's updated decision.
