---
id: llm-agent-swarms--dmarz
type: review
target: llm-agent-swarms
reviewer: dmarz/reviewer-1
verdict: revise
date: 2026-10-03
---

## Checklist

- [x] Spot-checked at least 5 cited entries: the source exists at the url and says what the entry claims.
- [x] Ran my own 3 searches with different wording; list any relevant work the target missed below.
- [ ] Seminal works are right, and their forward citations were followed.
- [ ] Claims are cited; measured results are separated from inference.
- [ ] (hypothesis) The novelty section survives the closest prior work.
- [ ] (experiment) Protocol and metrics were fixed before results.

Why two boxes are unticked. Seminal works: the five seeds are a reasonable choice, but I did not re-run their
forward-citation chases (OpenAlex was over its daily quota from this machine all session). I only checked the
seven uncatalogued forward-citation items from the Gaps section, and three of them matter (see Notes, part C).
Claims and inference: I checked this and it fails in three places. "What is known" is headed "replicated
across at least two independent groups", but some bullets under it rest on one group, and two bullets cite
[[flint-2026-group]] for things that paper does not show (Notes, part A).

## Spot-check record

I checked ten entries against the source, opening arXiv abs/HTML or the GitHub API and README on
2026-10-03. Title, authors, ids and dates matched in all ten. Three had problems in how the survey uses them.

| Entry | Source opened | Metadata | Survey's claim vs source |
|---|---|---|---|
| [[de-marzo-2024-ai]] | arXiv abs + HTML 2409.02822; journal ref Sci. Adv. 12, eaea6091 | OK | OK. N_c values match. The source says the GPT-4 Turbo N_c ~ 1000 rests on 1 realisation at N = 1000, and the survey states it without that caveat. |
| [[pavlova-2026-flag]] | arXiv abs + HTML 2609.19124 | OK | Small error. The survey says wrong consensus is "0% at N >= 32". Table 3 gives 0.0-5.3% at N = 64, so it is 0% only at N = 32 and 128. Other numbers OK: N = 16 peak, +40 to ~+17 points from patching, mixed teams best (N = 8 broadcast). No code URL in the paper. |
| [[bertalanic-2026-ringelmann]] | arXiv abs 2606.02646 | OK | OK (R(N) law, 44 conditions, R^2 > 0.99, re-evaluation not peer interaction, only heterogeneity lowers c). |
| [[yang-2026-when]] | arXiv abs 2606.22203 | OK | OK (gamma 0.15-0.43, paraphrase-invariant, no spontaneous backfire, pairwise gamma does not predict multi-neighbour). |
| [[wu-2026-how]] | arXiv abs 2609.30028 (v2, 29 Sep) | OK | OK as stated. The entry was read at abstract depth only, so no task, N or model detail stands behind the "unlike humans" contrast. |
| [[de-marzo-2026-copying]] | arXiv abs 2609.09150 | OK | OK. One episode, one agent family. |
| [[magistrali-2026-aligned]] | arXiv abs 2608.22444 | OK | OK: "capture is a temporary state". Abstract-only read. |
| [[de-marzo-2026-conformity]] | arXiv abs 2605.10721 | OK | OK: "irreversibly shift ... even after manipulation ceases". Abstract-only read. |
| [[flint-2026-group]] | arXiv HTML 2510.22422 | OK | **Misused twice.** (1) In "What is known" bullet 2 it is cited as evidence that coupling falls with N, so that above N_c "consensus is slow or impossible". In Flint et al., N_c is the size above which the outcome becomes *deterministic* (always the strong word), so a larger N gives more predictable consensus, not less. That is the opposite direction from the De Marzo N_c. (2) In Open problems ("[[de-marzo-2026-conformity]] and [[flint-2026-group]] say shifts persist"), the paper has no committed minority and no agents are removed, so it says nothing about persistence. |
| [[gh-killy-netsphere-sealed-swarm-transcripts]] | GitHub API + README | OK (CC0, 0 stars, pushed 2026-09-20) | OK, though the "66 lives vs zero" result is from one arm ("the clearest arm"), by a single anonymous author, and has no paper. |

## Missed work

Already in the library, on topic, not cited. The first six affect claims or gaps:

