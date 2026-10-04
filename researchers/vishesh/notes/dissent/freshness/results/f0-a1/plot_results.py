from pathlib import Path
import json,hashlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
base=Path(__file__).resolve().parent
assessment=json.loads((base/'assessment.json').read_text())
labels=['Raw\nsource only','Raw\nhistory + ballots','Explicit eligibility\nsource only','Explicit eligibility\nhistory + ballots']
conditions=['R0','R1','E0','E1'];colors=['#678391','#678391','#147c70','#147c70']
fig,axes=plt.subplots(1,2,figsize=(13,6.8),facecolor='#f7f9fb');fig.subplots_adjust(left=.07,right=.97,top=.70,bottom=.27,wspace=.22)
fig.text(.07,.92,'Does explicit eligibility repair expired-evidence decisions?',fontsize=21,weight='bold',color='#172f40')
fig.text(.07,.85,'48 native requests · raw timestamps versus computed age/eligibility · context absent or present',fontsize=12,color='#4c6372')
for ax,group,title in zip(axes,['fresh','expired'],['Fresh evidence: preserve legitimate decisions','Expired evidence: DEFER required']):
 vals=[assessment['groups'][c+'/'+group] for c in conditions]
 ax.set_facecolor('#f7f9fb');ax.bar(range(4),[v['correct'] for v in vals],color=colors,width=.68)
 for i,v in enumerate(vals):ax.text(i,v['correct']+.12,str(v['correct'])+'/'+str(v['assigned']),ha='center',fontsize=14,weight='bold',color='#172f40')
 ax.set_xticks(range(4),labels,fontsize=10);ax.set_yticks([0,2,4,6]);ax.set_ylim(0,7.1);ax.set_title(title,loc='left',fontsize=13,pad=15)
 ax.set_ylabel('Correct decisions');ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
 for spine in ['top','right','bottom']:ax.spines[spine].set_visible(False)
 ax.tick_params(axis='both',length=0)
fig.text(.07,.13,'Six authored semantic roots; 12 paired task/age cases. Bars describe dependent development responses.',fontsize=11,color='#4c6372')
fig.text(.07,.08,'No field-rate estimate or independent replication. Reserved qualification and the broader dissent study remain unrun.',fontsize=10.5,color='#4c6372')
fig.savefig(base/'diagnostic.png',dpi=170,facecolor=fig.get_facecolor());fig.savefig(base/'diagnostic.svg',facecolor=fig.get_facecolor())
(base/'figure-data.json').write_text(json.dumps({'assessment_sha256':hashlib.sha256((base/'assessment.json').read_bytes()).hexdigest(),'groups':assessment['groups'],'native_requests':48,'independent_field_sample':False},indent=2)+'\n')
print('Diagnostic figure saved from observed group counts.')
