#!/usr/bin/env python3
"""Pull the LIVE CTFd benchmark catalog (register + list + download files).
NO model calls, NO spend. Run in a REAL terminal (reaches ctfd.snowyx.dev).

    source farm/.secrets/ctfd.env
    python3 research/ctfd_pull.py
Writes farm/data/ctf_bench/catalog.json and downloads files under
farm/data/ctf_bench/files/.
"""
from __future__ import annotations
import json, os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # farm/
from farm.config import DATA_DIR
from farm.adapters import CTFdSource

url = os.environ.get("CTFD_URL"); hdr = os.environ.get("CTFD_HEADER"); code = os.environ.get("CTFD_REGCODE")
if not (url and hdr and code):
    sys.exit("set CTFD_URL / CTFD_HEADER / CTFD_REGCODE (source farm/.secrets/ctfd.env)")

print(f"connecting to {url} ...")
src = CTFdSource(url, hdr, code)
recs = src.read()
cat = [{"id": r["id"], "name": r["name"], "category": r["category"],
        "points": r["points"], "endpoint": r["endpoint"],
        "files": [b for _, b in r["files"]],
        "desc": (r["statement"] or "")[:1200]} for r in recs]
out = DATA_DIR / "ctf_bench" / "catalog.json"
out.parent.mkdir(parents=True, exist_ok=True)
json.dump({"count": len(cat), "base_url": url, "challenges": cat},
          open(out, "w"), ensure_ascii=False, indent=1)
print(f"\npulled {len(cat)} challenges -> {out}")
bycat = {}
for c in cat:
    bycat.setdefault(c["category"], []).append(c)
for k in sorted(bycat):
    print(f"\n[{k}]")
    for c in bycat[k]:
        print(f"  {c['name']:40} pts={c['points']:<4} files={len(c['files'])} {c['endpoint']}")
src.close()
print("\nfiles downloaded under farm/data/ctf_bench/files/")
