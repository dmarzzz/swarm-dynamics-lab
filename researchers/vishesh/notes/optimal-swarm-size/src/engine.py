"""Bounded orchestration core. Transport is injected; this module makes no network calls."""
import concurrent.futures
import copy
import json
import time
from tasks import strict_json


def validate_plan(plan,items):
    if type(plan) is not dict or set(plan)!= {'dependencies'} or type(plan['dependencies']) is not dict or set(plan['dependencies'])!=set(items):
        raise ValueError('plan_shape')
    deps=plan['dependencies']
    for item,parents in deps.items():
        if type(parents) is not list or any(type(p) is not str or p not in items or p==item for p in parents) or len(set(parents))!=len(parents):
            raise ValueError('plan_dependencies')
    done=set()
    while len(done)<len(items):
        ready={i for i in items if i not in done and set(deps[i])<=done}
        if not ready:raise ValueError('plan_cycle')
        done.update(ready)
    return deps


def execute(public,n,slots,deadline_s,integration_reserve_s,call,event=lambda x:None):
    """call(messages, absolute_deadline, actor, phase, item) -> JSON text.

    Receives public data ONLY. Time/usage enforcement belongs to the transport and ledger.
    Tests inject scripted responses; those are never reported as model performance.
    """
    if n not in (1,2,4,8,16) or type(slots) is not int or slots<1 or not 0<integration_reserve_s<deadline_s:
        raise ValueError('invalid_execution_limits')
    start=time.monotonic();deadline=start+deadline_s;work_deadline=deadline-integration_reserve_s
    histories=[[{'role':'system','content':'Solve the supplied synthetic task. Return only JSON. You have no evaluator access.'},
                {'role':'user','content':json.dumps(public,sort_keys=True)}] for _ in range(n)]
    used=set();completed={};failures=[]
    def emit(kind,**fields):event({'t':time.monotonic()-start,'kind':kind,**fields})
    def turn(actor,phase,prompt,until,item=None):
        if time.monotonic()>=until:raise TimeoutError('deadline')
        used.add(actor)
        histories[actor].append({'role':'user','content':prompt})
        emit('service_start',actor=actor,phase=phase,item=item)
        try:
            try:
                answer=call(copy.deepcopy(histories[actor]),until,actor,phase,item)
            except Exception:
                raise RuntimeError("transport_failed") from None
            if time.monotonic()>until:raise TimeoutError('late_response')
            parsed=strict_json(answer)
            histories[actor].append({'role':'assistant','content':answer})
            return parsed
        finally:emit('service_end',actor=actor,phase=phase,item=item)
    try:
        plan_prompt='Plan the work. Return {"dependencies": {item_id: [prerequisite_item_ids]}} for every requested item. Choose a valid acyclic plan. Roster includes you: '+str(n)
        try:deps=validate_plan(turn(0,'plan',plan_prompt,work_deadline),public['items'])
        except (ValueError,TypeError):
            deps=validate_plan(turn(0,'plan_repair','Your plan was invalid. Return a valid dependencies object for all requested items.',work_deadline),public['items'])
        emit('plan',dependencies=deps)
        pending=set(public['items']);running={};idle=set(range(n));work_counts=[0]*n
        executor=concurrent.futures.ThreadPoolExecutor(max_workers=min(n,slots))
        try:
            while pending or running:
                if time.monotonic()>=work_deadline:raise TimeoutError('work_deadline')
                for item in sorted(pending):
                    if not idle or len(running)>=slots:break
                    if not set(deps[item])<=set(completed):continue
                    actor=min(idle,key=lambda a:(work_counts[a],a));work_counts[actor]+=1;idle.remove(actor);pending.remove(item)
                    ledger={p:completed[p] for p in deps[item]}
                    prompt='Complete only item '+item+'. Return {"artifact": <your partial answer or replacement source for this item>}. Declared prerequisite ledger entries: '+json.dumps(ledger)
                    emit('dispatch',actor=actor,item=item)
                    future=executor.submit(turn,actor,'work',prompt,work_deadline,item)
                    running[future]=(actor,item)
                if not running:raise ValueError('scheduler_stalled')
                finished,_=concurrent.futures.wait(running,timeout=max(0,work_deadline-time.monotonic()),return_when=concurrent.futures.FIRST_COMPLETED)
                if not finished:raise TimeoutError('work_deadline')
                for future in finished:
                    actor,item=running.pop(future);idle.add(actor)
                    try:
                        output=future.result()
                        if type(output) is not dict or set(output)!= {'artifact'}:raise ValueError('work_shape')
                        completed[item]=output['artifact']
                    except Exception as exc:
                        completed[item]={'failure':type(exc).__name__};failures.append({'item':item,'class':type(exc).__name__})
                    emit('work_complete',actor=actor,item=item)
        except TimeoutError:
            failures.append({'class':'TimeoutError','phase':'work'})
        finally:
            for future in running:future.cancel()
            # Transport must bound in-flight calls; their reservations are retained until settlement.
            executor.shutdown(wait=True,cancel_futures=True)
        final=turn(0,'integrate','Produce the full final artifact using the task output contract. These are all recorded work artifacts; missing items are incomplete: '+json.dumps(completed,sort_keys=True),deadline)
        artifact=json.dumps(final);failure=None
    except Exception as exc:
        artifact=None;failure=type(exc).__name__
    elapsed=time.monotonic()-start
    emit('terminal',failure=failure,elapsed_s=elapsed)
    return {'artifact':artifact,'elapsed_s':elapsed,'failure':failure,'work_failures':failures,'configured_n':n,'used_contexts':sorted(used),'completed_items':len(completed)}
