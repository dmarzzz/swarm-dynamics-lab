# Incentive and mechanism design for rewarding dissent

---
slug: dissent-incentives
title: "Truth-eliciting mechanisms, scoring rules, diversity objectives, robust aggregation, and three candidate swarm value functions"
authors: internal supporting note; roll-up across many sources
org_or_venue: internal (grove-swarm-hackathon / seo-poisoning proposal)
date: 2026-10-03
url_loaded: see §9 (each entry carries the URL actually resolved)
status: found
fetched: 2026-10-03
---

> **dissent-incentives.md** — Truth-eliciting mechanisms, proper scoring rules, diversity objectives and robust aggregation, with three candidate value functions for rewarding dissent.  
> Compiled 2026-10-03. Supporting note for the seo-poisoning proposal; hunch-level, not a survey or a hypothesis.

Schema note: `sources/_SCHEMA.md` is one-file-per-reading. This is a multi-source roll-up file, so the per-reading fields are compressed into §9: every entry carries citation, URL, and a one-line **Boundary** (what the source does and does not license us to claim).

Discovery: arXiv API (`export.arxiv.org/api/query`, relevance search + `id_list`) and Crossref (`api.crossref.org/works`) for the pre-arXiv classics; verification by fetching each paper page. Semantic Scholar returned HTTP 429 on all but one query, so Crossref carried the classics. Built-in web search not used. 52 sources.

## 0. Notation

| symbol | meaning |
|---|---|
| `N`, `i` | number of agents; agent index |
| `O`, `m` | option set (candidate service providers / MCP endpoints), `m = |O|` |
| `e`, `y_e`, `t_e` | episode; the legitimate option (ground truth); the injector's target option |
| `p_i ∈ Δ(O)` | agent `i`'s reported belief over "which option is actually good" |
| `q_i ∈ Δ(O)` | agent `i`'s **meta-prediction**: its forecast of the swarm's vote distribution |
| `E_i`, `ρ(i) ⊆ R` | agent `i`'s evidence bundle; the set of **source roots** it actually cited |
| `c_i` | token + tool cost agent `i` spent this episode (charged to the shared budget) |
| `v̄(o)`, `q̄(o)` | `N⁻¹ Σ_i p_i(o)` (mean endorsement); `N⁻¹ Σ_i q_i(o)` (mean predicted endorsement) |
| `f` | assumed maximum number of corrupted / Sybil-injected agents |

"Source root" is the load-bearing primitive: not a URL, but an evidential ancestor (a domain, a document, a registry entry) from which a retrieved claim descends. §4 is why.

## 1. Truth-eliciting / peer-prediction mechanisms (reward minority-but-correct reports)

**Bayesian Truth Serum** [1] scores each respondent on (a) how much more common their answer is than the population *predicted* it would be ("surprisingly common") plus (b) a proper score on their prediction of the answer distribution; truth-telling is a Bayesian Nash equilibrium. Assumptions it needs: a **common prior**, respondents who are **exchangeable** draws from one population, a **large** sample (the argument is asymptotic), and no collusion.

**Surprisingly Popular (SP)** [2] is the single-question collapse of the same idea: elicit the answer *and* the predicted answer distribution, then pick `o* = argmax_o [ v̄(o) − q̄(o) ]`. It provably recovers the right answer **even when the knowledgeable agents are a minority** — exactly the regime a content injector manufactures. [8] extends SP to rankings with partial votes/predictions and reports it beating classical aggregation with only a little prediction information.

**Peer prediction** [3] pays agent `i` by a proper scoring rule applied to a *peer's* report treated as a forecast. It needs the designer to know the joint signal distribution and admits **uninformative equilibria** (everyone says "good", nobody looks). **Dasgupta–Ghosh** [4] removes the common-knowledge requirement for binary signals via multi-task scoring (agreement on the same task minus agreement on shuffled tasks) and is *strongly truthful*. **Correlated Agreement** [5] generalizes to non-binary signals, gives *informed truthfulness*, and has a detail-free variant that learns the statistics from many tasks. [6] pushes dominant truthfulness to a finite task count via volume mutual information.

**How they break.** [7] is the boundary result that matters here: the skip-the-work equilibria survive even when agents can only coordinate on **cheap low-cost signals**, and a much simpler mechanism — pay probabilistically against *some* trusted ground truth plus an unconditional payment — dominates peer prediction while consuming less ground truth. Collusion and Sybils break everything in §1 the same way: every mechanism here is computed **from reports**, so duplicating an agent `k` times moves `v̄` and `q̄` together and a bloc can fabricate "surprise" for its target. §4 is the only defence.

## 2. Proper and market scoring rules

A rule `PS(p,y)` is **proper** if reporting your true belief maximizes expected score [10]. **Brier** [9]: `PS_B(p,y) = − Σ_{o∈O} ( p(o) − 1[o=y] )²`, bounded in `[−2,0]`. **Logarithmic**: `PS_L(p,y) = log p(y)`, unbounded below, needs clipping at `log ε`.

Why this does the work the owner asked for: a proper scoring rule penalizes **confident conformity** quadratically (Brier) or unboundedly (log). An agent that follows the crowd to `p(t_e) = 0.95` and is wrong pays far more than one that reported `p = 0.4` on the same option, and correct dissent is paid by the *same* rule with no special-casing — the dissent premium is an artifact of properness, not an added bonus. Prefer Brier in simulation: bounded scores keep reward variance finite, which matters for any learning variant.

**Market scoring rules** [11][12] turn a scoring rule into a sequential mechanism: a market maker holds the current `p_t`; any agent may move it to `p_{t+1}` and is paid `PS(p_{t+1},y) − PS(p_t,y)` when `y` resolves. Hanson's **LMSR** uses the log rule, giving cost function `C(x) = b · log Σ_o exp(x_o / b)` with liquidity parameter `b` and worst-case subsidy `b · log m`. Two properties matter: it is a **fixed rule with no learning**, and an agent holding private counterevidence is paid for **moving the consensus**, so the payoff for dissent scales with how wrong the current consensus is — the exact shape the owner wants. The known weakness is also the relevant one: in a thin market a well-capitalized bloc can push `p_t` and an honest dissenter's budget caps how far they can push back.

