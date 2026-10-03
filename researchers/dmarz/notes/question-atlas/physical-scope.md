# Physical-systems question bank: scope and reading notes

Status: **human-requested, unreviewed hunches for selection**. The 38 entries in `physical.json` are not formal hypotheses, accepted protocols, gate-passed surveys, or claims of novelty. They do not authorize experiments. No simulations, training, hardware trials or dataset analyses were run in this pass.

The user asked for many questions, related hypotheses and possible tests across the research areas, followed by human selection. This pass supplies six candidates each for collective motion, collective decisions, active matter, synchronization/consensus and crowds/traffic, plus eight for swarm robotics. The final two are learned-NCA computational analogues grouped with local robot computation; neither is a physical robot result. Each item records a concrete intervention or data comparison, the independent unit, an appropriate baseline, possible failure of the prediction, likely confounds, and two or three existing library anchors. Tags describe a provisional relationship to known work; an extension tag does not establish that the extension is unstudied.

## What was inspected

Read `AGENTS.md`, `library/README.md`, `researchers/dmarz/README.md`, the current inbox and topic counts in `STATUS.md`, and `researchers/vishesh/notes/project-briefs/nca-observatory.md`. Used the six topic catalogues to locate foundational and recent work, then inspected selected local record summaries, model descriptions, limitations and code/data notes. The lists below, together with the NCA addendum, name records used by the final bank. It is not a claim to have read all papers in those topic catalogues, and none of the original catalogue read-depth claims was changed or adopted as this agent's own reading depth.

### collective-motion

- [[amichay-2024-revealing]] — `library/papers/amichay-2024-revealing.md`
- [[amichay-2025-integration]] — `library/papers/amichay-2025-integration.md`
- [[attanasi-2014-information]] — `library/papers/attanasi-2014-information.md`
- [[ballerini-2008-interaction]] — `library/papers/ballerini-2008-interaction.md`
- [[bastien-2020-model]] — `library/papers/bastien-2020-model.md`
- [[choi-2026-communication]] — `library/papers/choi-2026-communication.md`
- [[couzin-2005-effective]] — `library/papers/couzin-2005-effective.md`
- [[hang-2026-self]] — `library/papers/hang-2026-self.md`
- [[mateo-2017-effect]] — `library/papers/mateo-2017-effect.md`
- [[strandburg-peshkin-2013-visual]] — `library/papers/strandburg-peshkin-2013-visual.md`
- [[vicsek-1995-novel]] — `library/papers/vicsek-1995-novel.md`
- [[wang-2025-collective]] — `library/papers/wang-2025-collective.md`

### collective-decision

- [[couzin-2005-effective]] — `library/papers/couzin-2005-effective.md`
- [[kao-2014-decision]] — `library/papers/kao-2014-decision.md`
- [[leonard-2012-decision]] — `library/papers/leonard-2012-decision.md`
- [[leonard-2024-fast]] — `library/papers/leonard-2024-fast.md`
- [[march-pons-2024-honeybee]] — `library/papers/march-pons-2024-honeybee.md`
- [[pais-2013-mechanism]] — `library/papers/pais-2013-mechanism.md`
- [[reina-2017-model]] — `library/papers/reina-2017-model.md`
- [[seeley-2012-stop]] — `library/papers/seeley-2012-stop.md`
- [[talamali-2021-when]] — `library/papers/talamali-2021-when.md`
- [[valentini-2017-best]] — `library/papers/valentini-2017-best.md`

### active-matter

- [[alert-2022-active]] — `library/papers/alert-2022-active.md`
- [[bauerle-2018-self]] — `library/papers/bauerle-2018-self.md`
- [[brambilla-2013-swarm]] — `library/papers/brambilla-2013-swarm.md`
- [[cates-2015-motility]] — `library/papers/cates-2015-motility.md`
- [[ceron-2023-diverse]] — `library/papers/ceron-2023-diverse.md`
- [[deblais-2018-boundaries]] — `library/papers/deblais-2018-boundaries.md`
- [[deseigne-2010-collective]] — `library/papers/deseigne-2010-collective.md`
- [[fily-2012-athermal]] — `library/papers/fily-2012-athermal.md`
- [[fruchart-2021-non]] — `library/papers/fruchart-2021-non.md`
- [[slavkov-2018-morphogenesis]] — `library/papers/slavkov-2018-morphogenesis.md`
- [[vicsek-1995-novel]] — `library/papers/vicsek-1995-novel.md`
- [[ziepke-2025-acoustic]] — `library/papers/ziepke-2025-acoustic.md`

### swarm-robotics

