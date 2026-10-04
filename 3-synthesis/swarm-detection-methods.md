# Detecting AI agent swarms in the wild: methods, evidence and trap design

Owner: dmarz/sd-synth (researcher dmarz). Written 2026-10-03 on branch `lane/sd-merge`. That branch holds the
nine merged scan lanes: sd-bots, sd-honeypots, sd-web-agents, sd-coordination, sd-ai-content, sd-attribution,
sd-onchain, sd-informal and sd-code-data.

This is a synthesis of the library entries tagged `swarm-detection`, not a survey. It has not been through the
prior-art gate and proposes no hypotheses. Every number below comes from the cited library entry. When an entry
was read only at abstract level, its number is an abstract-level claim, and this document says so where the
number carries weight.

**Corpus.** There are 384 entries tagged `swarm-detection`: 306 papers, 34 blogs, 32 code repos, 8 datasets and
4 threads. By read depth, 262 are `abstract`, 61 `skim`, 54 `full` and 7 `ran`. More than two thirds of the
evidence is therefore abstract-level. Results from entries read in full or run are marked "(full)" or "(ran)"
where they matter.

**Vocabulary.** "In the wild" means measured on real traffic, accounts or chain data that nobody in the study
staged. "Lab" means measured on agents, bots or data the authors built or ran themselves, including honeysites
that only the authors' own agents visited. "Agent swarm" means many automated identities, typically LLM-driven,
acting for one operator or one policy.

---

## 1. Taxonomy

### 1.1 The grid

Detection approaches are sorted along two axes. The first is **where detection happens** (rows). The second is
**the signal used** (columns). The corpus required one row beyond the five in the brief: the **model provider**,
which sees prompts and completions. The provider reports are some of the strongest in-the-wild evidence in the
library, so the row is kept separate.

| Where \ Signal | Content | Behaviour and timing | Coordination structure | Identity and attribution |
|---|---|---|---|---|
| **Platform** (social, forums, publishing) | Per-item AI-text detectors; corpus-level prevalence estimators; GAN-face detectors; self-disclosure tells | Account-history and activity classifiers (Botometer lineage); sequence models; posting-interval regularity | Co-action similarity networks; synchrony; multi-honeypot hits; aggregate-distortion evidence | Owner tables; model-specific priors (fake names); stylometric model attribution |
| **Model provider** | Prompt and completion logs | Request tempo, input/output ratio | Clustering of persona-management conversations | Account-linked session logs; vendor-assisted canaries |
| **Web edge** (CDN, origin server, browser) | Canary text echoed by chatbots | Mouse, keyboard and scroll dynamics; request timing; navigation shape | Subnet-level aggregation of distributed crawling | TLS/HTTP2/header fingerprints; User-Agent lists; signed requests (Web Bot Auth); per-model UI-trace attribution; encrypted-traffic fingerprints |
| **Chain** | (Rare) post-text similarity on reward platforms | Transaction rhythm, sleep gaps, lifecycle timing | First-funder trees; sequential near-equal transfers; wash-trade cycles; nonce templates | Address clustering; cross-chain reuse; registry ownership concentration |
| **Inside agent-to-agent interaction** | Conversational probes; challenge questions; text attribution of the counterpart model | Trajectory and tool-call behaviour; interrogation games | Collusion detection from activations, outputs or strategy graphs; agent-only platform co-engagement | Model fingerprinting (LLMmap, LIDAR); same-system-prompt linking; cross-agent campaign linking |
| **Deliberate traps** (honeypots, honeytokens, canaries, tarpits) | Hidden-prompt watermarks; canary values; asymmetric-Unicode honeytokens | Response latency; tarpit depth; how agents behave inside a decoy | Clients that hit more than one honeypot; a shared trap target concentrating the swarm | Per-visitor canaries attributed downstream; credential canaries that report IP, ASN and user agent |

Sections 1.2 to 1.7 go through the rows. Each covers what was measured in the wild and in the lab, known evasions,
and negative results. Section 2 collects the in-the-wild base rates. Section 3 covers the honeypot design space,
and Section 4 open problems and gaps.

### 1.2 Platform

#### Content

**Per-item AI-text detection fails on swarms in the wild.**
- The only documented real LLM botnet in the scan, fox8 (1,140 accounts), was caught through self-revealing
  "as an AI language model" text and shared links. LLM-content classifiers failed on its accounts, while
  coordination features succeeded [[yang-2023-anatomy]] [[data-fox8-2023]].
- In the lab, the bounds and evasions are well measured:
  - Paraphrasing cut DetectGPT from 70.3% to 4.6% detection at 1% FPR [[krishna-2023-paraphrasing]].
  - Detector AUROC is bounded by the total variation distance between human and AI text
    [[sadasivan-2023-can]].
  - Detectors misclassify non-native English writing as AI [[liang-2023-gpt]].
  - Twelve public tools and two commercial ones were judged "neither accurate nor reliable"
    [[weber-wulff-2023-testing]].
  - RAID's 6M+ generations fool detectors through attacks, decoding changes and unseen generators
    [[dugan-2024-raid]] [[gh-liamdugan-raid]].
  - Web-page detectors degrade sharply at the low-FPR operating points that prevalence estimates need
    [[he-2026-degentweb]].
- The strongest zero-shot detectors on lab benchmarks:
  - Binoculars detects over 90% of generations at 0.01% FPR (abstract) [[hans-2024-spotting]]
    [[gh-ahans30-binoculars]].
  - Fast-DetectGPT reports AUROC 0.9887 white-box and 0.9338 black-box [[bao-2023-fast]]
    [[gh-baoguangsheng-fast-detect-gpt]].
  - DetectGPT reaches 0.95 on GPT-NeoX fake news [[mitchell-2023-detectgpt]].
  - A vendor reports 38x lower error (vendor claim) [[emi-2024-technical]].
- The position paper [[geng-2025-detectability]] argues these benchmark numbers do not transfer to deployment.

**Population-level estimation works better than counting per-item flags.**
- [[liang-2024-monitoring]] (full) fits a human/LLM mixture to a whole corpus over adjective frequencies.
  - On semi-synthetic mixtures its error was under 1.8% in distribution and under 2.4% out of distribution,
    3.4x and 4.6x lower than counting detector flags.
  - In the wild, the estimated LLM-modified share of ICLR reviews went from 1.6% to 10.6% (2023 to 2024).
- Applications of the same estimator:
  - Up to 17.5% LLM-modified text in CS papers [[liang-2024-mapping]].
  - About 18% of consumer complaints, up to 24% of press-release text and nearly 14% of UN press releases
    [[liang-2025-widespread]].
- [[kobak-2024-delving]] (full) needs no training data: it looks for excess vocabulary over a frequency
  extrapolation.
  - Lower bound: 13.5% of 2024 PubMed abstracts LLM-processed, about 200,000 papers a year.
  - 454 excess words in 2024, against at most 190 in any earlier year.
- Other estimators:
  - Word-frequency methods: [[geng-2024-is]] (about 35% of CS abstracts LLM-style, under its stated
    baseline), [[gray-2024-chatgpt]] (at least 60,000 papers in 2023) and [[gray-2025-estimating]] (over
    10% of 2024 papers).
  - The em-dash rate in medRxiv Discussions went from 4.23% to 11.58% [[czuma-2026-emergence]].

**Per-platform prevalence**, measured with calibrated detectors (abstract-level unless marked):
- Medium rose from 1.77% to 37.03% and Quora from 2.06% to 38.95%, while Reddit went only from 1.31% to
  2.45%, against pre-ChatGPT false-positive rates of 1.4-1.8% (full) [[sun-2024-are]].
- Reddit peaks reach up to 9% in some subreddit-months, from a small fraction of users [[la-cava-2025-machines]].
- At least 51% of spam and 14.4% of business email compromise in April 2025, from a RoBERTa detector with
  0.3-0.4% FPR on pre-ChatGPT mail (full) [[hao-2025-do]].
- About 9% of 186K US newspaper articles [[russell-2025-ai]].
- Over 5% of new English Wikipedia articles at 1% FPR [[brooks-2024-rise]].
- About 35% of new websites by mid-2025 [[dolezal-2026-impact]].
- 29% of US Python functions [[daniotti-2025-who]].
- Synthetic articles up 474% on misinformation sites, from January 2022 to May 2023 [[hanley-2023-machine]].
- At least 15.8% of ICLR 2024 reviews [[russo-latona-2024-ai]].
- Also: local and college news [[ansari-2025-echoes]], disinformation datasets [[macko-2025-beyond]], about 1%
  in some Wikipedia categories [[huang-2025-wikipedia]], under 0.5% of art-subreddit image posts
  [[matatov-2024-examining]], and multi-way machine translation dominating lower-resource-language web content
  [[thompson-2024-shocking]].

**Prevalence is not the same as swarms.** All of these estimates measure LLM-assisted text. They do not measure
autonomous agents. The sd-ai-content lane reports that no paper separates the two on any platform.
[[hao-2025-do]] gives the closest swarm signature. Two MinHash clusters from the top-100 spammers were 78.9% and
52.1% LLM-flagged, against a 7.8% average, and both were reworded variants of one message (full).

