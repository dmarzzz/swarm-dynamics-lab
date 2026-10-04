"""Bounded public-source capture. No credentials, model generation or labels to actors."""
from pathlib import Path
import argparse,collections,concurrent.futures,hashlib,json,re,sys,time,urllib.request,urllib.error
from html.parser import HTMLParser
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'realistic-sol60'))
from prepare_cases import convert,urlkey,unwrap,host
from group_audit import groups

def sha(b):return hashlib.sha256(b).hexdigest()
class Paragraphs(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.buf=[];self.rows=[]
 def handle_starttag(self,t,a):
  if t in ('script','style','noscript','svg'):self.skip+=1
  if t in ('p','li','h1','h2','h3','blockquote','td'):self.flush()
 def handle_endtag(self,t):
  if t in ('script','style','noscript','svg'):self.skip=max(0,self.skip-1)
  if t in ('p','li','h1','h2','h3','blockquote','td'):self.flush()
 def handle_data(self,d):
  if not self.skip:self.buf.append(d)
 def flush(self):
  s=' '.join(' '.join(self.buf).split());self.buf=[]
  if len(s)>=60:self.rows.append(s)

def fetch(url,out):
 key=sha(url.encode());path=out/'sources'/key;path.mkdir(parents=True,exist_ok=True)
 attempts=[]
 for candidate in dict.fromkeys([url,unwrap(url)]):
  started=time.time()
  try:
   req=urllib.request.Request(candidate,headers={'User-Agent':'QuorumResearch/1.0 public-evidence-audit'})
   with urllib.request.urlopen(req,timeout=20) as f:
    kind=f.headers.get('Content-Type','');final=f.url;raw=f.read(3000001)
   if len(raw)>3000000:raise ValueError('too_large')
   if not any(x in kind.lower() for x in ('html','text/plain')):raise ValueError('unsupported_media')
   parser=Paragraphs();parser.feed(raw.decode('utf-8',errors='replace'));parser.flush();ps=parser.rows
   if len(' '.join(ps))<200:raise ValueError('insufficient_text')
   suspect=bool(re.search(r'access denied|verify you are human|just a moment|enable javascript and cookies', ' '.join(ps[:4]),re.I))
   (path/'raw.html').write_bytes(raw);(path/'paragraphs.json').write_text(json.dumps(ps,ensure_ascii=False))
   receipt=dict(url=url,retrieved_url=final,requested_variant=candidate,capture_version_changed=candidate!=url,status='blocked_page' if suspect else 'captured',raw_sha256=sha(raw),paragraphs=len(ps),seconds=time.time()-started,attempts=attempts,captured_at=time.time())
   (path/'receipt.json').write_text(json.dumps(receipt,indent=2));return key,receipt
  except Exception as exc:
   attempts.append({'code':exc.code if isinstance(exc,urllib.error.HTTPError) else type(exc).__name__,'seconds':time.time()-started})
 receipt=dict(url=url,status='unavailable',attempts=attempts);(path/'receipt.json').write_text(json.dumps(receipt,indent=2));return key,receipt

def main():
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--report',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=False)
 records={};source_hashes={}
 for split in ('train','dev'):
  b=(a.source/'data'/f'{split}.json').read_bytes();source_hashes[split]=sha(b);records.update({f'{split}:{i}':r for i,r in enumerate(json.loads(b))})
 g=groups(records);old=Path(__file__).resolve().parent.parent/'realistic-sol60';exposed=set()
 for filename in ('case-preparation.json','case-preparation-v2.json'):
  j=json.loads((old/filename).read_text());exposed.update(f"{j['source_split']}:{r['source_index']}" for r in j['selected'])
 forbidden={g[k] for k in exposed};blocked={host(r.get('fact_checking_article','')) for r in records.values()};bins=collections.defaultdict(list);exclusions=collections.Counter()
 for k,r in records.items():
  if g[k] in forbidden:exclusions['development_connected']+=1;continue
  actor,reason=convert(r,int(k.split(':')[1]),blocked)
  if reason:exclusions[reason]+=1;continue
  bins[r['label']].append((sha(('B32-source-intake-v1:'+k).encode()),k))
 eligible={k:len(v) for k,v in bins.items()}
 for v in bins.values():v.sort()
 selected=[];used=set()
 while len(selected)<40 and any(bins.values()):
  for label in sorted(bins):
   while bins[label]:
    _,k=bins[label].pop(0)
    if g[k] in used:exclusions['already_selected_component']+=1;continue
    selected.append(k);used.add(g[k]);break
   if len(selected)==40:break
 urls={};candidates=[]
 for k in selected:
  r=records[k];locs=[];seen=set()
  for q in r['questions']:
   for ans in q['answers']:
    u=ans['source_url'];key=urlkey(u)
    if key not in seen:seen.add(key);locs.append(u)
  locs=locs[:3]
  for u in locs:urls[sha(u.encode())]=u
  candidates.append(dict(source_key=k,metadata_group_sha256=sha(g[k].encode()),claim=r['claim'],claim_date=r.get('claim_date'),published_label=r['label'],questions=[q['question'] for q in r['questions']],locators=locs))
 (a.out/'candidates.json').write_text(json.dumps(candidates,indent=2));receipts={}
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  for key,r in pool.map(lambda u:fetch(u,a.out),urls.values()):receipts[key]=r
 packets=[]
 for c in candidates:
  terms=set(re.findall(r'[a-z]{3,}',(c['claim']+' '+' '.join(c['questions'])).lower()))-{'the','and','was','were','that','this','with','from','what','which','have','has','did'}
  evidence=[]
  for u in c['locators']:
   k=sha(u.encode());r=receipts[k]
   if r['status']!='captured':continue
   ps=json.loads((a.out/'sources'/k/'paragraphs.json').read_text());ranked=sorted(range(len(ps)),key=lambda i:(-len(terms&set(re.findall(r'[a-z]{3,}',ps[i].lower()))),i))[:3]
   for i in sorted(ranked):evidence.append(dict(document_id=k,paragraph_index=i,text=ps[i],source_host=host(u),capture_version_changed=r['capture_version_changed']))
  packets.append(dict(source_key=c['source_key'],claim=c['claim'],claim_date=c['claim_date'],evidence=evidence))
 (a.out/'candidate-packets.json').write_text(json.dumps(packets,indent=2,ensure_ascii=False))
 report=dict(status='capture_only_not_case_admission',source_sha256=source_hashes,source_revision='7c62d1ec8df3fb560d6efe2b85fa191135636f81',rows=len(records),exclusions=dict(exclusions),eligible_by_label=eligible,selected_candidates=len(candidates),selected_by_label=dict(collections.Counter(c['published_label'] for c in candidates)),unique_locators=len(urls),capture_status=dict(collections.Counter(r['status'] for r in receipts.values())),candidates_with_any_excerpt=sum(bool(p['evidence']) for p in packets),verified_event_clusters=0,support_audited_packets=0,model_calls=0,source_keys=selected,private_packet_sha256=sha((a.out/'candidate-packets.json').read_bytes()),notes=['No source label inherited automatically.','Metadata groups are not verified independent events.','No actor packet contains annotation answers or gold.','Capture-version changes require manual temporal review.'])
 a.report.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('source_keys','source_sha256')}))
if __name__=='__main__':main()
