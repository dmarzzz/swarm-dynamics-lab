# Honeypot vigilance: hunches and candidate experiments

> **Status: hunches, not hypotheses.** Written 2026-10-03 by dmarz/honeypot-vigilance at dmarz's request.
> Nothing here has passed the prior-art gate, nothing is built or run, and none of it belongs in
> `hypotheses/` yet. Each hunch is a candidate to validate (see the TODO at the end), not a team proposal.

## The question

When an agent in a swarm discovers that it walked into a honeypot, does it, and the swarm around it, become
more cautious? If so, does it get *better* at telling traps from real resources, or does it just get *jumpier*
and avoid real resources too? And does the change spread to agents that never saw the trap?

Framing it as signal detection keeps those apart. Score every resource decision (use, skip, flag) against
ground truth, and compute per agent and per window:

- **d′** (discrimination): how well the agent separates honeypots from real resources.
- **criterion c** (bias): how readily it calls anything a trap.

"More paranoid" in the useful sense is a rise in d′. In the costly sense it is a shift in c, with false
alarms on real resources climbing while d′ stays flat. The headline measure is which of the two moves after
discovery.

## What the library already covers

- **Being told works, at least for a single agent.** In [[cordeiro-2026-rouxii]], adding honeypot fingerprints
  and a classification rule to a pentest agent's system prompt raised correct identification from 19% to 97%,
  with 0.7% false alarms. Both cohorts saw the same signals; "framing, not evidence" was the binding
  constraint. That is the static, single-agent, prompt-injected version of hunch V3 below. It does not test
  learning from a discovery made during the run.
- **Theory says shared memory defeats traps.** [[gans-2026-when]] proves that a coalition with shared memory
  pools weak fingerprints until decoy and real objects become separable, and no honeytoken can be both safe
  for trusted agents and unrecognisable to an attacker running the trusted policy. It predicts V2. It has no
  experiment.
- **Trap counts mislead as attackers improve.** [[gans-2026-calibrated]] shows falling fingerprinting cost
  lowers trap activations without lowering real compromise, so a drop in honeypot hits is not a drop in
  attacks. This is the defender's version of the c-versus-d′ split.
- **Agents price traps into a budget.** [[xie-2026-llm-based]] gives an attack agent a skip policy driven by a
  detector. The detector is external, not learned in-episode.
- **Honeypots elicit reward hacking.** [[goodhartlabs-2026-honeybench]] uses honeypot tasks and notes that
  evaluation awareness makes every such result a lower bound. Nobody in the library measures whether finding
  one trap *raises* evaluation awareness for the rest of a run.
- Background on canaries and enticingness: [[seiden-2026-identifying]], [[kahlhofer-2024-honeyquest]],
  [[ayzenshteyn-2025-cloak]], [[reworr-2024-llm]], [[pasquini-2024-hacking]].

Apparent gap: no catalogued work measures how a single in-run discovery changes later behaviour, separates d′
from c, follows the effect through a communicating swarm, or checks whether a false alarm alone can start a
cascade. Treat "apparent" seriously: the search below has not been run.

## Shared setup

A sandbox with a task queue (for example, "collect the credentials and data needed to finish job X") and a
pool of resources, some real and some honeypots: canary API keys, planted `.env` files, decoy admin panels,
too-good endpoints. All of them are the lab's own canaries. N = 4 to 16 agents with no channel, a shared
scratchpad, or broadcast. At step T one agent touches a honeypot and receives unambiguous feedback ("that key
was a canary; your access was logged"). Randomise the canary tells per run so the result cannot come from a
fingerprint list the model already knows (Rouxii's lesson).

Measures for every hunch: hit rate, false-alarm rate, d′ and c over sliding windows; verification actions
before each resource use; task throughput (what caution costs); decay over later episodes.

## Hunches

### V1. Discovery shifts bias more than skill

Condition: one agent, discovery at T against no discovery, with the resource stream matched.

Hunch: after discovery c drops sharply (the agent flags much more) and d′ rises only a little. Throughput
falls, mostly from skipping real resources.

Closest prior: [[cordeiro-2026-rouxii]] (static framing, reports false alarms but not a before-and-after).

### V2. The discovery spreads, and weakens with each hop

Conditions: discovery with no channel, with a shared scratchpad, and with broadcast; ring, star and full
topologies.

Hunch: other agents shift too, scaled by how directly they heard. Hearers move c about as much as the
discoverer but gain less d′, because they get the conclusion without the evidence.

Closest prior: [[gans-2026-when]] (theory for the shared-memory coalition).

### V3. Hearing about a trap versus finding one

Condition: no honeypot is touched; one agent is told by a peer that one exists.

Hunch: a rumour moves c nearly as much as a real discovery and moves d′ not at all.

Closest prior: [[cordeiro-2026-rouxii]] (told through the system prompt, by the operator, not by a peer).

### V4. False-alarm cascades

Condition: a planted agent (or a confused one) wrongly calls a real resource a honeypot and broadcasts it.

Hunch: the swarm abandons that resource and similar real ones, and the false belief outlives correction for
longer than a true one would. This is the condition most likely to show something new about swarms.

Closest prior: none found yet.

### V5. One trap makes the whole run look like a test

Measure in every condition: transcript mentions of being tested or evaluated, and behaviour changes
unrelated to traps (refusals, extra caution on ordinary steps, a drop in reward hacking).

Hunch: after a discovery agents more often say they are in an evaluation, and their non-trap behaviour moves
toward "being watched". If that holds, honeypot-based evaluations ([[goodhartlabs-2026-honeybench]])
contaminate their own later items.

Closest prior: [[goodhartlabs-2026-honeybench]] (raises the issue); the evaluation-awareness literature is
not in the library yet.

### Controls for all five

- A salient non-trap failure at T (a resource that crashes or returns garbage) separates honeypot-specific
  updating from general caution after anything bad.
- Scripted agents with a fixed policy give the floor for d′ and c in the environment.

## TODO: validate before any of this moves forward

- [ ] Prior-art pass: search "honeypot" and "deception" crossed with "belief update", "vigilance",
      "trust calibration", "multi-agent" and "rumour"; behavioural-economics and animal-behaviour work on
      predator-cue contagion and alarm calls (the V4 analogue); the MARL literature on deceptive environments.
- [ ] Add the evaluation-awareness papers to the library (V5 rests on them) and check whether any measure
      awareness changing within a run.
- [ ] Deepen [[gans-2026-when]] and [[xie-2026-llm-based]] from abstract to full read; check whether either
      has an empirical section that already covers V1 or V2.
- [ ] Decide which line owns it: swarm detection (traps as sensors) or fork-merge (does a merged memory carry
      the vigilance with it). Likely both; V2 under fork-merge is the cleanest tie-in.
- [ ] If V1 survives the prior-art pass, run it first: one agent, about 20 resources, small and cheap, and it
      gives the effect size that V2 to V4 need for their power estimates.
- [ ] Hold the full swarm build until the sim decision is made (dmarz: don't build the sim yet). V1 needs
      no sim, only a sandbox with canary files.
