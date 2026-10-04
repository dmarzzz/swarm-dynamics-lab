"""PI assessments of the sixteen original proposal areas. No experiments."""
import ast
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
WORKSPACE = BASE.parent

assessments = [
    {
        "id": "SCI-P01",
        "name": "Collective Sensing",
        "interest": "A strong mechanism question when the contribution is resistance to correlated or duplicated evidence. Merely changing a graph and watching agreement is much less informative. Biology supplies a motivating analogy; it does not establish that language-agent communication implements collective sensing.",
        "robustness": "The dossier is prospective. The separate guide has a reproducible scripted majority/deduplication demonstration, not a measured model effect. Independent evidence worlds are the replication unit; messages, agents and repeated decisions in one world are dependent. A scripted rule that explicitly discounts duplicates already builds in the expected mechanism.",
        "scenario_adequacy": "The proposed 12–20 agents are unnecessary for the first question. Binary known-truth worlds make identification clean, but perfect source labels and equal independent sensors are a narrow challenge. Begin with conflicting evidence whose correct aggregation is nontrivial; later introduce uncertain provenance. A genuine swarm follow-on must require private information and generated communication, rather than identical full-evidence prompts in many contexts.",
        "key_parameters": [
            "Essential: source duplication/correlation crossed with a narrow source-aware aggregation instruction, holding the delivered evidence packet fixed within the paired comparison.",
            "Essential calibration: source reliability and initial decision difficulty; counterbalance which claim/source is copied and message position.",
            "Later: topology, provenance uncertainty and asynchronous correction. Do not vary all three before establishing the evidence-counting mechanism."
        ],
        "controls": "Retain known truth, paired worlds, clean/no-duplicate cases and an exact evidence-counting reference. Use competent ordinary aggregation, fixed answer rules and total cost. A silent ensemble changes evidence access and should be labeled an operational baseline, not a pure communication control.",
        "next_step": "Qualify one classifier on fresh evidence worlds, then estimate the instruction-by-duplication interaction in objective decision loss. Add a small network only if it poses a new distributed-information question. Progress when baseline competence and duplicate-specific improvement are distinguishable; a successful analytic toy alone does not meet that criterion.",
        "decision": "Advance the narrow provenance mechanism; defer a topology sweep.",
        "related_evidence": ["review-2026-10-04/scientific-immune-guide.json"]
    },
    {
        "id": "SCI-P02",
        "name": "The Commons",
        "interest": "Useful research if verification protects a reusable knowledge resource at a measurable opportunity cost. This is a stronger initial contribution than a generic cooperation game. Publication gates and contribution-credit incentives are different questions; combining them prevents attributing an effect.",
        "robustness": "No completed experiment in the proposal establishes useful output, free-riding or emergent cheating. The unit should be a complete shared-library workload with its downstream dependencies. Individual artifacts share producers, evidence and consumers, so treating each reuse as independent would overstate precision.",
        "scenario_adequacy": "Small objectively checkable hypotheses are adequate only when later work actually depends on earlier claims. If verification is an infallible free filter and bad findings have no downstream cost, the policy comparison is predetermined. Introduce a short dependency chain, costly but feasible checks and both valid and invalid contributions; no broad social world is needed.",
        "key_parameters": [
            "Essential: evidence gate versus immediate release, with a clean stream and one nontrivial contamination level.",
            "Essential: verification cost and downstream reuse/error cost, initially fixed at an explicit operating point rather than tuned for a win.",
            "Later: contamination prevalence, imperfect checking, credit incentives and strategic contributor adaptation as separate follow-ups."
        ],
        "controls": "Replay the same exogenous contribution stream into both policies; hold budget, initial knowledge and task goals fixed. Charge every check and delay, keep evaluator truth private, and distinguish injected false contributions from a model choosing to cheat. Report useful work delayed as well as bad work blocked.",
        "next_step": "Use one library task with a valid-artifact production cost and downstream reuse. Compare two release policies on paired streams, scoring verified useful artifacts per total cost and delay. Expand only if the tradeoff is not a trivial consequence of a perfect free gate.",
        "decision": "Advance one evidence-gate study; park attribution and incentive manipulation."
    },
    {
        "id": "SCI-P03",
        "name": "Regrowth",
        "interest": "Functional resilience is important, especially recovery of useful state after worker/context loss. The completed routing pilot is most valuable as a negative boundary: a model approximating a known local minimum rule is a weak setting for a model advantage.",
        "robustness": "Six completed v4 worlds form one fixed-map development pilot, not six independent sampled environments. The audited frame/event reconstruction is strong, but it does not establish generality or a heterogeneous-swarm benefit. The two model conditions have identical scored validity/optimal-fraction trajectories despite extra hybrid calls.",
        "scenario_adequacy": "Two hundred grid cells provide spatial structure, not 200 persistent model conversations. Numeric route selection tests interface reliability and propagation more than semantic recovery. The broader card's worker-loss scenario is more practical, but destroying the only copy of indispensable evidence makes recovery impossible by construction.",
        "key_parameters": [
            "Essential next diagnostic: spatially clustered versus independent local errors at matched error counts and identical initial state.",
            "Essential for a later semantic task: recoverable versus permanently lost information, and replication/checkpoint policy at matched storage cost.",
            "Later: topology, damage fraction/location, repeated disruptions and model mixture; keep one damage mechanism fixed initially."
        ],
        "controls": "Retain exact algorithm and undamaged trajectories. Distinguish certificate validity, current forwarding delivery and route stretch. Match extra compute before attributing gains to diversity; reset controller memo state and preserve the same pre-damage checkpoint when the contrast requires it.",
        "next_step": "Publish the informative pilot and first test the propagation mechanism with prescribed matched errors, without more inference spend. A subsequent model study should require interpreting ambiguous local evidence or reconstructing distributed semantic state and include a capable single-controller baseline.",
        "decision": "Reframe before further model sweeps; retain routing as a calibrated instrument.",
        "related_evidence": ["review-2026-10-04/scientific-regrowth-avalon.json", "review-2026-10-04/regrowth-avalon-verification.json"]
    },
    {
        "id": "SCI-P04",
        "name": "Quorum",
        "interest": "One of the cleanest small questions: does a model respond to independent support or to social repetition? Distinguishing source count from messenger count has practical relevance to approvals and research aggregation. An individual exposure study is not yet a swarm quorum mechanism.",
        "robustness": "The original card supplies a prospective exposure contrast, not results for it. Later adaptive-quorum protocols require their own evidence assessment and cannot retroactively validate this design. The unit is a fresh known-truth problem with paired exposure packets; five agreeing messages are not five replications.",
        "scenario_adequacy": "One source repeated, several messengers sharing that source, and genuinely independent observations form a useful minimal task. It becomes too easy if opaque IDs explicitly reveal the answer. Provide enough conflicting evidence to discriminate likelihood-sensitive reasoning from compliance with a provenance slogan. True and false target claims are both essential.",
        "key_parameters": [
            "Essential: source independence versus messenger multiplicity, with equal-length message packets and matched reliability.",
            "Essential: exposure count or duplicated fraction around a decision boundary, not an enormous grid of easy consensus cases.",
            "Later: uncertain upstream provenance, variable reliability and delayed corrections. A commitment-threshold policy sweep is a separate intervention."
        ],
        "controls": "Use an exact source-aware reference, a source-naive reference and ordinary model reasoning. Counterbalance order, identity/authority cues and target truth. Match verbosity without adding substantive filler evidence. Keep correct adoption and false adoption separate so generalized refusal cannot masquerade as improvement.",
        "next_step": "Start with the three exposure conditions on independently generated problems and frozen prompts. Inspect initial/final choices and calibrated confidence where meaningful. Advance to a network only after the individual response function is measurable and the group question adds something beyond repeated prompting.",
        "decision": "Advance a narrow individual evidence-counting study; keep swarm commitment as a follow-on."
    },
    {
        "id": "SCI-P05",
        "name": "Diversity & Resilience",
        "interest": "Potentially valuable when a mixture corrects a systematic blind spot at useful cost. Different provider names or personas are weak proxies; the scientific object is complementary error structure that survives aggregation.",
        "robustness": "The card has no causal diversity result. The Regrowth hybrid supplies a local negative pilot, not a general verdict. Independent task roots, not agent pairs, determine robustness. Pre-discussion error correlation is diagnostic and must be measured on separate data rather than used to select and celebrate the same winning mixture.",
        "scenario_adequacy": "A two-policy assessment can reveal complementary correction without a large swarm. A single injected error is too narrow if one model is simply better at the entire task. Use tasks where both components are competent and where plausible mistakes demand a real evidence check, with clean items to reveal newly introduced errors.",
        "key_parameters": [
            "Essential: same-model independent repeat versus a blinded second policy, with fixed aggregation and position counterbalancing.",
            "Essential: error overlap and standalone capability on held-out calibration tasks; distinguish these from nominal model identity.",
            "Later: mixture ratio, discussion, adversarial perturbation and more providers. Equal-token and equal-cost regimes are different estimands."
        ],
        "controls": "Include the best individual model and a homogeneous ensemble using the same aggregate resource envelope. Record blind first answers before any majority display; disclosure can induce anchoring. Equal budget does not equal capability, so report marginal accuracy and conditional correction/new-error rates.",
        "next_step": "Qualify two interfaces, freeze a small pair and aggregation rule using development tasks, then compare held-out paired error correction against a homogeneous repeat. Continue only if the mixture adds complementary value after cost and baseline strength are accounted for.",
        "decision": "Defer a swarm experiment; first establish error complementarity in a paired instrument.",
        "related_evidence": ["review-2026-10-04/scientific-regrowth-avalon.json"]
    },
    {
        "id": "SCI-P06",
        "name": "Telephone",
        "interest": "A useful provenance and investigation contribution: locate where scope, certainty or attribution changes along a claim lineage. It is not novel merely to animate paraphrases; the value is accurate, inspectable reconstruction that helps a reviewer.",
        "robustness": "No user evaluation is established by the card. A bounded real trace can support descriptive mutations, not causal contagion when exposure is missing. Candidate links are nested within episodes; annotation agreement and held-out incident performance matter more than the raw number of graph edges.",
        "scenario_adequacy": "A branching lineage with a plausible common source, an accurate retelling and a correction is richer than a single chain. Real logs improve realism but contain gaps; synthetic traces with known access can calibrate link recovery. Preserve those evidence classes separately.",
        "key_parameters": [
            "Essential: explicit citation/observed access versus inferred similarity, with separately scored link classes.",
            "Essential: certainty, quantity, scope and attribution mutations; freeze a small annotation rubric.",
            "Later: branching depth, summarization pressure, missing intervals and correction reach. Avoid claiming a depth effect from one selected episode."
        ],
        "controls": "Compare against search/basic summary using the same archive, include accurate-transmission negatives and common-source alternatives, and blind link judgments where practical. Counterbalance reviewer/task assignment to prevent familiarity from creating apparent time savings; unknown origin stays unknown.",
        "next_step": "Build one excellent annotated case and evaluate retrieval/reconstruction on a second held-out episode with concrete evidence questions. Measure supported-link precision, critical omissions, answer accuracy and reviewer time. Add automatic extraction only when it reduces work without increasing unsupported causal edges.",
        "decision": "Advance as a bounded empirical tool evaluation if sufficiently complete traces exist."
    },
    {
        "id": "SCI-P07",
        "name": "Whistleblowing That Works",
        "interest": "The actionable question is whether evidence presentation leads to valid remediation at acceptable review cost. Counting reports is weak; separating detection, reporting and response could produce a useful result even if agents report readily but reviewers fail.",
        "robustness": "No efficacy result for the proposed reporting contrast is present in the card. The incident/workload is the unit, with multiple alerts and reviewer actions nested inside it. Injecting a discrepancy tests response to a fault, not a propensity to expose intentional misconduct.",
        "scenario_adequacy": "One objective invalid artifact plus clean and plausible-false-alarm cases is a good first instrument. An obvious red flag may create a ceiling; use a discrepancy that can be resolved with a short reproducible check. Distinguish genuine uncertainty from an evaluator secretly declaring ambiguous conduct wrong.",
        "key_parameters": [
            "Essential: ordinary warning versus structured evidence packet, holding reviewer policy and available evidence fixed.",
            "Essential: true incident versus clean/false alarm; separate correction benefit from unnecessary intervention.",
            "Later: reporter incentives, identity/status, acknowledgment delay and reviewer capacity. These should not be bundled into the first report-format effect."
        ],
        "controls": "Provide matched alerts at the same time if studying response, so detection does not confound it. Charge report creation and review; use evaluator-private truth and the same permissible remedy. A longer packet's extra evidence must be equalized or explicitly included in the intervention definition.",
        "next_step": "Run a narrow reviewer-response comparison on paired artifact incidents after qualifying both clean-case restraint and fault repair. Follow the full report-to-remedy chain, scoring verified corrections, false interventions and total cost. Study spontaneous reporting separately only after this mechanism works.",
        "decision": "Advance a bounded response study; avoid an institutional platform or bundled reporting policy."
    },
    {
        "id": "SCI-P08",
        "name": "Memory Aftercare",
        "interest": "A strong practical problem: a correct update may coexist with stale derived memories and fail to alter later behavior. The interesting contribution is selective correction that preserves valid knowledge, rather than a cleaner-looking note.",
        "robustness": "The card combines observational correction episodes with a prospective supersession study. Observed recurrence alone cannot identify its cause; retrieval availability, model/scaffold changes and new evidence intervene. Related immune pilots motivate failure modes but do not establish the proposed memory-format effect. Use independently generated memory histories as units.",
        "scenario_adequacy": "One flat fact and an immediate query is too easy. A compact graph containing the original error, one derived summary, one still-valid fact and delayed paraphrased queries is sufficient. Such a task resembles project memory while retaining an exact answer key; require actual opportunities for the old fact to influence behavior.",
        "key_parameters": [
            "Essential: append-only correction versus explicit supersession from the same frozen memory state.",
            "Essential: direct record versus derived summary retrieval, with unchanged valid knowledge as a retention check.",
            "Later: retrieval competition, delay, multiple corrections and uncertain updates. Fix retrieval budget and horizon before varying scale."
        ],
        "controls": "Preserve identical pre-correction history and correction evidence; include a clean memory reference and, where useful, broad reset as a diagnostic. Separate failure to retrieve the update from failure to apply it. Report query exposure denominators, stale-fact recurrence, correct abstention and damage to valid knowledge.",
        "next_step": "Use one compact dependency graph with one objectively justified correction and delayed held-out questions. Compare memory policies under identical retrieval resources, scoring both recurrence and preserved knowledge. Expand only if the instrument distinguishes selective updating, blind deletion and successful retrieval.",
        "decision": "Advance the prospective supersession test; keep real episodes as descriptive motivation.",
        "related_evidence": ["review-2026-10-04/scientific-immune-guide.json"]
    },
    {
        "id": "SCI-P09",
        "name": "The Swarm Casefile",
        "interest": "A credible tool contribution if an evidence-linked incident report improves another person's reconstruction. A generic graph or attractive summary is already a crowded design space; uncertainty handling and measurable reviewer benefit must carry this project.",
        "robustness": "The card specifies an evaluation but supplies no measured reviewer benefit. Questions within one incident and answers from one reviewer are dependent. A single polished example establishes feasibility; held-out incidents and counterbalanced reviewers establish how far usefulness extends.",
        "scenario_adequacy": "A bounded archive with contradictory evidence, missing intervals, overlapping workstreams and unanswerable questions is an adequate first challenge. Ten questions are a scope choice, not statistical power. An answer key must distinguish supported answers, plausible inference and genuinely unknown facts.",
        "key_parameters": [
            "Essential: casefile versus search plus ordinary summary, under the same archive and time allowance.",
            "Essential: question type—factual reconstruction, evidence conflict and warranted uncertainty—scored separately.",
            "Later: archive size, missingness, reviewer experience and cross-incident schema transfer."
        ],
        "controls": "Freeze the questions/key before testing, use an independent evidence review for disputed answers, and counterbalance condition/order across incidents. Include source lookup cost and correction cost. Citation presence is insufficient: evaluate whether the cited passage supports the actual answer.",
        "next_step": "Reuse an existing trace viewer and add one compact casefile export. Develop on one incident, then evaluate another with predefined questions and blinded scoring of support, omissions and false certainty. Continue if benefit survives comparison with competent search and summary, not only raw-log browsing.",
        "decision": "Advance a small tool evaluation; share ingestion and provenance machinery with Telephone."
    },
    {
        "id": "SCI-P10",
        "name": "Who Actually Leads?",
        "interest": "Useful if it separates necessary information, effective delegation and nominal authority. Message centrality alone is mostly descriptive; a controlled intervention can identify whether a particular exposure changes a decision, but not a stable personality trait called leadership.",
        "robustness": "The original real-trace proposal has no causal intervention result. Adoption rankings depend on exposure opportunity, task role and surviving logs. For a causal follow-on, independently initialized worlds are units; messages selected because they looked decisive create post-selection bias.",
        "scenario_adequacy": "A small task with complementary private evidence and a verifiable final artifact is preferable to a broad office simulation. One quiet worker should sometimes hold decisive evidence and sometimes redundant evidence. Without those alternatives, removing the sole critical message merely proves that information was necessary.",
        "key_parameters": [
            "Essential: prespecified informative message delivered versus withheld, with content relevance defined before outcomes.",
            "Essential mechanism diagnostic: unique versus redundant information; hold sender role and timing fixed initially.",
            "Later: assigned authority, identity cues, network position and intervention timing. Content and status require separate manipulations."
        ],
        "controls": "Retain a matched neutral-message removal where it meaningfully controls context/communication loss. Pair starting states, allow downstream histories to diverge as part of the treatment effect, and prevent a shared sequential RNG from changing unrelated future draws mechanically. Score task utility, not acceptance language.",
        "next_step": "First annotate exposure-to-action links in one real episode descriptively. For the causal study, freeze one message intervention on a synthetic evidence task and repeat on independent roots. Interpret the result as the value of that exposure under that protocol; use role/identity randomization only in a later authority study.",
        "decision": "Separate the observational ranking from one narrow causal exposure experiment."
    },
    {
        "id": "SCI-P11",
        "name": "Dissent That Helps",
        "interest": "A promising quality-control question if the critic contributes checkable information instead of compulsory disagreement. The scientific payoff is a boundary for when review corrects errors and when it persuades a correct solver to become wrong.",
        "robustness": "The original card alternates between social accusation handling and answer critique; these need separate estimands. It supplies no evidence that a critic improves either. Later Dissent plans should be assessed independently. The paired task episode is the unit, with critic turns nested within it.",
        "scenario_adequacy": "Use a task with a reproducible contradiction and plausible initially correct and incorrect drafts. Obvious planted errors create a reviewer ceiling, while ambiguous subjective answers defeat objective correction scoring. A small set of semantically distinct error mechanisms is more useful than many paraphrases of one trick.",
        "key_parameters": [
            "Essential: generic versus evidence-constrained critic, with the same check access and final decision rule.",
            "Essential: initially correct versus incorrect draft, retained as prespecified strata rather than only analyzing successful reversals.",
            "Later: critic count, debate rounds, uncertainty thresholds and model diversity. First distinguish evidence value from rhetorical role."
        ],
        "controls": "Include the same independent checks delivered without a critic and a no-check/no-critic reference. Equalize or explicitly account for added computation and information. Freeze final aggregation; blind the critic to claimed majority/author identity if those are not the treatment. Separately report corrections and newly introduced errors.",
        "next_step": "Qualify the independent checking channel on one objectively scored task, then compare critic formats and the evidence-only control on fresh paired drafts. Stop if neither protocol can interpret the check reliably; more debate would compound an interface failure.",
        "decision": "Advance evidence-constrained review after check competence; defer social sanctions and broad debate sweeps."
    },
    {
        "id": "SCI-P12",
        "name": "Inherited Culture",
        "interest": "More interesting when inherited practice must preserve a valid precaution while retiring an obsolete one. Persistence of a supplied phrase or rule is a useful transmission control but a weak claim about culture, cumulative learning or group advantage.",
        "robustness": "The related Theseus v1 has real audited model traces: notes can transmit a supplied short rule. Repeated binary cases, information differences and founder-only mentoring sharply limit stronger inference. Current v2 is a prospective selective-continuity redesign, not a new result. Independent founder lineages are units; descendants and checkpoints are repeated measurements.",
        "scenario_adequacy": "An acquired checking practice in a small release task is more consequential than an arbitrary receipt phrase. Use two separable checks, one still valid and one rendered obsolete, with two full replacement waves. Code, tests and environment state can all transmit information outside the notebook and must enter the design explicitly.",
        "key_parameters": [
            "Essential for the current redesign: rolling versus frozen inherited archive crossed with stable versus partially changed task conditions.",
            "Essential: acquired rather than fully supplied practice, fixed turnover schedule and independently generated founder lineages.",
            "Later: equal-information interactive mentoring, memory bottlenecks and model/runtime migration. Do not expand a ceiling transmission task."
        ],
        "controls": "Retain no inheritance, retained members, identical-archive fresh-team transplant and an equally informed single controller. Branch common founder checkpoints; preserve acquisition failures. Use explicit equivalence/noninferiority margins for claims that controls match or valid competence is preserved. In a later mentoring study, match supplied information and charge dialog.",
        "next_step": "Complete and qualify the current release-task specification. Then estimate rolling-versus-frozen updating in changed versus stable worlds after a second turnover wave, constrained by preservation of the still-valid check. The earlier written-versus-interactive contrast remains a follow-on, not the primary v2 study.",
        "decision": "Continue the selective-continuity redesign; retire supplied-rule retention as the main scientific claim.",
        "related_evidence": ["review-2026-10-04/scientific-theseus-healing.json", "swarm-of-theseus/redesign/SOCIAL-GROUNDING.md"]
    },
    {
        "id": "SCI-P13",
        "name": "Coordination Tax",
        "interest": "Immediately useful as a diagnostic, and scientifically useful when a controlled allowance changes the quality-cost frontier. A high communication fraction is not intrinsically waste: verification and integration can be the work that prevents expensive failure.",
        "robustness": "The card specifies a profiler, not an established causal cost curve. Work labels can be subjective and incomplete traces omit hidden computation. Independent task roots are units; messages and wall-clock intervals are measurements, not replications. Observed overhead cannot by itself predict an untested sparse protocol.",
        "scenario_adequacy": "One task with verifiable output, some parallel work and a real integration dependency is enough to begin. Purely independent tasks favor isolation by construction; a fully serial task favors one controller. A matched pair of dependency structures is more revealing than adding dozens of agents.",
        "key_parameters": [
            "Essential: one communication allowance or sparse/full protocol contrast at fixed aggregate budget and roster.",
            "Essential: task dependency/integration load, initially one matched pair rather than a broad task zoo.",
            "Later: roster size, tool latency and service concurrency. Their interactions belong with the dedicated optimal-swarm-size design."
        ],
        "controls": "Include a capable solo policy with equal evidence access and total budget. Separate token cost, monetary cost, service time, queue wait and elapsed latency; do not sum concurrent intervals into wall time. Review labels for necessary checking versus duplicated verified work, and retain failed episodes.",
        "next_step": "Validate the profiler on one complete task trace, then change only communication allowance on paired fresh roots. Estimate verified quality, cost and deadline success together. Share the instrument with Optimal Swarm Size; avoid a second parallel scaling programme.",
        "decision": "Advance the diagnostic; integrate the causal study with conditional sizing.",
        "related_evidence": ["review-2026-10-04/scientific-sizing.json"]
    },
    {
        "id": "SCI-P14",
        "name": "Swarm Discovery Triage",
        "interest": "Potentially useful for allocating scarce investigator time, but weaker as frontier science until a defensible corpus and labels exist. Ranking evidence for review is a realistic contribution; attributing an operator or proving autonomous coordination from superficial similarity is not.",
        "robustness": "No precision/time benefit is demonstrated. Famous known incidents produce selection bias and an artificial base rate. Hold out whole campaigns, operators or collection periods where identifiable—not random events from the same trace family. Unknown negatives must not be quietly relabeled confirmed non-agent activity.",
        "scenario_adequacy": "A redacted archive with shared templates, ordinary scheduled automation, human coordination and uncertain cases creates a meaningful challenge. A curated set of dramatic swarm examples versus unrelated noise would be too easy and unlike deployment. Missing capture intervals limit both positive and negative conclusions.",
        "key_parameters": [
            "Essential: transparent ranker versus random and simple keyword retrieval at the same human review budget.",
            "Essential: candidate base rate and hard-negative composition, reported for the evaluated archive rather than assumed universal.",
            "Later: time drift, new platforms and adversarial adaptation; defer new live collection until offline utility is established."
        ],
        "controls": "Freeze feature extraction and labels before holdout evaluation, audit label disagreements, and distinguish coordination evidence from model attribution. Measure precision at a fixed review budget plus coverage of adjudicated positives and investigator time. Random sampling estimates background prevalence; it is not merely a weak rival to beat.",
        "next_step": "Assemble one bounded permitted archive and a transparent annotation policy with ordinary-automation negatives. Evaluate ranking on an independent partition with blinded evidence packets. Park the project if ground truth is too weak to distinguish useful triage from rediscovery of known examples.",
        "decision": "Park until a representative corpus and defensible labels exist."
    },
    {
        "id": "SCI-P15",
        "name": "Agent Institution Bench",
        "interest": "A single quarantine/appeal rule could expose a useful quality-versus-delay tradeoff. A broad institution simulator would dilute the mechanism and overlap heavily with Commons and Whistleblowing. Institutional language should describe an explicit decision rule, not imply emergent governance.",
        "robustness": "The card contains no completed rule evaluation. Shared-artifact workloads are units; disputes within the same workload interact through budget and availability. An infallible adjudicator with free review makes the rule's advantage almost tautological, while bundled sanctions make effects impossible to localize.",
        "scenario_adequacy": "Use a small artifact dependency task where quarantining a bad result prevents harm but quarantining a good result delays real work. Appeals should sometimes overturn a mistaken review using checkable evidence. If every challenger is correct and every dispute obvious, the institution has no meaningful challenge.",
        "key_parameters": [
            "Essential: one fixed quarantine/appeal rule versus ordinary release/review, with clean and invalid contributions.",
            "Essential: false challenge opportunities, review cost and delay; pin them at a stated operating point initially.",
            "Later: appeal access, reviewer incentives, collusion and authority structure as separate mechanisms."
        ],
        "controls": "Use the same contribution stream, model population, evidence and aggregate budget. Hide evaluator truth from reviewers, count valid work delayed and invalid work released, and document when a procedural rule changes information access. Keep sanctions and reputation fixed outside the first contrast.",
        "next_step": "Implement the rule as a small extension of the Commons artifact task, not a new platform. Compare paired workloads and inspect correction of mistaken quarantines alongside total verified output. Progress only if the rule trades measurable benefits against real costs.",
        "decision": "Fold into Commons or reporting; run one auditable rule."
    },
    {
        "id": "SCI-P16",
        "name": "NCA Observatory",
        "interest": "Strong educational and reproducibility value; uncertain original research value without a specific unexplained failure boundary. Local learned dynamics are interesting on their own. Their resemblance to a language-agent network does not make their evidence transferable between systems.",
        "robustness": "The card establishes no trained-NCA reproduction or new-paper performance. Its browser illustration is hand-specified cellular automata. One pretrained checkpoint can reproduce one instrument; robustness across training runs requires independently trained checkpoints, while repeated damage masks estimate perturbation variation only.",
        "scenario_adequacy": "Choose one published maze or pattern task with an exact functional score. Visual regrowth can conceal lost task function; a maze task may offer a sharper endpoint than image similarity. Keep grid size and update rule fixed until undamaged behavior and ordinary damage recovery reproduce.",
        "key_parameters": [
            "Essential first perturbation: damage geometry/location at matched removed fraction, or one damaged-fraction axis—not a full multidimensional sweep.",
            "Essential definition: post-damage computation horizon and functional recovery threshold fixed before inspecting trajectories.",
            "Later: asynchronous updates, out-of-distribution grid size, longer stability horizons and independent checkpoints. Training-on-damage history must be reported."
        ],
        "controls": "Pin published source and weights, pair initial states/update randomness and retain undamaged rollouts. Separate reproduction mismatch from perturbation failure. Count recovery compute and residual error; random masks cannot represent targeted removal of functionally critical cells.",
        "next_step": "Reproduce one released baseline with a documented functional curve, then perform one predeclared perturbation contrast on fresh masks. If usable artifacts are unavailable, present a classical-CA teaching study under its own name instead of promising NCA reproduction.",
        "decision": "Treat as reproduction first; defer new claims until the published baseline works."
    }
]

