# Current differentiation design and historical mechanism sketches

**Owner-directed update:** HX-31 is the lead project; HX-33 supports it. HX-32 is deprioritized, HX-35 parked, and HX-37 consolidated into HX-31. See [PRIORITIES.md](PRIORITIES.md). Historical sections below are retained as context, not current recommendations.

These are exploratory design sketches, not registered hypotheses or runnable preregistrations. No experiment has started. Each must survive the formal prior-art gate and independent review. A future condition-specific public plan must pin exact models, sample size, seeds, resource limits, immutable URL and TLDR before qualification or experimental calls. The separate machine-allocation and run-review requirements also apply.

## Shared evaluation contract

Use bounded synthetic tasks with externally checkable answers or unit-tested artifacts. Actor-visible information excludes hidden test answers and evaluator-only labels. Exact Jev typed schemas and Haiku/Qwen versions require separate qualification; do not silently use a generative fallback where Jev cannot perform an operation. Compare Jev decisions with a deterministic gate using the same observations.

The heterogeneous condition needs strong homogeneous controls, including repeated calls to the strongest usable model and same-model specialists with matched tools. Model family, skill inventory, information, role and exposure time are separate factors. Report both fixed-dollar and fixed-call/token views; these are different estimands, not magically identical budgets. Charge creation, pruning, failed attempts, copying, retrieval, communication and evaluation overhead to separate visible ledgers.

For evolutionary language, specify the unit: a policy, skill bundle, pair or workspace. Copying is an externally controlled finite operation. There is no model-weight evolution. Replacement is permitted only within a fixed population/resource cap. Policies selected on development tasks face untouched held-out tasks. Precommit selection rules and keep unsuccessful lineages. A controller should never award a bonus simply for exhibiting the biological phenomenon being tested.

Use independent populations/islands as replicates, paired task seeds where appropriate, and population-level confidence intervals. Messages, offspring and generations within one lineage are dependent observations. Pilot variance may inform sample size only under a separate registered development plan; no sample-size adequacy is claimed now. The final preregistration must specify minimum relevant effects and decision thresholds before held-out outcomes are seen.

Every event needs run/condition/seed, policy and model IDs, artifact parents, exposure set, task result, cost, and intervention time. Define one measured replay per design below; aggregate summaries must be reproducible from that event stream. Missing model calls and invalid artifacts remain visible. None of the proposed visualizations currently exists as measured output.

## HX-31 — Self-differentiating swarms: specialization through subtraction

**Question and starting condition.** Can a uniform network discover a cheaper division of labor while preserving performance and the ability to adapt? Every initial agent uses the same generalist model, tools, skills, data permissions and resource rules. Model downgrades, smaller loaded skill inventories, shared providers and topology changes are outcomes. No agent is assigned a provider role in the adaptive arm.

**Concrete workload.** Repeated analysis jobs with overlapping data needs and externally checkable outputs. Agents initially fetch, parse and carry their own context. A shared service must expose data with timestamps and provenance through permitted interfaces. Freshness requirements and task arrival patterns are fixed independently of the candidate topology.

**Core comparison.** Frozen generalists; generalists with a simple shared cache/service; a static specialist configuration optimized on separate development jobs; and an adaptive configuration allowed to choose and revise services, capabilities and models. All arms share legal data access and an explicit lifetime budget. Charge optimizer inference, migration, context, provider calls, communication, validation and maintenance. A cache baseline receives the same freshness information and cannot be artificially disadvantaged.

**Mechanism ablations.** Separate service sharing from removal of tools/skills and model downgrading. Only then add the temporal hardening component from HX-37: expensive discovery produces reusable validated procedures, cheaper-model execution or deterministic code. Compare with repeated expensive execution and a fixed engineered workflow. A cheaper model must actually run its assigned work; a model label or mocked lower price is insufficient. Jev is a possible typed decision component only after its exact supported contract is qualified.

**Adaptation intervention.** After measuring stable-workload quality and cost, vary workload overlap, change an API/data schema or withdraw a provider. Allow a finite, costed repertoire of restoring capabilities, adding provider redundancy, changing edges or escalating to a stronger model. Freeze a matched copy of the learned configuration to isolate adaptation from the value of the learned architecture itself.

