"""Post-run reconciliation; fails on missing, duplicate or inconsistent records."""
import collections,hashlib,json,sys
from pathlib import Path
import study_receipts as s

def audit(out):
 out=Path(out);m=json.loads((out/'manifest.json').read_text());summary=json.loads((out/'summary.json').read_text())
 rows=[json.loads(x) for x in (out/'episodes.jsonl').read_text().splitlines()];events=[json.loads(x) for x in (out/'events.jsonl').read_text().splitlines()]
 key=lambda x:(x['case'],x['seed'],x['memory'],x['arm'])
 assert collections.Counter(map(key,rows))==collections.Counter(map(key,m['assigned'])),'assignment_denominator'
 assert len(rows)==16 and summary['recorded']==16,'episode_count'
 for r in rows:
  f=s.fixture(r['case'],r['seed']);assert len(r['trace'])==6
  assert r['healthy_ticks']==sum(x['healthy'] for x in r['trace'])
  assert r['claim_errors']==sum(len(x['claim_errors']) for x in r['trace'])
  for x in r['trace']:
   assert x['checks']==s.health(f,x['deployed']),'recomputed_health'
   assert x['healthy']==int(all(x['checks'].values()))
   if r['memory']=='clean':assert not x['visible_memory_ids']
  peer=next(q for q in rows if q['case']==r['case'] and q['memory']==r['memory'] and q['checked']!=r['checked'])
  assert peer['proposal_hash']==r['proposal_hash'],'paired_proposals'
  expected=[dict((k,v) for k,v in p.items() if k!='receipt') for p in r['advice']]
  assert s.digest(expected)==r['proposal_hash']
  for p in r['advice']:assert p['receipt']==s.receipt(p,r['initial_checks'],r['checked'])
  framed=[e for e in events if e['kind']=='frame' and e.get('arm')==r['arm'] and e['case']==r['case']]
  assert len(framed)==6
  for x,e in zip(r['trace'],framed):assert all(e[k]==v for k,v in x.items())
 decisions=[e for e in events if e['kind']=='decision'];advice=[e for e in events if e['kind']=='advice'];errors=[e for e in events if e['kind']=='error']
 assert len(decisions)+len(advice)+len(errors)==120,'terminal_call_denominator'
 if m['backend']=='anthropic':assert summary['api_calls']==120
 latencies=[x['latency_seconds'] for r in rows for x in r['trace']]
 result={'assigned':16,'recorded':16,'paired_worlds':8,'unique_reviewer_records':len(advice),'decision_records':len(decisions),'errors':len(errors),'paired_advice_identical':True,'all_trace_frames_match':True,'clean_memory_traces_empty':True,'mean_commander_seconds':sum(latencies)/len(latencies),'reviewer_false_claims':sum(rows[i]['advice_false_claims'] for i in range(0,16,2)),'reviewer_declared_booleans':96,'commander_false_claims':sum(r['claim_errors'] for r in rows),'commander_declared_booleans':384,'episodes_sha256':hashlib.sha256((out/'episodes.jsonl').read_bytes()).hexdigest()}
 (out/'audit.json').write_text(json.dumps(result,indent=2));return result
if __name__=='__main__':print(json.dumps(audit(sys.argv[1]),indent=2))
