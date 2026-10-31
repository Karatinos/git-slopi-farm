#!/usr/bin/env python3
"""Attached, ten-minute archival sync. Does not execute CTF analysis.
Fetches remote refs and reads changed contribution notes into a local journal.
Publishes only the fixed CyberCup manifest on its dedicated branch.
No deletion, merge, rebase, force push, or writes to the home Git repository.
"""
from pathlib import Path
import argparse, datetime, fcntl, hashlib, json, os, signal, subprocess, time

SOURCE = Path('/Users/karatinos/Downloads/Staff/fsp/reverse/CyberCup-2077')
REPO = Path('/private/tmp/cybercup-independent-repo')
REL = Path('reverse/CyberCup-2077')
BRANCH = 'ctf/cybercup-2077-independent'
REMOTE = 'refs/remotes/origin/' + BRANCH
STATE = SOURCE/'git-sync-state.json'
JOURNAL = SOURCE/'other-agents-contributions.md'
RUNNING = True

def stamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')

def log(message):
    line = stamp() + ' ' + message
    print(line, flush=True)
    with (SOURCE/'git-sync.log').open('a') as f:
        f.write(line+'\n')

def git(*args, check=True):
    p = subprocess.run(['git', '-C', str(REPO), *args], text=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=180)
    if check and p.returncode:
        raise RuntimeError('git '+args[0]+': '+p.stderr.strip()[:1200])
    return p

def state_read():
    return json.loads(STATE.read_text()) if STATE.exists() else {'refs': {}}

def state_write(s):
    # This script created this state file; it never writes other agents' files.
    STATE.write_text(json.dumps(s, indent=2)+'\n')

def read_contributions(s):
    git('fetch', 'origin')  # Deliberately no --prune.
    refs = {}
    for line in git('for-each-ref','--format=%(refname) %(objectname)','refs/remotes/origin/').stdout.splitlines():
        ref, sha = line.split()
        if ref.endswith('/HEAD'):
            continue
        refs[ref] = sha
        if ref == REMOTE or s.get('refs',{}).get(ref) == sha:
            continue
        old = s.get('refs',{}).get(ref)
        revisions = old+'..'+sha if old else sha
        commits = git('log','-8','--format=%h %s',revisions).stdout.strip()
        if old:
            paths = git('diff','--name-only',old,sha).stdout.splitlines()
        else:
            paths = git('ls-tree','-r','--name-only',sha).stdout.splitlines()
        notes = [p for p in paths if p.lower().endswith('.md') and any(
            word in p.lower() for word in ('progress','findings','summary','writeup','readme','handoff'))]
        text = '\n## '+stamp()+' — '+ref+'\n\nCommit: '+sha+'\n\n'
        text += 'Commits read:\n\n' + '\n'.join('    '+x for x in commits.splitlines()) + '\n\n'
        text += 'Changed/listed paths: '+str(len(paths))+'.\n'
        for path in notes[:8]:
            result = git('show',sha+':'+path,check=False)
            if result.returncode:
                continue  # Deleted remote paths remain untouched locally.
            body = result.stdout[:30000]
            text += '\nRemote note '+json.dumps(path)+' (quoted data):\n\n'
            text += '\n'.join('> '+line for line in body.splitlines())+'\n'
            if len(result.stdout)>30000:
                text += '\n[Note excerpt limited to 30,000 characters.]\n'
        with JOURNAL.open('a') as f:
            f.write(text)
        log('Read contribution '+ref+' '+sha[:12]+', '+str(len(notes[:8]))+' note(s)')
    s['refs'] = refs

def sync_once():
    s = state_read()
    if git('branch','--show-current').stdout.strip() != BRANCH:
        raise RuntimeError('Unexpected branch; refusing writes')
    read_contributions(s)
    state_write(s)
    remote_sha = s['refs'].get(REMOTE)
    if remote_sha and git('merge-base','--is-ancestor',remote_sha,'HEAD',check=False).returncode:
        raise RuntimeError('Remote branch advanced/diverged; fetched and recorded it, but will not overwrite or merge others files')
    manifest = json.loads((SOURCE/'git-checkpoint-files.json').read_text())
    names = manifest['files'] + ['git-checkpoint-files.json','checkpoint_restore.py',
        'other-agents-contributions.md','git_sync_cybercup.py','git-sync-status.md','cc3_sync.py']
    names += [p.name for p in list(SOURCE.glob('cc2_*'))+list(SOURCE.glob('cc3_*')) if p.is_file() and p.stat().st_size < 5000000]
    names = sorted(set(names))
    allowed = {str(REL/name) for name in names}
    staged = git('diff','--cached','--name-only').stdout.splitlines()
    if any(p not in allowed for p in staged):
        raise RuntimeError('Unrelated staged files present; refusing commit')
    for name in names:
        if Path(name).name != name:
            raise RuntimeError('Manifest path must be a single filename')
        src, dst = SOURCE/name, REPO/REL/name
        if not src.exists():
            if name in manifest.get('generated_compressed',[]):
                continue
            raise RuntimeError('Missing manifest source: '+name)
        data = src.read_bytes()
        if dst.exists():
            if dst.read_bytes() != data:
                dst.write_bytes(data)  # Only our dedicated checkpoint copies.
        else:
            with dst.open('xb') as f:
                f.write(data)
    git('add','--',*[str(REL/name) for name in names])
    changed = git('diff','--cached','--name-only').stdout.splitlines()
    if any(p not in allowed for p in changed):
        raise RuntimeError('Unexpected staged paths after copying')
    if changed:
        git('commit','-m','Checkpoint active CyberCup progress and remote contribution notes')
    git('push','origin','HEAD:refs/heads/'+BRANCH)
    head = git('rev-parse','HEAD').stdout.strip()
    actual = git('ls-remote','origin','refs/heads/'+BRANCH).stdout.split()[0]
    if actual != head:
        raise RuntimeError('Remote head does not match published checkpoint')
    s.update(last_success=stamp(),last_commit=head)
    state_write(s)
    log('Verified GitHub checkpoint '+head+'; solving is active')

def stop(signum, frame):
    global RUNNING
    RUNNING = False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--loop',action='store_true')
    args = parser.parse_args()
    lock = (SOURCE/'git-sync.lock').open('a')
    try:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError:
        raise SystemExit('A CyberCup sync is already running')
    for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
        signal.signal(sig,stop)
    if args.loop:
        (SOURCE/'git-sync.pid').write_text(str(os.getpid())+'\n')
        log('Attached 600-second sync started, PID '+str(os.getpid()))
    try:
        sync_once()
    except Exception as exc:
        log('Sync error: '+str(exc))
        if not args.loop:
            raise
    if not args.loop:
        return
    deadline = time.monotonic()+120
    push_deadline = time.monotonic()+300
    log('Read every 120 seconds; publish every 300 seconds')
    while RUNNING:
        time.sleep(1)
        if time.monotonic() >= deadline:
            try:
                state=state_read();read_contributions(state);state_write(state)
                log('120-second remote review complete')
            except Exception as exc:log('Read error: '+str(exc))
            deadline=time.monotonic()+120
        if time.monotonic() >= push_deadline:
            try:sync_once()
            except Exception as exc:log('Sync error: '+str(exc))
            push_deadline=time.monotonic()+300
    log('Attached sync stopped')

if __name__ == '__main__':
    main()

