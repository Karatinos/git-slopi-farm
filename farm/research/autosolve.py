#!/usr/bin/env python3
"""Generic, no-LLM auto-solver — a tooling-only baseline brain.

Runs in a task's working directory, tries a battery of standard CTF techniques
over the files, and prints the first `flag{...}` it recovers as `FLAG=<flag>`.
It is deliberately general (no task-specific knowledge), so what it solves is a
fair lower bound: "what the sandbox tooling cracks with zero reasoning". Used
both standalone and as the brain of the ScriptedSolver provider.
"""
import base64, binascii, bz2, io, math, os, re, sys, tarfile, zipfile, gzip, zlib

FLAG = re.compile(r"[A-Za-z0-9_]{2,16}\{[A-Za-z0-9_]{1,80}\}")

def hits(b):
    try:
        t = b.decode("latin-1") if isinstance(b, (bytes, bytearray)) else b
    except Exception:
        return []
    return FLAG.findall(t)

def try_decodes(data, depth=3):
    """Recursively try base64/base32/hex decodes, collecting flags."""
    found = []
    found += hits(data)
    if depth <= 0:
        return found
    s = data.strip() if isinstance(data, bytes) else data.encode()
    cand = []
    for fn in (lambda x: base64.b64decode(x, validate=False),
               lambda x: base64.b32decode(x + b"=" * (-len(x) % 8)),
               lambda x: binascii.unhexlify(re.sub(rb"\s", b"", x)),
               lambda x: base64.a85decode(x, adobe=x.startswith(b"<~")),  # ascii85
               lambda x: base64.b85decode(x),                            # base85
               lambda x: zlib.decompress(x),                             # raw zlib
               lambda x: bz2.decompress(x)):                             # bzip2
        try:
            d = fn(s)
            if d and d != s:
                cand.append(d)
        except Exception:
            pass
    for d in cand:
        found += try_decodes(d, depth - 1)
    return found

def carve_and_extract(data):
    found = []
    # appended / embedded archives
    for sig in (b"PK\x03\x04", b"\x1f\x8b", b"ustar"):
        i = data.find(sig)
        while i != -1:
            blob = data[i - 257:] if sig == b"ustar" else data[i:]
            found += extract_archive(blob)
            i = data.find(sig, i + 1)
            if len(found) > 50:
                break
    return found

def extract_archive(blob):
    found = []
    try:
        z = zipfile.ZipFile(io.BytesIO(blob))
        for name in z.namelist():
            d = z.read(name)
            found += hits(d) + carve_and_extract(d) + nested(d)
    except Exception:
        pass
    try:
        g = gzip.decompress(blob)
        found += hits(g) + nested(g)
    except Exception:
        pass
    try:
        t = tarfile.open(fileobj=io.BytesIO(blob))
        for m in t.getmembers():
            f = t.extractfile(m)
            if f:
                d = f.read(); found += hits(d) + nested(d)
    except Exception:
        pass
    return found

def nested(d):
    """One level of nested-archive handling for extracted members."""
    out = []
    try:
        out += extract_archive(d)
    except Exception:
        pass
    return out

def morse(data):
    try:
        s = data.decode("latin-1")
    except Exception:
        return []
    if s.count(".") + s.count("-") < 4:
        return []
    M = {v: k for k, v in {**{c: m for c, m in zip("abcdefghijklmnopqrstuvwxyz",
        ".- -... -.-. -.. . ..-. --. .... .. .--- -.- .-.. -- -. --- .--. --.- .-. ... - ..- ...- .-- -..- -.-- --..".split())},
        **{d_: m for d_, m in zip("0123456789",
        "----- .---- ..--- ...-- ....- ..... -.... --... ---.. ----.".split())},
        "_": "..--.-", "{": "-.--.", "}": "-.--.-"}.items()}
    dec = "".join(M.get(tok, "") for tok in s.strip().split(" / "))
    return hits(dec)

def lsb(path):
    try:
        from PIL import Image
        im = Image.open(path).convert("RGB")
        px = list(im.getdata())
    except Exception:
        return []
    out = []
    for chan in (0, 1, 2):
        bits = "".join(str(px[i][chan] & 1) for i in range(len(px)))
        bs = bytearray()
        for j in range(0, len(bits) - 7, 8):
            byte = int(bits[j:j+8], 2)
            if byte == 0:
                break
            bs.append(byte)
        out += hits(bytes(bs))
    return out

