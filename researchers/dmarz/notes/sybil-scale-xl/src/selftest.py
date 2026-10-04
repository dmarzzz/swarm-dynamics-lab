import importlib.util,json,tempfile,unittest,os
from pathlib import Path
import study,sim,provider,render
class Tests(unittest.TestCase):
 def test_anchor(self):
    path=study.ROOT.parent/'sybil-specialists/src/sim.py';spec=importlib.util.spec_from_file_location('oldsim',path);old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
    for task in (4900,4901):
     for rate in (.1,.9):
      cfg=study.cfg_for(36);a=old.make_world(task,1,rate,False,cfg);b=sim.make_world(task,1,rate,False,cfg)
      self.assertEqual(a,b)
      previous=old.run_episode(a,4,sim.ARMS,cfg)
      current=sim.checkpoints(b,[4],sim.ARMS,cfg)
      for x,y in zip(previous,current):self.assertEqual(x['trace'][-1]['admitted'],y['admitted']);self.assertEqual(x['trace'][-1]['metrics'],y['graph_metrics'])
 def test_graph_scaling(self):
    for n in study.design()['sizes']:
     w=sim.make_world(4900,n//36,.1,False,study.cfg_for(n));p=w['public'];adj=p['adj'];truth=w['truth']
     seen=set(p['trusted']);todo=list(seen)
     while todo:
      for v in adj[todo.pop()]:
       if v not in seen:seen.add(v);todo.append(v)
     self.assertEqual(len(seen),n);self.assertEqual(len(p['trusted']),2)
     self.assertEqual(sum(not v['honest'] for v in truth.values()),n//4)
     for node in adj:self.assertEqual(len(adj[node]),7 if w['groups'][node]==0 else 4)
     for group in (1,2):
      nodes=[node for node in adj if w['groups'][node]==group]
      self.assertEqual(sum(w['groups'][other]==0 for node in nodes for other in adj[node]),2*(n//36))
     profiles=[]
     for group in (1,2):profiles.append(sorted((v['skill'],v['age'],v['activity']) for node,v in p['nodes'].items() if w['groups'][node]==group))
     self.assertEqual(*profiles)
 def test_blind_packet(self):
    w=sim.make_world(4900,3,.1,False,study.cfg_for(108));nodes=list(w['public']['nodes'])[:54]
    a=study.packet(w,nodes,[], 'visible','random');b=study.packet(w,nodes,[],'masked','random')
    for x,y in zip(a['reports'],b['reports']):
     self.assertEqual({k:v for k,v in x.items() if k!='verification'},y)
     self.assertEqual(set(x),{'node','skill','claim','age','activity','verification'})
 def test_accounting_duplicate_and_cap(self):
    with tempfile.TemporaryDirectory() as td:
     ledger=provider.Ledger(Path(td)/'ledger');ledger.transact({'type':'reserve','call_id':'a','micro_usd':1})
     with self.assertRaises(provider.CallFailure):ledger.transact({'type':'reserve','call_id':'a','micro_usd':1})
     with self.assertRaises(provider.CallFailure):ledger.transact({'type':'reserve','call_id':'b','micro_usd':int(study.design()['budget']['aggregate_usd']*1_000_000)+1000000})
 def test_render_pending_and_failure(self):
    im=render.frame([],2400,'S1');self.assertEqual(im.size,(1800,1200))
    im=render.frame([{'status':'failed','kind':'pilot','n':36}],2400,'S1');self.assertEqual(im.size,(1800,1200))
 def test_principal_blind_checks(self):
    w=sim.make_world(4900,1,.1,False,study.cfg_for(36));p=json.loads(json.dumps(w['public']))
    expected=sim.select_check(p,'coverage',set(),set(),[],4900,1)
    for t in w['truth'].values():t['honest']=not t['honest']
    self.assertEqual(expected,sim.select_check(p,'coverage',set(),set(),[],4900,1))
 def test_splits(self):
    d=study.design();groups=[set(d[k]) for k in ('worlds','qualification_worlds','engineering_worlds')]
    self.assertTrue(all(not a&b for i,a in enumerate(groups) for b in groups[i+1:]));self.assertTrue(max(set.union(*groups))<10000)
 def test_invalid_answers(self):
    for vals in ({'0':True},{str(i):True for i in range(6)}):
     with self.assertRaises(ValueError):study.validate({'values':vals})
 def test_concurrent_failure_denominator(self):
    import worker,threading
    from unittest.mock import patch
    def fake_replay(rows,out,stage,total,initial):return 0
    base={'id':'a','task':1,'n':36,'arm':'coverage','checks':4,'visibility':'visible','attacker_pass':.1,'kind':'pilot',
          'packet_hash':'fake','packet':{'skills':list(range(6)),'reports':[]},'answers':[1]*6,'expected':{str(s):None for s in range(6)},'graph_metrics':{}}
    assignments=[dict(base,id=str(i)) for i in range(20)]
    class Broken:
     def call(self,packet,call_id):raise provider.CallFailure('injected_failure')
    with tempfile.TemporaryDirectory() as td:
     path=Path(td)/'out'
     with patch.object(study,'assignments',return_value=assignments),patch.object(render,'replay',fake_replay),patch.dict(os.environ,{'SYBIL_API_BUDGET_LEDGER':str(Path(td)/'ledger')}):
      with self.assertRaises(RuntimeError):worker.execute(study.params('S1'),path,backend=Broken())
     summary=json.loads((path/'summary.json').read_text())
     self.assertEqual(summary['terminal'],20);self.assertEqual(summary['invalid'],20)
     self.assertLessEqual(summary['started'],4);self.assertGreaterEqual(summary['not_started'],16)
     self.assertEqual(len({json.loads(line)['id'] for line in (path/'episodes.jsonl').read_text().splitlines()}),20)
 def test_fast_selection_matches_parent(self):
    # The tie-break shortcut must reproduce the frozen sybil-scale-api simulator exactly.
    path=study.ROOT.parent/'sybil-scale-api/src/sim.py';spec=importlib.util.spec_from_file_location('parentsim',path);old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
    for n in (36,108,324,972):
     for task in (4900,6000):
      for rate in (.1,.9):
       cfg=study.cfg_for(n);a=old.make_world(task,n//36,rate,False,cfg);b=sim.make_world(task,n//36,rate,False,cfg)
       self.assertEqual(a,b)
       self.assertEqual(old.checkpoints(a,[4,n//9],sim.ARMS,cfg),sim.checkpoints(b,[4,n//9],sim.ARMS,cfg))
    for node in ('n00','n1234'):
     for step in (1,977):self.assertEqual(old.rng(6001,'tie',step,node).random(),sim.tie_value(6001,step,node))
 def test_qualification_packet_size(self):
    for n in study.design()['sizes'][:2]:
     _,kind,world,recs=study.prepare((n,5000,.1,'qualification'))
     self.assertEqual([len(x) for _,x in recs],[n//2,n//2])
     self.assertEqual({world['public']['nodes'][x]['skill'] for x in recs[1][1]},{0,1,2})
     self.assertEqual({world['public']['nodes'][x]['skill'] for x in recs[0][1]},set(range(6)))
 def test_opus_request_and_settled_ledger(self):
    import io
    from unittest.mock import patch
    sent=[]
    class Resp(io.BytesIO):
     def __enter__(self):return self
     def __exit__(self,*a):return False
    def opener(request,timeout):
     body=json.loads(request.data);sent.append((request.full_url,body))
     if request.full_url.endswith('count_tokens'):return Resp(json.dumps({'input_tokens':1000}).encode())
     return Resp(json.dumps({'model':study.design()['model'],'stop_reason':'end_turn','usage':{'input_tokens':1000,'output_tokens':300},
       'content':[{'type':'thinking','thinking':'','signature':'x'},{'type':'text','text':json.dumps({'values':{str(i):None for i in range(6)}})}]}).encode())
    with tempfile.TemporaryDirectory() as td,patch.dict(os.environ,{'SWARM_MODEL_API_KEY':'k','SWARM_MODEL_WORKSPACE_ID':'w'}):
     ledger=provider.Ledger(Path(td)/'ledger');api=provider.Anthropic(ledger,opener)
     answer,acct=api.call({'skills':list(range(6)),'reports':[]},'c1')
     self.assertEqual(answer['values']['0'],None)
     msg=sent[-1][1];self.assertNotIn('temperature',msg);self.assertNotIn('thinking',msg)
     self.assertEqual(msg['model'],'claude-opus-5-5');self.assertEqual(msg['output_config']['effort'],'low')
     self.assertNotIn('max_tokens',sent[0][1])
     b=study.design()['budget'];self.assertEqual(acct['actual_usd'],(1000*b['input_usd_per_million']+300*b['output_usd_per_million'])/1e6)
     # Settled calls count actual cost, open reservations their full amount.
     ledger.transact({'type':'reserve','call_id':'open','micro_usd':5})
     total=int(b['aggregate_usd']*1e6)-int(acct['actual_usd']*1e6)-5
     ledger.transact({'type':'reserve','call_id':'fits','micro_usd':total})
     with self.assertRaises(provider.CallFailure):ledger.transact({'type':'reserve','call_id':'over','micro_usd':1})
if __name__=='__main__':unittest.main()