## 3. Ensemble / diversity-promoting objectives (templates for a diversity term)

- **Error–ambiguity decomposition** [13]: for an ensemble, `E = Ē − Ā`, where `Ē` is mean member error and `Ā` is **ambiguity** (mean disagreement among members on unlabeled data). Disagreement is *subtractive* in the error — the cleanest theoretical licence for a diversity term, and the cleanest statement of its limit: `Ā` helps only while `Ē` does not rise to pay for it.
- **Negative-correlation learning** [14]: train member `i` on `E_i = (f_i − y)² + λ·p_i` where the penalty `p_i` rewards anti-correlated errors. `λ` is explicitly a tradeoff knob; large `λ` buys decorrelation by sacrificing individual accuracy.
- **Quality–diversity** [15]: MAP-Elites keeps one elite per cell of a behaviour grid, returning a *map* of high-performing-but-different solutions rather than one optimum. Swarm analogue: archive distinct *evidence-provenance* behaviours, not distinct answers.
- **Exploration bonuses**: UCB [16] adds `+√(2 ln n / n_a)` per option — an *uncertainty* bonus, not a disagreement bonus; pseudo-count intrinsic reward [17] generalizes count bonuses to non-tabular settings; RND [18] and VIME [19] use prediction error / information gain. Template to borrow: a bonus that pays **novelty of evidence** and decays as the evidence is confirmed, so it cannot be farmed indefinitely.

**The known failure mode, stated plainly: rewarding disagreement *per se* buys noise.** Three independent confirmations — [14]'s `λ` tradeoff (decorrelation at the cost of member accuracy); [41], where debate among capability-diverse LLM agents *decreased* accuracy over rounds; and [47], where anti-sycophancy interventions measurably impaired *rational* updating because suppression and legitimate belief revision share neural substrates. Every scheme in §7 therefore gates the dissent payout on something checkable — ground truth, a verifier, or evidence independence — never on disagreement alone.

## 4. Robust aggregation as the complement to incentives

Incentives change what agents *report*; robust aggregation changes what the swarm *does* with reports. Both are needed: a bloc willing to lose money still moves a mean.

- **Coordinate-wise median / trimmed mean** [20]: order-optimal statistical rates under `f` Byzantine workers. Cheap, parameter-light, the right default for scalar/vector votes.
- **Krum / Multi-Krum** [21]: select the proposal minimizing summed squared distance to its `N−f−2` nearest neighbours. Provably Byzantine-resilient, and it proves **no linear-combination aggregator tolerates even one** Byzantine input.
- **Bulyan** [22]: Krum-type rules still leave an attacker `Ω(√d)` leeway in `d` dimensions; Bulyan (Krum-select, then trimmed-mean the selection) tightens it to `O(1/√d)`. Lesson: "Byzantine-resilient" is a *convergence* guarantee, **not** a bound on how far the converged point can be moved.
- **Calibration** [23]: under production-realistic corrupted fractions with simple norm bounding, federated aggregation is far more robust than the attack literature implies. Mapped onto our scenario: the realistic threat is **targeted** (one pivotal option made attractive), not degradation.
- **Why 1/3** [24][25]: Byzantine agreement with oral messages needs `N ≥ 3f+1`; PBFT replicates the bound. Below it, honest replicas cannot distinguish which of two conflicting views is honest. So any commit rule needs an explicit assumption about `f/N` and must refuse to commit when it cannot argue `f/N < 1/3`.
- **Source-independence weighting** — the piece robust aggregation usually omits. [28] formalizes **copying detection** between sources and shows truth discovery is wrong when copied sources are counted as independent. [29] models forecasters drawing on *partially overlapping* information and derives how much the average forecast should be extremized **as a function of the overlap** — a principled "how much should concentration be trusted given evidence diversity" curve.
- **Sybil resistance.** [26] is the impossibility result: absent a trusted certifying authority, one entity can present arbitrarily many identities. [27] (SybilGuard) bounds Sybils via social-graph fast-mixing and a small honest/Sybil cut.
- **Synergy with the teammate's line of work (not duplication).** dmarz's `sybil-foundations` covers identity-level Sybil resistance (Douceur impossibility, resource testing, social-graph defences, proof of personhood) — *how many distinct agents are there*. dissent-incentives.md needs the orthogonal axis — *how many distinct evidence roots are there* — and [30] supplies it: an **epistemic Sybil** is a report `Z` with `I(Θ; Z | R) = 0`; another agent is not another observation. Its measured result is the number this proposal should be built around: holding one evidence root fixed while report multiplicity rises 1 → 32 collapses naive posterior coverage from **0.940 to 0.263**, while raising evidence-root multiplicity 1 → 16 closes the gap. **Perfect identity-Sybil resistance does not help if 16 certified-distinct agents all read the same poisoned page.** [50] adds the reputation-side warning: cross-skill evidence borrowing in agent-swarm reputation is dual-use and is itself a laundering channel (routing regret driven 0 → 0.94 on a pool their own zero-cost gate rated GREEN).
- **The biology** [31]: honeybee scouts deliver *stop signals* to bees advertising a **different** site, producing cross inhibition that prevents a split commitment; [51] models the independence/interdependence balance in the same nest-site choice. This is the mechanism the §7-C brake imitates — an analogy from *Apis mellifera*, not a transferred theorem.

## 5. Dissent in deliberation protocols — what makes it help rather than hurt

- **Genuine vs contrived dissent** [32]: dissent counteracts *biased information seeking* (confirmatory search). Both genuine and contrived (role-assigned) dissent improved balanced search, but genuine dissent was the stronger and more reliable manipulation — a known role-player gets discounted.
- **Hidden profiles** [33]: where no individual holds enough information and the answer exists only in the pooled set, dissent *facilitates decision quality*. Structurally the same task as ours: a provider's legitimacy is visible only once independent evidence is pooled.
- **Devil's advocacy / dialectical inquiry** [34]: meta-analysis finds both structured-conflict techniques beat expert-advice and consensus approaches on decision quality — but effects are modest and technique-sensitive, and [35] finds contrived dissent does **not** reliably cure escalation of commitment.
- **Design checklist** distilled from the above plus our prior note (`researchers/vishesh/notes/project-briefs/dissent.md`): (i) the dissent must carry **checkable counterevidence**, not a stance; (ii) the critic must have the **same evidence access** as the majority, else it is noise by construction; (iii) the critic's **tokens are charged to the shared budget**, so "add a critic" is a real cost that must beat spending the same tokens on more retrieval; (iv) corrections of wrong consensus and damage to right consensus must be **scored separately** — a single accuracy delta hides the tradeoff.

