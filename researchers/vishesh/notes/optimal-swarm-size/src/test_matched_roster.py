"""Offline scripted fixtures, never model evidence."""
import json,time,unittest
from engine import execute,validate_plan
from tasks import generate,reference_answer
from run_qualification import assignments_for

class MatchedRoster(unittest.TestCase):
    def test_pairs_and_counterbalance(self):
        rows=assignments_for(dict(stage='matched-roster',attempt_id='q-a6',attempt_cap_microdollars=4000000,episode_cap_microdollars=2000000,response_contract='anthropic-json-schema-v1'))
        self.assertEqual(len(rows),8);self.assertEqual(len({r['id'] for r in rows}),8)
        self.assertEqual([r['n'] for r in rows],[1,2,2,1,2,1,1,2])
        self.assertEqual({r['root'] for r in rows},{4,5})
        for a,b in zip(rows[::2],rows[1::2]):
            self.assertEqual(a['pair_id'],b['pair_id']);self.assertEqual(a['public_task_sha256'],b['public_task_sha256'])
    def test_required_edges_and_optional_extra_edges(self):
        with self.assertRaisesRegex(ValueError,'missing_required'):
            validate_plan({'dependencies':{'a':[],'b':[]}},['a','b'],{'a':[],'b':['a']})
        self.assertEqual(validate_plan({'dependencies':{'a':[],'b':['a']}},['a','b'],{'a':[],'b':[]})['b'],['a'])
    def test_missing_edges_repair_once_then_stop(self):
        task=generate('evidence','chain',4,width=3);phases=[]
        def wrong(messages,deadline,actor,phase,item):
            phases.append(phase);return json.dumps({'dependencies':{i:[] for i in task.public['items']}})
        r=execute(task.public,2,4,10,2,wrong,strict_contract=True,enforce_dependencies=True)
        self.assertEqual(phases,['plan','plan_repair']);self.assertEqual(r['completed_items'],0);self.assertIsNotNone(r['failure'])
    def test_context_isolation_and_work_concurrency(self):
        for structure in ('parallel','chain'):
            task=generate('evidence',structure,4,width=4);answer=reference_answer(task);events=[];messages_seen=[]
            def scripted(messages,deadline,actor,phase,item):
                messages_seen.append((actor,phase,messages))
                if phase=='plan':return json.dumps({'dependencies':task.public['dependencies']})
                if phase=='work':
                    time.sleep(.02)
                    return json.dumps({'artifact':answer['answers'][item]})
                return json.dumps(answer)
            r=execute(task.public,2,4,10,2,scripted,events.append,strict_contract=True,enforce_dependencies=True)
            self.assertIsNone(r['failure']);self.assertEqual(r['used_contexts'],[0,1])
            active=peak=0
            for event in sorted(events,key=lambda x:x['t']):
                if event.get('phase')=='work':
                    if event['kind']=='service_start':active+=1;peak=max(peak,active)
                    elif event['kind']=='service_end':active-=1
            self.assertEqual(peak,2 if structure=='parallel' else 1);self.assertEqual(active,0)
            actor1=next(m for a,p,m in messages_seen if a==1 and p=='work')
            self.assertEqual(len(actor1),3)
            self.assertFalse(any('stage_diagnostics' in json.dumps(m) for _,_,m in messages_seen))
if __name__=='__main__':unittest.main()
