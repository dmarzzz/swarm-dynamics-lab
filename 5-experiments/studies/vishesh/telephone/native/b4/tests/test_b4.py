import copy,json,sqlite3,sys,tempfile,time,unittest,threading
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from corpus import cases,reference,ablations,assignments,canonical,sha
from contract import request,MODEL
from native import packet,Runner,ExistingLedger,release_unstarted
from report import analyze
from prepare import envelope
class B4(unittest.TestCase):
 def test_labels_and_offline_ablations(self):
  for c in cases():
   self.assertEqual(reference(c['actor'],c['question']),c['gold']['answer'])
   p=copy.deepcopy(c['actor']);p['records'].reverse();self.assertEqual(reference(p,c['question']),c['gold']['answer'])
   for a in ablations(c):self.assertNotEqual(reference(a['actor'],c['question']),'RELEASE')
  for f in {c['family'] for c in cases()}:self.assertEqual(sorted(c['gold']['answer'] for c in cases() if c['family']==f),['HOLD','INSUFFICIENT','RELEASE'])
 def test_identical_parent_fork_and_hidden_question(self):
  aa=assignments();self.assertEqual(len(aa),90)
  for chain in {a['chain'] for a in aa}:
   rr=[a for a in aa if a['chain']==chain and a['role']=='reader'];self.assertEqual(len(rr),2);self.assertEqual(rr[0]['parent'],rr[1]['parent'])
  c=cases()[0];prev={'handoff':'source prose GO','decision':'GO'}
  self.assertNotIn('question',json.loads(request('P',c['actor'],prev)['messages'][1]['content']))
  pp=json.loads(request('P',c['actor'],prev,c['question'])['messages'][1]['content']);rr=json.loads(request('R',c['actor'],prev,c['question'])['messages'][1]['content']);self.assertEqual(pp['handoff_text'],rr['handoff_text']);self.assertNotIn('decision',pp);self.assertNotIn('source_packet',pp)
 def test_exact_resource_bound(self):self.assertEqual(envelope()['max_calls'],92);self.assertEqual(envelope()['additional_max_nano'],3170448092)
 def test_native_roundtrip_same_handoff_and_reporting(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);db=sqlite3.connect(root/'ledger');db.executescript('CREATE TABLE authority(cap INTEGER,ref TEXT); CREATE TABLE charges(id TEXT PRIMARY KEY,stage TEXT,kind TEXT,reserve INTEGER,actual INTEGER,status TEXT,source TEXT); INSERT INTO authority VALUES(50000000000,"mock");');db.commit();db.close();ledger=ExistingLedger(root/'ledger');p=packet();calls=[];lock=threading.Lock()
   def generate(cid,req):
    with lock:calls.append(cid)
    v=json.loads(req['messages'][1]['content']);time.sleep(.001)
    if cid in ('q01','q02'):obj={'answer':'RELEASE' if cid=='q01' else 'INSUFFICIENT','evidence':'mock'}
    elif 'question' in v:
     src=v.get('source_packet') or {'records':[{'text':line} for line in v['handoff_text'].splitlines()]};obj={'answer':reference(src,v['question']),'evidence':'mock source-rule answer'}
    else:obj={'handoff':'\n'.join(r['text'] for r in v['source_packet']['records']) if 'source_packet' in v else v['previous_handoff']['handoff'],'decision':'GO'}
    return {'id':'mock-'+cid,'provider':'OpenAI','model':MODEL,'choices':[{'finish_reason':'stop','message':{'role':'assistant','content':canonical(obj)}}],'usage':{'prompt_tokens':100,'completion_tokens':100,'total_tokens':200,'cost':.0012}}
   runner=Runner(p,root/'out',ledger,generate,time.time()+600);runner.qualify();review={'manifest_sha256':p['manifest_sha256'],'assessor':'offline fixture','responses':{}}
   for cid in ('q01','q02'):review['responses'][cid]={'response_sha256':sha(json.loads((runner.out/(cid+'.response.json')).read_text())),'evidence_supported':True,'rationale':'mock'}
   result=runner.main(review);self.assertEqual(result['valid'],90);self.assertEqual(len(calls),92)
   for block in (1,2):
    for c in cases():
     reqs=[json.loads((runner.out/f'b{block}-{c["id"]}-reader-{a}.request.json').read_text()) for a in ('P','R')];vv=[json.loads(r['messages'][1]['content']) for r in reqs];self.assertEqual(vv[0]['handoff_text'],vv[1]['handoff_text'])
   report=analyze(p,runner.out,{c['id']:c['gold'] for c in cases()});self.assertEqual(len(report['audit_required_ids']),36);self.assertTrue(all(x['correct']==9 for x in report['cells']))
   with self.assertRaises(ValueError):runner.main(review)
   ledger.db.close()
if __name__=='__main__':unittest.main()
