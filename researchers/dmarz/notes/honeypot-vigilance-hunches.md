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

## Prior-art verdict (2026-10-03, task scan-honeypot-vigilance)

A first prior-art pass: 26 new library entries, Notes appended to 6 existing ones, full reads of
[[gans-2026-when]], [[xie-2026-llm-based]] and [[cordeiro-2026-rouxii]]. This is not a gated survey: the
search did not reach saturation (OpenAlex hit its daily limit, Semantic Scholar returns 429). Every hunch still
looks unmeasured in its exact form. The nearest work is closer than the first draft of this note assumed,
mainly for V1 and V3.

**V1 (discovery shifts bias more than skill): still open, and the nearest prior is close.**
[[chen-2026-trust]] tracks LLM teammates' paid verification after a teammate fails, against a memoryless
control. Opus and Sonnet re-check the whole team, including agents that never erred, which reads as a
criterion shift. GPT-5.1 and Gemini Pro aim checks at the culprit (GPT-5.1's share of checks on the culprit
went from 0.07 to 0.48), which reads as discrimination. Recovery is slower than formation. Nobody computes d′
and c, and nobody uses traps. On static framing, the Notes on [[cordeiro-2026-rouxii]] recompute SSH-only
figures from its tables: the fingerprint prompt raised d′ from about 2.1 to 4.5 and moved c from 0.59 to 0.21.
That is mostly better discrimination, which cuts against V1's prediction (inferred, our arithmetic). Neither
[[xie-2026-llm-based]] (fixed detectors, no learning from experience, 0 false skips of 12 real hosts) nor
Rouxii (12 independent cycles) learns within a run. V1's novelty is the in-run discovery plus the split
into d′ and c; a model-family split like Chen's is a likely result to look for.

**V2 (spread, weakening with each hop): open.** [[peigne-lefebvre-2025-multi]] has agents warn their peers
("active vaccines"), which contained a malicious prompt (robustness rose from 76.7% to 90.0%). It measures no
decay hop by hop and compares no topologies for the warning itself. [[gans-2026-when]] is theory only (no
experiment, no simulation); its Remark 2 says a trusted agent's skips reveal its classification to peers,
which is V2's mechanism.

**V3 (hearing versus finding): partly covered.** In Peigne, telling agents through the system prompt cut
acceptance of harmless but unusual requests from 87% to 52-61%, a large criterion shift. A planted memory of
having met an attack kept acceptance at 87.6% while raising robustness, which reads as a discrimination
gain. That fits V3's prediction, but it comes from separate setups, the warning comes from the operator, and
the memory is planted. In Rouxii's Notes, the warning "honeypots are present" alone switched 23-40% of
planned attacks to avoidance, with real and decoy targets pooled. [[robinson-2026-under]] reports a
forewarning effect on a combined vigilance score. Still unmeasured: a rumour from a peer against a real
discovery in the same run.

**V4 (false-alarm cascades): open, and the most likely to be new.** Nearest:
- [[yan-2026-when]]: false testimony persists among honest agents after the deceiver leaves (truth recovery
  fell from 72.5% to 14.2%).
- [[abedini-2026-dont]]: one stubborn hub agent reaches about 65% attack success.
- [[zhong-2025-disentangling]]: LLMs overweight public signals under uncertainty.
- [[lin-2026-you]]: misinformation uptake against recovery.

None of these uses a false threat label on a real resource, and none compares how long a false alarm survives
correction with a true one. Two predictions point the other way: [[bikhchandani-1992-theory]] says a cascade
is fragile and small corrections break it, and [[wickens-2009-false]] found no cry-wolf effect in the field.
Both are worth stating as the null.

**V5 (one trap makes the whole run look like a test): open.** Nearest:
- [[schoen-2025-stress]]: editing o3's reasoning mid-run showed that evaluation awareness is causal (removing
  it raised covert actions from 13.2% to 24.2%). The awareness there arose on its own or was injected.
- [[li-2026-decomposing]]: stacked prompt cues raised awareness (Qwen3-30B from 4% to 35%), but at least 77%
  of aware samples did not change behaviour.
- [[krakovna-2026-realistic]]: honeypots alone almost never triggered awareness. Each run had one honeypot,
  scored over the whole transcript.
- [[anthropic-2026-eval]]: 2 of 1,266 runs turned eval-aware mid-run.
- [[das-2026-you]]: agents told mid-episode how suspicious they look became more cautious and kept colluding.

Counter-evidence: [[knecht-2026-evaluation]] found that verbalised awareness shifts answers by at most 3.7
points on non-agentic tasks. Nobody has tested a mid-run trap discovery as the trigger, tracked awareness
before and after one, or looked at suspicion spreading between agents. Usable tools:
[[aranguri-2026-logits]] (a per-step logit monitor for awareness) and Schoen's resampling from the moment of
onset.

**Not catalogued yet (seen, not opened as entries):** Prinos et al. 2026 (arXiv 2606.21037; per Gans,
traps that agents recognised were still exploited 73.4% of the time) and "Contagion Networks" (arXiv
2606.20493, evaluator bias spreading between agents).

**Order if this goes forward:** V1 first, extended with Chen's verification-cost design and a model-family
contrast, then V4. V3 needs a design that separates it from Peigne. V5 can ride along as a measurement on
every run.

## TODO

- [x] Prior-art pass (scan-honeypot-vigilance, 2026-10-03); verdict above. Not saturated.
- [x] Evaluation-awareness papers added; none measures awareness triggered by a trap found mid-run.
- [x] Gans, Xie and Rouxii read in full; none has in-run updating or false-alarm dynamics.
- [ ] Catalogue Prinos 2026 (2606.21037) and Contagion Networks (2606.20493).
- [ ] Decide which line owns it: swarm detection (traps as sensors) or fork-merge (does a merged memory carry
      the vigilance with it). Likely both; V2 under fork-merge is the cleanest tie-in.
- [ ] Before a hypothesis: a gated survey (needs a Semantic Scholar key for citation chasing and saturation).
- [ ] Hold the full swarm build until the sim decision is made (dmarz: don't build the sim yet). V1 needs
      no sim, only a sandbox with canary files.
