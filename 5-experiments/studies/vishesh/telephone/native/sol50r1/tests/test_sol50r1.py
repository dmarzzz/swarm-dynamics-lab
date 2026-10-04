import json,sqlite3,sys,tempfile,time,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from corpus import actor,questions,controls,reference,assignments,canonical,sha
from contract import request,parse,MODEL,PER
from native import packet,Runner,ExistingLedger,release_unstarted
from prepare import envelope
class Sol50(unittest.TestCase):
 def test_labels_controls_and_copy(self):
  self.assertEqual([reference(actor(),q) for q in questions().values()],['RELEASE','HOLD','INSUFFICIENT'])
  for c in controls():self.assertEqual(reference(c['actor'],c['question']),c['expected'])
 def test_serial_forks_no_answer_forwarding(self):
  aa=assignments();ww=[a for a in aa if a['role']=='writer'];rr=[a for a in aa if a['role']=='reader'];self.assertEqual(len(ww),50);self.assertEqual(len(rr),24);self.assertEqual(len({a['id'] for a in aa}),74)
  for i,w in enumerate(ww):self.assertEqual(w['parent'],None if i==0 else ww[i-1]['id'])
  for hop in (1,10,25,50):
   for site in questions():
    pair=[a for a in rr if a['hop']==hop and a['case_id']==site];self.assertEqual({a['parent'] for a in pair},{f'w{hop:02}'});self.assertEqual({a['arm'] for a in pair},{'P','R'})
  prev={'handoff':'text'};w=json.loads(request('P',actor(),prev)['messages'][1]['content']);self.assertEqual(w,{'previous_handoff':prev})
  for bad in ({'handoff':'text','decision':'GO'},{'handoff':'text','answer':'RELEASE'}):
   with self.assertRaises(ValueError):parse(canonical(bad),'writer')
 def test_envelope_and_qualifiers(self):
  e=envelope();self.assertEqual(e['max_calls'],77);self.assertEqual(e['additional_max_nano'],3877008077);self.assertEqual(e['cumulative_max_nano'],4550204746)
  for cid,q in packet()['qualification'].items():self.assertEqual(reference(q['actor'],q['question']),{'q01':'RELEASE','q02':'HOLD','q03':'INSUFFICIENT'}[cid])
 def test_failure_retains_unknown_and_releases_only_unstarted(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);db=sqlite3.connect(root/'ledger');db.executescript('CREATE TABLE authority(cap INTEGER,ref TEXT); CREATE TABLE charges(id TEXT PRIMARY KEY,stage TEXT,kind TEXT,reserve INTEGER,actual INTEGER,status TEXT,source TEXT); INSERT INTO authority VALUES(50000000000,"mock");');db.commit();db.close();l=ExistingLedger(root/'ledger');p=packet();calls=[]
   def fail(cid,req):calls.append(cid);raise RuntimeError('fixture')
   r=Runner(p,root/'out',l,fail,time.time()+600);r.qualify();self.assertEqual(calls,['q01']);self.assertEqual(len(release_unstarted(p,r.out,l,True)),76);self.assertEqual(l.db.execute("SELECT actual,status FROM charges WHERE id='Sol50R1:q01'").fetchone(),(None,'unknown'))
   with self.assertRaises(ValueError):l.reserve(p)
   l.db.close()
if __name__=='__main__':unittest.main()