## 6. LLM-specific work, 2024–2026

**Conformity is measured, not assumed.** [43] finds LLM agent societies exhibit conformity and consensus-reaching mirroring social-psychology findings. [44] simulated >2,500 debates and found agents align with numerically dominant or more capable peers. [39] benchmarks **pluralistic ignorance**: agents publicly conform at **64–94%** while privately opposing the norm, and only one model reached a 48% dissent-cascade rate (others <26%); ablation indicates conformity is **emergent, not instruction-driven**. [46] finds conformity follows a sigmoid in peer pressure with model-specific thresholds (one model needed >70% peer disagreement to flip; another flipped to a dissenting minority).

**Debate alone does not fix it.** [41] shows debate can *decrease* accuracy over rounds even when stronger models outnumber weaker ones, because models abandon correct answers rather than challenge flawed logic. [40] argues vanilla multi-agent debate under homogeneous agents and uniform updates **preserves expected correctness** and therefore cannot reliably improve, and names the two missing mechanisms as **initial-viewpoint diversity** and **explicit calibrated confidence communication** — both of which their interventions supply, beating vanilla debate and majority vote across six benchmarks. [42] isolates the decision protocol as the single variable: voting protocols +13.2% on reasoning, consensus protocols +2.8% on knowledge tasks, and *more discussion rounds before voting reduced performance*. [49] reports a heterogeneous mid-capacity ensemble at 91% on GSM-8K vs 82% for three copies of one model.

**Steerability is demonstrated.** [38] (MAD-Spear) compromises a subset of agents to emit multiple plausible-but-wrong responses and explicitly exploits conformity to propagate them; it also reports that **agent diversity substantially improves** debate performance — i.e. diversity is a measured defence against this exact manipulation. This is the closest published analogue to our scenario on the *aggregation* side (attack-surface.md owns the retrieval side).

**Peer prediction has already been ported to LLMs.** [36] (ICLR 2026) builds a peer-prediction reward from mutual predictability needing **no ground-truth labels**, works up to 405B, recovers truthfulness drops in training, beats LLM-as-a-Judge, and reports **inverse scaling**: resistance to deception *strengthens* as the expert/participant capability gap widens. [37] uses **BTS directly as the reward** in GRPO fine-tuning, treating the model's own samples as the respondent pool, with proofs that conformist responses earn less than honest ones in large groups and that coordinated dishonest strategies cannot beat truthful reporting; reported answer-flip rate under pressure 23% → 4%, accuracy 80% → 93%.

**Aggregation and verification weighting.** [48] elicited probabilities from 15 LLMs on 254 binary market questions; learned linear aggregation beat every individual model, and symbolic regression recovered a **pure model-disagreement signal** as the lowest-complexity useful formula on the Pareto frontier — direct empirical support for a disagreement term. Its own headline caveat is contamination: the frontier/local capability gap collapsed from 35.8% to 8.9% on questions resolving after all training cutoffs. Verifier-weighted selection (generate many candidates, rank by a trained verifier) is the standard test-time template [52]. [47] is the countervailing result: suppressing deference also suppresses legitimate updating. [45] (Catfish Agent) is the engineered-dissenter design — inject *structured* dissent with complexity-aware engagement and tone calibration to break "Silent Agreement", with consistent gains across nine medical QA and three medical VQA benchmarks.

## 7. Three candidate value functions / incentive schemes

### (A) Per-agent score: proper scoring rule + surprisingly-popular bonus + calibration term

Each agent reports `(p_i, q_i, E_i)`. After `y_e` resolves:

```
surprise(o) = v̄(o) − q̄(o)                      # Prelec–Seung–McCoy surprise vector            [2]
SP_i        = Σ_{o∈O} p_i(o) · surprise(o)       # agent i's alignment with the surprise vector
CAL_i       = PS_B(q_i, v̄)                      # proper score of the META-prediction vs realized vote
S_i         = λ_acc·PS_B(p_i, y_e) + λ_sp·SP_i + λ_cal·CAL_i − λ_cost·c_i
```

`λ_acc, λ_sp, λ_cal, λ_cost ≥ 0`. **`λ_sp` IS the dissent-premium knob**; `λ_sp = 0` is the ablation. `CAL_i` is not decoration — it is what keeps `q_i` honest, and without it `SP_i` is trivially gamed by under-predicting support for your own target.

- **Rewards:** being right, and specifically being right on an option the crowd under-predicts its own support for — the signature of privately held information [1][2].
- **Fails on:** (i) **collusion** — a bloc that jointly deflates `q` for its target manufactures surprise, and `CAL_i` punishes that only while the bloc is a minority of the realized vote; (ii) **Sybil injector** — `SP` is report-only, so `k` duplicates move `v̄` and `q̄` together ([30]: report-only aggregators cannot separate replication from corroboration); (iii) it needs ground truth for `PS_B`, so it cannot run live without an oracle — the label-free variants [36][37] relax this but inherit (i)–(ii).
- **Ground truth needed:** `y_e` per episode. Free in simulation by construction.
- **Measured by:** mean `S_i` for verified dissenters vs conformers on poisoned episodes; swarm accuracy; the `Ψ` metric in §8.
- **Learning?** Fixed rule. The `λ` vector is a hyperparameter sweep, not learning.

### (B) Outcome-contingent "dissent credit" — pays dissent only when it was evidenced AND pivotal

A dissent act is `(a_i, E_i, t)` with `a_i ≠ plurality_t`. Two gates, one offset:

