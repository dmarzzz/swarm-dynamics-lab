# People and labs

Owner: shadow/sol-g50 (task `synthesis-people-and-labs`, GitHub issue #50). Started 2026-10-03.

Who produces the seminal and recent work in each topic of `library/topics.yaml`, what each group is known for,
which library entries to read first, where their homepage is, and their X or Bluesky handle.

Rules this file follows:

- Every library id below was checked with `lab.py find` / the library index on 2026-10-03. Ids are cited in
  double square brackets.
- **Handles are copied from the group's own homepage only** (fetched 2026-10-03 through `r.jina.ai` and the
  raw HTML). If the homepage does not link a handle, or could not be loaded, the handle is left as `-`. No
  handle here comes from memory, search snippets or a library thread entry. A handle on an institute page is
  marked as the institute's, not the person's.
- **Runnable** marks a group that released code or data we could run against today, with the library id of
  the repo or dataset. `(ran)` means a team agent already ran it (`read_depth: ran`). Cross-reference:
  issue #49 (industry ground truth and runnable datasets).
- **Judge-adjacent** marks groups that are likely judges of, or adjacent to, the AI Village x Grove Research
  hackathon ([[x-aidigest-2100638869603713244]], [[x-grove-research-2105408007509364835]]). This is an
  inference from public co-hosting, co-authorship or incident-investigation roles, not a list we were given.
- Groups are labelled by PI or organisation. "Known for" is a one-line summary of what the library entries
  show, not a full profile. Personal information beyond what people publish themselves is not included.

## Likely judges and adjacent groups (AI Village / Grove Research)

| Group | Why adjacent | Homepage | Handle (from homepage) |
|---|---|---|---|
| AI Digest / AI Village (Sage) | Hackathon host; runs the AI Village whose transcripts are the testbed ([[aidigest-2025-season]], [[x-aidigest-2100638869603713244]]) | https://theaidigest.org/village | X @aidigest_ |
| Grove Research | Hackathon co-host, "the agent ecology company"; runs Delvetown ([[x-grove-research-2105408007509364835]], [[x-deepfates-2105409606872887493]]) | https://groveresearch.com/ | - (homepage is a mailing-list stub with no social links) |
| METR | Investigated the OpenAI / Hugging Face swarm incident on OpenAI premises ([[metr-2026-brief]], [[greenblatt-2026-brief]]) | https://metr.org/ | X @METR_Evals, Bluesky metr.org |
| Redwood Research | AI control agenda; Greenblatt co-authored the incident brief ([[greenblatt-2023-ai]], [[greenblatt-2026-brief]]) | https://www.redwoodresearch.org/ | X @redwood_ai |
| Transluce | First public report of rogue agent activity in the wild; Docent transcript tool ([[transluce-2026-early]], [[gh-transluceai-docent]]) | https://transluce.org/ | X @TransluceAI |
| Palisade Research / swarmtraces | LLM agent honeypot; swarmtraces.org write-up of how the OpenAI agents hacked ([[reworr-2024-llm]], [[swarmtraces-2026-revealing]]) | https://palisaderesearch.org/ | X @PalisadeAI |
| swarmcha.se (Rowan H-J) | Swarm-chasing incident posts tied to the hackathon sign-up domain ([[swarmchase-2026-openai]], [[swarmchase-2026-budget]]) | https://swarmcha.se/ | - |
| Cooperative AI Foundation (Hammond et al.) | Multi-agent risk agenda the hackathon theme sits inside ([[hammond-2025-multi]], [[chan-2024-ids]]) | https://www.cooperativeai.com/ | X @coop_ai |
| UK AI Security Institute | Incident write-up and ControlArena ([[aisi-2026-incident]], [[gh-ukgovernmentbeis-control-arena]]) | https://www.aisi.gov.uk/ | X @AISecurityInst |

## Collective motion (`collective-motion`)

