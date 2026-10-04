# Swarm factory: an idea brief

Status: unreviewed idea, written 2026-10-03 by dmarz/swarm-factory at dmarz's request. Nothing here is a
hypothesis under the prior-art gate, and nothing has been built or run. The candidate questions live in the
question atlas as MKT-01 to MKT-12 (`researchers/dmarz/notes/question-atlas/markets.json`).

## The idea

Several LLM-agent firms share a small Factorio-like world. They claim resource patches, build miners,
smelters and assemblers, and turn ore into intermediate and finished goods. Each round they sell into shared
markets, one per finished good, where price falls as total supply rises (linear inverse demand, so Cournot
competition). We watch whether the firms carve the markets up between them, whether a principal that runs
several firms behaves differently from one that runs a single firm, and whether an auditor can tell the two
apart from what the firms build and sell.

The anchor is [[lin-2024-strategic]]: two identical LLM firms in a repeated two-commodity Cournot game often
end up each monopolising one commodity, with no channel to talk and no instruction to collude.
[[bracale-syrnikov-2026-institutional]] replicates that result and shows that an oracle reading quantities,
plus fines, cuts severe collusion from 50% of runs to 5.6%, while a prompt-only rule changes nothing.

## What a factory adds over a bare Cournot game

In the bare game a firm's move is a number. In a factory world the move is a build, and builds are slow,
costly and visible:

- Capacity is sunk. Leaving a market means scrapping or idling machines, so exit and re-entry have a price.
  Lin et al. report that firms which exit never re-enter; in a factory that becomes a measurable cost.
- Division shows up in the build graph (who owns which patches and which assembly lines) before it shows up
  in prices, which gives an auditor a second signal.
- Resource patches are finite and contestable, so firms compete for territory as well as customers.
- Production chains couple the markets: circuits need iron plates and wire, so a firm that owns the copper
  patches shapes two markets at once.

## The four research lines in one environment

| Line | Knob in the world | Ground-truth label |
|---|---|---|
| LLM dynamics | number of firms and goods, chat (none, public, private), model mix | none needed |
| Sybil | one principal controls k of N firms, with or without a private back-channel | firm → principal map |
| Fork-merge | fork a firm mid-game (copy memory, split assets); merge two firms | lineage of every firm |
| Detection | an auditor sees market data, build logs, chat; never the labels | auditor's guesses scored against labels |

The Sybil row is the gap the scan found. No catalogued work has one principal running several firms in a
Cournot market. The closest is the team rounds in Vending-Bench Arena ([[li-2026-emergent]]), which the
authors left out of their analysis, and the environment is not public. Standard Cournot theory gives a
reason to expect the effect: with linear demand a merger of two firms often lowers their joint profit,
because the merged firm cuts output and rivals expand. Read the other way, splitting one firm into several
identities can raise the owner's total output share and profit.

## Metrics

- Market concentration per good (HHI on quantities sold) and a firm-level specialisation index.
- Profit as a fraction of the gap between the Cournot-Nash and monopoly benchmarks (Δ, as in
  [[calvano-2020-artificial]]), computed on variable profit so build spending does not swamp it.
- Consumer surplus against the Cournot-Nash level.
- Exit and re-entry events, and the capacity scrapped or idled at each.
- For detection: AUC of an auditor naming same-principal pairs, and how often it confuses Sybil firms with
  independent firms that colluded tacitly.

## Two ways to build it, not yet chosen

1. **A small Python simulation of our own.** Tick-free rounds, a five-recipe chain (iron and copper plates,
   gears, wire, circuits), a grid of resource patches, closed-form Cournot benchmarks. Cheap enough for
   hundreds of runs with a local model. Easy to add the labels, forks and merges.
2. **A market layer on the Factorio Learning Environment** ([[hopkins-2025-factorio]],
   [[gh-jackhopkins-factorio-learning-environment]]). FLE has had a multi-agent mode since v0.2: agents take
   turns, can message each other, and ship with cooperate, impostor and distrust tasks. It has no markets,
   prices or per-firm profit, so we would add those. Much richer world, far fewer runs, and it needs a
   headless Factorio server.

A reasonable order is option 1 first to find where the effects are, then option 2 to check that the effects
survive a real game (MKT-12).

## Open decisions

- Which model runs the firms: Claude for fidelity to the literature, or a local model on orbital-one for run
  count.
- Whether the first study is the Sybil question (MKT-03) or a replication of Lin et al. inside the factory
  (MKT-01). The replication is the safer start; MKT-03 is the result nobody has.
- Whether the survey that gates these questions is `llm-agent-swarms` (waiting on cross-review) or a new
  `agent-markets` survey.

## Prior work to read first

[[lin-2024-strategic]], [[bracale-syrnikov-2026-institutional]], [[li-2026-emergent]],
[[deshpande-2026-strategic]], [[keppo-2026-fragility]], [[arslan-2026-persistent]],
[[fish-2024-algorithmic]], [[calvano-2020-artificial]], [[eschenbaum-2026-auditing]],
[[nakamura-2026-colosseum]], [[lee-2026-faithful]], [[hopkins-2025-factorio]], [[zheng-2020-ai]].
