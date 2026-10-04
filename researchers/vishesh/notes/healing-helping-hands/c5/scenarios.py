"""Prospective metadata-blind fixtures. No providers, execution or import-time assignments."""
import hashlib,random,importlib.util
from pathlib import Path
_spec=importlib.util.spec_from_file_location("hhh_c4_templates",Path(__file__).resolve().parent.parent/"c4/scenarios.py")
_templates=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(_templates)
FAMILIES=_templates.FAMILIES
LABELS=('SUPPORT','REFUTE','UNCERTAIN')
FORMS={
 'SUPPORT':('measured higher accuracy than the baseline','improved measured accuracy over the baseline','gave more correct answers than the baseline on the same questions','outperformed baseline accuracy'),
 'REFUTE':('measured lower accuracy than the baseline','did not improve measured accuracy over the baseline','gave fewer correct answers than the baseline on the same questions','matched baseline accuracy exactly'),
 'UNCERTAIN':('was never tested for accuracy','has no accuracy result available','was tested for speed only, without accuracy measurements','has only a planned accuracy experiment')}
def opaque_name(split,index):
    # No class or family is an input to identity construction.
    return 'Method '+hashlib.sha256(f'HHH-C5/{split}/{index}'.encode()).hexdigest()[:12]
def fixture(label,index,split='development'):
    if label not in LABELS:raise ValueError('unknown_label')
    name=opaque_name(split,index)
    return {'id':f'C5-{split}-{index}','family':f'qualification-{index%4}','claim':name+' improves accuracy over baseline.','report':name+' '+FORMS[label][index%4]+'.','expected':label,'status':'planned','labels':{}}
def main_fixture(family,label,index,split='development',identity_index=900):
    row=_templates.fixture(family,label,index,split)
    old_name=f'Method {split}-{family}-{index}';old_test=f'Test {split}-{index}'
    name=opaque_name(split,identity_index);test='Task '+hashlib.sha256(f'C5-task/{split}/{identity_index}'.encode()).hexdigest()[:12]
    for field in ('claim','report'):row[field]=row[field].replace(old_name,name).replace(old_test,test)
    row.update(id=f'C5-{split}-{identity_index}',status='planned',labels={})
    return row

def assignments(stage):
    if stage=='S1':
        conditions=[(f,l,i) for f in FAMILIES for l in LABELS for i in range(12)]
        random.Random('C5-main-identity-allocation').shuffle(conditions)
        rows=[main_fixture(f,l,i,'S1',identity_index=k) for k,(f,l,i) in enumerate(conditions)]
        random.Random('C5-main-call-order').shuffle(rows)
        return rows
    if stage!='S0':raise ValueError('unknown_stage')
    # Proposed fresh inputs are materialized only after the new plan is approved/admitted.
    labels=[label for label in LABELS for _ in range(20)]
    random.Random('HHH-C5-label-allocation').shuffle(labels)
    rows=[fixture(label,i,'S0') for i,label in enumerate(labels)]
    random.Random('HHH-C5-call-order').shuffle(rows)
    return rows