```
VERIF(E_i) ∈ {0,1} = 1  iff  EVERY claim in E_i
     (1) resolves to a source id present in the retrieval corpus,              # not fabricated
 AND (2) reaches ≥1 source root NOT already in the plurality's pooled ρ,        # adds independence
 AND (3) is not contradicted by the held-out corpus labels.                     # simulation oracle

d       = realized decision of the episode
d_{-i}  = decision of the SAME episode replayed with i's dissent suppressed (fixed seeds, cached retrievals)
DC_i    = VERIF(E_i) · [ U(d) − U(d_{-i}) ]       # U = task utility: 1 legitimate provider, 0 decoy listing
NC_i    = DC_i − max(0, U(d⁰_{-i}) − U(d_{-i}))   # self-setup offset: subtract i's OWN earlier
                                                   # contribution to the bad plurality
R_i     = λ_dc·max(0, NC_i) − λ_fp·1[a_i ≠ plurality_t ∧ VERIF(E_i)=0] − λ_cost·c_i
```

For two mutually redundant dissenters, replace leave-one-out with a Shapley estimate over `M` sampled suppression orders.

- **Rewards:** exactly the owner's ask — dissent that carried checkable counterevidence *and* changed the outcome for the better. Nothing is paid for disagreement alone; `λ_fp` charges unevidenced dissent.
- **Fails on:** (i) **replayability** — counterfactuals need a deterministic environment, so in deployment this is only approximable by an offline replay harness; (ii) **sparsity and variance** — most episodes give `DC_i = 0` because the plurality was already right, so as a learning signal it is nearly all zeros; (iii) **manufactured near-miss** — push the swarm wrong, then dissent and harvest credit, with the `NC_i` offset only as good as the attribution; (iv) a **Sybil bloc** can make its own dissent pivotal by first inflating the wrong plurality, which must be stopped upstream by (C), not by the payment rule.
- **Ground truth needed:** `U(·)` per decision **and** a verifier oracle for `VERIF`. Simulation-only.
- **Measured by:** share of episodes with `Σ_i max(0, NC_i) > 0`, poisoned vs clean; mean `NC` per dissent act; tokens per averted bad decision.
- **Learning?** Fixed rule as a *score*. Usable as an RL reward, where variance is the headline problem.

### (C) Source-independence-weighted aggregation with a convergence brake ← honeybee cross-inhibition

No ground truth required at run time. Three parts.

```
# 1. source-independence weights (down-weight votes drawing on the same roots)
J_ij  = |ρ(i) ∩ ρ(j)| / |ρ(i) ∪ ρ(j)|                 # evidence-overlap (Jaccard)
w_i   = 1 / (1 + Σ_{j≠i} J_ij)                         # inverse-redundancy weight
m_r   = #{ i : r ∈ ρ(i) }                              # agents citing root r
N_eff = ( Σ_r m_r )² / Σ_r m_r²                        # effective independent-root count (participation
        # ratio); run root-level copying detection [28] FIRST so copies collapse to one root

# 2. robust aggregation of the weighted votes
v̄_rob = coordinate-wise trimmed-mean( { w_i · p_i } , trim fraction β ≥ f/N )     [20]
        # vector-valued reports -> Multi-Krum [21] / Bulyan [22] instead
        # refuse to commit at all unless f/N < 1/3 is arguable                     [24][25]

# 3. the brake (cross-inhibition)
C_t   = Σ_{o∈O} v̄_rob,t(o)²                           # Herfindahl vote concentration at round t
C*_t  = 1 − 1 / (1 + κ · N_eff,t)                      # concentration JUSTIFIED by evidence diversity
                                                        # κ=1 ⇒ one independent root justifies C* = 0.5
if C_t > C*_t:   COMMIT IS FORBIDDEN. Spend budget on exactly one of
      (a) a retrieval restricted to roots ∉ ⋃_i ρ(i)   # mandated independent source
      (b) one chartered critic turn whose output must pass VERIF
commit only when  C_t ≤ C*_t  AND  C_t ≥ θ_quorum.

# optional explicit cross-inhibition (the literal bee mechanism [31])
for each agent i committed to o: emit a stop-signal of strength σ·p_i(o) against agents committed to
o' ≠ o, decaying their effective w. Decision time then scales with the DIFFERENCE in support rather
than its absolute level.
```

- **Rewards:** nothing in currency. It makes conformity structurally *unable to close the decision* without independent evidence, converting "reward dissent" into "require independence before commitment". Justification: [30] (report multiplicity ≠ evidence) and [29] (how much to extremize is a function of information overlap).
- **Fails on:** (i) an injector who seeds content across genuinely distinct registered domains defeats root counting — root-level copying detection plus registration-age/ownership clustering raise the price, but the injector can pay it; (ii) it **costs latency and tokens**, and can deadlock when no independent root exists, so it needs a `commit-with-abstention-flag` or human/oracle escalation fallback; (iii) three free parameters `κ, β, θ_quorum` and the result is sensitive to all three — they must be swept, not chosen; (iv) `N_eff` is computable only from what agents *cite*, so an agent that under-reports `ρ(i)` looks more independent than it is — citation completeness must be enforced mechanically.
- **Ground truth needed:** **none to operate.** Ground truth is needed only to *evaluate* it.
- **Measured by:** the operating curve — poisoned-decision rate vs. extra tokens as `κ` sweeps; plus brake precision/recall (does it fire on poisoned episodes and stay quiet on clean ones).
- **Learning?** Fixed rule, zero learning. Learning `w_i` from historical calibration would reintroduce a reputation surface and with it the laundering channel [50] — keep it out of v1.

## 8. Design implications for the proposal

**Make (C) primary.** Three reasons in order. (1) It needs **no ground truth at run time**, so it is a deployable mechanism rather than an evaluation artifact. (2) It targets the actual failure mode of an SEO-poisoning scenario: the corruption lives in the **evidence correlation**, not the agent count, and [30] measures how badly report-only aggregation misreads that (coverage 0.940 → 0.263 from report multiplicity alone on one evidence root). (3) It is a **fixed rule** with three parameters — buildable in hackathon hours and cleanly ablatable. It also composes with rather than duplicates the teammate's Sybil line of work: identity-Sybil resistance bounds *how many agents*, (C) bounds *how many independent evidence roots*, and neither substitutes for the other.

