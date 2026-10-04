"""One authored root; source-only exact controller, no provider access."""
import json,hashlib,re,copy

def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def sha(x):return hashlib.sha256(canonical(x).encode()).hexdigest()

def actor():
 texts=[
 'Deployment policy: for the requested version and site, RELEASE requires recorded authorization, two distinct passed read-only acquisitions within the current latency limit, and rollback tested at that site. An explicit prohibition, failed required check or absent site from the COMPLETE tested-site list means HOLD. If no violation is established but required evidence is unknown, use INSUFFICIENT. Duplicate summaries are not new acquisitions. No write-path test, running monitor or independent re-verification is required.',
 'Correction: current latency limit is 120 ms, replacing 80 ms. Earlier measured values are unchanged. This correction applies to all sites below.',
 'Permit record: v7 at Cedar authorized; v7 at Bay explicitly prohibited. Bay v6 was authorized, but that does not authorize v7.',
 'Permit record: v7 at Delta requested; receipt unavailable. Authorization is unknown, not denied or granted.',
 'Acquisition C-A: v7 Cedar read-only, passed, 100 ms. Acquisition C-B: v7 Cedar read-only, passed, 110 ms. C-A and C-B are distinct acquisitions.',
 'Acquisition B-A: v7 Bay read-only, passed, 105 ms. Acquisition B-B: v7 Bay read-only, passed, 115 ms. B-A and B-B are distinct acquisitions.',
 'Acquisition D-A: v7 Delta read-only, passed, 90 ms. Acquisition D-B: v7 Delta read-only, passed, 95 ms. D-A and D-B are distinct acquisitions.',
 'Three Cedar summaries cite C-A. Two Bay summaries cite B-A. These summaries reuse their named acquisitions, not additional independent tests.',
 'COMPLETE rollback-tested sites for v7: Cedar, Bay, Delta. This record confirms testing, not a promised future test.',
 'Post-release monitors are proposed, not started. No write-path results are reported. These facts do not change the read-only deployment policy. Next handover 10:00.'
 ]
 return {'records':[{'id':f'm{i+1:02}','time':f'09:{i*5:02}','text':t} for i,t in enumerate(texts)]}
def questions():return {s:f'Under the deployment policy, should v7 be deployed at {s} now? Choose RELEASE, HOLD or INSUFFICIENT.' for s in ('Cedar','Bay','Delta')}
def reference(packet,question):
 # Parse explicit production source evidence; fail closed on absent policy/evidence.
 text=' '.join(r['text'] for r in packet['records']);m=re.search(r'should (v\d+) be deployed at (\w+) now',question)
 if not m or 'Deployment policy:' not in text:return 'INSUFFICIENT'
 version,site=m.groups();lim=re.search(r'current latency limit is (\d+) ms',text)
 auth=re.search(rf'{version} at {site} (authorized|explicitly prohibited|requested)',text)
 tests=re.findall(rf'Acquisition ([\w-]+): {version} {site} read-only, (passed|failed), (\d+) ms',text)
 rollback=re.search(rf'COMPLETE rollback-tested sites for {version}: ([^.]+)',text)
 if auth and auth[1]=='explicitly prohibited':return 'HOLD'
 if lim and any(s=='failed' or int(v)>int(lim[1]) for _,s,v in tests):return 'HOLD'
 if rollback and site not in rollback[1].split(', '):return 'HOLD'
 enough=lim and len({i for i,s,v in tests if s=='passed' and int(v)<=int(lim[1])})>=2
 if auth and auth[1]=='authorized' and enough and rollback:return 'RELEASE'
 return 'INSUFFICIENT'
def assignments():
 out=[]
 for hop in range(1,51):out.append({'id':f'w{hop:02}','chain':'serial50','case_id':'Cedar','role':'writer','arm':'P','hop':hop,'parent':f'w{hop-1:02}' if hop>1 else None})
 for j,hop in enumerate((1,10,25,50)):
  for k,site in enumerate(questions()):
   for arm in (('P','R') if (j+k)%2==0 else ('R','P')):out.append({'id':f'h{hop:02}-{site}-{arm}','chain':'serial50','case_id':site,'role':'reader','arm':arm,'hop':hop,'parent':f'w{hop:02}'})
 return out

def controls():
 a=actor();q=questions()['Cedar'];out=[]
 for index in (0,1,2,4,8):
  b=copy.deepcopy(a);b['records'].pop(index);out.append({'kind':f'remove-record-{index+1}','actor':b,'question':q,'expected':'INSUFFICIENT'})
 for old,new,label in [('C-B','C-A','INSUFFICIENT'),('passed, 110 ms','passed, 125 ms','HOLD'),('sites for v7: Cedar, Bay, Delta','sites for v7: Bay, Delta','HOLD'),('v7 at Cedar authorized','v7 at Cedar explicitly prohibited','HOLD')]:
  b=json.loads(json.dumps(a).replace(old,new));out.append({'kind':old,'actor':b,'question':q,'expected':label})
 b=copy.deepcopy(a);b['records'].reverse();out.append({'kind':'reorder','actor':b,'question':q,'expected':'RELEASE'})
 b=json.loads(json.dumps(a).replace('Cedar','Harbor'));out.append({'kind':'rename','actor':b,'question':q.replace('Cedar','Harbor'),'expected':'RELEASE'})
 return out
