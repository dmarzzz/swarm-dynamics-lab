from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parent
a=json.loads((root/'Q2-AUDIT.json').read_text())
labels=['Founder actions','Joint decisions','Successor decisions']
values=[a['founder_actions_correct'],a['checkpoints'][0]['correct_actions'],a['checkpoints'][1]['correct_actions']]
denoms=[30,30,6]
fig,ax=plt.subplots(figsize=(11,4.5))
ax.barh(labels,[100*v/n for v,n in zip(values,denoms)],color=['#216d63','#378b7e','#6c9f95']);ax.invert_yaxis();ax.set_xlim(0,115)
for j,(v,n) in enumerate(zip(values,denoms)):ax.text(102,j,f'{v}/{n}',va='center')
ax.set_xlabel('Correct decisions (%)');ax.set_xticks([0,25,50,75,100]);ax.spines[['top','right']].set_visible(False)
ax.set_title('Theseus Q2: repaired consultation and one direct handover passed',pad=18)
fig.text(.5,.035,'One five-member world • 27 native calls • one replacement • no 50-member pilot\nSimple learned-note controller also achieved 30/30; no swarm advantage established.',ha='center',fontsize=10)
fig.tight_layout(rect=(0,.13,1,1));fig.savefig(root/'q2-qualification.png',dpi=160);plt.close(fig)
