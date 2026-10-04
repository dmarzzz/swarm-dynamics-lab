"""Publication figure from retained S1 records; no model calls."""
import argparse,json,statistics
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=argparse.ArgumentParser();p.add_argument('directory',type=Path);a=p.parse_args();r=a.directory
es=json.loads((r/'episodes.json').read_text());summary=json.loads((r/'summary.json').read_text())
fig,axes=plt.subplots(1,3,figsize=(16,6),layout='constrained')
colors={'team':'#236eac','single':'#ba5d2d','uniform':'#52815b'}
for ax,field,title in zip(axes,('unique','loss','wrong'),('Distinct inspections out of 12','Decision loss (%)','Known wrong / 36 (%)')):
 for i,policy in enumerate(('team','single','uniform')):
  vals=[]
  for guard in (False,True):
   items=[e for e in es if e['policy']==policy and e['report']=='misleading' and e['guard']==guard]
   def metric(e):
    m=e['endpoint']['metrics'];w=m['whole']
    return m['unique_cells'] if field=='unique' else 100*(w['wrong']+.25*w['missing'])/36 if field=='loss' else 100*w['wrong']/36
   vals.append(statistics.mean(map(metric,items)))
   ax.scatter([int(guard)+(i-1)*.07]*len(items),[metric(e) for e in items],color=colors[policy],alpha=.18,s=28)
  ax.plot([0,1],vals,'o-',label=policy.capitalize(),color=colors[policy],linewidth=2.3)
 ax.set_xticks([0,1],['Repeats allowed','Coverage guard']);ax.set_xlim(-.25,1.25);ax.set_title(title);ax.grid(axis='y',alpha=.2);ax.spines[['top','right']].set_visible(False)
 if field=='unique':ax.set_ylim(0,13);ax.set_yticks([0,3,6,9,12])
 else:ax.set_ylim(bottom=0)
axes[0].legend(frameon=False)
delta=summary['overall']['primary_loss_difference']*100
fig.suptitle(f'Phantom Coast PC-3 · misleading reports\nTeam guard effect: {delta:+.2f} percentage points of decision loss',fontsize=19)
fig.supxlabel('Lines: means across 8 paired roots. Dots: individual roots. Loss = (wrong + 0.25 × unknown) / 36.\nGuard removes measured cells from legal actions. Uniform already samples without replacement. Single model; exploratory evidence.',fontsize=10)
fig.savefig(r/'results-frame.png',dpi=140);plt.close(fig)
print(json.dumps({'output':str(r/'results-frame.png'),'independent_roots':8,'no_new_model_calls':True}))