**Primary evidence.** Compare total cost per verified success at a prespecified reliability/freshness requirement. Report the full quality-cost-latency tradeoff, including adaptation and exploration costs. Track duplicated calls, context traffic, retained skills, model allocation, provider count and recovery loss. Unit of replication is an independent swarm/workload seed, not individual messages or dependent task completions.

**Kill criteria.** Plain caching or static specialization captures all gains; savings require skipping work or serving stale data; hidden optimizer information or uncharged calls favor the adaptive arm; or realistic changes erase the benefit. These outcomes can still recommend a useful simpler architecture, without supporting a self-organization claim.

**Biological boundary.** Call the result Black Queen-like only when agents genuinely shed costly self-sufficiency and become dependent on providers, with removal/rescue evidence. Workflow hardening and deterministic compilation are broader software mechanisms. No foundation-model weights evolve.

**Visualization mapping.** Start with identical nodes. Use measured events to show provider formation, removed duplicate calls, unloaded capabilities, model substitutions and changing communication edges. Overlay verified quality, freshness and cumulative cost. Provider failures, restoration and escalation are visible on the same timeline; do not count omitted tasks as savings.

**Closest overlap.** [[morris-2014-coexistence]] informs the dependency mechanism. [[kim-2026-multi]], [[yue-2025-masrouter]], [[ong-2024-routellm]] and [[gh-denis-pplx-autojev]] motivate reuse/routing/cheaper-execution controls. The candidate contribution is discovering and revising their combination from a uniform start; novelty is unconfirmed.

## HX-32 — Historical symbiotic-pair sketch; deprioritized

**Current decision:** no separate project. The owner considers this ordinary modularity; the former sketch below does not establish a compelling practical gap.

**Question and unit.** Does learned interface compatibility make a persistent Jev–generative pair a useful inherited unit, while making it less adaptable? Unit of replication: independently adapted pair lineages; pairing itself is not evidence of a higher-level individual.

**Treatment and comparators.** Persistent versus shuffled partners × pair-level versus separate policy selection. In a second controlled comparison, fix a standardized interface or allow the same bounded set of interface fields/skill conventions to co-adapt. Match representation size, historical examples and total calls. Include same-model pairs and a deterministic-controller pair.

**Sequence.** Start with independently viable components and an interoperable interface. Select policy variants on the original task ecology. Freeze copies for solo, native-pair and reciprocal swapped-pair evaluation. Introduce a held-out task shift. Compare continued native pairing, partner exchange, and interface normalization without adding new information or compute. A normalization intervention must specify exactly what semantics it preserves.

**Primary evidence.** A pair-specific interaction exceeds each component's ordinary quality advantage; its interface persists under joint inheritance; and familiar-task gains trade off against adaptation after a shift. The sharper result is that normalization changes the adaptation penalty while preserving access and budget. Measure both release and destruction of useful cooperation.

**Kill criteria.** Dependence was wired in initially; any equally capable partner substitutes; only extra memory explains native-pair gains; or the alleged escape is extra inference. These support orchestration or memorization, not the proposed transition.

**Visualization mapping.** Draw measured pair genealogies with two model colors and an interface version. At swaps, show an empirical compatibility matrix; after the task shift, plot independent adaptation curves and the measured cost of interface normalization.

**Closest overlap.** [[kelley-2026-endosymbiotic]] already measures digital symbiotic constraint and organelle-like dependence. The remaining candidate is semantic/typed interface compatibility without hard-coded trait-match rewards. The conceptual label alone is not novel.

## HX-33 — Supporting study: workspace hardening and portability

**Question.** How much capability can move into durable tools, tests, schemas and cached knowledge so that a cheaper successor model preserves quality? This is a supporting ablation within HX-31.

**Comparison.** Cross naive/experienced agents with clean/hardened workspaces. Then cross workspace builder family with successor family at matched information, legal access and lifetime cost. Include an equal-information cache, standardized schemas and an independently engineered workspace. Do not award credit for answer leakage or relaxed freshness.

**Evidence.** Measure successor quality-cost curves, the number of repetitions needed to recover construction cost, portability across model families, and maintenance after a task or API change. A general benefit can justify useful engineering. A family-by-builder crossover supports a narrower compatibility effect; endogenous population feedback is a deferred extension rather than the primary endpoint.

**Kill criteria.** Ordinary caching/tool engineering explains all gains; construction and maintenance never repay their costs; gains disappear on held-out tasks or cheaper successors. Report these outcomes without embellishing them as ecological discoveries.

