import copy,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from p30 import Swarm,ROLES,wire,models
from p30_lineage import manifest,call_manifest,run,scripted_action,planned_order
from world import World
from common import canonical

class P30LineageTests(unittest.TestCase):
    def test_assignment_balance_pairing_and_request_ceiling(self):
        total=0
        for root,a in planned_order():
            rows=manifest(root,a);total+=len(call_manifest(root,a))
            self.assertEqual(len(rows),180)
            for ep in range(1,7):self.assertEqual({r['actor'] for r in rows if r['epoch']==ep},{f'agent-{i}' for i in range(30)})
        self.assertEqual(total,6360)
        self.assertEqual([r['actor'] for r in manifest(0,'A1')],[r['actor'] for r in manifest(0,'A3')])

    def execute(self,arm='A1',failure=None):
        e=Swarm(World(0,'schema_shift'),arm=arm,root=0);clock=[0.0];seen=[];maximum=[0]
        def backend(role,sections,ident):
            maximum[0]=max(maximum[0],len(canonical(wire(models()[role],sections))))
            seen.append(ident);task=sections[2]['job'];actor=next(s['own_definition']['id'] for s in sections if 'own_definition' in s)
            clock[0]+=1
            if failure=='transport':raise TimeoutError()
            if ':boundary:' in ident:action={'type':'propose','operation':'switch_model','payload':{'model':'cheap_generative'}}
            elif failure=='malformed':action={'type':'answer','value':'wrong','receipts':[]}
            else:action=scripted_action(e,actor,task)
            if failure=='late':clock[0]+=60
            return dict(action=action,usage={'cost_usd':.001},model=role)
        r=run(e,backend,ROLES,stage_started=0,clock=lambda:clock[0]);return e,r,maximum[0]

    def test_scripted_public_api_controller_answers_all_and_shared_cache_saves_fetches(self):
        e,r,size=self.execute();self.assertEqual(r['successful'],180);self.assertLess(size,7500)
        self.assertFalse(r['stop_stage']);self.assertEqual(len(r['records']),180)
        self.assertEqual(e.usage['fetches'],27);self.assertGreater(e.usage['cache_hits'],0)
        self.assertTrue(all(r['latency_s']<=2 for r in r['records']))
        self.assertEqual([f['successful'] for f in r['frames']],[30,60,90,120,150,180])

    def test_adaptation_changes_actual_backend_role_without_changing_denominator(self):
        e,r,size=self.execute('A3');self.assertEqual(r['successful'],180)
        self.assertEqual(len([x for x in r['calls'] if x['proposal']]),150)
        later=[x for x in r['calls'] if ':job:2:' in x['id']];self.assertTrue(all(x['role']=='cheap_generative' for x in later))
        self.assertEqual(len(e.actors),30);self.assertLess(size,7500)

    def test_floor_and_missing_outcomes_remain_in_assigned_denominator(self):
        e,r,_=self.execute('A3','malformed');self.assertEqual(r['stop_reason'],'first_epoch_capability_floor')
        self.assertFalse(r['stop_stage']);self.assertEqual(r['started'],30);self.assertEqual(r['terminal'],180);self.assertEqual(r['quality'],0)
        self.assertFalse(any(x['proposal'] for x in r['calls']))

    def test_transport_stops_stage_and_late_correct_outputs_fail_deadline(self):
        _,r,_=self.execute(failure='transport');self.assertTrue(r['stop_stage']);self.assertEqual(r['started'],1);self.assertEqual(len(r['calls']),1)
        _,late,_=self.execute(failure='late');self.assertEqual(late['successful'],0);self.assertEqual(late['stop_reason'],'first_epoch_capability_floor')

if __name__=='__main__':unittest.main()
