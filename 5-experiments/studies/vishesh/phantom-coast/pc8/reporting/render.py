import json,sys,html
from pathlib import Path
p=Path(sys.argv[1]);rs=json.loads((p/'records.json').read_text());s=json.loads((p/'summary.json').read_text());ds={r['id']:r for r in json.loads((p/'decisions.json').read_text())};parts=['<!doctype html><meta charset="utf-8"><title>PC8 native report interpretation</title><style>body{font:16px system-ui;max-width:1100px;margin:30px auto}pre{white-space:pre-wrap;background:#f5f5f5;padding:15px}details{padding:10px;border-bottom:1px solid #aaa}</style><h1>PC8 report interpretation — measured native results</h1><p>All assigned cases. Local serialized requests and safe raw answer fields, not full HTTP envelopes or hidden reasoning. Model evidence extraction; downstream Bayesian consequences are scripted.</p><pre>'+html.escape(json.dumps(s,indent=2))+'</pre>']
for r in rs:
 parts.append('<details><summary>'+html.escape(r['id']+' '+r['status']+' native field errors='+str(ds[r['id']]['native']['field_errors']))+'</summary><h3>Saved request</h3><pre>'+html.escape(json.dumps(r.get('request'),indent=2))+'</pre><h3>Safe returned answers</h3><pre>'+html.escape(json.dumps(r.get('checked',r.get('failure_code')),indent=2))+'</pre><h3>Scores and parser comparator</h3><pre>'+html.escape(json.dumps(ds[r['id']],indent=2))+'</pre></details>')
(p/'native-replay.html').write_text(''.join(parts))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,ax=plt.subplots(1,2,figsize=(11,4.8),layout='constrained');fig.suptitle('PC8: report interpretation qualification',weight='bold',fontsize=17)
for j,(field,color,label,offset) in enumerate([('native_correct','#297d83','Native',-.18),('parser_correct','#697c9e','Rule parser',.18)]):
 for i,c in enumerate(s['cells']):
  ax[0].bar(i+offset,c[field]/c['fields'],.34,color=color,label=label if i==0 else None);ax[0].text(i+offset,c[field]/c['fields']+.025,f"{c[field]}/{c['fields']}",ha='center',fontsize=10)
ax[0].set(xticks=[0,1],xticklabels=['Structured','Prose'],ylim=(0,1.18),ylabel='Correct record classifications / assigned');ax[0].legend(frameon=False)
for i,c in enumerate(s['cells']):
 ax[1].bar(i,c['native_protected_errors'],color='#b6584f');ax[1].text(i,c['native_protected_errors']+.15,f"{c['native_protected_errors']}/{c['protected_denominator']} harmed",ha='center')
ax[1].set(xticks=[0,1],xticklabels=['Structured','Prose'],ylim=(0,max(2,max(c['native_protected_errors'] for c in s['cells'])+2)),ylabel='Wrong / omitted eligible records in preservation cases')
for a in ax:a.spines[['top','right']].set_visible(False)
fig.supxlabel(f"{s['overall']['roots']} roots; {s['assigned']} dependent requests. Synthetic authored histories. Qualification: {s.get('qualification_passed','not applicable')}.",fontsize=10);fig.savefig(p/'results-frame.png',dpi=160)
