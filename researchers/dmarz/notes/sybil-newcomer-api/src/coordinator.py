"""Exact-runtime gates. Post-mortem-only commits do not invalidate qualifications."""
import study
import yaml


def enqueue(sr, stage):
    p=study.params(stage)
    runs=sr.runs('sybil-newcomer-api',limit=5000)
    if any(r.get('params',{}).get('batch')==p['batch'] for r in runs):
        raise ValueError('batch_exists_no_replay')
    prerequisite={'Q0':'S0','S1':'Q0'}.get(stage)
    if prerequisite:
        candidates=[r for r in runs if r.get('params',{}).get('stage')==prerequisite and
                    r.get('params',{}).get('source_hash')==p['source_hash'] and r['status']=='done' and
                    r.get('metrics',{}).get('invalid')==0 and r.get('metrics',{}).get('qualification_passed')==1]
        if len(candidates)!=1: raise ValueError('exact_runtime_qualification_required')
    exp=yaml.safe_load((study.ROOT/'experiment.yaml').read_text())
    sr.register(exp.pop('id'),**exp)
    return sr.enqueue('sybil-newcomer-api',[p],tags=[stage,p['backend'],'exploratory'])
