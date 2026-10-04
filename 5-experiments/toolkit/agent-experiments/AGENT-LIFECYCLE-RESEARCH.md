# Agent lifecycle, context and memory: research supplement

Reviewed **2026-10-04 UTC**. This focused reading map supports the [agent lifecycle standard and runbook](AGENT-LIFECYCLE.md). The [machine-readable source register](research/agent-lifecycle-sources.json) records source type, access depth, date, implications and limitations for every entry.

This is a focused review, not a systematic literature review or a replication. It adds **29 entries: 14 papers, 11 engineering articles or essays, two directly read social posts and two inaccessible social leads**. Papers were screened at abstract and bibliographic-record depth; detailed effect sizes and methodological robustness were not independently established. Several papers already appear in the broader bibliography; these are lifecycle annotations, not claims of 29 wholly new discoveries. Social posts and vendor accounts have a different evidentiary role from controlled studies. Repeated coverage of one project is counted as one underlying body of evidence.

## What we mean by an agent

For this lab, an agent instance is a versioned decision policy operating through a controller, with a defined identity, tools and permissions, and mutable context and memory inside a world. A policy may be scripted or model-based. The model is one component; the renderer, scheduler, retrieval rules, tool responses and persistent state can all change behavior. This is our operational definition, informed by the sources below, rather than a claim of universal terminology.

At a decision step, the controller assembles the instance's input from its fixed instructions, role, observation, retrieved state and delivered messages. The policy proposes an action; the environment validates and applies it; observations and permitted memory updates then affect the next step. The evaluator holds separate truth. Instances of the same definition may receive different private observations. Different roles require a predeclared role-specific definition or an explicit versioned role parameter captured in the receipt. Those differences must be allocated deliberately and preserved in the record.

## The claims we can defend

| Question | Defensible target | Evidence and implication |
| --- | --- | --- |
| Is this the same agent? | Same frozen definition and declared starting state, with a receipt showing what actually loaded | Interfaces and context affect behavior (P09, B01, B02); a name or persona is insufficient (P14). |
| Is startup deterministic? | Identical public input bytes and initialized state under the same specification, before model dispatch | Stable serialization and explicit context assembly help (B06). A generative initializer must be frozen or treated as a source of variation. |
| Will it answer identically? | State the numerical and service boundary; measure output variability when it is not guaranteed | Temperature zero does not control all numerical effects (B08). Determinism can be engineered under specified conditions; hosted metadata may be insufficient. |
| Does it have memory? | Identify stores, contents, readers/writers, retrieval, derived summaries and reset rules | Memory architecture and updates matter (P03–P05, P12). A stateless API can participate in a stateful controller. |
| Are agents independent? | Define which randomness, evidence, histories and resources are shared | Separate sessions do not remove shared-model or shared-source errors (B05, P14). Measure correlation rather than assuming diversity. |
| Is a rerun a replication? | A fresh experimental unit under a frozen protocol; retries and forks retain lineage | Reliability across trials differs from best-of-k selection (P02). Online learning across episodes may make the persistent cohort the unit (P12); a frozen learned checkpoint can still be evaluated on fresh independent episodes. |
| Is a result trustworthy? | Correct endpoint, verified state, preserved denominator and uncertainty over the right unit | Functional evaluation and harness isolation matter (P01, P02, P08, B03, B04). A trace hash proves integrity, not scientific truth. |

These are design inferences from the reviewed sources. None establishes that the proposed local runbook is sufficient without implementation and fault testing.

## How this changes our next experiments

Keep one protocol and the three existing agent/context/run specifications. Add a small initialization receipt that records actual loaded hashes, model metadata, role assignment, delivered initial context, memory namespace/reset, permissions and scheduler. Use a single launch path. This does not require a new orchestration platform.

Before adding experimental implementation, write its plan. Before any run, publish and verify the immutable public plan URL, register a condition-specific TLDR, and pass the mandatory launch preflight. The following are proposed questions, not approved or executed studies:

