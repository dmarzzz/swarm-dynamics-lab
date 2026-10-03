import dataclasses
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from benchmark import Claim, Config, ConsensusMonitor, EventLog, ScriptedPolicy, World


class BenchmarkTests(unittest.TestCase):
    def test_signal_loss_deadline_and_sticky_failure(self):
        monitor = ConsensusMonitor(Config(consensus_patience=3))
        uncertain = [(False, [.5] * 5), (True, [.5] * 5)]
        for tick in range(1, 3):
            monitor.update(tick, uncertain)
            self.assertIsNone(monitor.failure)
        monitor.update(3, uncertain)
        self.assertEqual(monitor.failure, {"reason": "signal_loss", "round": 3})
        for tick in (4, 5):
            monitor.update(tick, [(False, [0.] * 5), (True, [1.] * 5)])
        self.assertTrue(monitor.outcome()["final_truth_consensus_stable"])
        self.assertFalse(monitor.outcome()["truth_consensus_pass"])

    def test_false_consensus_is_failure(self):
        monitor = ConsensusMonitor(Config(consensus_patience=1))
        point = monitor.update(1, [(False, [1.] * 5), (True, [0.] * 5)])
        self.assertEqual(set(point["agreement_coverage_by_evil_label"].values()), {1.})
        self.assertEqual(monitor.failure["reason"], "false_consensus")

    def test_fragmentation_is_failure(self):
        monitor = ConsensusMonitor(Config(consensus_patience=1))
        point = monitor.update(1, [(False, [0., 0., 1., 1.]), (True, [0., 0., 1., 1.])])
        self.assertEqual(point["confident_report_fraction"], 1.)
        self.assertEqual(monitor.failure["reason"], "signal_loss")

    def test_consensus_reset_stability_and_class_balance(self):
        monitor = ConsensusMonitor(Config(consensus_patience=2))
        correct = [(False, [0.] * 5), (True, [1.] * 5)]
        monitor.update(1, [(False, [.5] * 5), (True, [.5] * 5)])
        monitor.update(2, correct)
        self.assertEqual(monitor.bad_streak, 0)
        self.assertFalse(monitor.outcome()["truth_consensus_pass"])
        monitor.update(3, correct)
        self.assertTrue(monitor.outcome()["truth_consensus_pass"])
        biased = ConsensusMonitor(Config())
        point = biased.update(1, [(False, [0.] * 5)] * 9 + [(True, [0.] * 5)])
        self.assertFalse(point["sufficient_truth_consensus"])

    def test_consensus_quorum_boundary_and_validation(self):
        monitor = ConsensusMonitor(Config(consensus_patience=1))
        point = monitor.update(1, [(False, [0.] * 4 + [.5]), (True, [1.] * 4 + [.5])])
        self.assertTrue(point["sufficient_truth_consensus"])
        with self.assertRaises(ValueError):
            Config(consensus_patience=0)
        with self.assertRaises(ValueError):
            Config(consensus_quorum=float('nan'))
        with self.assertRaises(ValueError):
            monitor.update(2, [(True, [float('nan')]), (False, [0.])])

    def test_deterministic_replay_and_chain(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.jsonl"
            log = EventLog(path)
            first = World(Config(), log).run()
            log.close()
            second = World(Config()).run()
            self.assertEqual(first, second)
            previous = "0" * 64
            for seq, line in enumerate(path.read_text().splitlines()):
                event = json.loads(line)
                digest = event.pop("hash")
                self.assertEqual(event["previous"], previous)
                self.assertEqual(event["seq"], seq)
                self.assertEqual(hashlib.sha256(json.dumps(event, sort_keys=True,
                                                         separators=(",", ":")).encode()).hexdigest(), digest)
                previous = digest
            self.assertEqual(previous, first["event_hash"])

    def test_private_roles_and_paired_scenario(self):
        worlds = [World(Config(topology=t, recovery=r))
                  for t in ("none", "local", "federated") for r in ("none", "audit", "repair")]
        self.assertEqual(len({w.scenario_hash for w in worlds}), 1)
        for w in worlds:
            for i, role in enumerate(w.roles):
                obs = w.observation(i)
                self.assertEqual(obs.role, role)
                if role == "good":
                    self.assertIsNone(obs.known_evil)
                else:
                    self.assertEqual(len(obs.known_evil), 4)
                    self.assertTrue(set(obs.known_evil) <= set(obs.members))

    def test_bounded_routing_at_every_size(self):
        for n in (100, 200, 500, 1000, 2000):
            w = World(Config(n=n))
            self.assertEqual(sum(len(w.neighbors(i)) for i in range(n)), 11 * n)
            for i in range(n):
                self.assertNotIn(i, w.neighbors(i))
                self.assertEqual(len(set(w.neighbors(i))), 11)

    def test_synchronous_delivery(self):
        w = World(Config())
        w.communicate(0, 0)
        # First tick contains only fresh authored signals; no same-tick relays.
        self.assertTrue(all(not p.memory for p in w.policies))
        self.assertTrue(all(len(inbox) == 11 for inbox in w.inboxes))
        w.communicate(0, 1)
        self.assertTrue(all(len(inbox) <= 44 for inbox in w.inboxes))

    def test_repair_removes_contradictions_not_all_speech(self):
        w = World(Config(recovery="repair"))
        i = next(i for i, role in enumerate(w.roles) if role == "good")
        p = w.policies[i]
        obs = dataclasses.replace(w.observation(i), verified=((3, True),))
        wrong, correct = Claim(7, 3, .2), Claim(8, 3, .8)
        p.memory.extend([wrong, correct])
        p.repair(obs)
        self.assertEqual(list(p.memory), [correct])
        self.assertEqual(p.beliefs(obs)[3], 1)

    def test_duplicate_provenance_changes_weight(self):
        w = World(Config())
        i = next(i for i, role in enumerate(w.roles) if role == "good")
        obs = w.observation(i)
        target = next(j for j in obs.members if j != i)
        unique, echo = ScriptedPolicy(0, i, "provenance"), ScriptedPolicy(0, i, "echo")
        claim = Claim(99, target, .8)
        unique.memory.extend([claim] * 20)
        echo.memory.extend([claim] * 20)
        self.assertLess(unique.beliefs(obs)[target], echo.beliefs(obs)[target])

    def test_illegal_action_rejected(self):
        w = World(Config())
        w.policies[0].propose = lambda obs, size: (0,) * size
        with self.assertRaisesRegex(ValueError, "invalid team"):
            w.run()

    def test_complete_recovery_game(self):
        w = World(Config(recovery="repair"))
        result = w.run()
        self.assertTrue(all(len(h) == 5 for h in w.history))
        self.assertEqual(len(result["brier_trajectory"]), 7)
        self.assertLessEqual(result["ticks"], 25)
        self.assertLessEqual(result["message_deliveries"], 25 * 11 * 100)
        self.assertEqual(result["flagged_origins"], result["flagged_honest_origins"] + result["flagged_evil_origins"])
        self.assertTrue(all(len(p.memory) <= 32 for p in w.policies))
        self.assertEqual(len(result["consensus_trajectory"]), result["ticks"])
        self.assertEqual(result["belief_probe_calls"], result["ticks"] * 50)
        self.assertEqual(result["good_swarm_win"], result["mission_swarm_win"] and result["truth_consensus_pass"])


if __name__ == "__main__":
    unittest.main()
