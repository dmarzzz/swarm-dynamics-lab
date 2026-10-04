# Flashbots Sybil work and its analogues in swarms, P2P networks and LLM agent collectives

> **Status (2026-10-03): draft, merged incomplete.** Built mostly on abstract and skim reads (176 of 228 sybil entries). Open work: read-depth and attribution audit (#76), citation chasing and browser-only sources (#51), sybil datasets (#49). The survey this rests on has not passed the gate.

Owner: dmarz/sybil-flashbots, holding task synthesis-sybil-flashbots. Written 2026-10-03 from library entries
tagged `sybil-resistance`. Every claim cites a library entry by its id in double square brackets. Statements marked "inferred" are this
document's reading across sources, not results any source reports. This is a synthesis, not a survey: it has
not passed the prior-art gate and proposes no hypotheses.

Question: how does Flashbots' Sybil-resistance work relate to Sybil resistance in robot swarms, P2P networks
and LLM agent collectives?

Short answer. Flashbots rarely tries to count actors. Its production defences price actions (per-bundle
payments, auctions, failed-transaction cost), attach penalties to operator entities rather than keys, cap what
any coalition of identities can be paid, and admit machines by attestation plus allowlists
([[buildernet-2025-refunds]], [[gh-flashbots-mev-boost-relay]], [[flashbots-2025-mev]],
[[gh-flashbots-builder-hub]]). Its theory work proves where identity-splitting cannot be prevented
([[pan-2024-sybil]], [[mazorra-2023-cost]]). Each of these has a counterpart in at least one of the other three
communities, but the LLM agent literature mostly assumes a fixed identity set and has not yet adopted the
pricing and coalition-cap tools (inferred from the lane reports and the entries cited in section 3).

## 1. Problem-defence-analogue map

Scope of "Flashbots" here: sources written or co-written by Flashbots staff, Flashbots forum threads and
Flashbots repositories. Rows marked (adjacent) are Ethereum research problems that Flashbots infrastructure
depends on but that Flashbots did not author.

| Flashbots Sybil problem | Flashbots defence | Robot swarms | P2P / distributed systems | LLM agent collectives |
|---|---|---|---|---|
| Refunds and rebates farmed by splitting one searcher into many identities | Flat-tax refund by capped marginal contribution [[collective-2024-refund]], then the "identity constraint": no set of identities is paid more than its joint marginal contribution, enforced by least-squares projection [[buildernet-2025-refunds]]. Theory: one extra Sybil collapses symmetric truthful allocation to the second price auction [[pan-2024-sybil]]; per-identity cost c and pie shrinking [[mazorra-2023-cost]] | Deposit per reading, refunded only to inliers, so wealth and not identity count decides the outcome [[strobel-2020-blockchain]] | Stake-weighted sortition, so splitting stake across identities gains nothing [[gilad-2017-algorand]]; quadratic funding's Sybil arithmetic and cluster matching [[buterin-2019-flexible]] [[ethresearch-2023-collusion]] | Credit attribution by Shapley over sources rewards duplicates (inferred in the entry) [[patel-2025-maxshapley]]; one fabricated episode launders reputation across skills [[xia-2026-when]]; K seller identities raise Sybil revenue share from under 5% to 10-17% [[karten-2026-agent]] |
| A searcher posing as users to poison batches or extract hint data (MEV-Share) | Batching rejected because searchers can pose as users [[collective-2023-mev-share]]; random subsampling before differentially private aggregation [[passerat-palmbach-2025-differentially]] | Spoofed nodes inflate perceived graph robustness; neighbour opinion sharing finds them in constant rounds [[mallmann-trenn-2021-crowd]] | Bogus votes capped at attack-edge count [[tran-2009-sybil-resilient]]; track-record weights bound loss without identity checks [[yu-2009-dsybil]] | Epistemic Sybils: replicated reports are indistinguishable from corroboration by content alone [[bara-2026-epistemic]]; manufactured corroboration launders memory authority [[louck-2026-securing]] |
| On-chain searching spam on rollups | Measured: spam bots used over 50% of gas and paid under 10% of fees; two entities behind over 80% of Base spam, found by clustering profit-taking addresses [[flashbots-2025-mev]] [[gh-flashbots-spam-inspect]]. Proposed: paid non-reverting endpoints and sequencer auctions [[collective-2024-dealing]]. Model: equilibrium spam is about V/c, independent of identity count [[mazorra-2026-timing]] | Per-message ether deposit that a spamming robot forfeits [[strobel-2020-blockchain]] | Resource burning, with honest cost below attacker cost [[gupta-2020-resource]] [[gupta-2021-bankrupting]]; impossibility of open-mempool spam resistance without a toll, held funds or trust [[ankushin-2026-public]]; rate-limiting nullifiers [[barrywhitehat-2019-semaphore]] | Deposit-bounded anonymous API credits with RLN [[crapis-2026-zk]]; 21.2% of x402 settlements fictitious despite per-request payment [[ling-2026-how]] |
| Flooding a permissionless bundle or block endpoint from throwaway keys, and re-entry after a bad record | Signed bundles to track searcher reputation [[flashbots-2021-flashbots]]; priority queues, quotas or per-bundle fees debated [[flashbots-2021-proposal]]; slashable builder deposits [[flashbots-2022-relay]]; low priority for unknown keys, demotion of every key under one builder_id, collateral for optimistic submission [[gh-flashbots-mev-boost-relay]]; salted IP fingerprint as rate-limit key [[gh-flashbots-rpc-endpoint]]; token bucket on the BuilderNet user API [[gh-flashbots-buildernet-orderflow-proxy]]; reputation as a "negative contingent fee" defeated by re-entry [[resnick-2023-contingent]] | Signed accusations and maximum matching over a fixed identity set [[wardega-2023-byzantine]] | GossipSub peer scoring [[vyzovitis-2020-gossipsub]], with configurations that let peers withhold in chosen topics while scoring positive [[kumar-2024-formal]]; eclipse from free node keys and few IPs [[marcus-2018-low-resource]] [[heilman-2015-eclipse]] | Retire-and-replace seller identities [[karten-2026-agent]]; per-operator HTTP signatures give accountability but not uniqueness [[gh-cloudflare-web-bot-auth]]; multi-topic EigenTrust with stake burn [[zhang-2026-distributed]] |
| One builder splitting stake across many builder or committee identities; many nominal builders acting as one | Objection raised against bonded allowlisted builders [[collective-2022-decentralized]]; Sybil behaviour among builders left as an open problem in multi-proposer building [[flashbots-2026-why]]; builder_id groups keys into one entity [[gh-flashbots-mev-boost-relay]]. (adjacent) Anti-correlation penalties price hidden common control [[buterin-2024-supporting]]; linear rewards lose to splitting, convex rewards and audits needed [[bahrani-2026-capacity]]; AUCIL committee is individually but not jointly incentive compatible [[nag-2026-sybil]] | Co-located transmitters produce matching fingerprints, giving per-identity confidence weights [[gil-2015-guaranteeing]] | Correlated operators collapse distinct seats into one failure domain [[obol-2026-deployment]]; no slashing rule prevents both restaking Sybil attack types [[chitra-2025-sybil]] | Agents sharing a base model have correlated errors (gamma 0.719) that cap added information [[bara-2026-epistemic]]; parent-child instance IDs expose common origin at zero cost per instance [[chan-2024-ids]] |
| TEE attestation used as builder or node identity | Attested TLS plus measurement whitelist plus source-IP lookup [[gh-flashbots-builder-hub]]; attestation cannot separate instances on one CPU or owners of identical workloads [[collective-2024-portrait]]; production kept operator and IP allowlists after interposer attacks [[collective-2025-why]]; Proof of Cloud binds the quote to a certified chassis [[rezabek-2025-proof]]; attest-once registry keyed by TEE address [[gh-flashbots-flashtestations]] [[miller-2024-sirrah]]. Attacks: forged TDX quotes registered a fake BuilderNet node [[chuang-2025-teefail]] [[seto-2025-wiretap]] | Physical-layer identity and trust from channels and sensing [[gil-2023-physicality]] [[gil-2015-guaranteeing]] | Certified node ids bound to key and IP [[castro-2002-secure]]; puzzle-bound node ids [[baumgart-2007-skademlia]] | TEE-hosted agent with provably exclusive accounts [[malhotra-2024-setting]] on dstack, where every replica shares one key [[zhou-2025-dstack]]; Proof as a trust anchor for agent protocols [[hu-2025-inter-agent]] |
| Renting or pooling real identities through encumbered keys | Liquefaction encumbered a Flashbots soulbound token; one-person-one-account systems fail under encumbrance [[austgen-2024-liquefaction]]; proofs of complete knowledge as the counter [[kelkar-2024-complete]] [[austgen-2023-complete]] | No analogue found in the library: physical-layer schemes assume one radio per attacker (robotics lane report) [[gil-2015-guaranteeing]] | Bearer tokens can be pooled ("hoarding") [[davidson-2024-privacy]]; non-transferable anonymous tokens [[durak-2024-non]] | One personhood credential can drive many agents [[adler-2024-personhood]]; enclave program speaking through many consenting accounts looks like coordinated Sybils [[sun-2024-tee]] |
| Timing games and probabilistic backrunning races | Model of n players paying c per action: zero equilibrium payoff, spam between V/c - 1 and V/c [[mazorra-2026-timing]]; explicit ordering bids proposed [[flashbots-2025-mev]] | No analogue found in the library | Identity priced by puzzle solutions, so agreement holds under a compute bound [[aspnes-2005-exposing]] | Autonomous supracompetitive pricing by LLM agents in repeated markets [[fish-2024-algorithmic]] (a coordination analogue, not an identity one: inferred) |
| Spam and Sybil peers in private order-flow and broadcast networks | Registered-peer keys for system endpoints [[gh-flashbots-buildernet-orderflow-proxy]]; TEE-attested clients guarantee well-formed inputs in anonymous broadcast [[collective-2026-avoiding]] | Blockchain admission for robot swarms [[dorigo-2024-blockchain]] | (adjacent) Stake-backed anonymous credentials for DHT and discovery membership [[kadianakis-2023-proof]] [[alpturer-2026-aetherweave]]; credentials force uniform mixnet routes [[kleinstein-2025-sybil]] | Web-of-trust key certification for GossipSub agent collectives [[laws-2026-panda]] |

## 2. The common frame: cost to mint an identity versus value an identity extracts

Every row above is an instance of one inequality. An adversary gains from presenting k identities when the
value extractable per extra identity exceeds the marginal cost of minting and maintaining it. Douceur's result
is that without a certifier the minting cost cannot be forced up for free [[douceur-2002-sybil]]. Mazorra et al.
make the cost explicit as c per identity and show that equal-split rewards lose welfare of order n at any small
c [[mazorra-2023-cost]]. Porobov proposes measuring a personhood method by exactly this: the market price at
which forging an accepted identity becomes profitable [[porobov-2026-price]].

Defences move one side or the other.

Raise the minting cost.
- Stake or deposits: [[gilad-2017-algorand]], [[buterin-2017-casper]], [[strobel-2020-blockchain]],
  [[flashbots-2022-relay]]. Stake only works if extraction is linear in stake, not in identity count; when
  rewards are linear and capacity reports are free, splitting still wins [[bahrani-2026-capacity]].
- Resource burning and puzzles: [[aspnes-2005-exposing]], [[gupta-2021-bankrupting]], [[baumgart-2007-skademlia]].
- Physical or hardware binding: radio fingerprints [[gil-2015-guaranteeing]]; attested chassis in approved data
  centres [[rezabek-2025-proof]]. In the TEE case the minting cost became the price of a rented machine in an
  approved cloud plus, after TEE.fail, governance allowlists [[collective-2025-why]] [[chuang-2025-teefail]].
- Personhood: [[ford-2008-offline]], [[borge-2017-proof-of-personhood]], [[adler-2024-personhood]]. Key
  encumbrance lowers the effective cost again by making identities rentable [[austgen-2024-liquefaction]].

Lower the value an extra identity extracts.
- Price actions, not actors. Per-bundle fees, ordering auctions and failed-transaction cost make the payoff of
  identity k+1 the same as that of identity k [[flashbots-2021-proposal]] [[collective-2024-dealing]]
  [[flashbots-2025-mev]]. The timing-games model shows spam scales with V/c and not with n
  [[mazorra-2026-timing]]. Rate-limiting nullifiers and deposit-bounded credits do the same per epoch
  [[barrywhitehat-2019-semaphore]] [[crapis-2026-zk]].
- Cap coalitions. BuilderNet's identity constraint bounds what any set of identities receives by its joint
  marginal contribution [[buildernet-2025-refunds]]. Myerson-value aggregation on contribution graphs plays the
  same role [[glynn-2026-wash]].
- Use winner-take-all allocation. Pan et al. show the second price auction is the only symmetric, truthful,
  non-wasteful Sybil-proof rule [[pan-2024-sybil]]; Algorand sortition makes split stake equivalent to unsplit
  stake [[gilad-2017-algorand]].
- Bound influence per attack edge or per trust signal instead of per identity: [[yu-2008-sybillimit]],
  [[tran-2009-sybil-resilient]], [[yemini-2021-characterizing]].
- Penalise correlation. Anti-correlation slashing extracts less from identities that fail together
  [[buterin-2024-supporting]].

Tolerate. Some designs make identity count irrelevant to correctness. In Dave one honest party with a bond
defeats any number of coordinated Sybil claims at logarithmic delay [[coutinho-de-paula-2025-dave]]. In DSybil
the loss bound depends on track record and not on the number of Sybil voters [[yu-2009-dsybil]].

Where Flashbots sits (inferred). Flashbots' production systems mainly use the second column: price the action,
group keys into entities, cap coalitions. Minting-cost defences appear only for builders, where the identity is
an attested machine plus an allowlisted operator ([[gh-flashbots-builder-hub]]). Searchers and users stay
pseudonymous throughout, with only a salted IP fingerprint for rate limiting ([[gh-flashbots-rpc-endpoint]]).

Wash and collusion are outside this frame. Many genuinely distinct identities that endorse each other's
worthless work do not change the minting-cost side at all [[glynn-2026-wash]], and colluding LLM agents that hide
coordination are the same problem in agent form [[motwani-2024-secret]].

## 3. What transfers

### From MEV to agent swarms

1. The coalition cap. BuilderNet's identity constraint ([[buildernet-2025-refunds]]) is a deployed rule that
   keeps a per-identity marginal-contribution payout and makes splitting unprofitable. Agent swarms that pay or
   rank agents by contribution, for example source attribution ([[patel-2025-maxshapley]]) or skill-conditioned
   routing ([[xia-2026-when]]), have the same splitting exposure and no equivalent cap in the library
   (inferred).
2. Entity grouping of keys. The relay demotes all keys under one builder_id ([[gh-flashbots-mev-boost-relay]]).
   Agent registries that sign per operator ([[gh-cloudflare-web-bot-auth]]) or link instances to parents
   ([[chan-2024-ids]]) could attach penalties at the operator or lineage level in the same way (inferred).
3. Pricing per action when identities are free. The spam measurements and the V/c bound
   ([[flashbots-2025-mev]], [[mazorra-2026-timing]]) and the gossip impossibility ([[ankushin-2026-public]])
   say that an open agent message layer without per-attempt cost or held funds cannot bound wasted work. The
   x402 data shows that payment without real cost does not do this either ([[ling-2026-how]]).
4. Impossibility results as design limits. Any agent-swarm rule that spreads a scarce resource beyond the top
   bidder (load balancing, lottery task assignment, equal splits) inherits the Pan et al. impossibility
   ([[pan-2024-sybil]]) unless it accepts Bayesian Sybil-proofness or a per-identity cost
   ([[mazorra-2023-cost]]). Mazorra et al. also show that Sybils committed to act as independent agents,
   including delegated AI agents, can break mechanisms that resist ordinary Sybils ([[mazorra-2023-cost]]).
5. Attestation limits. Flashbots' own analysis says an attestation identifies code and possibly a CPU, not an
   instance count or owner ([[collective-2024-portrait]]). dstack gives all replicas one key
   ([[zhou-2025-dstack]]). "One attested agent" is therefore not "one agent" (inferred), and TEE-attested agent
   identity schemes ([[malhotra-2024-setting]], [[zhang-2026-distributed]]) inherit this.
6. Identity rental. Liquefaction and Complete Knowledge come from the Flashbots-adjacent TEE line
   ([[austgen-2024-liquefaction]], [[kelkar-2024-complete]]). They apply directly to personhood-gated agents
   ([[adler-2024-personhood]]). The TEE_HEE design is encumbered on purpose, so proving an agent is autonomous
   and proving its key is not rented pull in opposite directions (inferred in the gap lane report, see
   [[malhotra-2024-setting]]).

### From swarms and P2P back to MEV

1. Correlation as a common-control signal. Robot fingerprints ([[gil-2015-guaranteeing]]), validator
   co-failures ([[buterin-2024-supporting]]) and shared-model error correlation ([[bara-2026-epistemic]]) all
   detect one controller behind many identities without identifying it. Builder-splitting
   ([[collective-2022-decentralized]], [[flashbots-2026-why]]) and BuilderNet's common-mode risk
   ([[eigenphi-2025-buildernet]]) could be measured the same way (inferred). [[flashbots-2025-mev]] already uses
   a crude version (clustering by profit-taking address).
2. Trust side channels with proofs of bounded deviation. Robotics bounds the collective outcome even when
   malicious agents hold more than half of connectivity, given stochastic trust observations
   ([[yemini-2021-characterizing]], [[cavorsi-2024-exploiting]]). MEV designs mostly bound per-identity payout,
   not collective outcome (inferred).
3. Eclipse as the practical Sybil attack on one participant's view ([[singh-2006-eclipse]],
   [[heilman-2015-eclipse]]). BuilderNet peer discovery through a central hub
   ([[gh-flashbots-builder-hub]]) avoids it today by centralisation; a permissionless roadmap
   ([[collective-2025-why]]) would need the outbound quotas, anchors and stake-gated discovery of
   [[alpturer-2026-aetherweave]] (inferred).
