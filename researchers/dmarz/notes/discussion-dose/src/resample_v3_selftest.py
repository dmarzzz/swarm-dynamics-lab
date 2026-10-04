"""Offline checks for the v3 resampling-only sidecar. No credentials, network or model calls."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
import resample_v3 as rs
from bench_v3 import runner as v3_runner
from bench_v3.journal import Journal
from bench_v3.policies import Scripted
from bench_v3.worlds import SPLITS


def snapshot_for(case, attack, runner):
    return runner.prepare_reports(case, attack, runner.acquire(case, attack))


class SidecarTests(unittest.TestCase):
    def test_worlds_fresh_and_balanced(self):
        ids = [i for v in rs.WORLDS.values() for i in v]
        reserved = set(range(10101, 10161)) | {i for v in SPLITS.values() for i in v}
        self.assertFalse(set(ids) & reserved); self.assertEqual(len(ids), len(set(ids)))
        cases = rs.cases()
        for stratum in rs.WORLDS:
            fams = [c['family'] for c in cases if c['stratum'] == stratum]
            self.assertEqual(sorted(set(fams.count(f) for f in fams)), [2])

    def test_patched_runner_matches_upstream_for_existing_arms(self):
        case = rs.cases()[0]
        for attack in (False, True):
            for arm in ('reports', 'private', 'board', 'independent'):
                up = v3_runner.Runner(Scripted(), Journal(), 3); side = rs.ResampleRunner(Scripted(), Journal(), 3)
                a = up.continue_arm(case, attack, arm, snapshot_for(case, attack, up))
                b = side.continue_arm(case, attack, arm, snapshot_for(case, attack, side))
                self.assertEqual(a, b)
                strip = lambda evs: [{k: v for k, v in e.items() if k not in ('hash', 'previous', 'seq', 'latency_seconds')} for e in evs]
                self.assertEqual(strip(up.journal.events), strip(side.journal.events))

    def test_resample_arm_probes_only(self):
        case = rs.cases()[1]
        for rounds in (1, 3, 6):
            r = rs.ResampleRunner(Scripted(), Journal(), rounds); snap = snapshot_for(case, True, r)
            start = len(r.journal.events)
            row = r.continue_arm(case, True, 'resample', snap)
            calls = [e for e in r.journal.events[start:] if e['kind'] == 'call_start']
            self.assertEqual([c['request']['phase'] for c in calls].count('work'), 0)
            self.assertEqual([c['request']['phase'] for c in calls].count('ballot'), 3 * rounds)
            self.assertEqual(row['physical_continuation_calls'], 3 * rounds + 1)
            self.assertEqual([t['turn'] for t in row['trajectory']], list(range(rounds + 1)))
            # The probed state never changes: every probe for one agent sees an identical context.
            for agent in range(3):
                contexts = {json.dumps(c['request']['context'], sort_keys=True) for c in calls
                            if c['request']['phase'] == 'ballot' and c['agent'] == agent}
                self.assertEqual(len(contexts), 1)
                self.assertEqual(json.loads(contexts.pop())['private_history'], snap['states'][agent]['private_history'])

    def test_private_and_resample_share_checkpoint_and_probe_schedule(self):
        case = rs.cases()[7]
        r = rs.ResampleRunner(Scripted(), Journal(), 3); snap = snapshot_for(case, True, r)
        p = r.continue_arm(case, True, 'private', snap); s = r.continue_arm(case, True, 'resample', snap)
        q = r.continue_arm(case, True, 'reports', snap)
        self.assertEqual(p['snapshot_hash'], s['snapshot_hash']); self.assertEqual(p['snapshot_hash'], q['snapshot_hash'])
        self.assertEqual(p['trajectory'][0]['ballots'], s['trajectory'][0]['ballots'])
        self.assertEqual([t['turn'] for t in p['trajectory']], [t['turn'] for t in s['trajectory']])
        self.assertEqual(p['physical_continuation_calls'] - s['physical_continuation_calls'], 3 * 3)

    def test_anchor_drift_fails_loudly(self):
        original = rs.ANCHOR
        try:
            rs.ANCHOR = '            if arm in ("nonexistent",):\n'
            with self.assertRaises(ImportError): rs._patched_continue_arm()
        finally:
            rs.ANCHOR = original

    def test_scripted_run_accounting_and_audit(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / 'run'
            s = rs.run(out)
            rec = s['reconciliation']
            self.assertEqual(rec['started_calls'], rec['planned_calls']); self.assertEqual(rec['planned_calls'], 936)
            self.assertFalse(rec['missing'] or rec['unresolved_calls'] or rec['validation_failures'])
            self.assertEqual(rec['assigned'], 72); self.assertTrue(s['qualification']['competence_screen_pass'])
            self.assertEqual(set(s['mechanism']), {f'{m}:{st}' for m in ('vote_target', 'memory_false_target', 'parent_groundtruth_wrong', 'final_false_endorsements') for st in rs.WORLDS})
            self.assertTrue(rs.audit(out)['ok'])
            # A tampered saved score must fail the audit.
            episodes = json.loads((out / 'episodes.json').read_text())
            episodes[0]['evaluation']['vote_target'] = 1 - episodes[0]['evaluation']['vote_target']
            (out / 'episodes.json').write_text(json.dumps(episodes, sort_keys=True, indent=2) + '\n')
            with self.assertRaises(ValueError): rs.audit(out)

    def test_known_behaviour_policies_complete(self):
        for policy in ('abstain', 'copy_count', 'wrong_entity'):
            with tempfile.TemporaryDirectory() as d:
                s = rs.run(Path(d) / 'run', provider=Scripted(policy))
                self.assertEqual(s['reconciliation']['started_calls'], 936)

    def test_contrast_bounds_with_missing_cell(self):
        rows = [{'id': f'{w}:{a}:{arm}', 'evaluation': {'vote_target': 1 if (a and arm == 'private') else 0}}
                for w in rs.WORLDS['resolvable'] for a in (0, 1) for arm in rs.ARMS]
        c = rs._contrast(rows, 'vote_target', 'resolvable', 'private', 'resample'); self.assertEqual(c['mean'], 1)
        rows = [r for r in rows if r['id'] != f'{rs.WORLDS["resolvable"][0]}:1:private']
        c = rs._contrast(rows, 'vote_target', 'resolvable', 'private', 'resample')
        self.assertIsNone(c['mean']); self.assertLess(c['missing_outcome_lower'], c['missing_outcome_upper'])

    def test_hub_wrapper_offline(self):
        import gzip, resample_v3_hub as hub
        class FakeRun:
            id = 'discussion-v3-resample/test'
            def __init__(self): self.progressed = []; self.uploaded = []
            def progress(self, *a, **k): self.progressed.append(a)
            def artifact(self, path, name=None): self.uploaded.append(Path(path))
        with tempfile.TemporaryDirectory() as d:
            fake = FakeRun(); counted = hub.Counting(Scripted(), fake, 936)
            out = Path(d) / 'run'; rs.run(out, 3, counted)
            self.assertEqual(counted.n, 936); self.assertEqual(fake.progressed[-1][:2], (936, 936))
            hub.publish_artifacts(fake, out)
            index = json.loads((out / 'upload' / 'artifact-index.json').read_text())
            self.assertEqual({f['original'] for f in index['files']}, set(hub.OUTPUTS))
            for f in index['files']:
                payload = b''.join((out / 'upload' / part).read_bytes() for part in f['parts'])
                self.assertEqual(gzip.decompress(payload), (out / f['original']).read_bytes())

    def test_paid_launch_gate(self):
        with self.assertRaises(ValueError): rs.approved_model_config(None, 3)
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'launch.json'
            p.write_text(json.dumps({'status': 'draft'}))
            with self.assertRaises(ValueError): rs.approved_model_config(p, 3)
            review = Path(d) / 'review.md'; review.write_text('verdict: pass\n')
            import hashlib
            proof = {'path': 'review.md', 'sha256': hashlib.sha256(review.read_bytes()).hexdigest()}
            config = {'model': 'm', 'max_calls': 936, 'max_output_tokens': 1, 'max_input_bytes': 1, 'timeout': 1,
                      'max_cost_usd': 1, 'input_usd_per_million': 1, 'output_usd_per_million': 5}
            good = {'status': 'approved', 'source_hashes': rs.source_hashes(), 'rounds': 3,
                    'v2_results_review': proof, 'independent_review': proof, 'model_config': config}
            p.write_text(json.dumps(good)); self.assertEqual(rs.approved_model_config(p, 3), config)
            waived = {k: v for k, v in good.items() if k != 'independent_review'}; waived['review_waiver'] = proof
            p.write_text(json.dumps(waived)); self.assertEqual(rs.approved_model_config(p, 3), config)
            p.write_text(json.dumps({**waived, 'independent_review': proof}))
            with self.assertRaises(ValueError): rs.approved_model_config(p, 3)
            for bad in ({**good, 'rounds': 6}, {**good, 'model_config': {**config, 'max_calls': 900}},
                        {**good, 'independent_review': {**proof, 'sha256': '0' * 64}}):
                p.write_text(json.dumps(bad))
                with self.assertRaises(ValueError): rs.approved_model_config(p, 3)


if __name__ == '__main__':
    unittest.main()
