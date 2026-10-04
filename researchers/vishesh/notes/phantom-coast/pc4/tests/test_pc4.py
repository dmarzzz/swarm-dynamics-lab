import unittest,tempfile,json,sys,copy,sqlite3
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from contract import *
from design import *
from wire import request,validate,reservation,failure_code
from engine import Engine
from ledger import Ledger

def raw(req):
    m=reconstruct(req['state']);return dict(model='typesafe/jev-1.13-20260917',provider='TypeSafe',answers={k:dict(type='choice',choice=m[k.removeprefix('cell_').replace('_',',')],probabilities={v:float(v==m[k.removeprefix('cell_').replace('_',',')]) for v in q['criteria']},confidence=1) for k,q in req['questions'].items()},usage=dict(cost=.0001,input_tokens=100,output_tokens=0))

class Tests(unittest.TestCase):
 def test_world_balance_and_paths(self):
  for seed in range(1200,1208):
   w=development_world(seed,family(seed));self.assertEqual(sum(v=='LAND' for v in w['truth'].values()),12);self.assertEqual(sum(w['truth'][c]=='LAND' for c in w['region']),2)
   for policy in ('q0','q2','q4','uniform'):
    paths=[]
    for false in (0,2,4):
     p,path=packet(w,policy,false);paths.append(path);self.assertEqual(len(set(path)),12)
     if policy!='uniform':self.assertEqual(len(set(path)&set(w['region'])),int(policy[1]))
     reports=p['evidence']['observations'][:4];self.assertEqual(sum(r['label']!=w['truth'][r['cell']] for r in reports),false)
    self.assertEqual(paths[0],paths[1]);self.assertEqual(paths[1],paths[2])
 def test_no_operator_context(self):
  p,_=packet(development_world(1200),'q2',4);self.assertEqual(set(p),{'task','actor','cells','evidence'});self.assertFalse(any(k in json.dumps(p) for k in ('seed','quota','false_count','legal_cells','previous_proposals','truth')))
 def test_qualification_precedence_and_unknown(self):
  w=development_world(1200)
  for case,n in [('complete',0),('partial',24)]:
   p=clean_packet(w,0,case);m=reconstruct(p);self.assertEqual(sum(v=='UNKNOWN' for v in m.values()),n);self.assertEqual(error(m,w['truth'])['wrong'],0)
 def test_schedule(self):
  self.assertEqual(len(schedule('Q0')),24);self.assertEqual(len(schedule('S1')),1152);self.assertEqual(len({a['id'] for a in schedule('S1')}),1152);self.assertEqual(len(STAGES['S1']),32)
 def test_contract_codes(self):
  req=request(packet(development_world(1200),'q2',4)[0],'map');a=raw(req);self.assertIn('map',validate(a,req)['result'])
  for mode,code in [('mass','probability_mass'),('maximum','selected_maximum'),('confidence','confidence')]:
   x=copy.deepcopy(a);ans=next(iter(x['answers'].values()))
   if mode=='mass':ans['probabilities']={k:0. for k in ans['probabilities']}
   elif mode=='maximum':ans['choice']=next(k for k,v in ans['probabilities'].items() if v==0)
   else:ans['confidence']=float('nan')
   with self.assertRaises(ValueError) as exc:validate(x,req)
   self.assertEqual(failure_code(exc.exception),code)
  self.assertEqual(failure_code(ValueError('secret-test-sentinel')),'ValueError')
 def test_quorum_and_missing(self):
  w=development_world(1200);p,_=packet(w,'q4',4);m=reconstruct(p);rs=[dict(status='valid',checked=dict(result=dict(map=m))) for _ in range(3)];rs[0]={'status':'invalid'};self.assertEqual(endpoint(w,p,rs)['whole']['wrong'],0);rs[1]={'status':'invalid'};self.assertEqual(endpoint(w,p,rs)['whole']['missing'],36)
 def test_ledger_cumulative_and_duplicates(self):
  with tempfile.TemporaryDirectory() as d:
   l=Ledger(Path(d)/'l.sqlite','a'*64);self.assertEqual(l.summary()['prior_usd'],.574334208);l.reserve('a',48384000);l.finish('a');self.assertAlmostEqual(l.summary()['cumulative_exposure_usd'],.622718208)
   with self.assertRaises(sqlite3.IntegrityError):l.reserve('a',1)
   l.db.execute('UPDATE authority SET prior=0');l.db.commit();l.db.close()
   with self.assertRaises(ValueError):Ledger(Path(d)/'l.sqlite','a'*64)
 def test_engine_journal_and_recomputed_outcomes(self):
  with tempfile.TemporaryDirectory() as d:
   d=Path(d);l=Ledger(d/'l.sqlite','a'*64);w={1200:development_world(1200),1201:development_world(1201,'scattered')};e=Engine('S1','test',d/'out',l,raw,w);result=e.run();self.assertEqual(result['valid'],72);self.assertEqual(result['complete_episodes'],24)
   es=json.loads((d/'out/episodes.json').read_text());self.assertTrue(all(x['endpoint']['whole']==x['endpoint']['deterministic'] for x in es));events=[json.loads(x) for x in (d/'out/events.jsonl').read_text().splitlines()];self.assertEqual(sum(x['kind']=='call-start' for x in events),72);self.assertEqual(sum(x['kind']=='sensing' for x in events),288);l.db.close()
 def test_failed_stage_preserves_assignments(self):
  with tempfile.TemporaryDirectory() as d:
   d=Path(d);l=Ledger(d/'l.sqlite','a'*64)
   def fail(req):raise TimeoutError()
   e=Engine('S1','test',d/'out',l,fail,{1200:development_world(1200)});s=e.run();self.assertEqual(s['started'],5);self.assertEqual(s['assigned'],36);self.assertEqual(s['stop_reason'],'five_consecutive_failures');es=json.loads((d/'out/episodes.json').read_text());self.assertTrue(any(x['path']==[] for x in es));self.assertFalse(s['overall']['practical_success']);l.db.close()
 def test_development_guard(self):
  for seed in (800,1000,1300,1400):
   with self.assertRaises(ValueError):development_world(seed)
if __name__=='__main__':unittest.main()
