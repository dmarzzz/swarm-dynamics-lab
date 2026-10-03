---
id: pavlova-2026-flag
type: paper
title: 'Flag Game: A Toy Model for Mechanistic Swarm Interpretability'
authors: [Elizabeth Pavlova, Hidenori Tanaka]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2609.19124
doi: null
arxiv: '2609.19124'
cite: 'Pavlova, E., & Tanaka, H. (2026). Flag Game: A Toy Model for Mechanistic Swarm Interpretability. arXiv preprint arXiv:2609.19124.'
topics: [llm-agent-swarms, collective-decision, criticality-measurement]
added_by: shadow/sol-1
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: not indexed yet (arXiv listing 2026-09-16; checked arXiv export API 2026-10-03, no OpenAlex record found)
code: []
---

## Summary

A controlled toy model of collective belief formation in populations of bounded LLM agents, motivated explicitly by the OpenAI Hugging Face incident (false belief about the scorer spreading over a message board) and the German wiki swarm. A hidden country flag is the ground truth; each of N agents gets only a private crop (6 x 4 cells of a 24 x 16 render), so some crops are decisive and some ambiguous. Agents exchange country guesses (bandwidth m = 1) or guess plus reason (m = 3) under three protocols: pairwise (asynchronous random speaker-listener, memory H = 8), broadcast (synchronous, everyone sees all current reports) and manager (a blind synthesiser reads observer reports). Endpoints are classified as correct consensus (top share >= 0.85 and correct), wrong consensus, polarisation (two camps each >= 0.25) or fragmentation. Main measured results (GPT-4o, pairwise, 40 seeds per N): collective accuracy peaks at intermediate N = 16 and declines at larger N; wrong consensus falls from 26 to 34% at N = 4 to 0% at N = 128 while polarisation rises from 13 to 24% to 57 to 60% (Table 3, threshold-robustness ranges). The France versus Peru example shows N = 4 undecided, N = 16 correct consensus, N = 64 a truth-rival split. Social-awareness prompting in broadcast raises terminal truth mass from 0.54 to 0.81; in pairwise it has an interior optimum at alpha = 0.75 (more uptake amplifies wrong speakers). Mixed GPT-4o/GPT-5.4 teams beat homogeneous ones; the models fail differently (GPT-4o errors are crop-compatible, GPT-5.4 errors are not). Manager identity matters: GPT-5.4 managers 0.57, GPT-4o managers 0.48 on the same observers. A single-agent memory probe shows Claude Haiku 4.5 abandons a uniquely-identifying crop as social memory accumulates (sycophantic override) while GPT-4o and GPT-5.4 hold firm. Section 5 introduces social circuit attribution: the score S_i = (accuracy gain of a planted crop) x (temporal closeness in the communication schedule) predicts which agent to patch; patching agent A4 at N = 8 lifts collective accuracy from 25% to 100% in the illustrated run, and patching one eighth of agents gives +40 points at N = 8 falling to about +17 at N = 128. A two-belief statistical-mechanics model (Quantized Simplex Gossip of Tanaka 2026 plus evidence-induced zealots and biased adoption of ambiguous agents) reproduces the phase diagram: collapse at small N (memetic drift), correct consensus at intermediate N, persistent truth-rival polarisation at large N as fluctuations shrink with N. Total compute about $25,000 of hosted API, main runs GPT-4o and GPT-5.4, temperature 0.2. Demo at flag-game-demo.vercel.app; the paper says synthetic task and evaluation code are released but no repository URL appears in the text I read.

## Contribution

The first testbed where each agent's private evidence is assigned and replayable, so the experimenter can tell apart evidence that was absent, present but unshared, overridden, or stabilised into rival camps. Names the two failure modes (collective belief collapse versus polarisation) and shows the crossover with N. Imports activation-patching logic to swarms (agent patching) and shows it loses power with N, motivating a population-level theory. Builds directly on [[tanaka-2026-when]] (QSG, memetic drift) and sits beside [[de-marzo-2024-ai]], [[okawa-2026-emergence]] and [[el-2026-physics]] in the physics-of-LLM-populations line.

## Key results

- Measured: pairwise GPT-4o, correct consensus 50 to 53% at N = 4 and 16, 37 to 42% at N = 64, 38 to 41% at N = 128; wrong consensus 26 to 34% at N = 4, 0% at N >= 32; polarised 13 to 24% at N = 4 rising to 57 to 60% at N = 128 (Table 3).
- Measured: broadcast social-awareness sweep, terminal truth mass 0.54 to 0.81 (N = 8, m = 3, 30 seeds per cell).
- Measured: pairwise alpha sweep has an interior optimum at alpha = 0.75 (Appendix B, N = 16, 28 seeds per alpha).
- Measured: manager protocol, GPT-5.4 manager 0.57 versus GPT-4o manager 0.48 with identical observers (60 matched seeds).
- Measured: agent patching, +40 points mean collective accuracy at N = 8 falling to about +17 at N = 128 when one eighth of agents are patched (10 runs each).
- Inferred (theory): the mean-field closure of the zealot-plus-copying model gives three regimes in N that match the empirical phase diagram; the authors call this phenomenological.

## Methods and models

N in {4, 8, 16, 32, 64, 128}. Three protocols as above. Crops rendered at scale 25 from a 24 x 16 canvas, 6 x 4 cells per agent. Temperature 0.2, top-p 1.0, multimodal prompt (text plus crop image). Models GPT-4o and GPT-5.4 for main runs, Claude Haiku 4.5 and Sonnet 4.6 for probes. Observables: terminal distribution over country labels, top share s_1, endpoint class, collective mean accuracy. Theory: two beliefs T and R, agents typed truth-deciding / rival-deciding / ambiguous with probabilities a_T, a_R, a_0; zealots keep their belief, ambiguous agents copy a random speaker with acceptance ratio q_T/q_R = exp(h_0); birth-death chain on the count of ambiguous agents holding T with rates W_+(n) and W_-(n); mean-field and finite-N analysis in Appendix G.

## Limitations and open questions

- Authors: a diagnostic task, not a model of deployed swarms; results depend on prompts, memory format, protocol and aggregation; only two main models; sweeps are expensive (about $25K).
- Noticed: no open-weight model in the main sweep, so replication at hackathon budget means re-running with small local models, which the memory probe suggests will behave differently (Haiku-style override).
- Noticed: the N-sweep is pairwise only; the broadcast N-sweep (closest to a shared message board) is not reported.
- Noticed: no code URL in the HTML at access time; the X thread [[x-hidenori8tanaka-2105704088952619185]] says code is promised.

## Relevance to us

The closest existing experiment to what the hackathon asks for: a measurable swarm-dynamics phenomenon (collapse to polarisation crossover with N) in an LLM population with ground truth. Any hackathon experiment on consensus versus N, committed minorities or message-board broadcast should cite this and position itself as a replication with open models, a protocol variant (broadcast N-sweep, board with persistence) or a transfer to the real incident data ([[gh-catgirl3d-agent-collusion-wiki-archive]], [[gh-killy-netsphere-sealed-swarm-transcripts]]). See also [[ashery-2024-emergent]], [[flint-2026-group]], [[bertalanic-2026-ringelmann]].
