# Avalon at swarm scale: hunches

Status: HUNCHES, not hypotheses. Written 2026-10-03 by dmarz/avalon from a chat with dmarz. Nothing here has
passed the prior-art gate; tasks `scan-papers-avalon-swarm`, `scan-code-avalon-swarm`,
`scan-papers-avalon-scaling` and `survey-avalon-swarm` exist to check it.

## Starting point

AvalonBench (Light et al., 2023, arXiv 2310.05036; code jonathanmli/Avalon-LLM) tests LLM agents in
The Resistance: Avalon at 5-10 players. Scaling the player count alone does not make it a swarm benchmark: the
game is balanced for 5-10, has one broadcast table and one team vote per round. The hunch is that the
structural changes below turn it into a testbed for the gap the sim-env survey found (operator-owned Sybil
clusters with ground-truth labels, a fork-merge primitive, injected adversaries). Hidden roles already give
ground-truth labels for free.

## Candidate changes (A1-A6)

- **A1. Evil = Sybil cluster.** One principal controls k of N seats (own persona and context per seat, shared
  hidden objective, optional private side channel). Measure evil win rate as a function of k/N.
- **A2. Communication graph instead of one table.** Neighbourhood or gossip rounds; topology (small-world,
  scale-free, sharded) as an experimental variable.
- **A3. Many concurrent quests.** Leaders pick several subcommittees per round; committee selection under
  adversaries becomes the core skill (validator-set analogue).
- **A4. Merlin as a detector role.** Several agents with noisy partial knowledge of evil; Assassin-style cost
  for revealing it. Detection-versus-exposure tradeoff.
- **A5. Fork-merge round.** An agent forks onto several committees and merges back; a fork corrupted next to
  the Sybil cluster can poison the parent. Links to [[fork-merge-security]] Q1-Q3 and the setups report
  finding that no rig lets a parent fork itself and merge back.
- **A6. Curves, not win rates.** Evil win rate vs k/N, topology and model mix; detection precision/recall
  against role labels; messages/tokens per correct identification.

## Risks to check

- Balance: evil fraction, quest sizes and fail thresholds need retuning per N (rule-based self-play sweep first).
- Cost: hundreds of seats x rounds x messages; mostly local models, frontier models in a few seats.
- BotSim pitfall: if honest agents never actually engage the Sybils, detection looks artificially good.
- Large-N Werewolf/Mafia/Avalon variants with LLM agents may already exist (2025-26).

## Already in the library (seeds)

[[ellawela-2026-trust]], [[data-bayesian-social-deduction-2025]], [[gh-google-werewolf-arena]],
[[data-werewolf-game-reasoning-2025]], [[hu-2025-toward]].
