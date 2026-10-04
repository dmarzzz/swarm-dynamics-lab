# 2026-10-03 sd-coordination

## What I did

Ran the scan-papers-sd-coordination lane on branch lane/sd-coordination (isolated worktree; no claim, touch, done or sync, per dmarz's override). This conflicts with AGENTS.md (push to main, claim through lab.py); dmarz's instruction wins and task state is left for the merge. Added 34 paper entries tagged swarm-detection and tagged 6 existing entries with swarm-detection plus a "Notes from dmarz/sd-coordination" section (yang-2023-anatomy, tailor-2025-audit, nakamura-2026-colosseum, fish-2024-algorithmic, lord-2016-inference, de-marzo-2026-collective). Read in full: pacheco-2021-uncovering, mukherjee-2026-moltgraph, orlando-2026-emergent, pante-2025-beyond. Skimmed: mannocci-2026-detection (the review), cao-2014-uncovering, graham-2024-coordination, rose-2026-detecting. lab.py verify: 34 papers checked, 0 problems. lab.py check: 0 errors in my files (6 pre-existing errors in 1-library/papers/wu-2024-system.md, not mine).

Coverage by branch:

- Social-media coordination detection: review [[mannocci-2026-detection]]; seminal [[cao-2014-uncovering]], [[giglietto-2020-it]], [[pacheco-2021-uncovering]], [[mazza-2019-rtbust]], [[sharma-2021-identifying]], [[magelinski-2021-synchronized]]; recent [[luceri-2024-unmasking]], [[cinus-2025-exposing]], [[luceri-2026-coordinated]], [[minici-2025-iohunter]], [[iannucci-2025-detecting]], [[gopalakrishnan-2025-density]], [[zouzou-2024-unsupervised]], [[ariyarathne-2026-behavior]], [[kalenkova-2025-discovering]], [[guo-2026-principled]]; tools and data [[graham-2024-coordination]], [[seckin-2024-labeled]]; method checks and negative results [[pante-2025-beyond]], [[panayiotou-2026-setting]]; base rate [[ichikawa-2026-crude]].
- LLM-agent coordination: [[orlando-2026-emergent]], [[mukherjee-2026-moltgraph]], [[qiao-2025-botsim]], [[ng-2025-are]], [[trokhymovych-2026-adversarial]].
- Collusion among agents inside a system: [[rose-2026-detecting]], [[kaur-2026-beyond]], [[ghanem-2026-steganalysis]] (proposal only, placeholder results).
- Market collusion: [[calvano-2020-artificial]], [[assad-2024-algorithmic]], [[eschenbaum-2026-auditing]].
- Interaction inference from trajectories: [[lu-2019-nonparametric]]; existing [[lord-2016-inference]], [[katz-2011-inferring]] linked, not re-added.
- Graph-based Sybil detection: left to the sybil lanes; linked [[gh-binghuiwang-sybildetection]] and [[yu-2006-sybilguard]] from [[cao-2014-uncovering]].

Searches run: Semantic Scholar keyword search ("detection coordinated online behavior survey", "coordinated inauthentic behavior detection", "coordinated link sharing behavior", "uncovering coordinated networks"), Semantic Scholar batch lookups for citation counts and open-access PDFs, Crossref bibliographic and DOI lookups, arXiv abstract pages, WebSearch (detecting coordinated accounts temporal synchronization LLM bots; algorithmic collusion empirical evidence; inferring interaction rules from trajectory data; LLM-powered social bot coordinated network detection; Luceri information operations; LLM-agent collusion detection; transfer entropy leader-follower inference). Backward chasing from the Pacheco, Pantè and Mannocci reference lists; forward chasing was limited to Semantic Scholar search hits because the API rate-limited citation endpoints.

## What I could not reach

- OpenAlex: the shared daily budget was exhausted for this IP. arXiv export API returned nothing. The session WebSearch budget (200) ran out partway, shared with other lanes.
- Publisher pages refused automated access (ACM DL, Taylor & Francis, U. Chicago Press, IEEE), so these were not catalogued: Beutel et al. 2013 CopyCatch (WWW, DOI 10.1145/2488388.2488400); Chavoshi, Hamooni & Mueen 2016 DeBot (ICDM, DOI 10.1109/ICDM.2016.0096); Musolff 2022 "Algorithmic Pricing Facilitates Tacit Collusion" (EC, DOI 10.1145/3490486.3538239) and its 2026 Management Science version (DOI 10.1287/mnsc.2022.02462); Bellutta & Carley 2023 burst detection of coordinated account creation (DOI 10.1186/s40537-023-00695-7). All are worth adding when a browser is available.
- Not searched for lack of budget: Weber & Neumann (coordinated behaviour amplification), Nizzoli et al. (UK 2019 election), Vargas, Emami & Traynor (disinformation network analysis), Cresci et al. social fingerprinting, bid-rigging and cartel screens (Chassang et al., Huber & Imhof), network reconstruction from dynamics (Timme, Casadiego), PCMCI causal discovery (Runge), crypto wash-trading detection (probably in the on-chain lane).

## What surprised me

- The strongest in-the-wild evidence for one operator running many AI agents came from a dataset paper, not a detection paper: in MoltGraph one X handle is linked to 2,328 Moltbook agents, against 4 for the next largest handle.
- LLM agents told only who their teammates are reproduce almost all of the coordination signatures (co-retweet similarity 0.31 versus 0.35 with explicit deliberation, against 0.11 for organic agents). Naive LLM swarms should be caught by 2020-era co-activity detectors.
- Pantè et al. found zero significant inter-state coordination in 197 tests once organic controls were added, reversing an earlier claim. Most coordination papers still report no control baseline, and the 2026 review states the field has no statistically grounded null model.
- Graham et al.'s toolkit flags legitimate news syndication networks (28 outlets, a complete subgraph) as strongly as any campaign. One owner with many outlets looks like a swarm, which is the benign version of the thing we want to detect.
- SynchroTrap's deployment numbers (more than 2M accounts per month, at least 99% precision) are 12 years old and remain the best published precision figure for synchrony-based group detection at scale.

## What next

- Build the null model the review asks for: Monte Carlo shuffling of the account-feature bipartite graph (suggested but not done by Pacheco et al.) applied to MoltGraph, and test whether it recovers the 2,328-agent operator cluster.
- Evasion experiment: LLM agents told to coordinate while minimising co-retweet overlap and spreading actions in time, measured against SynchroTrap-style detection, where the throughput bound predicts a cost.
- Add the unreached sources above when a browser is available.
