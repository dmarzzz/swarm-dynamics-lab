from pathlib import Path
import os,json
import tempfile
os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'theseus-s50-mpl'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parents[1];a=json.loads((p/'S50-AUDIT.json').read_text());out=Path(__file__).resolve().parents[1]
arms=['interactive','static','broken','retained'];labels=['Interactive handover','Static handover','Broken inheritance','Retained founders'];colors=['#167d8d','#2876b9','#ae5448','#667480']
fig,axes=plt.subplots(1,3,figsize=(13,5.8),gridspec_kw={'width_ratios':[1.3,1,1]});fig.subplots_adjust(left=.17,right=.98,bottom=.24,top=.74,wspace=.38)
for ax,metric,title,limit in zip(axes,['correct','useful','harmful'],['Correct decisions / 300','Useful approvals / 100','Harmful approvals'],[300,100,None]):
 vals=[a['observed_arms'][arm]['observed_decisions'][metric] for arm in arms]
 ax.barh(range(4),vals,color=colors,height=.62);ax.invert_yaxis();ax.set_title(title,fontsize=12,pad=12,loc='left',fontweight='bold');ax.set_yticks(range(4),labels if ax==axes[0] else ['']*4);ax.set_xlim(0,(limit or max(1,max(vals)))*1.16)
 for i,v in enumerate(vals):ax.text(v+(limit or max(1,max(vals)))*.025,i,str(v),va='center',fontsize=12,fontweight='bold')
 ax.spines[['top','right','left']].set_visible(False);ax.tick_params(axis='y',length=0);ax.grid(axis='x',alpha=.18);ax.set_axisbelow(True)
fig.suptitle('Swarm of Theseus · after the founders leave',x=.035,y=.96,ha='left',fontsize=20,fontweight='bold')
fig.text(.035,.85,'50 active positions · one complete replacement wave in each inheritance arm\nOne synthetic world; four paired branches share the same initial ancestor.',fontsize=11,color='#4c5b65')
missing=sum(a['observed_arms'][x]['missing_or_ungraded_decisions'] for x in arms)
fig.text(.035,.12,f"Shared initial checkpoint: {a['observed_initial']['correct']}/300 correct; {a['observed_initial']['harmful']} harmful approval.\nTerminal decisions missing or ungraded: {missing}/1,200. No population confidence interval (independent n=1).",fontsize=10,color='#4c5b65')
fig.text(.035,.035,'Native GPT-6 Sol outcomes. Deterministic learned-evidence reference: 300/300 correct, 100 useful, 0 harmful.\nMemory survival does not establish spontaneous culture or a benefit from dialogue.',fontsize=9,color='#4c5b65')
fig.savefig(out/'S50-RESULTS.png',dpi=180,facecolor='white');fig.savefig(out/'S50-RESULTS.svg',facecolor='white');print(out/'S50-RESULTS.png')
