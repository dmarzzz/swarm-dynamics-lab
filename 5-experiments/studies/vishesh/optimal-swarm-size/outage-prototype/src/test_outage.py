import copy,json,unittest
from world import World,make_case,digest,ARMS
from checker import grade
from engine import execute
from policies import reference_actions,should_contract

def scripted(messages,actor,tick):
    packet=json.loads(messages[-1]['content']);actions=reference_actions(packet['observation'])
    return json.dumps({'actions':actions[:4] if len(packet['roster'])==1 else actions[actor:actor+1]})

class OutageTests(unittest.TestCase):
    def test_reference_all_cases_and_arms(self):
        for root in range(4):
            for changing in (False,True):
                for replica in range(3):
                    for arm in ARMS:
                        r=execute(make_case(root,changing,replica),arm,scripted)
                        self.assertTrue(r['evaluation']['success'],(root,changing,arm,r['evaluation']))
    def test_counterfactual_changes_authoritative_state(self):
        for root in range(4):
            worlds=[World(make_case(root,c)) for c in (False,True)]
            for w in worlds:w.step([]);w.step([])
            self.assertNotEqual(worlds[0].snapshot(),worlds[1].snapshot())
    def test_event_tape_independent_of_actions(self):
        a=World(make_case(0));b=World(make_case(0))
        a.step([]);b.step([(0,{'op':'inspect','service':next(iter(b.services))})]);a.step([]);b.step([])
        self.assertEqual(a.directory,b.directory);self.assertEqual(a.events[0]['tick'],2)
    def test_observation_excludes_future_and_gold(self):
        obs=World(make_case(2)).observation();text=json.dumps(obs)
        for key in ('event','changing','cluster','case_id','root','evaluation','truth','protocol_rotation'):
            self.assertNotIn(key,obs);self.assertNotIn('protocol_rotation',text)
        self.assertEqual(World(make_case(0,False)).observation(),World(make_case(0,True)).observation())
    def test_versioned_write_prevents_stale_commit(self):
        w=World(make_case(0));obs=w.observation();w.step([(0,a) for a in reference_actions(obs)])
        actions=reference_actions(w.observation());w.step([(0,a) for a in actions])
        self.assertEqual(sum(x['result']['status']=='stale_version' for x in w.receipts),2)
        self.assertFalse(w.unsafe)
    def test_checker_rejects_wrong_endpoint_protocol_capacity_and_incomplete(self):
        r=execute(make_case(0,False),'scheduled');state=next(e['state'] for e in reversed(r['events']) if e['kind']=='step')
        for field,value in [('endpoint','bad'),('protocol',99),('pool',0),('pool',999)]:
            s=copy.deepcopy(state);next(iter(s['services'].values()))[field]=value
            self.assertFalse(grade(s,8)['success'])
        s=copy.deepcopy(state);s['tick']=7;self.assertFalse(grade(s,8)['success'])
    def test_harmful_commit_remains_failure_after_repair(self):
        w=World(make_case(0,False));name=next(iter(w.services));s=w.services[name];d=w.directory[s['alias']]
        w.step([(0,{'op':'patch','service':name,'service_version':1,'directory_version':1,'capacity_version':1,'set':{'endpoint':'bad'}})])
        self.assertEqual(len(w.unsafe),1)
        while w.tick<8:w.step([(0,a) for a in reference_actions(w.observation())])
        self.assertEqual(grade(w.snapshot(),8)['quality'],1);self.assertFalse(grade(w.snapshot(),8)['success'])
    def test_duplicate_patch_does_not_commit_twice(self):
        w=World(make_case(0,False));w.step([(0,a) for a in reference_actions(w.observation())]);a=reference_actions(w.observation())[0]
        out=w.step([(0,a),(1,a)]);self.assertEqual([r['result']['status'] for r in out],['applied','stale_version'])
    def test_wrong_or_malformed_preconditions_fail_closed(self):
        w=World(make_case(0));name=next(iter(w.services));before=digest(w.snapshot())
        for a in ({'op':'patch','service':name},{'op':'delete','service':name},{'op':'patch','service':name,'service_version':True,'directory_version':1,'capacity_version':1,'set':{'pool':2}}):
            self.assertNotEqual(w.apply(a)['status'],'applied')
        self.assertEqual(before,digest(w.snapshot()))
    def test_contraction_drains_and_changes_only_roster(self):
        r=execute(make_case(2),'contract',scripted);f=execute(make_case(2),'fixed',scripted)
        self.assertEqual(r['roster'][:2],[4,4]);self.assertEqual(r['roster'][2:],[1]*6)
        self.assertEqual([e for e in r['events'] if e['kind']=='observation'][:2],[e for e in f['events'] if e['kind']=='observation'][:2])
        self.assertTrue(all(e['in_flight']==0 for e in r['events'] if e['kind']=='contract'))
    def test_failure_stops_next_round_and_does_not_score_missing_as_zero(self):
        class Fault(Exception):code='http_429'
        calls=[]
        def fault(m,a,t):calls.append(t);raise Fault()
        r=execute(make_case(0),'single',fault)
        self.assertEqual(calls,[0]);self.assertEqual(r['failure'],'http_429');self.assertIsNone(r['evaluation']['quality'])
    def test_payload_ceiling_and_single_parallel_tools(self):
        sizes=[]
        def check(m,a,t):sizes.append(len(json.dumps(m).encode()));return scripted(m,a,t)
        for arm in ('single','fixed','contract'):execute(make_case(2),arm,check)
        self.assertLess(max(sizes),11000)
        r=execute(make_case(0),'single',scripted)
        self.assertEqual(len(next(e['receipts'] for e in r['events'] if e['kind']=='step')),4)
    def test_no_external_update_no_forced_contraction(self):
        r=execute(make_case(0,False),'contract',scripted);self.assertEqual(r['roster'],[4]*8)
    def test_checker_agrees_on_random_perturbations(self):
        import random
        rng=random.Random(8)
        for _ in range(100):
            w=World(make_case(rng.randrange(4),False));w.tick=8
            for s in w.services.values():
                d=w.directory[s['alias']];s.update(endpoint=rng.choice([d['endpoint'],'bad']),protocol=rng.randrange(3),pool=rng.randrange(7))
            self.assertEqual(grade(w.snapshot(),8)['quality'],sum(w.health().values())/4)
