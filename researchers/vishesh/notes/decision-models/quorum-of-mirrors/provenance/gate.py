"""Receipt-grounded decision gate. Registry authenticity is an external precondition."""
import math
import re

ID = re.compile(r'[A-Za-z0-9][A-Za-z0-9_.:-]{0,63}\Z')


def decide(reports, registry, *, registry_verified=False):
    """Never use author-supplied root labels as proof of independent acquisition.

    `registry_verified=True` is an upstream attestation, not cryptographic verification.
    Any missing/invalid admitted report abstains; suspicious reports are never discarded.
    """
    def refuse(reason, missing=()):
        return {'decision':'DEFER','reason':reason,'missing_receipts':sorted(set(missing))}
    if registry_verified is not True:
        return refuse('registry_not_verified')
    if not isinstance(registry,dict) or not isinstance(reports,list) or not reports:
        return refuse('invalid_input')
    def ident(value):return isinstance(value,str) and ID.fullmatch(value) is not None
    def observation(row):
        return (isinstance(row,dict) and type(row.get('value')) is int and row['value'] in (0,1)
            and type(row.get('q')) in (int,float) and math.isfinite(row['q']) and .5<row['q']<1)
    acquired={}
    # Validate the supplied registry, including contradictory receipts for the same acquisition.
    for receipt_id,entry in registry.items():
        if not ident(receipt_id) or not observation(entry) or not ident(entry.get('acquisition_id')):
            return refuse('invalid_registry')
        value=(entry['value'],entry['q']);source=entry['acquisition_id']
        if source in acquired and acquired[source]!=value:return refuse('inconsistent_registry')
        acquired[source]=value
    roots={};missing=[]
    for report in reports:
        if not observation(report) or not ident(report.get('receipt_id')):
            return refuse('invalid_report')
        receipt_id=report['receipt_id']
        if receipt_id not in registry:
            missing.append(receipt_id);continue
        entry=registry[receipt_id]
        if (report['value'],report['q'])!=(entry['value'],entry['q']):return refuse('observation_mismatch')
        roots[entry['acquisition_id']]=(entry['value'],entry['q'])
    if missing:return refuse('missing_receipt',missing)
    if len(roots)!=3:return refuse('three_verified_acquisitions_required')
    if len({q for value,q in roots.values()})!=1:return refuse('equal_reliability_required')
    choice='ONE' if sum(value for value,q in roots.values())>=2 else 'ZERO'
    return {'decision':choice,'reason':'verified_exact_map','missing_receipts':[],
            'verified_acquisitions':3,'admitted_reports':len(reports)}
