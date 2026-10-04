import hashlib,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import ledger,native,runner
from packet import roots,packet,assignments,request as scientific_request,exact
class AdmissionStub:
 def __init__(self,*args):self.public={"fixture":True}
 def current(self):return True
class Tests(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory();self.b=Path(self.t.name);self.prior=self.b/'prior';self.prior.write_bytes(b'unchanged archival fixture');self.patch=patch.object(ledger,'PREDECESSOR',hashlib.sha256(self.prior.read_bytes()).hexdigest());self.patch.start();self.l=ledger.Ledger(self.b/'budget',self.prior);self.l.claim();self.p=packet(roots('adapter-test')[0],True,'copies','linked',False)
 def tearDown(self):self.l.db.close();self.patch.stop();self.t.cleanup()
 def response(self,**changes):
  r=dict(model='openai/gpt-6-sol',provider='OpenAI',usage=dict(cost=.001,prompt_tokens=350,completion_tokens=12),choices=[dict(finish_reason='stop',message=dict(content=json.dumps(dict(p=exact(self.p))))) ]);r.update(changes);return r
 def test_exact_request(self):self.assertEqual(native.request(self.p),scientific_request(self.p))
 def test_wrong_route_and_output_rejected(self):
  for changes in [dict(provider='Other'),dict(model='other-model'),dict(choices=[dict(finish_reason='length',message=dict(content='{"p":0.6}'))])]:
   with self.assertRaises(ValueError):native.decode(self.response(**changes),self.p)
  for value in ['{"p":NaN}','{"p":true}','{"p":0.4,"p":0.6}','{"p":0.6,"label":"LAND"}']:
   with self.assertRaises(ValueError):native.decode(self.response(choices=[dict(finish_reason='stop',message=dict(content=value))]),self.p)
 def test_usage_bounds(self):
  for usage in [dict(cost=.01,prompt_tokens=350,completion_tokens=12),dict(cost=.001,prompt_tokens=1665,completion_tokens=12),dict(cost=.001,prompt_tokens=350,completion_tokens=33),dict(cost=.001,prompt_tokens=350,completion_tokens=12,completion_tokens_details=dict(reasoning_tokens=1))]:
   with self.assertRaises(ValueError):native.decode(self.response(usage=usage),self.p)
 def test_ledger_amendment_and_old_uncertainty(self):
  self.assertEqual(self.l.summary()['cumulative_exposure_nano'],1598553490);self.assertEqual(self.l.db.execute('SELECT id FROM amendments').fetchone()[0],'PI-FUND-20261004-02');self.l.reserve('a',4480000);self.l.finish('a',1000000);self.assertEqual(self.l.summary()['cumulative_exposure_nano']-self.l.summary()['cumulative_known_nano'],12096000)
 def test_budget_800_and_no_second_claim(self):
  for i in range(800):self.l.reserve(str(i),4480000)
  with self.assertRaises(ValueError):self.l.reserve('801',4480000)
  with self.assertRaises(Exception):self.l.claim()
  self.assertEqual(self.l.summary()['cumulative_exposure_nano'],5182553490)
 def test_started_batch_reconciles_after_invalid(self):
  a=runner.Actor(self.l,lambda bodies:[self.response(),dict(transport_error=True),self.response()],self.b,AdmissionStub());rows=a.collect([(str(i),self.p) for i in range(3)]);self.assertEqual([r['status'] for r in rows],['valid','failed','valid']);a.collect([('later',self.p)]);self.assertEqual(a.records[-1]['status'],'unstarted');self.assertEqual(self.l.summary()['calls'],3);self.assertEqual(self.l.summary()['cumulative_exposure_nano'],1598553490+6480000)
 def test_reviewed_semantic_hashes(self):
  for name,sha in runner.REVIEWED.items():self.assertEqual(hashlib.sha256((runner.ROOT/name).read_bytes()).hexdigest(),sha)
 def test_qualification_gate_and_complete_scripted_replay(self):
  ws=roots('adapter-scripted');m=self.b/'manifest.json';m.write_text(json.dumps(dict(roots=ws,assignments=assignments(ws))))
  for qualified in (False,True):
   count=[0]
   def transport(bodies):
    count[0]+=len(bodies);out=[]
    for body in bodies:
     p=json.loads(body['messages'][1]['content']);r=self.response();r['choices'][0]['message']['content']=json.dumps(dict(p=exact(p) if qualified else .5));out.append(r)
    return out
   c=dict(manifest=str(m),ledger=str(self.b/('ledger'+str(qualified))),predecessor=str(self.prior),output=str(self.b/('out'+str(qualified))),source_commit='fixture',decision='PI-FUND-20261004-02')
   with patch.object(runner,'Admission',AdmissionStub),patch.object(runner,'write',lambda *args:None):result=runner.run(c,transport,lambda *args:{},lambda *args:None)
   self.assertEqual(count[0],800 if qualified else 32);self.assertEqual(result['qualification']['qualification_passed'],qualified);self.assertEqual(result['analysis']['primary'],0 if qualified else None)
if __name__=='__main__':unittest.main()
