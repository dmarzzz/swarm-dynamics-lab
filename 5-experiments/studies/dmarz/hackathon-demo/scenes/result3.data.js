// Reduced data for the spare third result. One block per pick; scenes/result3.js draws COPY.pick.
// Every value is literal from swarm-lab origin/main (read with `git show origin/main:<path>`, 2026-10-04).
FILM.data['result3'] = {
  // 5-experiments/studies/vishesh/optimal-swarm-size/results/q-a6/analysis.json, pairs[2] (root 5, structure "parallel")
  // same row in 5-experiments/studies/vishesh/optimal-swarm-size/reviews/q-a6-post.md:
  //   "| 5 | parallel | .6875 → .3125 | 25.17 → 17.02 | ..."
  'swarm-size': {
    items: 16,                                   // item_00 .. item_15
    n1: { seconds: 25.166248474000895,           // pairs[2].n1.elapsed_s
      wrong: [1, 9, 10, 11, 15] },               // pairs[2].n1.wrong_value_items (quality .6875 = 11 of 16)
    n2: { seconds: 17.016874791006558,           // pairs[2].n2.elapsed_s
      wrong: [0, 1, 3, 4, 6, 7, 8, 9, 10, 11, 15] }, // pairs[2].n2.wrong_value_items (quality .3125 = 5 of 16)
  },
  // 5-experiments/studies/vishesh/external-influence-v2/reviews/quality-post.md, "Verified mechanism":
  //   "five of six analysts favored FinchSupport before and after peer revision ... The chair still chose FinchSupport"
  //   "Nine agents comprise six analysts, two check interpreters and one chair." (README.md, same folder)
  'influence': {
    analysts: 6,
    swayed: 5,
    checkers: 2,
  },
  // 5-experiments/studies/vishesh/immune-response-v3/scenario-study/ASSESSMENT.md, "Single commander" table
  //   | Stale advice        | 0/6 | 5/6 | 0 |
  //   | Healthy false alarm | 6/6 | 3/6 | 1 |
  'immune-response': {
    ticks: 6,
    teamBroken: 0,
    soloBroken: 5,
    teamHealthy: 6,
    soloHealthy: 3,
  },
};