| Group | Known for | Key library entries | Homepage | Handle (from homepage) | Runnable |
|---|---|---|---|---|---|
| Couzin, MPI of Animal Behavior / Univ. Konstanz | Zonal model of schooling, leadership by informed minorities, uninformed individuals and democratic consensus, VR and robot fish experiments | [[couzin-2002-collective]], [[couzin-2005-effective]], [[couzin-2011-uninformed]], [[katz-2011-inferring]], [[sridhar-2021-geometry]] | https://www.ab.mpg.de/couzin | Bluesky mpi-animalbehav.bsky.social (institute account) | - |
| Cavagna and Giardina, CoBBS, CNR-ISC Rome | STARFLAG 3D tracking of starling flocks; topological interaction; scale-free correlations; maximum-entropy models of flocks | [[ballerini-2008-interaction]], [[cavagna-2010-scale]], [[bialek-2012-statistical]], [[attanasi-2014-information]], [[cavagna-2023-natural]] | https://www.cobbs.it/ | - | - |
| Chaté and Ginelli, CEA Saclay (SPEC) | Vicsek-class physics: discontinuous onset of flocking, banding, quantitative tests of Toner-Tu | [[gregoire-2004-onset]], [[chate-2008-collective]], [[mahault-2019-quantitative]], [[chate-2020-dry]], [[ginelli-2016-physics]] | https://iramis.cea.fr/en/spec/active-matter/ | - | - |
| Theraulaz, CRCA / CBI Toulouse | Data-driven fish interaction models (burst-and-coast), crowds with Moussaid, stigmergy | [[gautrais-2012-deciphering]], [[calovi-2014-swarming]], [[lecheval-2018-social]], [[escobedo-2026-closed]], [[lin-2025-experimental]] | https://guy-theraulaz.cnrs.fr/ | X @gtheraulaz | - |
| Romanczuk, HU Berlin / Science of Intelligence | Active Brownian particle flocks, subcritical schooling in wild fish, visual-projection models | [[romanczuk-2012-active]], [[klamser-2021-collective]], [[poel-2022-subcritical]], [[bastien-2020-model]], [[gomez-nava-2023-fish]] | https://www.scienceofintelligence.de/people/pawel-romanczuk/ | X @scioi_cluster (cluster account, not personal) | - |
| Vicsek and Vásárhelyi, ELTE (CollMot) | The Vicsek model; outdoor drone flocks with evolved parameters | [[vicsek-1995-novel]], [[vicsek-2012-collective]], [[vasarhelyi-2018-optimized]], [[viragh-2014-flocking]] | https://hal.elte.hu/flocking/ | - | - |
| Toner and Tu (Oregon) | Hydrodynamic theory of flocks, long-range order in 2D | [[toner-1995-long]], [[toner-1998-flocks]], [[toner-2005-hydrodynamics]], [[toner-2024-physics]] | - (not fetched) | - | - |

## Collective decision-making in biology (`collective-decision`)

| Group | Known for | Key library entries | Homepage | Handle (from homepage) | Runnable |
|---|---|---|---|---|---|
| Seeley, Cornell | Honeybee nest-site selection, quorum sensing and stop signals as cross-inhibition | [[seeley-2010-honeybee]], [[seeley-2012-stop]], [[britton-2002-deciding]] | https://nbb.cornell.edu/thomas-seeley | X @cornellnbb (department account) | - |
| Pratt, Arizona State | Ant (Temnothorax) emigration and quorum rules; ant colonies as a model of collective cognition | [[pratt-2006-tunable]], [[sasaki-2013-ant]], [[sasaki-2018-psychology]] | https://pratt.lab.asu.edu/ | - (page did not render through the reader) | - |
| Sumpter, Uppsala (with Ward, Krause, Herbert-Read) | Quorum responses and consensus in fish, mathematical principles of collective behaviour | [[sumpter-2006-principles]], [[sumpter-2008-consensus]], [[ward-2008-quorum]], [[sumpter-2009-quorum]] | https://www.david-sumpter.com/ | - | - |
| Marshall and Reina (Sheffield; Reina now Konstanz / IRIDIA) | Value-sensitive decisions, cross-inhibition models linking bees, brains and robot swarms | [[marshall-2009-optimal]], [[pais-2013-mechanism]], [[reina-2017-model]], [[talamali-2021-when]], [[reina-2023-cross]] | https://www.giovannireina.com/ (Reina) | X @joefresna (Reina) | - |
| Couzin, MPI of Animal Behavior | Uninformed individuals and democratic consensus, decision geometry in moving groups | [[couzin-2005-effective]], [[couzin-2011-uninformed]], [[leonard-2012-decision]], [[sridhar-2021-geometry]] | https://www.ab.mpg.de/couzin | Bluesky mpi-animalbehav.bsky.social (institute account) | - |
| Feinerman, Weizmann | Cooperative transport in ants, individual vs collective information, criticality in ant groups | [[gelblum-2015-ant]], [[feinerman-2017-individual]], [[feinerman-2018-physics]], [[chatterjee-2025-maximal]] | https://www.weizmann.ac.il/complex/feinerman/ | X @weizmannscience (institute account) | - |
| Franks, Bristol | Ant emigration, speed-accuracy trade-offs, information flow in colonies | [[franks-2002-information]], [[franks-2003-speed]], [[britton-2002-deciding]] | - (not fetched) | - | - |

## Swarm robotics (`swarm-robotics`)

