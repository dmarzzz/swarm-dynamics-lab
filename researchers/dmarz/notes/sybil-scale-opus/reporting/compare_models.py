"""Descriptive model-A-minus-model-B comparison (A=this study, e.g. Opus; B=Haiku or Sonnet) on identical assignments, paired by world.

Post-collection only: reads saved records of both cohorts, never calls a model.
Usage: compare_models.py <sonnet-run-dir> <haiku-run-dir> <output-dir>
Each run dir holds assignments.jsonl.gz and episodes.jsonl.gz as fetched from its server.
"""
import argparse,csv,json,sys
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'src'))
import analyze

KEY=('n','arm','checks','attacker_pass','visibility')
METRICS=('rare_accuracy','task_accuracy')


def load(path):
    assigned=analyze.read_rows(path/'assignments.jsonl.gz')
    rows=analyze.read_rows(path/'episodes.jsonl.gz')
    return assigned,{r['id']:r for r in rows}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('sonnet',type=Path);ap.add_argument('haiku',type=Path);ap.add_argument('output',type=Path)
    a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=True)
    s_assigned,s_rows=load(a.sonnet);h_assigned,h_rows=load(a.haiku)
    # Pairing is only valid if both cohorts received byte-identical assignments.
    assert s_assigned==h_assigned,'assignments_differ'
    cells=defaultdict(lambda:defaultdict(list))
    for assignment in s_assigned:
        s,h=s_rows[assignment['id']],h_rows[assignment['id']]
        if s['kind']!='pilot' or s['status']!='completed' or h['status']!='completed':continue
        key=tuple(s[k] for k in KEY)
        for m in METRICS:
            cells[key][m].append((s['task'],s['evaluation'][m],h['evaluation'][m]))
        # Admission is computed before the model call, so seat shares must agree exactly.
        assert s['evaluation']['bad_seat_share']==h['evaluation']['bad_seat_share'],'admission_differs'
    out=[]
    for key,mm in sorted(cells.items()):
        row=dict(zip(KEY,key))
        for m,triples in mm.items():
            diffs=[sv-hv for _,sv,hv in sorted(triples)]
            row.update({m+'_sonnet':sum(sv for _,sv,_ in triples)/len(triples),m+'_haiku':sum(hv for _,_,hv in triples)/len(triples),
                        m+'_diff':sum(diffs)/len(diffs)})
            iv=analyze.interval(diffs);row[m+'_diff_low'],row[m+'_diff_high']=iv
            row['clusters']=len(triples)
        out.append(row)
    with (a.output/'model-comparison-cells.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
    diffs=[r['rare_accuracy_diff'] for r in out]
    overall={'cells':len(out),'mean_cell_rare_accuracy_diff':sum(diffs)/len(diffs),
             'cells_sonnet_higher':sum(d>0 for d in diffs),'cells_haiku_higher':sum(d<0 for d in diffs),'cells_equal':sum(d==0 for d in diffs)}
    (a.output/'model-comparison-summary.json').write_text(json.dumps({'overall':overall,'cells':out},indent=2)+'\n')
    print(json.dumps(overall))


if __name__=='__main__':main()
