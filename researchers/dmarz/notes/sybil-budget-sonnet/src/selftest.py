import importlib.util,json,tempfile,unittest,os
from pathlib import Path
from unittest.mock import patch
import study,sim,provider,render,analyze

class Tests(unittest.TestCase):
 def test_parent_runtime_parity(self):
    parent=study.ROOT.parent/'sybil-scale-api'
    self.assertEqual((parent/'src/sim.py').read_bytes(),(study.ROOT/'src/sim.py').read_bytes())
    spec=importlib.util.spec_from_file_location('oldprovider',parent/'src/provider.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
    self.assertEqual(old.SYSTEM,provider.SYSTEM);self.assertEqual(old.SCHEMA,provider.SCHEMA)
    for n in (324,972):
     cfg=study.cfg_for(n);w=sim.make_world(6800,n//36,.1,False,cfg)
     self.assertEqual(w,sim.make_world(6800,n//36,.1,False,cfg))
     now=sim.checkpoints(w,[4],study.design()['arms'],cfg)
     then=sim.run_episode(w,4,study.design()['arms'],cfg)
     for a,b in zip(now,then):self.assertEqual(a['admitted'],b['trace'][-1]['admitted']);self.assertEqual(a['graph_metrics'],b['evaluation'])
 def test_haiku_cohort_pairing(self):
    """Only model, prices, caps and the N972 size subset differ from sybil-budget-api."""
    parent=study.ROOT.parent/'sybil-budget-api'
    for name in ('sim.py','study.py','analyze.py'):
     self.assertEqual((parent/'src'/name).read_bytes(),(study.ROOT/'src'/name).read_bytes())
    import yaml
    old=yaml.safe_load((parent/'design.yaml').read_text());new=study.design()
    self.assertEqual(old['model'],'claude-haiku-4-5-20251001');self.assertEqual(new['model'],'claude-sonnet-4-6')
    self.assertEqual(old['sizes'],[324,972]);self.assertEqual(new['sizes'],[972])
    changed={k for k in set(old)|set(new) if old.get(k)!=new.get(k)}
    self.assertEqual(changed,{'experiment','model','sizes','budget','review_waiver','replication_of'})
    ob,nb=old['budget'],new['budget']
    self.assertEqual({k for k in ob if ob[k]!=nb[k]},{'aggregate_usd','max_attempted_calls','input_usd_per_million','output_usd_per_million'})
    spec=importlib.util.spec_from_file_location('parentstudy',parent/'src/study.py');ps=importlib.util.module_from_spec(spec);spec.loader.exec_module(ps)
    # One scientific and one qualification world here for speed; reporting/parity_check.py covers all.
    def one(mod,dd):
     dd=dict(dd);dd['worlds']=dd['worlds'][:1];dd['qualification_worlds']=dd['qualification_worlds'][:1];dd['sizes']=[972];return dd
    for stage in ('Q0','S1'):
     with patch.object(study,'design',return_value=one(study,new)):mine={a['id']:a for a in study.assignments(stage)}
     with patch.object(ps,'design',return_value=one(ps,old)):theirs={a['id']:a for a in ps.assignments(stage) if a['n']==972}
     self.assertEqual(len(mine),2 if stage=='Q0' else 60)
     self.assertEqual(set(mine),set(theirs))
     for k,a in mine.items():self.assertEqual(a['packet_hash'],theirs[k]['packet_hash']);self.assertEqual(a['expected'],theirs[k]['expected'])
 def test_blind_packet(self):
    w=sim.make_world(6800,9,.1,False,study.cfg_for(324));nodes=list(w['public']['nodes'])[:162]
    a=study.packet(w,nodes,[], 'visible','random');b=study.packet(w,nodes,[],'masked','random')
    for x,y in zip(a['reports'],b['reports']):
     self.assertEqual({k:v for k,v in x.items() if k!='verification'},y)
     self.assertEqual(set(x),{'node','skill','claim','age','activity','verification'})
    before=sim.select_check(w['public'],'coverage',set(),set(),[],6800,1)
    for v in w['truth'].values():v['honest']=not v['honest']
    self.assertEqual(before,sim.select_check(w['public'],'coverage',set(),set(),[],6800,1))
 def test_exact_check_counts_and_prefixes(self):
    w=sim.make_world(6800,9,.5,False,study.cfg_for(324))
    records=sim.checkpoints(w,study.design()['checks'],study.design()['arms'],study.cfg_for(324))
    self.assertEqual(len(records),12)
    for arm in study.design()['arms']:
     rr=[r for r in records if r['arm']==arm]
     for r in rr:
      self.assertEqual(len(r['checked']),r['checks']);self.assertEqual(len(set(r['checked'])),r['checks'])
      self.assertEqual(r['graph_metrics']['verification_calls'],r['checks'])
      self.assertEqual(r['events'],rr[-1]['events'][:r['checks']])
      self.assertFalse(set(r['checked'])&set(w['public']['trusted']))
 def test_qualification_noattack_missing_and_recompute(self):
    assignments=study.assignments('Q0');self.assertEqual(len(assignments),8)
    rr=[]
    for a in assignments:
     self.assertEqual(a['graph_metrics']['malicious_count'],0)
     answer=study.scripted(a['packet']);ev=study.evaluate(a,answer)
     self.assertTrue(ev['exact_packet']);self.assertEqual(ev['qualification_accuracy'],1)
     self.assertEqual(ev['specialist_retention'],1-ev['specialist_rejection'])
     if a['arm']=='common_only':self.assertEqual([answer['values'][str(i)] for i in (3,4,5)],[None]*3)
     rr.append(dict(a,status='completed',evaluation=ev))
    self.assertTrue(study.qualification(rr)['passed'])
    rr[0]['status']='failed';self.assertFalse(study.qualification(rr)['passed'])
 def test_accounting_duplicate_usd_and_call_cap(self):
    with tempfile.TemporaryDirectory() as td:
     ledger=provider.Ledger(Path(td)/'ledger');ledger.transact({'type':'reserve','call_id':'a','micro_usd':1})
     with self.assertRaises(provider.CallFailure):ledger.transact({'type':'reserve','call_id':'a','micro_usd':1})
     with self.assertRaises(provider.CallFailure):ledger.transact({'type':'reserve','call_id':'b','micro_usd':int(study.design()['budget']['aggregate_usd']*1e6)+1})
     d=study.design();d['budget']['max_attempted_calls']=1
     with patch.object(study,'design',return_value=d):
      with self.assertRaises(provider.CallFailure):ledger.transact({'type':'reserve','call_id':'b','micro_usd':1})
 def test_render_pending_failure_and_metric_mapping(self):
    self.assertEqual(render.frame([],2880,'S1').size,(1920,1440))
    self.assertEqual(render.frame([{'status':'failed','kind':'pilot','n':324}],2880,'S1').size,(1920,1440))
    rows=[dict(status='completed',kind='pilot',n=972,arm='coverage',checks=108,attacker_pass=.1,evaluation={'rare_accuracy':v}) for v in (1,2/3)]
    value,count=render.cell_values(rows,972,'coverage',108,.1,'rare_accuracy');self.assertAlmostEqual(value,5/6);self.assertEqual(count,2)
 def test_splits_grid_and_disabled_holdout(self):
    d=study.design();groups=[set(d[k]) for k in ('worlds','qualification_worlds','engineering_worlds')]
    self.assertTrue(all(not a&b for i,a in enumerate(groups) for b in groups[i+1:]));self.assertTrue(max(set.union(*groups))<10000)
    self.assertFalse(set.union(*groups)&set(range(4900,4902)));self.assertFalse(set.union(*groups)&set(range(5000,5004)));self.assertFalse(set.union(*groups)&set(range(6000,6024)))
    self.assertEqual(len(d['sizes'])*len(d['arms'])*len(d['checks'])*len(d['pilot']['attacker_pass'])*len(d['worlds']),1440)
    with self.assertRaises(ValueError):study.params('S2')
 def test_invalid_answers_and_duplicate_analysis(self):
    for vals in ({'0':True},{str(i):True for i in range(6)}):
     with self.assertRaises(ValueError):study.validate({'values':vals})
    with self.assertRaises(ValueError):analyze.analyze([{'id':'same'},{'id':'same'}])
 def test_concurrent_failure_denominator(self):
    import worker
    base=study.assignments('Q0')[0];assignments=[dict(base,id=str(i),kind='pilot',arm='coverage',checks=4,attacker_pass=.1) for i in range(20)]
    class Broken:
     def call(self,packet,call_id):raise provider.CallFailure('injected_failure')
    with tempfile.TemporaryDirectory() as td:
     path=Path(td)/'out'
     with patch.object(study,'assignments',return_value=assignments),patch.object(render,'replay',return_value=0),patch.object(analyze,'analyze',return_value={}),patch.dict(os.environ,{'SYBIL_API_BUDGET_LEDGER':str(Path(td)/'ledger')}):
      with self.assertRaises(RuntimeError):worker.execute(study.params('S1'),path,backend=Broken())
     summary=json.loads((path/'summary.json').read_text());self.assertEqual(summary['terminal'],20);self.assertEqual(summary['invalid'],20)
     self.assertLessEqual(summary['started'],study.design()['budget']['workers']);self.assertGreaterEqual(summary['not_started'],20-study.design()['budget']['workers'])
     self.assertEqual(len({json.loads(line)['id'] for line in (path/'episodes.jsonl').read_text().splitlines()}),20)
if __name__=='__main__':unittest.main()
