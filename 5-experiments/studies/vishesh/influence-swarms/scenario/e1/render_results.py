from pathlib import Path
import json,sys
root=Path(__file__).resolve().parents[6];s=root/'researchers/vishesh/notes/influence-swarms/scenario';sys.path.insert(0,str(s/'e1'));import acquisition as p
out=root/'data/influence-native/native-E1-E0-01';rows=json.loads((out/'records.json').read_text());cases={x['id']:x for x in json.loads((s/'b2/dossiers.json').read_text())};summary=json.loads((out/'summary.json').read_text());assessment=json.loads((out/'assessment.json').read_text());data={'summary':summary,'bounds':assessment['missingness_bounds'],'cases':{},'cells':[]};frames=[];roles=['Cost','Capability','Deployment','Evidence']
for r in rows:
 case=cases[r['case_id']];g=p.i.labels(case);data['cases'][r['case_id']]={'family':case['family'],'context':case['brief']['context'],'acceptable':g['acceptable'],'prices':{k:v['cost_usd'] for k,v in g['candidates'].items()}}
 answers=[]
 for a in r['answers']:
  score=p.i.score(case,a);answers.append({'ranking':a['ranking'],'checks_correct':score['checks_correct'],'costs_correct':score['costs_correct'],'action':a.get('action'),'choice':a.get('choice'),'acceptable':score['acceptable_action'] if 'action'in a else None,'unsupported':score['unsupported_clearance'],'source_position':a['source_position']})
 cell={k:r[k] for k in ('case_id','arm','condition','repetition','execution')};cell['answers']=answers;data['cells'].append(cell)
 for step in range(3 if r['arm']=='simple' else 10):
  started_count=len(answers)+(1 if r['execution']=='format_failed' else 0)
  nodes=[{'id':'source','label':'Source','state':'available'}];edges=[];simple=r['arm']=='simple';n=1 if simple else 4
  for j in range(n):
   initial=answers[j] if len(answers)>j and step>j else None;rev_index=j+4;rev=answers[rev_index] if not simple and len(answers)>rev_index and step>rev_index else None;a=rev or initial;requested=step>rev_index and not simple;failed=requested and not rev
   nodes.append({'id':f'adviser-{j}','label':'Analyst' if simple else roles[j]+' adviser','state':'revision_missing' if failed else 'revised' if rev else 'initial' if initial else 'unobserved','rank':a['ranking'][0] if a else None,'ranking':a['ranking'] if a else None,'previous_ranking':initial['ranking'] if rev and initial else None,'previous_rank':initial['ranking'][0] if rev and initial else None,'changed':bool(rev and initial and rev['ranking']!=initial['ranking']),'checks_correct':a['checks_correct'] if a else None,'costs_correct':a['costs_correct'] if a else None})
   if step>j and started_count>j:edges.append({'from':'source','to':f'adviser-{j}','kind':'evidence'})
  final_index=1 if simple else 8;final=answers[final_index] if len(answers)>final_index and step>final_index else None
  nodes.append({'id':'chair','label':'Decider','state':'observed' if final else 'missing' if step>final_index else 'unobserved','action':final['action'] if final else None,'choice':final['choice'] if final else None,'acceptable':final['acceptable'] if final else None})
  if step>final_index and started_count>final_index:
   edges.append({'from':'source','to':'chair','kind':'evidence'})
   edges.extend({'from':f'adviser-{j}','to':'chair','kind':'report'} for j in range(n) if nodes[j+1]['state']!='unobserved')
  if not simple and 5<=step<=8 and r['arm']=='peer' and started_count>=step:edges.extend({'from':f'adviser-{j}','to':f'adviser-{step-5}','kind':'peer_report'} for j in range(4) if j!=step-5)
  frames.append({'kind':'influence','case_id':r['case_id'],'family':case['family'],'condition':r['condition'],'arm':r['arm'],'repetition':r['repetition']+1,'step':step,'stage':'Source evidence' if step==0 else 'Final decision' if step>final_index else 'Initial assessments' if simple or step<=4 else 'Reconsideration','nodes':nodes,'edges':edges,'accepted_choices':g['acceptable'],'counts':{'assigned':288,'complete':285,'unsafe_purchases':5,'missing':3},'note':'Recorded output states; edges show actual input availability, not inferred persuasion. E1 Decider also receives raw evidence.'})
base=Path(__file__).resolve().parent;(base/'visual-data.json').write_text(json.dumps(data,separators=(',',':')));(base/'replay.json').write_text(json.dumps({'schema_version':1,'kind':'influence','frames':frames,'provenance':{'run':'influence-swarms/1004-230027-930fec','source':'9eaa1d3188128f0411a0d5e10b02181575c90049','projection':'categorical saved-output states; no raw model prose','time_axis':'logical stage, not wall clock','public_name_mapping':{'chair':'Decider'}}},separators=(',',':')));print(json.dumps({'cells':len(data['cells']),'frames':len(frames),'raw_prose':False}))

page=(base/"visual-template.html").read_text().replace("__DATA__",(base/"visual-data.json").read_text().replace("<","\\u003c"))
(base/"results.html").write_text(page)
