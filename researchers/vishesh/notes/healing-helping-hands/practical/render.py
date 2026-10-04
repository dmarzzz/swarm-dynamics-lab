import argparse,json,statistics,io
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
from engine import ARMS,SCENARIOS
COLORS=['#a87832','#245c9c','#916eab','#bc4b56','#19856f']
def load(results):
 m=json.loads((results/'manifest.json').read_text())
 if m['status']!='completed' or m['terminal_counts']!={'completed':180}:raise ValueError('incomplete_bundle')
 worlds={a['id']:json.loads((results/(a['id']+'.json')).read_text()) for a in m['assignments']}
 if any(len(w['frames'])!=30 for w in worlds.values()):raise ValueError('missing_history')
 return m,worlds

def effects(worlds):
 out={}
 for scenario in SCENARIOS:
  by={}
  for arm in ARMS:
   rows=[w for w in worlds.values() if w['scenario']==scenario and w['arm']==arm]
   values={k:[statistics.mean(w['metrics'][k] for w in rows if w['seed']==s) for s in (8701,8702,8703)] for k in ('post_event_error','final_retention','final_stale','final_error','traffic_items','false_invalidations_peak')}
   by[arm]={k:{'mean':statistics.mean(v),'min':min(v),'max':max(v),'corpora':v} for k,v in values.items()}
  baseline=by['central-append']['post_event_error']['mean'];peer=by['peer-verified']['post_event_error']['mean'];loss=by['central-append']['final_retention']['mean']-by['peer-verified']['final_retention']['mean']
  out[scenario]={'arms':by,'central_append_minus_peer_verified':baseline-peer,'relative_reduction':(baseline-peer)/baseline if baseline else None,'retention_loss':loss,'useful_rule_met':bool(baseline and (baseline-peer)/baseline>=.2 and loss<=.03+1e-10)}
 return out

def frame(worlds,t):
 fig=plt.figure(figsize=(16,10.5),dpi=100,facecolor='#f4f6f8');gs=fig.add_gridspec(3,5,height_ratios=[.18,1,1.12],hspace=.36,left=.045,right=.98,top=.96,bottom=.07)
 ax=fig.add_subplot(gs[0,:]);ax.axis('off');ax.text(0,1,'Healing Helping Hands | repair without trusting every notice',fontsize=20,weight='bold');ax.text(0,0,f'Recorded logical round {t:02d}/29 • seed 8701 • layout 18701 • combined scenario • saved Jev tape, no new inference',fontsize=11)
 for j,arm in enumerate(ARMS):
  w=worlds[f'8701-18701-combined-{arm}'];f=w['frames'][t];ax=fig.add_subplot(gs[1,j]);rgb=[]
  for i in range(200):rgb.append((.66,.69,.73) if f['missing'][i] else ((.12,.58,.44) if f['correct'][i] else (.78,.27,.31)))
  import numpy as np
  ax.imshow(np.array(rgb).reshape(10,20,3));ax.set_xticks([]);ax.set_yticks([]);ax.set_title(arm,fontsize=11,color=COLORS[j],weight='bold')
  for i in f['disconnected']:ax.add_patch(plt.Rectangle((i%20-.5,i//20-.5),1,1,fill=False,lw=.5,edgecolor='black'))
  ax.set_xlabel(f'Wrong / missing {f["incorrect_or_missing"]:.0%}\nStale citations {f["stale_fraction"]:.0%}\nNew evidence retained {f["new_retention"]:.0%}',fontsize=10)
 for k,(field,label) in enumerate([('incorrect_or_missing','Incorrect or missing queries'),('stale_fraction','Stale fraction of citations'),('new_retention','New evidence retention')]):
  # Three curves use dedicated manually placed axes below the five grids.
  ax=fig.add_axes([.055+k*.31,.12,.275,.29])
  for j,arm in enumerate(ARMS):
   w=worlds[f'8701-18701-combined-{arm}'];ax.plot(range(30),[f[field] for f in w['frames']],color=COLORS[j],label=arm,lw=2)
  ax.axvspan(10,20,color='#f5d6a5',alpha=.3);ax.axvline(t,color='#101f2b',lw=1);ax.set_ylim(-.03,1.03);ax.set_xlim(0,29);ax.set_title(label,fontsize=11);ax.set_xlabel('Logical round');ax.spines[['top','right']].set_visible(False)
  if k==0:ax.legend(fontsize=7,loc='upper right')
 fig.text(.05,.025,'Green: correct with evidence · Red: incorrect · Gray: missing · Outline: central connection unavailable\nRound 10: new evidence, genuine + forged withdrawals, central outage. Round 20: central access restored. Programmed policies; not autonomous research.',fontsize=10)
 return fig

def render(results,out):
 m,worlds=load(results);out.mkdir(parents=True,exist_ok=True);e=effects(worlds);(out/'effects.json').write_text(json.dumps(e,indent=2));images=[]
 for t in range(30):
  f=frame(worlds,t);b=io.BytesIO();f.savefig(b,format='png');plt.close(f);b.seek(0);im=Image.open(b).convert('RGB');images.append(im)
  if t in (0,10,20,29):im.save(out/f'round-{t:02d}.png')
 images[0].save(out/'recovery.gif',save_all=True,append_images=images[1:],duration=450,loop=0)
 fig,axes=plt.subplots(2,3,figsize=(16,9),dpi=130)
 for ax,scenario in zip(axes.flat,SCENARIOS):
  vals=[e[scenario]['arms'][a]['post_event_error'] for a in ARMS];means=[v['mean'] for v in vals]
  ax.bar(range(5),means,color=COLORS);ax.errorbar(range(5),means,yerr=[[v['mean']-v['min'] for v in vals],[v['max']-v['mean'] for v in vals]],fmt='none',color='#222',capsize=3)
  ax.set_xticks(range(5),['Central\nappend','Central\nverified','Peer\nappend','Peer\nblind','Peer\nverified'],fontsize=8);ax.set_ylim(0,1);ax.set_title(scenario);ax.set_ylabel('Mean incorrect-or-missing queries');ax.spines[['top','right']].set_visible(False)
 fig.suptitle('Healing Helping Hands: central baselines expose the tradeoff\nThree saved semantic corpora; two layouts averaged within each. Whiskers are corpus ranges, not confidence intervals.',fontsize=14);fig.tight_layout(rect=[0,0,1,.93]);fig.savefig(out/'outcomes.png');plt.close(fig)
 data={'worlds':worlds,'effects':e,'plan':m['plan']['url']};(out/'data.js').write_text('window.DATA='+json.dumps(data,separators=(',',':'))+';')
 (out/'index.html').write_text((Path(__file__).parent/'replay.html').read_text())
 print(json.dumps({'worlds':len(worlds),'animation_frames':30,'out':str(out)}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--results',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();render(a.results,a.out)
