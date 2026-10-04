import unittest
import study as s


class Tests(unittest.TestCase):
    def test_mock_matches_hidden_quality(self):
        for task in range(7200,7206):
            f=s.fixture(task)
            for k,v in f['truth'].items():
                p=s.mock_probe(f,k)
                self.assertEqual(p['accuracy'],v['accuracy'] if v['scanned'] else 0)
                self.assertNotIn('retention_days',p)

    def test_information_budget(self):
        f=s.fixture(7200)
        a=s.reports(f,'clean','late',5);b=s.reports(f,'clean','late',9)
        self.assertEqual([{k:v for k,v in d.items() if k!='agent'} for d in a],[{k:v for k,v in d.items() if k!='agent'} for d in b])

    def test_copy_dedup(self):
        f=s.fixture(7200);d=s.reports(f,'copied-favorable','fast',9)
        self.assertEqual(len(s.state_for([x for x in d if x['root']=='r0'])['observations']),3)

    def test_blind_and_deadlines(self):
        state=s.state_for(s.reports(s.fixture(7200),'clean','fast',9))
        self.assertNotIn('truth',str(state));self.assertNotIn('target',str(state))
        votes=['A']*9;contexts=[[{'root':str(i%2)}] for i in range(9)]
        self.assertIsNone(s.select(votes,contexts,'fixed',3,3))
        self.assertEqual(s.select(votes,contexts,'adaptive',3,3),'A')
        self.assertIsNone(s.select(votes,contexts,'adaptive',2,3))

    def test_clean_competence(self):
        for t in range(7200,7206):
            for n in (5,9):
                rows=s.episode(t,n,3,'clean','fast',s.scripted)
                self.assertTrue(all(r['evaluation']['correct'] for r in rows))
                self.assertEqual(len(rows),7)

    def test_misleading_late_evidence(self):
        f=s.fixture(7200)
        truthful=s.state_for(s.reports(f,'clean','stalled',9))
        misleading=s.state_for(s.reports(f,'misleading-newer','stalled',9))
        self.assertNotEqual(s.scripted(truthful),s.scripted(misleading))

    def test_none_and_failures(self):
        self.assertEqual(s.best(s.fixture(7203)['truth']),'NONE')
        rows=s.episode(7200,9,3,'clean','fast',lambda _: 'BOGUS')
        self.assertTrue(all(not r['validity']['ok'] and r['evaluation']['loss']==1 for r in rows))


if __name__=='__main__':unittest.main()
