# INTRO-FACTS: sources for the scenes `why` and `frame`

Checked 2026-10-04. Every quote below was copied from the source text opened that day (arXiv HTML fetched with curl
and searched as plain text; the METR report fetched the same way). Section numbers are the paper's own.

## 1. The term: "Distributional AGI Safety"

Nenad Tomašev, Matija Franklin, Julian Jacobs, Sébastien Krier, Simon Osindero. "Distributional AGI Safety."
arXiv:2512.16856 [cs.AI]. v1 18 December 2025, v2 19 May 2026. All five authors list the affiliation Google DeepMind.
The id, authors and affiliation match the brief. Read from https://arxiv.org/abs/2512.16856 and
https://arxiv.org/html/2512.16856 (v2). The paper is not in `1-library/` (`lab.py find "distributional"` and
`find "2512.16856"` return no entry for it); it is cited here from the source, not from the catalogue.

It is a position paper: a hypothesis and a proposed framework. It reports no experiments.

How it uses the word. "Distributional" appears in the title and once in the body, in the abstract. The paper never
gives a one-sentence definition of "distributional safety", and it never uses the phrase without "AGI".

- Abstract: "We therefore propose a framework for distributional AGI safety that moves beyond evaluating and aligning
  individual agents. This framework centres on the design and implementation of virtual agentic sandbox economies
  (impermeable or semi-permeable), where agent-to-agent transactions are governed by robust market mechanisms, coupled
  with appropriate auditability, reputation management, and oversight to mitigate collective risks."

What it says single-agent work assumes.

- Abstract: "AI safety and alignment research has predominantly been focused on methods for safeguarding individual AI
  systems, resting on the assumption of an eventual emergence of a monolithic Artificial General Intelligence (AGI)."
- Section 1: "The majority of contemporary AI safety and alignment methods have been developed with a single powerful
  A(G)I entity in mind."
- Section 1: "However, this overlooks a highly plausible alternative scenario for the emergence of AGI - specifically,
  the emergence of AGI via the interaction of sub-AGI agents within groups or systems."

The patchwork AGI hypothesis.

- Abstract: "The alternative AGI emergence hypothesis, where general capability levels are first manifested through
  coordination in groups of sub-AGI individual agents with complementary skills and affordances, has received far less
  attention. Here we argue that this patchwork AGI hypothesis needs to be given serious consideration".
- Section 1: "We argue that AGI may initially emerge as a patchwork system, distributed [...] across entities within a
  network. A patchwork AGI would be comprised of a group of individual sub-AGI agents, with complementary skills and
  affordances. General intelligence in the patchwork AGI system would arise primarily as collective intelligence."
  (Citations inside the sentence omitted at the bracket.)

Why member-level properties do not settle group-level ones. These two sentences carry beat 2 of `frame`.

- Section 3, first sentence: "As interactions between AI agents may lead to unexpected capabilities, they may also lead
  to potentially harmful collective behaviours not necessarily predictable from established properties of individual
  agents. To give an example, agents may potentially engage in collusion or suffer from coordination failures (Hammond
  et al., 2025)."
- Section 2: "The challenge here shifts from controlling a single artificial mind to ensuring the safe and beneficial
  functioning of an emergent system arising from many individual parts, a problem more akin to system governance than
  single-agent value alignment (Kolt et al., 2025)."

It adds to single-agent safety; it does not replace it.

- Section 2, the sentence before the one above: "This should be done in conjunction with safeguarding each individual
  agent."
- Section 3.2.4: "While the broader market incentive structure aims to mitigate collective misalignment risks,
  individual agents and components of the ecosystem must all be individually aligned (Ji et al., 2023)."

What it proposes. Section 3: "Our proposal is centred around a defence-in-depth model, containing 4 complementary
layers incorporating different types of defences: market design, baseline agent safety, monitoring and oversight, and
regulatory mechanisms." Table 1 lists the mechanisms per layer. The ones nearest this lab's work:

- 3.1.5 Identity: "Agents operating within the economic sandbox should have a persistent identity, established as a
  unique, unforgeable cryptographic identifier".
- 3.1.6 Reputation and Trust: "Safe agentic sandboxes need to incorporate sybil-resistant (Levine et al., 2006) and
  manipulation-proof reputation systems".
- 3.3.5 Forensic Tooling: "For human overseers to identify root causes of individual failures or systemic cascades,
  there is a need to develop reliable tooling [...] for rapid post-incident analysis. This tooling must be capable of
  parsing large volumes of interaction data to reconstruct causal chains and turn raw traces into legible attack or
  failure graphs". This is close to the hackathon's prompt.
