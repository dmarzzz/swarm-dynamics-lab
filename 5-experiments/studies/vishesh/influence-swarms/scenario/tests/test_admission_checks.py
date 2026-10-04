import copy,datetime,sys,unittest
from pathlib import Path
B=Path(__file__).resolve().parents[1];sys.path.insert(0,str(B/'analysis'))
from admission_checks import verify_claims,validate_envelope
class Admission(unittest.TestCase):
 def test_allocation_faults(self):
  now=datetime.datetime.now(datetime.timezone.utc);c={'running':{'status':'running','until':(now+datetime.timedelta(hours=1)).isoformat(),'shared':False,'by':'vishesh/codex-experiments','experiment':'influence-swarms','servers':['registered']}}
  def check(servers,claims):verify_claims(servers,claims,'registered','running','vishesh/codex-experiments',now)
  check({'registered':{}},c)
  with self.assertRaises(ValueError):check({},c)
  bad=copy.deepcopy(c);bad['conflict']=copy.deepcopy(c['running'])
  with self.assertRaises(ValueError):check({'registered':{}},bad)
  bad=copy.deepcopy(c);bad['running']['until']=(now-datetime.timedelta(seconds=1)).isoformat()
  with self.assertRaises(ValueError):check({'registered':{}},bad)
 def test_payload_allowlists(self):
  good={'secret':{'SWARM_MODEL_API_KEY':'fixture'},'routing':{'workspace_id':'wrkspc_fixture'}}
  def validator(v):
   if set(v)!= {'SWARM_MODEL_API_KEY'}:raise ValueError('bad')
  validate_envelope(good,validator)
  for bad in ({**good,'extra':1},{**good,'routing':{**good['routing'],'extra':1}},{**good,'secret':{**good['secret'],'extra':1}}):
   with self.assertRaises(ValueError):validate_envelope(bad,validator)