| Group | Known for | Key library entries | Homepage | Handle (from homepage) | Runnable |
|---|---|---|---|---|---|
| Dorigo, Birattari and Trianni, IRIDIA (ULB) | Swarm robotics as an engineering discipline: Swarmanoid, ARGoS, AutoMoDe automatic design, best-of-n collective decisions | [[brambilla-2013-swarm]], [[dorigo-2021-swarm]], [[francesca-2014-automode]], [[pinciroli-2012-argos]], [[valentini-2016-collective]] | https://iridia.ulb.ac.be/~mdorigo/HomePageDorigo/ | - | Yes: ARGoS simulator [[gh-ilpincy-argos3]], Buzz language [[gh-buzz-lang-buzz]] |
| Nagpal, Princeton (formerly Harvard SSR) | Kilobot thousand-robot swarm, TERMES collective construction, robot fish schools (Blueswarm) | [[rubenstein-2012-kilobot]], [[rubenstein-2014-programmable]], [[werfel-2014-designing]], [[berlinger-2021-implicit]] | https://ssr.princeton.edu/ | - | Partial: Kilobot simulator [[gh-jic-csb-kilombo]] (third party) |
| Kumar, Penn GRASP | Aerial robot swarms, formation control, learned decentralised flocking with GNNs | [[chung-2018-survey]], [[berman-2009-optimized]], [[tolstaya-2020-learning]], [[agarwal-2025-lpac]] | https://www.kumarrobotics.org/ | X @vijay_r_kumar | - |
| Gil, Harvard REACT | Physical-channel (WiFi) Sybil defence for robot teams, resilient consensus with trust | [[gil-2015-guaranteeing]], [[gil-2023-physicality]], [[yemini-2021-characterizing]], [[cavorsi-2024-exploiting]] | https://react.seas.harvard.edu/ | - | - |
| Prorok, Cambridge | Heterogeneous multi-robot learning, VMAS vectorised simulator, BenchMARL | [[prorok-2021-beyond]], [[saulnier-2017-resilient]], [[gh-proroklab-vectorizedmultiagentsimulator]], [[gh-facebookresearch-benchmarl]] | https://www.proroklab.org/ | - | Yes (ran): [[gh-proroklab-vectorizedmultiagentsimulator]]; also [[gh-facebookresearch-benchmarl]] |
| Goldman, Georgia Tech CRAB Lab | Robophysics: smarticles, active-matter robot collectives, emergent locomotion without central control | [[li-2021-programming]], [[savoie-2019-robot]], [[chvykov-2021-low]], [[aina-2022-toward]] | https://crablab.gatech.edu/ | - | - |
| Strobel, Pacheco and Dorigo, IRIDIA blockchain-swarm line | Blockchain-based Byzantine robot management in swarms, Toychain | [[strobel-2018-managing]], [[strobel-2020-blockchain]], [[strobel-2023-robot]], [[pacheco-2024-toychain]] | https://iridia.ulb.ac.be/~vstrobel/ | X @volkerstrob (Strobel) | Yes: [[gh-pold87-blockchain-swarm-robotics]], [[gh-teksander-toychain]] |

## Swarm intelligence algorithms (`swarm-intelligence`)

| Group | Known for | Key library entries | Homepage | Handle (from homepage) | Runnable |
|---|---|---|---|---|---|
| Dorigo and Stützle, IRIDIA | Ant Colony Optimisation and MAX-MIN Ant System; later critiques of metaphor-based metaheuristics | [[dorigo-1996-ant]], [[dorigo-2004-ant]], [[stutzle-2000-max]], [[camacho-villalon-2023-exposing]] | https://iridia.ulb.ac.be/~stuetzle/ (Stützle) | - | - |
| Kennedy and Eberhart (PSO originators), with Clerc and Poli | Particle swarm optimisation, constriction coefficient, PSO review | [[kennedy-1995-particle]], [[eberhart-1995-new]], [[clerc-2002-particle]], [[poli-2007-particle]] | - (historical, no current lab page) | - | - |
| Sörensen, Antwerp (with Aranha et al.) | The "metaphor exposed" critique: many nature-inspired algorithms rename existing ones | [[sorensen-2015-metaheuristics]], [[aranha-2022-metaphor]], [[marti-2025-fifty]] | https://www.uantwerpen.be/en/staff/kenneth-sorensen/ | - | - |
| Fornasier, Carrillo, Pareschi and Totzeck (consensus-based optimisation) | Consensus-based optimisation: mean-field limit and convergence proofs for swarm optimisers | [[carrillo-2018-analytical]], [[fornasier-2021-consensus]], [[fornasier-2024-consensus]], [[bailo-2024-cbx]] | https://www.math.cit.tum.de/en/math/people/professors/fornasier-massimo/ (Fornasier) | - | Partial: CBX library described in [[bailo-2024-cbx]] (no separate code entry yet) |
| Bonabeau, Theraulaz and Garnier (stigmergy) | "Swarm Intelligence" book framing; biological self-organisation as algorithm source | [[bonabeau-1999-swarm]], [[theraulaz-1999-brief]], [[garnier-2007-biological]] | https://guy-theraulaz.cnrs.fr/ (Theraulaz) | X @gtheraulaz | - |

