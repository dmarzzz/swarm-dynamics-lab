"""Synthetic local fixtures only: no credentials or model/collector calls."""
import importlib.util,json,pathlib,sys,tempfile
from unittest.mock import patch
ROOT=pathlib.Path(__file__).resolve().parents[5]

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    obj=importlib.util.module_from_spec(spec);sys.modules[name]=obj;spec.loader.exec_module(obj);return obj

collect=load('collect_probe',ROOT/'scripts/collect.py')
result={}
with tempfile.TemporaryDirectory() as td:
    d=pathlib.Path(td);(d/'raw').mkdir();(d/'raw/fixture.jsonl').touch()
    base=dict(id='x:1',source='x',url='https://example.invalid/1',text='synthetic',found_by='shadow/test',topic='llm-agent-swarms')
    rows=[dict(base,likes=1),dict(base,likes=2)]
    class Args: source=None;no_repo_check=True;min_score=1;min_batch=1;size=10
    with patch.object(collect,'RAW',d/'raw'),patch.object(collect,'CAND',d/'cand'),patch.object(collect,'SEEN',d/'seen'),patch.object(collect,'library_seen',return_value=set()),patch.object(collect,'load_seen',return_value=set()),patch.object(collect,'jl_read',return_value=rows),patch.object(collect,'score',return_value=3):
        try:collect.cmd_batch(Args())
        except KeyError as e:result['duplicate_replacement_crash']=str(e)

src=ROOT/'researchers/shadow/notes/capture-memory-mix/src';sys.path.insert(0,str(src))
worker=load('worker_probe',src/'worker.py')
p=dict(tasks='0-0',seeds=[1],arms=['A','B'],memory='1',world='synthetic',dose=0,stage='synthetic',split='dev',cfg={})
def record(arm):
    return dict(task_id=0,seed=1,arm=arm,validity={'ok':True},evaluation={'captured':True,'frac_original_T':.5,'delta_original':0},cost_actual={'model_calls':2,'cost_usd':.25},backend='old/model')
with tempfile.TemporaryDirectory() as td:
    d=pathlib.Path(td)
    out=d/'valid.jsonl';out.write_text(''.join(json.dumps(record(arm))+'\n' for arm in ['A','B']))
    with patch.object(worker.sim,'run_episode') as net:
        summary=worker.execute(p,out,None,'new/model')
        result['resume_ignored_changed_model']=not net.called
        result['resume_cost_usd']=summary['metrics']['cost_usd']
        result['saved_record_cost_usd']=.5
    out=d/'duplicate.jsonl';out.write_text(''.join(json.dumps(record('A'))+'\n' for _ in range(2)))
    with patch.object(worker.sim,'run_episode') as net:
        summary=worker.execute(p,out,None,'new/model')
        result['duplicate_arm_skips_missing_arm']=not net.called and summary['stats']['B']['n']==0
print(json.dumps(result,indent=2))