1. **Initialization fidelity.** Can two local constructions produce identical public initial-state and context hashes? Test this without model dispatch first. For registered model repetitions, report action agreement and task outcomes rather than promising exact text equality.
2. **Context-position sensitivity.** Hold evidence content and budget fixed; counterbalance order across scenario blocks. Treat retrieval misses and truncation as observable mediators, not silently missing records.
3. **Memory repair.** Start from one frozen memory snapshot. Compare append-only correction with explicit supersession under equal retrieval budget; measure stale-fact recurrence, legitimate retained facts and cost on held-out queries. Freeze the scorer before inspecting outcomes.
4. **Reset leakage.** Place an authorized synthetic marker in one episode; verify fresh namespaces cannot read it. Test permissions through the actual adapter. This is a local harness invariant unless a model interaction is introduced, in which case register that run.
5. **Within-swarm heterogeneity.** Randomize role-to-position assignment, record private evidence, and compare error correlation before and after communication. Separate evidence diversity, policy diversity and model-family diversity instead of bundling all three.
6. **Continuation and recovery.** Compare a fresh repetition with a resumed checkpoint only under a protocol that defines inherited history, pending effects and budgets. Score recovery against the common parent; do not count forks as independent worlds.

Choose one question and its necessary controls first. Pilot variance and cost determine confirmatory size; an arbitrary large episode count does not produce a strong design. Read full methods and relevant ablations of the nearest papers before committing to a novel empirical claim.

## Annotated sources

### Papers

#### P01 · AI Agents That Matter