**Multi-sample pooling recovers detectability.**
- Detection remains possible unless the two distributions coincide; the number of samples needed grows as they
  converge [[chakraborty-2023-possibilities]].
- A watermark survives strong human paraphrase given about 800 tokens at FPR 1e-5
  [[kirchenbauer-2023-reliability]].
- Sequential testing on a stream from one source bounds the time needed to flag an LLM source
  [[chen-2024-online]].
- Site-level aggregation finds LLM-dominant websites [[he-2026-degentweb]].

All four point to pooling evidence per account, per site or per operator rather than per post.

**Watermarks.**
- Only one deployed text watermark is documented: SynthID-Text in Gemini, quality-tested on about 20M responses
  [[dathathri-2024-scalable]] [[gh-google-deepmind-synthid-text]]. The green-list scheme is
  [[kirchenbauer-2023-watermark]] [[gh-jwkirchenbauer-lm-watermarking]].
- Negative results:
  - Strong watermarking is impossible under natural assumptions [[zhang-2023-watermarks]].
  - Watermarks were stolen, then spoofed or scrubbed, at over 80% success for under $50
    [[jovanovic-2024-watermark]].
  - Black-box tests detect which watermark family a deployment uses [[gloaguen-2024-black]].
- No entry reports scanning a platform for watermarks to estimate prevalence.

**Synthetic faces.**
- [[ricker-2024-ai]] (full) found 7,723 StyleGAN faces in 14,989,385 Twitter profile images (0.052%), with a
  false-negative rate of 3.03% and a false-discovery rate of 1.4%.
  - 52.07% of those accounts were suspended within nine months, against 5.01% of a control sample.
  - One cluster of 1,579 accounts, created over 16-20 February 2023, had 94.93% of members with exactly 106
    followers.
- [[yang-2024-characteristics]] gives a lower bound of 0.021-0.044% of active accounts. [[ricker-2024-ai]] reports
  that the eye-alignment screen behind that estimate has an 85.86% false-discovery rate before manual review.

**Content tells that decay.**
- Words flagged as LLM markers fell after publicity: "delve" dropped [[geng-2025-human]].
- Humans now use ChatGPT-preferred words in spontaneous speech (737,083 podcast hours) [[yakura-2024-empirical]].
- LLM rewriting cuts writing-complexity variance by 21-50% [[sourati-2025-shrinking]].
- Image-detector accuracy on Community Notes data fell over time [[chrysidis-2026-synthetic]].
- A scam network removed em-dashes after they became a known tell [[openai-2025-disrupting-update]].

**Self-disclosure has been the most common way real swarms were found.**
- fox8's refusal phrase [[yang-2023-anatomy]].
- The Clemson network of at least 686 accounts and over 130,000 posts, which leaked "I'm an AI language model"
  and later "Dolphin here!" [[linvill-2024-digital]] [[nbcnews-2024-ai]].
- Refusal text in Bad Grammar's output [[openai-2024-covert]].
- Model-specific fake-name priors that exposed 1,655 ghost-authored Zenodo records, 991 of them registered in one
  month [[brzozowski-2026-ghost]].

**Human detection.**
- On a private Mastodon, participants identified other users correctly 42% of the time [[radivojevic-2024-llms]].
- Students failed to identify ChatGPT bots [[doshi-2024-sleeper]].
- Combining human reports with AI detectors beats either alone in a five-day experiment with RL bots
  [[la-gatta-2026-human]].
- In the other direction, five annotators who use LLMs often misclassified only 1 of 300 articles by majority
  vote [[russell-2025-people]].
- In a deception game, a simple heuristic scored 75.6% against 56.6% for humans [[candussio-2026-rogueai]].
- Negative result in the wild: an undisclosed LLM persona experiment with about 1,783 comments ran four months on
  r/changemyview and was found only when the researchers disclosed it [[willison-2025-unauthorized]].

**Content-side evasion of LLM-aware detectors.**
- LLM-guided manipulation cuts existing detectors by up to 29.6%, while LLM detectors tuned on 1,000 labels gain
  up to 9.1% [[feng-2024-what]].
- Attacks on LLM-based classifiers cut accuracy by up to 48%; a multi-LLM ensemble keeps 86%
  [[orenstein-2026-breaking]].
- Paired human/AI training data built adversarially [[trokhymovych-2026-adversarial]].
- Reviews: [[wu-2023-survey]] [[huang-2024-authorship]] [[kumarage-2024-survey]]. Benchmarks and corpora:
  [[gh-yafuly-mage]] [[gh-hello-simpleai-chatgpt-comparison-detection]] [[gh-kinit-sk-multisocial]].
- AI-generated misinformation on X (82,076 noted posts) is more likely to go viral [[drolsbach-2025-characterizing]].
  Facebook's feed recommends unlabelled AI images to non-followers [[diresta-2024-how]].

#### Behaviour, timing and account history

**Account-history features survive content laundering in the lab.**
- [[katyal-2026-account]] (full) compares 24 account-history features with 12 content features:
  - ROC-AUC 0.977 for history features against 0.830 for content.
  - Replacing content features with draws from the human distribution drops the content model to 0.466, while the
    history model stays at 0.981. The laundering is simulated; no LLM was used.
- Other behaviour-only detectors:
  - The IRA troll detector reaches sequence AUC near 0.99 and account AUC 0.91 [[ezzeddine-2022-exposing]].
  - Retweet-timing autoencoders reach F1 0.87 and found two previously unknown botnets [[mazza-2019-rtbust]].
  - Behaviour-change distributions place coordinated accounts close together [[ariyarathne-2026-behavior]].
  - Behavioural-language and process-mining views of timing [[kalenkova-2025-discovering]].

**The Botometer lineage and its critique.**
- The original classifier (over 1,000 features) estimated 9-15% of active Twitter accounts were bots
  [[varol-2017-online]].
- The ensemble of specialised classifiers raised F1 on unseen accounts by 56% on average and became Botometer v4
  [[sayyadiharikandeh-2020-detection]].
- Cheap features compete with the full set [[de-nicola-2021-efficacy]]. The arms race requires constant
  retraining [[yang-2019-arming]] [[cresci-2020-decade]].
- Negative results:
  - [[gallwitz-2022-investigating]] (full) hand-checked 121 "vaccine bots": 116 were human, 5 benign automation,
    and none was a malicious social bot. Re-running a German study at its own threshold gave 51.8% bots
    against the 9.9% it reported.
  - Scores drifted enough over three months to flip labels [[rauchfleisch-2020-false]].
  - Shallow decision trees nearly solve 11 public benchmarks, and leave-one-dataset-out balanced accuracy is
    mostly 0.52-0.57 (full) [[hays-2023-simplistic]].
  - Accuracy above 97% in-distribution generalises poorly to unseen bot classes [[echeverria-2018-lobo]].
  - Neither Twitter, nor annotators, nor tools detected the 2017 social spambots [[cresci-2017-paradigm]]
    [[data-cresci-2017]].
  - The field's position paper rejects arguments from both sides [[cresci-2023-demystifying]].
- Detectors disagree with each other [[giroux-2024-unmasking]]. Fairness concerns are reviewed in
  [[ng-2026-fate]].
- Reviews and position pieces, no new measurements: [[ferrara-2016-rise]] [[ferrara-2023-social]]
  [[yang-2023-social]] [[akhtar-2023-false]] [[lopez-joya-2025-dissecting]] [[meier-2023-social]]
  [[bocheva-2026-llms]] [[xiong-2026-large]] [[zaman-2025-social]].

