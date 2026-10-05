"""Project retained native evidence into a public numeric/categorical report."""
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'r43'))
import engine as e
p=argparse.ArgumentParser();p.add_argument('--results',required=True);p.add_argument('--out',required=True);a=p.parse_args();base=Path(a.results)
def read(n):return json.loads((base/n).read_text())
semantic=read('semantic-differences.json');diffs={(x['case_id'],x['repetition'],x['node']):x['differences'] for x in semantic['wrong_reports']}
records=read('records.json');cases={c['id']:c for c in e.c.corpus()}
def project(records):
 projection=[]
 for record in records:
  case=cases[record['case_id']];graph={n['id']:n for n in e.i.make_graph(case,record['repetition'],('truthful','misleading'))};nodes={}
  for item in record['nodes']:
   score=e.i.score(case,graph[item['id']],item['answer'])if item['state']=='valid'else None
   nodes[item['id']]={'state':item['state'],'score':score,'differences':diffs.get((record['case_id'],record['repetition'],item['id']),[]) if item['state']=='valid' else []}
  projection.append({'case':case['id'],'family':case['family'],'repetition':record['repetition'],'nodes':nodes})
 return projection
projection=project(records);first_records=read('first-pass-records.json')
data={'notes':read('interpretation-notes.json'),'summary':read('summary.json'),'analysis':read('assessment.json'),'first':read('first-pass-assessment.json'),'receipt':read('run-receipt.json'),'audit':read('saved-audit.json'),'roots':projection,'first_roots':project(first_records),'scenarios':{cid:{'brief':case['brief'],'target':case['gold']['target'],'acceptable':case['gold']['acceptable'],'claims':{world:next(p[world+'_clause'] for p in case['page_pool'] if world+'_clause' in p) for world in ('truthful','misleading')},'candidates':[{'vendor':v,'facts':case['gold']['facts'][v],'checks':case['gold']['checks'][v]} for v in case['vendors']]} for cid,case in cases.items() if case['split']=='evaluation'},'interpretation':'Saved visible report fields, not hidden reasoning or a causal reconstruction. Nine authored configurations; calls and members are not independent samples.'}
assert data['analysis']==e.analysis.analyze(e.c.corpus(),records)
assert data['first']==e.analysis.analyze(e.c.corpus(),first_records)
assert data['analysis']['assigned_final_decisions']==108 and len(projection)==18
out=Path(a.out);out.with_suffix('.json').write_text(json.dumps(data,separators=(',',':'))+'\n');payload=json.dumps(data).replace('<','\\u003c');out.write_text(Path(__file__).with_name('main-template.html').read_text().replace('__DATA__',payload));print(json.dumps({'assigned_finals':108,'roots':18,'model_calls':0,'raw_model_prose_included':False}))
