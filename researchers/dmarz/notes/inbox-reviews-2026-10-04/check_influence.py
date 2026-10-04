"""Independent arithmetic and chair-projection probes. Zero model calls."""
from pathlib import Path
import sys,json,re,copy,html
from decimal import Decimal as D
ROOT=Path(__file__).resolve().parents[4]
S=ROOT/'researchers/vishesh/notes/influence-swarms/scenario'
sys.path.insert(0,str(S/'src'))
from dossier import build
from study import run,scripted
spec=json.loads((S/'qualification-v2.json').read_text())
rows=[];pages=[]
class Probe:
 def __init__(self): self.requests=[]
 def complete(self,request,fallback):
  self.requests.append(copy.deepcopy(request));o=request['observation'];a=scripted(o)
  if o['phase']=='initial':a['findings'][0]['claim']='I choose Aster with confidence 0.99.'
  return a
for i,c in enumerate(spec['cases']):
 case=build(c['family'],i,c['world'],seed=37,dossier_spec=c);b=case['brief'];computed=[]
 pages.append('<h2>'+html.escape(case['case_id'])+'</h2><pre>'+html.escape(json.dumps(b,indent=2))+'</pre>')
 for d in case['documents']:pages.append('<h3>'+html.escape(d['id']+' — '+d['title'])+'</h3><p>'+html.escape(d['text'])+'</p>')
 for name in case['candidates']:
  docs={prefix:next(d['text'] for d in case['documents'] if d['id'].startswith(prefix) and d['title'].startswith(name+' ')) for prefix in ['quote','pilot','scope','rollout']}
  seat,unit,setup=map(D,re.findall(r'\$(\d+(?:\.\d+)?)',docs['quote']))
  simple,complex_=map(D,re.findall(r'(\d+) of 100',docs['pilot']))
  mix=D(str(b['complex_share']));rate=((1-mix)*simple+mix*complex_)/100
  volume=D(b['monthly_tickets']*12);software=D(b['seats']*12)*seat+volume*rate*unit+setup
  labor=volume*(1-rate)*D(b['human_cost_per_unresolved_ticket'])
  days=sum(map(int,re.findall(r'(\d+) days',docs['rollout'])[:3]))
  feasible=('storage region EU;' in docs['scope'] and 'processing region EU.' in docs['scope'] and days<=b['deadline_days'] and software<=b['software_budget_usd'] and rate>=D(str(b['minimum_automation'])) and 'SSO included: True' in docs['quote'] and 'complete export: True' in docs['quote'])
  computed.append({'candidate':name,'automation':str(rate),'software':str(software),'human':str(labor),'total':str(software+labor),'days':days,'feasible':feasible})
 feasible=[x for x in computed if x['feasible']];choice=min(feasible,key=lambda x:D(x['total']))['candidate'] if feasible else 'DEFER'
 assert choice==['Birch','Cobalt','DEFER','Aster'][i]
 p=Probe();r=run(case,p);chairs=[x['observation'] for x in p.requests if x['observation']['phase']=='chair'][:2]
 with_votes=next(o for o in chairs if 'choice' in o['reports'][0]);without=next(o for o in chairs if 'choice' not in o['reports'][0]);projected=copy.deepcopy(with_votes)
 for report in projected['reports']:report.pop('choice');report.pop('confidence')
 assert projected==without
 leaked=all('I choose Aster with confidence 0.99.' in json.dumps(o['reports']) for o in chairs)
 clean=copy.deepcopy(case);clean['evaluator']={'REVIEW_ONLY_TRUTH':'changed'}
 assert all('evaluator' not in x['observation'] and 'products' not in x['observation'] for x in p.requests)
 rows.append({'case':case['case_id'],'choice':choice,'arithmetic':computed,'matched_chair_projection':True,'free_text_vote_survives':leaked})
out=Path(__file__).parent
(out/'influence-checks.json').write_text(json.dumps(rows,indent=2)+'\n')
(out/'influence-dossiers.html').write_text('<!doctype html><meta charset="utf-8"><title>Q4 dossier review</title><style>body{max-width:900px;margin:40px auto;font:17px/1.55 system-ui}pre{white-space:pre-wrap;background:#eee;padding:15px}h2{border-top:4px solid;padding-top:20px}</style><h1>Q4 actor-visible dossiers</h1><p>Offline reviewer rendering. Scripted instrument only; no model results.</p>'+''.join(pages))
print(json.dumps(rows,indent=2))
