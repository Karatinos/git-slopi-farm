"""Automated reconnaissance of attachments (ACI booster, blueprint §2.3/§4.2).

Runs cheap read-only analysis over the real attachments INSIDE the sandbox and
hands the agent a compact digest before it reasons: file type, size, Shannon
entropy, embedded-file signatures (stego/appended data), image EXIF incl. GPS
(PIL), OCR text (tesseract), PDF first-page text (pypdf), and a flag/secret grep
over strings. Python-first so it does not depend on exiftool/zbarimg/binwalk,
which are frequently absent — it uses only python3 + PIL/pypdf (optional) and
the always-present file/strings/tesseract.
"""
from __future__ import annotations

from ..sandbox.base import Sandbox

_RECON_PY = r'''
import os, sys, re, math, subprocess
from collections import Counter

MAXF = 40
def sh(*a, t=30):
    try:
        return subprocess.run(a, capture_output=True, text=True, timeout=t).stdout
    except Exception:
        return ""

def entropy(b):
    if not b:
        return 0.0
    c = Counter(b); n = len(b)
    return round(-sum((v/n)*math.log2(v/n) for v in c.values()), 2)

SIGS = {b"\x89PNG": "PNG", b"PK\x03\x04": "ZIP", b"\xff\xd8\xff": "JPEG",
        b"%PDF": "PDF", b"Rar!": "RAR", b"7z\xbc\xaf": "7Z", b"\x1f\x8b": "GZIP",
        b"BZh": "BZIP2", b"ID3": "MP3", b"OggS": "OGG", b"fLaC": "FLAC"}

def carve(b):
    hits = []
    for sig, name in SIGS.items():
        i = b.find(sig, 1)                      # skip offset 0 (own header)
        if i != -1:
            hits.append("%s@%d" % (name, i))
    return hits

files = []
for dp, dn, fn in os.walk("."):
    for f in fn:
        if f in ("_snippet.py", "_inspect_image.py", "_recon.py", "TASK.md"):
            continue
        files.append(os.path.join(dp, f))
files = sorted(files)[:MAXF]

for p in files:
    print("=== %s ===" % p)
    ft = sh("file", "-b", p).strip()
    print(" type:", ft[:120])
    try:
        data = open(p, "rb").read()
    except Exception:
        data = b""
    print(" size:", len(data), "entropy:", entropy(data[:200000]))
    cv = carve(data[:2000000])
    if cv:
        print(" embedded:", ", ".join(cv[:6]))
    low = p.lower()
    if low.endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp", ".tif", ".tiff")):
        try:
            from PIL import Image, ExifTags
            im = Image.open(p)
            print(" image:", im.size, im.mode)
            ex = getattr(im, "_getexif", lambda: None)()
            if ex:
                named = {ExifTags.TAGS.get(k, k): v for k, v in ex.items()}
                for key in ("GPSInfo", "DateTimeOriginal", "Make", "Model",
                            "Software", "ImageDescription", "UserComment", "Artist"):
                    if key in named:
                        print("  exif %s: %r" % (key, str(named[key])[:160]))
        except Exception:
            print("  (PIL unavailable or not an image)")
        ocr = " ".join(sh("tesseract", p, "stdout", "-l", "rus+eng", t=60).split())[:500]
        if ocr.strip():
            print("  ocr:", ocr)
    if low.endswith(".pdf"):
        try:
            from pypdf import PdfReader
            r = PdfReader(p)
            txt = (r.pages[0].extract_text() or "") if r.pages else ""
            print("  pdf pages:", len(r.pages), "text:", " ".join(txt.split())[:400])
        except Exception:
            pass
    st = sh("strings", "-n", "4", p)
    fl = sorted(set(re.findall(r"[A-Za-z0-9_]{2,16}\{[^}\n]{1,120}\}", st)))[:3]
    if fl:
        print("  FLAG?:", fl)
    hot = [l for l in st.splitlines()
           if re.search(r"(?i)secret|password|passwd|http|api[_-]?key|BEGIN |ssh-", l)][:4]
    for h in hot:
        print("  str:", h[:120])
'''


def signal_level(digest: str) -> str:
    """Classify exploitable signal -> 'high' | 'low' for the adaptive scheduler."""
    if not digest:
        return "low"
    d = digest.lower()
    if "flag?:" in d or "qr" in d or "exif gps" in d or " embedded:" in d:
        return "high"
    lines = [ln for ln in digest.splitlines()
             if ln.strip().startswith(("ocr:", "exif", "str:", "text:"))]
    if sum(len(ln) for ln in lines) >= 60:
        return "high"
    return "low"


def run_recon(sandbox: Sandbox, max_chars: int = 5000) -> str:
    try:
        sandbox.write_file("_recon.py", _RECON_PY)
        res = sandbox.run("python3 _recon.py", timeout=120)
    except Exception as e:  # noqa: BLE001
        return f"(recon failed: {e})"
    out = (res.stdout or "").strip()
    if not out:
        return "(recon produced no readable content — files may be opaque)"
    return out[:max_chars] + ("\n...(recon truncated)" if len(out) > max_chars else "")
