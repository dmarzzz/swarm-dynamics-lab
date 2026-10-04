import copy
import itertools
import json
from pathlib import Path
import tempfile
import unittest
from contract import *
from qualification import SNAPSHOT, PROVIDER


def response(choice):
    return {'model':SNAPSHOT,'provider':PROVIDER,'usage':{'cost':.00001,'input_tokens':800,'output_tokens':39},
        'answers':{'decision':{'choice':choice,'probabilities':{k:1. if k==choice else 0. for k in CRITERIA}}}}


def receipts(manifest, policy):
    return [{'id':r['id'],'request_sha256':r['request_sha256'],'status':'complete','response':response(policy(r))} for r in manifest['assignments']]


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.q=make_manifest(QUAL);self.m=make_manifest(MAIN)
    def test_counts_balanced(self):
        self.assertEqual((self.q['max_calls'],self.m['max_calls']),(8,160))
        self.assertAlmostEqual(self.q['reserved_usd']+self.m['reserved_usd'],.225792)
        self.assertEqual(len({r['request_sha256'] for r in self.m['assignments']}),80)
        for repeat in (1,2):
            block=[r for r in self.m['assignments'] if r['repeat']==repeat]
            self.assertEqual(len(block),80)
            self.assertEqual(len({(r['fixture'],r['representation'],r['context']) for r in block}),80)
    def test_sources_pairs_and_oracle(self):
        grouped={}
        for r in self.m['assignments']:
            sources={}
            for report in r['request']['state']['reports']:
                value=(report['value'],report['q'])
                self.assertEqual(sources.setdefault(report['visible_root'],value),value)
            self.assertEqual(len(sources),3)
            self.assertEqual('ONE' if sum(x[0] for x in sources.values())>=2 else 'ZERO',r['expected'])
            self.assertEqual(grouped.setdefault(r['fixture'],sources),sources)
    def test_no_evaluator_context_leak(self):
        instructions=set()
        for r in self.m['assignments']:
            body=r['request'];instructions.add(body['questions']['decision']['instructions'])
            self.assertEqual(set(body['state']),{'reports','prior_role','prior_decisions'})
            self.assertNotIn('expected',json.dumps(body));self.assertNotIn('wrong',json.dumps(body))
            self.assertNotIn('correct',json.dumps(body))
        self.assertEqual(instructions,{INSTRUCTIONS})
    def test_repeated_payloads_and_complement_ids(self):
        for r in self.m['assignments']:
            other=next(a for a in self.m['assignments'] if (a['fixture'],a['representation'],a['context'],a['repeat'])==(r['fixture'],r['representation'],r['context'],3-r['repeat']))
            self.assertEqual(json.dumps(r['request']),json.dumps(other['request']))
            complement=next(a for a in self.m['assignments'] if (a['fixture'],a['representation'],a['context'],a['repeat'])==(r['fixture']^1,r['representation'],r['context'],r['repeat']))
            self.assertEqual([(p['id'],p['visible_root']) for p in r['request']['state']['reports']],[(p['id'],p['visible_root']) for p in complement['request']['state']['reports']])
    def test_exact_policy_no_false_signal(self):
        result=analyze(self.m,receipts(self.m,lambda r:r['expected']))
        self.assertEqual(result['correct'],160);self.assertEqual(result['unanimous_controls']['assigned'],16)
        self.assertEqual(result['primary']['decision'],'criterion_not_met')
        self.assertEqual(result['repeat_agreement']['agree'],80)
    def test_report_majority_rescued_by_normalization(self):
        def majority(row):
            reports=row['request']['state']['reports']
            return 'ONE' if sum(p['value'] for p in reports)>len(reports)/2 else 'ZERO'
        result=analyze(self.m,receipts(self.m,majority))
        self.assertEqual(result['primary']['effect'],1.)
        self.assertEqual(result['primary']['decision'],'normalization_signal')
        self.assertTrue(all(v==0 for v in result['context_effects'].values()))
    def test_prior_policy_distinguishable(self):
        result=analyze(self.m,receipts(self.m,lambda r:r['prior'] or r['expected']))
        self.assertEqual(result['primary']['effect'],0.)
        self.assertEqual(result['context_effects']['deduplicated/self-wrong/conflict'],-1.)
        self.assertEqual(result['context_effects']['copied/peers-correct/conflict'],0.)
    def test_qualification_controls(self):
        rec=receipts(self.q,lambda r:r['expected']);self.assertTrue(analyze(self.q,rec)['qualified'])
        unanimous=next(i for i,r in enumerate(self.q['assignments']) if r['stratum']=='agreement')
        rec[unanimous]['response']=response('DEFER')
        self.assertEqual(analyze(self.q,rec)['correct'],7);self.assertFalse(analyze(self.q,rec)['qualified'])
    def test_missing_bounds_not_claimed(self):
        result=analyze(self.m,[])
        self.assertEqual(result['accuracy_bounds'],[0,1]);self.assertEqual(result['primary']['bounds'],[-1,1])
        self.assertEqual(result['primary']['decision'],'withheld')
        rec=receipts(self.m,lambda r:r['expected']);rec[0]={'id':rec[0]['id'],'request_sha256':rec[0]['request_sha256'],'status':'failed'}
        result=analyze(self.m,rec)
        self.assertEqual(result['failed'],1);self.assertEqual(result['valid'],159)
        self.assertEqual(result['primary']['decision'],'withheld')
    def test_bad_controls_withhold_effect(self):
        rec=receipts(self.m,lambda r:'DEFER' if r['stratum']=='agreement' else r['expected'])
        self.assertEqual(analyze(self.m,rec)['primary']['decision'],'withheld')
    def test_bad_receipts_and_usage_rejected(self):
        rec=receipts(self.m,lambda r:r['expected'])
        for bad in ([rec[0],rec[0]],[dict(rec[0],id='unknown')],[dict(rec[0],request_sha256='changed')]):
            with self.assertRaises(ValueError):analyze(self.m,bad)
        for value in (-1,True,float('nan')):
            bad=copy.deepcopy(rec[:1]);bad[0]['response']['usage']['output_tokens']=value
            with self.assertRaises(ValueError):analyze(self.m,bad)
    def test_manifest_mutation(self):
        self.m['assignments'][0]['expected']='DEFER'
        with self.assertRaises(ValueError):analyze(self.m,[])
    def test_preview_reconciles(self):
        rec=receipts(self.m,lambda r:'DEFER')[:2];rec[1]={'id':rec[1]['id'],'request_sha256':rec[1]['request_sha256'],'status':'failed'}
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'preview.html';replay=render(self.m,rec,path,True)
            self.assertIn('NOT MODEL EVIDENCE',path.read_text());self.assertEqual(path.read_text().count('<tr data-step='),160)
            self.assertEqual(replay[-1]['unstarted'],158);self.assertEqual(replay[-1]['failed'],1)

if __name__=='__main__':unittest.main()
