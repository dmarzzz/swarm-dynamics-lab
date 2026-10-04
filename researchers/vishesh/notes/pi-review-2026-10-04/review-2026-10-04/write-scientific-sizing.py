"""Write the PI design assessment; no source mutations or experiments."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
REF = "f027940fcb5b892057e65306f8e7550456ed2945"
REMOTE = "researchers/vishesh/notes/optimal-swarm-size/"

review = {
    "id": "SCI-SIZING",
    "name": "Optimal swarm size: a deployable conditional launch policy",
    "evidence_class": "Detailed prospective design only. No implemented harness, validated task generator, qualification, model episode, or sizing result is established by these documents.",
    "decision": "Develop the task contracts and a smaller identifying pilot. Defer the proposed 2,512-episode core/transfer programme and 1,280-episode optional extension until useful size-dependent heterogeneity exists and the runtime is measurable.",
    "interest": {
        "judgment": "Scientifically worthwhile and operationally clear, with unusually careful prospective controls.",
        "why": "A launch rule that increases verified success under an actual deadline and aggregate budget is useful; charging selection, coordination, retrieval, retries and cancellation makes the question substantially more meaningful than a best-looking N sweep.",
        "novelty_boundary": "Task- and architecture-dependent scaling is already acknowledged in the design. The proposed contribution is a deployable rule evaluated on fresh executions with charged overhead, not discovery of a universal optimum. Novelty remains unestablished pending the focused methods comparison."
    },
    "robustness": {
        "supported": "The draft specifies a coherent estimand, independent-root splits, intention-to-treat failures, hidden evaluators, aggregate resource accounting, paired comparisons and fresh policy evaluation. These are design strengths, not demonstrated harness properties.",
        "unsupported": "No evidence yet supports an optimal size, reliable five-point near-optimality, a learned selector, physical-memory effects, or cross-domain transfer. One locked transfer family supports one-family transfer only.",
        "unit": "An independently generated task root; repeated model samples, paraphrases, sizes and profiles remain nested or paired within that root.",
        "independent_variation": "Root semantics and dependencies, plus independent model sampling. Two development families and one transfer family do not create a broad population of independent task domains.",
        "assessment": "Four fit and four validation roots per structural cell cannot establish fine conditional boundaries. The documents candidly flag this. Choose complexity and interval interpretation accordingly; do not let 2,512 correlated episodes imply strong precision. Simultaneous uncertainty must govern the smallest-within-epsilon decision."
    },
    "scenario_quality": {
        "size": "N=1,2,4,8,16 counts addressable stateful contexts including the coordinator; four runnable slots in P0 make N>4 a queue/context-capacity intervention as well as a roster intervention. This is legitimate but must be interpreted explicitly.",
        "challenge": "The arithmetic dossier and clamp repair are contract illustrations, not evidence of research-grade difficulty. Establish non-ceiling correctness and a genuine serial/parallel tradeoff before the response map.",
        "complexity": "Vary dependency width/depth while matching atomic work, output count and evaluator burden. The roster-aware model also constructs a plan, so primary effects concern the whole protocol, including changed decomposition quality.",
        "realism": "Repository repair offers practical task structure; synthetic dossiers and simulated incidents offer control. None yet captures long-running deployment, evolving requirements, human escalation or uncontrolled services, which should remain outside the initial claim.",
        "definition": "Exact artifact contracts, equivalent repair sequences and accepted alternative citation proofs are strong. Pin all currently open actor-turn, truncation, initialization and integration-reserve values before implementation."
    },
    "scenarios": [
        {
            "name": "Q-A baseline calibration and Q-B engineering qualification",
            "assessment": "The 16 N=1 screening episodes and 64 larger-roster episodes intentionally use different caps; they cannot estimate a size effect. Success-conditioned pooled cost/time quantiles select an operating regime rather than a production SLA.",
            "improvement": "Check cap-hit and solvability distributions by family/structure before freezing the core. Separate marginal cost/time quantiles do not guarantee joint feasibility. Preserve screening failures and stop when a cell is trivial or impossible."
        },
        {
            "name": "Evidence dossier: independent sections versus linked deductions",
            "assessment": "Best first mechanism environment: verifiable sources and proof requirements make information access auditable. Trivial arithmetic risks measuring formatting or retrieval overhead alone.",
            "improvement": "Use matched multistep provenance problems with plausible distractors and alternative valid proofs. Keep distractor load fixed initially; vary dependency structure, not every difficulty dimension simultaneously."
        },
        {
            "name": "Repository repair: independent defects versus interface chains",
            "assessment": "A useful second family with real integration costs. Isolated copies and deterministic merging prevent uncontrolled filesystem races, but this is a particular coordination protocol; merge conflicts may dominate the apparent size effect.",
            "improvement": "Match defect count and hidden-test burden; report planning, patch correctness and integration failures separately. Include meaningful interface dependencies rather than many independent one-line fixes."
        },
        {
            "name": "Incident triage: locked transfer",
            "assessment": "Stateful observations, safety constraints and equivalent repair sequences are a stronger transfer test than renamed arithmetic. A task contract exists, but no reviewed held-out fixture yet demonstrates complexity or realizability.",
            "improvement": "Validate the simulator and evaluator with separate development fixtures. Freeze transfer generators and selector features before revealing transfer outcomes; report the narrow family-transfer boundary."
        },
        {
            "name": "Core P0/P1/P2/P3 and optional M1/M2/M3/H1",
            "assessment": "Baseline, half deadline, half budget and one runnable slot are interpretable one-axis contrasts. Reduced context, no ledger, reduced physical memory and eight slots are distinct extensions; no-ledger changes communication architecture.",
            "improvement": "Initially prioritize N-by-dependency; add N-by-deadline or N-by-service-capacity only when the first pilot identifies a mechanism. Defer physical-memory claims until local measurement is available, and label ledger removal a protocol change."
        },
        {
            "name": "Fresh locked selector evaluation",
            "assessment": "Charging selection and keeping the transfer size map sealed are excellent protections against hindsight. A global best fixed N is insufficient by itself to establish the value of task-conditioned sizing.",
            "improvement": "Compare against a development-frozen resource-profile-only size rule, or explicitly make this an ablation of the existing heuristic. This distinguishes useful task features from simply responding to a tighter deadline or fewer slots."
        }
    ],
    "controls": {
        "retain": "N=1 with the same tools and sequential work interface; equal retrievable evidence union; aggregate budgets; coordinator included in N; hidden evaluator; all failures retained; paired roots; fresh policy runs; charged initialization/selection; source and context receipts.",
        "missing": "A resource-only selector comparison for incremental task-feature value, and a separate deterministic scheduling fixture with a known public work graph to distinguish scheduler overhead from model decomposition errors. The latter is harness validation, not an oracle-assisted primary arm.",
        "confounds": "Roster-dependent plans, N-by-service contention, aggregate context capacity and integration conflicts are combined in the operational effect. External API load and version changes require randomized blocked execution; logical concurrency is not a physical-hardware measurement."
    },
    "parameters": [
        {"parameter": "Dependency width/depth", "current": "Independent versus linked structures", "priority": "Essential identifying axis", "proposed_variation": "Two matched structures within one family initially", "reason": "Establish whether useful parallel work changes the value of added contexts."},
        {"parameter": "Roster size", "current": "1,2,4,8,16", "priority": "Essential identifying axis", "proposed_variation": "Start at 1,2,4 under four service slots", "reason": "Identify a practically useful transition before paying for queue-dominated larger rosters."},
        {"parameter": "Resource pressure", "current": "P0 plus half deadline, half budget and one slot", "priority": "Essential for eventual conditional deployment; staged", "proposed_variation": "Freeze one baseline envelope first, then one mechanism-motivated pressure contrast", "reason": "Avoid an uninterpretable map dominated by universal feasibility or failure."},
        {"parameter": "Task difficulty", "current": "Generated roots; illustrative simple cases", "priority": "Qualification requirement", "proposed_variation": "Match work/output burden and calibrate nontrivial baseline solvability", "reason": "A ceiling masks benefits; universal failure makes size selection meaningless."},
        {"parameter": "Selector complexity and epsilon", "current": "Interpretable tree/response model; proposed epsilon=0.05", "priority": "Essential decision definition", "proposed_variation": "Predeclare a shallow rule and operationally justified tolerance; permit inconclusive near-ties", "reason": "Data volume must support the claimed decision resolution."},
        {"parameter": "Context, ledger and hardware", "current": "Optional M1/M2/M3/H1", "priority": "Later stress tests", "proposed_variation": "One extension justified by observed bottlenecks", "reason": "These change different mechanisms and need separate estimands and measurement."}
    ],
    "next_study": {
        "question": "Does task dependency structure produce a reproducible difference in the operational benefit of increasing a fixed-protocol roster?",
        "primary_contrast": "The paired N=4 minus N=1 success-by-deadline difference in parallel versus linked dossiers; N=2 locates the response rather than creating another primary claim.",
        "endpoint": "Verified complete artifact received by the frozen deadline within aggregate budget; partial proof quality, cost and integration failures are diagnostic secondary outcomes.",
        "unit": "Fresh independent dossier roots paired across sizes; model samples nested within root.",
        "design": "One family, two matched structures, three roster sizes and one frozen resource profile. Validate deterministic contracts and lifecycle receipts first. Freeze screening-derived caps before fresh pilot roots; choose affordable root replication for the desired uncertainty using qualification variability, not a universal sample minimum. Hold out root lineages and use only genuinely launch-visible features. Train no flexible selector until a stable interaction is plausible.",
        "go_no_go": "Expand if task scoring and resource accounting work, the regimes are neither ceiling nor floor, and root-level evidence suggests a practically meaningful conditional choice. Otherwise revise task difficulty or use the simplest fixed policy. Only then evaluate a frozen conditional rule against the resource-only baseline on fresh executions."
    },
    "sources": [
        {"path": f"review-2026-10-04/scientific-sources/optimal-swarm-size-{name}", "upstream_path": REMOTE + name, "ref": REF, "url": f"https://github.com/dmarzzz/swarm-lab/blob/{REF}/{REMOTE}{name}", "detail": detail}
        for name, detail in [
            ("README.md", "Full read: prospective scope, conditional objective, grid, profile arms, 2,512/3,792 planning totals, split/analysis and launch gates."),
            ("PROTOCOL.md", "Full read: actor lifecycle, deterministic scheduler, budget reservations, selection accounting, qualification caps and transfer lock."),
            ("TASK-CONTRACTS.md", "Full read: dossier proof checker, isolated repair/merge evaluation, simulated triage, information equivalence and root splitting.")
        ]
    ]
}

payload = {
    "scope": "PI scientific-design review of the three pinned optimal-swarm-size documents. No experiments, model calls, or source modifications performed. Qualitative judgments concern a prospective design, not empirical results.",
    "reviews": [review]
}
task_check = BASE / "scientific-sizing-thread-check.json"
if task_check.exists():
    payload["latest_task_check"] = json.loads(task_check.read_text())
    review["sources"].append({
        "path": "review-2026-10-04/scientific-sources/optimal-swarm-size-design.json",
        "detail": "Current task design.json copied read-only; structured draft v3 confirms reviewed dimensions and unresolved launch values. No new experiments."
    })
(BASE / "scientific-sizing.json").write_text(json.dumps(payload, indent=2) + "\n")
print("Wrote scientific-sizing.json")
