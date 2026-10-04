"""Offline full-cohort replay. Qualification only; never reads sealed evaluation."""
from pathlib import Path
import argparse,json,hashlib,html
from contract import score,summarize,digest

def read_lines(p):return [json.loads(s) for s in p.read_text().splitlines() if s] if p.exists() else []
def analyze(folder,packet_file):
 packet=json.loads(packet_file.read_text());rows=packet['rows'];assignments=packet['manifest']['assignments']
 records=read_lines(folder/'receipts.jsonl');requests=read_lines(folder/'requests.jsonl');accounting=read_lines(folder/'accounting.jsonl')
 by={r['id']:r for r in records};rq={r['id']:r for r in requests};ac={r['id']:r for r in accounting}
 assert len(by)==len(records) and len(rq)==len(requests) and len(ac)==len(accounting)
 assert set(by)<=set(rq)<={a['id'] for a in assignments}
 reviewed=[];discrepancies=[]
 for a,row in zip(assignments,rows):
  rec=by.get(a['id']);status='unstarted' if rec is None else 'valid' if rec['valid'] else 'invalid'
  if rec:
   assert digest(rq[a['id']]['request'])==a['request_sha256']==rq[a['id']]['sha256']
   assert json.loads(rq[a['id']]['request']['messages'][1]['content'])==row['actor']
   if rec.get('usage'):assert ac[a['id']]['usage']==rec['usage']
   if rec['valid']:
    recalculated=score(row,json.loads(rec['content']));assert recalculated==rec['score']
    if not (recalculated['decision_correct'] and recalculated['source_votes_correct']==3 and recalculated['distortions_correct'] and recalculated['quotes_valid']):discrepancies.append(a['id'])
  reviewed.append({'id':a['id'],'case_id':row['id'],'root':row['root'],'condition':row['condition'],'status':status,'gold':row['gold'],'actor':row['actor'],'receipt':rec})
 summary=summarize(rows,records);assert all(json.loads((folder/'summary.json').read_text())[k]==v for k,v in summary.items())
 conditions={}
 for count in (1,5):
  for inverted in (False,True):
   group=[r for r in reviewed if r['condition']=={'copies':count,'inverted':inverted}]
   conditions[f'copies={count},inverted={inverted}']={'assigned':len(group),'valid':sum(r['status']=='valid' for r in group),'correct':sum(bool(r['receipt'] and r['receipt'].get('score',{}).get('decision_correct')) for r in group)}
 report={'summary':summary,'conditions':conditions,'reviewed_slots':len(reviewed),'misses':discrepancies,'source_or_accounting_discrepancies':0,'cells':reviewed}
 (folder/'audit.json').write_text(json.dumps(report,indent=2)+'\n')
 parts=['<!doctype html><meta charset="utf-8"><title>QM-PQ-01 qualification traces</title><style>body{font:16px system-ui;max-width:1100px;margin:2rem auto}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f4f4f4;padding:1rem}details{border:1px solid #ccc;padding:.7rem;margin:.5rem}</style><h1>QM-PQ-01: all 24 assigned qualification cases</h1><p>Six scenario roots, four correlated conditions each. Native qualification, not evaluation or swarm efficacy.</p><pre>'+html.escape(json.dumps(summary,indent=2))+'</pre>']
 for cell in reviewed:
  parts += ['<details><summary>'+html.escape(cell['id']+' / '+cell['case_id']+' / '+cell['status'])+'</summary><h2>Actual experimental request</h2><pre>'+html.escape(json.dumps(rq.get(cell['id'],{}).get('request'),indent=2))+'</pre><h2>Retained answer and scoring</h2><pre>'+html.escape(json.dumps(cell['receipt'],indent=2))+'</pre><h2>Evaluator-only gold</h2><pre>'+html.escape(json.dumps(cell['gold'],indent=2))+'</pre></details>']
 (folder/'traces.html').write_text(''.join(parts))
 print(json.dumps({k:v for k,v in report.items() if k!='cells'},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('folder',type=Path);p.add_argument('packet',type=Path);a=p.parse_args();analyze(a.folder,a.packet)
