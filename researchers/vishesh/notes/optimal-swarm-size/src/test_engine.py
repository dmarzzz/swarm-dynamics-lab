import json
import unittest
from engine import execute,validate_plan
from tasks import generate,reference_answer,evaluate

class Engine(unittest.TestCase):
    def test_plan_validation(self):
        for plan in ({'dependencies':{'a':['b'],'b':['a']}},{'dependencies':{'a':['a'],'b':[]}},{'dependencies':{'a':[]}}):
            with self.assertRaises(ValueError):validate_plan(plan,['a','b'])
    def test_scripted_transport_all_sizes(self):
        # The scripted transport owns reference answers; the engine never receives truth.
        for family in ('evidence','repository'):
            task=generate(family,'chain',0);answer=reference_answer(task)
            for n in (1,2,4,8,16):
                traces=[];contexts=[]
                def scripted(messages,deadline,actor,phase,item):
                    contexts.append(messages)
                    if phase=='plan':return json.dumps({'dependencies':task.public['dependencies']})
                    if phase=='work':return json.dumps({'artifact':answer['answers'][item] if family=='evidence' else answer['files'][item+'.py']})
                    return json.dumps(answer)
                result=execute(task.public,n,4,10,2,scripted,traces.append)
                self.assertIsNone(result['failure'])
                self.assertTrue(evaluate(task,result['artifact'])['substantive_success'])
                self.assertEqual(result['completed_items'],16)
                self.assertEqual(len(result['used_contexts']),n)
                self.assertTrue(all('hidden_inputs' not in json.dumps(m) for m in contexts))
                self.assertEqual(traces[-1]['kind'],'terminal')
    def test_invalid_plan_repaired_once(self):
        task=generate('evidence','parallel',0);phases=[]
        def broken(messages,deadline,actor,phase,item):phases.append(phase);return '{}'
        r=execute(task.public,2,2,10,2,broken)
        self.assertIsNotNone(r['failure']);self.assertEqual(phases,['plan','plan_repair'])
    def test_transport_value_error_is_not_retried(self):
        task=generate('evidence','parallel',0);calls=[]
        def broken(*args):calls.append(1);raise ValueError('route_changed')
        r=execute(task.public,1,1,10,2,broken)
        self.assertEqual(r['failure'],'route_changed');self.assertTrue(r['fatal']);self.assertEqual(len(calls),1)
    def test_provider_error_preserved(self):
        task=generate('evidence','parallel',0)
        def broken(*args):raise RuntimeError('synthetic provider failure')
        r=execute(task.public,1,1,10,2,broken)
        self.assertEqual(r['failure'],'transport_failed');self.assertTrue(r['fatal']);self.assertIsNone(r['artifact'])
if __name__=='__main__':unittest.main()