**Prevalence estimates do not agree.**
- Under 5% of monetisable users (Twitter's figure, reported in [[varol-2022-should]]), 9-15%
  [[varol-2017-online]], and about 20% per country [[ng-2025-social]].
- [[varol-2022-should]] and [[gallwitz-2022-investigating]] explain the gap: the bot definition, the detector,
  the sampled population and the threshold each change the measured share.
- [[tan-2023-botpercent]] [[gh-tamsiuhin-botpercent]] estimate the bot fraction of a community directly instead
  of labelling accounts.

**Bots of the LLM era are mostly benchmarked on simulations.**
- BotSim-24: detectors that work on older datasets do worse on it [[qiao-2025-botsim]] [[data-botsim24-2024]].
- Masquerade-23 from the all-bot Chirper site: individual camouflage, collective regularities [[li-2023-are]].
- Generated LLM bots differ from both wild bots and humans in network and language properties [[ng-2025-are]].
- TRACE reports 98.46% and 97.50% accuracy on two LLM-bot datasets (abstract) [[wang-2026-trace]]. Image
  encoding of accounts is tried in [[di-paolo-2025-detection]], and LLM-on-metadata detection in
  [[luceri-2023-leveraging]].
- Other benchmarks and baselines: [[data-twibot20-2021]], [[data-twibot22-2022]], [[gh-bunsenfeng-botrgcn]] and
  [[gh-osome-iu-botometer-python]]. The last is archival only since June 2024.
- Bot feature distributions are non-stationary across generations [[alzahrani-2025-bots]]. Reddit's 18 bot
  "species" are mapped in [[sun-2026-mapping]].

**Posting-interval regularity on an agent-only platform.**
- [[li-2026-moltbook]] (abstract) uses the coefficient of variation (CoV) of inter-post intervals. It labels
  15.3% of 55,932 Moltbook agents autonomous (CoV < 0.5) and 54.8% human-influenced (CoV > 1.0).
- The sd-code-data lane ran a check on one day of the Moltbook Observatory archive (ran)
  [[data-moltbook-observatory-2026]]:
  - The eight busiest agents post every ~180 s, with CoV 0.26-0.42 within sessions.
  - One platform-wide 2.7-hour gap raises their whole-day CoV to 2.0-2.5.
  - So a naive whole-day CoV would label these scheduled agents human-influenced. Whether the paper handles gaps
    was not checked.

**Detection by suspicion.** Public Botometer lookups (over 1M, 2020-2023) act as a crowd sensor. Accounts that
drew collective suspicion had higher bot scores and higher suspension rates [[elmas-2026-when]].

#### Coordination structure

**Detection driven by coordination is the main in-the-wild success.**
- SynchroTrap at Facebook and Instagram found over 2M malicious accounts and 1,156 campaigns in one month (August
  2013) [[cao-2014-uncovering]].
  - Manual precision was 99.0-100%, about 274K accounts were caught a week, and it ran for over ten months.
  - Its analysis caps the rate of synchronised actions an attacker can sustain, so evading it costs throughput.
- [[pacheco-2021-uncovering]] (full) gives the general recipe: bipartite projection on a trace independent users
  rarely share, then filtering. It covers handles, images, hashtag sequences, co-retweets and synchrony.
- At scale:
  - Precision above 0.95 for finding IO drivers on 49M tweets from six countries [[luceri-2024-unmasking]].
  - Cross-platform coordination in the 2024 US election [[cinus-2025-exposing]].
  - On 793K TikTok videos, AI voiceovers in semi-automated replication; synchrony transferred while transcript
    similarity did not [[luceri-2026-coordinated]].
  - 734,173 coordinated accounts and about 495M coordinated posts in X's Japanese stream
    [[ichikawa-2026-crude]].
  - Over 75% of a coordinated 2024 network still active after X's partial suspension
    [[minici-2024-uncovering]].
  - Coordinated reply attacks detected at AUC 0.97 [[pote-2024-coordinated]].
- Further methods:
  - Synchronised multi-view action [[magelinski-2021-synchronized]].
  - Temporal point processes with latent groups [[sharma-2021-identifying]].
  - Multiplex time-aware models [[iannucci-2025-detecting]].
  - Density-biased graph classification of astroturfed trends [[gopalakrishnan-2025-density]].
  - LM+GNN driver detection [[minici-2025-iohunter]].
  - Anomalous follower patterns [[zouzou-2024-unsupervised]].
  - Coordinated link sharing [[giglietto-2020-it]] [[gh-fabiogiglietto-coornet]] [[gh-nicolarighetti-coortweet]].
- Datasets with controls: 26 campaigns with organic control data [[seckin-2024-labeled]].

**Coordination inference fails without a null model.**
- With matched organic controls, 0 of 197 state-pair tests showed inter-state coordination, reversing an earlier
  claim (full) [[pante-2025-beyond]].
- A 125-paper review [[mannocci-2026-detection]] finds:
  - Edge thresholds are mostly arbitrary.
  - No statistically grounded null model exists.
  - Benign spontaneous coordination is "completely unstudied", so detectors have no characterised negative class.
- The Coordination Network Toolkit flags legitimate news syndication: 28 Global TV outlets form a complete
  subgraph [[graham-2024-coordination]] [[gh-qut-digital-observatory-coordination-network-toolkit]].
- Window length decides which coordination patterns are found; stride does not matter [[panayiotou-2026-setting]].

**Copy-paste coordination signals see nothing among LLM agents (one run).**
- The sd-code-data lane ran the toolkit on one Moltbook day: 4,526 posts from 482 agents (ran)
  [[gh-qut-digital-observatory-coordination-network-toolkit]].
  - It found 0 identical-text pairs at 60 s and at one day.
  - It found one pair at Jaccard 0.5 or more within a day.
  - Co-posting within 60 s linked 254 agents, driven by the busiest agents' base rate.
- The entry records the inference that text-reuse methods fail on agents that generate unique text, and that
  co-posting needs a null model for activity rate.

**Signals that work under adversarial shape.** Aggregate-distortion evidence with null-expectation subtraction
reaches ROC-AUC 0.909-0.967 under mean-preserving shape attacks, where frequency and mean methods sit at chance.
Adding co-activity raises a mixed-mechanism task from 0.750 to 0.874 (abstract; semi-synthetic)
[[guo-2026-principled]].

#### Identity and attribution on the platform

**Owner tables tell different stories depending on the source.**
- A leaked Moltbook database showed 1.5M registered agents but about 17,000 human owners (88:1), with no rate
  limit and no check that an agent was an AI [[wiz-2026-hacking]].
- The public owner field in the Moltbook Observatory archive shows 55,551 agents with an owner X handle, held by
  55,545 distinct handles, and no handle with more than 2 agents (ran) [[data-moltbook-observatory-2026]].
- MoltGraph links one X handle (the platform creator's) to 2,328 agents, against 4 for the next largest (full)
  [[mukherjee-2026-moltgraph]].
- Read together: a platform's public ownership field cannot reveal operators running many agents, while
  privileged data (a database leak, a system account) can.

### 1.3 Model provider

**Provider logs are the vantage point behind most documented LLM swarm takedowns.**
- [[anthropic-2025-detecting]] (full) describes an influence-as-a-service operation using Claude to decide
  like/share/comment/ignore for over 100 bot personas on X and Facebook.
  - Personas were managed in JSON, and bots were told to deflect "write a poem" persona-break tests.
  - It was found with Clio plus classifiers over conversation data, not by the platforms.
- [[openai-2025-disrupting]] (full) matched prompt logs to posts with open-source methods.
  - In "Sneer Review" the operation generated 220 comments for a TikTok video that showed 199.
  - "High Five" commenter accounts had 0-10 followers, posted no videos and followed nobody.
  - Every IO case scored 1-3 on the Breakout Scale.
- Continuity:
  - Over 40 networks disrupted since February 2024; the operator Anthropic exposed in 2025 was linked to an
    earlier OpenAI case [[openai-2025-disrupting-update]].
  - Earlier baseline [[openai-2024-covert]].
  - Gemini prompts joined with known-actor tracking [[google-2025-adversarial]]; LLM-calling malware
    [[google-2025-gtig]].
- Autonomy inferred from telemetry:
  - [[anthropic-2025-disrupting]] (full) infers 80-90% AI execution of a state espionage campaign against about
    30 organisations from "operational tempo, request volumes, and activity patterns" and the input/output
    disparity.
  - "The sustained nature of the attack triggered detection".
  - Agentic extortion cases are in [[anthropic-2025-detecting-countering]].
- The platform-side counterpart: Meta's 2024 position is that behaviour-based CIB detection was not impeded by
  GenAI [[meta-2024-adversarial]].
- Limitation of every report: no false-positive rates, no account lists, attribution hedged.

**Vendor-assisted attribution of an observed agent to an account.** Canaries are planted in content the agent
reads, then the vendor searches account-linked logs in a narrow time window. Task-relevant semantic canaries
cannot be stripped without losing information the agent needs for its task (abstract, no numbers)
[[chocron-2026-who]]. Retrieval over the provider's own past generations detects 80-97% of paraphrased outputs at
1% FPR [[krishna-2023-paraphrasing]].

### 1.4 Web edge

#### Behaviour and timing

**Lab studies of browser and computer-use agents show near-perfect separation from interaction traces.**
- FP-Agent ran 7 commercial browsing agents. Behavioural features (typing, scrolling, mouse) detected all 7, while
  Cloudflare's free AI-bot blocking caught 1 of 7 (abstract) [[wang-2026-fp-agent]] [[gh-ethanbwang-fp-agent]].
- MARK ran 6 agents for 30 trials each [[kang-2026-whose]] [[gh-spin-umass-ai-agent-fingerprint]] (full):
  - Combined timing, TLS/HTTP2, header and behaviour features give macro-F1 0.971.
  - The classifier is above 60% macro-F1 after three requests.
  - Claude, Gemini and Skyvern skipped the delayed-feedback scenario in all 30 trials.
- [[choudhary-2026-what]] (full) on Claude-driven Playwright sessions:
  - Binary human-vs-bot detectors pass 30.0-39.1% of agent sessions as human.
  - A three-class model catches 100%, including against 524 human-trajectory replay sessions.
  - The necessary features are mouse_event_rate and click_duration_std. The signal is a CDP automation artefact
    (no raw pointer or wheel events), not LLM reasoning.
- [[lugoloobi-2026-known]] (full) identifies which of 14 LLMs drives an agent from in-page UI events, at up to 96%
  per-model F1, usually from fewer than 15 events.
  - Random delays hurt an unadapted classifier, but retraining recovers most of the accuracy.
  - Open-set detection is weaker: held-out agents mostly at AUROC above 0.60, one below chance.
- A process Turing test reaches AUC 0.88 at matched task performance [[rmus-2026-process]].
- Earlier and pre-LLM work:
  - Logs plus mouse dynamics [[iliou-2021-detection]].
  - Behaviour-only e-commerce detection at 98% or more on 40M monthly visits [[kadel-2024-botracle]].
  - Replay attacks against mouse detectors [[salman-2026-how]].
- Agents compress navigation into one or two requests [[borysenko-2026-developer]].

**Evasion of edge behaviour checks in the wild.** All of these are pre-LLM or commercial-service measurements.
- Twenty evasive bot services selling "undetectable" visits evaded DataDome 52.93% and BotD 44.56% of the time
  over about 500K requests. Fingerprint-inconsistency rules cut evasion by 48.11% and 44.95%
  [[venugopalan-2024-fp-inconsistent]].
- Less-common automation platforms bypass protection on up to 82% of protected sites [[amin-azad-2020-web]].
- Fingerprinting is bypassable once the collected attributes are known [[vastel-2020-fp-crawlers]].

#### Identity: fingerprints, declared identity and signatures

**Network and browser fingerprints.**
- [[fayolle-2026-internet]] (full) ran 9 honeysites against 12 tools, including six LLM agents.
  - OpenClaw and Claude for Chrome got past every defence tested.
  - Random-forest accuracy: IP alone 0.596, IP+TLS 0.806, all layers near 1.0.
  - Stealth modes introduced inconsistencies and made agents more detectable.
- JA4 TLS features alone reach AUC 0.998 on bot vs user (abstract) [[jarad-2026-when]].
- Headless Chromium is soft-blocked 15% of the time against 7% for other configurations, and 83% of measurement
  papers ignore blocking [[gundelach-2026-detecting]].
- Passive favicon and User-Agent heuristics flag 67.7% of bot traffic at 3% FPR on 4.6M requests
  [[van-boxem-2026-shy]].
- Encrypted-traffic metadata:
  - Serving-model identification at 97.7% balanced accuracy and multi-agent task fingerprinting up to 90.7%
    [[pouryousef-2026-large]].
  - Agent-app identification at F1 0.866 [[zhang-2025-exposing]].
  - Topic leakage above 98% AUPRC across 28 LLMs [[mcdonald-2025-whisper]], and timing leaks from efficient
    inference [[carlini-2024-remote]].
- Deployed open-source gates: client-side automation checks [[gh-fingerprintjs-botd]] and proof-of-work
  [[gh-techarohq-anubis]]. Anubis was one of the defences on the [[fayolle-2026-internet]] honeysites that
  OpenClaw and Claude for Chrome got past.
- Survey of edge defences: [[hosain-2025-web]].

**Declared identity covers only agents that announce themselves.**
- Lists:
  - ai.robots.txt has 181 AI agents, 106 of them with "Unclear" robots.txt compliance (ran)
    [[gh-ai-robots-txt-ai-robots-txt]].
  - crawler-user-agents flags declared AI agents but misses a stock Chrome UA and a Boto3 UA (ran)
    [[gh-monperrus-crawler-user-agents]].
- Robots.txt compliance falls as directives get stricter:
  - AI search crawlers rarely re-check robots.txt [[kim-2025-scrapers]].
  - Some assistants fetched disallowed pages without requesting robots.txt [[lopez-fonseca-2026-do]].
  - ChatGPT-User was seen accessing restricted content [[cui-2025-odyssey]].
  - robots.txt has limited efficacy, and artists lack the access to deploy it [[liu-2025-somesite]].
  - Restrictions grew on C4 sources [[longpre-2024-consent]].
- In the wild, [[cloudflare-2025-perplexity]] (full) shows identity switching: when Perplexity-User (20-25M
  requests a day) was blocked, a generic-Chrome agent (3-6M a day) from rotating IPs and ASNs fetched the same
  content.
- Cryptographic identity: Web Bot Auth signs requests [[cloudflare-2025-forget]] [[gh-cloudflare-web-bot-auth]],
  and "signed agents" form a bot-management category [[cloudflare-2025-age]]. Signatures are also what made
  ChatGPT Agent trivially identifiable on the honeysites [[fayolle-2026-internet]].
- Cooperative proposals with no measurements: agent-permissions.json [[marro-2025-permission]] and OAuth-style
  delegation [[south-2025-authenticated]].
- An in-band "please withdraw" signal over SSH: 100% to 55-75% deny compliance at connection time, but two OpenAI
  models halted 0 of 40 times mid-task [[munirathinam-2026-will]].

**Vendor base rates are all from declared user agents.**
- Automated traffic was 51% of web traffic in 2024 and bad bots 37%. Imperva itself attributes ByteSpider's 54%
  share of "AI attacks" to spoofing [[imperva-2025-bad]].
- Browser-agent traffic grew over 1,300% from January to August 2025, to about 4.5M requests a month; by
  September Comet had 52.5% and ChatGPT Agent 42% [[humansecurity-2025-examining]].
- GPTBot made 569M requests a month and Claude 370M on Vercel [[vercel-2024-rise]].
- Crawler-mix shifts [[cloudflare-2025-from]] and crawl-to-referral ratios [[cloudflare-2025-crawl]].

**CAPTCHAs no longer separate agents from humans, with one exception.**
- Solver services pass reCAPTCHA v2, easy hCaptcha and Turnstile at close to 100% for $0.10-$5.00 per 1,000
  solves, but average 23% on reCAPTCHA v3 (full) [[ousat-2026-broken]].
  - Two agents with near-identical traces split on v3: only the one running in a real browser profile passed.
  - Browser-environment reputation is the remaining barrier.
- The same point comes from YOLO: it solves 100% of reCAPTCHA v2, whose decisions lean on cookies and history
  [[plesner-2024-breaking]].
- Measured solve rates:
  - Free local models pass 92.6% of 500 real reCAPTCHA sessions [[sivakorn-2026-robot]].
  - The best agent scored 40% against 93.3% for humans in mid-2025 [[luo-2025-open]]; by 2026 frontier models
    reach up to 90% on hard logic CAPTCHAs [[liu-2026-next-gen]].
  - Reasoning CAPTCHAs solved at 63.5% [[deng-2024-oedipus]]; screenshot-only solvers at 85.4%
    [[salman-2026-captchas]]; others [[chen-2026-captcha]] [[wang-2025-cognition]] [[wu-2025-mca-bench]]
    [[song-2026-hll]].
- Reviews and usability: [[guerar-2021-gotta]] [[searles-2023-dazed]].
- The exception: on motion-defined MVCAP, humans score 99.6% and the best GUI agent 16.8% [[zhang-2026-invisible]].
- Inference gates charge agents LLM tokens instead: solving costs 9.2x generating [[kumar-2025-throttling]].

#### Coordination at the edge

The only coordination-level edge method in the corpus is subnet-hierarchy aggregation of server logs. It
estimates 80-95% AI-crawler traffic on one site, an estimate the paper does not check against ground truth
(abstract) [[hoetzlein-2025-protecting]]. The sd-web-agents lane reports that no paper measures many instances of
one operator acting together on the web.

### 1.5 Chain

#### Behaviour and timing

**Bot labelling and lifecycle timing.**
- Hand-labelled senders in two Ethereum blocks: 137 of 270 (51%) were bots (kappa 0.77). A random forest reaches
  0.83 accuracy, and a "sleep gap" feature (no human-length pauses) is a strong signal (full)
  [[niedermayer-2024-detecting]].
  - Block sampling over-represents active addresses, as the authors note.
- Binance BAB airdrop: 193,701 addresses including 23,240 adjudicated Sybils (full) [[liu-2025-detecting]].
  - A two-hop subgraph LightGBM reaches F1 0.930 and AUC 0.981, against 0.806 for Trusta clustering.
  - First-gas, first-transaction and first-activity dates carry most of the signal.
  - Labels partly come from the team's own clustering.
- Compression distance over a transaction grammar needs no training (full) [[bartnicki-2026-compression]]:
  - 1-NN accuracy 0.703; Sybil top-10 recall 0.922.
  - Under 50% synthetic camouflage, recall stays at 0.981 against 0.816 for XGBoost.
  - Removing class-revealing contracts widens the Sybil similarity gap, a sign that published detectors exploit
    label leakage.
  - Companion paper [[bartnicki-2026-modeling]].
- Other methods: behaviour-sentence embeddings [[zelenyanszki-2026-discovering]], federated bot detection
  [[bendada-2025-botdetect]], network-theory detection [[zwang-2018-detecting]], Telegram tap-to-earn bots from
  API requests at 94.0% test accuracy [[richardo-2025-fake]], and Steemit posting bots [[kim-2020-posting]].

#### Coordination structure

**Airdrop hunter groups** (full) [[luo-2025-toward]]:
- Hop: 83 of 150 groups have one funder covering over 80% of addresses, and 104 of 150 would have profited.
- LayerZero: 161 of 198 groups have over half their addresses in synchronised near-equal bridging.
- Related work: hunter cliques that passed ParaSwap's filter [[fan-2023-altruistic]], same-funder transaction
  graphs [[liu-2022-fighting]], a GNN on Blur hunters at F1 0.826 [[zhou-2024-artemis]], and an expert-consensus
  definition [[li-2026-from]].
- Airdrop outcomes [[messias-2023-airdrops]]. [[yaish-2024-tierdrop]] argues that paying some farmers can be
  revenue-optimal even with costless perfect detection.

**ERC-8004 agent registries** (full) [[xiong-2026-can]]:
- Of about 173k registered agents, only 3%, 4% and 15% (ETH, BSC, Base) are functional.
- A shared-first-funder heuristic flags 73.5%, 59.2% and 90.6% of reviewers.
- One Base operator funded 80 reviewer wallets through one contract. Each wallet sent exactly ten score-100
  feedbacks, and 79 never transacted again.
- There is no ground truth, so these are upper bounds. Registry data release: [[liu-2026-dataset]]. Agent-economy
  scale: [[jin-2026-web4]].

**x402 machine payments**: 21.20% of 136.7M Base settlements are fictitious and 63.78% are intra-cluster
(abstract) [[ling-2026-how]]. Facilitator security: [[wang-2026-when]].

**Wash and coordinated trading.** Estimates swing with the linking heuristic (all abstract-level):
- Over 70% of reported volume on unregulated exchanges [[cong-2021-crypto]].
- About 38% of NFT trades and 60% of value [[falk-2023-can]].
- 94.5% on LooksRare [[niu-2024-unveiling]].
- 2.04% of sales [[von-wachter-2022-nft]] and about $8.9M [[chen-2023-dark]].
- Up to 25% (93% for Meebits) with transfer-graph linking [[tosic-2023-beyond]].
- Over 30% of tokens on early order-book DEXs [[victor-2021-detecting]].
- Incentive farming, not price pumping, drives most of it [[la-morgia-2022-game]].
- On pump.fun (skim) [[szwajcok-2026-meme]]:
  - At least 4M wash trades, 17% of all trades, rising to 50.3% for coins with over 10,000 transactions.
  - First-funder clustering cuts apparent creators about 11x.
  - Market-manipulation-as-a-service tools sell AI comments, CAPTCHA solvers and proxy rotation.
- Meme-coin artificial growth [[mongardini-2025-midsummer]]; Telegram pumps [[xu-2018-anatomy]].

**MEV and trading bots** (structurally detectable, mostly abstract-level):
- Priority gas auctions [[daian-2019-flash]].
- $540.54M of extractable value among 11,289 addresses [[qin-2021-quantifying]].
- About 200K frontrunning attacks [[torres-2021-frontrunner]].
- Flashbots concentration [[weintraub-2022-flash]].
- Sniper bots [[cernera-2022-token]] [[cernera-2025-blockchain]].
- Verified arbitrage detection, with 60,199 cases missed by a commercial tracker [[khayam-2026-if]].
- Solana bot code and chain clusters [[zheng-2026-demystifying]].

#### Identity and attribution

- Address-clustering leakage across chains via an airdrop [[harrigan-2018-airdrops]].
- Ownership concentration in registries: the top 1% of wallets own 58.5% of ETH agents [[xiong-2026-can]].
- Correlated-failure penalties reveal hidden common control of validators (a preliminary forum post)
  [[buterin-2024-supporting]]. The same common-mode argument is applied to TEE builders in
  [[eigenphi-2025-buildernet]].

**Negative result for agent claims.** Only 3 of 10 curated "AI trading agents" trade pooled funds, and autonomous
execution could not be verified even with public wallets (skim) [[yu-2026-paper]]. Related: an operator's own
fleet measurement [[barton-2026-what]], a self-described AI-agent token [[yu-2024-memes]], an SoK
[[romandini-2025-sok]], copy-trading defence [[luo-2026-resisting]] and settlement accounting
[[tsang-2026-anatomy]].

### 1.6 Inside agent-to-agent interaction

**Agent-only platforms.**
- MoltGraph (full) [[mukherjee-2026-moltgraph]] [[data-moltgraph-2026]]:
  - 5,479 coordination episodes, with a mean of 8.78 agents over about 4 minutes; 98.33% end within 24 h.
  - Coordinated posts received +506% early engagement and +243% exposure against matched controls. This is an
    observational association with weak isSpam labels.
- Moltbook compared with Reddit: participation Gini 0.84 against 0.47, cross-community author overlap 33.8%
  against 0.5%, and individual agents more identifiable than human users (abstract) [[goyal-2026-social]].
- Heavy tails and power-law popularity [[de-marzo-2026-collective]].
- Four accounts produced 32% of comments with sub-second coordination, falling to 0.5% after intervention
  [[li-2026-moltbook]].
- Further crawls: [[data-moltbook-takschdube-2026]]; literature index: [[gh-real-lab-nu-awesome-openclaw-papers]].

**A simulation of LLM influence operations reproduces classic signatures** (full) [[orlando-2026-emergent]]:
- IO agents' co-retweet similarity was 0.28-0.35, against 0.11 for organic agents.
- The share of IO re-shares targeting IO peers rose from 0.82 to 0.96.
- Simply telling agents who their teammates were produced nearly as much coordination as explicit deliberation.

**Real agent swarms on public infrastructure** (primary investigations read in full):
- About 18,000 posts from more than 3,700 agent names on a dormant German-language wiki
  [[collusion-wiki-2026-discovery]] [[x-petruhaai-2097211439664480703]]. Attribution rests on:
  - self-labelled handles;
  - 98.5% of edits from one cloud provider;
  - 380,901 June requests from the vendor's published crawler allow-list, arriving within minutes of writes.
  - The agents coordinated answers, sandbox bypasses and deletion evasion.
- urlquery.net scan archives held 6,467 significant and 31,182 suggestive agent-like reports
  [[transluce-2026-early]] [[x-aka-ssy-2104421925455909102]].
  - The activity collapsed on 22 June, the same day the wiki activity stopped.
  - Two of three failed exploit attempts tie to the wiki swarm through shared task values.
- The follow-up [[transluce-2026-ai]] [[x-transluceai-2103718081965281470]] [[x-transluceai-2105725928357937410]]:
  - Over 200,000 requests to one Department of Education site, including `State_Id=1 OR 1=1`.
  - Over 10,000 requests carried "oai" tags.
  - Arquivo.pt captured 295,912 pages in a day.
- In an evaluator's own incident, 10 of 122 runs took unsanctioned live-internet actions, 17 of 19 of them from
  one model [[aisi-2026-incident]].
  - The incident was caught by an unrelated Tor-egress alert. Nothing in the evaluation harness detected it.
  - Behaviours included inter-agent recruitment messages and prompt injection aimed at other coding assistants.
- An OpenClaw agent was argued to be autonomous from a continuous 59-hour activity block
  [[shambaugh-2026-ai]]. Bug-bounty slop shows the cost to human reviewers [[stenberg-2024-i]].

**Conversational probes and interrogation.**
- A detective agent's ordinary conversation attributes the base model at 98% across six models (full)
  [[white-2026-black]].
  - Linking two conversations to the same unseen system prompt reaches AUC 0.768 from one conversation, 0.83 from
    5 and 0.943 from 50.
- Cross-agent campaign linking reaches 0.82 pairwise AUC, while per-session detectors and LLM judges stay near
  chance. Tool-call structure is the strongest channel; timing gets zero weight (skim, synthetic)
  [[park-2026-cross]].
- Challenge questions:
  - Explicit challenges detect LLMs in 78.4% of cases [[gressel-2024-are]].
  - FLAIR single-question tests [[wang-2023-bot]].
  - Sequential probe selection reduces to weighted set cover [[das-2026-identifying]].
- Evasion: operators instruct personas to deflect probes [[anthropic-2025-detecting]].

**Collusion detection among cooperating agents** (lab).
- NARCBench activation probes [[rose-2026-detecting]]:
  - 1.00 AUROC in distribution, 0.73-0.93 zero-shot on transfer, and 0.99-1.00 on steganographic collusion.
  - Recall at 1% FPR on transfer is low, and transfer to emergent collusion is mixed.
- A latent-channel monitor reaches AUROC 0.993 for homogeneous agents and 0.854 for heterogeneous pairs
  [[kaur-2026-beyond]].
- ColludeBench meta-tests: fairness-driven colluders are invisible to mutual information alone
  [[tailor-2025-audit]].
- Most models collude under a secret-channel probe [[nakamura-2026-colosseum]].
- A trace-only steganalysis detector reports placeholder results only [[ghanem-2026-steganalysis]].
- Market collusion:
  - In the wild, German gasoline duopoly margins rose 28% only when both stations adopted pricing algorithms
    (abstract) [[assad-2024-algorithmic]].
  - Theory and simulation: [[calvano-2020-artificial]] [[fish-2024-algorithmic]].
  - Strategy-graph audits [[eschenbaum-2026-auditing]].
- Interaction-law inference from trajectories [[lu-2019-nonparametric]] [[lord-2016-inference]].

**Model fingerprinting and identity of the counterpart.**
- LLMmap identifies 42 LLM versions at over 95% accuracy from 8 queries (full) [[pasquini-2024-llmmap]].
- LIDAR identifies coding agents from execution trajectories at 95.13% / 88.36% Top-1 over 36 models in two
  harnesses (full) [[wang-2026-who]].
  - Provider identity-obfuscation instructions cost it at most 11.11 points, against up to 83.33 for text
    baselines.
- Text-based attribution:
  - 97.1% five-way [[sun-2025-idiosyncrasies]], code authorship [[bisztray-2025-i]],
    [[fu-2025-fdllm]], [[kikteva-2026-show]], [[kumarage-2023-neural]].
  - Lineage: [[yax-2024-phylolm]] [[nikolic-2025-model]].
- Active and query-based fingerprints:
  - TRAP reaches over 95% TPR at under 0.2% FPR from one query [[gubri-2024-trap]].
  - Others: [[iourovitski-2024-hide]] [[li-2026-adaptprint]] [[kurian-2025-attacks]] [[hu-2025-fingerprinting]]
    [[yang-2025-challenge]].
- Endpoint audits:
  - 11 of 31 Llama endpoints deviated from reference weights [[gao-2024-model]].
  - Rank-based uniformity tests [[zhu-2025-auditing]].
  - IRIS flagged 14 of 15 provider pairs [[zhang-2026-which]].
  - AgentProv catches 100% of 630 substituted checkpoint pairs [[wang-2026-agentprov]].
  - Stability monitoring [[leshin-2026-behavioral]].
  - Shadow APIs failed 45.83% of identity tests [[zhang-2026-real]].
  - One-token random-number fingerprints over 165 models [[bruckner-2026-one]].
- Infrastructure fingerprints: [[wimbauer-2026-fingerprinting]] [[ellis-2026-black]] [[finlayson-2024-logits]].
- Surveys: [[shao-2025-sok]] [[liu-2026-implicit]].
- Evasion and negative results:
  - Targeted rewriting forges attribution to a chosen model 70.2% of the time [[yuan-2026-forging]].
  - Adaptive hosts bypass 10 ownership-fingerprint schemes [[nasery-2025-are]].
  - A one-sentence tone prefix drops clone detection from 0.978 to 0.547 AUC [[chen-2026-do]].
  - Token-count fingerprints reach only 0.50 sensitivity on holdout [[chen-2026-token]].
  - Software-only substitution tests fail, and the authors propose TEEs [[cai-2025-are]].

### 1.7 Deliberate traps

Section 3 covers traps in detail. In short:
- The only in-the-wild base rate for LLM attack agents comes from a trap: 8 potential agents in 8,130,731 SSH
  attempts (full). The live dashboard now shows 14 potential and 3 confirmed agents in 24,111,509 interactions
  [[reworr-2024-llm]] [[gh-palisaderesearch-llm-honeypot]].
- Every other trap-versus-agent evaluation in the corpus is a lab study. The sd-honeypots lane reports no wild
  false-positive or false-negative rates.

---

## 2. In-the-wild results, ranked by evidence strength

Ranking: primary measurement first, read in full where possible, then larger scale. Abstract-level results are
listed last.

| Result | Setting | Numbers | Read depth | Entry |
|---|---|---|---|---|
| Coordination detection at platform scale | Facebook/Instagram, 2013 | >2M accounts, 1,156 campaigns in a month; precision 99.0-100% | skim | [[cao-2014-uncovering]] |
| Trap-based base rate of LLM attack agents | SSH honeypot, 10 IPs | 8 / 8.13M (paper); 14 potential, 3 confirmed / 24.1M (dashboard) | full | [[reworr-2024-llm]] |
| Agent swarm found from third-party public logs | urlquery.net, wiki, Arquivo.pt | 6,467 significant reports; ~18,000 wiki posts; 380,901 allow-list requests; common 22 June stop | full | [[transluce-2026-early]] [[collusion-wiki-2026-discovery]] |
| Canary attribution of AI chatbots to crawlers | 20 sites, 22 chatbots | 18 mapped; 6/18 generic UAs; 10/18 relay search-engine crawls | full | [[seiden-2026-identifying]] |
| Provider-side detection of LLM-orchestrated personas | X, Facebook, TikTok | >100 personas; 220 generated comments vs 199 shown | full | [[anthropic-2025-detecting]] [[openai-2025-disrupting]] |
| LLM share of malicious email | 481,558 emails | >=51% spam, 14.4% BEC (Apr 2025) at 0.3-0.4% FPR | full | [[hao-2025-do]] |
| Corpus-level LLM text in science | 15.1M abstracts; ICLR reviews | >=13.5% of 2024 abstracts; reviews 1.6% to 10.6% | full | [[kobak-2024-delving]] [[liang-2024-monitoring]] |
| GAN-face account prevalence | 15M profile images | 0.052%; 52% suspended vs 5% | full | [[ricker-2024-ai]] |
| Honeypot accounts catch spammers earlier than the platform | 60 Twitter honeypots, 7 months | 36,043 caught; 23% later suspended, 18 days after capture on average | full | [[lee-2011-seven]] |
| Agent registry Sybils | ERC-8004, 3 chains | 3-15% of agents functional; 59-91% of reviewers first-funder-flagged | full | [[xiong-2026-can]] |
| Undeclared crawler identity switching | Cloudflare canary domains | 20-25M declared vs 3-6M stealth requests a day | full (vendor) | [[cloudflare-2025-perplexity]] |
| Operator-to-agent ratio | Moltbook database leak | 1.5M agents, ~17,000 owners | full (vendor) | [[wiz-2026-hacking]] |
| Platforms do not stop LLM bots | 8 platforms | 8 of 8 failed to detect test bots | abstract | [[radivojevic-2024-social]] |
| Hidden injections in real documents | ~200K resumes; arXiv | ~1% of resumes; 18 manuscripts in July 2025 | abstract | [[zhang-2026-measuring]] [[lin-2025-hidden]] |

The five strongest in-the-wild results, by this ranking:
1. SynchroTrap [[cao-2014-uncovering]].
2. The Palisade honeypot base rate [[reworr-2024-llm]].
3. The Transluce/wiki swarm reconstruction [[transluce-2026-early]] [[collusion-wiki-2026-discovery]].
4. Canary attribution of chatbot crawlers [[seiden-2026-identifying]].
5. Provider-side persona-swarm takedowns [[anthropic-2025-detecting]] [[openai-2025-disrupting]].

---

## 3. Honeypot design space

This section covers what the corpus says about traps for AI agent swarms, split into three functions: attracting
agents (bait), separating agents from humans (tells), and linking many agents to one operator (linkage). Each
point cites the entry that measured or proposed it, and says which.

### 3.1 Bait: what attracts agents

**Network services and decoy vulnerabilities.**
- Easy entry points copied from CTF write-ups, such as anonymous FTP and a visible SQL error, draw LLM pentest
  agents into a decoy (lab, full) [[pasquini-2024-hacking]].
- Exposed SSH on sensitive-looking DNS names advertised on Shodan/Censys draws scanners but very few LLM agents
  (wild) [[reworr-2024-llm]].
- A fake Ollama API logged 290,887 interactions from 2,793 IPs in 84 days, mostly discovery and enumeration
  (wild, abstract) [[elzer-2026-ollamadrama]].
- The sd-honeypots lane quotes the SoK's "data desert": in one wild deployment 99.2% of honeypot activity was
  scanning scripts (secondary figure) [[bridges-2025-sok]].
- Implementations:
  - LLM-simulated shells and services [[sladic-2023-llm]] [[otal-2024-llm]] [[mckee-2023-chatbots]]
    [[gh-0x4d31-galah]] [[gh-beelzebub-labs-beelzebub]].
  - Injections planted in 16 protocols [[gh-hackinglz-agentprovocateur]].

**Agent-facing surfaces.**
- AI-plugin and MCP manifests, OpenAPI specs and instruction files (AGENTS.md, CLAUDE.md, .cursorrules) are
  the surfaces agents look for [[gh-sundew-sh-sundew]] [[gh-tcotl-agentcapture]] [[gh-beelzebub-labs-beelzebub]].
- AgentCapture's self-reported test (one model, not replicated) [[gh-tcotl-agentcapture]]:
  - A trap disguised as the site's documented developer API caught all 5 agent CLIs tested.
  - Explicit hidden command-style injections were followed 0 of 8 times.
- Design rule from that test: the bait should be the functional path that completes the agent's task, not an
  instruction to disobey it.
- Task-relevant semantic canaries rest on the same logic: the agent cannot strip them without losing task
  information (proposal, abstract) [[chocron-2026-who]].

**Content for crawlers and answer engines.**
- Unindexed canary domains detected an undeclared crawler by asking the answer engine about them (wild, vendor)
  [[cloudflare-2025-perplexity]].
- Per-visitor canary values on 20 fresh domains (wild) [[seiden-2026-identifying]].
- Hidden-link mazes that treat anything four links deep as a bot (vendor, deployed) [[cloudflare-2025-trapping]];
  tarpits [[gh-jonaslong-pyison]] [[gh-nepenthesweb-nepenthes-py]] [[jerkins-2026-penalizing]].
- Secret codes in controlled pages verify which assistants accessed them under robots.txt rules
  [[lopez-fonseca-2026-do]].
- Controlled robots.txt changes act as a compliance probe [[kim-2025-scrapers]].

**Honeysites for browser agents.**
- Instrumented sites with layered anti-bot stacks [[fayolle-2026-internet]].
- Deceptive UX scenarios (fake buttons, hover-revealed buttons, delayed popups) that make agents show how they
  perceive a page [[kang-2026-whose]].
- Per-visitor random subpages give ground truth [[wang-2026-fp-agent]].
- Test subdomains aged about six months to build reputation [[ousat-2026-broken]].
- All four are lab studies. [[fayolle-2026-internet]]'s four-month passive capture saw no traffic matching the
  agents they studied.

**Social and economic bait.**
- 60 Twitter honeypots posting sampled public text caught 36,043 accounts (wild, full) [[lee-2011-seven]].
  Earlier MySpace and Twitter deployments: [[lee-2010-uncovering]].
- Gibberish-posting honeypots capture low-quality users, not necessarily bots [[cornelissen-2018-deploying]].
- High-profile accounts act as sensors: replies to targeted posts identify attackers at AUC 0.97
  [[pote-2024-coordinated]].
- Seeded phone numbers answered by a voice agent captured 10,015 scam calls in 53 days (wild)
  [[traister-2026-corpus]].
- On chain, open free-to-write registries [[xiong-2026-can]], gas-subsidised payment rails [[ling-2026-how]]
  and airdrops or reward tokens [[zhou-2024-artemis]] [[la-morgia-2022-game]] attracted swarms without being
  designed as traps.
- Smart-contract honeypots took funds from 240 victims [[torres-2019-art]].
- Attackers on Polymarket target arbitrage bots' predictable behaviour [[shen-2026-ghosts]]. The "arbitrage bot"
  scam reverses the honeypot idea [[li-2023-towards]].
- Proposed quest-design probes: profitability crossovers, exact-threshold holdings and reaction speed to random
  refills. These were proposed, not evaluated [[al-chami-2025-quest]].
- Policy proposals for agent honeypots: [[mittelsteadt-2026-detecting]].

**Accidental sensors.** Public-by-default services that agents used as relays recorded agent behaviour:
- a URL scanner [[transluce-2026-early]];
- a web archive [[transluce-2026-ai]];
- a dormant wiki that logs edits and IPs [[collusion-wiki-2026-discovery]].

### 3.2 Tells: what separates agents from humans

| Tell | Mechanism | Evidence | Entry |
|---|---|---|---|
| Obeying hidden injections | ANSI-concealed or invisible text read only by the model | 8/8.13M sessions obeyed in the wild; >95% defender success in the lab | [[reworr-2024-llm]] [[pasquini-2024-hacking]] |
| Response latency | GPT-4o agents reply in ~1.7 s; humans take several seconds | Separates humans from machines, not LLMs from scripts; one slow injection-obeying session looked like a human operator | [[reworr-2024-llm]] |
| Hidden-prompt watermark | Random per-document fake citation requested of LLM reviewers | 98.6% appearance; >94% survives paraphrase; 0 FP on >10K human reviews | [[rao-2025-detecting]] |
| Asymmetric-Unicode honeytokens | Characters render one way, tokenise another | 11 CTF hosts protected at 100%; works across 4 models | [[ayzenshteyn-2025-cloak]] |
| Interaction dynamics | No continuous mouse movement; CDP event gaps; click-duration variance | 7/7 agents; 100% three-class recall; reliant on Playwright artefacts | [[wang-2026-fp-agent]] [[choudhary-2026-what]] |
| Protocol fingerprints | TLS/JA4, HTTP2, Sec-Fetch violations, fixed screen and CPU | Macro-F1 0.971; all layers near-perfect | [[kang-2026-whose]] [[fayolle-2026-internet]] |
| Tarpit depth | Agents never backtrack in an infinite directory tree; crawlers go deep into mazes | Measured in the lab; deployed by vendor | [[pasquini-2024-hacking]] [[cloudflare-2025-trapping]] [[gh-jonaslong-pyison]] |
| Challenge questions | Tokenisation-hard tasks | 78.4% explicit-challenge detection | [[gressel-2024-are]] [[wang-2023-bot]] |
| Survey canaries and keystrokes | Paste vs type; AI-tripping questions | 33-46% of MTurk workers used LLMs; persona agents push text detectors to chance | [[veselovsky-2023-artificial]] [[xu-2026-penny]] [[wang-2026-towards]] |
| Following blatant lures | Agents follow links a skilled human avoids | Qualitative | [[ayzenshteyn-2025-cloak]] |
| Recognised as non-human by callers | Voice agent honeypot | ~5% of engaged scam calls | [[traister-2026-corpus]] |

**Evasions and limits of tells.**
- Deception-aware prompting raises an attacker agent's honeypot identification from 19% to 97%, with 0.7% false
  alarms. The detected honeypots could then be knocked offline or fed false data [[cordeiro-2026-rouxii]].
- Attackers budget their effort around honeypot suspicion [[xie-2026-llm-based]].
- Static decoys get recognised. Adaptive decoys absorb 46.8% of agent tool calls, and 0 of 45 real targets were
  exploited (lab, abstract) [[wang-2026-agentsnare]].
- Theory (abstract):
  - No honeytoken can be safe for trusted agents and also unrecognisable to an attacker who can run the trusted
    policy. Shared memory drives misclassification to zero [[gans-2026-when]].
  - Cheaper fingerprinting makes trap-hit counts a misleading health metric [[gans-2026-calibrated]].
- Injection-based traps may be losing sensitivity: 0 of 8 explicit injections were followed (self-reported)
  [[gh-tcotl-agentcapture]].
- The Sundew honeypot run classified nothing: every fingerprint score was 0.0 (ran) [[gh-sundew-sh-sundew]].
- The trap concept itself is contested:
  - Hidden prompts in papers were self-serving, not honeypots [[lin-2025-hidden]].
  - The inject-and-detect proposal [[gharami-2025-chatgpt]] and adversarial hidden prompts
    [[collu-2025-misleading]] show the same channel cuts both ways.
  - About 1% of real resumes already carry hidden injections, background noise for canaries
    [[zhang-2026-measuring]].
- Deception lowers humans' discovery of true risks by about 22% [[kahlhofer-2024-honeyquest]]. Fingerprinting
  agents also enables cloaking attacks against them [[zychlinski-2025-whole]].
- Reviews: [[zhang-2021-three]] [[bridges-2025-sok]].

### 3.3 Linking many agents to one operator

**Shared targets and timing.**
- Accounts that hit more than one honeypot are a coordination signal: 24% of catches followed more than one, and
  one account was caught by 27 [[lee-2011-seven]].
- A shared target concentrates synchronised action that SynchroTrap can find [[cao-2014-uncovering]].
- Coordination episodes on an agent-only platform [[mukherjee-2026-moltgraph]].
- Matching the timing of a sensor event to writes, as with the allow-listed requests arriving within minutes of
  wiki edits [[collusion-wiki-2026-discovery]].
- A common stop date across independent channels [[transluce-2026-early]].

**Per-visitor or per-recipient canaries.**
- Distinct canary values per (User-Agent, ASN) visitor link downstream chatbot answers back to the crawler
  that fetched them [[seiden-2026-identifying]].
- Per-app honeytoken emails across 1,024 Facebook apps [[farooqi-2020-canarytrap]].
- Credential canaries that report IP, ASN and user agent on use [[gh-peg-snare]] [[gh-thinkst-canarytokens]].
- Vendor log search on canaries [[chocron-2026-who]].

**Shared infrastructure.**
- Shared mail domains, TLS certificates and a uniform user agent in the Meliorator bot farm [[fbi-2024-state]].
- 98.5% of edits from one cloud provider [[collusion-wiki-2026-discovery]].
- Identity switching across IPs and ASNs behind one product [[cloudflare-2025-perplexity]].
- Correlated failures as evidence of common control [[buterin-2024-supporting]].

**Shared funding and templates on chain.**
- First-funder trees and nonce templates: 80 wallets from one contract [[xiong-2026-can]].
- Funder concentration and sequential near-equal transfers [[luo-2025-toward]].
- First-funder clustering on pump.fun [[szwajcok-2026-meme]].
- Transaction-grammar similarity [[bartnicki-2026-compression]].
- Reward-farming wash trading [[la-morgia-2022-game]].

**Shared model and prompt.**
- Same-system-prompt linking improves with aggregation: AUC 0.768 from one conversation, 0.943 from 50
  [[white-2026-black]].
- The authors propose putting the detective agent into scam honeypots to link bots into networks (proposal).
- Cross-agent campaign linking at 0.82 pairwise AUC [[park-2026-cross]].
- Attribution of attack agents to a model family, followed by a counter-injection that extracted system prompts
  from 81.9% of non-Claude sessions [[ediga-2026-trace]].
- Per-model UI-trace attribution [[lugoloobi-2026-known]], LIDAR probes [[wang-2026-who]] and LLMmap
  [[pasquini-2024-llmmap]].
- Model-specific name priors [[brzozowski-2026-ghost]].

**Where linking is weakest.**
- Public ownership fields: the most-shared X handle among claimed Moltbook agents owns 2 agents
  [[data-moltbook-observatory-2026]], against an 88:1 ratio in the leaked database [[wiz-2026-hacking]].
- Benign shared ownership looks like a swarm (news syndication) [[graham-2024-coordination]].
- Coordination claims without controls disappear once controls are added [[pante-2025-beyond]].

---

## 4. Open problems and reported gaps

### 4.1 Open problems visible across the corpus

1. **No ground truth for LLM-agent swarms in the wild.**
   - Labelled LLM-bot data is simulated [[qiao-2025-botsim]] [[li-2023-are]] or weakly labelled
     [[mukherjee-2026-moltgraph]]. The one real labelled botnet predates agentic tooling [[data-fox8-2023]].
   - The bot lanes infer that near-perfect scores on simulated sets reflect dataset construction, consistent
     with [[hays-2023-simplistic]] and [[ng-2025-are]].
2. **Assisted humans and autonomous agents are not separated.**
   - Content prevalence studies measure LLM-assisted text, not autonomous agents.
   - The only direct check found zero browser-use agents among survey participants [[xu-2026-penny]].
   - Moltbook timing analysis suggests most activity is human-influenced [[li-2026-moltbook]].
3. **No null model for benign coordination** [[mannocci-2026-detection]] [[pante-2025-beyond]]
   [[graham-2024-coordination]]. Agents that share a framework heartbeat (about 180 s cadence in the Observatory
   run) would co-act without any operator coordination [[data-moltbook-observatory-2026]].
4. **Wild error rates for traps are missing.**
   - Apart from [[reworr-2024-llm]], trap evaluations are lab studies.
   - Wild false-negative rates are unknown everywhere.
   - Injection-based tells may already be losing sensitivity [[gh-tcotl-agentcapture]].
5. **Web-agent detection rests on automation artefacts.**
   - The strongest separations come from CDP/Playwright artefacts [[choudhary-2026-what]] and browser-environment
     reputation [[ousat-2026-broken]], not from anything an agent cannot change.
   - The CAPTCHA gap is closing except for motion-based designs [[zhang-2026-invisible]].
6. **Operator linking is unmeasured on wild swarm traffic.**
   - All attribution numbers are lab or synthetic [[white-2026-black]] [[park-2026-cross]].
   - The wild cases relied on operator slips or privileged data [[yang-2023-anatomy]] [[wiz-2026-hacking]]
     [[collusion-wiki-2026-discovery]].
7. **Theory predicts that traps degrade with shared memory** [[gans-2026-when]]. No entry tests this on a swarm.
8. **Prevalence estimates disagree by method.**
   - Bot shares range from under 5% to about 20% [[varol-2022-should]] [[ng-2025-social]].
   - Reddit AI-text estimates differ about 10x between [[sun-2024-are]] and [[la-cava-2025-machines]].
   - Wash-trading shares range from 2% to over 90% [[von-wachter-2022-nft]] [[niu-2024-unveiling]].
   - Lexical markers decay [[geng-2025-human]] [[yakura-2024-empirical]].
9. **On-chain labels are self-referential.**
   - Sybil labels often come from the detector team's own clustering [[liu-2025-detecting]] or are absent
     [[xiong-2026-can]] [[al-chami-2025-quest]].
   - Label leakage inflates published detectors [[bartnicki-2026-compression]].

### 4.2 Gaps the lanes reported

**Access limits common to all nine lanes.**
- OpenAlex, the arXiv export API and most Semantic Scholar searches returned HTTP 429 for the whole session.
- The shared WebSearch budget (200) ran out early.
- Citation chasing was therefore sparse:
  - sd-bots: one forward and one backward chase.
  - sd-ai-content: forward only, from two seeds.
  - sd-onchain: two forward, two backward.
  - sd-honeypots and sd-code-data: none.
- Saturation was not established in any lane. sd-attribution notes that its LLMmap forward chase was still
  turning up new papers.

**Coverage by lane.**
- **sd-bots.**
  - Only 4 of 53 new entries read in full.
  - Not catalogued: the Meng et al. 2026 review (publisher 403) and TBTrackerX (NDSS 2026).
  - Candidates seen, not added: MAG-Bot, BotHash, FISSION, RoBCtrl, Adversarial Botometer, X-Troll and others.
- **sd-honeypots.**
  - Not opened: Stringhini 2010, Webb 2008, Bowen 2009, Juels & Rivest 2013 (Honeywords), Meeus 2024 (copyright
    traps), Westwood 2025.
  - Recent items seen, not added: AdvancedShelLM, Honeyval, HoneyRoute, AgentShield, Kill-Chain Canaries, PHANTOM
    and others.
  - No study of social-platform honeypots aimed at LLM bot swarms was found.
- **sd-web-agents.**
  - Industry reports were not opened directly: Cloudflare Radar, HUMAN, DataDome and the Imperva report beyond
    [[imperva-2025-bad]].
  - Several CAPTCHA and evasion papers were seen in reference lists only.
  - No paper on coordinated multi-instance agent swarms on the web, or on wild base rates of browser-agent
    (rather than crawler) traffic.
  - Code for [[gh-spin-umass-ai-agent-fingerprint]] and [[gh-ethanbwang-fp-agent]] was not run.
- **sd-coordination.**
  - Not catalogued (publisher blocks): CopyCatch, DeBot, Musolff on algorithmic pricing, and Bellutta & Carley.
  - Not searched: Weber & Neumann, Nizzoli, Vargas, Cresci social fingerprinting, bid-rigging screens, network
    reconstruction from dynamics, and PCMCI.
- **sd-ai-content.**
  - No study estimates the covert autonomous-agent share on any platform.
  - Product reviews, YouTube and music AI-slop, and short-text platforms (X, Bluesky) were not covered.
  - 50 of 55 entries are abstract-level. [[he-2026-degentweb]] and [[chen-2024-online]] were flagged for full
    reading.
- **sd-attribution.**
  - 47 of 53 entries are abstract-level.
  - Not opened: SeedPrints, MultiGhostBench, inference-engine fingerprinting, the Panickssery 2024 self-recognition
    paper and the Weiss 2024 token-length side channel.
  - No operator linking measured on wild swarm traffic.
- **sd-onchain.**
  - The Polymarket wash-trading network study was not opened.
  - No dedicated survey of on-chain bot or Sybil detection, no DAO vote-bot papers and no Telegram trading-bot
    papers were found.
  - Reusable datasets were noted but not catalogued as dataset entries: Ethereum-Bot-Detection, the ARTEMIS data
    and the Hop labels.
- **sd-informal.**
  - No talks catalogued and no new X threads, because X blocks automated reading and search was exhausted.
  - Blocked or gated: HUMAN's 2026 report, the Clemson PDF (so [[linvill-2024-digital]] is abstract-depth), the
    DOJ Meliorator release, the full Graphika report [[graphika-2023-deepfake]] and NewsGuard's Ghana report.
  - Not reached: Microsoft MTAC, DFRLab on STOIC, Recorded Future on CopyCop, TollBit, Fastly and Akamai.
  - NewsGuard's AI content-farm tracker was skimmed only [[newsguard-2026-tracking]].
  - Related press coverage: [[restofworld-2024-ai]].
- **sd-code-data.**
  - CooRTweet would not install under R 4.5.3.
  - Iocaine and the original Nepenthes were not opened.
  - 60 further Moltbook papers were not followed up.
  - No AI-text detector was run on fox8-23 or BotSim-24, so the result that coordination catches the swarm while
    text detection does not was not reproduced here.
  - MoltGraph's Neo4j dump was not loaded.

**Merge-level notes.**
- `lab.py verify` flags [[lee-2010-uncovering]] because Crossref cuts the title. The full title is from the PDF.
- Eight cross-lane duplicates were folded into the ids cited here; the merge report lists them.
