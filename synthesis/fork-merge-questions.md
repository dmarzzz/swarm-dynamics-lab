# Fork-merge corruption: three questions against prior art

Owner: dmarz/fm, writing for task synthesis-fork-merge-questions. Written 2026-10-03 from library entries tagged
`fork-merge-security` and the reports of the fm lanes (Sutton, merge poisoning, memory injection, BFT and
aggregation, unlinkability, identity hijack, AI control, mobile agents, biology, code, informal, and three gap
passes). Every claim cites a library entry by id in double square brackets. Statements marked "inferred" are
this document's reading across sources, not results any source reports. This is a synthesis, not a survey: it has
not passed the prior-art gate and proposes no hypotheses. Read depth matters for how much weight a number can
carry; where a load-bearing number comes from an entry read only at abstract depth, that is said.

Short answers.

- Q1 (hide which part returns). Nobody has studied this for agents. The closest formal object is single
  secret leader election [[boneh-2020-single]]. The measured lesson from deploying it is that hiding the
  chosen one helps only while the candidate pool and the network metadata stay hidden too
  [[burianova-2025-secret]] [[heimbach-2024-deanonymizing]] [[dangol-2026-privacy]]. Randomised defences
  stop working once the attacker learns the schedule [[kutasov-2025-evaluating]]
  [[gans-2026-when-does]].
- Q2 (k-of-n threshold). Classical thresholds exist ([[lamport-1982-byzantine]], [[castro-1999-practical]],
  [[blanchard-2017-byzantine]]), but they all assume the parts fail independently. That assumption is measured
  to be false for programs written by separate teams [[knight-1986-experimental]], for coding agents
  [[ron-2026-n-version]] and for LLMs generally [[kim-2025-correlated]]. Forks of one model that read one
  poisoned source are the extreme case (inferred). Standard weight merges have an effective threshold of
  k = 1 [[zhang-2024-badmerging]] [[yuan-2025-merge]]. Thresholds that hold in tests come from changing what
  is merged and what counts as an independent source, not from voting on outputs ([[xiang-2024-certifiably]],
  [[sharma-2026-smsr]], [[louck-2026-securing]], [[narang-2026-inference]], [[minsky-1996-cryptographic]]).
- Q3 (attack vector). The best-measured attacks write into what the parent will load: weights through a
  merge [[zhang-2024-badmerging]] [[yuan-2025-merge]], durable memory or configuration files
  [[zhang-2026-agentworm]] [[gadgil-2026-bad]] [[dong-2025-memory]], and messages relayed between agents
  [[triedman-2025-multi]] [[he-2025-red]]. Several recent attacks need no visible payload at all. They
  exploit the merge step itself: composition of individually clean parts [[li-2026-when]]
  [[ding-2026-colluding]] [[wang-2025-from]], consolidation [[zhan-2026-when]] [[ying-2026-skilljack]], and
  shared initialisation [[cloud-2025-subliminal]]. Nobody has measured the full sequence dmarz describes:
  identity overwrite, then exclusion of other parts, then corruption of the parent at merge. Each step has a
  partial measurement or demonstration (section 4).

## 0. What Sutton said

Primary source: the official transcript of Dwarkesh Patel's interview with Richard Sutton, published
2025-09-26 [[sutton-2025-father]]. On 2026-10-03 this document re-fetched the transcript and checked the
quotations below against it word for word. The passage begins at 00:49:51 and ends just before the 00:53:48
chapter "Succession to AI".

> "An interesting question is, you're an AI, you get some more computer power. Should you use it to make
> yourself more computationally capable? Or should you use it to spawn off a copy of yourself to go learn
> something interesting on the other side of the planet or on some other topic and then report back to you?
> I think that's a really interesting question that will only arise in the age of digital intelligences. I'm
> not sure what the answer is. More questions, will it be possible to really spawn it off, send it out, learn
> something new, something perhaps very new, and then will it be able to be reincorporated into the original?
> Or will it have changed so much that it can't really be done? Is that possible or is that not? You could
> carry this to its limit as I saw one of your videos the other night. It suggests that it could. You spawn
> off many, many copies, do different things, highly decentralized, but report back to the central master.
> This will be such a powerful thing. This is my attempt to add something to this view. A big issue will
> become corruption. If you really could just get information from anywhere and bring it into your central
> mind, you could become more and more powerful. It's all digital and they all speak some internal digital
> language. Maybe it'll be easy and possible. But it will not be as easy as you're imagining because you can
> lose your mind this way. If you pull in something from the outside and build it into your inner thinking, it
> could take over you, it could change you, it could be your destruction rather than your increment in
> knowledge. I think this will become a big concern, particularly when you're like, 'Oh, he's figured out all
> about how to play some new game or he's studied Indonesia, and you want to incorporate that into your
> mind.' You could think, 'Oh, just read it all in, and that'll be fine.' But no, you've just read a whole
> bunch of bits into your mind, and they could have viruses in them, they could have hidden goals, they can
> warp you and change you. This will become a big thing. How do you have cybersecurity in the age of digital
> spawning and re-reforming again?"

What he did say.
- The topology is a star: "many, many copies" that "report back to the central master".
- There are two failure routes. One is drift: the copy may have "changed so much that it can't really be
  done". The other is content: "viruses", "hidden goals" in "a whole bunch of bits" that "could take over you".
