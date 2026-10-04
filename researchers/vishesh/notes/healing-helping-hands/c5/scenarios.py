"""Prospective metadata-blind fixtures. No providers, execution or import-time assignments."""
import hashlib,random
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
def assignments(stage):
    if stage!='S0':raise ValueError('C5_has_no_main_stage')
    # Proposed fresh inputs are materialized only after the new plan is approved/admitted.
    labels=[label for label in LABELS for _ in range(20)]
    random.Random('HHH-C5-label-allocation').shuffle(labels)
    rows=[fixture(label,i,'S0') for i,label in enumerate(labels)]
    random.Random('HHH-C5-call-order').shuffle(rows)
    return rows
