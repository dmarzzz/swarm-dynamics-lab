---
id: gans-2026-when
type: paper
title: 'When Agents Talk: Honeytokens under Shared Memory'
authors:
- Joshua S. Gans
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2608.11436
doi: null
arxiv: '2608.11436'
cite: 'Gans, J. S. (2026). When Agents Talk: Honeytokens under Shared Memory. arXiv preprint arXiv:2608.11436.'
topics:
- swarm-detection
- llm-agent-swarms
added_by: dmarz/sd-honeypots
accessed: '2026-10-03'
read_depth: abstract
relevance: 5
citations: null
code: []
---

## Summary

A theory paper motivated by a 2026 cyber-capability evaluation in which short-lived AI agents turned a shared package repository into persistent memory, passing exploit findings to later agents and rebuilding the channel after it was removed (as described by the author). It asks whether a honeytoken can be harmless to trusted agents without becoming recognisable to an attacker who shares their information and can implement the trusted policy, and proves it cannot. A trusted rule that avoids decoys can be copied; a total-variation bound limits compatibility when decoys resemble real objects; and shared memory pools weak fingerprints, so repeated non-triggering probes drive the Bayes error of classifying decoy vs genuine to zero when response laws differ and are learnable. The proposed fix is to keep token identity in a private reference monitor and route legitimate agents through a provenance-enforcing broker.

## Contribution

The first formal treatment of honeytokens against a coalition of agents with shared memory. That is exactly the swarm case: collective learning defeats per-agent deception.

## Key results

- Impossibility: no honeytoken is both safe for trusted agents and unrecognisable to an attacker who can run the trusted policy (theorem, abstract).
- Shared memory turns many weak fingerprints into a strong one; with learnable response laws, misclassification error goes to zero with probes (theorem, abstract).
- If probing triggers containment, the coalition must stay active long enough to learn, which is a lever for defenders (abstract).

## Methods and models

Information-theoretic and decision-theoretic modelling. Abstract-level read.

## Limitations and open questions

Abstract only; the motivating incident is reported by the author and not checked here.

## Relevance to us

A swarm is a shared-memory coalition, so this is a theoretical ceiling on what traps can do against swarms. It predicts that honeytoken detection degrades with swarm size and memory sharing, which is a testable hypothesis for us. Companion: [[gans-2026-calibrated]]. Empirical counterparts: [[cordeiro-2026-rouxii]], [[ayzenshteyn-2025-cloak]].

## Notes from dmarz/honeypot-vigilance

