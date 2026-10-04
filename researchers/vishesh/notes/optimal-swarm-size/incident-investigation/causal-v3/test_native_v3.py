import copy,json,tempfile,unittest
from pathlib import Path
from native_v3 import assignments,execute,payload,encode,decode,SCHEMA,SYSTEM,validate
from worlds import World
from broker import Broker,scripted_run
from admission_v3 import errors,gate,STAGE_CAPS,STAGE_CALLS,FLAGS
from receipts_v3 import write_manifest

class NativeV3Tests(unittest.TestCase):
    def test_full_roster_reference_through_native_boundary(self):
        records=[]
        for row in assignments():
            script,_=scripted_run(World(row['root'],row['condition']),row['n']);events=[]
            def call(messages,actor,turn):
                self.assertLessEqual(len(json.dumps(payload(messages)).encode()),24000)
                packet=json.loads(messages[1]['content']);self.assertNotIn('condition',packet);self.assertNotIn('root',packet);self.assertNotIn('state',packet)
                return json.dumps(encode(script.events[turn]['proposals'][actor]))
            result=execute(row,call,events.append);self.assertTrue(result['evaluation']['joint_correct'],row);self.assertIsNone(result['failure']);records.append(result)
        self.assertTrue(gate('A',[r for r in records if r['assignment']['stage']=='A']))
        self.assertTrue(gate('B',[r for r in records if r['assignment']['stage']=='B']))
    def test_roster_cost_sessions_and_pairing(self):
        rows=assignments();self.assertEqual(len(rows),60);self.assertEqual(len({r['id'] for r in rows}),60)
        self.assertEqual(sum(r['round_limit']*r['n'] for r in rows),900)
        for stage in 'ABC':
            calls=sum(r['round_limit']*r['n'] for r in rows if r['stage']==stage);self.assertEqual(calls,STAGE_CALLS[stage]);self.assertLessEqual(calls*38632,STAGE_CAPS[stage])
        c=[r for r in rows if r['stage']=='C']
        self.assertEqual({r['session'] for r in c},{1,2})
        for block in range(3):self.assertEqual(len([r for r in c if r['block']==block]),12)
    def test_worst_permitted_nonterminal_history_serialization(self):
        # Repeated typed, maximum-length diagnosis disagreement never yields a finished answer.
        for n in (1,3):
            b=Broker(World('route_config','clean'),n)
            if n==1:
                for _ in range(9):b.step([[{'op':'wait'}]*3])
            else:
                d={'target':'incident','cause':'schema_rollout_stalled','evidence':['x'*64,'y'*64,'z'*64]}
                for _ in range(9):b.step([[{'op':'finish','decision':'resolve' if a!=2 else 'escalate','diagnoses':[d]}] for a in range(3)])
            for actor in range(n):
                req=payload([{'role':'system','content':SYSTEM},{'role':'user','content':json.dumps(b.packet(actor))}]);self.assertLessEqual(len(json.dumps(req).encode()),24000)
    def test_maximum_patch_history_serialization(self):
        for n in (1,3):
            b=Broker(World('route_config','fault'),n)
            q=[[{'op':'query','handle':h} for h in b.packet(a)['owned_handles']] for a in range(n)];b.step(q)
            for _ in range(8):
                b.step([[{'op':'patch','field':f,'value':'x'*128} for f in b.packet(a)['owned_fields']] for a in range(n)])
            for actor in range(n):self.assertLessEqual(len(json.dumps(payload([{'role':'system','content':SYSTEM},{'role':'user','content':json.dumps(b.packet(actor))}])).encode()),24000)
    def test_schema_bounds_and_finite_round_scopes(self):
        value=encode([{'op':'wait'}]*4)
        with self.assertRaises(ValueError):decode(value)
        bad=encode([{'op':'query','handle':'x'*65}])
        with self.assertRaises(ValueError):decode(bad)
        from local_relay import contracts
        a,_,_=contracts('causal-v3-session1');b,_,_=contracts('causal-v3-session2');self.assertEqual(len(a)+len(b),900);self.assertFalse(set(a)&set(b))
    def test_operational_vs_task_failures(self):
        row=assignments()[0]
        bad=execute(row,lambda *a:'{}',lambda e:None);self.assertEqual(bad['failure'],'response_schema');self.assertTrue(bad['operational_failure'])
        wrong=execute(row,lambda *a:json.dumps(encode([{'op':'query','handle':'service-name'}])),lambda e:None);self.assertEqual(wrong['failure'],'broker_contract');self.assertFalse(wrong['operational_failure'])
        waited=execute(row,lambda *a:json.dumps(encode([{'op':'wait'}])),lambda e:None);self.assertEqual(waited['failure'],'turn_limit');self.assertFalse(waited['evaluation']['joint_correct'])
    def test_withdrawn_authority_cannot_admit(self):
        r={k:True for k in FLAGS}|{'funding_authority':'PI-FUND-20261004-03','source_commit':'x','verified_epoch':100,'claim_expiry_epoch':1000,'allocated_seconds_used':0,'hourly_rate_usd':.1,'api_packet_cap_microdollars':35000000,'all_in_packet_cap_microdollars':36000000,'study_cap_microdollars':50000000}
        self.assertIn('funding_missing_or_withdrawn',errors(r,'x',100));self.assertTrue(errors({},'x',100))
    def test_receipts_parallel_parse_failure_and_unstarted(self):
        repo=Path(__file__).resolve().parents[6];row=next(r for r in assignments() if r['n']==3)
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);d=root/f"{row['index']:02d}";d.mkdir();events=[]
            for actor in range(3):
                cid=f"{row['id']}/0/{actor}";events.extend([{'kind':'request_context','call':cid,'serialized_request':'{}'},{'kind':'model_response','call':cid,'text':'{}','usage':{'cost':0}}])
            events.extend([{'kind':'parsed','turn':0,'actor':0,'value':{}},{'kind':'grade','value':{'joint_correct':False}}]);(d/'trace.jsonl').write_text('\n'.join(map(json.dumps,events)))
            write_manifest(root,[row],'a'*40,repo);m=json.loads((root/'trace-manifest.json').read_text());self.assertEqual(len(m['calls']),12);self.assertEqual(sum(c['status']=='failed' for c in m['calls']),3);self.assertEqual(sum(c['status']=='unstarted' for c in m['calls']),9)

if __name__=='__main__':unittest.main()
