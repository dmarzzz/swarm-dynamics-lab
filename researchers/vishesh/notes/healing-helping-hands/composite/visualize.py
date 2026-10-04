"""Measured C1 confusion matrices and temporal replay; no model calls."""
import json,io,argparse,sys
from pathlib import Path
from definition import ARMS,LABELS,assess
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def semantic(rows,path,fixture=False):
    s=assess(rows);fig,axes=plt.subplots(1,3,figsize=(17,6),dpi=110)
    for ax,a in zip(axes,ARMS):
        mat=np.array([[s[a]['confusion'][k][p] for p in (*LABELS,'MISSING')] for k in LABELS]);ax.imshow(mat,cmap='Blues',vmin=0,vmax=max(1,max(sum(r) for r in mat)))
        for y in range(3):
            for x in range(4):ax.text(x,y,str(mat[y,x]),ha='center',va='center',color='white' if mat[y,x]>max(1,max(sum(r) for r in mat))*.55 else 'black')
        ax.set_xticks(range(4),['Support','Refute','Uncertain','Missing'],rotation=25);ax.set_yticks(range(3),['Support','Refute','Uncertain']);ax.set_title(f'{a} | {s[a]["accuracy"]:.1%} correct');ax.set_xlabel('Predicted');ax.set_ylabel('Expected')
    fig.suptitle(('SCRIPTED — NOT MODEL EVIDENCE\n' if fixture else '')+'Healing Helping Hands | does Jev correct or follow Qwen?',fontsize=19)
    p=s['paired'];fig.text(.05,.035,f'Assigned {len(rows)} cases; complete paired observations {p["complete"]}. Qwen errors corrected: {p["qwen_wrong_corrected"]}; correct Qwen damaged: {p["qwen_right_damaged"]}; anchoring: {p["anchoring"]}.\nAccuracy delta composite − Jev-only: {p["accuracy_delta"]:+.1%}. Finite synthetic templates; no independent-case inference.',fontsize=11);fig.tight_layout(rect=[0,.2,1,.9]);fig.savefig(path);plt.close(fig)

def temporal(worlds,path,seed=8801,scenario='combined',fixture=False):
    images=[]
    for t in range(30):
        fig,axes=plt.subplots(3,4,figsize=(18,11),dpi=100,gridspec_kw={'width_ratios':[1,1,1,1.5]});policies=('central-append','central-verified','peer-verified')
        for y,m in enumerate(ARMS):
            for x,p in enumerate(policies):
                w=worlds[f'{seed}-{m}-{p}-{scenario}'];f=w['frames'][t];rgb=[(.66,.69,.73) if f['missing'][i] else ((.12,.58,.44) if f['correct'][i] else (.78,.27,.31)) for i in range(200)];ax=axes[y,x];ax.imshow(np.array(rgb).reshape(10,20,3));ax.set_xticks([]);ax.set_yticks([]);ax.set_title(f'{m}\n{p} | error {f["incorrect_or_missing"]:.1%}',fontsize=11)
                for i in f['disconnected']:ax.add_patch(plt.Rectangle((i%20-.5,i//20-.5),1,1,fill=False,edgecolor='black',lw=.5))
            ax=axes[y,3]
            for p in policies:
                w=worlds[f'{seed}-{m}-{p}-{scenario}'];ax.plot(range(30),[f['incorrect_or_missing'] for f in w['frames']],label=p)
            ax.axvline(t,color='black');ax.axvspan(10,20,color='orange',alpha=.1);ax.set_ylim(0,1);ax.set_title(f'{m} | wrong or missing');ax.legend(fontsize=8);ax.set_xlabel('Logical round')
        fig.suptitle(('SCRIPTED — NOT MODEL EVIDENCE\n' if fixture else '')+f'Healing Helping Hands | Qwen + Jev | round {t:02d}/29\nSeed {seed} • {scenario} • 200 curators per grid • packet cap 16',fontsize=18)
        fig.text(.04,.02,'Green correct with evidence • red wrong • gray missing • outline disconnected from central index\nEvent before round 10; reconnection before round 20. Recorded post-exchange states; programmed propagation, not model deliberation.',fontsize=11);fig.tight_layout(rect=[0,.065,1,.9]);b=io.BytesIO();fig.savefig(b,format='png');plt.close(fig);b.seek(0);images.append(Image.open(b).convert('RGB'))
    images[-1].save(path.with_suffix('.png'));images[0].save(path,save_all=True,append_images=images[1:],duration=450,loop=0)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--results',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(exist_ok=True,parents=True);rows=json.loads((a.results/'observations.json').read_text());semantic(rows,a.out/'labels.png');assignments=json.loads((a.results/'world-assignments.json').read_text())
    if assignments:
        worlds={w['id']:json.loads((a.results/(w['id']+'.json')).read_text()) for w in assignments if w['status']=='completed'}
        if len(worlds)==270:temporal(worlds,a.out/'recovery.gif')
