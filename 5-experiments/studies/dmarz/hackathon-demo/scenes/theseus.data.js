// Swarm of Theseus pilot, attempt S1-a1 (vishesh). Reduced from
//   5-experiments/studies/vishesh/swarm-of-theseus/results/S1-a1/rows.json   (36 runs, per-step collective vs expected)
//   5-experiments/studies/vishesh/swarm-of-theseus/results/S1-a1/summary.json (by_scenario means, cost.calls = 864)
// mean[arm][step] = % of 4 cases the crew's majority answer got right, averaged over 2 worlds per scenario, then
// equally over the 3 scenarios. The mean of steps 4 and 5 reproduces the RESULTS.md table (52.08 / 100 / 91.67 / 100 / 89.58 / 100).
// runs[arm] = one row per world (seed-bank 200, 201, observatory 200, 201, repair-dock 200, 201): cases right out of 4 at steps 0..5.
FILM.data['theseus'] = {
  steps: [0, 1, 2, 3, 4, 5],
  founders: [3, 2, 1, 0, 0, 0],          // founders still in the crew at each step (rows.json history[].members)
  mean: {
    neither:  [91.67, 87.5, 95.83, 50.0, 41.67, 62.5],
    notes:    [91.67, 87.5, 100.0, 91.67, 100.0, 100.0],
    mentor:   [91.67, 91.67, 95.83, 87.5, 91.67, 91.67],
    both:     [91.67, 87.5, 100.0, 91.67, 100.0, 100.0],
    founders: [91.67, 87.5, 100.0, 91.67, 91.67, 87.5],
    verbatim: [91.67, 91.67, 100.0, 91.67, 100.0, 100.0],
  },
  after: { neither: 52.08, notes: 100, mentor: 91.67, both: 100, founders: 89.58, verbatim: 100 },   // mean of steps 4 and 5
  runs: {
    neither: [[4, 4, 4, 1, 1, 1], [4, 4, 3, 3, 3, 3], [4, 3, 4, 0, 0, 0], [2, 2, 4, 4, 4, 4], [4, 4, 4, 1, 0, 3], [4, 4, 4, 3, 2, 4]],
    notes:   [[4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4], [4, 3, 4, 3, 4, 4], [2, 2, 4, 3, 4, 4], [4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4]],
  },
};
