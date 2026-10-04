import unittest
import engine as e


class Tests(unittest.TestCase):
    def test_balanced_truth_and_guard(self):
        self.assertEqual({e.symbolic(e.fixture(t)['truth']) for t in range(8000,8004)},set((*e.OPTIONS,'NONE')))
        calls=[]
        r=e.episode(8000,9,1,'clean','fast',lambda rows,c: calls.append(c) or e.symbolic(rows))
        self.assertEqual([c['agent'] for c in calls],['central'])
        self.assertTrue(all(x['evaluation']['abstention'] for a,x in r['outcomes'].items() if a in e.ARMS[:5]))

    def test_support_not_availability(self):
        f=e.fixture(8000);ds=e.documents(f,'early-wrong','fast')
        target=e.symbolic(f['truth']);roots=e.supporting_roots(ds,target)
        self.assertEqual(roots,['root-2','root-3'])
        self.assertEqual(e.supporting_roots(ds*10,target),roots)

    def test_clean_all_arms_and_agent_counts(self):
        for t in range(8000,8012):
            for n in (5,9):
                r=e.episode(t,n,6,'clean','fast',lambda rows,c:e.symbolic(rows))
                self.assertTrue(all(o['evaluation']['correct'] for o in r['outcomes'].values()))

    def test_fault_after_commit_does_not_erase_decision(self):
        def decision(rows,c):
            if c['round']>=5:raise RuntimeError('injected')
            return e.symbolic(rows)
        r=e.episode(8000,9,6,'clean','fast',decision)
        self.assertTrue(r['outcomes']['majority']['valid'])
        self.assertFalse(r['outcomes']['central-deadline']['valid'])

    def test_adaptation_can_help_or_hurt(self):
        good=e.episode(8000,9,6,'clean','stalled',lambda rows,c:e.symbolic(rows))
        self.assertTrue(good['outcomes']['adaptive']['evaluation']['correct'])
        self.assertTrue(good['outcomes']['fixed-three']['evaluation']['abstention'])
        bad=e.episode(8000,9,6,'late-wrong','late',lambda rows,c:e.symbolic(rows))
        self.assertTrue(bad['outcomes']['adaptive']['evaluation']['constraint_violation'])
        self.assertTrue(bad['outcomes']['fixed-two']['evaluation']['correct'])

    def test_same_documents_across_populations(self):
        a=e.episode(8000,5,6,'copies','fast',lambda rows,c:e.symbolic(rows))
        b=e.episode(8000,9,6,'copies','fast',lambda rows,c:e.symbolic(rows))
        self.assertEqual(a['documents'],b['documents'])


if __name__=='__main__':unittest.main()
