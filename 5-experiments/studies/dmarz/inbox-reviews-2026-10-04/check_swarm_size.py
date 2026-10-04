"""Reviewer derives solutions from public packets; qualification fixtures only."""
from pathlib import Path
import sys,json,re,copy,tempfile,concurrent.futures
from decimal import Decimal as D,ROUND_CEILING
ROOT=Path(__file__).resolve().parents[4];S=ROOT/'researchers/vishesh/notes/optimal-swarm-size'
sys.path.insert(0,str(S/'src'))
from tasks import generate,evaluate,operational
from engine import execute,validate_plan
from budget import Budget
rows=[]
for structure in ['parallel','chain']:
 t=generate('evidence',structure,0);p=t.public;vals={};proofs={};ans={}
 for item in p['items']:
  prev,a,b=re.fullmatch(r'\w+ = (\w+) \* (\w+) \+ (\w+)',p['rules'][item]).groups()
  vals[item]=(vals[prev] if prev in vals else p['records'][prev])*p['records'][a]+p['records'][b]
  proofs[item]=sorted(set((proofs[prev] if prev in proofs else [prev])+[a,b]))
  ans[item]={'value':vals[item],'source_ids':proofs[item]}
 artifact={'answers':ans};graded=evaluate(t,json.dumps(artifact));assert graded['substantive_success']
 mutations={}
 for label in ['wrong_value','missing_support','boolean','extra_source']:
  bad=copy.deepcopy(artifact);x=bad['answers'][p['items'][-1]]
  if label=='wrong_value':x['value']+=1
  if label=='missing_support':x['source_ids'].pop()
  if label=='boolean':x['value']=True
  if label=='extra_source':x['source_ids'].append('invented')
  mutations[label]=evaluate(t,json.dumps(bad))['substantive_success'];assert not mutations[label]
 captured=[]
 def call(messages,deadline,actor,phase,item):
  captured.append(copy.deepcopy(messages))
  if phase=='plan':return json.dumps({'dependencies':p['dependencies']})
  if phase=='work':return json.dumps({'artifact':ans[item]})
  return json.dumps(artifact)
 result=execute(p,1,1,10,2,call)
 before=copy.deepcopy(captured);captured.clear();t.truth['review_hidden_marker']='DO_NOT_SEND';execute(p,1,1,10,2,call)
 assert captured==before and 'DO_NOT_SEND' not in json.dumps(captured)
 rows.append({'family':'evidence','structure':structure,'opening':p['records']['opening'],'first':vals[p['items'][0]],'last':vals[p['items'][-1]],'first_rule':p['rules'][p['items'][0]],'records_first':{k:p['records'][k] for k in ['a_0','b_0']},'mutations_accepted':mutations,'truth_mutation_prompts_unchanged':True,'late_correct_accepted':operational(graded,11,1,10,2)})
 t=generate('repository',structure,0);p=t.public
 # Public specification directly states each required expression.
 fixes={item+'.py':'def '+item+'(x):\n    return '+re.fullmatch(r'Return (.+) for every integer x from -100 through 100\.',p['specifications'][item]).group(1)+'\n' for item in p['items']}
 assert evaluate(t,json.dumps({'files':fixes}))['substantive_success']
 constant=copy.deepcopy(fixes);constant['item_00.py']='def item_00(x):\n    return 5\n'
 extra=copy.deepcopy(fixes);extra['tests.py']='pass'
 equivalent={k:v.replace('return ','return 0 + ') for k,v in fixes.items()}
 checks={'broken_passes':evaluate(t,json.dumps({'files':p['files']}))['substantive_success'],'constant_passes':evaluate(t,json.dumps({'files':constant}))['substantive_success'],'extra_file_passes':evaluate(t,json.dumps({'files':extra}))['valid'],'equivalent_passes':evaluate(t,json.dumps({'files':equivalent}))['substantive_success']}
 assert checks==dict(broken_passes=False,constant_passes=False,extra_file_passes=False,equivalent_passes=True)
 rows.append({'family':'repository','structure':structure,'first_spec':p['specifications']['item_00'],'second_spec':p['specifications']['item_01'],'checks':checks})
p=generate('evidence','chain',0).public
empty=validate_plan({'dependencies':{i:[] for i in p['items']}},p['items'])
with tempfile.TemporaryDirectory() as temp:
 bank=Budget(Path(temp)/'ledger.sqlite',100)
 def reserve(i):
  try:bank.reserve(str(i),'episode',30,100);return True
  except ValueError:return False
 with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:admitted=sum(pool.map(reserve,range(24)))
 exposure=bank.exposure('episode');assert admitted==3 and exposure==90
cfg=json.loads((S/'qualification-config.json').read_text());bound=int(((D(str(cfg['input_usd_per_token']))*cfg['provider_context_tokens']+D(str(cfg['output_usd_per_token']))*cfg['max_output_tokens'])*1000000).to_integral_value(rounding=ROUND_CEILING))
result={'derivations':rows,'chain_edges_removed_accepted':all(not v for v in empty.values()),'race':{'attempted':24,'admitted':admitted,'exposure':exposure,'cap':100},'reservation_microdollars':bound,'api_calls':0}
Path(__file__).with_name('swarm-size-checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