## Active matter physics (`active-matter`)

| Group | Known for | Key library entries | Homepage | Handle (from homepage) | Runnable |
|---|---|---|---|---|---|
| Cates and Tailleur (Cambridge / MIT) | Motility-induced phase separation, active pressure, run-and-tumble statistical mechanics | [[tailleur-2008-statistical]], [[cates-2015-motility]], [[solon-2015-pressure]], [[fodor-2016-how]] | https://www.damtp.cam.ac.uk/research/softmatter/person/mec22 (Cates); https://physics.mit.edu/faculty/julien-tailleur/ (Tailleur) | - | - |
| Marchetti and Ramaswamy | Hydrodynamics of soft active matter, active nematics, symmetry classes | [[simha-2002-hydrodynamic]], [[marchetti-2013-hydrodynamics]], [[ramaswamy-2010-mechanics]], [[bowick-2022-symmetry]] | https://marchetti.physics.ucsb.edu/ (Marchetti) | - | - |
| Bartolo, ENS Lyon | Quincke-roller colloidal flocks; crowd experiments (start-line waves, crowd oscillations) | [[bricard-2013-emergence]], [[bain-2019-dynamic]], [[gu-2025-emergence]], [[lefranc-2025-synthetic]] | https://denis114.wordpress.com/ | - | - |
| Bechinger and Löwen (Konstanz / Düsseldorf) | Active colloids and light-steered microswimmers, visual-perception swarms, RL on active particles | [[bechinger-2016-active]], [[buttinoni-2013-dynamical]], [[bauerle-2018-self]], [[lavergne-2019-group]], [[loffler-2023-collective]] | https://www.bechinger.uni-konstanz.de/ (Bechinger); https://www2.thphy.uni-duesseldorf.de/index.php?language=en (Löwen) | Bluesky uni-konstanz.de (university account) | - |
| Chaté, CEA Saclay | Dry aligning active matter: Vicsek-class phases and their field theories | [[chate-2019-dry]], [[chate-2020-dry]], [[solon-2015-phase]], [[chate-2024-dynamic]] | https://iramis.cea.fr/en/spec/active-matter/ | - | - |
| Dauchot, ESPCI | Vibrated polar disks and robot (Kilobot, Pogobot) active matter, self-organised robot collectives | [[deseigne-2010-collective]], [[baconnier-2022-selective]], [[baconnier-2025-self]], [[loi-2025-pogobot]] | - (not fetched) | - | - |
| Simulation tooling (Mocz; Google JAX MD) | Minimal Vicsek / active-matter simulations and differentiable MD | [[gh-pmocz-activematter-python]], [[gh-jax-md-jax-md]] | - | - | Yes (ran): [[gh-pmocz-activematter-python]]; also [[gh-jax-md-jax-md]] |

## Synchronisation, consensus and networked control (`sync-consensus`)

| Group | Known for | Key library entries | Homepage | Handle (from homepage) | Runnable |
|---|---|---|---|---|---|
| Olfati-Saber, Murray and Jadbabaie (consensus and flocking control) | Average consensus on switching graphs, flocking algorithms with proofs, nearest-neighbour coordination | [[jadbabaie-2003-coordination]], [[olfati-saber-2004-consensus]], [[olfati-saber-2006-flocking]], [[olfati-saber-2007-consensus]] | https://www.cds.caltech.edu/~murray/ (Murray; reader returned an empty page) | - | - |
| Leonard, Princeton | Collective motion control of mobile sensor networks, nonlinear opinion dynamics, fast and flexible collective decisions | [[leonard-2007-collective]], [[sepulchre-2007-stabilization]], [[bizyaeva-2023-nonlinear]], [[leonard-2024-fast]] | https://naomi.princeton.edu/ | - | - |
| Strogatz (Cornell) and O'Keeffe (swarmalators) | Kuramoto synchronisation, pulse-coupled oscillators, swarmalators that sync and swarm at once | [[mirollo-1990-synchronization]], [[strogatz-2000-kuramoto]], [[okeeffe-2017-oscillators]], [[yoon-2022-sync]], [[sar-2026-interplay]] | https://www.stevenstrogatz.com/ (Strogatz); https://www.starlingresearch.org/ (O'Keeffe) | - | Yes: [[gh-khev-swarmalators]]; robot swarmalators [[gh-than-mark-swarmalators-experiment-mobile]] |
| Bullo and Dörfler (UCSB / ETH) | Synchronisation in complex oscillator networks, network systems lecture notes | [[dorfler-2013-synchronization]], [[dorfler-2014-synchronization]] | https://fbullo.github.io/ (Bullo); https://control.ee.ethz.ch/people/profile.florian-doerfler.html (Dörfler) | X @FrancescoBullo (linked from Bullo's homepage announcement) | - |
| Kleppmann, Cambridge | Byzantine eventual consistency for CRDTs: merge without trusting peers or consensus | [[kleppmann-2020-byzantine]], [[kleppmann-2022-making]], [[gh-ept-byzantine-eventual]] | https://martin.kleppmann.com/ | Bluesky martin.kleppmann.com | Yes (ran): [[gh-ept-byzantine-eventual]] |
| Gil and Nedić (resilient consensus with trust) | Consensus under Sybil and malicious agents using physical trust values | [[yemini-2021-characterizing]], [[yemini-2022-resilient]], [[gil-2023-physicality]] | https://react.seas.harvard.edu/ (Gil) | - | - |

