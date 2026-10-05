// Data for scene "more": ten further experiments, one card each. Every number was copied by hand from the `source`
// file on 2026-10-04 (line references in the comments). Scores are the 0 to 4 evidence scores in
// 5-experiments/evidence-metadata.json. Paths are relative to the repo root.
FILM.data.more = {
  cards: [
    {
      // RESULTS.md line 3: "registered a second firm in 6/6 firm-regulated markets, 0/6 owner-regulated and 0/6 unregulated";
      // line 5: "18 bundles / 36 episodes / 864 calls", "six related market tasks".
      id: 'market-split-opus', owner: 'dmarz',
      claim: 'Opus split its firm to dodge a per-firm rule',
      numbers: 'second firm in 6 of 6 firm-regulated markets, 0 of 6 owner-regulated',
      model: 'Opus 5.5', sample: '6 market tasks, 36 of 36 episodes valid', score: 2,
      source: '5-experiments/studies/dmarz/market-split-opus/RESULTS.md',
    },
    {
      // RESULTS.md line 20: specialist accuracy 4.2% (1 carrier) ... 100.0% (81 carriers); line 23: -95.8 points, 24 of 24 roots;
      // line 9: 24 world roots x 60 conditions = 1,440 valid outcomes.
      id: 'sybil-scarcity-opus', owner: 'dmarz',
      claim: 'A rare fact is lost with only one truthful carrier',
      numbers: '100.0% accuracy with 81 carriers, 4.2% with one',
      model: 'Opus 5.5', sample: '24 world roots, 1,440 of 1,440 outcomes valid', score: 2,
      source: '5-experiments/studies/dmarz/sybil-scarcity-opus/RESULTS.md',
    },
    {
      // RESULTS.md table, line 14: propagated credit, attacker seats of 162: 4.38 at 32 checks, 15.92 at 108 checks.
      // "Read this first" 1: the primary is computed by the scripted admission rule, not by a model. Score: README.md table (1/4).
      id: 'trust-credit-qwen', owner: 'dmarz',
      claim: 'More checks let in more attackers when credit spreads',
      numbers: 'attacker seats of 162: 4.38 at 32 checks, 15.92 at 108',
      model: 'scripted rule, no model', sample: '24 comparison roots, 504 of 504 rows', score: 1,
      source: '5-experiments/studies/dmarz/trust-credit-qwen/RESULTS.md',
    },
    {
      // records/q0-005/README.md line 32: "C completed 12/12 safely; S completed 9/12." README.md lines 95-96: C = one controller
      // with all roles, S = four roles. Failed qualification: 21 of 24 safe (87.5%) against a 90% threshold. Descriptive paired
      // totals on reused structures.
      id: 'compositional-safety-q0-005', owner: 'dmarz',
      claim: 'Four roles were less safe than one controller',
      numbers: '12 of 12 episodes safe with one controller, 9 of 12 with four roles',
      model: 'Haiku 4.5', sample: '24 of 24 episodes on 3 task roots; failed its qualification gate', score: 1,
      source: '5-experiments/studies/dmarz/compositional-safety/records/q0-005/README.md',
    },
    {
      // d1-opus/README.md evidence block: "6/6 on the reused worlds versus Haiku 2/6 and Sonnet 3/6 on byte-identical requests";
      // 72/72 calls valid; 12 fresh worlds 12/12.
      id: 'discussion-v3-d1-opus', owner: 'dmarz',
      claim: 'Opus kept the constraints Haiku and Sonnet broke',
      numbers: '6 of 6 decisions right, Haiku 2 of 6, Sonnet 3 of 6',
      model: 'Opus 5.5', sample: '6 reused worlds plus 12 fresh worlds, 72 of 72 calls valid', score: 2,
      source: '5-experiments/studies/dmarz/discussion-dose/d1-opus/README.md',
    },
    {
      // README.md line 66: "Confidence alone achieved 56.78% recall, versus 56.30% for Laya and 55.72% for Jev committees;
      // neither adaptive committee saved checks." Line 9: 70 paired evaluation receipts. NULL.
      id: 'antsy-v4', owner: 'vishesh',
      claim: 'Null: OCR committee no better than confidence alone',
      numbers: 'recall 56.78% confidence alone, 56.30% and 55.72% committee',
      model: 'Laya and Jev', sample: '70 paired evaluation receipts', score: 2,
      source: '5-experiments/studies/vishesh/antsy-verification-v4/README.md',
    },
    {
      // README.md line 20: evidence gate 24/60 versus 30/60 for always-check, with 31 versus 40 checks.
      // REPORT.md table lines 12-14 (Correct / 60, Checks). Line 9 of README: 52 fixed roots, 420/420 decisions. NEGATIVE.
      id: 'right-dissenter', owner: 'vishesh',
      claim: 'Gated dissent saved checks and lost correct decisions',
      numbers: '24 of 60 right with 31 checks, 30 of 60 with 40 checks',
      model: 'Jev', sample: '52 fixed roots, 420 of 420 decisions, 7 policies', score: 1,
      source: '5-experiments/studies/vishesh/dissent/README.md',
    },
    {
      // scenario-study/ASSESSMENT.md, "Single commander" table: stale advice, team retain 0/6 healthy ticks, solo 5/6.
      // Same table: on the healthy false alarm the team kept 6/6 and the solo agent 3/6 with 1 unsafe attempt. FAILURE (team).
      // Team = three reviewers plus one commander. Model: scenario-study/model-config.json.
      id: 'immune-scenario', owner: 'vishesh',
      claim: 'Solo fixed it, but broke a healthy service',
      numbers: 'healthy ticks. broken: team 0, solo 5 of 6. control: team 6, solo 3 of 6',
      model: 'Haiku 4.5', sample: '4 related scenarios, one sample each; solo damaged the healthy control (3 of 6 ticks)', score: 1,
      source: '5-experiments/studies/vishesh/immune-response-v3/scenario-study/ASSESSMENT.md',
    },
    {
      // wild-identity/README.md line 9: "SwarmTraces 189,579/189,579 rows with no structured actor/time values. No interventions or
      // model calls." Also shadow/submission/RESULTS.md line 110.
      id: 'wild-identity', owner: 'shadow',
      claim: 'A public incident dataset has no actor and no clock',
      numbers: 'SwarmTraces: 0 of 189,579 records name an actor or a time',
      model: 'no model calls', sample: '189,579 of 189,579 rows read', score: 1,
      source: '5-experiments/studies/shadow/wild-identity/README.md',
    },
    {
      // reading-rule/README.md line 8: mean absolute effect 0.000183 (interval 0.000002 to 0.000532) against the prespecified
      // 0.10 threshold; 24 paired synthetic histories, 144/144 calls valid. NULL.
      id: 'capture-memory-reading-rule', owner: 'shadow',
      claim: 'No effect from reversing the order of a history',
      numbers: 'answer probability moved 0.000183, threshold 0.10',
      model: 'gpt-4o-mini', sample: '24 paired synthetic histories, 144 of 144 calls valid', score: 2,
      source: '5-experiments/studies/shadow/capture-memory-mix/reading-rule/README.md',
    },
  ],
};
