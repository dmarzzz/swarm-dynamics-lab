"""Fail-closed public documentation check; no credentials or model calls."""
import argparse,datetime,hashlib,json,re,urllib.request
from pathlib import Path
REQUIRED=('tldr','question and prediction','setup','protocol','metrics')
def validate(experiment,markdown,run_tldr):
    url=experiment.get('url','') or ''
    match=re.fullmatch(r'https://github\.com/dmarzzz/swarm-lab/blob/([0-9a-f]{40})/(.+\.md)',url)
    if not match:raise ValueError('immutable_public_plan_required')
    if not (experiment.get('description') or '').startswith('TLDR: '):raise ValueError('registered_tldr_required')
    if len(run_tldr.strip())<40:raise ValueError('specific_run_tldr_required')
    sections={m.group(1).strip().lower():m.group(2).strip() for m in re.finditer(r'^## ([^\n]+)\n(.*?)(?=^## |\Z)',markdown,re.M|re.S)}
    if any(not sections.get(s) or sections[s].startswith('TODO') for s in REQUIRED):raise ValueError('public_plan_sections_missing')
    return {'experiment':experiment['id'],'url':url,'commit':match.group(1),'plan_sha256':hashlib.sha256(markdown.encode()).hexdigest(),'registered_tldr':experiment['description'],'run_tldr':run_tldr,'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'SwarmLab-PlanPreflight/1.0'}),timeout=25) as r:return r.read().decode()
def check(experiment_id,run_tldr):
    state=json.loads(fetch('https://swarm-live.pages.dev/api/state'))
    exp=next((e for e in state['experiments'] if e['id']==experiment_id),None)
    if exp is None:raise ValueError('experiment_not_registered')
    url=exp.get('url') or ''
    if not re.fullmatch(r'https://github\.com/dmarzzz/swarm-lab/blob/[0-9a-f]{40}/.+\.md',url):raise ValueError('immutable_public_plan_required')
    raw=url.replace('https://github.com/','https://raw.githubusercontent.com/').replace('/blob/','/')
    return validate(exp,fetch(raw),run_tldr)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--experiment',required=True);p.add_argument('--run-tldr',required=True);p.add_argument('--receipt',required=True);a=p.parse_args()
    try:
        receipt=check(a.experiment,a.run_tldr)
        with Path(a.receipt).open('x') as f:json.dump(receipt,f,indent=2)
        print('Public plan preflight passed: '+a.experiment)
    except Exception as e:
        print('Public plan preflight failed: '+(str(e) if isinstance(e,ValueError) else type(e).__name__));raise SystemExit(1)
