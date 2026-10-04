"""Plot all scripted S1 cells; each mean contains the same 12 paired worlds."""
import argparse
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

COLORS={'no_verification':'#909bab','degree':'#bb9cff','random':'#efcf76','coverage':'#51d7ad'}
LABELS={'no_verification':'No checks','degree':'Highest degree','random':'Random','coverage':'Uncovered neighborhoods'}


def plot(directory, output):
    cells=[json.loads(p.read_text()) for p in Path(directory).rglob('summary.json')]
    cells=[c for c in cells if c['params']['stage']=='S1']
    assert len(cells)==18 and all(c['invalid']==0 for c in cells)
    assert len({(c['params']['bridges'],c['params']['attacker_pass'],c['params']['verification_budget']) for c in cells})==18
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'text.color':'#edf2f7',
        'axes.labelcolor':'#bdc9d9','xtick.color':'#bdc9d9','ytick.color':'#bdc9d9',
        'axes.edgecolor':'#42516b','axes.facecolor':'#121d2e','figure.facecolor':'#0c1220'})
    fig,axes=plt.subplots(2,3,figsize=(18,11.8),sharex=True,sharey=True)
    for i,bridges in enumerate([1,3]):
        for j,rate in enumerate([.1,.5,.9]):
            ax=axes[i,j]
            rows=sorted([c for c in cells if c['params']['bridges']==bridges and c['params']['attacker_pass']==rate],key=lambda c:c['params']['verification_budget'])
            assert [c['params']['verification_budget'] for c in rows]==[2,4,8]
            for arm,color in COLORS.items():
                ms=[c['arms'][arm]['metrics'] for c in rows]
                xs=[m['malicious_admission'] for m in ms]; ys=[m['rare_accuracy'] for m in ms]
                ax.plot(xs,ys,'o-',color=color,lw=2,ms=6,label=LABELS[arm],alpha=.95)
                if arm=='coverage':
                    for x,y,k in zip(xs,ys,[2,4,8]): ax.annotate(str(k),(x,y),xytext=(5,-17) if k==4 else (5,7),textcoords='offset points',color=color,fontsize=11)
            ax.set_title(f'{bridges} bridge swap'+('' if bridges==1 else 's')+f' | attacker pass {rate:.0%}',pad=14,fontsize=14)
            ax.set_xlim(-.035,1.055); ax.set_ylim(-.04,1.08)
            ax.xaxis.set_major_formatter(PercentFormatter(1)); ax.yaxis.set_major_formatter(PercentFormatter(1))
            ax.grid(alpha=.14); ax.set_axisbelow(True)
            if i==1: ax.set_xlabel('Adversarial identities admitted (lower is better)',labelpad=12)
            if j==0: ax.set_ylabel('Rare facts resolved correctly (higher is better)',labelpad=12)
    handles,labels=axes[0,0].get_legend_handles_labels()
    fig.legend(handles,labels,loc='upper center',bbox_to_anchor=(.5,.885),ncol=4,frameon=False)
    fig.suptitle('Where verification helps — and where it admits attackers',fontsize=25,x=.055,ha='left',y=.965)
    fig.text(.055,.914,'SCRIPTED S1 • 12 paired worlds • 18 conditions • equal budgets of 2, 4 or 8 checks • zero API calls',fontsize=14,color='#efcf76')
    fig.text(.055,.055,'Each line connects budgets 2 → 4 → 8; green numbers label the coverage heuristic. No-check reference spends zero.',fontsize=12,color='#bdc9d9')
    fig.text(.055,.027,'Synthetic graph and modeled verification service. Descriptive means; no LLM result or general Sybil-resistance guarantee.',fontsize=12,color='#bdc9d9')
    fig.subplots_adjust(left=.08,right=.975,top=.80,bottom=.135,hspace=.29,wspace=.18)
    output=Path(output)
    if output.exists(): raise FileExistsError(output)
    fig.savefig(output,dpi=100); plt.close(fig)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('directory',type=Path);ap.add_argument('output',type=Path);a=ap.parse_args()
    plot(a.directory,a.output)
