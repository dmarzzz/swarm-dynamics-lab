import unittest,json,tempfile
from pathlib import Path
import jev
from test_policies import fixture,CAL
from policies import initial,purchase,query_model
class JevTests(unittest.TestCase):
    def test_allowlist_covers_reachable_inputs(self):
        records=[fixture() for _ in range(21)];allowed=set(jev.allowlist(records))
        # Use the identical calibration as allowlist generation.
        from policies import calibrate
        cal=calibrate(records[:20])
        class AssertAllowed:
            def choose(self,s,i,c,x):
                assert jev.digest(s,{'type':'choice','instructions':i,'criteria':c}) in allowed
                return 'A'
        for first in [None,'A','B','C']:
            b=initial(records[-1],cal)
            if first:purchase(b,records[-1],first)
            for r in range(5):query_model(AssertAllowed(),b,r,False,{})
            query_model(AssertAllowed(),b,4,True,{})
    def test_route_and_schema(self):
        d={'model':jev.SNAPSHOT,'provider':jev.PROVIDER,'usage':{'cost':.00001,'input_tokens':100,'output_tokens':5},'answers':{'decision':{'choice':'A','probabilities':{'A':1,'B':0}}}}
        self.assertEqual(jev.validate_response(d,{'A':'a','B':'b'})['answers']['decision']['choice'],'A')
        d['provider']='other'
        with self.assertRaises(ValueError):jev.validate_response(d,{'A':'a','B':'b'})
    def test_recovery_reuses_exact_valid_response(self):
        state='fixture';q={'type':'choice','instructions':'pick','criteria':{'A':'a','B':'b'}};context={'task':25}
        old={'valid':True,'context':context,'input_hash':jev.digest(state,q),'choice':'B','probabilities':{'A':0,'B':1},'encoded_tokens':10,'wall_s':1}
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'old.json';p.write_text(json.dumps([old]));journal=Path(tmp)/'journal.jsonl'
            rt=jev.Runtime('http://127.0.0.1:1',previous=[p],journal=journal)
            self.assertEqual(rt.choose(state,'pick',q['criteria'],context),'B')
            self.assertTrue(rt.receipts[0]['reused_from']);self.assertEqual(len(journal.read_text().splitlines()),1)
    def test_rounded_vector_is_retained_not_normalized(self):
        probs={'A':.17,'B':.55,'C':.04,'STOP':.23}
        d={'model':jev.SNAPSHOT,'provider':jev.PROVIDER,'usage':{'cost':.00001,'input_tokens':100,'output_tokens':45},'answers':{'decision':{'choice':'B','probabilities':probs}}}
        self.assertEqual(jev.validate_response(d,probs)['answers']['decision']['probabilities'],probs)
        d['answers']['decision']['probabilities']['STOP']=.20
        with self.assertRaises(ValueError):jev.validate_response(d,probs)
    def test_probe_balance(self):
        p=jev.probes();self.assertEqual(len(p),16);self.assertEqual(sum(x['kind']=='option' for x in p),4)
if __name__=='__main__':unittest.main()
