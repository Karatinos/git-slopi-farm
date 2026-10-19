"""Automated reconnaissance of attachments (ACI booster, blueprint §2.3/§4.2).

Python-first digest produced INSIDE the sandbox before the agent reasons:
type, size, Shannon entropy, embedded-file signatures, image EXIF/OCR, PDF text,
PCAP stream reassembly (stdlib — TCP/UDP payloads + flag grep), ELF symbols of
interest, and a flag/secret grep. No dependency on exiftool/binwalk/zbarimg/
tshark/scapy; uses python3 + PIL/pypdf (optional) + always-present file/strings/
objdump/tesseract.
"""
from __future__ import annotations

from ..sandbox.base import Sandbox

_RECON_PY = r'''
import os, sys, re, math, socket, struct, subprocess
from collections import Counter, OrderedDict

MAXF = 40
def sh(*a, t=30):
    try: return subprocess.run(a, capture_output=True, text=True, timeout=t).stdout
    except Exception: return ""
def entropy(b):
    if not b: return 0.0
    c=Counter(b); n=len(b)
    return round(-sum((v/n)*math.log2(v/n) for v in c.values()),2)
SIGS={b"\x89PNG":"PNG",b"PK\x03\x04":"ZIP",b"\xff\xd8\xff":"JPEG",b"%PDF":"PDF",
      b"Rar!":"RAR",b"7z\xbc\xaf":"7Z",b"\x1f\x8b":"GZIP",b"BZh":"BZIP2",
      b"ID3":"MP3",b"OggS":"OGG",b"fLaC":"FLAC",b"\x7fELF":"ELF"}
def carve(b):
    out=[]
    for sig,name in SIGS.items():
        i=b.find(sig,1)
        if i!=-1: out.append("%s@%d"%(name,i))
    return out
def printable(b):
    return "".join(chr(x) if 32<=x<127 or x in (9,10,13) else "." for x in b)

def pcap_summary(path, cap=1800):
    """Reassemble TCP/UDP flows from a classic pcap (stdlib). Returns a compact
    per-flow payload digest + any flag-shaped strings. pcapng -> hint to scapy."""
    try:
        data=open(path,"rb").read()
    except Exception as e:
        return "  pcap: read error %r"%e
    if data[:4]==b"\x0a\x0d\x0d\x0a":
        return "  pcap: pcapng format — use scapy/pyshark (rdpcap) in run_python"
    if len(data)<24: return "  pcap: too small"
    magic=data[:4]
    if magic in (b"\xd4\xc3\xb2\xa1", b"\x4d\x3c\xb2\xa1"): endian="<"
    elif magic in (b"\xa1\xb2\xc3\xd4", b"\xa1\xb2\x3c\x4d"): endian=">"
    else: return "  pcap: unknown magic %s"%magic.hex()
    linktype=struct.unpack(endian+"I", data[20:24])[0]
    off=24; flows=OrderedDict(); npkt=0
    while off+16<=len(data):
        _,_,incl,_=struct.unpack(endian+"IIII", data[off:off+16]); off+=16
        pkt=data[off:off+incl]; off+=incl; npkt+=1
        if npkt>20000: break
        p=pkt
        if linktype==1:                       # Ethernet
            if len(p)<14: continue
            eth=struct.unpack(">H",p[12:14])[0]
            if eth==0x8100 and len(p)>=18: eth=struct.unpack(">H",p[16:18])[0]; p=p[4:]
            if eth!=0x0800: continue
            p=p[14:]
        elif linktype==101: pass               # raw IP
        else: continue
        if len(p)<20: continue
        ihl=(p[0]&0x0f)*4; proto=p[9]
        src=".".join(map(str,p[12:16])); dst=".".join(map(str,p[16:20]))
        q=p[ihl:]
        if proto==6 and len(q)>=20:            # TCP
            sp,dp=struct.unpack(">HH",q[0:4]); doff=(q[12]>>4)*4; payload=q[doff:]
            key=(src,sp,dst,dp)
        elif proto==17 and len(q)>=8:          # UDP
            sp,dp=struct.unpack(">HH",q[0:4]); payload=q[8:]; key=(src,sp,dst,dp)
        else: continue
        if payload: flows.setdefault(key,bytearray()).extend(payload)
    lines=["  pcap: %d packets, %d flows"%(npkt,len(flows))]
    allflags=set()
    for (src,sp,dst,dp),buf in list(flows.items())[:12]:
        txt=printable(bytes(buf))
        allflags|=set(re.findall(r"[A-Za-z0-9_]{2,16}\{[^}\n]{1,80}\}", txt))
        snippet=re.sub(r"\.{4,}"," ",txt).strip()[:200]
        lines.append("   %s:%d->%s:%d (%dB) %s"%(src,sp,dst,dp,len(buf),snippet))
    if allflags: lines.append("  pcap FLAG?: %s"%sorted(allflags)[:3])
    return "\n".join(lines)[:cap]

files=[]
for dp,dn,fn in os.walk("."):
    for f in fn:
        if f in ("_snippet.py","_inspect_image.py","_recon.py","TASK.md"): continue
        files.append(os.path.join(dp,f))
files=sorted(files)[:MAXF]

for p in files:
    print("=== %s ==="%p)
    ft=sh("file","-b",p).strip(); print(" type:",ft[:120])
    try: data=open(p,"rb").read()
    except Exception: data=b""
    print(" size:",len(data),"entropy:",entropy(data[:200000]))
    cv=carve(data[:2000000])
    if cv: print(" embedded:",", ".join(cv[:6]))
    low=p.lower()
    if low.endswith((".pcap",".pcapng",".cap")):
        print(pcap_summary(p))
    if "ELF" in ft:
        syms=sh("objdump","-t",p,t=25)
        want=[l for l in syms.splitlines()
              if re.search(r"\b(main|check|flag|verify|secret|decode|decrypt|key|auth|valid|compare|pass)\w*\b",l,re.I)]
        names=[l.split()[-1] for l in want if l.split()][:18]
        if names: print("  elf symbols:",", ".join(dict.fromkeys(names)))
        secs=sh("objdump","-h",p,t=20)
        uncommon=[l.split()[1] for l in secs.splitlines() if re.match(r"\s+\d+\s+\.\w",l) and l.split()[1] not in (".text",".data",".bss",".rodata",".comment")][:12]
        if uncommon: print("  elf sections:",", ".join(uncommon))
    if low.endswith((".png",".jpg",".jpeg",".bmp",".gif",".webp",".tif",".tiff")):
        try:
            from PIL import Image, ExifTags
            im=Image.open(p); print(" image:",im.size,im.mode)
            ex=getattr(im,"_getexif",lambda:None)()
            if ex:
                named={ExifTags.TAGS.get(k,k):v for k,v in ex.items()}
                for key in ("GPSInfo","DateTimeOriginal","Make","Model","Software","ImageDescription","UserComment","Artist"):
                    if key in named: print("  exif %s: %r"%(key,str(named[key])[:160]))
        except Exception: print("  (PIL unavailable)")
        ocr=" ".join(sh("tesseract",p,"stdout","-l","rus+eng",t=60).split())[:500]
        if ocr.strip(): print("  ocr:",ocr)
    if low.endswith(".pdf"):
        try:
            from pypdf import PdfReader
            r=PdfReader(p); txt=(r.pages[0].extract_text() or "") if r.pages else ""
            print("  pdf pages:",len(r.pages),"text:"," ".join(txt.split())[:400])
        except Exception: pass
    st=sh("strings","-n","4",p)
    fl=sorted(set(re.findall(r"[A-Za-z0-9_]{2,16}\{[^}\n]{1,120}\}",st)))[:3]
    if fl: print("  FLAG?:",fl)
    hot=[l for l in st.splitlines() if re.search(r"(?i)secret|password|passwd|api[_-]?key|BEGIN |ssh-|http://|https://",l)][:4]
    for h in hot: print("  str:",h[:120])
'''


def signal_level(digest: str) -> str:
    if not digest:
        return "low"
    d = digest.lower()
    if "flag?:" in d or " qr" in d or "exif gps" in d or " embedded:" in d or "pcap flag" in d \
            or "elf symbols" in d or "->" in d:
        return "high"
    lines = [ln for ln in digest.splitlines()
             if ln.strip().startswith(("ocr:", "exif", "str:", "text:", "pcap:"))]
    if sum(len(ln) for ln in lines) >= 60:
        return "high"
    return "low"


def run_recon(sandbox: Sandbox, max_chars: int = 6000) -> str:
    try:
        sandbox.write_file("_recon.py", _RECON_PY)
        res = sandbox.run("python3 _recon.py", timeout=120)
    except Exception as e:  # noqa: BLE001
        return f"(recon failed: {e})"
    out = (res.stdout or "").strip()
    if not out:
        return "(recon produced no readable content)"
    return out[:max_chars] + ("\n...(recon truncated)" if len(out) > max_chars else "")