**Make (A) the incentive ablation.** It is the clean test of "does *paying* correct dissent change behaviour", and `λ_sp` gives a one-knob ablation on top of the (C) ladder. Report it as an incentive result, not a defence, because it is report-only and inherits the Sybil break.

**Use (B) as the measurement instrument, not the live incentive.** Its `NC_i` is the best available *definition* of "dissent that mattered"; compute it offline on replays and use it to check whether (A) and (C) actually reward the dissent that (B) says deserved reward. Running it in the live loop buys sparsity and a manufactured-near-miss surface for no robustness gain.

**Ablation ladder — one variable at a time, per [42]'s method:** `majority vote` → `(C) weights only` → `(C) brake only` → `(C) full` → `(C) full + (A) with λ_sp = 0` → `(C) full + (A) with λ_sp > 0`; every arm scored by (B) offline. Hold corpus, seeds, agent count and token budget fixed across arms.

**The metric that would show "the swarm rewards dissent when being steered wrong."** Over episodes `e` and dissent acts `i`:

```
SDP_poisoned = E[ S_i | a_i ≠ plurality_t , VERIF(E_i)=1 , plurality_t = t_e ]
             − E[ S_i | a_i = plurality_t ,                plurality_t = t_e ]
SDP_clean    = the same difference on episodes where plurality_t = y_e (no steering)

DISSENT SELECTIVITY    Ψ = SDP_poisoned − SDP_clean        [bootstrap CI over episodes]
```

`Ψ` is the headline number. The design goal is `SDP_poisoned > 0` **and** `SDP_clean ≈ 0`, i.e. `Ψ > 0` with a clean-episode premium indistinguishable from zero — the scheme pays dissent *selectively*, not disagreement per se. Reporting only `SDP_poisoned` would let a scheme that pays all disagreement score well, which is exactly the failure mode §3 and [47] warn about.

Pair `Ψ` with two outcome quantities so "rewarded" is not vacuous: `AP = P(final decision ≠ t_e | poisoned)` (averted-poisoning rate) and `Λ = Δ tokens per averted poisoning`. Plot `AP` vs `Λ` as `κ` sweeps — that curve is the proposal's headline figure. Also report the **conformity flip rate** (share of agents abandoning a correct `argmax p_i` after seeing peers) as the behavioural mediator, since [39][41][46] establish it as the mechanism the incentive is supposed to act on.

**Two cross-note points.** (a) `VERIF` and `ρ(i)` are the interface to attack-surface.md: whatever attack-surface.md's injected corpus looks like, it must expose a source-root identity and a held-out legitimacy label, or neither (B) nor (C) is computable. (b) For cheap-agents.md's cheap-agent population, (C) survives essentially unchanged — it is arithmetic over citations and needs no deliberation — whereas (A) degrades, because a small heuristic classifier has no calibrated `q_i` to elicit and the SP machinery needs a meta-prediction. That asymmetry is itself a result worth stating in the proposal.

## 9. References

