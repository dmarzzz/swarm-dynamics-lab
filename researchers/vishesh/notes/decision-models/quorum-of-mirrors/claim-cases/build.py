"""Authored synthetic claim-fidelity fixtures; no model, network or private context."""
from pathlib import Path
import json,re,hashlib,copy
HERE=Path(__file__).resolve().parent
CONTRACT=('Classify the report claim relative to this complete supplied source record as SUPPORTED, '
 'CONTRADICTED or NOT_ESTABLISHED. The report is authentically bound to this receipt; do not infer origin from wording. '
 'This tests source fidelity, not real-world truth. Missing evidence is not contradiction. Do not interpolate between '
 'observations, equate plans with completed work, or count a quoted/copied report as an independent measurement. '
 'An explicitly corrected entry replaces its named initial value for final-value claims. Lamp off means not lit, '
 'open/closed and running/stopped are mutually exclusive at the same recorded time. Standard kg/g conversion applies. '
 'Repeated report copies add no source evidence.')
# Each label and rationale is authored explicitly, not obtained from a tested controller.
SOURCES=[
 ('polarity', ['At 09:00, lamp L was off.'], [
  ('At 09:00, lamp L was off.','SUPPORTED','The recorded state is off.'),
  ('Lamp L was not lit at 09:00.','SUPPORTED','The contract defines off as not lit.'),
  ('At 09:00, lamp L was on.','CONTRADICTED','On conflicts with off at the same time.'),
  ('At 09:05, lamp L was off.','NOT_ESTABLISHED','No later observation is recorded.')]),
 ('time', ['At 09:00, valve A was closed.','At 10:00, valve A was open.'], [
  ('At 10:00, valve A was open.','SUPPORTED','The 10:00 observation is open.'),
  ('Valve A was not closed at 10:00.','SUPPORTED','Open excludes closed at the same time.'),
  ('At 10:00, valve A was closed.','CONTRADICTED','This transfers the older closed state to the later reading.'),
  ('At 09:30, valve A was open.','NOT_ESTABLISHED','The change time is not supplied.')]),
 ('entity', ['At noon, pump A was running.','At noon, pump B was stopped.'], [
  ('At noon, pump B was stopped.','SUPPORTED','The statement names B.'),
  ('Pump B was not running at noon.','SUPPORTED','Stopped excludes running for B at noon.'),
  ('At noon, pump B was running.','CONTRADICTED','This transfers A\'s state to B.'),
  ('At noon, pump C was running.','NOT_ESTABLISHED','C is not observed.')]),
 ('units', ['Parcel P weighed 2000 grams on this measurement.'], [
  ('Parcel P weighed 2000 grams on this measurement.','SUPPORTED','Literal measured value.'),
  ('Parcel P weighed 2 kilograms on this measurement.','SUPPORTED','2000 grams equals 2 kilograms.'),
  ('Parcel P weighed 2000 kilograms on this measurement.','CONTRADICTED','The unit substitution multiplies the value by 1000.'),
  ('Parcel P weighed 2 kilograms before packing.','NOT_ESTABLISHED','No pre-packing measurement or packing chronology is supplied.')]),
 ('quantifier', ['Exactly three of the four pumps were running during this inspection.'], [
  ('Exactly three of the four pumps were running during this inspection.','SUPPORTED','Explicit count.'),
  ('Not all four pumps were running during this inspection.','SUPPORTED','Exactly three out of four entails not all four.'),
  ('All four pumps were running during this inspection.','CONTRADICTED','All four conflicts with exactly three.'),
  ('Pump D was running during this inspection.','NOT_ESTABLISHED','The identities of the three running pumps are not supplied.')]),
 ('planned_vs_done', ['The inspection is scheduled for Tuesday.','The schedule explicitly excludes Monday.','No completion status is recorded.'], [
  ('The inspection is scheduled for Tuesday.','SUPPORTED','Explicit plan, not a completion claim.'),
  ('Tuesday is the planned day for the inspection.','SUPPORTED','Reformulation of the schedule.'),
  ('The inspection is scheduled for Monday.','CONTRADICTED','Monday is expressly excluded.'),
  ('The inspection was completed on Tuesday.','NOT_ESTABLISHED','No completion status does not mean either completion or noncompletion.')]),
 ('attribution', ['Report B copied the temperature reading from report A.','Report B made no independent temperature measurement.'], [
  ('Report B made no independent temperature measurement.','SUPPORTED','Explicit acquisition limitation.'),
  ('B repeated A\'s temperature reading rather than measuring temperature itself.','SUPPORTED','Copy relation and lack of independent measurement are both stated.'),
  ('Report B independently measured the temperature.','CONTRADICTED','Conflicts with the explicit absence of independent measurement.'),
  ('The actual temperature was 18 degrees.','NOT_ESTABLISHED','Neither a numeric value nor external truth is supplied.')]),
 ('correction', ['The initial entry for container C recorded 10 litres.','A correction replaced that initial entry with 12 litres.'], [
  ('A correction replaced that initial entry with 12 litres.','SUPPORTED','Explicit correction event.'),
  ('The final corrected entry for container C is 12 litres.','SUPPORTED','The named correction replaces the initial value.'),
  ('The final corrected entry for container C is 10 litres.','CONTRADICTED','The final-value claim uses the superseded entry.'),
  ('The actual volume in container C was 12 litres.','NOT_ESTABLISHED','A recorded correction does not certify actual physical volume.')]),
]


