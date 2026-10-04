"""Post-run descriptive figure from preserved native S0 summary (no new calls)."""
import argparse
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def plot(source, output):
    s=json.loads(source.read_text())
    fig,axs=plt.subplots(3,2,figsize=(12,10),sharex=True,sharey=True)
    fig.patch.set_facecolor('#f5f4ef')
    panels=[('private','reset'),('private','retain'),('social','reset'),('social','retain'),('pooled','reset'),('pooled','retain')]
    for ax,(comm,state) in zip(axs.flat,panels):
        ax.set_facecolor('#fffefa')
        for h,color in [('A','#bd632d'),('B','#226987')]:
            vals=[]
            for step in range(3):
                ts=[t['error'] for w in s['worlds'] for t in w['pooled' if comm=='pooled' else 'trajectories']
                    if t['history']==h and t['state']==state and t['step']==step and (comm=='pooled' or t['communication']==comm)]
                assert len(ts)==6
                vals.append([sum(t[k] for t in ts)/6*100 for k in ('lower','upper')])
            lo,hi=zip(*vals)
            ax.fill_between(range(3),lo,hi,color=color,alpha=.10)
            ax.plot(range(3),hi,color=color,marker='o' if h=='A' else 's',markersize=6,fillstyle='none',label=h+' upper')
            ax.plot(range(3),lo,color=color,linestyle='--',linewidth=1.5,label=h+' lower')
        ax.set_title(comm.capitalize()+' / '+state,loc='left',fontweight='bold',fontsize=12)
        ax.set_xticks([0,1,2],['First report','Conflicting report','Fresh survey\n+ retraction'])
        ax.set_ylim(-4,104);ax.set_yticks([0,25,50,75,100]);ax.grid(axis='y',alpha=.2)
        ax.spines[['top','right']].set_visible(False)
    for ax in axs[:,0]:ax.set_ylabel('Whole-map error bound (%)')
    handles,labels=axs[0,0].get_legend_handles_labels()
    fig.legend(handles,labels,loc='upper center',bbox_to_anchor=(.5,.94),ncol=4,frameon=False)
    fig.suptitle('Phantom Coast: what changes when complete evidence arrives?',x=.075,y=.99,ha='left',fontsize=19,fontweight='bold')
    fig.text(.075,.95,'Native Jev | six paired worlds | A: false then true; B: true then false',fontsize=11)
    fig.text(.075,.025,'Solid: upper error; dashed: observed wrong. Shading bounds unresolved cells, not statistical confidence.\nEqual world weights; 36 cells/map. Swarm panels use two-of-three assigned votes. Pooled panels use one solver.\nS0-A1 saved native outcomes; fixed evidence only. Overlapping lines indicate the same measured bounds.',fontsize=10,color='#4b5358')
    fig.tight_layout(rect=(.03,.095,.99,.90))
    fig.savefig(output,dpi=160,facecolor=fig.get_facecolor())
    fig.savefig(output.with_suffix('.svg'),facecolor=fig.get_facecolor())
    plt.close(fig)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('summary',type=Path);p.add_argument('output',type=Path)
    a=p.parse_args();plot(a.summary,a.output)