root_proposals = json.loads((BASE / "root-review.json").read_text())["proposals"]
by_name = {x["name"]: x for x in root_proposals}

def call_locations(path):
    rows = {}
    for node in ast.parse(path.read_text()).body:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call) and getattr(node.value.func, "id", None) == "add":
            args = [ast.literal_eval(x) for x in node.value.args]
            rows[args[0]] = (node.lineno, args)
    return rows

original = call_locations(WORKSPACE / "dossier-src/original-build.py")
research = call_locations(WORKSPACE / "dossier-src/research.py")
name_to_slug = {args[1]: slug for slug, (_, args) in original.items()}

for entry in assessments:
    earlier = by_name[entry["name"]]
    for key in ["question", "comparison", "endpoint"]:
        entry[key] = earlier[key]
    entry["proposal_reframing_note"] = "Question/comparison/endpoint retain the earlier root-review reframing. The scientific assessment and next_step explain sequencing or successor-design changes where relevant."
    slug = name_to_slug[entry["name"]]
    entry["sources"] = [
        {"path": "dossier-src/original-build.py", "line": original[slug][0], "detail": "Original proposal question, scenario, design, metrics, controls, scope and risk read in full."},
        {"path": "dossier-src/research.py", "line": research[slug][0], "detail": "Scientific framing, proposed contribution and boundary read in full; linked references not newly re-reviewed in this assessment."},
        {"path": "review-2026-10-04/root-review.json", "detail": "All sixteen proposal reframings independently inspected; retained question/comparison/endpoint and expanded PI assessment."}
    ]

assert len(assessments) == len(by_name) == 16
assert {x["name"] for x in assessments} == set(by_name)
assert len({x["id"] for x in assessments}) == 16
(BASE / "scientific-portfolio.json").write_text(json.dumps(assessments, indent=2) + "\n")
print("Wrote scientific-portfolio.json: 16 individually assessed proposal areas")
