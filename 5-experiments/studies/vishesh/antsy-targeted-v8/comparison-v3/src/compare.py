"""Paired policy evaluation, preserving abstentions and incomplete calls."""
from common import original,repaired
POLICIES=('original_primary','repaired_primary','selective_checker')


def decisions(primary,checker):
    def candidate(record,parser):
        return parser.extract(record['raw_words']) if record and record['status']=='valid' else None
    old=candidate(primary,original);new=candidate(primary,repaired);check=candidate(checker,repaired)
    fallback=bool(new and new['status']!='ok')
    selected=check if fallback else new
    return {'original_primary':{'candidate':old,'used':['P']},'repaired_primary':{'candidate':new,'used':['P']},
            'selective_checker':{'candidate':selected,'used':['P','C'] if fallback else ['P']}}


def evaluate(cases,records):
    rows=[]
    for case in cases:
        r=records.get(case['id'],{});p=r.get('P');c=r.get('C')
        for policy,result in decisions(p,c).items():
            candidate=result['candidate']; value=candidate['value'] if candidate else None
            outcome=('failed_or_missing' if candidate is None else 'unscorable' if case['value'] is None
                     else 'abstain' if value is None else 'correct' if value==case['value'] else 'wrong')
            calls=[r.get(reader) for reader in result['used']]
            elapsed=sum(x['wall_s'] for x in calls) if all(x and x.get('wall_s') is not None for x in calls) else None
            rows.append({'case':case['id'],'policy':policy,'outcome':outcome,'value':value,
                         'checker_needed':'C' in result['used'],'service_time_s':elapsed,
                         'within_45s_each':bool(all(x and x['status']=='valid' and x['wall_s']<=45 for x in calls))})
    totals={}
    for policy in POLICIES:
        selected=[r for r in rows if r['policy']==policy]
        counts={k:sum(r['outcome']==k for r in selected) for k in ('correct','wrong','abstain','unscorable','failed_or_missing')}
        accepted=counts['correct']+counts['wrong']
        totals[policy]={**counts,'assigned':len(cases),'accepted_scorable':accepted,
                        'wrong_per_accepted':counts['wrong']/accepted if accepted else None,
                        'correct_per_assigned':counts['correct']/len(cases) if cases else None,
                        'checker_requests':sum(r['checker_needed'] for r in selected)}
    rescue=harm=shared_wrong=same_wrong=0
    for case in cases:
        pair={r['policy']:r for r in rows if r['case']==case['id']}
        a=pair['repaired_primary']['outcome'];b=pair['selective_checker']['outcome']
        rescue+=a=='abstain' and b=='correct';harm+=a=='abstain' and b=='wrong'
        r=records.get(case['id'],{});p=r.get('P');c=r.get('C')
        if p and c and p['status']==c['status']=='valid' and case['value'] is not None:
            pv=repaired.extract(p['raw_words'])['value'];cv=repaired.extract(c['raw_words'])['value']
            both=pv is not None and cv is not None and pv!=case['value'] and cv!=case['value']
            shared_wrong+=both;same_wrong+=both and pv==cv
    return {'policies':totals,'rescues':rescue,'introduced_wrong_accepts':harm,
            'both_readers_wrong':shared_wrong,'same_wrong_value':same_wrong,'rows':rows,
            'scope':'paired observations; policy service times are accounting estimates, not measured workflow throughput'}


def qualify(cases,records):
    report=evaluate(cases,records)
    return len(cases)==6 and all(c['value'] is not None for c in cases) and all(
      records.get(c['id'],{}).get(reader,{}).get('status')=='valid' for c in cases for reader in ('P','C')) and (
      report['policies']['repaired_primary']['correct']>=4 and report['policies']['repaired_primary']['wrong']==0
      and report['policies']['selective_checker']['wrong']==0)