def rsa_fermat(text):
    kv = {}
    for k in ("n", "e", "c"):
        m = re.search(rf"\b{k}\s*=\s*(\d+)", text)
        if m:
            kv[k] = int(m.group(1))
    if len(kv) != 3:
        return []
    n, e, c = kv["n"], kv["e"], kv["c"]
    a = math.isqrt(n)
    if a * a < n:
        a += 1
    for _ in range(1 << 20):
        b2 = a * a - n; b = math.isqrt(b2)
        if b * b == b2:
            p, q = a - b, a + b
            try:
                d = pow(e, -1, (p - 1) * (q - 1)); m = pow(c, d, n)
                return hits(m.to_bytes((m.bit_length() + 7) // 8, "big"))
            except Exception:
                return []
        a += 1
    return []

def xor_crib(data, crib=b"flag{"):
    best = None
    for L in range(1, 17):
        for off in range(len(data) - len(crib) + 1):
            kb = {(off + i) % L: data[off + i] ^ crib[i] for i in range(len(crib))}
            if len(kb) != min(L, len(crib)):
                continue
            key = bytes(kb.get(j, 0) for j in range(L))
            pt = bytes(data[i] ^ key[i % L] for i in range(len(data)))
            pr = sum(32 <= x < 127 or x in (9, 10, 13) for x in pt) / max(1, len(pt))
            if pr < 0.999:
                continue
            m = FLAG.search(pt.decode("latin-1"))
            if m and (best is None or pr > best[0]):
                best = (pr, m.group(0))
    return [best[1]] if best else []

def pysource(text):
    # invert an xor-against-constants password check: ENC=[...], KEY=0xNN
    enc = re.search(r"ENC\s*=\s*(\[[^\]]+\])", text)
    key = re.search(r"KEY\s*=\s*(0x[0-9a-fA-F]+|\d+)", text)
    if enc and key:
        try:
            import ast
            vals = ast.literal_eval(enc.group(1)); k = int(key.group(1), 0)
            return hits("".join(chr(v ^ k) for v in vals))
        except Exception:
            pass
    return []

def rot_brute(data):
    """Try all 25 Caesar shifts over printable text (covers ROT13/ROT-N flags).
    Only letters rotate, so `synt{...}` -> `flag{...}`; `{`/digits are untouched."""
    if not data or len(data) > 8192:
        return []
    try:
        t = data.decode("latin-1")
    except Exception:
        return []
    if not t or sum(1 for c in t if 32 <= ord(c) < 127 or c in "\t\n\r") / len(t) < 0.9:
        return []
    if not re.search(r"[A-Za-z]", t):
        return []
    found = []
    for s in range(1, 26):
        def shift(c, s=s):
            if "a" <= c <= "z":
                return chr((ord(c) - 97 + s) % 26 + 97)
            if "A" <= c <= "Z":
                return chr((ord(c) - 65 + s) % 26 + 65)
            return c
        found += hits("".join(shift(c) for c in t))
    return found


def xor_single(data):
    """Single-byte XOR brute over a SMALL blob; keep only near-fully-printable
    decodings (guards against the flag regex matching XOR noise)."""
    if not data or len(data) > 4096:
        return []
    found = []
    for k in range(1, 256):
        dec = bytes(b ^ k for b in data)
        if sum(32 <= x < 127 or x in (9, 10, 13) for x in dec) / len(dec) < 0.9:
            continue
        found += hits(dec)
    return found


def png_text(path):
    """Read a PNG's tEXt/iTXt/zTXt metadata chunks (a classic hiding spot)."""
    try:
        data = open(path, "rb").read()
    except Exception:
        return []
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        return []
    found, i = [], 8
    while i + 12 <= len(data):
        ln = int.from_bytes(data[i:i + 4], "big")
        typ = data[i + 4:i + 8]
        chunk = data[i + 8:i + 8 + ln]
        if typ in (b"tEXt", b"iTXt"):
            found += hits(chunk)
        elif typ == b"zTXt":
            nul = chunk.find(b"\0")
            if nul != -1:
                try:
                    found += hits(zlib.decompress(chunk[nul + 2:]))
                except Exception:
                    pass
        if typ == b"IEND":
            break
        i += 12 + ln
    return found


def solve_dir(root="."):
    found = []
    for dp, _, fn in os.walk(root):
        for f in fn:
            if f in ("description.txt", "_autosolve.py", "_snippet.py"):
                continue
            p = os.path.join(dp, f)
            try:
                data = open(p, "rb").read()
            except Exception:
                continue
            found += hits(data)
            found += try_decodes(data)
            found += carve_and_extract(data)
            found += morse(data)
            found += rsa_fermat(data.decode("latin-1", "ignore"))
            found += rot_brute(data)
            found += xor_single(data)
            if f.lower().endswith((".png", ".bmp", ".gif")):
                found += lsb(p)
            if f.lower().endswith(".png"):
                found += png_text(p)
            if f.lower().endswith(".bin"):
                found += xor_crib(data)
            if f.lower().endswith(".py"):
                found += pysource(data.decode("latin-1", "ignore"))
    # dedupe, prefer a flag{...}
    uniq = list(dict.fromkeys(found))
    uniq.sort(key=lambda x: (not x.lower().startswith("flag{"), len(x)))
    return uniq


def solve_endpoint(ep):
    """Probe a live service (http(s) or host:port) for a flag."""
    import socket, re as _re, urllib.request
    found = []
    ep = (ep or "").strip()
    murl = _re.search(r"https?://[^\s]+", ep)
    if murl or "://" in ep:
        base = (murl.group(0) if murl else ep).rstrip("/")
        for path in ("", "/", "/flag", "/flag.txt", "/robots.txt", "/index.html",
                     "/.env", "/admin", "/secret", "/api/flag", "/static/flag.txt"):
            try:
                req = urllib.request.Request(base + path, headers={"User-Agent": "curl/8"})
                data = urllib.request.urlopen(req, timeout=6).read()
                found += hits(data)
            except Exception:
                pass
        return found
    mhp = _re.search(r"(\d{1,3}(?:\.\d{1,3}){3}|[\w.-]+)[:\s]+(\d{2,5})", ep)
    if mhp:
        host, port = mhp.group(1), int(mhp.group(2))
        try:
            s = socket.create_connection((host, port), timeout=6); s.settimeout(4)
            buf = b""
            for probe in (b"", b"\n", b"help\n", b"1\n"):
                try:
                    if probe:
                        s.sendall(probe)
                    buf += s.recv(8192)
                except Exception:
                    break
            s.close(); found += hits(buf)
        except Exception:
            pass
    return found

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    res = solve_dir(root)
    ep = os.environ.get("SLOPI_ENDPOINT", "")
    if not res and ep:
        res = solve_endpoint(ep)
    if res:
        print("FLAG=" + res[0])
    else:
        print("NO_FLAG_FOUND")
