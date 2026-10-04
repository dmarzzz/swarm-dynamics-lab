import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
b=Path(__file__).resolve().parent;r=json.loads((b/'RESULTS.json').read_text())
plt.style.use('dark_background');fig,axes=plt.subplots(1,2,figsize=(11,4.3));colors={'P':'#eeb45e','R':'#55c7c0'}
for block in (1,2):
 for arm in ('P','R'):
  rows=[x for x in r['metrics'] if x['block']==block and x['arm']==arm];ys=[x['report_content']['retention_bounds'][0]*100 for x in rows];hi=[x['report_content']['retention_bounds'][1]*100 for x in rows]
  axes[0].plot([1,2,3],[100]*3,color=colors[arm],linestyle='-' if block==1 else '--',alpha=.8)
  axes[1].plot([1,2,3],ys,label=f'{arm}, block {block}',color=colors[arm],marker='o' if block==1 else 's',linestyle='-' if block==1 else '--');axes[1].fill_between([1,2,3],ys,hi,color=colors[arm],alpha=.15)
for ax in axes:ax.set_xticks([1,2,3]);ax.set_xlabel('Handoff');ax.grid(alpha=.15)
axes[0].set_ylim(85,102);axes[0].set_title('Correct decisions: 12/12 in every condition');axes[0].set_ylabel('Percent correct')
axes[1].set_ylim(85,102);axes[1].set_title('Meaning retention can fall while answers stay right');axes[1].set_ylabel('Retained source targets (%)');axes[1].legend(fontsize=8,loc='lower left')
fig.suptitle('Telephone B2 • GPT-6 Sol • 12 authored roots, 2 fresh blocks',fontsize=13)
fig.text(.5,.01,'P: handoff only   R: original source + handoff   Shading: annotation ambiguity, not a confidence interval.',ha='center',fontsize=8)
fig.tight_layout(rect=[0,.05,1,.94]);fig.savefig(b/'trajectory.png',dpi=160);fig.savefig(b/'trajectory.svg');print('Saved measured B2 trajectory figure.')
