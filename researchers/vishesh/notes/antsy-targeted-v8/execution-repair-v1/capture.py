"""Offline-tested single-call supervisor. Not a native launcher or admission authority.

The caller supplies an already admitted command and input hash. Tests use only
local fake children. No retry, secret-bearing environment fallback or raw log return.
"""
import hashlib,json,math,os,signal,subprocess,time
from pathlib import Path
from telemetry import inspect_phases


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def append(path,event):
    with Path(path).open('a') as f:
        f.write(json.dumps(event)+'\n');f.flush();os.fsync(f.fileno())


def stop_group(proc):
    # Dedicated start_new_session process group only; never match arbitrary PIDs.
    try:os.killpg(proc.pid,signal.SIGTERM)
    except ProcessLookupError:pass
    try:proc.wait(timeout=1)
    except subprocess.TimeoutExpired:pass
    try:os.killpg(proc.pid,signal.SIGKILL)
    except ProcessLookupError:pass
    proc.wait(timeout=1)


def candidate_valid(value):
    if not isinstance(value,dict) or set(value)!= {'candidate','raw_words'} or not isinstance(value['raw_words'],list):return False
    c=value['candidate']
    if not isinstance(c,dict) or c.get('status') not in ('ok','missing','ambiguous') or c.get('contract')!='anchor-row-v2':return False
    if c['status']=='ok':
        import re
        if not isinstance(c.get('value'),str) or not re.fullmatch(r'\d+\.\d{2}',c['value']):return False
    elif c.get('value') is not None:return False
    return isinstance(c.get('evidence'),list) and isinstance(c.get('reasons'),list)


def run_once(command,directory,image,expected_sha256,deadline_s=90,eligibility_s=45):
    if any(type(x) not in (int,float) or not math.isfinite(x) or x<=0 for x in (deadline_s,eligibility_s)) or deadline_s<eligibility_s or deadline_s>90:
        raise ValueError('invalid_time_contract')
    directory=Path(directory);image=Path(image)
    if not image.is_file() or image.is_symlink() or sha(image)!=expected_sha256:raise ValueError('input_mismatch')
    if directory.parent.is_symlink() or not directory.parent.is_dir():raise ValueError('unsafe_output_parent')
    directory.mkdir(mode=0o700,exist_ok=False)
    private=directory/'private';private.mkdir(mode=0o700)
    journal=directory/'calls.jsonl';started=time.monotonic();proc=None
    result={'status':'error','category':'spawn_error','returncode':None,'latency_eligible':False,'input_sha256':expected_sha256}
    # Only worker parameters are substituted; command itself is never published.
    argv=[str(x).replace('{out}',str(private/'output.json')).replace('{phases}',str(private/'phases.jsonl')) for x in command]
    env={k:os.environ[k] for k in ('PATH','LANG','LC_ALL','SYSTEMROOT') if k in os.environ}
    env.update(OMP_NUM_THREADS='1',OMP_THREAD_LIMIT='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',PYTHONHASHSEED='0',PYTHONUNBUFFERED='1')
    append(journal,{'status':'started','monotonic_s':started})
    try:
        with (private/'stdout.bin').open('xb') as stdout,(private/'stderr.bin').open('xb') as stderr:
            try:
                proc=subprocess.Popen(argv,stdin=subprocess.DEVNULL,stdout=stdout,stderr=stderr,env=env,start_new_session=True)
                try:code=proc.wait(timeout=max(0,deadline_s-(time.monotonic()-started)))
                except subprocess.TimeoutExpired:
                    result['category']='timeout';stop_group(proc);code=proc.returncode
                else:
                    result['category']='worker_signal' if code<0 else 'worker_exit' if code else 'invalid_output'
                result['returncode']=code
            finally:
                if proc is not None:stop_group(proc)
                stdout.flush();stderr.flush();os.fsync(stdout.fileno());os.fsync(stderr.fileno())
    except (OSError,subprocess.SubprocessError):
        if proc is not None and proc.poll() is None:stop_group(proc)
        if result['category']!='timeout':result['category']='supervisor_error'
    except BaseException:
        if proc is not None:stop_group(proc)
        result['category']='supervisor_interrupted'
        raise
    finally:
        result['wall_s']=time.monotonic()-started
        phase=inspect_phases(private/'phases.jsonl',complete=result['returncode']==0)
        result['phases']=phase
        output=private/'output.json'
        if result['returncode']==0 and result['category'] not in ('timeout','supervisor_error','supervisor_interrupted'):
            try:
                if output.is_symlink() or not output.is_file() or not candidate_valid(json.loads(output.read_text())):raise ValueError()
                if not phase['valid'] or not phase['complete']:result['category']='invalid_phases'
                else:result.update(status='valid',category='ok',latency_eligible=result['wall_s']<=eligibility_s)
            except (OSError,ValueError,TypeError):result['category']='invalid_output'
        result['streams']={n:{'bytes':(private/n).stat().st_size,'sha256':sha(private/n)} for n in ('stdout.bin','stderr.bin') if (private/n).is_file()}
        result['phase_file_sha256']=sha(private/'phases.jsonl') if (private/'phases.jsonl').is_file() and not (private/'phases.jsonl').is_symlink() else None
        result['output_sha256']=sha(output) if output.is_file() and not output.is_symlink() else None
        result['direct_child_reaped']=proc is None or proc.poll() is not None
        result['group_cleanup_requested']=proc is not None
        append(journal,{'status':result['status'],'category':result['category'],'wall_s':result['wall_s']})
        (directory/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    return result
