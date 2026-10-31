#!/usr/bin/env python3
"""Restore omitted convenience files from this trusted CyberCup checkpoint.
Run from this directory after cloning. Existing files are verified, never replaced.
Requires the same Unicorn/Python dependencies as the saved state.
"""
from pathlib import Path
import gzip, hashlib, json, pickle, zipfile

ROOT = Path(__file__).resolve().parent
inventory = {x["name"]: x for x in json.loads((ROOT/"artifact-inventory.json").read_text())["files"]}

def restore(name, data):
    expected = inventory[name]["sha256"]
    if hashlib.sha256(data).hexdigest() != expected:
        raise RuntimeError("Checkpoint hash mismatch: " + name)
    out = ROOT/name
    if out.exists():
        if hashlib.sha256(out.read_bytes()).hexdigest() != expected:
            raise RuntimeError("Existing file differs; refusing to overwrite: " + str(out))
        print("Already present and verified:", name)
        return
    with out.open("xb") as f:
        f.write(data)
    print("Restored and verified:", name)

with zipfile.ZipFile(ROOT/"cybercup.zip") as archive:
    for name in ("cybercup.exe", "cybercup.sys"):
        candidates = [n for n in archive.namelist() if Path(n).name == name and not n.startswith("__MACOSX/")]
        if len(candidates) != 1:
            raise RuntimeError("Ambiguous archive member: " + name)
        restore(name, archive.read(candidates[0]))

# This is the task-generated, trusted pickle; do not substitute an untrusted pickle.
with gzip.open(ROOT/"unpack_initialized_state.pkl.gz", "rb") as f:
    saved = pickle.load(f)
images = [bytes(data) for address, data in saved["mem"] if address == 0x140000000]
if len(images) != 1:
    raise RuntimeError("Expected one initialized image in saved state")
restore("unpack_initialized.bin", images[0])
with gzip.open(ROOT/"check_clean.bin.gz", "rb") as f:
    restore("check_clean.bin", f.read())

