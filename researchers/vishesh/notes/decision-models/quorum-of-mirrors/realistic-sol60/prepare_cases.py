"""Offline candidate preparation. Does not label, call models or admit a run."""
import argparse, collections, hashlib, json, re
from pathlib import Path
from urllib.parse import urlsplit
LABELS=('Supported','Refuted','Not Enough Evidence','Conflicting Evidence/Cherrypicking')
def digest(x):return hashlib.sha256(x).hexdigest()
def norm(s):return re.sub(r'\W+',' ',s.casefold()).strip()
def unwrap(u):
 p=urlsplit(u)
 if p.hostname in ('web.archive.org','web.archive.org:443'):
  m=re.search(r'/web/[^/]+/(https?://.*)',u)
  if m:return m.group(1)
 return u
def host(u):return (urlsplit(unwrap(u)).hostname or '').removeprefix('www.')
def urlkey(u):
 p=urlsplit(unwrap(u));return host(u)+p.path.rstrip('/')
def convert(row,index,blocked_hosts=()):
 if row['label'] not in LABELS:return None,'unsupported_label'
 if len(row['questions'])<2:return None,'fewer_than_two_questions'
 evidence=[]
 for q in row['questions']:
  if not q.get('question','').strip():return None,'empty_question'
  for a in q['answers']:
   if a.get('source_medium','').casefold() not in ('web text','webpage','text'):return None,'non_text_or_unspecified_medium'
   if not a.get('source_url') or not a.get('answer'):return None,'missing_evidence'
   if host(a['source_url']) in blocked_hosts:return None,'fact_check_domain'
   if host(a['source_url']) in ('google.com','bing.com','averitec.eu') or urlsplit(unwrap(a['source_url'])).path.endswith('/404'):return None,'placeholder_or_search_source'
   if urlkey(a['source_url'])==urlkey(row.get('fact_checking_article','')):return None,'fact_check_article_in_evidence'
   evidence.append({'evidence_id':f'e{len(evidence):02d}','question':q['question'],'answer':a['answer'],'explanation':a.get('boolean_explanation',''),'document_id':'doc-'+digest(urlkey(a['source_url']).encode())[:16],'source_host':host(a['source_url'])})
 if len(evidence)<3:return None,'fewer_than_three_evidence_records'
 actor={'case_id':'av-'+digest(str(index).encode())[:12], 'claim':row['claim'],'claim_date':row.get('claim_date'),'evidence':evidence}
 # This is an offline length screen, not a provider tokenizer or runtime guarantee.
 if len(json.dumps(actor,ensure_ascii=False).encode())>12000:return None,'oversized_candidate'
 return actor,None

def prepare(rows):
 bins={x:[] for x in LABELS};excluded=collections.Counter();seen_claim=set();seen_article=set()
 blocked_hosts={host(r.get('fact_checking_article','')) for r in rows}
 for i,row in enumerate(rows):
  a,reason=convert(row,i,blocked_hosts)
  if reason:excluded[reason]+=1;continue
  ck=norm(row['claim']);ak=urlkey(row.get('fact_checking_article',''))
  if ck in seen_claim or ak in seen_article:excluded['duplicate_claim_or_article']+=1;continue
  seen_claim.add(ck);seen_article.add(ak)
  bins[row['label']].append((digest(('R60-development-v1:'+str(i)).encode()),i,a,row))
 selected=[]
 for label in LABELS:
  for _,i,a,row in sorted(bins[label])[:6]:selected.append((i,a,row))
 return selected,dict(excluded),{k:len(v) for k,v in bins.items()}

def main():
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--revision',required=True);p.add_argument('--private-out',type=Path,required=True);p.add_argument('--report',type=Path,required=True);args=p.parse_args()
 raw=args.source.read_bytes();rows=json.loads(raw);selected,excluded,eligible=prepare(rows);args.private_out.mkdir(parents=True,exist_ok=False)
 actors=[a for _,a,_ in selected];gold=[{'case_id':a['case_id'],'source_index':i,'label':r['label'],'justification':r['justification'],'source_locators':[{ 'document_id':'doc-'+digest(urlkey(a['source_url']).encode())[:16],'source_url':a['source_url']} for q in r['questions'] for a in q['answers']],'article_group_sha256':digest(urlkey(r['fact_checking_article']).encode())} for i,a,r in selected]
 for name,data in [('actors.json',actors),('evaluator.json',gold)]: (args.private_out/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
 report={'status':'development_candidates_not_run_ready','source_repository':'https://github.com/MichSchli/AVeriTeC','source_revision':args.revision,'source_split':'train','source_sha256':digest(raw),'license':'CC-BY-NC-4.0','attribution':'Michael Schlichtkrull, Zhijiang Guo, Andreas Vlachos (2023), AVeriTeC','rows_examined':len(rows),'eligible_by_label':eligible,'excluded_counts':excluded,'selected_count':len(selected),'selected':[{'source_index':i,'case_id':a['case_id'],'label':r['label'],'questions':len(r['questions']),'evidence_records':len(a['evidence']),'unique_urls':len(set(e['document_id'] for e in a['evidence'])),'actor_sha256':digest(json.dumps(a,sort_keys=True).encode())} for i,a,r in selected],'actor_fields':['case_id','claim','claim_date','evidence'],'gold_fields_removed':['label','justification','fact_checking_article','claim_types','fact_checking_strategies','required_reannotation'],'limitations':['QA evidence is annotation-guided and may reveal verdicts semantically.','URL identity does not establish independent acquisition.','Manual answerability, leakage and event-group audit pending.','Development source selection inspected; no untouched qualification/evaluation claimed.'],'native_calls':0}
 args.report.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['selected_count','eligible_by_label','excluded_counts','native_calls']}))
if __name__=='__main__':main()