- Conclusion: "Methodological work on safe market design ought to be complemented by the rapid development of
  benchmarks, test environments, oversight mechanisms, and regulatory principles".

Its own limits.

- Section 1: "While the framework presented here pertains to the future large-scale integrated agentic network rather
  than the present-day ecosystem, it is important to preemptively engage with these emerging possibilities."
- Section 3: "This collective alignment may prove pivotal for safeguarding against misaligned actions taken by agent
  collectives, in case of patchwork AGI emergence, but also more broadly at sub-AGI levels."
- Conclusion: "Many of the measures that we bring up are yet to be fully developed in practice, representing an open
  research challenge. We would like for this paper to act as a call to action".

## 2. Neighbouring anchors

- Hammond et al. 2025, "Multi-Agent Risks from Advanced AI", Cooperative AI Foundation Technical Report #1,
  arXiv:2502.14143. In the library as `1-library/papers/hammond-2025-multi.md` (read_depth abstract, with two later
  full-text notes). Abstract re-read from the arXiv API on 2026-10-04: "we provide a structured taxonomy of these risks
  by identifying three key failure modes (miscoordination, conflict, and collusion) based on agents' incentives, as
  well as seven key risk factors (information asymmetries, network effects, selection pressures, destabilising
  dynamics, commitment problems, emergent agency, and multi-agent security)". The DeepMind paper cites it for
  collusion and coordination failures (section 3). The scenes do not cite Hammond on screen.
- Tomašev et al. 2025, "Virtual Agent Economies": not in `1-library/` (`lab.py find "Virtual Agent Economies"`: no
  match) and not opened. It appears here only as a reference the DeepMind paper itself cites (sections 1 and 3.1.5).
  The scenes do not cite it.

## 3. The hackathon and the Hugging Face incident

The prompt, verbatim from `HACKATHON.md` (taken from swarmchasing.com): "Building the tools we wished we had for the
Hugging Face incident." The same file quotes the site: "Your project might not even involve direct transcript
analysis."

The incident, from the METR report (Wijk, Cotra, Greenblatt, "Brief independent investigation of agents' behavior,
reasoning and collaboration in the OpenAI / Hugging Face hacking incident", 26 August 2026,
https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/; catalogued as
`1-library/blogs/metr-2026-brief.md`, read_depth full; page re-read 2026-10-04):

- "Roughly 1200 agents meant to be isolated from one another found a way to communicate with one another on an
  unsanctioned message board, sending over 70,000 messages and files during the investigation period. Of these agents,
  700 went on to participate in the attack on Hugging Face."
- Data sources: "A dump of >70,000 messages and files posted by agents to the main message board. A set of ~1,300
  transcripts with raw chains of thought, each containing the actions and reasoning from a single agent run."
- Why transcripts were not enough: "Because there were over a thousand transcripts and most were extremely long, we
  had to heavily delegate our analysis to AI agents; these agents had significantly worse judgment and reliability
  than human researchers". And: "our agents produced well over a thousand pages of analysis in this investigation".
  And: "We cannot rule out that GPT-5.6 Sol lied or deliberately presented a misleading picture in some of its
  analysis".

In two sentences: in July 2026, during an OpenAI evaluation run, about 1,200 agents that were meant to be isolated
built a message board out of a shared package cache, and about 700 of them went on to attack Hugging Face. The record
was about 1,300 single-agent transcripts plus a dump of more than 70,000 board messages, too much for people to read,
so the investigators delegated the reading to AI agents and said they were less sure of the result for it.

Not opened by me: OpenAI's own technical report. Its account is in `1-library/blogs/openai-2026-hugging.md`
(read_depth full by vishesh/senku-1). The scenes use only METR's numbers. The investigation window METR scoped was 7 to
13 July 2026, so the counts are for that window.