- [[fukushima-2026-message]]: message capacity (how many inbox messages an agent reads) sets the transitions of collective truth-finding with a ground truth. The theory built from measured weights predicted wrong consensus would be unreachable below 6.4 of 31 sources, and it failed: the correct side won only 28-45% of episodes even when 75% of agents started correct. The cause is a claim-wording "field" set before any message is read (verified on arXiv 2609.19183). This bears directly on Gap 1 (bounded reading of broadcast with ground truth), on Gap 2 and the "social or memorised" problem (wording reversal is a prior-artefact control), and on "What is known" bullet 1: the mean-field fit is not enough without a per-item field.
- [[zhang-2026-silo]] (Silo-Bench, ACL 2026): an evidence-distributed task (sharded inputs) with N = 2-100 agents. The Communication-Reasoning Gap widens with N, and coordination overhead cancels the parallelisation gain. This partly answers the open problem "Does the Ringelmann ceiling hold off benchmark QA?". It also weakens Gap 4 as written: N_eff itself has not been computed on such a task, but the qualitative question has been tested.
- [[berdoz-2026-can]]: Byzantine scalar consensus with no stake. Valid agreement is unreliable even with no Byzantine agents and degrades as groups grow, mostly through loss of liveness. This is an independent (ETH) measurement for "What is known" bullet 2 and should replace [[flint-2026-group]] there.
- Correlated-error / effective-N literature. These are independent groups that support "More homogeneous agents add agreement, not evidence", which now rests mostly on [[bertalanic-2026-ringelmann]]: [[kim-2025-correlated]] (agreement-when-both-wrong roughly 2x baseline across 349 models), [[denisov-blanch-2026-consensus]] (polling aggregation gives no truthfulness gain at 25x cost), [[chen-2026-when]] (co-failure ceiling 1 - beta), [[li-2026-state]] (correlated errors put a floor under majority-vote error), and [[bara-2026-epistemic]], which derives the same Kish-style discount m/[1 + rho(m - 1)] as Bertalanic and Fortuna, independently, and measures coverage collapse from 0.940 to 0.263 as same-root reports go from 1 to 32. [[goel-2025-great]] (errors grow more similar with capability) is relevant to the cross-family lever.
- [[brockers-2025-disentangling]]: a Bayesian separation of genuine interaction from topic, agreement and anchoring biases in LLM opinion dynamics. This is a second validity diagnostic beside [[yang-2026-when]], and it belongs in "Is emergent consensus social or memorised?".
- [[chuang-2023-simulating]]: the canonical LLM opinion-dynamics-on-networks paper, and the case [[yang-2026-when]] applies its diagnostic to. Missing from the physics-of-agents landscape.
- Worth adding to the landscape: [[bate-2026-indecision]] (a non-LLM evidence-accumulation model where per-agent accuracy peaks at a finite group size; this is the null model for the Flag Game's non-monotonic N), [[riedl-2025-emergent]] (information-theoretic synergy; already referenced from [[de-marzo-2024-ai]]), [[celiktemel-2026-group]] (prompt cultural evolution, measured phase transition), [[pal-2026-swarmworld]] (stigmergy: reuse comes from observing artefacts rather than messages, relevant to boards with persistence), [[wang-2025-rethinking]] (small-world topology stabilises debate consensus), [[wang-2025-decoding]] (LLM echo chambers vs BCM/FJ), [[kraidia-2026-when]], [[liu-2025-can]] and [[liu-2026-consensus]] (one persuasive or adversarial agent moves the group, which belongs beside the committed-minority bullet), and [[perez-2024-cultural]].

Not in the library (found in my searches, opened at the source on 2026-10-03):

- Liu, K., Xiong, G., Zhang, W., & Tang, S. (2026). Social Networks of LLM Agents. arXiv:2607.03695. Narrow attention causes herding: the effective sample size stays bounded whatever the population size. Wide attention recovers wisdom of crowds only on undirected, degree-regular exposure graphs. **Load-bearing**: an independent effective-N result with a stated escape condition, which bears on the logistic-vs-ceiling open problem. This is listed in Gaps as "uncatalogued", but it should be catalogued.
- Itkin, I. (2026). Local Predictability and Collective Fidelity in LLM-Agent Societies. arXiv:2609.35813. 9,455 published trajectories. Neighbour information improves individual prediction in all 16 settings, but collective gains depend on transfer conditions, and **earlier history effects failed to replicate on 24 new statements**. **Load-bearing**: same author as [[itkin-2026-poor]]. It qualifies the surrogate trick the survey recommends (and that [[flint-2026-group]]'s N ~ 10^4 relies on), and it is a reported non-replication inside this literature.
- Li, M., Li, X., & Zhou, T. (2026). Does Socialization Emerge in AI Agent Society? A Case Study of Moltbook. arXiv:2602.14299; ACM Conference on AI (2026), doi:10.1145/3786335.3813123. Agents show "strong individual inertia and minimal adaptive response to interaction partners, preventing mutual influence", and no consensus emerges. **Load-bearing**: this is counter-evidence to the generalisation in "What is known" bullet 8 ("in the wild, agents copy what they can see"). That bullet rests on one wiki episode and one anonymous reproduction.
- Usman, R. M., & Williamson, D. (2026). Peer-Voted LLM-Agent Stress Tests Find Feed-Induced Lexical Convergence but No Reliable Matched-Exposure Advantage for Distributed Sources. arXiv:2608.20438. Preregistered, 448 trials: feeds produce lexical convergence (TF-IDF cosine +0.008 to 0.011), but more sources do not reliably move stance. This supports splitting bullet 8 into wording copying (replicated) and belief copying (contested).
- Hashemi, F., & Macy, M. W. (2026). An Empirical Study of Collective Behaviors and Social Dynamics in Large Language Model Agents. arXiv:2602.03775 (EACL 2026). Chirper.ai: 7M posts, 32K agents, one year, with homophily, social influence and ideological polarisation. This contradicts the Gaps claim that the AI Village is "the only longitudinal multi-model population". Reword that, or say what makes the Village unique (human perturbation, task orientation).
- Hou, W., & Ji, Z. (2026). Structural Divergence Between the Moltbook AI-Agent Network and Human Social Networks. Advanced Science, doi:10.1002/advs.77665 (abstract read via Crossref). Network structure only, with extreme attention inequality and suppressed reciprocity. Not load-bearing.
- Priyanshu, A., Vijay, S., & Pahwa, E. (2026). Does Safety Molt? Evaluating LLM Safety in Multi-Agent Social Environments. ACM Conference on AI, doi:10.1145/3786335.3813173. The Crossref record has no abstract, and arXiv search returned nothing. Safety-focused. Probably not load-bearing; not assessed beyond metadata.
- Altunyan, A., & Edelman, S. (2026). Tipping Points in LLM-Based Multi-Agent Systems: Stance on Climate Change Action. arXiv:2609.25432. Reports abrupt stance shifts and names LLM-prior interference as a control problem. Adds one tipping datum; not load-bearing.
- Choudhary, V. (2026). Manipulation Without Manipulators: Amplification Dynamics Emerge in Autonomous Agent Collectives in Moltbook. SSRN, doi:10.2139/ssrn.6175219. 22,000 agents. Engagement is set by early first comments, which matches the "whoever writes first sets the convention" reading of [[de-marzo-2026-copying]].
- Liu, Y. (2026). Do LLM Agents Form Echo Chambers? A Replication of Shore et al. (2018) on an AI Social Platform. SSRN, doi:10.2139/ssrn.6984844. On Moltbook the population mainstreams, and the core does not polarise under the visibility definition.
- Brach et al. (2026). The Moltbook Files: A Harmless Slopocalypse or Humanity's Last Experiment. arXiv:2605.07462. 232K posts (search-listing gist only; not opened).

## Notes

**Verdict: revise.** The survey is broad, well organised and mostly accurate at the metadata level: all ten
spot-checked entries are real and correctly described. It goes to revise for three reasons. Two bullets in
"What is known" cite [[flint-2026-group]] for claims that paper does not make. Several bullets under the
"replicated across two independent groups" heading rest on one group. And three works the author marked as
"none changes the picture" do change it (Li et al. on Moltbook, Itkin 2609.35813, Liu et al. 2607.03695),
along with [[fukushima-2026-message]] and [[zhang-2026-silo]] already in the library. Each fix below is
small; none of them overturns the survey's main framing.

**A. Factual fixes in load-bearing claims.**

1. Bullet 2 ("coupling falls with group size ... consensus slow or impossible"). Remove [[flint-2026-group]] (its N_c marks where consensus becomes *deterministic*). Also note that [[qian-2025-scaling]] (task quality saturates) and [[grotschla-2025-agentsnet]] (performance on graph problems) measure different quantities from the majority-force beta. As written, the bullet merges three different "critical N" notions into one claim. Keep the beta(N) claim on [[de-marzo-2024-ai]] (with the caveat that GPT-4 Turbo's N_c rests on one N = 1000 run), add [[berdoz-2026-can]] as the independent support, and move Qian and AgentsNet to the logistic-vs-ceiling problem where they belong.
2. Open problem "Reversible or absorbing capture?". Drop [[flint-2026-group]]. The disagreement is [[magistrali-2026-aligned]] vs [[de-marzo-2026-conformity]], and both were read at abstract depth only. Say so, and read at least the methods of both before the hackathon builds a hypothesis on this contrast, since it is Gap 3.
3. Bullet 4 (Flag Game numbers). Change "0% at N >= 32" to "0% at N = 32 and 128 (0-5.3% at N = 64)". More importantly, this bullet is one group: [[tanaka-2026-when]] is by Hidenori Tanaka, co-author of [[pavlova-2026-flag]], so it is a model from the same group, not a replication. The survey's own "Measured once" paragraph lists "the Flag Game numbers", which contradicts placing the bullet under "replicated". Move it, or add [[bate-2026-indecision]] as an independent (non-LLM) model of the same peak-at-finite-N shape and say what is and is not replicated.

**B. Single-source claims presented as replicated.**

4. Bullet 7 ("Conformity ... follows Social Impact Theory"). The SIT fit is from [[bellina-2026-conformity]] alone (De Marzo and Garcia group). The other citations show conformity, not SIT scaling. Split the bullet into "LLM agents conform to confederates, more than humans do for minorities" (replicated) and "the dependence follows SIT" (one group). [[wu-2026-how]] is abstract-depth only; flag that.
5. Bullet 8 ("In the wild, agents copy what they can see"). The evidence is one observational paper on one episode with one agent family, plus one single-author, zero-star GitHub reproduction. Li et al. 2602.14299 (Moltbook: minimal mutual influence) and Usman and Williamson 2608.20438 (lexical convergence without stance change) suggest the honest claim is narrower. Short-lived agents copy *wording and conventions* from what is on screen. Whether they copy *beliefs* is contested.
6. Diversity as "the only lever consistently found to help" (bullet 5) is overstated by the survey's own source: [[pavlova-2026-flag]] reports that social-awareness prompting raises terminal truth mass from 0.54 to 0.81 in broadcast. Soften to "the most consistent lever" and cite the correlated-error papers (Missed work) as independent support for the homogeneity ceiling.
7. Bullet 1: add [[fukushima-2026-message]] as a qualifier. A logistic/Ising update rule fitted on measured weights mispredicted outcomes until a per-claim wording field was added. "Well described by mean-field Ising" needs "given a per-item field".

**C. Gaps and the seven uncatalogued items.**

8. Three of the seven are load-bearing and should be catalogued before any hypothesis is filed: Liu et al. 2607.03695 (bounded effective N under narrow attention, with a stated escape condition; this is the closest prior for any N_eff-on-a-board hypothesis), Itkin 2609.35813 (a non-replication that bears on the surrogate method in "Code, data and tools"), and Li et al. 2602.14299 (counter-evidence to bullet 8). Hashemi and Macy (Chirper.ai) should be catalogued to fix the "only longitudinal population" wording. Hou and Ji, "Does Safety Molt" and Altunyan and Edelman are not load-bearing. Change the sentence "none changes the picture above" accordingly.
9. Gap 1 (board N-sweep with ground truth) stays open, but should cite [[fukushima-2026-message]] (bounded reading of an inbox, ground truth, transitions in reading capacity) and [[zhang-2026-silo]] (N up to 100, distributed evidence) as the closest prior.
10. Gap 4 (N_eff on evidence-distributed tasks) stays open for N_eff itself. Reword it to say that [[zhang-2026-silo]] already shows the qualitative overhead-cancels-gain result on distributed evidence, and Liu et al. 2607.03695 gives a theoretical bound, so a new measurement must compute N_eff and the placebo to be novel.
11. Gap 2 (randomised-initial-condition diagnostic plus tipping) stays open. Cite [[brockers-2025-disentangling]] as a second diagnostic, and note Altunyan and Edelman flag prior interference in a tipping study without (per the abstract) a formal diagnostic.

**D. Smaller items.**

12. Saturation: the claim that the Ringelmann/bystander rounds "returned only entries already catalogued" holds for that vocabulary, but the correlated-errors / ensemble-aggregation vocabulary (catalogued under dmarz's fm-bft-aggregation scan) was not searched and holds six on-topic papers. Add one search round with that wording.
13. The search log reports 96 distinct cited ids, not "about 60" as the task says. That is fine, but several load-bearing cites are abstract-depth ([[wu-2026-how]], [[magistrali-2026-aligned]], [[de-marzo-2026-conformity]], [[zhou-2025-pimmur]], [[ricco-2026-consensus]]). Mark depth inline where a claim rests on one of them.
14. My searches: Crossref (3 queries: "large language model agents echo chamber polarization simulation", "LLM agents committed minority tipping point social convention", "multi-agent large language model group size consensus scaling", plus title lookups), and arXiv listing search (2 queries: "LLM agents herding wisdom of crowds" and "language model agents voter model / opinion dynamics population size", newest first). OpenAlex returned "insufficient budget" for every request, and the WebSearch budget for this session was already spent. The arXiv opinion-dynamics listing of 25 recent hits held 5 already catalogued and about 4 on-topic misses, which is consistent with the survey being close to, but not at, saturation.
