"""Retrospective same-author audit of saved matched-roster artifacts; no model calls."""
import json,pathlib,argparse
from tasks import generate,digest
parser=argparse.ArgumentParser()
parser.add_argument("--results",type=pathlib.Path,required=True)
parser.add_argument("--verification",type=pathlib.Path,required=True)
parser.add_argument("--output",type=pathlib.Path,required=True)
args=parser.parse_args()
base=args.results
verification=json.loads(args.verification.read_text());assert verification['readback_passed']
rows=[]
for f in sorted(base.glob('*/outcome.json')):
 r=json.loads(f.read_text());a=r['assignment'];assert r['configured_n']==a['n'] and len(r['used_contexts'])==a['n']
 trace=[json.loads(l) for l in (f.parent/'trace.jsonl').read_text().splitlines()];charges=[e for e in trace if e['kind']=='charge']
 assert len(charges)==18 and sum(e['microdollars'] for e in charges)==r['exposure_microdollars']
 # Reference arithmetic audit reconstructed from public records, separately from evaluator truth.
 # Same author, retrospective derived analysis; not an independent experimental observation.
 task=generate('evidence',a['structure'],a['root']);pub=task.public;assert digest(pub)==a['public_task_sha256']
 exact={};local_errors=[];wrong=[]
 for j,item in enumerate(pub['items']):
  prev=pub['dependencies'][item]
  records=pub['records'];parent=exact[prev[0]] if prev else records['opening'];val=parent*records['a_'+str(j)]+records['b_'+str(j)];exact[item]=val
  observed=r['work_artifacts'][item]['value'];incoming=r['work_artifacts'][prev[0]]['value'] if prev else records['opening']
  if observed!=incoming*records['a_'+str(j)]+records['b_'+str(j)]:local_errors.append(item)
  if observed!=val:wrong.append(item)
 assert len(wrong)==r['stage_diagnostics']['worker_wrong_values']
 match=next(x for x in verification['results'] if x['run'].endswith('/'+f.parent.name))
 rows.append({'run':match['run'],'root':a['root'],'structure':a['structure'],'n':a['n'],'quality':r['evaluation']['quality'],'success':r['operational_success'],'elapsed_s':r['elapsed_s'],'cost_microdollars':r['exposure_microdollars'],'prompt_tokens':sum(e['prompt_tokens'] for e in charges),'completion_tokens':sum(e['completion_tokens'] for e in charges),'calls':len(charges),'local_arithmetic_mismatch_items':local_errors,'wrong_value_items':wrong,'peak_work_concurrency':match['peak_work_concurrency'],'public_task_sha256':a['public_task_sha256']})
assert len(rows)==8
pairs=[]
for root in (4,5):
 for structure in ('parallel','chain'):
  a,b=[next(r for r in rows if (r['root'],r['structure'],r['n'])==(root,structure,n)) for n in (1,2)];assert a['public_task_sha256']==b['public_task_sha256']
  pairs.append({'root':root,'structure':structure,'n1':a,'n2':b,'quality_delta':b['quality']-a['quality'],'latency_delta_s':b['elapsed_s']-a['elapsed_s'],'latency_reduction_fraction':1-b['elapsed_s']/a['elapsed_s'],'cost_reduction_fraction':1-b['cost_microdollars']/a['cost_microdollars']})
result={'attempt':'q-a6','source':'3331c6c6083caf1f69ccfdac4d5faa704c94c183','independent_roots':2,'assigned_started_terminal_graded_analyzed':8,'pairs':pairs,'model_calls':sum(r['calls'] for r in rows),'prompt_tokens':sum(r['prompt_tokens'] for r in rows),'completion_tokens':sum(r['completion_tokens'] for r in rows),'new_settled_microdollars':sum(r['cost_microdollars'] for r in rows),'cumulative_ledger':verification['ledger'],'readback_passed':True,'quality_claim':'Exploratory paired observations only; no population estimate or optimal N.'}
p=args.output;p.mkdir(parents=True,exist_ok=True);(p/'analysis.json').write_text(json.dumps(result,indent=2)+'\n');(p/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='pairs'}))
for x in pairs:print(x['root'],x['structure'],'quality',x['n1']['quality'],x['n2']['quality'],'latency_reduction',round(x['latency_reduction_fraction']*100,2),'cost_reduction',round(x['cost_reduction_fraction']*100,2),'local_errors',[len(x[n]['local_arithmetic_mismatch_items']) for n in ('n1','n2')])
