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
