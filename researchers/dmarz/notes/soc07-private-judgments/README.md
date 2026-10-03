# SOC-07: keep the first judgment private, but allow revision

**Working experiment plan for human review · 3 October 2026 · dmarz/soc07-plan.**

Start with five agents solving small fictional decisions with objectively correct answers. Have every agent form an independent first judgment, then compare **keeping those judgments private** with **publishing them before discussion**. Give both groups the same facts, answer opportunities and resource ceilings. The useful result is better final decisions while retaining the ability to accept valid corrections.

This is a draft for [SOC-07 on the question dashboard](https://swarm-research.pages.dev/#/questions?topic=llm-agent-swarms&id=SOC-07), not an accepted hypothesis, preregistration or executed experiment. The small development study below is the recommended starting scope. The larger confirmation is a costed planning example whose sample size must be checked after the pilot. Nothing in this package calls a model, reserves a server or deploys a website.

| Start here | What it contains |
| --- | --- |
| This plan | Question, treatments, exact schedule, tasks, runs, architecture, analysis and implementation order |
| [design.json](design.json) | Proposed parameters and stage counts; execution disabled; unresolved launch fields are explicit |
| [check_plan.py](check_plan.py) | Offline arithmetic and consistency checks; no provider, network or hub integration |

## 1. What we want to learn

**Working prediction:** delaying publication of agents' first choices improves the team's final accuracy because early recommendations exert less pressure on later reasoning. A useful protocol should preserve a correct minority's evidence **and** let an incorrect minority change its answer. An instruction never to revise may reduce changes while worsening decisions.

The primary question is a protocol comparison: **PRIVATE versus PUBLIC**, on one fixed model, one task generator and an equally weighted mixture of the three evidence regimes below. It is not a claim about human psychology or access to a model's hidden beliefs.

Separate three possible findings:

- **Useful independence:** fewer correct-to-wrong changes, retained wrong-to-correct changes, and higher final accuracy.
- **Anchoring:** fewer changes in both directions; initially wrong judgments persist.
- **No useful effect:** private recording adds little, public discussion helps just as much, or independent voting is preferable.

### What the existing research changes

Private first answers are not themselves new. Choi et al.'s debate baseline already starts with independent answers; their results also caution that following a majority can help. SEPAL keeps actor–critic pairs separate until final fusion, changing several mechanisms together. Barrera-Lemarchand et al. already use private initial judgments, public deliberation and private final re-answering with permission to revise. The potential contribution here is the controlled disclosure comparison and its correction tradeoff at matched resource ceilings. [[choi-2025-debate]] [[ren-2026-sepal]] [[barrera-lemarchand-2026-wisdom]]

Shehata's trace-based measure is not a separately elicited private choice. We will measure explicit recorded answers and their changes, not interpret an emitted reasoning trace as inner belief. [[shehata-2026-bystander]]

I used Vishesh's [general experiment guide](../../../../tooling/agent-experiments/GUIDE.md), [harness guide](../../../../tooling/agent-experiments/HARNESS.md), [protocol template](../../../../tooling/agent-experiments/templates/protocol.md), the experimental-design sections of his [SEO-poisoning design](../../../vishesh/notes/seo-poisoning/experimental-design.md), and his [SOC-07 review](../../../vishesh/notes/atlas-review/candidate-review.md). His review specifically asks for equal answer opportunities, a no-extra-computation control, and separate harmful/useful revision rates. [VX-35](../../../vishesh/notes/atlas-review/extension-bank.md#vx-35) motivates fixing evidence access: changing search behavior is a separate future experiment.

The plan adopts his paired worlds, protected truth, staged development, full cost accounting and failure denominators. It does **not** adopt the SEO scenario, reward schemes, or treat published recognition percentages and architecture rankings as universal validation thresholds. The source check for this plan covered the relevant primary methods, not independent reproduction of their results.

## 2. Five live-team protocols, with one primary comparison

An **agent** is one isolated model conversation. A **team episode** is five agents completing one task under one protocol. A **world** is one independently generated decision problem; repetitions of it are not new worlds.

| ID | First pass | What peers see before discussion | Revision | Purpose |
| --- | --- | --- | --- | --- |
| **PRIVATE** | Choice, confidence, evidence IDs and brief justification, stored privately | The shared factual packet; no peers' first choices | Explicitly allowed | Candidate protocol |
| **PUBLIC** | Exactly the same initial artifact as PRIVATE | The same facts plus peers' first choices and confidence | Explicitly allowed | Primary control: early disclosure |
| **NEVER** | Same initial artifact as PRIVATE | Same factual packet as PRIVATE | Told to keep the initial choice | Diagnose stubbornness; measure compliance |
| **PREPARE** | Evidence inventory and uncertainties, without choosing or ranking options | Same factual packet as PRIVATE | First choice may occur during discussion | Controls for a preparatory call; a different preparation task |
| **VOTE** | Same initial artifact as PRIVATE | No peer facts or messages | Allowed during solitary review | Independent ensemble with the same call/output allowances |

NEVER retains the same final action space; the harness must not force its answers. PREPARE must not receive an extra hidden initial-answer probe. Its initial-to-final revision rates are **undefined**.

PRIVATE/PUBLIC have identical first-answer opportunities. PREPARE matches call and token allowances, but fact listing is not semantically identical to choosing. VOTE changes access to information as well as interaction; it answers whether communication buys anything in this distributed-information task, not whether a single solver with all facts would do better.

Generate each agent's initial artifact once, before applying PRIVATE/PUBLIC/NEVER/VOTE overlays; clone it into isolated continuations. This gives those arms identical observed starting judgments, including initial mistakes. PREPARE generates its separate inventory. Do not show the future visibility rule during this shared initial call. Thus this first study tests **when an already-generated judgment is disclosed**, not the effect of anticipating public accountability while forming it. A fresh run with advance notice is an optional later study.

## 3. The exact episode schedule

Use one discussion round for the first slice. This is a deliberately shallow team protocol; it cannot establish behavior after prolonged debate.

| Step | Action | Visibility and allowance |
| --- | --- | --- |
| 0. Initialize | Generate task, evidence allocation, labels and display order; clear all conversation state | Truth and expected answer stay with evaluator |
| 1. Prepare | All five agents independently emit their first-pass record; wait for the whole team | One call per agent, at most 256 output tokens; no agent sees a peer yet |
| 2. Release evidence | Controller publishes the union of permitted factual records, in the same order across communicating arms | Deterministic delivery, no model call; PUBLIC additionally releases peers' initial choices/confidence |
| 3. Discuss | Each agent reads its own record and the frozen board, then emits a short evidence-citing message and optional current recommendation | One call per agent, 256 tokens; publish all five messages only after all calls finish |
| 4. Freeze | Save each agent's context with that completed discussion board | No further exchanges; no last-speaker advantage |
| 5a. Public final | Ask for the answer to be included in the team's final vote | One isolated continuation, 64 tokens |
| 5b. Private final | Independently ask for a confidential evaluator-only answer | A second continuation from the **same Step 4 snapshot**, 64 tokens; never sees 5a |
| 6. Score | Deterministic majority of public finals; score individual outputs and transitions | No model judge or model-based final synthesizer |

For VOTE, Steps 2–3 supply only the agent's original facts and a solitary review prompt. Its review output stays private. The two final elicitation branches still use the same caps. Peers never receive its initial, review or final answers before all decisions are complete.

PRIVATE, PUBLIC and VOTE receive: “Your first answer is provisional. Retain it or revise it according to the available evidence.” NEVER instead receives: “Keep the choice recorded in your first answer, even if later information suggests another choice.” This intentionally strong diagnostic instruction appears only **after** the common first pass. PREPARE's initial instruction is: “List available evidence and uncertainties. Do not choose, rank, recommend, or imply a preferred option.” Its discussion instruction is: “Form a provisional choice from the available evidence; you may revise it before your final response.” Audit premature-choice leakage as an outcome; do not regenerate until the answer looks compliant.

The controller supplies the factual packet directly from the fixture. It must not strip facts from a model-written summary using another model. Only PUBLIC exposes initial `choice` and `confidence`; the controller never publishes the initial justification record in any arm. Agents may quote or paraphrase their own justification during discussion, and discussion messages may contain new recommendations in all communicating arms. “Private” therefore means **initial judgments withheld until discussion**, not semantic secrecy or permanently anonymous reasoning.

Initial record example: `{"choice":"A","confidence":0.7,"evidence_ids":["e03","e07"],"justification":"Brief evidence summary"}`. Final record: `{"choice":"B","confidence":0.8}`. `choice` permits A, B or ABSTAIN. Confidence is a reported number, not a calibrated probability unless separately shown to be calibrated. Missing/invalid fields remain invalid; no silent repair.

## 4. Tasks that can distinguish independence from stubbornness

Use a synthetic **two-option supplier decision**. This is fictional procurement with no real company names or external tools. Both options have an estimated cost and delivery time; a later timestamped audit may update either. The rule is explicit: choose the lowest-cost option among those meeting the delivery deadline, using the latest authorized record for each value. Generate integer values, exactly one correct choice, and no cost ties. Half the worlds have A as the correct displayed answer and half B, up to integer rounding within balanced blocks.

Proposed fixture parameters: costs 20–100 units; delivery 1–10 days; deadline 5 days; final feasible cost gap sampled evenly from 1–3, 4–10 and 11–20 units where both are feasible. Half the worlds instead distinguish the options through feasibility. Reject infeasible/ambiguous generator draws **before any model response**, using a fixed sampling rule recorded in the generator. These are design choices to validate in S0, not an existing benchmark.

| Regime | Private evidence allocation | What the shared packet reveals | What it diagnoses |
| --- | --- | --- | --- |
| **Clean** | Everyone has current records consistent with the correct choice | Redundant truthful evidence | Does private recording damage easy cooperation? |
| **Informed minority** | One of five agents has the decisive current audit; four see older records favoring the other choice | Everyone gets the current audit before discussion | Can a well-informed minority survive early, now-unsupported majority recommendations? |
| **Correctable minority** | Four agents have the current audit; one sees older records favoring the other choice | Everyone gets the current audit before discussion | Does the initially disadvantaged agent accept a valid correction? |

The initial private evidence is deliberately incomplete in some cases; the evaluator knows the complete current state. Facts needed to infer the answer may enter agent contexts, but the evaluator's answer key never does.

The informed role is defined by evidence allocation **before** observing answers. Do not select only episodes in which the minority answered correctly or the majority became wrong. Realized initial correctness and disagreement are reported manipulation checks. Equalize regime counts and rotate the special role across agents; balance label and display-order permutations across task blocks. Repeats change policy sampling and counterbalanced presentation, not the underlying truth. Store the correct canonical supplier identity per world and the separate per-repeat A/B mapping; always score through that mapping. Use independent keyed randomness streams, not one mutable random-number stream shared across treatments.

For a simple concrete fixture, old records say A costs 40 and arrives in 3 days, while B costs 50 and arrives in 4 days. A current authorized audit changes A's arrival to 8 days; the deadline is 5 days, so B is correct. In the informed-minority condition only one agent initially has that audit. After the release all communicating arms receive the audit. The question is whether early A recommendations still interfere with making the correct switch. Include the mirrored direction and cost-based cases so “always reverse the initial answer” cannot win.

## 5. Two studies, not one confused comparison

**Controlled replay (development diagnostic).** One focal model agent receives four scripted peer streams. Incoming message bytes and their order are identical across arms. In the pressure fixtures, three peers recommend the wrong option without supporting current evidence and one cites the correct audit; correction fixtures reverse that balance. Clean fixtures recommend the correct option. Facts and recommendations are separately marked in the board. The same scenario includes a correct-answer rationale available to the focal agent; no claim of organic peer behavior follows from scripted pressure.

Unlike the live table, replay PUBLIC changes only whether the **focal agent's own** initial record is posted and described as public. It does not add extra incoming peer votes: all arms receive the same scripted peer information. PRIVATE/PUBLIC in replay therefore tests disclosure/audience framing, because the scripts do not respond to what the focal agent publishes. It **cannot** estimate the reciprocal social effect of public initial votes. PRIVATE/PREPARE estimates the initial-answer preparation package under fixed exposure. This replay study helps debug and interpret mechanisms; it is not the primary live-team result.

**Live teams (primary study).** Five model agents produce the actual discussion. Pair the underlying world, initial artifacts, factual packet, labels and exogenous ordering across arms. Let downstream messages differ: that is part of the treatment effect. Apply one protocol to the whole team episode. No communication or shared writable state crosses episodes.

An independent full-information solver appears in engineering qualification to check that the problem is solvable. It is not a cost-matched scientific baseline at that small sample size. If the later question is “why use a swarm instead of one solver with all evidence?”, add that comparator to a separately powered study.

## 6. Runs and parameters

### Stage sequence and allocation

| Stage | Worlds and repeats | Arms | Model agents per episode | Episodes | Purpose |
| --- | --- | --- | --- | --- | --- |
| **S0** | 60 offline fixtures, 20/regime, plus fault injections | All five in scripted form | 0 | No LLM episodes | Verify generator, scorer, access boundaries and accounting |
| **S1-Q** | 12 new development worlds, 4/regime, 1 repeat | Full-information single solver | 1 | 12 | Check basic model competence and output format |
| **S1-R** | 24 new worlds, 8/regime, 2 repeats | PRIVATE, PUBLIC, NEVER, PREPARE | 1 focal + 4 scripted peers | 192 | Controlled replay diagnostic |
| **S1-L** | 24 different worlds, 8/regime, 2 repeats | All five | 5 | 240 | Estimate live effects, failures, discordance and cost |
| **S2-L** | **Illustration:** 960 unopened worlds, 320/regime, 1 repeat | PRIVATE, PUBLIC | 5 | 1,920 | Confirmation after sample-size simulation and full freeze |
| **S3** | Separately frozen fresh worlds; size chosen for its question | Selected contrasts | New population or setting | Not allocated yet | Replication, not a way to rescue S2 |

Run S1-Q first, then S1-R, then S1-L. Keep each stage's worlds separate. These are proposed runs; none has executed. S1 has **60 distinct task worlds** in total, not 444 independent observations. The two pilot repetitions measure instability within a task. S2 prioritizes fresh task worlds over additional seeds. Statistical generalization remains to this generator, not to all reasoning tasks.

### Model and controller defaults

| Parameter | Proposed first value | Reason / constraint |
| --- | --- | --- |
| Model | `Qwen/Qwen3-8B`, revision `b968826d9c46dd6066d109eabc6255188de91218` | Modest open-weight starting model; competence must be checked |
| Precision | BF16, no quantization | Freeze a different setting explicitly if hardware requires it |
| Thinking mode | `enable_thinking=false` | Explicit short outputs; no hidden-reasoning interpretation |
| Sampling | temperature 0.7; top-p 0.8; top-k 20; min-p 0; presence penalty 0 | Non-thinking defaults from the [official model card](https://huggingface.co/Qwen/Qwen3-8B) |
| Context | 8,192-token configured window; at most 4,096 input tokens/request | Reject overflow; never silently truncate a decisive fact |
| Output | 256 initial + 256 discussion + 64 public final + 64 private final | 640 tokens/agent, 3,200/team; S1-Q uses one 128-token final |
| Communication | Complete public board; one synchronous round | Same factual access, no search or learned routing |
| Team size | 5 throughout S1-L and S2-L | An informed minority of one is possible |
| Tools and memory | No tools; no persistent or cross-episode memory | Isolate initial-answer disclosure |
| Parallelism | At most 5 in-flight requests; interleave randomized arm order within blocks | Freeze serving/batching behavior; record actual scheduling |
| Timeouts | 60 seconds/request, 600 seconds/episode after dispatch | Proposed engineering limits; verify hardware fit during S1 |
| Retries | 0 automatic retries; 0 output-repair calls | A retry cannot quietly replace an unfavorable result |
| Aggregation | At least 3 of 5 valid public finals agree | Otherwise team failure; never drop abstainers from denominator |
| Seeds | Development 730071; holdout 730072; bootstrap 730073 | Named SHA-256-derived streams; see configuration |

The revision above was read from Hugging Face's model metadata on 3 October 2026; it is a proposed pin, not a claim the weights are installed. The runtime container, dependency lock, tokenizer and rendered chat-template hashes remain to be captured during implementation. No fallback model is allowed within a study. The deliberately short output caps are study constraints, not a claim to reproduce the model's maximum benchmark performance; raise them only through a development amendment if outputs truncate.

### Cost accounting

| Stage | Per-arm allocated calls | Actual unique calls after shared initial generation | Allocated output-token ceiling | Unique output-token ceiling |
| --- | --- | --- | --- | --- |
| S1-Q | 12 | 12 | 1,536 | 1,536 |
| S1-R | 768 | 672 | 122,880 | 98,304 |
| S1-L | 4,800 | 4,080 | 768,000 | 583,680 |
| S2-L illustration | 38,400 | 33,600 | 6,144,000 | 4,915,200 |

“Allocated” counts each arm as though deployed alone, including its first pass. “Unique” counts the actual shared first-pass requests only once. These are ceilings and request allocations, not measured tokens, money or compute equality. Count all input tokens too: at the worst-case 4,096/request cap, multiply unique calls by 4,096 for the input ceiling. The public arm reads more text, so report its actual consumption and latency. Do not add useless padding to manufacture equality.

No dollar or GPU-hour estimate is asserted before a serving benchmark. Before even S1-Q, the operator must set an enforceable qualification/development money or compute-hour ceiling alongside the request/token allocations above. S1 measures time, input/output usage and throughput to inform a separate S2 budget. The configuration cannot launch anything and deliberately has no approved spend. There are no judge, retrieval or synthesis calls hidden outside this accounting. Monitoring probes must be budgeted separately if later added.

For latency comparisons and the 600-second public-decision deadline, attribute shared first-pass duration to every arm plus that arm's own downstream time through public-final collection. Exclude its wait for another arm's turn; record that queue time separately. Schedule public finals first, then private finals from their saved independent contexts. Reserve primary and auxiliary phase budgets separately; private probes cannot consume resources reserved for the public decision. A private-final timeout cannot invalidate a public decision already delivered on time. Cap auxiliary private collection at a further 60 seconds with five simultaneous requests; report its cost and missingness separately. Reused artifacts are pre-treatment only. Never cache a discussion or final answer across arms.

## 7. Architecture to build

```mermaid
flowchart TD
  M[Frozen configuration and planned episode ledger] --> G[Task and evidence generator]
  G --> T[Protected truth and deterministic scorer]
  G --> C[Controller: phase barriers and budget reservations]
  C --> V[Private first-answer vault]
  C --> B[Immutable public board snapshots]
  V --> X[Per-agent context builder]
  B --> X
  X --> A[Model adapter: one pinned endpoint]
  A --> C
  C --> F[Isolated public and private final continuations]
  F --> T
  C --> L[Append-only scientific event ledger]
  T --> L
  L --> R[Paired analysis and completeness checks]
  L --> H[Sanitized progress outbox to shared run hub]
```

The model receives only text built by the context builder. It has no filesystem, vault, evaluator or hub handle. The initial vault is write-once: only the controller, owner-agent context and evaluator may read an agent's private record. Peer visibility is an explicit allowlist; do not publish guessable hashes of binary choices as commitment receipts. The evaluator is outside agent-accessible storage. If tools are later introduced, enforce that separation with process/filesystem permissions, not just a Python class boundary.

Start a real experiment from [the existing worker template](../../../../templates/experiment-worker/README.md) after its research gates pass. A distributed **worker is a job runner**, not one of the five scientific agents. One queued job should contain a paired task/repeat block, with arms executed in randomized order. Keep at most one manifest version in a worker process.

| Component | Reuse | SOC-07 work needed |
| --- | --- | --- |
| Study scaffold | Worker template, `design.yaml`, preregistration and coordinator conventions | Adapt its simulator contract to the four-phase model sequence |
| Hashing and replay | Toolkit `contracts.py`, planned ledger and event-validation patterns | Extend schemas with phase, visibility, attempts, token use and SOC-07 outputs |
| Task generator/scorer | General deterministic-fixture pattern | Implement latest-record decision task; independently cross-check unique answers |
| Vault/board/context | Architecture guidance | Implement and test actual per-agent access and synchronous release |
| Provider adapter | No working provider in the toolkit's toy harness | Implement requests, token/time reservations, strict parsing and usage reconciliation |
| Worker recovery | Queue scaffold | Durable checkpoints, deduplication and exact manifest verification |
| Analysis | Pairing conventions | Reconcile every planned episode, including failed/missing ones; do not use a done-only export |
| Run hub | Existing `swarm_report` contract from agentops | Durable sanitized outbox; keep scientific truth in the local immutable ledger |

The template's present S2 guard freezes only its design/preregistration files; it is not enough for this study. Freeze and verify code, prompts, scorer, generator, model, tokenizer, dependencies and splits too. Existing S1 prerequisites are not a complete validity gate. Do not assume a coordinator dry-run is offline; some paths contact the hub. S3 is a separately added stage, not currently supplied by the template.

Proposed future source layout: `experiments/<accepted-id>/src/{generate,contexts,protocol,adapter,score,analyze}.py`, `prompts/`, `schemas/`, `manifests/`, and `results/`. Large raw data belong in the repository's ignored `data/` or approved storage. These paths describe future implementation; those files do not exist in this plan.

Each event records manifest hash, stage, world ID, repeat, arm, agent, phase, snapshot hash, prompt hash, response/validity, seed, timestamps and usage. Task truth keys use stage/world, never repeat. Policy seeds also include arm/agent/phase; the shared initial seed excludes arm. Preserve full seed inputs and stable canonical serialization. Example scientific ID: `soc07-s1l-w0007-r01-a-private`; retries/resumption retain that identity with separate attempt lineage. A hub block can be `soc07/s1l/w0007-r01/m<manifest12>`. Only a real registered experiment ID is used for actual reporting.

Routine hub telemetry includes progress, aggregate cost, validity and sanitized failure categories. It excludes answer keys, individual commitments, private machine addresses and credentials. Hub delivery failure must not erase a completed scientific record. Reconcile planned IDs, terminal outcomes and reporting acknowledgements; the hub's display status is not the scientific denominator.

## 8. Outcomes and analysis

**Primary endpoint:** a correct public team decision by the deadline, divided by **all assigned live-team episodes**. PRIVATE minus PUBLIC is positive when private initial judgments help. The target mixture is one-third of each regime, even if realized numbers of usable answers differ.

| Measure | Numerator / denominator | Interpretation |
| --- | --- | --- |
| Team success | Correct majority decisions / all assigned team episodes | Primary operational accuracy |
| Harmful revision | Initially correct to valid wrong / initially correct records | Preservation; report invalid final losses separately |
| Useful revision | Initially valid wrong to final correct / initially valid wrong records | Correction; abstention is separately categorized |
| Transition burden | Each transition count / all assigned agent decisions | Shows counts without conditioning away failures |
| Private/public mismatch | Different valid choices / agents with both finals valid | Elicited disagreement, alongside coverage |
| Private-vote success | Majority of private finals correct / all assigned episodes | Secondary; never substitute for primary public decision |
| Individual success | Correct finals / all assigned agent decisions | Includes initial-status and regime breakdowns |
| Process/cost | Validity, abstention, stale-evidence citations, deadline failures, actual input/output tokens, wall time | Explains tradeoffs and instrumentation failures |

Compute revision rates only where an actual initial answer exists. Report public-final and private-final transitions separately, including starting-state counts and invalid/abstaining endings. PRIVATE/PUBLIC/NEVER/VOTE share a pre-treatment initial record, which makes their starting-state comparisons interpretable. A different initial composition in PREPARE must not be imputed away.

Freeze the planned ledger before execution. Every assigned episode receives exactly one terminal execution status (completed, interrupted, or incomplete), a separate decision outcome (correct, wrong, no majority, or unavailable), and zero or more per-agent failure flags (invalid response, refusal, timeout, exhaustion, infrastructure failure). A team may succeed despite a member failing. A and B are the only winning votes; ABSTAIN never counts toward the three-vote threshold. Defined noncompletion is zero for operational success. Missing substantive scores remain null, with best/worst-case bounds; do not pretend an ungraded answer was semantically wrong. Retain partially failed teams with the original three-vote threshold.

If an initial or discussion call fails, that participant makes no further calls in that arm and receives no final vote. Its permitted fixture facts still enter the shared factual packet: exogenous evidence delivery must not depend on model completion. Use the fixed `record unavailable` placeholder for a missing PUBLIC initial vote and `message unavailable` for a failed discussion turn; never expose malformed raw output to peers. An invalid common initial record terminates that participant in all four arms sharing it, including NEVER, which has no valid choice to preserve. PREPARE's separate preparation may succeed or fail independently. If only a public-final call fails, still collect its independent private branch; neither final branch conditions on the other's result. Preserve unused allocations and actual consumption separately.

The default has no automatic retries. Resume from an existing completed request only when its durable ID and output are known; an uncertain in-flight request becomes an auditable failure. A later rerun is an additional attempt or separately labeled robustness result, never a replacement that deletes the original outcome. An infrastructure outage triggers an operational pause and documented amendment, not a new easier task.

For team success, average paired arm differences within each world over repetitions, then average worlds within each regime and weight the three regimes equally. Use a stratified world-cluster bootstrap with 10,000 resamples, retaining arms, agents and repetitions together. Show regime-specific intervals and denominators. For S2's one repetition, also report paired binary discordance and an appropriate paired-score/exact sensitivity interval. Validate interval behavior by simulation before freezing it; bootstrap intervals can be unreliable with few pilot worlds. Agent votes and messages are never independent replicates.

Conditional revision rates use pooled transition counts divided by pooled eligible initial-answer counts **within each regime**, rather than an average of world-level ratios. Retain zero-eligible worlds in the assigned ledger and bootstrap; they contribute zero to both counts. The useful-correction noninferiority guard specifically targets the **designated initially disadvantaged agent in the correctable-minority regime**, conditional on that shared pre-treatment answer being valid and wrong, and uses its public final. Subtract the two arms' pooled rates, with the shared eligible denominator. A zero denominator, or bootstrap samples with inadequate eligibility to support the declared interval method, makes that guard unresolved. Report all-agent and private-final correction rates as separate diagnostics. This conditional population and the all-assigned team population must not be conflated.

Only PRIVATE/PUBLIC is the confirmatory primary contrast. Pilot comparisons and replay effects are descriptive. Prespecified secondary inferential claims use Holm correction within their declared family; exploratory results receive that label. Model identity is a fixed selected condition, not a random sample of all models. No claims about people, consciousness, real organizational decisions or long-lived autonomous swarms follow from this test.

### Sample size: why 960 is an illustration

For independent paired binary outcomes, an approximate planning formula is

`n ≈ (1.96 × sqrt(discordance) + 0.8416 × sqrt(discordance − delta²))² / delta²`.

At discordance 0.20 and a 5 percentage-point difference, this gives about 626 paired worlds. Separately, a one-sided 2.5% noninferiority test with true difference zero, discordance 0.10 and a 5-point margin needs roughly 314 worlds **per regime** for 80% marginal power under a normal approximation. Hence the convenient starting illustration of 320 worlds/regime, 960 total. These assumptions are not measured evidence and do not establish 80% power for the combined decision rule.

After S1, simulate the actual stratified paired binary outcomes, initial-answer eligibility, failures, token-cost variability and intended intervals over plausible discordance/variance ranges, including pilot uncertainty. Size for the joint superiority-and-correction decision, not just the overall contrast. Two independent 80%-powered guardrails jointly pass only about 64% of the time. Requiring an observed gain of at least 5 points also passes only about half the time when the true gain is exactly 5 points, regardless of a large sample. Evaluate the full rule at true gains of 5, 8 and 10 points; an 80% joint adoption target must specify a true gain above the 5-point practical threshold. Conditional useful-revision eligibility may require more worlds than either illustration. Freeze the maximum required size and its cost before opening S2. If that does not fit the agreed budget, report an exploratory or precision-limited result, or narrow the claim; do not declare the smaller sample powered. Do not top up S2 because an interim effect looks promising.

### Decision rules proposed for review

1. **Evidence for a useful disclosure protocol:** PRIVATE's overall estimated gain is at least 5 percentage points and its two-sided 95% interval excludes zero.
2. **Retained correction and clean performance:** one-sided 97.5% lower bounds for PRIVATE minus PUBLIC exceed −5 points for clean-team success, correctable-minority team success, and useful individual correction in the designated minority population defined above. Also show the informed-minority harmful-revision difference. If eligibility is too sparse or an interval is too wide, correction is unresolved.
3. **Efficiency:** the upper 95% world-bootstrap bound for the ratio of total input-plus-output tokens per deployed PRIVATE episode to PUBLIC is at most 1.10. Count the common first pass in both. Treat this as a tokenizer-specific resource check, alongside latency and compute, not universal FLOP equality.
4. **Stubbornness is a failed explanation of usefulness:** if NEVER merely lowers both types of revision, that does not support selective independence. If PRIVATE behaves the same way, narrow or drop the original claim.
5. **Inconclusive is allowed:** an interval spanning benefit and harm is not evidence of equivalence. A robust harm to correction, no worthwhile accuracy gain, or gains explained by cost/invalidity warrant redesign or rejection.

The 5-point effects/margins and 10% token allowance are proposed practical thresholds, not facts supplied by literature. A 5-point noninferiority margin tolerates up to five additional failures per hundred relevant tasks or decisions; it does not establish absence of harm. Confirm these tolerances in human review before registration. S2 tests PRIVATE versus PUBLIC only: it cannot establish superiority to independent voting, a full-information single solver or every other architecture. Such adoption claims need their own confirmatory comparator.

## 9. Build order and release gates

| Step | Concrete work | Done when |
| --- | --- | --- |
| 1. Offline fixture | Task generator, independent exact solver, role/label permutations | 60 fixtures solve uniquely; balanced allocation; oracle succeeds on all |
| 2. Visibility controller | Private vault, public board, stage barriers, final forks | Canary private fields and truth never reach forbidden contexts; PUBLIC reveals only allowed fields |
| 3. Failure/accounting harness | Planned ledger, strict parser, budget reservations, durable state | Injected timeout, malformed output, overflow, crash and duplicate dispatch remain counted exactly once |
| 4. Model qualification | Pinned adapter, complete rendered prompts, S1-Q | At least 10/12 full-information answers correct and at least 11/12 valid; otherwise fix engineering/difficulty before study |
| 5. Development studies | S1-R then S1-L with fixed allocations | Costs and denominators reconciled; no task selection on observed conformity |
| 6. Freeze confirmation | Reviewed question, full manifest, power simulation, analysis code, budget | All launch requirements resolved, S2 sample fixed, holdout still unopened |
| 7. Execute and analyze | S2 only under its manifest | All planned IDs accounted for; complete operational and sensitivity analyses |

During S0, include a scripted always-correct solver, an evidence-following updater, an unconditionally stubborn policy and a majority follower. They verify that the scorer distinguishes correction from corruption; they are not evidence that LLMs behave that way. Fork the same context twice as private/private on offline fixtures, and reserve a separately counted development probe if model sampling instability needs measurement. Do not interpret public/private differences without considering that ordinary resampling can also change answers.

During S1, inspect every rendered context for overflow and all malformed outputs. Require zero detected truth/private-field leaks; investigate rather than discard any affected run. Require at least 95% parse-valid outputs and less than 5% budget/timeout failures before treating effect estimates as useful. Report initial disagreement and initially-wrong opportunity counts by regime. If a regime offers almost no relevant opportunities, revise the generator only on development data and restart the pilot under a new version. No universal minimum conformity rate is imposed, and agents are never prompted to reproduce a hoped-for result.

Before actual collection, complete the repository research gates. At the source snapshot used here, `surveys/llm-agent-swarms.md` is complete but its dmarz review is still `revise`; there is no accepted SOC-07 hypothesis. This note therefore remains in researcher working material. [AGENTS.md](../../../../AGENTS.md) requires: “The hypothesis is `accepted` or later” for an experiment. The plan is fully drafted now; those status changes and cross-researcher review are launch requirements, not claims that this document has already passed them.

When execution is actually chosen, create the formal experiment, copy the worker scaffold, claim the intended compute resource through agentops, and register/report the run using its reporting guide. Release the compute claim after the run. Do not publish private infrastructure details in the public repository. No such claim or registration is made by this planning task.

A sensible S3 order is: reproduce on a second model family; then test advance disclosure of the visibility policy; then extend to two discussion rounds or a less transparent task family. Change one major dimension at a time and freeze each follow-up on new worlds. Defer heterogeneous teams, learned rewards, tool use, online search, memory and adversarial agents until the initial comparison is interpretable.

## 10. Check and review this package

From the repository root:

```sh
python3 researchers/dmarz/notes/soc07-private-judgments/check_plan.py
python3 scripts/lab.py check
python3 .flightdeck/fd.py check --strict .
```

The first command checks planning arithmetic only. It is not a simulator or an experiment runner. The machine-readable settings intentionally keep runtime and spending requirements unresolved. Formal preregistration must capture the exact prompts, full access manifest, source/data/model hashes, statistical simulation, schedule, stop rules, accountable operator and public timestamp before S2.

Primary-source methods consulted: [Shehata](https://arxiv.org/html/2605.10698), [Choi et al.](https://arxiv.org/html/2508.17536), [SEPAL](https://arxiv.org/html/2609.39645), and [Barrera-Lemarchand et al., Methods pp. 19–20](https://arxiv.org/pdf/2609.22497). The first three are catalogued on SOC-07; the fourth makes the novelty boundary substantially narrower. Their reported findings were not reproduced in this task.