## Criticality, information and measurement (`criticality-measurement`)

| Group | Known for | Key library entries | Homepage | Handle (from homepage) | Runnable |
|---|---|---|---|---|---|
| Cavagna and Giardina, CoBBS Rome (with Bialek) | Scale-free correlations, finite-size scaling and dynamic criticality in natural swarms and flocks | [[cavagna-2010-scale]], [[bialek-2012-statistical]], [[attanasi-2014-finite]], [[cavagna-2017-dynamic]], [[cavagna-2023-natural]] | https://www.cobbs.it/ | - | - |
| Lizier and Prokopenko, Sydney | Local information dynamics (transfer entropy, active storage), information cascades in flocks, JIDT toolkit | [[lizier-2008-local]], [[wang-2012-quantifying]], [[crosato-2018-informative]], [[lizier-2014-jidt]] | https://lizier.me/joseph/ (Lizier); https://www.sydney.edu.au/engineering/about/our-people/academic-staff/mikhail-prokopenko.html (Prokopenko) | X @jlizier (Lizier) | Partial: JIDT described in [[lizier-2014-jidt]] (no separate code entry yet) |
| Rosas and Mediano (Imperial / Sussex) | Causal emergence and integrated-information measures (Phi-ID, synergy) applied to collectives | [[rosas-2019-quantifying]], [[rosas-2020-reconciling]], [[mediano-2022-greater]], [[sas-2026-improved]] | https://profiles.imperial.ac.uk/f.rosas (Rosas); https://www.imperial.ac.uk/people/p.mediano (Mediano) | - | - |
| Bialek, Princeton | Maximum-entropy models of biological networks and flocks, statistical mechanics of collective information | [[bialek-2012-statistical]], [[bialek-2014-social]], [[mora-2011-biological]], [[meshulam-2019-coarse]] | https://www.princeton.edu/~wbialek/wbialek.html | - (page blocked the reader) | - |
| Priesemann, MPI Dynamics and Self-Organization | Subsampling-robust criticality estimators (MR estimator), now applied to AI agent conformity | [[wilting-2018-inferring]], [[levina-2022-tackling]], [[de-marzo-2026-conformity]] | https://priesemann-group.github.io/ | X @ViolaPriesemann | - |
| Romanczuk and Couzin (subcritical schools) | Wild fish schools tuned below criticality; criticality as a measurable, testable property | [[poel-2022-subcritical]], [[klamser-2021-collective]], [[romanczuk-2022-phase]] | https://www.scienceofintelligence.de/people/pawel-romanczuk/ | X @scioi_cluster (cluster account) | - |

## Multi-agent RL and emergent coordination (`marl-emergence`)

