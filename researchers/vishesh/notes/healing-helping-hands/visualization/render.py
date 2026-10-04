"""Replay compiler and measured image exports. No inference or random decisions."""
import argparse,json,collections,hashlib,shutil
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from PIL import Image,ImageDraw,ImageFont
LABELS=('SUPPORT','REFUTE','UNCERTAIN')
def load(p):return json.loads(p.read_text())
def main(root,attempt,out):
 out.mkdir(parents=True,exist_ok=True);p=root/attempt;m=load(p/'manifest.json');
 if m['status']=='running':raise ValueError('results_not_terminal')
 assign=m['assignments'];
 if any(not (p/(a['id']+'.json')).is_file() for a in assign):raise ValueError('results_transfer_incomplete')
 seeds=sorted({a['seed'] for a in assign});worlds={a['id']:load(p/(a['id']+'.json')) for a in assign};completed=sum(a['status']=='completed' for a in assign)
 data={'attempt':attempt,'plan':m['plan'],'seeds':seeds,'total':len(assign),'worlds':worlds,'corpora':{s:load(p/f'corpus-{s}.json') for s in seeds},'tapes':{s:load(p/f'tapes-{s}.json') for s in seeds},'attempts':[],'status':f'{attempt}: {completed}/{len(assign)} assigned worlds completed. '+('The Jev semantic reference qualified. Qwen-derived conditions remain not-run.' if completed==72 else 'Exact extraction is an engineering control; model conditions remain not-run.')}
 for d in sorted(root.glob('pilot-*')):
  mm=load(d/'manifest.json');data['attempts'].append({'id':d.name,'qualification':mm['qualification'],'total':len(mm['assignments']),'completed':sum(a['status']=='completed' for a in mm['assignments'])})
 for r in data['worlds'].values():r.pop('final_state',None)
 data['defaultArm']='jev' if all(worlds.get(f'{s}-jev-evidence+withdrawals-combined',{}).get('status')=='completed' for s in seeds) else 'exact'
 (out/'data.js').write_text('window.REPLAY='+json.dumps(data,separators=(',',':'))+';')
 src=Path(__file__).with_name('index.html')
 if src.resolve()!=(out/'index.html').resolve():shutil.copyfile(src,out/'index.html')
 arms=['exact','qwen','qwen+qwen','qwen+laya','jev'];effects=[]
 for arm in arms:
  for scenario in ('none','withdrawal','erasure','combined'):
   for s in seeds:
    a=worlds.get(f'{s}-{arm}-evidence-only-{scenario}');b=worlds.get(f'{s}-{arm}-evidence+withdrawals-{scenario}');
    if not a or not b:continue
    if a['status']==b['status']=='completed':effects.append({'seed':s,'arm':arm,'scenario':scenario,'error_delta':b['metrics']['post_event_error']-a['metrics']['post_event_error'],'stale_delta':b['metrics']['post_event_stale']-a['metrics']['post_event_stale'],'final_accuracy':b['metrics']['final_accuracy'],'final_stale':b['metrics']['final_stale'],'event_accuracy':b['metrics']['initial_event_accuracy'],'pre_accuracy':b['metrics']['pre_event_accuracy'],'recovery_rounds':b['metrics']['recovery_rounds']})
 (out/'paired-effects.json').write_text(json.dumps(effects,indent=2))
 # Fixed illustrative pair: first seed, combined scenario, exact control (always available).
 seed=seeds[0];illustrative=data['defaultArm'];pair=[worlds[f'{seed}-{illustrative}-{policy}-combined'] for policy in ('evidence-only','evidence+withdrawals')];corpus=data['corpora'][seed]
 bg='#101716';ink='#edf4e9';muted='#aebeb3';colors=['#ff927a','#76ddad']
 plt.rcParams.update({'figure.facecolor':bg,'axes.facecolor':bg,'axes.edgecolor':muted,'text.color':ink,'axes.labelcolor':ink,'xtick.color':muted,'ytick.color':muted,'font.size':11})
 fig,axes=plt.subplots(1,3,figsize=(17,5),dpi=130)
 for j,(key,title) in enumerate([('atlas_accuracy','Atlas accuracy / 20 claims'),('stale_fraction','Stale cited roots / all cited roots'),('coverage','Valid informative source coverage')]):
  for policy,color,label in zip(('evidence-only','evidence+withdrawals'),colors,('Evidence only','Evidence + withdrawals')):
   fs=[worlds[f'{s}-{illustrative}-{policy}-combined']['frames'] for s in seeds];vals=np.array([[f[key] for f in frames] for frames in fs]);axes[j].plot(range(24),vals.mean(0),color=color,label=label);axes[j].fill_between(range(24),vals.min(0),vals.max(0),color=color,alpha=.13)
  if j==0:
   baseline=np.array([[f['gold'].count('UNCERTAIN')/20 for f in worlds[f'{seed}-{illustrative}-evidence+withdrawals-combined']['frames']] for seed in seeds]);axes[j].plot(range(24),baseline.mean(0),color='#aebeb3',ls=':',label='Always uncertain (sanity check)')
  axes[j].axvline(10,color='#f1cd76',ls='--',lw=1);axes[j].set(xlim=(0,23),ylim=(-.02,1.03),xlabel='Recorded round',title=title);axes[j].grid(alpha=.12)
 axes[0].legend(frameon=False,fontsize=9,labelcolor=ink);fig.suptitle('Healing Helping Hands | memory erasure + source withdrawal | '+illustrative.upper()+' reference',fontsize=17)
 fig.text(.05,.01,'Lines = mean of 3 paired synthetic corpus seeds; shaded bands = min–max, not confidence intervals. Event before round 10. Scripted propagation; no Qwen or heterogeneous-head efficacy claim.',fontsize=9,color=muted);fig.tight_layout(rect=(0,.04,1,.92));fig.savefig(out/'outcomes.png');plt.close(fig)
 fp=font_manager.findfont('DejaVu Sans');font=lambda n:ImageFont.truetype(fp,n)
 frames=[]
 for t in range(24):
  im=Image.new('RGB',(1600,980),bg);d=ImageDraw.Draw(im);d.text((50,32),'HEALING HELPING HANDS',font=font(38),fill=ink);d.text((50,87),f'Measured replay · {illustrative} reference · seed {seed} · round {t:02d}/23',font=font(20),fill=muted);d.text((50,126),'40 memories erased + 20 source roots withdrawn before round 10',font=font(20),fill='#f1cd76')
  for k,r in enumerate(pair):
   f=r['frames'][t];ox=50+k*790;d.text((ox,180),['Evidence only','Evidence + withdrawal notices'][k],font=font(26),fill=colors[k]);d.text((ox,225),f"Atlas {f['atlas_accuracy']:.0%}   ·   Stale citations {f['stale_fraction']:.1%}",font=font(20),fill=ink)
   for i in range(200):
    x=ox+(i%20)*35;y=275+(i//20)*35;fill='#436552' if f['correct'][i] else '#834f41';outline='#f1cd76' if f['known_withdrawals'][i] else fill;d.rounded_rectangle((x,y,x+31,y+31),radius=3,fill=fill,outline=outline,width=2);symbol={'SUPPORT':'+','REFUTE':'−','UNCERTAIN':'?'}[f['local'][i]];d.text((x+8,y+5),symbol,font=font(17),fill=ink)
    if t==10 and i in corpus['erased']:d.line((x,y,x+31,y+31),fill=ink,width=2)
   d.text((ox,644),'Atlas accuracy (green) / stale citations (gold)',font=font(16),fill=muted)
   for key,col in [('atlas_accuracy','#76ddad'),('stale_fraction','#f1cd76')]:
    pts=[(ox+j/23*696,815-r['frames'][j][key]*130) for j in range(24)];d.line(pts,fill=col,width=3)
   eventx=ox+10/23*696;d.line((eventx,679,eventx,820),fill='#9a8758',width=1);xx=ox+t/23*696;d.line((xx,679,xx,820),fill=ink,width=2);d.text((ox,827),'0',font=font(15),fill=muted);d.text((eventx-7,827),'10',font=font(15),fill=muted);d.text((ox+677,827),'23',font=font(15),fill=muted)
  d.text((50,891),'Green = correct local state · Rust = incorrect · Gold border = received withdrawal · + / − / ? = support / refute / uncertain',font=font(18),fill=muted);d.text((50,925),'White slash = erased scout at round 10. Full recorded curves; cursor selects the state. Logical time. Evaluator overlays are not model inputs.',font=font(17),fill=muted)
  frames.append(im)
 frames[0].save(out/'initial.png');frames[10].save(out/'event.png');frames[-1].save(out/'final.png');frames[0].save(out/'recovery.gif',save_all=True,append_images=frames[1:],duration=[600]*23+[2200],loop=0,optimize=True)
 (out/'artifact-manifest.json').write_text(json.dumps({'attempt':attempt,'mapping':'H1-retrospective-recorded','illustrative_pair':{'seed':seed,'arm':illustrative,'scenario':'combined'},'rounds':list(range(24)),'files':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in out.iterdir() if f.is_file() and f.name!='artifact-manifest.json'}},indent=2))
 print(json.dumps({'completed':completed,'assigned':len(assign),'effects':len(effects),'out':str(out)}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--results',type=Path,required=True);p.add_argument('--attempt',required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();main(a.results,a.attempt,a.out)
