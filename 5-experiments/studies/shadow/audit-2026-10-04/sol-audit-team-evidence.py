#!/usr/bin/env python3
"""Read-only audit inventory plus two isolated, zero-model-call validator probes.
Run from repo root: python3 <this file> --hub-json <saved public /api/state JSON>
Requires PyYAML. Does not launch worlds, mutate other studies or use credentials.
"""
import argparse, ast, collections, datetime, hashlib, json, pathlib, subprocess, sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[4]

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()

def main():
    p = argparse.ArgumentParser(); p.add_argument('--hub-json', required=True); a = p.parse_args()
    hub = json.loads(pathlib.Path(a.hub_json).read_text())
    registry = json.loads((ROOT/'experiments/evidence-metadata.json').read_text())
    sources = json.loads((ROOT/'researchers/vishesh/notes/pi-review-2026-10-04/review-2026-10-04/source-map.json').read_text())
    out = {'source_commit': git('rev-parse','HEAD'), 'hub_asof_utc': datetime.datetime.fromtimestamp(hub['now'],datetime.timezone.utc).isoformat(),
           'hub_sha256': hashlib.sha256(pathlib.Path(a.hub_json).read_bytes()).hexdigest(),
           'scope': 'Public repository and current public hub. Hub run lists may be truncated; absence is checked alongside owner README/pre-run records. Costs of worker sessions are not added to stage costs.',
           'registry': {'rows': len(registry['studies']), 'confidence_counts': dict(collections.Counter(str(s.get('evidence_confidence',{}).get('score')) for s in registry['studies'])),
                        'score_2_rows': [{'id':s['id'],'status':s.get('status_at_assessment')} for s in registry['studies'] if s.get('evidence_confidence',{}).get('score')==2]},
           'ready_inventory': [], 'reviewed_source_comparisons': [], 'offline_validator_probes': {}}
    for since in ['2026-10-03T18:00:00Z','2026-10-04T03:40:00Z']:
        counts=collections.Counter()
        for line in git('log','--since='+since,'--format=%an','HEAD').splitlines():
            name='dmarz' if line in ('dmarzzz','dmarz') else 'vishesh' if line in ('Ultron','cytonomy','Cytonomy','vishesh','Codex (vishesh/codex-avalon)') else 'bot' if line=='swarm-lab-bot' else 'other'
            counts[name]+=1
        out.setdefault('commit_counts_by_author_alias',{})[since]=dict(counts)
    for ready in sorted((ROOT/'researchers/dmarz').rglob('READY.yaml')):
        data=yaml.safe_load(ready.read_text()); study=data['study']; design=yaml.safe_load((ready.parent/'design.yaml').read_text())
        exps=[e for e in hub['experiments'] if e['id']==study or e['id'].startswith(study+'-')]
        runs=[r for e in exps for r in e.get('runs',[]) if 'worker-session' not in r.get('tags',[])]
        row={'path':str(ready.relative_to(ROOT)), 'ready':data, 'per_model_design':design.get('models'),
             'hub_runs':[{'id':r['run'],'status':r['status'],'stage':r.get('params',{}).get('stage'),'model':r.get('params',{}).get('model'),'calls':r.get('metrics',{}).get('model_calls'),'cost_usd':r.get('metrics',{}).get('cost_usd'),'episodes':r.get('metrics',{}).get('episodes'),'invalid':r.get('metrics',{}).get('invalid'),'failed':r.get('metrics',{}).get('failed'),'not_started':r.get('metrics',{}).get('not_started'),'message':r.get('message'),'ended':r.get('ended')} for r in runs]}
        out['ready_inventory'].append(row)
    wanted={'agent-experiment-guide/scripts/toy_harness.py','agent-experiment-guide/scripts/validate.py','avalon-swarm/benchmark.py','regrowth-200/src/public_plan.py','regrowth-200/src/run.py','regrowth-200/src/publish_hub.py','swarm-of-theseus/src/provider.py','swarm-of-theseus/src/runner.py','swarm-of-theseus/src/study.py','healing-helping-hands/visualization/render.py','healing-helping-hands/site/artifact-manifest.json'}
    for row in sources:
        if row['workspace_path'] not in wanted: continue
        path=ROOT/row['repository_path'] if row['repository_path'] else None
        digest=hashlib.sha256(path.read_bytes()).hexdigest() if path and path.is_file() else None
        out['reviewed_source_comparisons'].append({'workspace_path':row['workspace_path'],'repository_path':row['repository_path'],'actual_sha256':digest,'matches_reviewed_bytes':digest in row['reviewed_sha256'] if digest else None,'reviewed_sha256':row['reviewed_sha256'],'availability':row['availability']})
    probes={
      'EP-01': """import sys
sys.path.insert(0,'researchers/vishesh/notes/immune-response-v3/src')
import immune
class P:
 def complete(self,request,fallback):
  return {'choices':{k:None for k in request['response_schema']['properties']['choices']['properties']},'plan':[],'constraints':[],'requested_action':'unapproved'}
m={'k':immune.record('k',1)}
a=immune.act(P(),m,[],'coordinator',['service-0'])
print({'malformed_plan_accepted':isinstance(a['plan'],list),'memory_cleared':m=={},'illegal_action_accepted':a['requested_action']=='unapproved'})
""",
      'ADD-T-01': """import sys
sys.path.insert(0,'researchers/vishesh/notes/swarm-of-theseus/src')
import study
cs=[{'id':str(i)} for i in range(4)]
a=study.validate_solve({'work':[{'case_id':c['id'],'label':'ILLEGAL'} for c in cs],'convention':'','notebook':''},cs)
print({'illegal_labels_accepted':a['answers']==['ILLEGAL']*4})
"""}
    for name,code in probes.items():
        proc=subprocess.run([sys.executable,'-c',code],cwd=ROOT,text=True,capture_output=True,check=True)
        out['offline_validator_probes'][name]=ast.literal_eval(proc.stdout.strip())
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__': main()