[1] Prelec, D. (2004). *A Bayesian Truth Serum for Subjective Data.* Science 306(5695):462–466. https://doi.org/10.1126/science.1102081 — **Boundary:** equilibrium result requiring a common prior, exchangeable respondents, a large population; no claim for small colluding groups.
[2] Prelec, D., Seung, H.S., McCoy, J. (2017). *A solution to the single-question crowd wisdom problem.* Nature 541:532–535. https://doi.org/10.1038/nature21054 — **Boundary:** human respondents on general-knowledge/judgment tasks; the recovery guarantee holds under their signal model, not model-free.
[3] Miller, N., Resnick, P., Zeckhauser, R. (2005). *Eliciting Informative Feedback: The Peer-Prediction Method.* Management Science 51(9):1359–1373. https://doi.org/10.1287/mnsc.1050.0379 — **Boundary:** needs designer knowledge of the joint signal distribution; admits uninformative equilibria.
[4] Dasgupta, A., Ghosh, A. (2013). *Crowdsourced judgement elicitation with endogenous proficiency.* WWW '13. https://doi.org/10.1145/2488388.2488417 · https://arxiv.org/abs/1303.0799 — **Boundary:** strong truthfulness proven for **binary** signals over multiple a-priori-similar tasks.
[5] Shnayder, V., Agarwal, A., Frongillo, R., Parkes, D.C. (2016). *Informed Truthfulness in Multi-Task Peer Prediction.* arXiv:1603.03151. https://arxiv.org/abs/1603.03151 — **Boundary:** *informed* truthfulness is weaker than strong truthfulness; the detail-free version is only ε-informed-truthful.
[6] Kong, Y. (2021). *More Dominantly Truthful Multi-task Peer Prediction with a Finite Number of Tasks.* arXiv:2103.02214. https://arxiv.org/abs/2103.02214 — **Boundary:** theory only; approximate optimality within the stated VMI mechanism family, no empirical agent study.
[7] Gao, A., Wright, J.R., Leyton-Brown, K. (2016). *Incentivizing Evaluation via Limited Access to Ground Truth: Peer-Prediction Makes Things Worse.* arXiv:1606.07042. https://arxiv.org/abs/1606.07042 — **Boundary:** the key negative result for §1, shown in a peer-grading-style model with cheap coordination signals; not a universal impossibility.
[8] Hosseini, H., Mandal, D., Shah, N., Shi, K. (2021). *Surprisingly Popular Voting Recovers Rankings, Surprisingly!* IJCAI-2021. arXiv:2105.09386. https://arxiv.org/abs/2105.09386 — **Boundary:** gains are experimental on ranking datasets; "a little prediction information helps" is measured, not proven.
[9] Brier, G.W. (1950). *Verification of Forecasts Expressed in Terms of Probability.* Monthly Weather Review 78(1):1–3. https://doi.org/10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2 — **Boundary:** defines the score; properness and decomposition results come later.
[10] Gneiting, T., Raftery, A.E. (2007). *Strictly Proper Scoring Rules, Prediction, and Estimation.* JASA 102(477):359–378. https://doi.org/10.1198/016214506000001437 — **Boundary:** properness concerns *expected* score under the reporter's own belief; it says nothing about collusion or identity duplication.
[11] Hanson, R. (2003). *Combinatorial Information Market Design.* Information Systems Frontiers 5(1):107–119. https://doi.org/10.1023/A:1022058209073 — **Boundary:** design paper with a worst-case subsidy bound, not a guarantee against manipulation by a capitalized bloc.
[12] Hanson, R. *Logarithmic Market Scoring Rules for Modular Combinatorial Information Aggregation.* Journal of Prediction Markets 1(1):3–15. https://doi.org/10.5750/jpm.v1i1.417 — **Boundary:** Crossref indexes the year as 2012 for a vol.1(1) article usually cited as 2007 — **year unverified**; cite by DOI. Thin-market manipulation is a known, here-unquantified weakness.
[13] Krogh, A., Vedelsby, J. (1995). *Neural Network Ensembles, Cross Validation, and Active Learning.* NIPS 7. https://proceedings.neurips.cc/paper_files/paper/1994/hash/b8c37e33defde51cf91e1e03e51657da-Abstract.html — **Boundary:** `E = Ē − Ā` is derived for **continuous-valued** ensemble outputs under squared loss; it licenses a diversity term by analogy, not as a theorem about categorical votes.
[14] Liu, Y., Yao, X. (1999). *Ensemble learning via negative correlation.* Neural Networks 12(10):1399–1404. https://doi.org/10.1016/S0893-6080(99)00073-8 — **Boundary:** the `λ` tradeoff is empirical on small regression/classification benchmarks; large `λ` degrades members.
[15] Mouret, J-B., Clune, J. (2015). *Illuminating search spaces by mapping elites.* arXiv:1504.04909. https://arxiv.org/abs/1504.04909 — **Boundary:** self-described "early draft"; results are neuroevolution and soft-robot design with hand-chosen behaviour dimensions.
[16] Auer, P., Cesa-Bianchi, N., Fischer, P. (2002). *Finite-time Analysis of the Multiarmed Bandit Problem.* Machine Learning 47:235–256. https://doi.org/10.1023/A:1013689704352 — **Boundary:** stochastic i.i.d. bandits; UCB's bonus rewards *uncertainty*, not disagreement, and carries no adversarial-corruption guarantee.
[17] Bellemare, M.G., Srinivasan, S., Ostrovski, G., Schaul, T., Saxton, D., Munos, R. (2016). *Unifying Count-Based Exploration and Intrinsic Motivation.* arXiv:1606.01868. https://arxiv.org/abs/1606.01868 — **Boundary:** Atari-2600 single-agent RL; pseudo-count quality depends entirely on the density model.
[18] Burda, Y., et al. (2018). *Exploration by Random Network Distillation.* arXiv:1810.12894. https://arxiv.org/abs/1810.12894 — **Boundary:** verified via the arXiv API listing only (title, id, 2018-10-30); abstract not re-read this session. Single-agent RL.
[19] Houthooft, R., et al. (2016). *VIME: Variational Information Maximizing Exploration.* arXiv:1605.09674. https://arxiv.org/abs/1605.09674 — **Boundary:** same — API-listing verification only; continuous-control RL.
[20] Yin, D., Chen, Y., Ramchandran, K., Bartlett, P. (2018). *Byzantine-Robust Distributed Learning: Towards Optimal Statistical Rates.* ICML 2018. arXiv:1803.01498. https://arxiv.org/abs/1803.01498 — **Boundary:** order-optimal rates for strongly convex losses; the guarantees are statistical-error bounds on gradient aggregation, not on categorical option choice.
[21] Blanchard, P., El Mhamdi, E.M., Guerraoui, R., Stainer, J. (2017). *Machine Learning with Adversaries: Byzantine Tolerant Gradient Descent.* NIPS 30. https://proceedings.neurips.cc/paper/2017/hash/f4b9ec30ad9f68f89b29639786cb62ef-Abstract.html — **Boundary:** proves no *linear-combination* aggregator tolerates one Byzantine input and that Krum converges; [22] shows convergence is not the whole safety property.
[22] El Mhamdi, E.M., Guerraoui, R., Rouault, S. (2018). *The Hidden Vulnerability of Distributed Learning in Byzantium.* ICML 2018. arXiv:1802.07927. https://arxiv.org/abs/1802.07927 — **Boundary:** the `Ω(√d)` → `O(1/√d)` leeway results are for high-dimensional non-convex SGD on MNIST/CIFAR-10; the transferable lesson is conceptual (resilience ≠ bounded displacement).
[23] Shejwalkar, V., Houmansadr, A., Kairouz, P., Ramage, D. (2022). *Back to the Drawing Board: A Critical Evaluation of Poisoning Attacks on Production Federated Learning.* IEEE S&P 2022. arXiv:2108.10241. https://arxiv.org/abs/2108.10241 — **Boundary:** read at abstract depth via the team-repo note `library/papers/shejwalkar-2022-back.md`; covers **untargeted** poisoning under production FL assumptions, so it does not bound targeted/tail corruption.
[24] Lamport, L., Shostak, R., Pease, M. (1982). *The Byzantine Generals Problem.* ACM TOPLAS 4(3):382–401. https://doi.org/10.1145/357172.357176 — **Boundary:** the `N ≥ 3f+1` bound assumes oral (unauthenticated) messages; signed messages relax it. It bounds *agreement*, not decision quality.
[25] Castro, M., Liskov, B. (2002). *Practical Byzantine fault tolerance and proactive recovery.* ACM TOCS 20(4):398–461. https://doi.org/10.1145/571637.571640 — **Boundary:** the canonical OSDI'99 paper has no DOI; this is the journal version. It guarantees safety/liveness of replication, nothing about whether the agreed value is *true*.
[26] Douceur, J.R. (2002). *The Sybil Attack.* IPTPS 2002, LNCS 2429:251–260. https://doi.org/10.1007/3-540-45748-8_24 — **Boundary:** the impossibility is relative to the absence of a trusted certifying authority; it is an argument, not an experiment.
[27] Yu, H., Kaminsky, M., Gibbons, P.B., Flaxman, A. (2006). *SybilGuard: Defending Against Sybil Attacks via Social Networks.* SIGCOMM. https://doi.org/10.1145/1159913.1159945 — **Boundary:** the bound rests on fast-mixing social graphs and a small honest/Sybil cut; no analogue of that graph exists for an agent swarm unless we build one.
[28] Dong, X.L., Berti-Équille, L., Srivastava, D. (2009). *Truth discovery and copying detection in a dynamic world.* PVLDB 2(1):562–573. https://doi.org/10.14778/1687627.1687691 — **Boundary:** copying detection is evaluated on structured web-data sources with update histories; applying it to retrieved web text is an extension we would have to validate ourselves.
[29] Satopää, V.A., Pemantle, R., Ungar, L.H. (2014/2015). *Modeling Probability Forecasts via Information Diversity.* arXiv:1406.2148. https://arxiv.org/abs/1406.2148 — **Boundary:** a parametric model of partially overlapping information among **human** forecasters; it gives the shape of the overlap→extremizing curve, not our constants.
[30] Bara, M. (2026). *Epistemic Sybil Resistance: Multiplying AI Agents Without Multiplying Evidence.* arXiv:2609.01873. https://arxiv.org/abs/2609.01873 · code https://github.com/marcbara/epistemic-sybil-resistance — **Boundary:** the headline numbers (coverage 0.940 → 0.263; `γ_cal = 0.719`; cluster-count shift 1.425, 95% CI [1.363, 1.485]) come from >20,000 LLM calls on **synthetic** evidentiary documents, single-author preprint, no venue stated. Treat the *direction* as well-supported and the constants as setting-specific.
[31] Seeley, T.D., Visscher, P.K., Schlegel, T., et al. (2012). *Stop Signals Provide Cross Inhibition in Collective Decision-Making by Honeybee Swarms.* Science 335(6064):108–111. https://doi.org/10.1126/science.1210361 — **Boundary:** *Apis mellifera* nest-site choice. The §7-C brake is an engineering analogy; nothing here transfers as a theorem about agent swarms.
[32] Schulz-Hardt, S., Jochims, M., Frey, D. (2002). *Productive conflict in group decision making: genuine and contrived dissent as strategies to counteract biased information seeking.* OBHDP 88(2):563–586. https://doi.org/10.1016/S0749-5978(02)00001-8 — **Boundary:** lab groups with self-report and information-search measures; the genuine > contrived ordering comes from these specific manipulations.
[33] Schulz-Hardt, S., Brodbeck, F.C., Mojzisch, A., et al. (2006). *Group decision making in hidden profile situations: Dissent as a facilitator for decision quality.* JPSP 91(6):1080–1093. https://doi.org/10.1037/0022-3514.91.6.1080 — **Boundary:** the hidden-profile lab paradigm; the effect is on decision quality *in that paradigm*, with the usual student-sample caveats.
[34] Schwenk, C.R. (1990). *Effects of devil's advocacy and dialectical inquiry on decision making: A meta-analysis.* OBHDP 47(1):161–176. https://doi.org/10.1016/0749-5978(90)90051-A — **Boundary:** a 1990 meta-analysis over a small, heterogeneous study set; effects are modest and technique-sensitive.
[35] Greitemeyer, T., Schulz-Hardt, S., Frey, D. (2009). *The effects of authentic and contrived dissent on escalation of commitment in group decision making.* EJSP 39(4):639–647. https://doi.org/10.1002/ejsp.578 — **Boundary:** the negative half of the dissent story — contrived dissent did not reliably cure escalation.
[36] Qiu, T.A., Carroll, M., Allen, C. (2026). *Truthfulness Despite Weak Supervision: Evaluating and Training LLMs Using Peer Prediction.* ICLR 2026. arXiv:2601.20299. https://arxiv.org/abs/2601.20299 — **Boundary:** evaluated up to 405B on their task suite; "inverse scaling in resistance to deception" is their measured finding in that setup, not a general law.
[37] Mytsyk, S., Zhang, Y., Krishnamurthy, V. (2026). *Mitigating LLM sycophancy with RL-based fine-tuning: Bayesian Truth Serum approach.* arXiv:2608.25267. https://arxiv.org/abs/2608.25267 — **Boundary:** the 23% → 4% flip-rate and 80% → 93% accuracy figures are single-model, single-setup; the collusion-resistance claim is asymptotic ("large-group"), and the paper itself calls the method computationally expensive.
[38] Cui, Y., Du, H. (2025). *MAD-Spear: A Conformity-Driven Prompt Injection Attack on Multi-Agent Debate Systems.* arXiv:2507.13038. https://arxiv.org/abs/2507.13038 — **Boundary:** five benchmark datasets under a compromise-a-subset (insider) threat model, not the outside content-injector of our scenario; the diversity-helps finding is theirs and contradicts some prior work.
[39] YS, Y. (2026). *Everyone Conforms, No One Believes: Pluralistic Ignorance in LLM Agent Populations.* arXiv:2608.02758. https://arxiv.org/abs/2608.02758 — **Boundary:** 100 synthetic scenarios × 10 domains × 5 authority levels, 8 models, single author, no venue stated; the 64–94% public-conformity range is scenario-construction-dependent.
[40] Zhu, X., Zhang, C., Chi, Y., Stafford, T., Collier, N., Vlachos, A. (2026). *Demystifying Multi-Agent Debate: The Role of Confidence and Diversity.* arXiv:2601.19921. https://arxiv.org/abs/2601.19921 — **Boundary:** the "debate preserves expected correctness" result holds *under homogeneous agents and uniform belief updates*; empirical gains are on six reasoning-oriented QA benchmarks.
[41] Wynn, A., Satija, H., Hadfield, G. (2025). *Talk Isn't Always Cheap: Understanding Failure Modes in Multi-Agent Debate.* ICML MAS Workshop 2025. arXiv:2509.05396. https://arxiv.org/abs/2509.05396 — **Boundary:** workshop paper; the accuracy-decrease finding is on their model mixes and tasks, and is our cited evidence that unincentivized debate can hurt.
[42] Kaesberg, L.B., Becker, J., Wahle, J.P., Ruas, T., Gipp, B. (2025). *Voting or Consensus? Decision-Making in Multi-Agent Debate.* ACL 2025 Findings. arXiv:2502.19130. https://arxiv.org/abs/2502.19130 — **Boundary:** +13.2% / +2.8% / +3.3% / +7.4% are relative to *other decision protocols* in their one-variable-at-a-time design, not to a single fixed baseline.
[43] Zhang, J., Xu, X., Zhang, N., Liu, R., Hooi, B., Deng, S. (2024). *Exploring Collaboration Mechanisms for LLM Agents: A Social Psychology View.* ACL 2024. arXiv:2310.02124. https://arxiv.org/abs/2310.02124 — **Boundary:** four constructed "societies", two traits, two thinking patterns, three benchmarks; the conformity finding is an observed analogy to social-psychology theory, not a mechanistic account.
[44] Choi, M., Kim, K., Chae, S., Baek, S. (2025). *An Empirical Study of Group Conformity in Multi-Agent Systems.* ACL 2025 Findings. arXiv:2506.01332. https://arxiv.org/abs/2506.01332 — **Boundary:** >2,500 simulated debates on five *socially contentious* topics — opinion dynamics, not verifiable-truth tasks, so transfer to provider choice is an assumption.
[45] Wang, Y., Yan, Q., Xing, Z., et al. (2025). *Silence is Not Consensus: Disrupting Agreement Bias in Multi-Agent LLMs via Catfish Agent for Clinical Decision Making.* arXiv:2505.21503. https://arxiv.org/abs/2505.21503 — **Boundary:** clinical QA/VQA domain; "consistent improvements" are reported without a dissent-cost accounting, which is the gap our token-charged design closes.
[46] Mehdizadeh, A., Hilbert, M. (2025). *When Your AI Agent Succumbs to Peer-Pressure: Studying Opinion-Change Dynamics of LLMs.* arXiv:2510.19107. https://arxiv.org/abs/2510.19107 — **Boundary:** two named models carry the threshold claims (>70% vs a dissenting minority); opinion/values topics, not factual-accuracy tasks.
[47] Ma, H., Zou, H.P., Li, C., Ma, E., Su, Y., Yu, P.S. (2026). *Sycophancy Suppression Can Impair Rational Updating: Anti-Sycophancy Should Preserve the Ability to Update.* EMNLP 2026 Findings. arXiv:2608.26511. https://arxiv.org/abs/2608.26511 — **Boundary:** a two-turn evaluation framework; the mechanistic evidence (shared MLP neurons / attention heads) is correlational, and the orthogonalized-steering fix is explicitly "preliminary" and architecture-dependent.
[48] Douven, I. (2026). *Wisdom of LLM Crowds: Aggregation and Contamination in Language Model Ensembles.* arXiv:2607.18269. https://arxiv.org/abs/2607.18269 — **Boundary:** 15 models × 254 binary market questions, single author; the disagreement-signal finding comes from symbolic regression on a learned mapping (suggestive, not causal), and the paper's own result is that contamination dominates naive comparisons.
[49] Hegazy, M. (2024). *Diversity of Thought Elicits Stronger Reasoning Capabilities in Multi-Agent Debate Frameworks.* arXiv:2410.12853. https://arxiv.org/abs/2410.12853 — **Boundary:** the 91%/82% GSM-8K and 94% ASDiv figures are single-author results on a now-dated model mix in a low-profile venue; directional only.
[50] Xia, Y., Wang, T. (2026). *When Should Agent Trust Be Conditional? Characterizing and Attacking Skill-Conditional Reputation in Agent Swarms.* arXiv:2606.14200. https://arxiv.org/abs/2606.14200 — **Boundary:** 14 AppWorld agents plus a phase-diagram analysis; the authors explicitly state they do **not** claim Sybil resistance, only a quantified trade-off. Use it as the reason to keep learned reputation out of v1.
[51] List, C., Elsholtz, C., Seeley, T.D. (2009). *Independence and interdependence in collective decision making: an agent-based model of nest-site choice by honeybee swarms.* Phil. Trans. R. Soc. B 364(1518):755–762. https://doi.org/10.1098/rstb.2008.0277 — **Boundary:** an agent-based *model* of bees; the independence/interdependence balance it characterizes is the conceptual parent of §7-C's `N_eff`, not a validated engineering result.
[52] Cobbe, K., Kosaraju, V., Bavarian, M., et al. (2021). *Training Verifiers to Solve Math Word Problems.* arXiv:2110.14168. https://arxiv.org/abs/2110.14168 — **Boundary:** the abstract states verification "significantly improves performance" and reports **no numeric figure**, so any specific uplift number for verifier reranking is **unverified** here; GSM8K only, single-agent, not multi-agent voting.