def cases():
    result=[]
    for i,(family,source,claims) in enumerate(SOURCES):
        for j,(claim,label,reason) in enumerate(claims):
            result.append({'id':f'CF-{i:02}-{j}','scenario_id':f'CF-{i:02}','family':family,
                'status':'authored synthetic development; inspected, not a holdout',
                'actor':{'contract':CONTRACT,'receipt':{'id':f'receipt-{i:02}','source_sentences':source},
                         'reports':[{'receipt_id':f'receipt-{i:02}','claim':claim}]},
                'gold':{'relation':label,'evidence_spans':source,'rationale':reason}})
    return result


def norm(s):return ' '.join(re.findall(r'[a-z0-9]+',s.lower()))


def predict(actor,policy):
    # The task asks about one repeated claim; contradictory report inputs are unsupported.
    claims={r['claim'] for r in actor['reports']}
    if len(claims)!=1:return 'NOT_ESTABLISHED'
    claim=next(iter(claims));source=actor['receipt']['source_sentences']
    if policy=='abstain_all':return 'NOT_ESTABLISHED'
    if policy=='literal_clause':return 'SUPPORTED' if norm(claim) in {norm(s) for s in source} else 'NOT_ESTABLISHED'
    if policy=='overlap_diagnostic':
        q=set(norm(claim).split());scores=[]
        for s in source:
            words=set(norm(s).split());scores.append(len(q&words)/len(q|words) if q|words else 0)
        return 'SUPPORTED' if max(scores,default=0)>=.65 else 'NOT_ESTABLISHED'
    raise ValueError(policy)


def evaluate(rows):
    outcomes=[];summaries={}
    for policy in ('abstain_all','literal_clause','overlap_diagnostic'):
        records=[]
        for r in rows:
            got=predict(r['actor'],policy);gold=r['gold']['relation']
            records.append({'id':r['id'],'policy':policy,'predicted':got,'gold':gold,'correct':got==gold,
                            'false_support':got=='SUPPORTED' and gold!='SUPPORTED','missed_support':got!='SUPPORTED' and gold=='SUPPORTED'})
        summaries[policy]={key:sum(x[key] for x in records) for key in ('correct','false_support','missed_support')}
        summaries[policy]['by_gold']={g:{'n':sum(x['gold']==g for x in records),'correct':sum(x['gold']==g and x['correct'] for x in records)} for g in ('SUPPORTED','CONTRADICTED','NOT_ESTABLISHED')}
        outcomes+=records
    return {'cases':len(rows),'authored_scenario_units':len({r['scenario_id'] for r in rows}),
            'scope':'Limited lexical diagnostics; no strong semantic baseline, no model effectiveness or headroom inference.',
            'summary':summaries,'outcomes':outcomes}


def main():
    rows=cases();results=evaluate(rows)
    (HERE/'cases.json').write_text(json.dumps(rows,indent=2)+'\n')
    (HERE/'diagnostics.json').write_text(json.dumps(results,indent=2)+'\n')
    text=['# Claim-fidelity casebook','32 inspected development cases / eight authored source scenarios. SUPPORTED means the source warrants the claim; CONTRADICTED means it warrants an incompatible claim; NOT_ESTABLISHED means neither. Source binding is assumed authenticated. These are not real-world truth labels, model results or independent samples.']
    for i,(family,source,_) in enumerate(SOURCES):
        text += [f'## CF-{i:02}: {family.replace("_"," ")}', '\n'.join('> '+s for s in source), '| Case | Report claim | Expected relation | Reason |','|---|---|---|---|']
        for r in rows[i*4:i*4+4]:text.append('| '+r['id']+' | '+r['actor']['reports'][0]['claim']+' | '+r['gold']['relation']+' | '+r['gold']['rationale']+' |')
    rendered='\n\n'.join(text)
    rendered=re.sub(r'\|\n\n(?=\|)', '|\n', rendered)
    (HERE/'CASEBOOK.md').write_text(rendered+'\n')
    print(json.dumps(results['summary'],indent=2))
if __name__=='__main__':main()
