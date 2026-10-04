"""One supervised local relay, reverse tunnel and remote worker; no retries.

SSH aliases/configuration and admission receipts are private operator inputs.
This command neither allocates machines nor copies credentials to them.
"""
import argparse
import json
from pathlib import Path
import shlex
import subprocess
import sys
import time
from common import digest, save
from rd5_runtime import PORT, URL, verify_native


def remote_command(checkout, args):
    return 'cd '+shlex.quote(str(checkout))+' && exec python3 '+shlex.join(
        ['researchers/vishesh/notes/dissent/rd5/src/rd5_cli.py']+list(args))


def stop_children(children):
    for child in reversed(children):
        if child.poll() is None:child.terminate()
    for child in reversed(children):
        try:child.wait(timeout=5)
        except subprocess.TimeoutExpired:child.kill();child.wait(timeout=5)


def supervise(a):
    packet=json.loads(a.packet.read_text());receipt=json.loads(a.receipt.read_text())
    verify_native(packet,receipt,check_host=False)
    a.output.mkdir(parents=True,exist_ok=False)
    ssh=['ssh','-F',str(a.ssh_config),'-o','BatchMode=yes','-o','ConnectTimeout=8',
         '-o','ServerAliveInterval=5','-o','ServerAliveCountMax=2']
    children=[];logs=[];status={'stage':packet['stage'],'run_id':receipt['run_id'],'ready':False}
    started=time.monotonic()
    try:
        for name in ('relay','worker'):
            logs.append((a.output/(name+'.log')).open('w'))
        relay=subprocess.Popen([sys.executable,str(Path(__file__).with_name('rd5_cli.py')),'relay',
            '--packet',str(a.packet),'--receipt',str(a.receipt),'--credential-file',str(a.credential_file),'--ledger',str(a.ledger)],
            stdout=logs[0],stderr=subprocess.DEVNULL)
        children.append(relay)
        tunnel=subprocess.Popen(ssh+['-N','-o','ExitOnForwardFailure=yes','-R',f'{PORT}:127.0.0.1:{PORT}',a.host_alias],
                                stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        children.append(tunnel)
        # Probe through the actual remote loopback, not a process-liveness delay.
        probe='import json,urllib.request; print(json.dumps(json.load(urllib.request.urlopen('+repr(URL+'/health')+',timeout=3))))'
        expected={'ready':True,'packet_sha256':digest(packet)}
        for _ in range(10):
            if any(c.poll() is not None for c in children):break
            checked=subprocess.run(ssh+[a.host_alias,'python3 -c '+shlex.quote(probe)],capture_output=True,timeout=15)
            try:ready=checked.returncode==0 and json.loads(checked.stdout)==expected
            except (ValueError,UnicodeError):ready=False
            if ready:status['ready']=True;break
            time.sleep(1)
        if not status['ready']:raise RuntimeError('remote_relay_not_ready')
        command=remote_command(a.remote_checkout,['run','--packet',a.remote_packet,'--receipt',a.remote_receipt,'--output',a.remote_output])
        worker=subprocess.Popen(ssh+[a.host_alias,command],stdout=logs[1],stderr=subprocess.DEVNULL);children.append(worker)
        while worker.poll() is None:
            if relay.poll() is not None or tunnel.poll() is not None or time.monotonic()-started>1800:
                raise RuntimeError('supervised_child_exited_or_deadline')
            time.sleep(.25)
        status.update(worker_exit=worker.returncode,relay_exit=relay.poll(),tunnel_exit=tunnel.poll())
        if worker.returncode!=0:raise RuntimeError('worker_failed')
    except Exception:
        status['operational_failure']=True
        raise RuntimeError('supervised_attempt_failed') from None
    finally:
        status['elapsed_seconds']=time.monotonic()-started
        status['child_exit_before_cleanup']=[c.poll() for c in children]
        stop_children(children)
        status['local_children_stopped']=all(c.poll() is not None for c in children)
        status['remote_worker_exit_verified']=status.get('worker_exit') is not None
        save(a.output/'supervisor.json',status)
        for f in logs:f.close()


if __name__=='__main__':
    p=argparse.ArgumentParser()
    for name in ('packet','receipt','credential-file','ledger','ssh-config','output'):
        p.add_argument('--'+name,type=Path,required=True)
    for name in ('host-alias','remote-checkout','remote-packet','remote-receipt','remote-output'):
        p.add_argument('--'+name,required=True)
    try:supervise(p.parse_args())
    except Exception:
        print(json.dumps({'supervisor':'failed','details':'see sanitized supervisor.json'}));raise SystemExit(1)