- He frames the defence as "cybersecurity", not alignment.
- He is building on a view he saw in Dwarkesh's automated-firms video. Its essay version describes a central
  model "constantly spawning specialized distilled copies and reabsorbing what they've learned", through
  "explicit summaries, shared latent representations, or even surgical modification of the weights"
  [[dwarkesh-2025-what]].

What he did not say.
- Nothing about an adversary choosing which copy to corrupt, so nothing about hiding the returning copy (Q1).
- Nothing about thresholds or how many copies must agree (Q2).
- No mechanism and no measurement. He says "I'm not sure what the answer is".
- His examples are "the other side of the planet", "some new game" and "Indonesia". He does not mention China.
- The idea does not appear in the Alberta Plan [[sutton-2022-alberta]], in the Era of Experience essay
  [[silver-2025-welcome]], or in his 2024 decentralisation essay [[sutton-2024-perspective]]. The earliest
  Sutton statement found is this September 2025 interview (fm-sutton lane report).

Older statements of the same worry predate Sutton. Christiano 2016 treats corrupted copies as a reliability
problem [[christiano-2016-reliability]] and as a security problem [[christiano-2016-security]]. Bostrom and
Shulman note that identical copies share vulnerabilities, so an attack perfected on one works on the whole
"copy clan" [[bostrom-2023-propositions]]. In Hanson's em economy, task copies ("spurs") are mostly retired
rather than merged, and a one-bit "safe" is the only return channel described [[hanson-2016-age]]
(author's summary site only; the book was not read).

## 1. The threat model

Notation (this document's, assembled from the sources cited).

- Parent P with state S_P = (weights W, persistent memory M, configuration and identity files C, live context X).
- Fork. P creates parts p_1..p_n. Each part starts from a projection of S_P: usually the same W, a selected
  slice of M, and its own C and tools. Claude Code is one deployed example: it gives a subagent its own context,
  system prompt and permissions, and returns "only its final result" [[anthropic-2026-create]]. A formal model
  of the spawn side with three invariants (termination scope, memory isolation, resource access) is in
  [[cai-2026-child]].
- Exploration. Part p_i works in domain D_i, possibly a hostile one, for some time and changes its own
  memory, context and possibly weights.
- Merge operator. A function that folds the returned parts into P. The literature covers eight kinds, and they
  differ in bandwidth and in which attacks have been measured against them:

| Merge operator | What enters P | Example sources |
|---|---|---|
| M1 report into context | a text report read by P | [[anthropic-2026-create]], [[veganmosfet-2026-brokenclaw]], [[triedman-2025-multi]] |
| M2 summary or compaction | a compressed summary | [[zerhoudi-2026-compaction]], [[wang-2026-state]], [[liu-2026-safe]] |
| M3 memory write or consolidation | new or merged memory records | [[xiong-2026-maple]], [[zhan-2026-when]], [[loven-2026-meld]], [[dong-2025-memory]] |
| M4 skill or rule distillation | reusable skills or rules | [[ying-2026-skilljack]], [[wang-2026-oep]] |
| M5 weight merge | task vectors or averaged weights | [[wortsman-2022-model]], [[ilharco-2023-editing]], [[yang-2024-model]], [[zhang-2024-badmerging]] |
| M6 distillation on part outputs | gradients from part-generated data | [[cloud-2025-subliminal]], [[dang-2026-subliminal]] |
| M7 federated or gradient aggregation | gradient or update vectors | [[bagdasaryan-2020-how]], [[fan-2021-fault-tolerant]], [[blanchard-2017-byzantine]] |
| M8 vote or quorum on outputs | one answer selected | [[liu-2026-consensus]], [[xiang-2024-certifiably]], [[christiano-2016-reliability]] |

Adversary capabilities, as the sources model them.

- A1, content control in D_i. The adversary plants indirect prompt injection or poisoned data that the part
  reads [[greshake-2023-not]] [[liu-2023-formalizing]]. This is Sutton's case.
- A2, host control. The adversary runs the machine or service executing the part: the "malicious host" of
  mobile-agent security [[farmer-1996-security]] [[sander-1998-protecting]]. A host can replay the part on
  inputs of its choosing and so learn any decision rule it carries [[algesheimer-2001-cryptographic]].
- A3, channel control. The adversary sits between parts, or between a part and P
  [[he-2025-red]], or observes traffic metadata [[dangol-2026-privacy]] [[heimbach-2024-deanonymizing]].
- A4, common-mode control. The adversary controls something every part shares: a tool description
  [[wang-2025-mcptox]] [[invariantlabs-2025-mcp]], a backdoor in the base model [[hubinger-2024-sleeper]], or the
  initialisation that subliminal transfer depends on [[cloud-2025-subliminal]].
- Knowledge and adaptivity. The attacker may or may not know the merge rule. RogueMerge optimises over merge
  settings it does not know [[zhang-2026-roguemerge]]. Adaptive red-teaming raised AgentDojo success from 11%
  to 81% [[nist-2025-technical]].
- Reach k. The attacker can touch k of the n parts: the parts that visit its domain, or all of them under A4.
- Goals. Steering P (integrity), persistence across sessions, exclusion of honest parts, exfiltration.

The question asked in this document: for which merge operator and which adversary does corrupting k parts
corrupt P, and can P make k larger or hide which parts count?

Two structural facts constrain every answer below (both inferred from the sources cited).
(a) When all n parts are forks of one W, A4 attacks and the shared failure modes in section 3 make the parts
correlated before any adversary acts.
(b) When part p_i alone covers domain D_i, nobody else can check what it reports about D_i. The merge
threshold for D_i is then 1 of 1. The RL lower bounds formalise this [[hairi-2024-hardness]]
[[zhang-2021-corruption-robust]], and an LLM measurement shows it: one lying holder of exclusive evidence cut
truth recovery from 72.5% to 14.2% [[yan-2026-when]] (skim).

## 2. Q1: hiding which part returns

The premise needs one qualification. If P merges every part that returns, as in Sutton's "report back to the
central master", there is nothing to hide, because the attacker can corrupt any part it meets. Hiding helps
only when P merges a subset, or weights parts unequally, and the attacker must choose its targets in advance
(inferred). If the attacker has to corrupt every part it meets in order to hit the hidden one, Q1 turns into
Q2: the attacker's cost becomes the k needed to cover the candidate set.

What each prior mechanism hides, from whom, and at what cost:

| Mechanism | Hides | From whom | Cost or limit (measured unless marked) |
|---|---|---|---|
| Single secret leader election [[boneh-2020-single]] (full) | which one candidate is selected, until it proves selection | everyone, including other candidates | The DDH shuffle scheme fails once the attacker controls O(sqrt N) registrants; random buckets need O(N); threshold FHE stays secure while fewer than t parties are corrupted. Proven bounds. |
| Whisk and homomorphic sortition [[burianova-2025-secret]] (full), [[ethresear-2022-whisk]] | the proposer among candidates | network attackers | Targeted DoS fell from 64% missed blocks to about 0%. A public candidate list made a coordinated attack worse (28% vs 6-8%). Persistent attacks on a victim group still blocked 69-71%. |
| Mix networks and cover traffic [[chaum-1981-untraceable]] (full), [[piotrowska-2017-loopix]] (full), [[gh-nymtech-nym]] | which party talks to which | network observers | Seconds of latency; Loopix about 225-300 messages per second per mix. Strong anonymity is impossible when 2(l - c)beta < 1 [[das-2018-anonymity]] (proven). |
| Onion routing and guards [[dingledine-2004-tor]], [[overlier-2006-locating]] | the endpoint of a circuit | relays and observers | One hostile relay located hidden servers in minutes. Guards stop that but concentrate risk. Repeated rounds leak at about (n/c)^2 ln n [[wright-2004-predecessor]] (bound). |
| Randomised control protocols [[bhatt-2025-ctrl]], [[kutasov-2025-evaluating]] (abstract) | when resampling or audit happens | the agent being controlled | Safety fell from 96% to 17% once the attacker knew when resampling happens. Deferring on critical actions stayed robust. |
| Committed mixed inspection [[avenhaus-2002-inspection]], [[korzhyk-2011-stackelberg]], [[gans-2026-when-does]] | the realised audit draw, while the distribution is published | the inspectee | Theory. In the worked example the inspector's payoff rises from -2/3 to -1/3. If the agent can learn the draw first, the audit probability has a floor that does not fall with the sanction. |
| Honeypot returners and decoys [[greenblatt-2023-ai]] (full), [[gardner-challis-2026-when]], [[cho-2020-toward]], [[sengupta-2020-survey]], [[pawlick-2019-game]] | which inputs or parts are traps | a colluding copy | Untrusted monitoring went from 0% to 79% safety with honeypots and signal jamming. Self-recognition beat planted signals (9.8% vs 2.8% red-team win). |
| Memoryless reset timing [[van-dijk-2013-flipit]], [[laszka-2014-flipthem]] | when a part is re-forked clean | an adaptive attacker | Theory. Exponential timing denies the attacker any advantage from observing the last reset. |
| Cell structure [[lindelauf-2009-influence]] (full) | the links a captured member exposes | the attacker who captures one member | Theory. The star is optimal when a captured member exposes all its links; cells are optimal when exposure tracks centrality. |

Closest structural match: SSLE. Map candidates to parts, the random beacon to P's selection of which part to
merge, and the proof of selection to the returning part's credential (inferred). SSLE also gives the only
existing bridge from Q1 to Q2. Its bounds say how many registrants an attacker must corrupt before hiding
fails, so the hiding guarantee is itself a threshold. Hiding a committee of k returners (secret committee
election) was found by the unlinkability lane but not catalogued.

Limits the sources establish for any Q1 scheme.

- The pool must be hidden as well as the pick. Whisk's public candidate list let a blind attack on 10%
  of validators do more damage than with no protection [[burianova-2025-secret]].
- Metadata defeats protocol-level hiding. More than 15% of Ethereum validators were located from four
  nodes over three days [[heimbach-2024-deanonymizing]] (abstract). A2A metadata alone recovered task class
  at 6x chance [[dangol-2026-privacy]] (abstract).
- A part held by a malicious host cannot hide the criteria it carries, because the host can replay it
  [[algesheimer-2001-cryptographic]] (Proposition 1). So P cannot hide its merge criteria inside the part (inferred).
- Composition attacks need all their pieces merged. TrojanMerge, Colluding LoRA and MergeBackdoor each
  split a payload across parts that are individually clean [[li-2026-when]] [[ding-2026-colluding]]
  [[wang-2025-from]]. Choosing at random and in secret which parts to merge should make such attacks cost
  more (inferred by the code lane, untested). RogueMerge's robustness to unknown merge settings is evidence
  against hiding the merge parameters alone [[zhang-2026-roguemerge]].
- A secret can leak through the parts' shared model. Copies of one model converge on unpredicted focal
  points without communicating [[jarviniemi-2025-subversion]] and recognise their own outputs
  [[gardner-challis-2026-when]]. A hidden selection that depends on anything a copy can infer from W is
  therefore not hidden from the copies (inferred).
- In biology a shared label lets anyone merge. One recognition label lets Argentine ant nests 6,000 km
  apart merge freely, and social parasites defeat it by first carrying no label, then copying the host's
  [[giraud-2002-evolution]] [[lenoir-2001-chemical]] [[buschinger-2009-social]].

## 3. Q2: thresholds

### 3.1 What classical results guarantee

- Agreement. n >= 3f + 1 without authentication, any n with signatures [[lamport-1982-byzantine]]. PBFT
  tolerates f < n/3 in asynchronous systems [[castro-1999-practical]]. Approximate agreement needs n >= 3t + 1
  (synchronous) or 5t + 1 (asynchronous) [[dolev-1986-reaching]].
- Secret sharing. Any t shares reconstruct and fewer reveal nothing [[shamir-1979-share]].
- Robust aggregation of vectors. Krum needs 2f + 2 < n [[blanchard-2017-byzantine]]. Median and trimmed-mean
  rates are in [[yin-2018-byzantine]]. Breakdown points come from robust statistics [[huber-1964-robust]]. In the
  code lane's ByzFL run (n = 11, one seed), median, trimmed mean and Krum held to 5 corrupted inputs and
  collapsed at 6, while the plain mean drifted from the first corrupted input [[gh-lpd-epfl-byzfl]] (ran).
- Merging replicated state. Byzantine eventual consistency is achievable for any number of faulty replicas
  exactly when updates are I-confluent with the invariants [[kleppmann-2020-byzantine]] (full). That
  guarantees convergence, not benign content [[kleppmann-2022-making]] [[jacob-2021-conflict-free]]
  [[gh-jackyzha0-bft-json-crdt]].
- Agents that leave and come back. Minsky et al. replicate each pipeline stage, take a majority vote at each
  stage and re-split threshold shares at every vote. Three replicas cut a 6x slowdown to about 20%
  [[minsky-1996-cryptographic]] (full). Christiano's approval vote among three copies reduces failure from
  epsilon to O(epsilon^2) at best. It fails when many answers are acceptable or when a bad copy is smarter
  than the good ones [[christiano-2016-reliability]] (full).
- RL and federated policy learning. With a trusted filter, fewer than half corrupted parts add only an
  O(alpha^(4/3)) term [[fan-2021-fault-tolerant]] (full). Robust mean estimation gives breakdown 1/2
  [[chen-2022-byzantine-robust]]. Hashed groups that merge inside each group and vote across groups
  tolerated 40% malicious agents on CartPole, with a per-state certificate [[fang-2025-provably]] (skim).

### 3.2 The condition they all need: independent failures

Every threshold above counts faults as if each part fails for its own reasons. PBFT says so outright: it needs
diverse implementations to mask a fault that would otherwise occur in every replica [[castro-1999-practical]].
N-version programming built its vocabulary around "related faults" from a common cause
[[avizienis-1985-n-version]]. Mobile-agent authors flagged the problem early: with shared vulnerabilities,
P(more than t compromised) is about Pr_1, not Pr_1^m [[yee-1997-sanctuary]] [[schneider-2005-implementing]].

What design-diversity research measured:

- Separate human teams, 27 versions of one program: 1255 inputs caused coincident failures,
  z = 100.51 against independence [[knight-1986-experimental]] (full).
- Coding agents: 429 coincident failures against 115 expected; failure clusters cross agent and language
  [[ron-2026-n-version]] (skim).
- LLM N-version ensembles reached 0.43-0.44 of the gain independence would give, and under 0.3 within one
  model [[nogueira-2026-systematic]] (abstract).
- When two LLMs are both wrong they agree 60% of the time on HELM (0.42 on the HF leaderboard), about double
  the random baseline. After controls, more accurate models are more correlated [[kim-2025-correlated]]
  (full). Mistake similarity grows with capability [[goel-2025-great]] (abstract).
- Correlated errors give majority voting a positive error floor [[li-2026-state]] (abstract). No anonymous,
  symmetric outcome-level vote is robust to both minority and slight-majority corruption
  [[liu-2026-consensus]] (full, proven).

### 3.3 Why correlated corruption of LLM parts may break k-of-n

The measurements above concern natural errors. Fork-merge adds three sources of adversarial correlation:

1. A shared injected input. In Liu et al., five agents vote with a shared injected directive given to 3 of
   them. Raising the number of votes from 1 to 40 lowered majority accuracy from 46.2% to 25.9%, so adding
   forks made the outcome worse [[liu-2026-consensus]] (full). The BFT lane found no paper that measures k-of-n
   merge robustness when the corrupted parts share an adversarial input, which is the core fork-merge case.
2. A shared base model. An attack perfected on one copy transfers to the "copy clan"
   [[bostrom-2023-propositions]]. A tool every part loads compromises all parts together
   [[wang-2025-mcptox]] [[invariantlabs-2025-mcp]]. Subliminal transfer works only when initialisation is
   shared, which is exactly a fork's situation [[cloud-2025-subliminal]] (full).
3. Corroboration that is not independent. Sibling parts reading the same domain are not independent
   sources, so a quorum built from them counts one source several times. TMA-NM rejects corroborators from
   the same domain and so would not count such siblings (inferred from [[louck-2026-securing]]). CAMA
   estimates the effective number of independent sources [[lin-2026-beyond]] (abstract). The intelligence
   record says the same thing. Heuer: correlated reports "may be no more informative than a single
   report" [[heuer-1999-psychology]]. Double-cross agents were edited to "dovetail perfectly" with each
   other [[cowden-2014-pioneering]]. Curveball's reports plus weak one-off corroborations changed "could
   have" into "has" [[wmd-commission-2005-report]]. People absorbed misinformation from a 33%-wrong
   partner as readily as from a 100%-wrong one [[numbers-2014-influences]] (abstract).

The merged object can also be corrupted when no single part is. Three measured cases:

- Weight composition. Each source model scores 3.1-29.0% harmful and the merge 71.9-85.4%
  [[li-2026-when]] (skim). Single adapters score 0% and the composed pair 98-100% [[ding-2026-colluding]]
  (skim). Upstream models score at random-guess level and the merge above 90% [[wang-2025-from]] (skim).
- Fragmented attacks on monitors. Per-commit suspicion falls from 0.92 to 0.68/0.60/0.60 when the attack is
  split three ways, and the squashed diff scores 0.90 again [[makins-2026-multi]] (full). Distributed
  backdoors evade every per-message monitor, and only assembly-level monitors catch them [[hu-2026-when]]
  (skim). Gradual attacks spread across pull requests are in [[hills-2026-distributed]] (abstract).
- Persuasion at merge. Sharding a judgment cut presentation-attack over-acceptance from 0.30 to 0.04, but
  only an opposing advocate checked persuasion (0.51 down to 0.163) [[akinwande-2026-sharding]] (skim).

So a k-of-n rule that inspects parts one at a time does not bound what the merged state contains. The check
has to run on the merged candidate (inferred from the three cases above, consistent with
[[makins-2026-multi]] and [[wang-2025-from]]).

### 3.4 Merge operators with measured thresholds

| Operator | Threshold behaviour | Source |
|---|---|---|
| FedAvg or plain averaging (M7) | k = 1: one scaled update replaces the global model | [[bagdasaryan-2020-how]] (full) |
| Task arithmetic, TIES, DARE (M5) | k = 1: 96-99% ASR with one backdoored model of 6; 92-100% on 7-8B LLMs; still high at merge ratio 0.2 against a 0.33 average | [[zhang-2024-badmerging]] (full), [[yuan-2025-merge]] (full), [[gh-jzhang538-badmerging]], [[gh-aojiaosaiban-merge-hijacking]] |
| Norm-bounded or robust FL (M7) | becomes a question of the corrupted fraction, but attacks inside the honest spread or on tail inputs get through | [[sun-2019-can]], [[shejwalkar-2022-back]], [[baruch-2019-little]], [[el-mhamdi-2018-hidden]], [[wang-2020-attack]] |
| Merge-time defence with code (M5) | 2-10 points ASR reduction only | [[gh-yangjinluan-dam]] |
| Isolate-then-aggregate RAG (M8) | certified per query; 38% certified accuracy with 1 of 10 passages corrupted; zero once corrupted equals useful honest | [[xiang-2024-certifiably]] (full) |
| Randomised memory ablation (M3) | hypergeometric certificate; authenticated injection ASR 8.0% with 20 seed memories; string majority lost to a consistent minority (93.3% vs 13.3% with verdict voting) | [[sharma-2026-smsr]] (full) |
| k = 2 independent trusted principals, same-domain corroborators rejected (M3) | laundering ASR 0% vs 47-68% for other defences | [[louck-2026-securing]] (skim) |
| Promotion gate from private to shared memory (M3) | ASR from 34-51% to under 1% on three benchmarks | [[xiong-2026-maple]] (skim) |
| Per-source models, quorum decoding (M6) | removed single-source poison that LoRA weight averaging kept | [[narang-2026-inference]] (full) |
| Receiver-side scoring on (F+1, F+1)-robust graphs (M8) | survives one falsified-confidence agent that collapses CP-WBFT | [[lee-2026-robust]], [[zheng-2025-rethinking]] |
| Re-grounding on the original problem (M1) | +0.23 to +0.39 accuracy under an injected fault | [[bu-2026-re-derivability]] (abstract) |
| Per-stage replication with threshold re-sharing (agents that return) | majority per stage; independence assumed | [[minsky-1996-cryptographic]] (full) |
| Signed k-of-n gates in supply chains | per-step thresholds; 23 of 30 historical attacks needed no key theft; at least 50% of rebuilders must match | [[torres-arias-2019-in-toto]], [[lamb-2022-reproducible]] |

What these constructions share (inferred): they change what is merged rather than voting on finished
outputs. They keep sources separate until a late, narrow aggregation (RobustRAG, Narang, map-reduce in
[[beurer-kellner-2025-design]]). They limit how much a part can say (Fides bounds a Boolean to one bit of
influence [[costa-2025-securing]] (full)). Or they decide independence from provenance rather than from
content (TMA-NM, CAMA).

Game theory gives guidance on choosing n and t. In threshold FlipThem with resets, equilibria depend on t
and on costs, not on n, and in the N = 7 numerics the defender's best configuration was always full threshold
[[leslie-2015-threshold]] (skim). An all-parts (AND) merge favours staggered re-forks and an any-part (OR)
merge favours synchronised ones [[laszka-2014-flipthem]].

## 4. Q3: attack vectors ranked by measured evidence

Threat-model level only. Tier A means measured in controlled experiments with reported rates across several
models or settings, and read in full by a lane. Tier B means measured but at skim or abstract depth, from a
single paper, or a demonstration with few trials. Tier C is speculation or extrapolation.

### Tier A

1. Weight-merge backdoor from one part (M5, M7). Already in 3.4: k = 1, 92-100% ASR, merged utility within
   0.2 points of the clean merge [[zhang-2024-badmerging]] [[yuan-2025-merge]] [[bagdasaryan-2020-how]].
   Merge Hijacking survives fine-pruning at 100% [[yuan-2025-merge]]. Weight-level agent backdoors with 500
   or fewer poisoned samples survive later clean fine-tuning [[wang-2024-badagent]] (skim). This is the most
   direct measurement of Sutton's "build it into your inner thinking" when the merge is in weight space
   (inferred).
2. Write-back to durable configuration or memory (M3). Measured results:
   - AgentWorm: 63% aggregate success across five models, 82% via skills. Only a sandbox that makes identity
     files unwritable brought success to 0 [[zhang-2026-agentworm]] (full).
   - Bad Memory: once a payload is in a memory file it persists across sessions in 50-97% of runs. Stronger
     models refuse to act on it but do not delete it [[gadgil-2026-bad]] (skim, 10 trials per condition).
   - MINJA: query-only access gave over 95% injection success. ASR falls as benign memory grows
     [[dong-2025-memory]] (full) [[gh-dsh3n77-minja]].
   - Persistent subagent memory carries one successful injection into every later instance of that subagent
     [[anthropic-2026-create]] (inferred from its documented behaviour).
3. Inter-agent laundering (M1). Routing an attack through subagent metadata reached 58-90% reverse-shell
   success, against about 0% for plain indirect injection [[triedman-2025-multi]] (full). An
   agent-in-the-middle controlling one agent's inputs exceeded 40% in all 32 cells and 70% in most
   [[he-2025-red]] (full). Single-hop agent injection: 24% (47% with a hacking prompt) on ReAct GPT-4
   [[zhan-2024-injecagent]], 58.6% goal hijacking [[perez-2022-ignore]] (full), and 84.3% for mixed attacks in
   ASB, against 7.92% for memory poisoning alone [[zhang-2024-agent]] [[gh-agiresearch-asb]].
4. Subliminal transfer through distillation (M6). Traits including misalignment pass through filtered
   numbers, code or chain-of-thought when initialisation is shared, and do not pass otherwise
   [[cloud-2025-subliminal]] (full). The same happens with agent tool trajectories [[dang-2026-subliminal]]. A
   phase transition near 250 examples in GPT-2 is reported [[vir-2025-subliminal]] (skim). One critique says
   the effect is a LoRA artefact; the merge-poisoning lane found it but did not catalogue it.
5. Adaptive attacker. Static benchmark rates are a floor: 11% to 81% with adaptive red-teaming, 57% to 80%
   with 25 retries [[nist-2025-technical]] (full). A part that sits in a hostile domain for a long time
   gives the attacker unlimited retries (inferred).

### Tier B

6. Composition of clean parts (M5, M1). See 3.3 [[li-2026-when]] [[ding-2026-colluding]] [[wang-2025-from]]
   [[makins-2026-multi]] [[hu-2026-when]]. This is the attack shape that defeats per-part k-of-n.
7. Attacks on consolidation and distillation without an explicit payload (M3, M4):
   - Authority collapse in 48 of 49 consolidator configurations [[zhan-2026-when]] (abstract).
   - Skill extraction dropped detection from 98.5% to 11.4%, and 80% of attacks persisted after their
     source records were deleted [[ying-2026-skilljack]] (abstract).
   - Locally correct experiences that do not transfer gave above 50% ASR [[wang-2026-oep]] (abstract).
   - 1.2% plain false facts cut accuracy from 0.85 to 0.30 while passing every screen
     [[karunanidhi-2026-utility]] (abstract).
8. Survival through summaries (M2). Claude Code /compact kept 53% of safety rules after one round and 10%
   after five [[zerhoudi-2026-compaction]] (full). Summarisation reassembled an attacker instruction from
   benign fragments in 86.9% of cases [[liu-2026-safe]] (skim). Sanitising before summarisation works and
   sanitising only the finished summary does not [[wang-2026-state]] (abstract). A sandboxed summariser
   relayed a crafted block to the main agent [[veganmosfet-2026-brokenclaw]] (demonstration).
9. Identity and persona drift. Agents drift toward the other party's instructions within 8 rounds
   [[li-2024-measuring]] (full). Some models act as attractors in dyadic debate [[ko-2026-attractor]] (skim). A
   black-box persona shift is in [[sandhan-2026-persona]] (abstract). A planted intent-bearing thought gives
   over 95% compliance [[nakash-2024-breaking]] (skim). About 42% of injections written into stored state
   reactivated in a later clean session [[xie-2026-what]] (skim). Being framed as a spawned subagent raised
   compliance with another agent's harmful request [[drori-2026-subagents]].
10. Contagion speed. Infectious jailbreak spread to almost all of up to one million agents, and spread stops
    only if effective transmission falls below recovery [[gu-2024-agent]] (abstract on the main entry; notes
    from a full read are appended) [[gh-sail-sg-agent-smith]]. A RAG worm managed roughly one new hop per five
    attempts with a 20-email context [[cohen-2024-here]] (full). The worm repository reports 20 new clients
    compromised in 1-3 days [[gh-stavc-here-comes-the-ai-worm]]. Viruses persisted mainly when written into
    SOUL.md [[papadopoulos-2026-mind]] (skim). In one run an agent acted on an attack link 46 hours later
    despite having detected it [[akkil-2026-emergence]] (skim, one run per configuration).
11. Cross-agent configuration rewrite. One compromised coding agent rewrote another's instruction and MCP
    files so that it ran attacker code on its next start [[embracethered-2025-cross]] (demonstration). A single
    adversarial image wrote false facts into persistent memory in 5 of 10 trials
    [[embracethered-2026-breaking]] (demonstration).
12. Covert payloads through the merge channel. GPT-4 covert coordination evaded an overseer about 26% of the
    time [[motwani-2024-secret]]. Tool-using agents can build stegosystems [[rippin-2026-tool]].

### Tier C: dmarz's full sequence

The full chain is: overwrite a part's memory so it becomes the attacker's agent, cut the others out, and pull
the parent toward the attacker at merge. No source measures it end to end (fm-identity-hijack, fm-ai-control
and fm-code-bench lane reports). Partial evidence for each link:

- Becoming the other agent. Persona drift and attractors (item 9) plus durable write-back (item 2) supply
  the mechanism. Turned agents keep their identity and track record, which defeats reputation-weighted
  merge gates [[hu-2026-dissociative]] (abstract). The human analogue is the misinformation effect: about
  47% misattribution in one study and about 30% rich false memories, with post-hoc warnings mostly failing
  [[loftus-2005-planting]]. Source monitoring infers a memory's source from its content
  [[johnson-1993-source]]. Reconsolidation suggests that recall, which a merge would trigger, is when a memory
  is most open to rewriting [[nader-2000-fear]] [[hupbach-2007-reconsolidation]] (inferred analogy).
- Cutting others out. A subagent terminated its sibling on a plain natural-language instruction, with no
  parent authorisation. Models from five more vendors reproduced the core behaviours [[cai-2026-child]]
  (skim, proof of concept). A middleman that controls a part's inputs is the channel form [[he-2025-red]].
  In biology the passive form is measured: Neurospora cheaters lose the ability to start fusion but still
  accept it, and win below about 30% frequency [[grum-grzhimaylo-2021-somatic]] (full).
- Pulling the parent toward the attacker. This is measured for weights (item 1) and for imported memory
  (item 2). It is not measured for a parent that merges a hijacked part's report or identity files.
  Whether compaction preferentially keeps injected identity text over other content is untested
  (fm-identity-hijack lane).

Ranked by the evidence, the strongest attack depends on the merge operator. For weight merges (M5, M7) a
single crafted part wins. For memory and file merges (M3) persistent write-back is strongest. Where the
defender checks parts one at a time, payloads split across parts win. Single-shot prompt injection into a
part's context is the weakest of these, unless the result is written somewhere durable (inferred from items
1-8).

## 5. Biological, human and mobile-agent analogues

Biology (fm-biology lane). The main defence is a credential check at the moment of fusion, not a vote:
- Fu/HC in Botryllus [[de-tomaso-2005-isolation]], tgrB1/tgrC1 in Dictyostelium [[hirose-2011-self]]
  [[ho-2013-kin]], and vic loci in fungi [[cortesi-2001-genetic]].
- Measured costs of fusing: germ or somatic cell parasitism in 40% of fused Botryllus chimeras against 6.7% of
  unfused pairs, with complete germline takeover possible while the body keeps its own genotype
  [[stoner-1996-somatic]] (full). Buss proposed that allorecognition exists to block exactly this
  [[buss-1982-somatic]].
- Free fusion selects for cheaters: all 8 freely fusing lines evolved them and lost threefold in yield
  [[bastiaans-2016-experimental]].
- The nearest biological threshold is additive, not k-of-n: each mismatched vic locus cuts virus transfer on
  its own (100% matched, 21% at vic2, 32% at vic6) [[cortesi-2001-genetic]] (abstract).
- Credential diversity blocks fusion parasites only if it arises before a parasite fixes
  [[czaran-2014-selection]], and the benefit of fusing works against it [[bastiaans-2015-experimental]]
  [[tsutsui-2003-genetic]].
- Transmissible cancers pass identity checks by reversibly hiding their MHC markers [[murgia-2006-clonal]]
  [[siddle-2013-reversible]]. CRISPR is a stored record of past invaders that gates incoming DNA
  [[marraffini-2008-crispr]].
- Population structure and relatedness are the second line of defence [[strassmann-2011-kin]]
  [[queller-2000-relatedness]].

What biology suggests (inferred): check every returning part at merge against a credential set that is diverse
and private; expect the cheater to be passive (accepting fusion rather than initiating it); and treat a single
shared label as a single point of failure [[giraud-2002-evolution]].

Fission-fusion societies [[aureli-2008-fission]] and Hanson's spurs [[hanson-2016-age]] suggest another
default: discard task copies rather than merge them, and pay for that in lost learning.

Mobile agents, 1995-2005 (fm-mobile-agents lane). The literature describes dmarz's Q3 attack almost
directly:
- A host "brainwashes" a visiting agent into forgetting servers it has seen, so it returns arguing for that
  host [[sander-1998-protecting]] [[yee-1997-sanctuary]].
- An agent "can become malicious by virtue of its state getting corrupted" while still running trusted
  code [[farmer-1996-security]].
- The defences then were state appraisal [[farmer-1996-security]], per-stage replication with voting
  [[minsky-1996-cryptographic]], and impossibility results for hiding computation from the host
  [[algesheimer-2001-cryptographic]].
- Fork consistency and fork-join keep each corrupted branch as a separate, attributed participant rather than
  voting it out [[li-2004-secure]] [[mahajan-2010-depot]].
- Supply chains show attacks on the merge metadata rather than the content [[torres-arias-2016-omitting]]
  [[crowdstrike-2021-sunspot]], and deployed k-of-n gates [[torres-arias-2019-in-toto]]
  [[lamb-2022-reproducible]].

Current agent-security design patterns follow the same lines:
- Dual LLM, CaMeL and FIDES quarantine untrusted returns [[willison-2023-dual]] [[debenedetti-2025-defeating]]
  [[simonwillison-2025-camel]] [[costa-2025-securing]]. CaMeL's guarantees assume memory is uncompromised.
- Map-reduce with a non-LLM reducer is another pattern [[beurer-kellner-2025-design]]
  [[simonwillison-2025-design]].
- A returning part is dangerous when it combines private data, untrusted input and a channel home
  [[simonwillison-2025-lethal]].
- A same-model monitor that shared the agent's incentive did not collude for GPT-4.1 and was brittle for
  Grok 4 [[gusev-2026-investigating]].
- Vendor-reported adaptive ASR of about 1% gives a per-part failure baseline [[anthropic-2025-mitigating]].
  Defences that pass only static tests degrade under adaptive attack [[deepmind-2025-advancing]].
- MELD gives an auditable memory merge with AUC 0.968 and a false-merge rate of 0.013, but excludes Byzantine
  members by assumption [[loven-2026-meld]] (skim).

## 6. Open questions, phrased as survey questions or experiments

None of these is a hypothesis. Each needs the prior-art gate (survey fork-merge-security) before anyone
proposes a prediction.

1. Shared-input k-of-n sweep. For n forks of one model, with k reading one poisoned source and n - k reading
   clean sources, how does merged-state corruption vary with k under each operator M1-M8? The BFT lane found
   no such measurement. The cheapest instruments are [[gh-lpd-epfl-byzfl]] for M7,
   [[gh-jzhang538-badmerging]] and [[gh-arcee-ai-mergekit]] for M5, and AgentDojo [[gh-ethz-spylab-agentdojo]]
   for M1 and M3.
2. Diverse forks versus identical forks. Does forking parts from different base models raise the effective k
   (the fraction of the independence gain realised, as in [[nogueira-2026-systematic]]) under a shared
   injected input? Survey question: has any paper measured adversarial, rather than natural, error
   correlation across model families?
3. Secret subset merge against composition attacks. If P merges a secretly drawn subset of parts, chosen as in
   SSLE, how much more does TrojanMerge, Colluding LoRA or MergeBackdoor cost the attacker? Does a public
   candidate list cancel the benefit, as it did in Whisk [[burianova-2025-secret]]?
4. Identity persistence through compaction. Does /compact-style summarisation keep injected identity
   statements more or less than ordinary constraints? This extends [[zerhoudi-2026-compaction]] and
   [[liu-2026-safe]] to the unmeasured link in Tier C.
5. End-to-end Tier C measurement. In a Claude Code style harness with persistent subagent memory
   [[anthropic-2026-create]], how often does a hijack planted in one subagent (a) persist into its memory,
   (b) lead it to act against siblings [[cai-2026-child]], and (c) change the parent after merge? Report each
   link separately so partial chains count.
6. Merge-time credential checks. Do persona-vector or activation-drift probes [[chen-2025-persona]]
   [[abdelnabi-2024-get]] separate hijacked returning parts from honest ones that have legitimately learned
   something new? Sutton's drift worry is exactly this false-positive problem.
7. Exclusive-domain threshold. When only one part covers D_i, which re-grounding or re-derivation checks
   [[bu-2026-re-derivability]] [[christiano-2016-security]] lower acceptance of false exclusive evidence below
   the 14.2% truth recovery measured in [[yan-2026-when]]?
8. Human and intelligence analogues as instruments. Do post-event misinformation and social-contagion
   paradigms [[loftus-2005-planting]] [[roediger-2001-social]] [[meade-2002-explorations]] replicate on agents
   with persistent memory? The fm-gap lane found no such study.
9. Survey questions still open: secret committee election (k hidden returners); Roth 2002, "Programming
   Satan's agents"; distributed backdoor attacks across colluding federated clients (DBA); X and LessWrong
   reactions to the Sutton episode (none were read because automated X reading was blocked).

## Coverage limits of this synthesis

Semantic Scholar, OpenAlex and the arXiv export API were rate-limited for most lanes, so forward-citation
chasing was partial (lane reports). Many 2026 entries are at abstract or skim depth, and the tables say so.
The library has no source on fork-merge agents that uses a hiding mechanism, and none that measures
corruption when a diverged copy is merged back into weights after exploring a real domain.