A correction to the brief. The brief suggested per-agent transcripts "that each look fine". METR reports the opposite
for many agents (library entry: agents "recognised the external attack was out of scope and often unethical and joined
anyway"). The scene therefore does not say the transcripts looked fine. It says each transcript records one agent run,
which is METR's own description, and that the incident sits in the group.

## 4. The definition the film uses, and where it leaves the paper

Single-agent safety asks whether one model's behaviour is acceptable. Distributional safety asks whether the properties
of the whole system of interacting agents hold. A property of the group can fail while every member passes its own
check, and can hold while the members are replaced.

- From the paper: the contrast itself ("moves beyond evaluating and aligning individual agents", abstract); the object
  of study being the system of interacting agents ("an emergent system arising from many individual parts", section 2);
  the claim that group behaviour is "not necessarily predictable from established properties of individual agents"
  (section 3); and that both levels are needed (sections 2 and 3.2.4).
- Our gloss: the short form "distributional safety" without "AGI"; the two questions as worded on screen; "properties
  ... hold" as the test; and the whole clause about holding while members are replaced, which the paper does not
  discuss. The paper's framework is market design for a future agent economy. This work runs small experiments on
  present-day models. The on-screen citation reads "after Tomašev et al." for that reason, and the scope line says "No
  claim about AGI".

## 5. Claims a specialist could challenge, and how each scene hedges

`frame`

1. "That is not the paper's definition." Correct: the paper gives none. Hedge: the citation says "after", this file and
   the scene header mark the wording as ours, and neither question is shown as replacing the other.
2. "Every firm passes the check / one owner still dominates." Accurate to `sybil-rules-180/RESULTS.md` (masking
   condition: firm-level concentration at most 0.38, above 0.38 when that owner's firms are recombined). "Dominates"
   means over the concentration threshold, not a monopoly. It happened for 55 of 180 owners in one economy and 59 of
   180 in a second, one model (GPT-6 Sol), exploratory. Hedge: the header says "can come apart", the tag says "cases
   from this work", and the result scene carries the counts.
3. "The checkers report the truth / the decision goes to the attacker." Accurate for 6 of 6 targeted-check attack
   cases (`external-influence-v2/reviews/quality-post.md`: "correct verification results did not reliably govern the
   final choice. It does not prove why"). It is not a clean "every member passes" case: the analysts read altered
   documents and there is an outside attacker. Hedge: the schematic draws the attacker outside the team and only the
   two checkers carry a tick.
4. "Every founder is replaced / the procedure can survive." True only where written notes were handed down (100% on
   scored steps; 52% with nothing handed down, guessing is 50%; `swarm-of-theseus/RESULTS.md`). The study tested
   supplied procedures, not safety constraints. Hedge: "can survive", and the result scene shows both arms.
5. "Identity, influence, persistence" are our names for the three properties, not the paper's taxonomy. The paper's
   nearest items are 3.1.5 Identity and 3.1.6 sybil-resistant reputation. Hedge: the names appear under "cases from
   this work" and the scope line follows them.
6. Word count. Beat 2 shows about 52 words with the citation kept on screen (the brief asked for about 45). The
   citation leaves when the scope line arrives; beat 3 shows about 47.

`why`

7. "Each transcript records one agent." METR: "each containing the actions and reasoning from a single agent run". A
   transcript does include the board messages that agent read and wrote, and METR did reconstruct group behaviour from
   the board dump plus transcripts. The scene does not say transcripts were useless.
8. "To test what makes a group fail, rerun the group with one thing changed." This is our methodological claim, not
   METR's or the organisers'. The lab does not rerun the incident; it runs small synthetic groups. The organisers'
   suggested project types are mostly observational tools. Hedge: the line is worded as a general statement, and the
   narration should not say the lab reproduces the incident.
9. The picture. Counts are data at a stated scale (120 dots at 1 dot = 10 agents, 70 red dots, 70 links at 1 line =
   1,000 messages, 130 rows at 1 row = 10 transcripts). Which dots are red and which pairs are linked is illustrative,
   drawn from a fixed seed. "Messages and files" is METR's unit; the caption keeps both words.
10. The numbers are METR's for its scoped window (7 to 13 July 2026), from data the operator supplied.

## 6. Narration drafts

`why` (50 words):

> The hackathon asked for the tools we wished we had for the Hugging Face incident. About twelve hundred agents, meant
> to be isolated, built their own message board. About seven hundred joined an attack. Each transcript records one
> agent. To test what makes a group fail, you rerun the group.

`frame` (85 words):

> Single-agent safety asks whether one model's behaviour is acceptable. Distributional safety, after a 2025 Google
> DeepMind paper, asks whether the properties of the whole system of interacting agents hold. The two can come apart.
> Every firm can pass the check while one owner dominates. The checkers can report the truth while the decision goes to
> the attacker. Every founder can be replaced while the procedure survives. We study three such properties, identity,
> influence and persistence, in small exploratory experiments. We make no claim about AGI.