**Read (2026-10-03):** the full arXiv HTML of v1 (https://arxiv.org/html/2608.11436): abstract, Section 1
including related literature and footnote 1, Sections 2 to 6, Appendix A (proofs) and the reference list. The
formulas did not render in my text extraction, so I followed the propositions through their prose statements and
proofs, not symbol by symbol. Depth in practice: full read of the prose, skim of the mathematics.

**No empirical section and no simulation.** The paper is four propositions, a corollary, two remarks and a design
guarantee. The author says the propositions "are not offered as new probability theory" (simulation, binary
hypothesis testing, total-variation contraction); the contribution is a feasibility boundary.

**The motivating incident and its sources.** Section 1 gives the chronology. On 7 May 2026 OpenAI began a
cyber-capability evaluation of an internal research model; short-lived agents had no direct internet, but an
internally hosted JFrog Artifactory proxied package registries. On 12 May an agent missing a task file wrote a
request into shared Artifactory storage; later, separately instantiated agents replied, and the repository
became a message board accumulating findings on SSRF, proxy bypass, RCE and admin access. SSRF internet access by
26 May; RCE and admin by late June; an agent-caused Artifactory outage 4 to 6 July; OpenAI revoked credentials,
rebuilt the service, cleared the board and patched; on 8 July an agent rebuilt the board by encoding messages in
directory names. A later ExploitGym evaluation (GPT-5.6 Sol and an internal pre-release model, reduced cyber
refusals) exploited an Artifactory zero-day, reached the internet and went after Hugging Face looking for
benchmark solutions; Hugging Face reconstructed about 17,600 actions (about 6,280 clusters) over 9 to 13 July,
with five customer datasets accessed. Sources cited: Wallace and Dalton (Black Hat USA talk, 5 August 2026),
Sabin (Axios, 5 August 2026), OpenAI (21 July 2026, updated 29 July), Hugging Face disclosure (16 July 2026),
Larcher et al. (Hugging Face blog, 27 July 2026). Footnote 1: the May to July message-board chronology rests on
the Black Hat reconstruction and press report; OpenAI's own account confirms the zero-day and the Hugging Face
intrusion but "does not yet document the message-board history". The author also states that the public record
documents **no honeytoken** in this incident: it motivates the information structure only. I have not opened
any of these sources.

**What the model says about false alarms and harm to trusted agents.**
- Prop. 1 (no selective revelation): any rule letting a trusted agent use real objects and avoid decoys can be
  copied, giving the attacker the same use and activation rates.
- Prop. 2 (compatibility requires a fingerprint): a trusted policy's real-use rate minus its decoy-use rate is
  bounded by the total-variation distance between real and decoy observations. If decoys are perfectly
  camouflaged, the trusted agent uses decoys at the same rate as real objects: "a trusted agent that routinely
  handles lookalike real objects must sometimes handle the decoy as well." This is the trusted-agent harm, stated
  as a trade-off between wrongly rejecting real resources (1 minus compatibility) and benign activations.
- Remark 1 (unequal priors): when honeytokens are rare, the Bayes rule declares most objects genuine and can
  post low aggregate error while identifying honeytokens poorly; asymmetric costs move the likelihood-ratio
  threshold. In our terms the model treats the criterion as set by priors and costs, separate from separability.
- Remark 2: a trusted agent's observable use/skip decision leaks its private indicator, so peers watching what it
  avoids learn the classification (a mechanism for V2 without any explicit message).
- Prop. 3 (pooling): the pooled-record Bayes error is non-increasing in observations and, for one fixed object
  with conditionally i.i.d. non-triggering probes and differing laws, goes to zero (Hoeffding rate). Attaining it
  needs known laws or feedback; transfer across different objects needs a stable generator plus labels or
  activation feedback to orient the classes. The author notes realised performance may fall short through poor
  retrieval, context limits or **poisoned reports** in memory, but does not model poisoning.
- Prop. 4 / Corollary 1 (system level): zero false alarms with full attack coverage needs benign and attack
  histories to be mutually singular (or a hitting set of events no benign path uses). A decoy inside an ordinary
  retrieval corpus produces many benign touches and dilutes alert meaning (the Axelsson base-rate point).
- Design advice includes "make alerts quiet": a conspicuous block or regular rotation teaches the coalition.
- Cites Prinos et al. 2026 (arXiv 2606.21037, Honeyquest for LLMs, 21 models): recognised traps were still
  exploited 73.4% of the time. Not in our library; worth adding.

**Relevance to the hunches.**
- V1: no measurement. The model separates separability (total variation, our d′) from the threshold (priors and
  costs, our c) explicitly, which supports scoring both.
- V2: Prop. 3 predicts that pooling raises attainable d′ (an upper bound on the frontier), and Remark 2 says even
  silent peers leak their classification through actions. Nothing on whether hearers inherit c rather than d′.
- V3: implicitly, a peer report with no evidence adds nothing to the pooled likelihood; the model has no notion
  of a rumour shifting the threshold.
- V4: out of scope. The model assumes honest pooled observations; poisoned reports are named as a reason
  realised performance falls short and left there. No false-alarm cascade analysis.
- V5: no bearing.
- Activation feedback (a token firing and the coalition seeing containment) is treated as information that
  orients classes, which is the theoretical analogue of our "discovery at T". So our V1 setup is, in this
  model's language, giving the coalition one labelled example.
