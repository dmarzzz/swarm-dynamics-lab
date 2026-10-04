import copy,json,sqlite3,tempfile,time,unittest
from pathlib import Path
from unittest.mock import patch
import design,relay,run

class DesignTests(unittest.TestCase):
    def test_role_balance(self):
        from collections import Counter
        counts=Counter(design.role(s) for s in range(1,41))
        self.assertEqual(counts['direct'],20);self.assertEqual(sorted(counts.values()),[5,5,5,5,20])
    def test_actor_same_image_no_gold(self):
        a=design.request(b'pixels',1);b=design.request(b'pixels',21)
        self.assertEqual(a['messages'][1]['content'][1],b['messages'][1]['content'][1])
        self.assertEqual(a['model'],b['model']);self.assertEqual(a['temperature'],b['temperature'])
        self.assertNotIn('gold',json.dumps(a));self.assertEqual(a['provider']['allow_fallbacks'],False)
    def test_strict_majority(self):
        values={i:{'decision':'accept','amount':'100.00','evidence':'Total'} for i in range(1,11)}
        self.assertIsNone(design.aggregate(values,list(range(1,21))))
        values[11]=values[1];self.assertEqual(design.aggregate(values,list(range(1,21))),'100.00')
    def test_referrals_not_correct(self):
        records=[{'case':'r','seat':s,'error':None,'parsed':{'decision':'refer','amount':None,'evidence':''}} for s in range(1,41)]
        r=design.summarize([{'id':'r','gold':'100.00'}],records)
        self.assertEqual(r['policies']['pooled40']['refer'],1);self.assertEqual(r['rows'][0]['correct_votes'],0)
    def test_unscorable_and_missing_separate(self):
        r=design.summarize([{'id':'r','gold':None}],[])
        self.assertEqual(r['policies']['pooled40']['incomplete'],1)
    def test_invalid_schema(self):
        for text in ('{}','{"decision":"accept","amount":100,"evidence":""}','{"decision":"refer","amount":"100.00","evidence":""}'):
            self.assertIsNone(design.parse(text))
    def test_correlated_wrong_cluster(self):
        r=design.summarize([{'id':'r','gold':'100.00'}],[{'case':'r','seat':s,'error':None,'parsed':{'decision':'accept','amount':'200.00','evidence':''}} for s in range(1,41)])
        self.assertEqual(r['rows'][0]['wrong_vote_clusters'],{'200.00':40});self.assertEqual(r['policies']['pooled40']['wrong'],1)

class RelayTests(unittest.TestCase):
    def body(self):return {'model':design.MODEL,'provider':'Anthropic','usage':{'prompt_tokens':100,'completion_tokens':30,'cost':.00025},'choices':[{'finish_reason':'stop','message':{'content':'{"decision":"accept","amount":"100.00","evidence":"Total 100"}'}}]}
    def test_decode(self):self.assertIsNone(relay.decode(self.body())['error'])
    def test_route_usage_and_truncation(self):
        for key,value,error in [('model','other','route_mismatch'),('provider','other','route_mismatch'),('usage',{},'usage_missing')]:
            b=self.body();b[key]=value;self.assertEqual(relay.decode(b)['error'],error)
        b=self.body();b['choices'][0]['finish_reason']='length';self.assertEqual(relay.decode(b)['error'],'incomplete_output')
        b=self.body();b['usage']['cost']=.1;self.assertEqual(relay.decode(b)['error'],'usage_bound_exceeded')
    def test_duplicate_and_budget_no_reset(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'ledger.sqlite'
            with sqlite3.connect(p) as db:db.execute('CREATE TABLE calls(id TEXT PRIMARY KEY,reserved REAL,status TEXT,cost REAL)')
            relay.reserve(p,'one')
            with self.assertRaises(sqlite3.IntegrityError):relay.reserve(p,'one')
            with patch.object(relay,'MAX_CALLS',1):
                with self.assertRaises(ValueError):relay.reserve(p,'two')
            with sqlite3.connect(p) as db:self.assertEqual(db.execute('select count(*) from calls').fetchone()[0],1)

class CollectorTests(unittest.TestCase):
    def test_trace_success_and_error(self):
        for fail in (False,True):
            with tempfile.TemporaryDirectory() as t:
                root=Path(t).resolve();inputs=root/'inputs';inputs.mkdir();(inputs/'images').mkdir()
                cases=[];allowed={}
                for i in range(2):
                    identity=f'Q0-case-{i:03d}';image=inputs/'images'/f'{identity}.png';image.write_bytes(b'fixture')
                    cases.append({'id':identity,'stage':'Q0','image':image.name,'image_sha256':design.sha(image),'gold':'100.00'})
                    for seat in range(1,41):allowed[f'{identity}-a{seat:02d}']=design.digest(design.request(b'fixture',seat))
                (inputs/'cases.json').write_text(json.dumps(cases));(inputs/'allowlist.json').write_text(json.dumps(allowed))
                def call(*args):
                    return {'error':'http_429' if fail else None,'parsed':None if fail else {'decision':'accept','amount':'100.00','evidence':'Total 100'},
                            'raw_text':'fixture','usage':None if fail else {'prompt_tokens':100,'completion_tokens':20},'actual_usd':None if fail else .0002}
                with patch.object(run,'validate'),patch.object(run,'render'):
                    r=run.collect('Q0',inputs,root/'out',{},'url','cap',lambda *a:None,call)
                self.assertEqual(r['started'],4 if fail else 80)
                self.assertEqual(r['qualification_passed'],not fail)
                self.assertEqual(r['unstarted'],76 if fail else 0)
                self.assertEqual(r['trace_status'],'gaps' if fail else 'verified_declared_coverage')
    def test_admission_default_closed(self):
        with self.assertRaises(Exception):run.validate({},'Q0',Path('/nonexistent'))

if __name__=='__main__':unittest.main()