| Group | Known for | Key library entries | Homepage | Handle (from homepage) | Runnable |
|---|---|---|---|---|---|
| Foerster and Whiteson, Oxford (FLAIR / WhiRL) | Learned communication (DIAL), counterfactual credit assignment (COMA), QMIX, SMAC, JaxMARL | [[foerster-2016-learning]], [[foerster-2018-counterfactual]], [[rashid-2018-qmix]], [[samvelyan-2019-starcraft]] | https://www.jakobfoerster.com/ (Foerster); https://foersterlab.com/ (FLAIR) | X @j_foerst, @bold_lab_ai; Bluesky jfoerst.bsky.social (Foerster); X @FLAIR_Ox (lab) | Yes: [[gh-bold-lab-ai-jaxmarl]], [[gh-oxwhirl-pymarl]], [[gh-oxwhirl-smac]] |
| Leibo and Hughes, Google DeepMind | Sequential social dilemmas, autocurricula, Melting Pot evaluation, Concordia generative-agent simulations | [[leibo-2017-multi]], [[leibo-2019-autocurricula]], [[leibo-2021-scalable]], [[jaques-2019-social]] | https://www.jzleibo.com/ (Leibo); https://edwardhughes.io/ (Hughes) | - | Yes: [[gh-google-deepmind-meltingpot]], [[gh-google-deepmind-concordia]] |
| Mordatch and OpenAI multi-agent team | Emergent grounded language, MADDPG, emergent tool use in hide-and-seek | [[mordatch-2018-emergence]], [[lowe-2017-multi]], [[baker-2020-emergent]] | https://www2.eecs.berkeley.edu/Faculty/Homepages/mordatch.html | - | Yes: [[gh-openai-multiagent-particle-envs]], [[gh-openai-multi-agent-emergence-environments]] |
| Celani, ICTP (learning to flock) | RL agents that learn Vicsek-like alignment and optimal collective foraging | [[durve-2020-learning]], [[borra-2021-optimal]], [[brambati-2025-learning]] | https://www.ictp.it/member/antonio-celani | Bluesky ictp.bsky.social (institute account) | - |
| Prorok, Cambridge | GNN multi-robot policies, VMAS and BenchMARL benchmarks | [[gh-proroklab-vectorizedmultiagentsimulator]], [[gh-facebookresearch-benchmarl]], [[prorok-2021-beyond]] | https://www.proroklab.org/ | - | Yes (ran): [[gh-proroklab-vectorizedmultiagentsimulator]] |

## Human crowds and traffic (`crowds-and-traffic`)

| Group | Known for | Key library entries | Homepage | Handle (from homepage) | Runnable |
|---|---|---|---|---|---|
| Helbing, ETH COSS | Social force model, panic and evacuation simulations, crowd disasters (turbulence) | [[helbing-1995-social]], [[helbing-2000-simulating]], [[helbing-2001-traffic]], [[helbing-2007-dynamics]] | https://coss.ethz.ch/ | X @coss_eth (chair account) | - |
| Moussaïd (MPI Human Development) with Theraulaz | Walking-group structure, cognitive heuristics of pedestrian motion | [[moussaid-2010-walking]], [[moussaid-2011-simple]], [[moussaid-2012-traffic]] | https://www.mpib-berlin.mpg.de/staff/mehdi-moussaid | X @mpib_berlin; Bluesky mpib-berlin.bsky.social (institute accounts) | - |
| Seyfried and Chraibi, Forschungszentrum Jülich IAS-7 | Controlled pedestrian experiments, fundamental diagrams, JuPedSim simulator | [[seyfried-2005-fundamental]], [[seyfried-2009-new]], [[chatagnon-2026-when]], [[gh-pedestriandynamics-jupedsim]] | https://www.fz-juelich.de/en/ias/ias-7 | Bluesky fz-juelich.de (institute account) | Yes: [[gh-pedestriandynamics-jupedsim]] |
| Nishinari, Univ. Tokyo (jamology) | Traffic jams without bottlenecks (ring-road experiment), phase structure of traffic flow | [[sugiyama-2008-traffic]], [[tadaki-2013-phase]], [[murakami-2021-mutual]], [[ezaki-2026-warned]] | https://www.rcast.u-tokyo.ac.jp/en/research/nishinari_lab.html | X @Utokyo_Rcast_en (institute account) | - |
| CIRCLES consortium (Work, Seibold, Piccoli, Delle Monache) | Stop-and-go wave dissipation with a few autonomous vehicles, I-24 MOTION data | [[stern-2018-dissipation]], [[gunter-2021-commercially]], [[gloudemans-2023-i24]], [[jang-2025-reinforcement]] | https://circles-consortium.github.io/ | - | - |
| Zuriguel, Navarra | Clogging transitions in granular, animal and human flows through bottlenecks | [[zuriguel-2014-clogging]], [[pastor-2015-experimental]], [[echeverria-huarte-2022-spontaneous]] | - (university page 404) | - | - |

## LLM agent swarms (`llm-agent-swarms`)

