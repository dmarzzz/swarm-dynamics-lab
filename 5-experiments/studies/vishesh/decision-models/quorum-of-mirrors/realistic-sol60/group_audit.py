"""Conservative offline split-leakage audit; does NOT certify event independence."""
import argparse,collections,json,hashlib
from pathlib import Path
from prepare_cases import norm,urlkey

def groups(records):
 parent={k:k for k in records};seen={}
 def find(k):
  while parent[k]!=k:parent[k]=parent[parent[k]];k=parent[k]
  return k
 def join(a,b):
  a,b=find(a),find(b)
  if a!=b:parent[max(a,b)]=min(a,b)
 for k,r in records.items():
  keys=[('claim',norm(r.get('claim',''))),('article',urlkey(r.get('fact_checking_article','')))]
  for q in r.get('questions',[]):
   for a in q.get('answers',[]):
    if a.get('source_url'):keys.append(('document',urlkey(a['source_url'])))
  for key in keys:
   if not key[1]:continue
   if key in seen:join(k,seen[key])
   else:seen[key]=k
 return {k:find(k) for k in records}

def main():
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--development-reports',nargs='+',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 records={};hashes={}
 for split in ('train','dev'):
  raw=(a.source/'data'/f'{split}.json').read_bytes();hashes[split]=hashlib.sha256(raw).hexdigest()
  records.update({f'{split}:{i}':r for i,r in enumerate(json.loads(raw))})
 memberships=groups(records);exposed=set()
 for path in a.development_reports:
  j=json.loads(path.read_text());exposed.update(f"{j['source_split']}:{r['source_index']}" for r in j['selected'])
 forbidden={memberships[k] for k in exposed};sizes=collections.Counter(memberships.values())
 report={'status':'metadata_audit_only_not_event_independence','native_calls':0,'source_sha256':hashes,'rows':len(records),'components':len(sizes),'largest_component':max(sizes.values()),'development_rows_excluded':len(exposed),'transitively_excluded_rows':sum(v in forbidden for v in memberships.values()),'remaining_rows_by_split':{s:sum(k.startswith(s+':') and v not in forbidden for k,v in memberships.items()) for s in ('train','dev')},'development_source_indices':sorted(exposed),'rule':'Connected components over normalized claim, canonical fact-check article, and canonical evidence document; archive aliases normalized, semantic query parameters preserved.','limitations':['Shared generic reference pages can over-group unrelated events.','Different documents about the same event can remain separate; semantic event audit still required.','No qualification or evaluation cases selected or opened in this audit.','No label support, model access, approval or launch admission implied.']}
 a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ('rows','components','largest_component','development_rows_excluded','transitively_excluded_rows','remaining_rows_by_split')}))
if __name__=='__main__':main()
