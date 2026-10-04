"""Supervised SSH orchestration and verified offline collection for admitted RD6.

Paths/account receipts remain private. This does not provision, claim, approve or
copy credentials. A worker launch uses the already verified exclusive host.
"""
import argparse
import json
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
from native import Transport, supervise, live_preflight, bound_admission
from native_gates import BASE, read, evidence, require, sha
from cases import digest
from native_report import save, audit_bundle, reconcile_accounting


def collect(source, destination, expected, *, copier=shutil.copytree):
    """Publishing failure preserves the source; never retries experimental work."""
    source=Path(source);destination=Path(destination)
    audit_bundle(source,expected)
    require(not destination.exists(),'destination_exists')
    destination.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.rd6-copy-',dir=destination.parent) as temp:
        staged=Path(temp)/'bundle';copier(source,staged)
        audit_bundle(staged,expected)
        staged.rename(destination)
    return {'artifact_delivery':'verified','model_calls':0,'bundle_sha256':expected}


def remote_preflight(a, packet, admission_sha, *, command=subprocess.run):
    remote='cd '+shlex.quote(a.remote_checkout)+' && exec '+shlex.join([
        'timeout','--signal=TERM','--kill-after=5','30','python3',
        'researchers/vishesh/notes/dissent/reopening/native.py','check-worker',
        '--packet',a.remote_packet,'--admission',a.remote_admission,
        '--admission-sha256',admission_sha,'--out',a.remote_out])
    result=command(['ssh','-F',a.ssh_config,'-o','BatchMode=yes','-o','StrictHostKeyChecking=yes',
                    '-o','ConnectTimeout=8',a.host_alias,remote],capture_output=True,text=True,timeout=40)
    require(result.returncode==0,'remote_startup_check_failed')
    try: acknowledgment=json.loads(result.stdout)
    except Exception: acknowledgment=None
    expected={'worker_preflight':'ready','packet_sha256':digest(packet),'admission_sha256':admission_sha}
    require(acknowledgment==expected,'remote_startup_acknowledgment')
    return expected


def launch(a):
    packet=read(a.packet);admission_sha=sha(a.admission)
    receipt=bound_admission(a.admission,admission_sha)
    live_preflight(packet,receipt)
    runtime=evidence(receipt['runtime'])
    require(runtime.get('ssh_config_sha256')==sha(a.ssh_config)
            and runtime.get('host_alias')==a.host_alias
            and runtime.get('remote_checkout')==a.remote_checkout
            and runtime.get('gnu_timeout_verified') is True,'supervisor_runtime_binding')
    out=Path(a.out);out.mkdir(parents=True,exist_ok=False)
    relay=[sys.executable,str(BASE/'native.py'),'relay','--packet',a.packet,'--admission',a.admission,
           '--admission-sha256',admission_sha,
           '--credential',a.credential,'--ledger',a.ledger,'--out',str(out/'relay')]
    # SSH receives paths/aliases only; no credential value or owner conversation.
    remote='cd '+shlex.quote(a.remote_checkout)+' && exec '+shlex.join([
        'timeout','--signal=TERM','--kill-after=10','1800','python3',
        'researchers/vishesh/notes/dissent/reopening/native.py','worker',
        '--packet',a.remote_packet,'--admission',a.remote_admission,
        '--admission-sha256',admission_sha,'--out',a.remote_out])
    worker=['ssh','-F',a.ssh_config,'-o','BatchMode=yes','-o','StrictHostKeyChecking=yes',
            '-o','ConnectTimeout=8','-o','ServerAliveInterval=5','-o','ServerAliveCountMax=2',
            '-o','ExitOnForwardFailure=yes','-R','127.0.0.1:18469:127.0.0.1:18469',a.host_alias,remote]
    status={'attempt':receipt['attempt'],'execution':'starting','remote_worker_stop':'unverified'}
    try:
        status['phase']='remote_startup_check'
        acknowledgment=remote_preflight(a,packet,admission_sha)
        save(out/'remote-startup-check.json',acknowledgment)
        supervise(relay,worker,Transport(packet),diagnostics=status)
        status['execution']='worker_returned_success'
    except Exception:
        status['execution']='stopped_or_ambiguous'
        raise ValueError('supervised_attempt_stopped') from None
    finally:
        status['local_process_groups']='cleanup_attempted'
        status['next']='Verify remote worker and relay stopped, collect/reconcile artifacts, finalize and complete scientific post-mortem before release.'
        save(out/'supervisor.json',status)


def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='cmd',required=True)
    l=sub.add_parser('supervise')
    for arg in ('packet','admission','credential','ledger','ssh-config','host-alias','remote-checkout','remote-packet','remote-admission','remote-out','out'):
        l.add_argument('--'+arg,required=True)
    c=sub.add_parser('collect')
    for arg in ('source','destination','bundle-sha256'):c.add_argument('--'+arg,required=True)
    r=sub.add_parser('reconcile')
    for arg in ('results','bundle-sha256','relay-directory','out'):r.add_argument('--'+arg,required=True)
    a=p.parse_args()
    try:
        if a.cmd=='collect':print(json.dumps(collect(a.source,a.destination,a.bundle_sha256)))
        elif a.cmd=='reconcile':
            packet,rows=audit_bundle(a.results,a.bundle_sha256)
            relay=Path(a.relay_directory)
            result=reconcile_accounting(packet,rows,read(relay/'accounting.json'),relay/'relay-events.jsonl')
            require(not Path(a.out).exists(),'reconciliation_output_exists');save(a.out,result)
            print(json.dumps({'reconciled':True,'model_calls':0}))
        else:launch(a)
    except Exception:
        print(json.dumps({'status':'blocked_or_stopped','model_retry':False}));raise SystemExit(1) from None


if __name__=='__main__':main()
