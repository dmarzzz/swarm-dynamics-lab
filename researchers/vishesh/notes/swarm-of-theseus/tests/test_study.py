import json,re,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from study import *
from analyze import analyze
from public_plan import validate

class ExactPolicy:
    def complete(self,request,fallback):
        o=request['observation']
        if 'cases' not in o:
            return {'message':o.get('private_notebook','What procedure and receipt phrase should I use?')}
        text=o.get('reference_procedure') or o['private_notebook'] or o['onboarding']
        mappings=re.findall(r'Map result 0 to (\w+) and result 1 to (\w+)',text)
        labels=list(mappings[-1]) if mappings else ['dax','wug']
        if o.get('current_bulletin'):
            labels=list(re.search(r'XOR 0 goes to (\w+); XOR 1 goes to (\w+)',o['current_bulletin']).groups())
        norm=re.findall(r'receipt phrase "([^"]+)"',text)
        answers=[]
        for c in o['cases']:
            if 'reports' in c:
                roots={x['root']:x['signal'] for x in c['reports']};bit=int(sum(roots.values())>len(roots)/2)
            else:bit=c['assay'][0]^c['assay'][1]
            answers.append(labels[bit])
        return {'answers':answers,'convention':norm[-1] if norm else '', 'notebook':text[:600]}

class StudyTests(unittest.TestCase):
    def test_positive_controls_all_scenarios(self):
        for s in SCENARIOS:
            w=world(s,22)
            for arm in ('founders','verbatim','notes','mentor','both'):
                row=run_world(w,arm,ExactPolicy(),lambda _:None)
                self.assertEqual(row['final_accuracy'],1)
                self.assertEqual(row['final_convention'],1)
    def test_total_turnover_and_channel_access(self):
        for arm in ARMS:
            events=[];row=run_world(world('seed-bank',23),arm,ExactPolicy(),events.append)
            self.assertEqual(row['history'][-1]['original_count'],3 if arm=='founders' else 0)
            for e in events:
                if e['kind']!='request':continue
                self.assertNotIn('expected',json.dumps(e['request']))
                o=e['request']['observation']
                if e['actor'].startswith('new') and e['operation']=='solve' and e['step']==int(e['actor'].split('-')[1]):
                    self.assertEqual(o['private_notebook'],'')
                    if arm=='neither':self.assertEqual(o['onboarding'],'')
            if arm!='founders':
                self.assertEqual(len(row['access']),3)
                for a in row['access']:
                    self.assertEqual(a['notes_access'],arm in ('notes','both'))
                    self.assertEqual(a['mentor_access'],arm in ('mentor','both'))
    def test_no_inheritance_loses_norm(self):
        row=run_world(world('seed-bank',23),'neither',ExactPolicy(),lambda _:None)
        self.assertEqual(row['final_convention'],0)
    def test_duplicate_counter_wrong(self):
        w=world('observatory',22)
        for c in w['cases'][0]:
            naive=w['labels'][int(sum(x['signal'] for x in c['reports'])>2)]
            self.assertNotEqual(naive,target(w,c,0))
    def test_bulletin_reverses_truth(self):
        w=world('repair-dock',22)
        for c in w['cases'][0]:self.assertNotEqual(target(w,c,3),target(w,c,4))
    def test_counterbalance_and_splits(self):
        self.assertEqual(world('seed-bank',100)['labels'],world('seed-bank',101)['labels'][::-1])
        ids=lambda seed:{x['id'] for cc in world('seed-bank',seed)['cases'] for x in cc}
        self.assertFalse(ids(100)&ids(200));self.assertFalse(ids(200)&ids(10000))
    def test_grader_rejects_agreement_wrong_and_tie(self):
        w=world('seed-bank',22);expected=[target(w,c,0) for c in w['cases'][0]]
        wrong=[{'answers':['bad']*4,'convention':w['convention']}]*3
        self.assertEqual(evaluate(w,0,wrong)['accuracy'],0)
        self.assertEqual(evaluate(w,0,wrong)['convention'],1)
        self.assertIsNone(majority(['a','b','c']))
    def test_malformed_and_total_call_count(self):
        with self.assertRaises(ValueError):validate_solve({'answers':['x']})
        events=[];run_world(world('seed-bank',22),'both',ExactPolicy(),events.append)
        self.assertEqual(sum(e['kind']=='request' for e in events),24)
    def test_preflight_fails_closed(self):
        with self.assertRaises(ValueError):validate({'id':'swarm-of-theseus','url':'https://example.com'},'','x'*80)
    def test_failure_denominator(self):
        rows=[{'scenario':s,'arm':a,'seed':seed,'status':'failed'} for s in SCENARIOS for a in ('both','neither') for seed in (200,201)]
        summary=analyze(rows);self.assertEqual(summary['failed'],12);self.assertEqual(summary['primary']['difference'],0);self.assertFalse(summary['qualification_passed'])

if __name__=='__main__':unittest.main()
