"""Known-answer UI fixture: three recorded examples plus missing observations, no provider."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from instrument import assignments,commands,truth,ARMS
from analyze import summarize
from render import render
root=Path(sys.argv[1]);root.mkdir();(root/'calls').mkdir();aa=assignments((10,11,12));(root/'manifest.json').write_text(json.dumps({'evidence_type':'software_fixture','assignments':aa}))
for i,a in enumerate(aa[:3]):
 value={'decisions':[{'id':c['id'],'command':commands(a['context'])[truth(c,a['context'],a['rule'])]} for c in a['cases']]}
 if ARMS[a['arm']][2]:value['notebook']='SCRIPTED SOFTWARE FIXTURE, NOT MODEL EVIDENCE'
 if i==1:value['decisions'][0]['command']='INVALID-FIXTURE-COMMAND'
 if i==2:value['decisions']=[]
 (root/'calls'/(a['id']+'-finished.json')).write_text(json.dumps({'value':value,'error':None,'actual_usd':0}))
(root/'summary.json').write_text(json.dumps(summarize(root)));render(root)
print('SCRIPTED SOFTWARE FIXTURE, NOT MODEL EVIDENCE: viewer generated')
