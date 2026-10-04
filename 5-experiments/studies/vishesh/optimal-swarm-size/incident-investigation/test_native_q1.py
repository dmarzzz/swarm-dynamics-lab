import copy,json,unittest
from native_q1 import assignments,execute,SCHEMA,validate,payload
from prototype import World,build_case,reference

DEFAULT=dict(op='finish',handles=[],service='',field='pool',value_string='',value_int=0,allocations=[],decision='continue',diagnoses=[])
def script(row):
    w=World(build_case(row['structure'],row['condition'],row['seed']),row['slots']);actions=[]
    class Tools:
        def start(self):return w.start()
        def query(self,handles):actions.append(DEFAULT|dict(op='query',handles=handles));return w.query(handles)
        def act(self,a):
            if a['op']=='rebalance':v=DEFAULT|dict(op='rebalance',allocations=[dict(service=s,pool=p) for s,p in a['allocations'].items()])
            else:
                field,value=next(iter(a['set'].items()));v=DEFAULT|dict(op='patch',service=a['service'],field=field,**({'value_string':value} if field=='revision' else {'value_int':value}))
            actions.append(v);return w.act(a)
    answer=reference(Tools());actions.append(DEFAULT|dict(op='finish',**answer));return actions
class NativeTests(unittest.TestCase):
    def test_all_nine_interface_solutions_and_isolation(self):
        for row in assignments():
            actions=script(row);events=[];messages_seen=[]
            def call(messages,actor,turn):
                messages_seen.append(copy.deepcopy(messages));return json.dumps(actions[turn])
            r=execute(row,call,events.append);self.assertTrue(r['evaluation']['success'],row);self.assertLessEqual(r['model_calls'],10)
            packet=json.loads(messages_seen[0][1]['content']);self.assertNotIn('structure',packet);self.assertNotIn('condition',packet);self.assertNotIn('gold',packet)
            self.assertLess(max(len(json.dumps(payload(m)).encode()) for m in messages_seen),24000)
    def test_unjustified_escalation_is_not_correct(self):
        row=next(r for r in assignments() if r['condition']=='insufficient')
        r=execute(row,lambda *args:json.dumps(DEFAULT|{'decision':'escalate'}),lambda e:None)
        self.assertFalse(r['evaluation']['success']);self.assertFalse(r['evaluation']['observed_missing_evidence'])
    def test_schema_failure_and_transport_failure_preserved(self):
        row=assignments()[0]
        self.assertEqual(execute(row,lambda *args:'{}',lambda e:None)['failure'],'response_or_tool_contract')
        def failed(*args):raise RuntimeError('do not expose transport text')
        self.assertEqual(execute(row,failed,lambda e:None)['failure'],'execution_failed')
    def test_turn_limit_does_not_become_success(self):
        row=assignments()[0];first=World(build_case(row['structure'],row['condition'],row['seed'])).start()['handles'][0]
        r=execute(row,lambda *args:json.dumps(DEFAULT|dict(op='query',handles=[first])),lambda e:None)
        self.assertEqual(r['failure'],'turn_limit');self.assertFalse(r['evaluation']['success'])
    def test_finite_relay_scope(self):
        from local_relay import contracts
        ids,tokens,size=contracts('incident-q1');self.assertEqual(len(ids),90);self.assertEqual((tokens,size),(1024,24000))
        self.assertLess(90*38632,4000000)
    def test_invalid_action_types_rejected(self):
        with self.assertRaises(ValueError):validate(DEFAULT|{'value_int':True},SCHEMA)
        with self.assertRaises(ValueError):validate(DEFAULT|{'extra':1},SCHEMA)
if __name__=='__main__':unittest.main()

class ReceiptTests(unittest.TestCase):
    def test_call_receipts_success_failure_interruption_and_unstarted(self):
        import tempfile
        from pathlib import Path
        from receipts_q1 import write_manifest
        repo=Path(__file__).resolve().parents[5]
        for kind in ('success','transport','parse','interrupted'):
            with tempfile.TemporaryDirectory() as temp:
                root=Path(temp).resolve();target=root/'00';target.mkdir()
                row=assignments()[0];cid=row['id']+'/0/0'
                events=[{'kind':'request_context','call':cid,'serialized_request':'{}'}]
                if kind in ('success','parse'):events.append({'kind':'model_response','call':cid,'text':'{}','usage':{'cost':0}})
                if kind=='success':events.extend([{'kind':'parsed','turn':0,'value':{}},{'kind':'transition','turn':0,'receipt':{}}])
                if kind!='interrupted':events.append({'kind':'grade','value':{'correct':False}})
                (target/'trace.jsonl').write_text('\n'.join(json.dumps(e) for e in events)+'\n')
                write_manifest(root,[row],'a'*40,repo)
                m=json.loads((root/'trace-manifest.json').read_text());self.assertEqual(len(m['calls']),10)
                self.assertEqual(m['calls'][0]['status'],{'success':'valid','transport':'failed','parse':'failed','interrupted':'started'}[kind])
                self.assertTrue(all(c['status']=='unstarted' for c in m['calls'][1:]))
