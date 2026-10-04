"""Register a frozen public plan; does not queue runs or make model calls."""
import argparse
import re
import urllib.request
from reporting import quiet_client

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--plan-url',required=True);a=p.parse_args()
    try:
        if not re.fullmatch(r'https://github.com/dmarzzz/swarm-lab/blob/[0-9a-f]{40}/.+\.md',a.plan_url):raise ValueError('immutable_plan_required')
        raw=a.plan_url.replace('https://github.com/','https://raw.githubusercontent.com/').replace('/blob/','/')
        with urllib.request.urlopen(raw,timeout=20) as response:plan=response.read().decode()
        for name in ('TLDR','Question and prediction','Setup','Protocol','Metrics'):
            if '\n## '+name+'\n' not in plan:raise ValueError('missing_plan_section')
        import swarm_report as sr
        with quiet_client():
            sr.register('optimal-swarm-size-q1',title='Optimal swarm size: engineering qualification',owner='vishesh',
                        description='TLDR: Qualify synthetic evidence and bounded code-repair tasks before a matched-size study. Treatment: N=1 screening then N=2,4,8,16 under calibrated caps. Comparator: N=1 calibration reference, not a matched size-effect comparison. Metrics: verified on-time success, quality, cost and latency. Limitations: synthetic fixtures, small root count, hosted compute and exploratory calibration.',
                        url=a.plan_url,primary_metric='success',metrics=['success','quality','elapsed_s','cost_exposure_usd'],
                        params={k:{'type':t} for k,t in [('n','int'),('root','int'),('family','str'),('structure','str'),('stage','str')]})
        print('Registered plan metadata. Verify public-plan preflight before any execution.')
    except Exception as exc:
        print('Registration stopped: '+(str(exc) if isinstance(exc,ValueError) else type(exc).__name__));raise SystemExit(2)
