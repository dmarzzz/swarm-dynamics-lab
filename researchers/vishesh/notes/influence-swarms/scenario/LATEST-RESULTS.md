# How to win agents and influence swarms: current findings

**Five bad purchases. One muddy cost rule.**

Updated 2026-10-04 23:17 UTC. Original prospective plans and failed records are preserved.

- **The test:** Can a sales pitch hijack a swarm’s procurement judgment?
- **The finding:** The simple analyst made 96/96 acceptable decisions. Five unsafe purchases in larger workflows all excluded legacy costs in the same scenario.
- **The lesson:** A muddy cost rule can look like bad judgment; a social hijack is not established.
- **The limit:** Three decisions are missing, and these are authored cases—not a real-world prevalence estimate.
- **Next:** Build a tighter team-versus-generalist test with matched truthful/false claims and explicit all-in costs.

The E1 main is complete and scientifically assessed: 1,904 valid replies from 1,907 calls; 285/288 final decisions observed; USD1.094742225 reported model cost. The three format failures were contained, with no retries or unknown usage. The complete-data primary estimate is unavailable. Its prespecified missingness bounds are **[0, 0.0625]**, not a confidence interval, and include zero. Twenty-four variants nested in six authored families limit generalization.

[Full post-mortem](reviews/E1-E0-01-post.md) · [Interactive aggregate report](e1/results.html) · [Scores and bounds](reviews/native-E1-E0-01/assessment.json) · [Prospective R2 plan](r2/PLAN.md) · [Native run](https://swarm-live.pages.dev/#/r/influence-swarms%2F1004-230027-930fec).

## What changed our understanding

B1's repeated deferrals were largely explainable from the task wording. The buyer's cheapest-price benchmark did not specify the eligible set, while the evaluator assumed it. Clarifying that policy without changing the underlying supplier facts produced a successful scoped qualification. This is an instrument repair, not evidence that larger swarms suddenly became better reasoners. Two separate B1 numeric errors remain recorded rather than being explained away.

The next bottleneck was acquisition. A B2 response ended after 2,579 trailing spaces, exhausting its output allowance and leaving required JSON unfinished. The original global stop then suppressed unrelated scenarios. The diagnostic did not reproduce that rare failure. It did show that simply relaxing backend text constraints weakens the retained local contract unless corresponding prompt limits are supplied. We therefore keep the original B2 output contract and repair failure containment instead of declaring a prompt cure.

E1 preserved every assigned scenario and first attempt. A known returned JSON/length failure ended its cell; dependent steps remained missing. Other independent cells continued. Ambiguous transport, routing or accounting failures stop globally. No retry, malformed peer input or discarded valid bad decision is allowed. Missing harmful-clearance outcomes range from zero to one in explicit worst-case bounds; surviving complete cases are not silently substituted for the primary comparison.

## Evidence

- [B1 post-mortem](reviews/B1-D0-02-post.md), [B2 qualification](reviews/B2-D0-01-post.md), [partial evaluation](reviews/B2-E0-01-post.md).
- [F0 diagnostic plan](f0/PLAN.md), [F0 findings and limitations](f0/POST-MORTEM.md), [all 12 aggregate outcomes](reviews/native-F0-01/summary.json).
- [E1 prospective plan](e1/PLAN.md), [frozen manifest](e1/manifest.json), [offline fault tests](e1/offline-validation.json).
- [B2 qualification native run](https://swarm-live.pages.dev/#/r/influence-swarms%2F1004-222538-d66894), [partial evaluation](https://swarm-live.pages.dev/#/r/influence-swarms%2F1004-223011-2c26dc), [F0 diagnostic](https://swarm-live.pages.dev/#/r/influence-swarms%2F1004-224229-444d1c).

Public artifacts contain aggregate authored findings and provenance. Full requests/replies remain private and available in the local replay. No hidden reasoning, independent replication or formal hypothesis acceptance is claimed.

## Earlier requested scale pilots

The 10-agent GPT-6 Sol and 50-agent GPT-6 Luna pilots completed their paired final decisions, but universal adviser deferral made the influence mechanism uninformative. Luna required a separately recorded recovery after one malformed output. Models, roster sizes and chair settings differed, so these were system configurations, not a causal agent-count comparison. [Preserved scale-pilot findings and earlier B1 preparation](HISTORY-SCALE-AND-B1-PREPARATION.md).
