"""Offline equal-capacity broker; no model calls or funded native launcher."""
import copy
from worlds import infer


class Broker:
    def __init__(self,world,n):
        if n not in (1,3):raise ValueError('roster')
        self.world,self.n=world,n;self.rounds=0;self.events=[];self.answer=None
    def packet(self,actor):
        if not 0<=actor<self.n:raise ValueError('actor')
        pending=self.world.coverage()['pending'];fields=sorted(self.world.start()['mutable_fields'])
        return {'start':self.world.start(),'actor':actor,'n':self.n,'round':self.rounds,
                'owned_handles':[h for i,h in enumerate(pending) if self.n==1 or i%3==actor],
                'owned_fields':[k for i,k in enumerate(fields) if self.n==1 or i%3==actor],
                'diagnosis_owner':0,'history':copy.deepcopy(self.events)}
    def step(self,proposals):
        if self.answer is not None:raise ValueError('already_finished')
        if len(proposals)!=self.n or any(type(x)is not list for x in proposals):raise ValueError('proposal_roster')
        before_complete=self.world.coverage()['complete'];packets=[self.packet(i) for i in range(self.n)]
        ops=[]
        for actor,batch in enumerate(proposals):
            if len(batch)>(3 if self.n==1 else 1):raise ValueError('actor_capacity')
            for a in batch:
                if type(a)is not dict or a.get('op') not in ('query','patch','rebalance','finish','wait'):raise ValueError('operation')
                if a['op']=='query' and (set(a)!={'op','handle'} or a['handle'] not in packets[actor]['owned_handles']):raise ValueError('query_ownership')
                if a['op']=='patch' and (set(a)!={'op','field','value'} or a['field'] not in packets[actor]['owned_fields']):raise ValueError('repair_ownership')
                if a['op']=='finish' and (set(a)!={'op','decision','diagnoses'} or a['decision'] not in ('resolve','escalate') or type(a['diagnoses'])is not list):raise ValueError('finish_schema')
                if a['op']=='wait' and set(a)!={'op'}:raise ValueError('wait_schema')
                if a['op']=='rebalance' and actor!=0:raise ValueError('shared_owner')
                ops.append((actor,a))
        cost=sum(3 if a['op']=='rebalance' else 1 if a['op'] in ('query','patch') else 0 for _,a in ops)
        if cost>3:raise ValueError('total_capacity')
        if any(a['op'] in ('patch','rebalance') for _,a in ops) and not before_complete:raise ValueError('round_start_investigation_incomplete')
        queries=[a['handle'] for _,a in ops if a['op']=='query']
        if len(set(queries))!=len(queries):raise ValueError('duplicate_query')
        patches=[a['field'] for _,a in ops if a['op']=='patch']
        if len(set(patches))!=len(patches):raise ValueError('duplicate_patch')
        finishes=[(i,a) for i,a in ops if a['op']=='finish']
        if finishes and any(a['op'] not in ('finish','wait') for _,a in ops):raise ValueError('mixed_finish')
        if any(a['op']=='rebalance' for _,a in ops) and len([a for _,a in ops if a['op']!='wait'])!=1:raise ValueError('shared_conflict')
        self.rounds+=1;receipts=[]
        if queries:receipts=self.world.query(queries)
        for actor,a in ops:
            if a['op'] in ('patch','rebalance'):receipts.append({'actor':actor,'operation':copy.deepcopy(a),'result':self.world.act(a)})
        finish_status='not_requested'
        if finishes:
            if len(finishes)!=self.n or len({i for i,_ in finishes})!=self.n or len({a['decision'] for _,a in finishes})!=1:finish_status='consensus_missing'
            elif any(a['diagnoses'] for i,a in finishes if i!=0):finish_status='diagnosis_owner_violation'
            else:
                a=next(a for i,a in finishes if i==0);candidate={'decision':a['decision'],'diagnoses':copy.deepcopy(a['diagnoses'])}
                # Typed syntax/score validation here is evaluator-side only; grade never enters actor history.
                self.world.evaluate(candidate);self.answer=candidate;finish_status='finished'
        self.events.append({'round':self.rounds,'proposals':copy.deepcopy(proposals),'tool_units':cost,'receipts':copy.deepcopy(receipts),'coverage':self.world.coverage(),'finish_status':finish_status})
        return copy.deepcopy(self.events[-1])


def scripted_run(world,n,max_rounds=10):
    """Exact public-evidence reference fixture; no claim of native coordination."""
    broker=Broker(world,n);repairs=None;answer=None
    while broker.rounds<max_rounds and broker.answer is None:
        proposals=[[] for _ in range(n)]
        if world.coverage()['pending']:
            for actor in range(n):
                proposals[actor]=[{'op':'query','handle':h} for h in broker.packet(actor)['owned_handles'][:3 if n==1 else 1]]
        else:
            if repairs is None:repairs,answer=infer(copy.deepcopy(world.receipts))
            if repairs:
                # Batch independent repairs; preserve the public reader-before-producer dependency.
                limit=1 if n==3 and any(a['field']=='producer_schema' for a in repairs) else 3
                used=set()
                for a in list(repairs)[:limit]:
                    owner=next(i for i in range(n) if a['field'] in broker.packet(i)['owned_fields'])
                    if n==3 and owner in used:continue
                    proposals[owner].append(a);used.add(owner);repairs.remove(a)
            else:
                for actor in range(n):proposals[actor]=[{'op':'finish','decision':answer['decision'],'diagnoses':answer['diagnoses'] if actor==0 else []}]
        broker.step(proposals)
    return broker,world.evaluate(broker.answer) if broker.answer else {'joint_correct':False,'reason':'turn_limit'}
