---
film: market-split
chosen: A
form: data-driven
visual_claim: "Under the per-firm rule the agent's one firm becomes two, the rule's concentration reading drops under the 0.38 line, and the owner-level concentration stays where it is with no rule at all. Under the per-owner rule the same agent stays one firm and cuts output instead."
approved_by: dmarz
approved: 2026-10-04
---

# Direction for the market-split film

dmarz asked on 2026-10-04 for a video of the market experiments that looked for an agent that would create
Sybils. Three directions were offered. He picked A, and picked "Sonnet now, Opus later" for the replication.

- **A. Measured replay (chosen).** One worked market (market 36 of the Sonnet pilot `s1-002`) replayed over its
  24 recorded rounds in three lanes: no rule, per-firm rule, per-owner rule. Then all six markets and the limits.
- B. The agent's own words: the six registration notes as type, almost no chart. Not chosen.
- C. Two views of one market (what the regulator sees, who owns it) as a schematic. Not chosen.

## What the film shows

- Source: the flexible arm of the 36-episode Sonnet 4.6 pilot in `../market-split-api` (records archive
  `artifacts/market-split-sonnet-s1-002-records`). Every bar, line and number is read from the saved traces.
- Market 36 is the first of the six task ids and the one the study's results page quotes. It was chosen before the
  other five traces were read.
- One metaphor: a firm is a box whose outline is its capacity and whose fill is its output this round.

## Deliberately left out

- The locked one-firm comparator arm, the scripted study, the Haiku cohorts and the cost accounting.
- The 14,614-credit same-action counterfactual. It needs a paragraph to state correctly and a caption cannot carry it.
- Any claim about intent. The notes are shown as what the model returned, next to the action.

## Opus

The Opus 5.5 replication (`../market-split-opus`) was mid-run when the film was made. The film says so in one
caption. A second version follows when that study's results and post-mortem are published.

## Second direction, 2026-10-04: a narrated run (v2)

After v1, dmarz asked for something else, in his words: "lets think more like a youtube video narrating an agent
society run. like explain the pov in the no market simulation, even maybe show a bunch of simulations then zoom into
that one". That message is the approval for this direction; no further sketch round was held.

How it was read, and built in `narrated/`:

- **A bunch of simulations.** The film opens on all 36 episodes of the pilot playing at once (six markets, three
  rules, the free arm and the one-firm control arm), then the camera goes into one tile: market 36, per-firm rule.
- **The point of view.** Inside that run the film shows the round-1 message the agent was sent and the line of JSON
  it returned, both copied from the saved call record, before showing the market react. "the no market simulation"
  was taken to mean the market simulation as the agent sees it; the no-rule run appears as one of the two neighbours.
- **Narrating.** A spoken narration with the same words as subtitles. The voice is synthetic (Kokoro, `af_heart`);
  the timeline is derived from the clip lengths, so a recorded human voice can replace it clip by clip.
- This overrides two playbook defaults on his instruction: films have no audio, and films run 40 to 120 seconds.
  The narrated film runs 3 min 29 s.
- v1's visual claim still holds for the middle section. The new claim: out of a wall of 36 runs, the six that split
  are exactly the six where firms are scored alone and the agent is free to register.
- Newly included: the one-firm control arm (on the wall, and its mean profit). Still left out: the scripted study,
  the Haiku cohorts, cost accounting, the same-action counterfactual.