**Visualization and overlap.** Replay workspace artifacts with provenance and matched successor performance. [[kim-2026-multi]] and the Artifact Ecology preprint in `LITERATURE.md` are close prior art. The practical question is where to invest in model capability versus its operating environment.

## HX-35 — Historical cultural-speciation sketch; parked

**Current decision:** defer until a realistic integration scenario and practical payoff are identified. The theoretical sketch below is retained for reference.

**Question and unit.** Do independently adapted skill bundles become internally complementary but difficult to recombine? Unit of replication: islands initialized with identical model mixtures, tasks and allowed tool schemas.

**Treatment and comparators.** Vary a preregistered migration rate while holding total exchanges fixed through within-island controls. Freeze bundles at the same resource milestones. Cross island A/B agent policies with A/B procedural modules. Include same-island recombination, shuffled unlinked bundles, homogeneous-model islands and a fixed shared protocol.

**Sequence.** Permit bounded skill adaptation and inheritance; then evaluate native and hybrid configurations on held-out compositions of familiar task primitives. Provide a dictionary and schema translator with equal total budget. Separately test a semantic procedure translator to identify whether a deeper rewrite, rather than a lexical translation, is required. Do not select only the most visually divergent islands.

**Primary evidence.** Native combinations outperform hybrids after symbol/schema alignment, with a procedure-by-partner interaction larger than arbitrary shuffled-module incompatibility. Controlled migration should change that gap. Measure whether benefits from specialization compensate for loss of mergeability.

**Kill criteria.** Ordinary vocabulary translation repairs all failures; one base model is simply weaker; components were incompatible from initialization; or shuffled bundles exhibit the same failure without historical co-adaptation. That would be dialect variation or generic integration difficulty, not the proposed speciation-like mechanism.

**Visualization mapping.** Show island exchange histories and procedure genealogies, then a measured recombination matrix. Keep lexical distance separate from functional compatibility. The most informative frame may show similar vocabulary with sharply different hybrid performance.

**Closest overlap.** [[stengel-eskin-2026-glossogen]] and [[lai-2024-evolving]] rule out claiming language invention or social clusters as the novelty. This is a more demanding procedural recombination test.

## HX-37 — Historical failed-artifact salvage sketch; consolidated

**Current decision:** no independent project. The active interpretation is temporal workflow hardening inside HX-31. The earlier concurrent-salvage design below is an optional mechanism and must not be treated as identical to temporal hardening.

**Question and unit.** Can a consumer earn a resource niche by transforming discarded donor work? Unit of replication: paired donor-consumer task populations, with artifact histories retained.

**Treatment and comparators.** Consumers receive verified locally useful fragments from failed whole attempts, length/topic-matched shuffled fragments, successful trajectories, or no donor material. Include an independent fresh-attempt arm with equal total inference resources. Compare direct reuse against consumer transformation; use identical selection rules in all arms.

**Sequence.** Produce donor attempts before assigning consumer exposure. Mark whole-attempt failure using the independent task verifier; separately label local validity without revealing held-out answers. Freeze donor artifacts for matched comparisons. Measure consumer contribution, then remove and restore the byproduct stream. In a population phase, initialize a low consumer resource share and let an externally fixed marginal-contribution rule determine its future share.

**Primary evidence.** Verified new output is causally traceable through transformation of failed material, rather than copying a concealed complete answer. Resource removal eliminates the consumer's advantage; restoration rescues it. A consumer that repeatedly earns a share from rarity supports a niche claim. A one-shot gain supports artifact salvage only.

**Kill criteria.** Completed answers leak through; donor costs are excluded; the consumer merely supplies more attempts; or the harness reserves a consumer quota. Cross-feeding is also weakened if another identical donor continuation performs as well at the same cost.

**Visualization mapping.** A provenance graph links failed donor artifacts to intermediate transformations and independently verified outcomes. Edge weights show charged resource flows and measured marginal value. The replay includes withdrawals, unsuccessful transformations and consumer resource share, not just successful examples.

**Closest overlap.** [[kim-2026-multi]] and [[park-2026-scaling]] establish reuse and shared progress. Bacterial cross-feeding needs the outstanding Rosenzweig methods read. Information is non-rival; the scarce currency is compute/context, not literal consumption of text.