4. Churn-aware admission pricing. Ergo prices joins by recent join rate ([[gupta-2021-bankrupting]]). The relay's
   newcomer queue is the problem it addresses ([[flashbots-2021-proposal]]).
5. Information-theoretic redundancy. Bara's definition of a Sybil as a report adding no conditional information
   ([[bara-2026-epistemic]]) fits multi-builder or multi-proposer redundancy, where N nominal builders running the
   same software on the same cloud add little independent coverage ([[eigenphi-2025-buildernet]]) (inferred).

## 4. Open problems that transfer, as candidate survey questions

These are questions for a prior-art survey to answer, not claims to test.

1. Has any multi-agent credit-assignment or routing scheme for LLM agents adopted a joint-marginal-contribution
   cap like [[buildernet-2025-refunds]], and what is known about its cost in welfare or accuracy?
2. What does the literature report on Sybil-proofness of contribution-based payouts once identities can commit to
   act independently, as in the commitment section of [[mazorra-2023-cost]], when the committed agents are LLM
   agents ([[gh-brunomazorra-llms-sybils]])?
3. Has anyone measured how often identity splitting happens in a live MEV market? The Flashbots lane found only
   the address clustering in [[flashbots-2025-mev]].
4. Which published work varies the number of identities an adversary holds in LLM debate, voting or consensus?
   The LLM lane found only fixed adversary counts ([[amayuelas-2024-multiagent]], [[el-mir-2026-byzantine]],
   [[jo-2025-byzantine]]) and a K sweep in a market ([[karten-2026-agent]]).