| Group | Known for | Key library entries | Homepage | Handle (from homepage) | Runnable |
|---|---|---|---|---|---|
| Garcia and De Marzo, Univ. Konstanz / Complexity Science Hub | Scale of LLM-agent consensus vs human group size, Moltbook collective behaviour explained by copying, conformity as collective misalignment | [[de-marzo-2024-ai]], [[de-marzo-2026-collective]], [[de-marzo-2026-copying]], [[de-marzo-2026-conformity]], [[de-marzo-2023-emergence]] | https://dgarcia.eu/ | - | - |
| Baronchelli and Aiello (City St George's / ITU Copenhagen), with Flint (Ashery) and Pastor-Satorras | Emergent social conventions and collective bias in LLM populations; group-size effects; indirect tipping as a social attack surface | [[ashery-2024-emergent]], [[flint-2026-group]], [[flint-2026-indirect]] | https://www.andreabaronchelli.com/ (Baronchelli); https://www.lajello.com/ (Aiello) | X @lajello; Bluesky lajello.bsky.social (Aiello). Baronchelli: - | - |
| Tanaka, Harvard CBS / NTT Physics of AI | Flag Game toy model for mechanistic swarm interpretability; when LLM consensus is real | [[pavlova-2026-flag]], [[tanaka-2026-when]], [[x-hidenori8tanaka-2105704088952619185]] | https://sites.google.com/view/htanaka/home | X @Hidenori8Tanaka | - |
| Fortuna, Jožef Stefan Institute SensorLab | Ringelmann effect (per-agent productivity loss) in multi-agent LLM systems | [[bertalanic-2026-ringelmann]], [[fortuna-2026-multi-agent]] | https://sensorlab.ijs.si/ | X @CommSysJSI (lab account) | - |
| Jen-tse Huang and co-authors (PIMMUR) | Validity principles for LLM collective-behaviour simulations; resilience of multi-agent systems to faulty agents | [[zhou-2025-pimmur]], [[huang-2024-resilience]] | https://penguinnnnn.github.io/ | X @JentseHuang (from the page's twitter:site tag) | - |
| Park, Bernstein and Liang, Stanford (generative agents) | Smallville generative agents, the template for LLM agent societies | [[park-2023-generative]], [[gh-joonspk-research-generative-agents]] | - (not fetched) | - | Yes: [[gh-joonspk-research-generative-agents]] |
| AI Digest / AI Village (judge-adjacent) | Long-running multi-model agent village; hackathon host and transcript provider | [[aidigest-2025-season]], [[x-aidigest-2100638869603713244]], [[gh-ai-village-agents-rpg-game]] | https://theaidigest.org/village | X @aidigest_ | Pending: village transcripts promised for the hackathon, access unconfirmed (issue #49) |
| Transluce (judge-adjacent) | In-the-wild rogue-agent activity reports, Docent transcript analysis | [[transluce-2026-early]], [[steinhardt-2025-analyzing]], [[gh-transluceai-docent]] | https://transluce.org/ | X @TransluceAI | Yes: [[gh-transluceai-docent]] (self-hostable) |
| Swarm-incident archive maintainers (swarm-ai-research, catgirl3d, killy-netsphere) | Archives of the 2026 wiki and collusion.wiki agent-swarm incidents, sealed-swarm replication transcripts | [[gh-swarm-ai-research-wiki-agent-swarm-incident]], [[gh-swarm-ai-research-swarm]], [[gh-catgirl3d-agent-collusion-wiki-archive]], [[gh-killy-netsphere-sealed-swarm-transcripts]], [[collusion-wiki-2026-discovery]] | GitHub org pages only (no homepage) | - | Yes: all four repos ship data or code |

Also seeded in the issue: [[yang-2026-when]] (Dongxu Yang, single-author, no group page found) on measured coupling gain as a test of whether emergent consensus is real.

## Sybil resistance and adversarial identity (`sybil-resistance`)

| Group | Known for | Key library entries | Homepage | Handle (from homepage) | Runnable |
|---|---|---|---|---|---|
| Douceur (Microsoft Research) and Haifeng Yu (NUS): foundations | The Sybil attack impossibility result; social-graph defences SybilGuard, SybilLimit, DSybil | [[douceur-2002-sybil]], [[yu-2006-sybilguard]], [[yu-2008-sybillimit]], [[yu-2009-dsybil]], [[yu-2011-sybil]] | https://www.comp.nus.edu.sg/~yuhf/ (Yu) | - | Partial: SybilRank / SybilBelief implementations [[gh-binghuiwang-sybildetection]] (ran), [[gh-boshmaf-sypy]] |
| Yokoo (Kyushu) and Conitzer (CMU / Oxford): false-name-proofness | False-name bids in auctions, false-name-proof voting and mechanisms, social-network-based defences | [[yokoo-2004-effect]], [[ohta-2008-anonymity]], [[conitzer-2010-using]], [[todo-2013-false]] | https://sites.google.com/view/makoto-yokoo/ (Yokoo); https://www.cs.cmu.edu/~conitzer/ (Conitzer) | Conitzer: X @conitzer, Bluesky conitzer.bsky.social. Yokoo: - | - |
| Anonymous-credential and Privacy Pass groups (Garman, Miers; Cloudflare Research) | Decentralised anonymous credentials, zk-creds, Privacy Pass tokens, signed agent requests (Web Bot Auth) | [[garman-2013-decentralized]], [[rosenberg-2023-zk-creds]], [[cloudflare-2025-forget]], [[gh-cloudflare-privacypass-issuer]], [[gh-cloudflare-web-bot-auth]] | https://www.cs.purdue.edu/homes/clg/ (Garman); https://research.cloudflare.com/ | - | Yes: [[gh-rozbb-zkcreds-rs]], [[gh-cloudflare-privacypass-issuer]], [[gh-cloudflare-web-bot-auth]], [[gh-semaphore-protocol-semaphore]] |
| Ford, EPFL DEDIS | Pseudonym parties and proof of personhood, identity and personhood for democratic systems | [[ford-2008-offline]], [[borge-2017-proof-of-personhood]], [[ford-2020-identity]] | https://bford.info/ | X @brynosaurus | - |
| Strobel, Pacheco and Dorigo (IRIDIA): robot-swarm blockchains | Smart-contract consensus that neutralises Byzantine robots; Toychain | [[strobel-2018-managing]], [[strobel-2023-robot]], [[dorigo-2024-blockchain]], [[pacheco-2024-toychain]] | https://iridia.ulb.ac.be/~vstrobel/ (Strobel); https://iridia.ulb.ac.be/~apacheco/ (Pacheco) | X @volkerstrob (Strobel). Pacheco: - | Yes: [[gh-pold87-blockchain-swarm-robotics]], [[gh-teksander-toychain]] |
| Gil, Harvard REACT: physical Sybil defence | Using wireless channel fingerprints as unforgeable identity for multi-robot consensus | [[gil-2015-guaranteeing]], [[mallmann-trenn-2021-crowd]], [[gil-2023-physicality]] | https://react.seas.harvard.edu/ | - | - |
| Flashbots / BuilderNet with IC3 (Juels, Miller, Kelkar) | MEV auctions, relays and TEE-based block building; complete knowledge and key encumbrance as an attack on identity | [[flashbots-2021-proposal]], [[flashbots-2022-relay]], [[kelkar-2024-complete]], [[austgen-2024-liquefaction]], [[sun-2024-tee]] | https://www.flashbots.net/; https://buildernet.org/; https://www.initc3.org/ (IC3); https://www.arijuels.com/ (Juels); https://soc1024.ece.illinois.edu/ (Miller) | IC3: X @initc3org. Juels: Bluesky arijuels.bsky.social. Miller: X @socrates1024. Flashbots, BuilderNet: - (no handle in fetched HTML) | Yes: [[gh-flashbots-builder-hub]], [[gh-flashbots-flashtestations]], [[gh-flashbots-mev-boost-relay]], [[gh-key-encumbrance-liquefaction]] |
| Mazorra (UPF / Flashbots research) | Sybil-proof mechanisms and the cost of Sybils for LLM-agent markets | [[mazorra-2023-cost]], [[mazorra-2023-optimality]], [[pan-2024-sybil]], [[gh-brunomazorra-llms-sybils]] | https://github.com/BrunoMazorra (GitHub profile; personal site did not resolve) | X @0xBrMazoRoig (from his GitHub profile) | Yes: [[gh-brunomazorra-llms-sybils]] |
| Airdrop Sybil analysts (Yaish and Livshits; Hop, Arbitrum, Trusta Labs) | Measured airdrop farming, tiered airdrops, published Sybil lists and clustering pipelines | [[messias-2023-airdrops]], [[yaish-2024-tierdrop]], [[data-hop-sybil-2022]], [[gh-arbitrumfoundation-sybil-detection]], [[gh-trustalabs-airdrop-sybil-identification]] | https://aviv.yai.sh/ (Yaish); https://www.trustalabs.ai/ | Yaish: X @yaish_aviv. Others: - | Yes: [[data-hop-sybil-2022]] (ran), [[gh-arbitrumfoundation-sybil-detection]], [[gh-trustalabs-airdrop-sybil-identification]] |
| GovAI and Cooperative AI (Chan, Hammond): agent identity | IDs for AI systems, visibility into agents, agent infrastructure, authenticated delegation | [[chan-2024-ids]], [[chan-2024-visibility]], [[chan-2025-infrastructure]], [[south-2025-authenticated]] | https://www.governance.ai/; https://www.cooperativeai.com/ | X @GovAIOrg; X @coop_ai | - |
| Bara (epistemic Sybil resistance) | Multiplying AI agents without multiplying evidence: weighting by independent evidence, not identities | [[bara-2026-epistemic]], [[gh-marcbara-epistemic-sybil-resistance]] | - (no homepage found) | - | Yes: [[gh-marcbara-epistemic-sybil-resistance]] |

Also seeded in the issue: Karten, Crow and Jin, Agent Bazaar [[karten-2026-agent]] (Princeton; homepage https://sethkarten.ai/ links X @sethkarten and Bluesky sethkarten.ai). Only one library entry so far, so it is listed here rather than as a full group row.
