import argparse,json,statistics,shutil,hashlib
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from engine import SCENARIOS
COLORS=['#a87832','#245c9c','#8abdb0','#19856f']
def analyze(root,out,site=None):
 out.mkdir(parents=True,exist_ok=True);results={};confusions={}
 for attempt in ('practical-01','practical-02'):
  p=root/attempt;m=json.loads((p/'manifest.json').read_text());rows=json.loads((p/'summary.json').read_text());assert m['terminal_counts']=={'completed':180}
  groups={}
  for scenario in SCENARIOS:
   groups[scenario]={}
   for arm in ('central-append','central-verified','peer-append','peer-blind','peer-verified'):
    xs=[r for r in rows if r['scenario']==scenario and r['arm']==arm];fields={}
    for k in ('post_event_error','final_error','final_retention','final_stale','traffic_items','false_invalidations_peak'):
     values=[statistics.mean(r[k] for r in xs if r['seed']==seed) for seed in (8701,8702,8703)];fields[k]={'mean':statistics.mean(values),'min':min(values),'max':max(values),'per_corpus':values}
    groups[scenario][arm]=fields
    # Descriptive confusion counts only; repeated queries are not independent trials.
    counts={g:{v:0 for v in ('SUPPORT','REFUTE','UNCERTAIN','MISSING')} for g in ('SUPPORT','REFUTE','UNCERTAIN')}
    for x in xs:
     w=json.loads((p/(x['id']+'.json')).read_text())
     for f in w['frames'][10:]:
      for i,pred in enumerate(f['local']):counts[f['gold'][i%20]]['MISSING' if f['missing'][i] else pred]+=1
    confusions[f'{attempt}/{scenario}/{arm}']=counts
  results[attempt]={'packet_cap':m.get('packet_cap',4),'seconds':m['seconds'],'source':m['plan']['commit'],'conditions':groups}
 contrasts={}
 for scenario in SCENARIOS:
  a=results['practical-01']['conditions'][scenario];b=results['practical-02']['conditions'][scenario];base=b['central-append']['post_event_error']['mean'];peer=b['peer-verified']['post_event_error']['mean'];retention_loss=b['central-append']['final_retention']['mean']-b['peer-verified']['final_retention']['mean']
  contrasts[scenario]={'cap4_minus_cap16_peer_error':a['peer-verified']['post_event_error']['mean']-peer,'central_append_minus_peer16_error':base-peer,'relative_reduction_vs_append':(base-peer)/base if base else None,'retention_loss_vs_append':retention_loss,'utility_rule_met_at16':bool(base and (base-peer)/base>=.2 and retention_loss<=.03),'peer16_minus_central_verified_error':peer-b['central-verified']['post_event_error']['mean']}
 payload={'scope':'Paired engineering sensitivity; 3 reused semantic corpora, 2 nested layouts; no independent replication or CI claim.','attempts':results,'contrasts':contrasts,'confusion_counts':confusions}
 (out/'capacity-results.json').write_text(json.dumps(payload,indent=2)+'\n')
 fig=plt.figure(figsize=(18,10),dpi=110);gs=fig.add_gridspec(2,2,height_ratios=[1,1],hspace=.38,wspace=.26);ax=fig.add_subplot(gs[0,:]);selections=[('practical-01','central-append','Central append'),('practical-01','central-verified','Central verified'),('practical-01','peer-verified','Peer verified · cap 4'),('practical-02','peer-verified','Peer verified · cap 16')]
 for j,(attempt,arm,label) in enumerate(selections):
  vs=[results[attempt]['conditions'][s][arm]['post_event_error'] for s in SCENARIOS];pos=[i+(j-1.5)*.18 for i in range(6)];means=[v['mean'] for v in vs];ax.bar(pos,means,width=.17,color=COLORS[j],label=label);ax.errorbar(pos,means,yerr=[[v['mean']-v['min'] for v in vs],[v['max']-v['mean'] for v in vs]],fmt='none',color='#37434a',lw=.8,capsize=2)
 ax.set_xticks(range(6),SCENARIOS);ax.set_ylim(0,.65);ax.set_ylabel('Post-event incorrect-or-missing queries');ax.legend(ncol=4,loc='upper left',fontsize=10);ax.spines[['top','right']].set_visible(False)
 ax=fig.add_subplot(gs[1,0]);bx=fig.add_subplot(gs[1,1]);labels=[];rets=[]
 for j,(attempt,arm,label) in enumerate(selections):
  v=results[attempt]['conditions']['combined'][arm];x=v['traffic_items']['mean']/1000;y=v['post_event_error']['mean'];ax.scatter([x],[y],s=130,color=COLORS[j]);ax.annotate(label,(x,y),xytext=(8,10 if j!=2 else -20),textcoords='offset points',fontsize=10);labels.append(label);rets.append(v['final_retention']['mean'])
 ax.set(xlim=(40,112),ylim=(.1,.49),xlabel='Transmitted item copies (thousands)',ylabel='Mean incorrect-or-missing queries',title='Combined incident: accuracy has a traffic cost');ax.spines[['top','right']].set_visible(False)
 bx.bar(range(4),rets,color=COLORS);bx.set_xticks(range(4),['Central\nappend','Central\nverified','Peer verified\ncap 4','Peer verified\ncap 16']);bx.set_ylim(0,1.15);bx.set_title('Combined incident: retain legitimate new evidence');bx.set_ylabel('Final fraction of curator queries retaining R4')
 for j,v in enumerate(rets):bx.text(j,v+.025,f'{v:.1%}',ha='center')
 bx.spines[['top','right']].set_visible(False);fig.suptitle('Healing Helping Hands | verified corrections help; distribution is not free',fontsize=19,weight='bold');fig.text(.08,.015,'360 completed worlds, but only 3 reused semantic corpora. Layouts are averaged within corpus; whiskers show corpus ranges, not confidence intervals.\nLogical rounds and item-copy traffic, not hardware latency or bytes. Central bulk reads are deliberately strong. No new model inference; Qwen/Laya remain unqualified.',fontsize=10);fig.subplots_adjust(bottom=.12,top=.90);fig.savefig(out/'capacity-outcomes.png');plt.close(fig)
 if site is not None:
  for name in ('capacity-outcomes.png','capacity-results.json'):shutil.copyfile(out/name,site/name)
  p=site/'index.html';html=p.read_text();html=html.replace('All-scenario results</a>', 'All-scenario results</a> · <a href="capacity-outcomes.png">Compare both packet capacities</a>');p.write_text(html)
  p=site/'render-provenance.json';provenance=json.loads(p.read_text());provenance['comparison_compiler_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();p.write_text(json.dumps(provenance,indent=2))
 print(json.dumps({'contrasts':contrasts}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--site',type=Path);a=p.parse_args();analyze(a.root,a.out,a.site)