[Kapoor et al.](https://arxiv.org/abs/2407.01502) · 2024-07-01

**Read:** Abstract and bibliographic record; no full-methods replication. **Source says:** Agent evaluation can be distorted by accuracy-only comparisons, cost differences, benchmark overfitting and weak standardization. **Our design inference:** Freeze the complete harness; report quality against aggregate cost and protect held-out scenarios. **Limit:** A methodological argument does not establish the sample size or success threshold for this project.

#### P02 · τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains

[Yao et al.](https://arxiv.org/abs/2406.12045) · 2024-06-17

**Read:** Abstract and bibliographic record; no full-methods replication. **Source says:** Evaluates stateful tool interactions against desired final database states and studies reliability over repeated trials. **Our design inference:** Score the resulting world independently; report repeated-execution consistency as well as mean success. **Limit:** pass^k consistency and pass@k best-of-k answer different questions; neither repairs dependence between runs.

#### P03 · Generative Agents: Interactive Simulacra of Human Behavior

[Park et al.](https://arxiv.org/abs/2304.03442) · 2023-04-07

**Read:** Abstract and bibliographic record; no full-methods replication. **Source says:** The architecture combines stored observations, reflection, retrieval and planning to support simulated behavior. **Our design inference:** Specify each memory stage and preserve the provenance of derived reflections. **Limit:** Believability in a particular social simulation is not proof of task correctness, human equivalence or general causal validity.

#### P04 · MemGPT: Towards LLMs as Operating Systems

[Packer et al.](https://arxiv.org/abs/2310.08560) · 2023-10-12

**Read:** Abstract and bibliographic record; no full-methods replication. **Source says:** Uses memory tiers and explicit control flow to manage information beyond an active context window. **Our design inference:** Define what is in active context versus external stores, and log transfers that affect decisions. **Limit:** A memory architecture does not by itself make model responses deterministic or memory retrieval correct.

#### P05 · LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory

[Wu et al.](https://arxiv.org/abs/2410.10813) · 2024-10-14

**Read:** Abstract and bibliographic record; no full-methods replication. **Source says:** Separates memory abilities including extraction, multi-session reasoning, temporal reasoning, knowledge updates and abstention. **Our design inference:** Test updates, stale-fact recurrence and correct abstention separately from retrieval hit rate. **Limit:** Its conversational tasks do not directly validate a swarm memory protocol. Headline failure rates are not transferred here.

#### P06 · Lost in the Middle: How Language Models Use Long Contexts

[Liu et al.](https://arxiv.org/abs/2307.03172) · 2023-07-06

**Read:** Abstract and bibliographic record; no full-methods replication. **Source says:** Studies changes in performance as relevant information moves within a long input. **Our design inference:** Freeze or counterbalance evidence position; record actual delivered order and truncation. **Limit:** The effect sizes are model/task dependent; this is not a universal law about every current model.

#### P07 · AgentBench: Evaluating LLMs as Agents

[Liu et al.](https://arxiv.org/abs/2308.03688) · 2023-08-07

**Read:** Abstract and bibliographic record; no full-methods replication. **Source says:** Evaluates agents across multiple interactive environments and discusses reasoning, decision and instruction-following failures. **Our design inference:** Qualify the chosen model on the exact action contract and task before starting a swarm comparison. **Limit:** Broad benchmark coverage is not evidence that a particular local runner or role is qualified.

#### P08 · WebArena: A Realistic Web Environment for Building Autonomous Agents

[Zhou et al.](https://arxiv.org/abs/2307.13854) · 2023-07-26

**Read:** Abstract and bibliographic record; no full-methods replication. **Source says:** Provides a self-hostable web environment with functional task evaluation. **Our design inference:** Freeze the world snapshot and evaluate state changes, rather than relying solely on plausible transcripts. **Limit:** A reproducible environment does not guarantee identical language-model outputs.

#### P09 · SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering

[Yang et al.](https://arxiv.org/abs/2405.15793) · 2024-05-24

**Read:** Abstract and bibliographic record; no full-methods replication. **Source says:** Studies how an agent-computer interface affects software-engineering agent performance. **Our design inference:** Treat tool schemas, command affordances and returned error formatting as part of the agent definition. **Limit:** Software-repair results do not establish the best interface for routing or social simulation.

#### P10 · PettingZoo: Gym for Multi-Agent Reinforcement Learning

[Terry et al.](https://arxiv.org/abs/2009.14471) · 2020-09-30

**Read:** Abstract and bibliographic record; no full-methods replication. **Source says:** Introduces the Agent Environment Cycle model and a multi-agent environment API to make interaction order explicit. **Our design inference:** Specify turn order, barriers, delivery and state transitions in the protocol. **Limit:** Borrow the semantics; this lab does not need to adopt a reinforcement-learning framework to obtain them.

#### P11 · Why Do Multi-Agent LLM Systems Fail?

[Cemri et al.](https://arxiv.org/abs/2503.13657) · 2025-03-17

**Read:** Abstract and bibliographic record; no full-methods replication. **Source says:** Analyzes multi-agent traces and organizes failures into a taxonomy spanning design, inter-agent alignment and verification. **Our design inference:** Code failures with a small, defined taxonomy and link classifications to observable events. **Limit:** A post-hoc category is not a demonstrated causal mechanism. The study does not validate this repository.

#### P12 · Reflexion: Language Agents with Verbal Reinforcement Learning

[Shinn et al.](https://arxiv.org/abs/2303.11366v4) · 2023-03-20

**Read:** Abstract and bibliographic record; no full-methods replication. **Source says:** Carries reflective textual feedback in episodic memory to affect later trials without updating model weights. **Our design inference:** Classify retained reflection as learned state; evaluate persistent cohorts separately from fresh-agent episodes. **Limit:** Unchanged weights do not imply unchanged agents. Reported benchmark gains are specific to its tasks and feedback setup.

#### P13 · ReAct: Synergizing Reasoning and Acting in Language Models

[Yao et al.](https://arxiv.org/abs/2210.03629v3) · 2022-10-06

**Read:** Abstract and bibliographic record; no full-methods replication. **Source says:** Interleaves model-guided decisions with environment actions and observations. **Our design inference:** Define the policy-observation-action loop explicitly; archive authorized actions, observations and concise decisions. **Limit:** The design does not require extracting private reasoning traces from a hosted model; the full system includes its tools and environment.

#### P14 · Persona Inconstancy in Multi-Agent LLM Collaboration: Conformity, Confabulation, and Impersonation

[Baltaji et al.](https://arxiv.org/abs/2405.03862v3) · 2024-05-06

**Read:** Abstract and bibliographic record; no full-methods replication. **Source says:** Finds persona and opinion instability in the studied collaboration/debate settings. **Our design inference:** Measure role fidelity and pre-discussion error correlation; distinguish assigned persona from persistent identity. **Limit:** Specific cultural-persona tasks do not justify universal claims that all role prompting fails.

### Engineering accounts

#### B01 · Effective context engineering for AI agents

[Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) · 2025-09-29

**Read:** Substantive article text. **Source says:** Discusses curating instructions, tools, history and retrieved information, with compaction and structured notes for longer work. **Our design inference:** Version the context renderer, selection and compaction policies; measure the actual context received by each instance. **Limit:** Practitioner guidance, not a controlled comparison establishing one optimal policy.

#### B02 · Effective harnesses for long-running agents

[Justin Young / Anthropic](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) · 2025-11-26

**Read:** Substantive article text, including initializer/session distinction. **Source says:** Describes initial setup followed by incremental sessions that rely on durable artifacts. **Our design inference:** Distinguish initializer and continuation roles. Freeze any generated setup before cloning paired conditions. **Limit:** A productive coding workflow is not a research replication contract. Live generative initialization can introduce uncontrolled variation.

#### B03 · Demystifying evals for AI agents

[Anthropic](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) · 2026-01-09

**Read:** Substantive sections on trials, harnesses, outcomes, grading and isolation. **Source says:** Separates tasks, repeated trials and evaluation harnesses; discusses outcome evaluation and contamination through residual state. **Our design inference:** Require fresh namespaces, preserve failed trials and compare final state with independent truth. **Limit:** An engineering guide is not a power analysis. Small suggested starting suites are for development, not automatic confirmatory adequacy.

#### B04 · Quantifying infrastructure noise in agentic coding evals

[Gian Segato / Anthropic](https://www.anthropic.com/engineering/infrastructure-noise) · 2026-02-05

**Read:** Substantive article text. **Source says:** Examines how execution-resource settings can affect measured coding-agent performance. **Our design inference:** Record concurrency, timeout and resource limits; block treatment order and distinguish infrastructure failures from model behavior. **Limit:** The observed magnitude in coding evaluations is not a universal acceptable-noise threshold.

#### B05 · How we built our multi-agent research system

[Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system) · 2025-06-13

**Read:** Substantive article text through architecture, delegation and lessons. **Source says:** Describes an orchestrator with specialist contexts, explicit delegation and substantial coordination costs. **Our design inference:** Record each specialist task, received context and output contract, and charge coordination to total cost. **Limit:** Vendor production experience; comparisons bundle architecture, models and resources. Separate contexts do not imply independent errors.

#### B06 · Context Engineering for AI Agents: Lessons from Building Manus

[Yichao Ji / Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) · 2025-07-18

**Read:** Substantive article text. **Source says:** Discusses stable prompt prefixes, append-only history, filesystem context, error retention and managed variation. **Our design inference:** Specify cache semantics and serialization. Treat intentional variation as a declared intervention, not invisible launcher behavior. **Limit:** Production optimization advice may conflict with experimental control. KV caching and response memoization have different implications.

#### B07 · Context Engineering for Agents

[LangChain](https://www.langchain.com/blog/context-engineering-for-agents) · 2025-07-02

**Read:** Introductory framework and write/select sections; classification overview. **Source says:** Organizes context management into writing, selecting, compressing and isolating information. **Our design inference:** Use those four verbs as a completeness check for the memory/context specification. **Limit:** Framework-oriented synthesis, not independent experimental support for each suggested technique.

#### B08 · Defeating Nondeterminism in LLM Inference

[Horace He / Thinking Machines Lab](https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/) · 2025-09-10

**Read:** Technical explanation including batch invariance and numerical operations. **Source says:** Explains how batch-dependent numerical computation can change inference output and develops batch-invariant implementations. **Our design inference:** Do not equate temperature zero or one seed with byte-identical output. Pin controllable runtime details and measure repeated behavior. **Limit:** Determinism is achievable under defined implementation conditions; this is not proof that every hosted endpoint is nondeterministic or that custom kernels are necessary here.

#### B09 · Building effective agents

[Anthropic](https://www.anthropic.com/engineering/building-effective-agents) · 2024-12-19

**Read:** Architecture introduction and workflow/agent distinction. **Source says:** Distinguishes predefined workflows from systems in which the model dynamically controls its process, and advocates simple components. **Our design inference:** Name the actual system honestly: scripted environment, model decision policy, or adaptive agent. Start with one auditable launcher. **Limit:** Historical architecture guidance; current tooling may differ. Model-based decisions inside a fixed loop can still be useful scientific objects.

#### B11 · Scaling Managed Agents: Decoupling the brain from the hands

[Anthropic](https://www.anthropic.com/engineering/managed-agents) · 2026-04-08

**Read:** Opening architecture section; later implementation sections not reviewed. **Source says:** Separates session history, the model/tool loop and execution sandbox, and notes that model changes can invalidate harness assumptions. **Our design inference:** Keep conceptual boundaries between durable history, controller and environment, and requalify when any changes. **Limit:** This is vendor architecture. Stable interfaces do not guarantee a stable hidden implementation; no hosted-service adoption is recommended.

### Practitioner essay

#### B10 · Context engineering

[Simon Willison](https://simonwillison.net/2025/Jun/27/context-engineering/) · 2025-06-27

**Read:** Full short post. **Source says:** Discusses terminology for the broader problem of assembling the information supplied to a model and quotes public discourse. **Our design inference:** Use context as a first-class experimental variable in documentation rather than using prompt as a catch-all. **Limit:** Opinion and secondary quotation, not experimental evidence. The linked X posts below were not directly accessible in this audit.

### Directly read social posts

#### S01 · Post linking context-engineering discussion

[Simon Willison](https://bsky.app/profile/simonwillison.net/post/3lsriizps222v) · 2025-06-29

**Read:** Primary post text and timestamp. **Source says:** Shares a discussion of context engineering as a distinct practical challenge. **Our design inference:** Retain as a dated pointer to practitioner vocabulary and further reading. **Limit:** Social signal only; not an experiment, an independent replication or evidence of broad consensus.

#### S02 · Announcement: effective harnesses for long-running agents

[Anthropic](https://www.linkedin.com/posts/anthropicresearch_effective-harnesses-for-long-running-agents-activity-7399550329031180288-xR_w) · absolute publication date not verified

**Read:** Primary post text; page exposed relative age only. **Source says:** Highlights incremental work and durable artifacts across context windows. **Our design inference:** Connect the social announcement to B02 rather than counting it as separate corroboration. **Limit:** Absolute post date not independently verified. Same underlying engineering work as B02; comments are not used as evidence.

### Unverified primary social leads

#### S03 · Context-engineering post

[Andrej Karpathy](https://x.com/karpathy/status/1937902205765607626) · absolute publication date not verified

**Read:** Direct fetch returned 403; linked/quoted in B10. **Source says:** No independent primary-text claim made in this review. **Our design inference:** Retain as a discovery lead; verify the original before quoting or dating it. **Limit:** Secondary quotation is available in B10 but is not direct verification.

#### S04 · Context-engineering terminology post

[Tobi Lütke](https://x.com/tobi/status/1935533422589399127) · absolute publication date not verified

**Read:** Direct fetch returned 403; linked/quoted in B10. **Source says:** No independent primary-text claim made in this review. **Our design inference:** Retain as a discovery lead; verify the original before quoting or dating it. **Limit:** Do not count an inaccessible social post as an independent source of empirical evidence.

## Search and evidence discipline

Searches combined agent initialization/reproducibility, context engineering, memory, agent harnesses, inference determinism and multi-agent failure analysis. We followed primary paper records, original engineering articles and author/company social posts. The search was purposive and English-language; it favors accessible sources and includes substantial vendor engineering commentary. We did not conduct a complete negative-result search, independently assess every cited method, or reproduce performance claims.

The date field for a paper generally denotes its first arXiv submission; a versioned link may refer to a later revision. Access depth refers to this supplement, even when another repository document previously consulted more of a source. The inaccessible X entries remain leads. No external page content or post has been copied wholesale into the repository.

Before a confirmatory study, upgrade the nearest-method papers from abstract screening to full-methods review, record the exact version, and extract the intervention, comparator, unit, sample, endpoint and known limitations. Keep a claim-to-source link. Engineering posts are useful for mechanisms and operational hazards; they do not establish independent replication or universal gains.
