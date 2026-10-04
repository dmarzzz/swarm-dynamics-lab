import json,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from cases import development_examples,make_case
from policies import ExactReference
from study import execute,private_packets,collect_private,natural_challenge_case,audit_attempt

class StudyTests(unittest.TestCase):
    def test_private_views_do_not_see_peers(self):
        for p in private_packets(make_case()):
            self.assertEqual(len(p['records']),1);self.assertEqual(p['votes'],[]);self.assertIsNone(p['challenge'])
    def test_natural_votes_and_unanimous_cases_kept(self):
        c=make_case();v=collect_private(c,ExactReference());n=natural_challenge_case(c,v)
        self.assertEqual(v.count('PROCEED'),4);self.assertIsNotNone(n['challenge'])
        self.assertIsNone(natural_challenge_case(c,['PROCEED']*5)['challenge'])
    def test_reconcile_and_never_overwrite(self):
        with tempfile.TemporaryDirectory() as p:
            target=Path(p)/'attempt';s=execute(development_examples(),['majority','evidence-gate'],ExactReference(),target)
            self.assertEqual(s['assigned'],10);self.assertEqual(s['terminal'],10)
            with self.assertRaises(FileExistsError):execute(development_examples(),['majority'],ExactReference(),target)
    def test_provider_failures_still_terminal(self):
        def fail(*args):raise ValueError('not printed')
        with tempfile.TemporaryDirectory() as p:
            s=execute([make_case()],['evidence-gate'],fail,Path(p)/'a')
            self.assertEqual(s['terminal'],1);self.assertEqual(s['outcomes']['failures'],1)
    def test_interruption_retains_all_assignments(self):
        def interrupted(*args):raise KeyboardInterrupt()
        with tempfile.TemporaryDirectory() as p:
            out=Path(p)/'a'
            with self.assertRaises(KeyboardInterrupt):execute([make_case()],['evidence-gate'],interrupted,out)
            audit=audit_attempt(out)
            self.assertEqual(audit['assigned'],1);self.assertEqual(audit['missing'],1)
            self.assertEqual(audit['correct_on_time_all_assigned'],0)
    def test_random_arm_requires_frozen_schedule(self):
        with tempfile.TemporaryDirectory() as p:
            with self.assertRaises(ValueError):execute([make_case()],['matched-random'],ExactReference(),Path(p)/'a')
            c=make_case();s=execute([c],['matched-random'],ExactReference(),Path(p)/'b',random_schedule={c['case_id']:False})
            self.assertEqual(s['outcomes']['checks'],0)
    def test_duplicate_assignments_rejected(self):
        with tempfile.TemporaryDirectory() as p:
            with self.assertRaises(ValueError):execute([make_case(),make_case()],['majority'],ExactReference(),Path(p)/'a')

if __name__=='__main__':unittest.main()
