"""Bounded orchestration core. Transport is injected; this module makes no network calls."""
import concurrent.futures
import copy
import json
import time
import threading
from failures import SafeFailure,safe_code
from tasks import strict_json
from response_contract import schema_for,validate_shape


def validate_plan(plan,items,required=None):
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
    if required is not None and any(not set(required[item])<=set(deps[item]) for item in items):
        raise ValueError("plan_missing_required_edges")
    return deps


def execute(public,n,slots,deadline_s,integration_reserve_s,call,event=lambda x:None,strict_contract=False,enforce_dependencies=False):
    """call(messages, absolute_deadline, actor, phase, item) -> JSON text.

    Receives public data ONLY. Time/usage enforcement belongs to the transport and ledger.
    Tests inject scripted responses; those are never reported as model performance.
    """
    if n not in (1,2,4,8,16) or type(slots) is not int or slots<1 or not 0<integration_reserve_s<deadline_s:
        raise ValueError('invalid_execution_limits')
    start=time.monotonic();deadline=start+deadline_s;work_deadline=deadline-integration_reserve_s
    histories=[[{'role':'system','content':'Solve the supplied synthetic task. Return raw JSON only, with no Markdown code fences or commentary. You have no evaluator access.'},
                {'role':'user','content':json.dumps(public,sort_keys=True)}] for _ in range(n)]
    used=set();completed={};deps={};failures=[];fatal_stop=threading.Event()
    def emit(kind,**fields):event({'t':time.monotonic()-start,'kind':kind,**fields})
    def turn(actor,phase,prompt,until,item=None):
        if fatal_stop.is_set():raise SafeFailure('transport_failed')
        if time.monotonic()>=until:raise SafeFailure('deadline')
        used.add(actor)
        histories[actor].append({'role':'user','content':prompt})
        emit('service_start',actor=actor,phase=phase,item=item)
        try:
            try:
                answer=call(copy.deepcopy(histories[actor]),until,actor,phase,item)
            except Exception as exc:
                failure=SafeFailure(safe_code(exc))
                if failure.fatal or (strict_contract and failure.code in ('incomplete_response','provider_refusal')):fatal_stop.set()
                raise failure from None
            if time.monotonic()>until:raise TimeoutError('late_response')
            try:
                parsed=strict_json(answer)
            except ValueError:
                emit('response_format',actor=actor,phase=phase,item=item,valid_json=False,fenced=isinstance(answer,str) and answer.strip().startswith('```'))
                if strict_contract:raise SafeFailure('schema_output_invalid') from None
                raise
            if strict_contract:
                try:validate_shape(parsed,schema_for(public,phase,item))
                except ValueError:
                    emit('schema_validation',actor=actor,phase=phase,item=item,valid=False)
                    raise SafeFailure('schema_output_invalid') from None
                emit('schema_validation',actor=actor,phase=phase,item=item,valid=True)
            emit('response_format',actor=actor,phase=phase,item=item,valid_json=True,fenced=False)
            histories[actor].append({'role':'assistant','content':answer})
            return parsed
        finally:emit('service_end',actor=actor,phase=phase,item=item)
    try:
        plan_prompt='Plan the work. Return {"dependencies": {item_id: [prerequisite_item_ids]}} for every requested item. Choose a valid acyclic plan. Roster includes you: '+str(n)
        plan_parsed=False
        try:
            plan=turn(0,'plan',plan_prompt,work_deadline);plan_parsed=True
            deps=validate_plan(plan,public['items'],public['dependencies'] if enforce_dependencies else None)
        except (ValueError,TypeError):
            reason='invalid_dependency_map' if plan_parsed else 'invalid_json'
            emit('plan_repair_reason',reason=reason)
            deps=validate_plan(turn(0,'plan_repair','Your plan failed '+reason+'. Return raw JSON only, no Markdown code fences or commentary: a valid dependencies object for all requested items.',work_deadline),public['items'],public['dependencies'] if enforce_dependencies else None)
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
                        code=safe_code(exc) if isinstance(exc,SafeFailure) else 'malformed_output'
                        completed[item]={'failure':code};failures.append({'item':item,'code':code})
                        if isinstance(exc,SafeFailure) and (exc.fatal or fatal_stop.is_set()):raise
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
        artifact=None;failure=safe_code(exc) if isinstance(exc,(SafeFailure,TimeoutError)) else 'malformed_output'
    elapsed=time.monotonic()-start
    emit('terminal',failure=failure,elapsed_s=elapsed)
    return {'artifact':artifact,'elapsed_s':elapsed,'failure':failure,'fatal':bool(failure and SafeFailure(failure).fatal),'work_failures':failures,'configured_n':n,'used_contexts':sorted(used),'completed_items':len(completed),'work_artifacts':copy.deepcopy(completed),'plan_dependencies':copy.deepcopy(deps)}
