import contextlib,io,json,tempfile,time,unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch
from budget import Budget
from engine import execute
from tasks import generate,reference_answer
from run_qualification import assignments_for,run_batch

class Canary(unittest.TestCase):
    def config(self):
        c=json.loads((Path(__file__).parent.parent/'qualification-config.json').read_text())
        c.update(stage='canary',attempt_id='q-a3-canary',attempt_cap_microdollars=5000000,episode_cap_microdollars=1250000)
        return c
    def test_balanced_width_aware_manifest(self):
        rows=assignments_for(self.config())
        self.assertEqual([(r['family'],r['structure']) for r in rows],[('evidence','parallel'),('repository','chain'),('evidence','chain'),('repository','parallel')])
        self.assertEqual(len(set(r['id'] for r in rows)),4)
        self.assertTrue(all('/width2/' in r['id'] and len(r['public_task_sha256'])==64 for r in rows))
        self.assertTrue(set(r['id'] for r in rows).isdisjoint(r['id'] for r in assignments_for({})))
    def test_attempt_cap_atomic_and_immutable(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'budget.sqlite';old=Budget(p,100);old.reserve('old','old',10,20)
            b=Budget(p,100,'canary',20)
            def reserve(i):
                try:b.reserve(str(i),str(i),10,10);return True
                except ValueError:return False
            with ThreadPoolExecutor(max_workers=4) as pool:self.assertEqual(sum(pool.map(reserve,range(4))),2)
            with self.assertRaisesRegex(ValueError,'cannot_reset_attempt_cap'):Budget(p,100,'canary',30)
            self.assertEqual(old.exposure('old'),10)
            with self.assertRaisesRegex(ValueError,'attempt_budget_exhausted'):b.reserve('more','more',1,10)
    def test_schema_violation_stops_before_integration(self):
        task=generate('evidence','parallel',0,width=2);calls=[]
        def call(messages,deadline,actor,phase,item):
            calls.append(phase)
            if phase=='plan':return json.dumps({'dependencies':task.public['dependencies']})
            return '{"artifact":{"value":true,"source_ids":[]}}'
        r=execute(task.public,1,1,10,2,call,strict_contract=True)
        self.assertEqual(r['failure'],'schema_output_invalid');self.assertEqual(calls,['plan','work'])
    def test_full_paths_both_families(self):
        for family in ('evidence','repository'):
            for structure in ('parallel','chain'):
                task=generate(family,structure,0,width=2);answer=reference_answer(task);events=[]
                def call(messages,deadline,actor,phase,item):
                    if phase=='plan':return json.dumps({'dependencies':task.public['dependencies']})
                    if phase=='work':return json.dumps({'artifact':answer['answers'][item] if family=='evidence' else answer['files'][item+'.py']})
                    return json.dumps(answer)
                r=execute(task.public,1,1,10,2,call,events.append,strict_contract=True)
                self.assertIsNone(r['failure']);self.assertEqual(r['completed_items'],2)
                self.assertEqual(sum(e['kind']=='schema_validation' and e['valid'] for e in events),4)
    def test_early_stop_keeps_four_assigned_and_delivery_separate(self):
        class Reporter:
            def __init__(self,*a):pass
            def finish(self,*a):return {'complete':True}
        class Broken:
            def __init__(self,*a):pass
            def __call__(self,*a):return '```json\n{}\n```'
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'run';out.mkdir();cfg=self.config()
            with patch('run_qualification.Reporter',Reporter),patch('run_qualification.Provider',Broken),contextlib.redirect_stdout(io.StringIO()):
                run_batch(cfg,'offline',out,Path(tmp)/'budget.sqlite',assignments_for(cfg))
            r=json.loads((out/'reconciliation.json').read_text())
            self.assertEqual((r['assigned'],r['terminal'],r['unstarted']),(4,1,3))
            self.assertEqual(r['stop_reason'],'schema_output_invalid')
            self.assertTrue(r['executed_publication_complete']);self.assertFalse(r['execution_complete'])