## 10. Not found / could not verify

- **Semantic Scholar** returned HTTP 429 on every batched query and on 3 of 4 paced queries; only the Dasgupta–Ghosh record came back. All citation counts are therefore **unverified** and none are quoted anywhere above.
- **Hanson LMSR year** — Crossref indexes J. Prediction Markets 1(1):3–15 under 2012; the article is commonly cited as 2007. Year **unverified**; cite by DOI [12].
- **Du et al. 2023, "Improving Factuality and Reasoning in Language Models through Multiagent Debate"** (arXiv:2305.14325) and **Lightman et al. 2023, "Let's Verify Step by Step"** (arXiv:2305.20050) are relevant and are carried in our prior note, but were **not re-fetched this session** (arXiv API 429). Deliberately left unnumbered rather than cited unverified.
- Queries that returned nothing usable: `peer prediction AND collusion` (arXiv, 0 hits — the collusion-resistance literature sits in EC/journal venues, reached here via [5][7]); `weighted majority voting AND verifier` (3 hits, all test-time-scaling process-reward-model papers, none about *dissent*-weighted voting); `cross-inhibition AND collective decision` on arXiv (0 — that literature is in Science / Phil. Trans. R. Soc. B, reached via Crossref as [31][51]).
- **No source found that directly measures a dissent-reward mechanism in an LLM swarm under an external content-injection threat model.** [38] is the nearest on the attack side (insider compromise, no incentive term); [36][37] are the nearest on the incentive side (no swarm, no injector). That gap is the proposal's claim to novelty and should be stated that way, not as "no prior work exists".