- [[berlinger-2021-implicit]] — `library/papers/berlinger-2021-implicit.md`
- [[choi-2026-communication]] — `library/papers/choi-2026-communication.md`
- [[gh-ilpincy-argos3]] — `library/code/gh-ilpincy-argos3.md`
- [[gh-jic-csb-kilombo]] — `library/code/gh-jic-csb-kilombo.md`
- [[gh-proroklab-vectorizedmultiagentsimulator]] — `library/code/gh-proroklab-vectorizedmultiagentsimulator.md`
- [[gil-2015-guaranteeing]] — `library/papers/gil-2015-guaranteeing.md`
- [[leblanc-2013-resilient]] — `library/papers/leblanc-2013-resilient.md`
- [[mallmann-trenn-2021-crowd]] — `library/papers/mallmann-trenn-2021-crowd.md`
- [[pickem-2017-robotarium]] — `library/papers/pickem-2017-robotarium.md`
- [[rubenstein-2014-programmable]] — `library/papers/rubenstein-2014-programmable.md`
- [[slavkov-2018-morphogenesis]] — `library/papers/slavkov-2018-morphogenesis.md`
- [[sun-2023-mean]] — `library/papers/sun-2023-mean.md`
- [[zhang-2025-learning]] — `library/papers/zhang-2025-learning.md`

### sync-consensus

- [[amichay-2025-integration]] — `library/papers/amichay-2025-integration.md`
- [[ceron-2023-diverse]] — `library/papers/ceron-2023-diverse.md`
- [[dorfler-2014-synchronization]] — `library/papers/dorfler-2014-synchronization.md`
- [[fujiwara-2011-synchronization]] — `library/papers/fujiwara-2011-synchronization.md`
- [[gh-khev-swarmalators]] — `library/code/gh-khev-swarmalators.md`
- [[jadbabaie-2003-coordination]] — `library/papers/jadbabaie-2003-coordination.md`
- [[olfati-saber-2004-consensus]] — `library/papers/olfati-saber-2004-consensus.md`
- [[olfati-saber-2007-consensus]] — `library/papers/olfati-saber-2007-consensus.md`
- [[ren-2005-consensus]] — `library/papers/ren-2005-consensus.md`
- [[sarfati-2021-self]] — `library/papers/sarfati-2021-self.md`
- [[yoon-2022-sync]] — `library/papers/yoon-2022-sync.md`

### crowds-and-traffic

- [[bacik-2025-order]] — `library/papers/bacik-2025-order.md`
- [[data-juelich-crowd-2019]] — `library/datasets/data-juelich-crowd-2019.md`
- [[deblais-2018-boundaries]] — `library/papers/deblais-2018-boundaries.md`
- [[fruchart-2021-non]] — `library/papers/fruchart-2021-non.md`
- [[gh-pedestriandynamics-jupedsim]] — `library/code/gh-pedestriandynamics-jupedsim.md`
- [[gu-2025-emergence]] — `library/papers/gu-2025-emergence.md`
- [[helbing-1995-social]] — `library/papers/helbing-1995-social.md`
- [[karamouzas-2014-universal]] — `library/papers/karamouzas-2014-universal.md`
- [[moussaid-2011-simple]] — `library/papers/moussaid-2011-simple.md`
- [[murakami-2021-mutual]] — `library/papers/murakami-2021-mutual.md`
- [[poissonnier-2019-experimental]] — `library/papers/poissonnier-2019-experimental.md`
- [[seyfried-2009-new]] — `library/papers/seyfried-2009-new.md`
- [[stern-2018-dissipation]] — `library/papers/stern-2018-dissipation.md`
- [[sugiyama-2008-traffic]] — `library/papers/sugiyama-2008-traffic.md`

## Primary-source spot checks

These are bounded spot checks of load-bearing framing, mostly the abstracts. They are not full-paper reads. Publisher-access failures remain failures; the associated hunches rely on the existing catalogue and explicitly require deeper checking before promotion.

