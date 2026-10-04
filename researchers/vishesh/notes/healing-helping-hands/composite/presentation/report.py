"""Saved-data C1 presentation only: no provider access or scientific reruns."""
import argparse,json,statistics,hashlib,shutil,sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from definition import ARMS,SEEDS
from visualize import semantic,temporal
POLICIES=('central-append','central-verified','peer-append','peer-blind','peer-verified')
SCENARIOS=('benign','withdrawal','forged','missing-lineage','central-outage','combined')
FIELDS=('post_event_error','final_error','final_retention','final_stale','traffic_items','false_invalidations_peak')
def stats(xs):return {'mean':statistics.mean(xs),'min':min(xs),'max':max(xs),'per_corpus':xs}
def run(root,out):
 out.mkdir(parents=True,exist_ok=True)
 manifest=json.loads((root/'manifest.json').read_text());assign=json.loads((root/'world-assignments.json').read_text())
 assert manifest['status']=='completed' and len(assign)==270 and all(w['status']=='completed' for w in assign)
 worlds={w['id']:json.loads((root/(w['id']+'.json')).read_text()) for w in assign}
 effects={};contrasts={}
 for m in ARMS:
  effects[m]={}
  for s in SCENARIOS:
   arms={p:{k:stats([worlds[f'{seed}-{m}-{p}-{s}']['metrics'][k] for seed in SEEDS]) for k in FIELDS} for p in POLICIES}
   effects[m][s]={'arms':arms,'peer_minus_central':arms['peer-verified']['post_event_error']['mean']-arms['central-verified']['post_event_error']['mean']}
 for s in SCENARIOS:
  paired=[worlds[f'{seed}-qwen+jev-peer-verified-{s}']['metrics']['post_event_error']-worlds[f'{seed}-jev-peer-verified-{s}']['metrics']['post_event_error'] for seed in SEEDS]
  contrasts[s]={'composite_minus_jev':stats(paired)}
 data={'attempt':'C2-S1','packet_cap':16,'plan':manifest['plan']['url'],'completed_worlds':len(worlds),'worlds':worlds,'effects':effects,'contrasts':contrasts}
 (out/'data.js').write_text('const DATA='+json.dumps(data,separators=(',',':'))+';\n')
 shutil.copyfile(HERE/'replay.html',out/'index.html')
 (out/'effects.json').write_text(json.dumps({'effects':effects,'contrasts':contrasts,'unit':'three corpora; ranges not confidence intervals'},indent=2))
 semantic(json.loads((root/'observations.json').read_text()),out/'labels.png')
 temporal(worlds,out/'recovery.gif')
 fig,axes=plt.subplots(3,2,figsize=(18,13),dpi=110,sharey=True)
 colors=['#a87832','#245c9c','#916eab','#bc4b56','#19856f']
 for ax,s in zip(axes.flat,SCENARIOS):
  for j,p in enumerate(POLICIES):
   vs=[effects[m][s]['arms'][p]['post_event_error'] for m in ARMS];pos=[i+(j-2)*.15 for i in range(3)];means=[v['mean'] for v in vs]
   ax.bar(pos,means,width=.14,color=colors[j],label=p);ax.errorbar(pos,means,yerr=[[v['mean']-v['min'] for v in vs],[v['max']-v['mean'] for v in vs]],fmt='none',color='#334455',capsize=2)
  ax.set_xticks(range(3),['Qwen-only','Jev-only','Qwen + Jev']);ax.set_ylim(0,1);ax.set_title(s);ax.set_ylabel('Wrong or missing queries, rounds 10–29');ax.spines[['top','right']].set_visible(False)
 handles,labels=axes.flat[0].get_legend_handles_labels();fig.legend(handles,labels,loc='upper center',bbox_to_anchor=(.5,.945),ncol=5)
 fig.suptitle('Healing Helping Hands | every model, architecture and scenario',fontsize=20)
 fig.text(.07,.022,'270 completed worlds, 200 curators each; three fresh synthetic corpora. Whiskers are corpus ranges, not confidence intervals.\nShared extraction tapes pair architectures. Logical rounds and item-copy traffic do not establish equal compute or real-world latency.',fontsize=11)
 fig.tight_layout(rect=[0,.065,1,.90]);fig.savefig(out/'outcomes.png');plt.close(fig)
 provenance={'source_commit':manifest['plan']['commit'],'source_manifest_sha256':hashlib.sha256((root/'manifest.json').read_bytes()).hexdigest(),'renderer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'html_sha256':hashlib.sha256((HERE/'replay.html').read_bytes()).hexdigest(),'worlds':270,'frames':sum(len(w['frames']) for w in worlds.values()),'mapping':'C1 measured labels and propagation; saved-data render only'}
 (out/'render-provenance.json').write_text(json.dumps(provenance,indent=2));print(json.dumps({'rendered':True,'contrasts':contrasts}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--results',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();run(a.results,a.out)
