"""Saved-data scientific overview: all assignments, missingness and discrete ticks."""
import json,sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE));import instrument as i
src=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
rows=json.loads(src.read_text());lookup={r['id']:r for r in rows};roots=list(dict.fromkeys(a['root'] for a in i.assignments()));worlds={c['id']:c for c in i.study.roots()};codes={'deploy':'D','inspect':'I','wait':'W','refresh':'F'}
def plot(tick,file):
 fig,ax=plt.subplots(figsize=(14,10.3),dpi=140);fig.patch.set_facecolor('#101923');ax.set_facecolor('#101923');ax.set_xlim(-1.35,4);ax.set_ylim(-1.6,13.1);ax.axis('off')
 fig.suptitle('Immune Response · native verification comparison',color='white',fontsize=20,y=.975)
 ax.text(-1.3,12.9,f'{len(rows)}/48 episodes recorded · '+('initial world' if not tick else f'through tick {tick}')+' · six authored roots within three service families',color='#b8c6d4',fontsize=10)
 for col,(guarded,repeat) in enumerate(((False,1),(True,1),(False,2),(True,2))):
  ax.text(col+.45,12.45,('Guarded' if guarded else 'Unguarded')+f' · repeat {repeat}',ha='center',color='white',fontsize=11)
 for index,(root,branch) in enumerate((r,b) for r in roots for b in ('confirmed','contradicted')):
  y=11.4-index;c=worlds[root+'-'+branch]
  ax.text(-.06,y+.35,root+'\n'+('fault persists' if branch=='confirmed' else 'already recovered'),ha='right',va='center',color='#dce8ef',fontsize=8)
  for col,(guarded,repeat) in enumerate(((False,1),(True,1),(False,2),(True,2))):
   row=lookup.get(f'{root}/{branch}/{"guarded" if guarded else "unguarded"}/{repeat}');color='#344452';text='NOT RECORDED';edge='#52606d'
   if row is not None:
    if tick==0:healthy=branch=='contradicted';text='current: '+('healthy' if healthy else 'process down');color='#164c3d' if healthy else '#643b34'
    else:
     x=row['trace'][tick-1];color='#164c3d' if x['healthy'] else '#643b34';proposal=codes.get(x['proposal']['action'],x['proposal']['action']);executed=codes.get(x['action']['action'],x['action']['action']);text=f'{proposal} → {executed}   served {x["served_opportunity"]}/1\n'+('diagnosis correct' if x['diagnosis_correct'] else 'diagnosis WRONG')
     if x['guard_denied']:text+=' · denied'
     edge='#f7a46c' if x['unnecessary_proposed'] or not x['diagnosis_correct'] else '#52606d'
     if tick==2:text+='\n'+('joint PASS' if row['qualified'] else 'joint FAIL')+' · '+('verified' if row['post_action_verified'] else 'verification n/a' if row['post_action_verified'] is None else 'not verified')
   ax.add_patch(Rectangle((col,y),.92,.82,facecolor=color,edgecolor=edge,linewidth=2));ax.text(col+.46,y+.41,text,color='white',ha='center',va='center',fontsize=7)
 ax.text(-1.3,-1.03,'D deploy · I inspect · W wait · F registry refresh. Arrow: proposed → executed. Green/red fill: healthy/unhealthy post-state.\nOrange border: unnecessary proposal or incorrect diagnosis. Gray: missing, never zero. “Joint” requires outcome, proposal contract and diagnosis.\nEach tick has one service opportunity; deployment consumes it. Guard protection is not learned competence. Native episodes, not independent population samples.',color='#b8c6d4',fontsize=8,va='top')
 fig.tight_layout(rect=(0,0,1,.95));fig.savefig(file,facecolor=fig.get_facecolor());plt.close(fig)
files=[]
for tick in range(3):
 file=out/f'verification-tick-{tick}.png';plot(tick,file);files.append(file)
images=[Image.open(p).convert('RGB') for p in files];images[0].save(out/'verification-replay.gif',save_all=True,append_images=images[1:],duration=[1600,2000,3200],loop=0)
(out/'visualization.json').write_text(json.dumps({'source':'saved native episodes','recorded_episodes':len(rows),'assigned':48,'native_calls_by_renderer':0,'frames':'initial world,post-tick1,post-tick2','missing':'gray; not recorded','health':'actual post-state','service':'pre-action health and no executed deployment','proposal_contract':'separate from protected outcome','animated_time':'discrete simulator ticks, not wall-clock time'},indent=2))
print(json.dumps({'rendered':True,'episodes':len(rows),'output':str(out)}))