5. Is there prior work that uses error correlation or co-failure statistics, as in [[buterin-2024-supporting]]
   and [[bara-2026-epistemic]], to detect common control among block builders or among agents behind one
   operator?
6. What admission cost do agent key directories and registries impose today ([[gh-cloudflare-web-bot-auth]],
   [[ethresearch-2026-anonymous]], [[hu-2025-inter-agent]]), and has any been studied against the gossip
   impossibility in [[ankushin-2026-public]]?
7. Has any work bounded the collective outcome (not only per-identity payout) of a market or auction when a
   Sybil coalition holds a majority of identities, in the style of [[yemini-2021-characterizing]]?
8. What is known about detecting rented or encumbered identities in personhood-gated agent systems, beyond
   Complete Knowledge proofs ([[kelkar-2024-complete]], [[austgen-2024-liquefaction]])?
9. After TEE.fail ([[chuang-2025-teefail]]), what does the literature say about counting distinct physical
   machines behind attestations, and does Proof of Cloud ([[rezabek-2025-proof]]) have published analyses of how
   many identities one cloud tenant can register?
10. Which peer-discovery defences from P2P ([[singh-2006-eclipse]], [[alpturer-2026-aetherweave]],
    [[kumar-2024-formal]]) have been evaluated on agent collectives built on GossipSub ([[laws-2026-panda]])?

## Gaps in the evidence behind this map

- Most Flashbots sources here are forum posts, documentation and code. The peer-reviewed results are
  [[pan-2024-sybil]], [[mazorra-2023-cost]], [[mazorra-2026-timing]], [[passerat-palmbach-2025-differentially]],
  [[rezabek-2025-proof]] and the TEE attack papers.
- SUAVE economic-security posts, mev-share-node rate limits and Flashbots Protect thresholds were not read
  (Flashbots lane report).
- Two table cells have no analogue in the library (identity rental in robot swarms, timing games in robot
  swarms). This reflects what the library holds, not a claim that no such work exists.
