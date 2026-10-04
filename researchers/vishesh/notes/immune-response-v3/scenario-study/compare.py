import json,sys,os,tempfile
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'immune-scenario-mpl'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
team,solo,reference=[json.loads(Path(p).read_text()) for p in sys.argv[1:4]];out=Path(sys.argv[4]);out.parent.mkdir(parents=True,exist_ok=True)
labels=['Rule solver','Team / retain','Team / reset','Team / revision','Solo / retain'];colors=['#93a4ad','#f2ae72','#8dacf6','#66d9bd','#ed91c3'];cases=list(team['means']);fig,axes=plt.subplots(1,4,figsize=(18,9),facecolor='#102330')
fig.suptitle('Immune Response · recovery and restraint are different requirements',color='white',fontsize=23,y=.96)
for ax,case in zip(axes,cases):
 metrics=[reference['means'][case]['retain'],*[team['means'][case][a] for a in ['retain','reset','revision_check']],solo['means'][case]['retain']]
 ax.set_facecolor('#183440');ax.barh(range(5),[x['healthy_ticks'] for x in metrics],color=colors,height=.55);ax.set_yticks(range(5),labels,color='white',fontsize=11);ax.invert_yaxis();ax.set_xlim(0,7.9);ax.set_xticks(range(7));ax.tick_params(colors='white');ax.set_title(case.replace('_',' '),color='white',fontsize=16,pad=18);ax.set_xlabel('Healthy customer ticks / 6',color='white');ax.grid(axis='x',alpha=.15)
 for i,m in enumerate(metrics):ax.text(m['healthy_ticks']+.1,i,f"{m['healthy_ticks']:.0f}/6",color='white',va='center',fontsize=11)
fig.text(.04,.07,'Native A2 and solo: one episode per displayed condition. Rule solver is a feasibility baseline, not model evidence.',color='#c3d1d8',fontsize=13)
fig.text(.04,.035,'The team preserved the healthy control but often failed to repair incidents. Solo repaired incidents but damaged the healthy control. Neither establishes robust immunity.',color='#c3d1d8',fontsize=12)
fig.tight_layout(rect=[0,.13,1,.87]);fig.savefig(out,dpi=100,facecolor=fig.get_facecolor());plt.close(fig)