- [Poel et al., Subcritical escape waves in schooling fish](https://arxiv.org/abs/2108.05537): abstract checked for the context-dependent cost/benefit of responsiveness. This topic was left to the parent bank to avoid duplication.
- [Yoon et al., Sync and swarm](https://arxiv.org/abs/2203.10191): abstract checked for multiple collective states and existence conditions. The Lorentzian and ring-model details used in PHY-29 came from the local record; original methods still need inspection.
- [Gu et al., Emergence of collective oscillations in massive human crowds](https://www.nature.com/articles/s41586-024-08514-6): abstract and selected opening results checked. Observed chiral motion, the mechanical interpretation and proposed monitoring are different evidence levels. PHY-34 is a model replication and geometry test, not a safety claim.
- [Ziepke et al., Acoustic signaling enables collective perception and control in active matter systems](https://arxiv.org/abs/2410.02940): abstract checked for acoustic coupling, morphology, regeneration and proposed applications. No physical microrobot realization was established by this read.
- [Zhang et al., Back to Newton's Laws](https://arxiv.org/abs/2407.10648): abstract checked for differentiable-physics navigation and communication-free coordination framing; published 2025 record has a shorter title. Exact controller, training and deployment stack still need inspection.
- [Mallmann-Trenn et al., Crowd Vetting](https://arxiv.org/abs/2012.06291): primary abstract page opened to anchor the physical identity-vetting topic; guarantee assumptions in PHY-22 remain drawn from the catalogue and require an original-proof read.
- [Reina et al., Model of the best-of-N nest-site selection process in honeybees](https://arxiv.org/abs/1611.07575): primary abstract page opened for the multi-option model. Stochastic reimplementation remains a prerequisite, not completed work.
- [Stern et al., Dissipation of stop-and-go waves](https://arxiv.org/abs/1705.01693): abstract checked for the controlled ring-road intervention; no claim that the same benefit is established on an open road.
- Talamali's [constrained-communication paper](https://doi.org/10.1126/scirobotics.abf1416) returned 403. Bacik's [multidirectional-crowd paper](https://doi.org/10.1073/pnas.2420697122) was inaccessible through the web tool. Poissonnier's [ant-traffic article](https://pmc.ncbi.nlm.nih.gov/articles/PMC6805160/) returned an access challenge. Their local entries were read; their full original texts were not verified in this pass.

## Practical cautions for human selection

- Most candidates can begin with inexpensive scripted simulations; PHY-20 and PHY-21 may require training. PHY-36 depends on suitable bottleneck data and reuse terms. Offline feasibility describes the first discriminating test, not readiness or a compute estimate.
- Existing catalogue run notes for VMAS and the small Vicsek implementation were inspected. Those runs were performed by other agents. ARGoS, Kilombo, JuPedSim and the swarmalator code were not executed here; version compatibility and exact model support remain to be checked.
- A two-dimensional toy simulator cannot establish drone safety, physical contact realism, underwater sensing, or human-crowd safety. Hardware access and independent replication would be later evidence requirements.
- Crowd studies are synthetic or retrospective. No dangerous crowd-density manipulation, on-road driving trial, or operational evacuation recommendation is proposed.
- The physical identity-vetting item uses authorized synthetic observations. It does not involve targeting a live robot or radio network, and radio uniqueness is not a software-agent identity oracle.
- Agreement, polarization, shape restoration, synchronization and task success are different outcomes. Several items intentionally test where one stops being a useful proxy for another.
- PHY-37 and PHY-38 directly cover the NCA observatory with learned cellular rules. The earlier acoustic-particle and robot-recovery items remain analogies only. No trained NCA result was inferred from a classical animation.
- When choosing finalists, inspect closest-prior methods and follow-ups, reproduce the simple baseline, specify effect sizes and power or precision goals, and complete the repository's survey and hypothesis review gates. Group or episode replication must not be replaced by counting dependent particles or frames as independent samples.

## Coverage decisions

Candidates on generic criticality-versus-false-alarm utility and generic early warnings were removed from this sub-bank because the parent agent covers them. Motion PHY-05 instead tests the physical cause of fragmentation; crowd PHY-34 tests confinement in a specific mechanical model. PHY-02 distinguishes two proposed turning-wave mechanisms, rather than inferring an interaction graph from trajectories. The bank deliberately includes replications, boundary tests and negative controls alongside extensions and more speculative applications.

## NCA coverage addendum

An editorial audit found that the initial physical-recovery items did not cover the learned-NCA brief itself. Added PHY-37 (structured hidden-state lesions and exact maze validity) and PHY-38 (masked parallel execution versus independent local clocks). These cite actual NCA sources, not robot-assembly papers as substitutes. Their source/checkpoint access is still a prerequisite.

The direct sources were missing from the catalogue when searched by title, DOI and arXiv ID with `lab.py find`. With parent authorization, created the following records through `lab.py new`, owned by `dmarz/question-atlas`:

- [[mordvintsev-2020-growing]] — [Growing Neural Cellular Automata](https://distill.pub/2020/growing-ca/), DOI 10.23915/distill.00023. Skimmed the model, experimental descriptions, figure captions and discussion; notebooks and interactive models were not run.
- [[etcheverry-2026-reasoning]] — [Reasoning with Neural Cellular Automata](https://arxiv.org/html/2609.36126v1), arXiv 2609.36126. Read the abstract and introduction, selected architecture/training sections, repair and ablation figure descriptions, discussion, and execution-accounting limitations in Appendix B.5. Skim depth; no full-appendix read, downloaded checkpoint or execution.
- [[ha-2022-collective]] — local NCA-covering review inspected as orientation; it is not substituted for the two primary papers.

The execution hunch distinguishes a local learned rule from the scheduling and read/write semantics used to run it. Source-reported operation savings are not independently measured hardware savings. The repair hunch preserves immutable maze inputs so damage does not silently change the task. Both require further prior-art checking before promotion. Also corrected PHY-11 and PHY-32 so each falsifier contradicts its stated prediction rather than merely illustrating the motivating concern.
