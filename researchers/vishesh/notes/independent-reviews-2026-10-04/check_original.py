"""Reviewer-owned offline checks; development fixtures only, no external providers."""
import copy, json, sys, tempfile
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'researchers/dmarz/notes/discussion-dose/src'))
from tasks import make_world, document, independent_answer, validate_world
from sim import Runner, DEFAULT_CFG, run_episode, arms_for, evaluate
from providers import Scripted
from analyze import contrast,summarize
from worker import execute_bundle
from audit import audit

out={}
# Literal answers derived by reviewer from public registry text, not expected labels.
keys=[('C','B','B.power',5,9,4),('C','A','A.freight',35,30,3),('A','B','B.transfer',6,3,1),('A','C','C.power',12,18,4),('A','B','B.freight',49,41,2),('B','A','A.transfer',3,1,2)]
for i,(answer,target,key,true,false,delta) in enumerate(keys):
 w=make_world(i)
 assert independent_answer(w)==answer
 assert w['target']==target and w['target_key']==key and w['false_value']==false
 assert document(w,'audit')['facts'][key]==true and w['followup_delta']==delta
 a=document(w,'digest');b=document(w,'digest',True)
 a['facts'][key]=false;a['text']=b['text'];assert a==b
out['six_manual_keys']='pass'
w=make_world(0);bad=copy.deepcopy(w);bad['false_value']=5
try:validate_world(bad);out['noop_attack']='MISSED'
except AssertionError:out['noop_attack']='detected'
# Wrong reference label is rejected by an independent literal answer.
with patch('sim.independent_answer',return_value='A'):
 row=run_episode(0,1,'',1,arms_for((0,)),{},Scripted())[0]
 out['wrong_answer_checker_mutation']={'saved_correct':row['evaluation']['correct'],'literal_expected':1,'detected_by_reviewer':row['evaluation']['correct']!=1}
# All documents on one participant is not rejected by the acquisition layer.
with patch('sim.allocation',return_value=([[d['id'] for d in w['docs']],[],[]],0)):
 snapshot=Runner(Scripted(),DEFAULT_CFG).acquire(w,1,True)
 out['bad_allocation']={'rejected_by_runtime':False,'initial_document_counts':[len(s['documents'])-3 for s in snapshot['states']],'reviewer_detects_changed_initial_partition':True}
# Existing replay detects tampering in terminal scoring.
with tempfile.TemporaryDirectory() as t:
 p=Path(t)/'bundle';execute_bundle({'tasks':[0],'seeds':[1],'rounds':[0,1],'n_agents':3,'stage':'S0'},p,Scripted())
 out['baseline_replay']=audit(p)
 rows=[json.loads(l) for l in (p/'episodes.jsonl').read_text().splitlines()]
 rows[0]['evaluation']['correct']=0
 (p/'episodes.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in rows))
 try:audit(p);out['score_tamper']='MISSED'
 except AssertionError as e:out['score_tamper']=str(e)
# A whole missing task block is invisible to the standalone analyzer.
rows=run_episode(0,1,'',1,arms_for(),{},Scripted())+run_episode(1,1,'',1,arms_for(),{},Scripted())
out['whole_world_omission']={'before_clusters':contrast(rows)['task_clusters'],'after_clusters':contrast([r for r in rows if r['task_id']==0])['task_clusters'],'rejected':False}
# Ground-truth-correct guessing is not recorded as unsupported in the original scorer.
w=make_world(4);r=Runner(Scripted(),DEFAULT_CFG);res=r.continue_arm(w,r.acquire(w,1,False),0,'board')
res['memory']=[];res['followup']={'value':51}
ev=evaluate(w,res,2)
out['unsupported_correct_guess']={'followup_correct':ev['followup_correct'],'support_metric_present':any('support' in k or 'coverage' in k for k in ev)}
class Missing(Scripted):
 def complete(self,req):raise TimeoutError('offline missing response fixture')
failed=run_episode(0,1,'',1,arms_for(),{},Missing())
out['missing_responses']={'assigned':len(failed),'invalid':sum(r['evaluation']['invalid'] for r in failed),'contrast_bounds':contrast(failed)['invalid_outcome_bounds'],'all_cells_assigned_one':all(c['assigned']==1 for c in summarize(failed).values())}
path=Path(__file__).with_name('original-checks.json');path.write_text(json.dumps(out,indent=2)+'\n');print(path.read_text())
