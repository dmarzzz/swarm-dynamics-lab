import json,sys,unittest,copy
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE/'analysis'))
import scale_decision as sd,scale_qualification as sq
from study import scripted
class DecisionTests(unittest.TestCase):
 def fixtures(self,p):
  rows=[]
  for i in p['requests']:
   o=json.loads(i['wire_body']['messages'][1]['content']);o['documents']=sq.compact_docs(sq.saved()[i['case_id']][0]['request']['observation']['documents']);a=scripted(o);r=o['verified_report'];checks=r['candidate_checks'];eligible={n:all(checks[n][f]=='PASS' for f in sq.tp.FIELDS) for n in o['candidates']};minimum=min((r['arithmetic'][n]['total_usd'] for n in eligible if eligible[n]),default=None);a['decision_table']={n:{'eligible':eligible[n],'within_cost_tolerance':bool(eligible[n] and r['arithmetic'][n]['total_usd']<=minimum*1.03)} for n in eligible};rows.append({'status':'valid','answer':a})
  return {'assignments':rows,'usage_missing':0}
 def test_table_and_decision_must_both_pass(self):
  p=sd.build('SD-LUNA');s=self.fixtures(p);self.assertTrue(sd.grade(p,s)['qualified']);s['assignments'][2]['answer']['choice']='DEFER';self.assertFalse(sd.grade(p,s)['qualified'])
 def test_wrong_table_rejected_scientifically(self):
  p=sd.build('SD-SOL');s=self.fixtures(p);s['assignments'][0]['answer']['decision_table']['Aster']['eligible']=True;self.assertFalse(sd.grade(p,s)['qualified'])
 def test_frozen_bounds_and_no_answer_leak(self):
  for stage in sd.MODELS:
   p=sd.build(stage);self.assertEqual(p,json.loads((BASE/f'reviews/{stage}-packet.json').read_text()))
   for i in p['requests']:
    self.assertLessEqual(i['wire_bytes'],9216);obs=json.loads(i['wire_body']['messages'][1]['content']);self.assertNotIn('decision_table',obs);self.assertNotIn('evaluator',obs)
 def test_duplicate_json_never_salvaged(self):
  p=sd.build('SD-LUNA');s=self.fixtures(p);i=p['requests'][0];a=s['assignments'][0]['answer'];r={'route':{'provider':'OpenAI','model':i['wire_body']['model']},'tool_calls':None,'content':[{'type':'text','text':json.dumps(a)+'garbage'+json.dumps(a)}]}
  with self.assertRaises(ValueError):sd.validator(i)(r)
