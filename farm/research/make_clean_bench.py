#!/usr/bin/env python3
"""Generate a CLEAN, self-contained, offline CTF benchmark for fair prototype
comparison — deterministic tasks with known flags and a reference solver each.

Why: the shipped `tasks/` folder is a writeup archive (contaminated / missing
original artifacts), so it cannot fairly measure solving. This set is generated
from scratch: each task has ONLY a problem statement + a genuine artifact, the
flag is never present in plaintext, and a reference solver proves solvability.

    python3 research/make_clean_bench.py --out research/clean_bench \
        --answer-key data/answer_key_clean.json [--selftest]

Layout: <out>/<category>/<name>/{description.txt, <artifact...>}
Flags:  flag{...}; written to the answer-key (quarantined, harness-only).
"""
from __future__ import annotations
import argparse, base64, io, json, os, struct, tarfile, zipfile, zlib, binascii
from pathlib import Path

FLAGS = {
    "crypto/base_chain":   "flag{l4y3rs_0f_3nc0d1ng_p33l3d}",
    "crypto/xor_crib":     "flag{kn0wn_pl41nt3xt_br34ks_x0r}",
    "crypto/rsa_toy":      "flag{sm4ll_m0dulus_f4ct0rs_f4st}",
    "misc/matryoshka":     "flag{d0wn_thr0ugh_3v3ry_l4y3r}",
    "misc/morse_wav":      "flag{d0ts_4nd_d4sh3s_sp34k}",
    "forensic/png_append": "flag{d4t4_h1des_p4st_1end}",
    "forensic/lsb_stego":  "flag{l34st_s1gn1f1c4nt_truth}",
    "reverse/pycheck":     "flag{1nv3rt_th3_ch3ck_l0g1c}",
}

def _w(d: Path, name: str, data):
    d.mkdir(parents=True, exist_ok=True)
    p = d / name
    p.write_bytes(data if isinstance(data, bytes) else data.encode())

def _desc(d: Path, text: str):
    _w(d, "description.txt", text.strip() + "\n")

# ---------- generators (return nothing; write artifacts) ------------------- #
def gen_base_chain(d):
    f = FLAGS["crypto/base_chain"].encode()
    enc = base64.b64encode(binascii.hexlify(f))            # b64(hex(flag))
    _desc(d, "A short message was encoded, then encoded again. Recover the flag.")
    _w(d, "message.txt", enc)

def gen_xor_crib(d):
    key = b"R4dio"
    pt = ("The quick brown fox. " + FLAGS["crypto/xor_crib"] + " end.").encode()
    ct = bytes(b ^ key[i % len(key)] for i, b in enumerate(pt))
    _desc(d, "A short ASCII key XORs the plaintext (repeating). The flag format is flag{...}.")
    _w(d, "cipher.bin", ct)

def gen_rsa_toy(d):
    from sympy import nextprime
    p = nextprime(2**256 + 0x1234567)
    q = nextprime(p + 2)                                   # CLOSE primes -> Fermat
    n = p * q; e = 65537
    dkey = pow(e, -1, (p - 1) * (q - 1))
    m = int.from_bytes(FLAGS["crypto/rsa_toy"].encode(), "big")
    assert m < n
    c = pow(m, e, n)
    _desc(d, "Toy RSA with two CLOSE primes. params.txt has n, e, c (c = m^e mod n). "
             "Factor n (Fermat works) and recover m -> flag.")
    _w(d, "params.txt", f"n = {n}\ne = {e}\nc = {c}\n")
    assert pow(c, dkey, n) == m

def gen_matryoshka(d):
    flag = FLAGS["misc/matryoshka"].encode()
    # innermost: flag.txt -> tar.gz -> zip
    tgz = io.BytesIO()
    with tarfile.open(fileobj=tgz, mode="w:gz") as t:
        ti = tarfile.TarInfo("flag.txt"); data = flag
        ti.size = len(data); t.addfile(ti, io.BytesIO(data))
    zb = io.BytesIO()
    with zipfile.ZipFile(zb, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("inner.tar.gz", tgz.getvalue())
    _desc(d, "Keep unpacking until you reach the flag.")
    _w(d, "outer.zip", zb.getvalue())

def gen_morse_wav(d):
    # encode flag body as morse into a text 'signal' file (no audio dep): dots/dashes
    MORSE = {**{c: m for c, m in zip("abcdefghijklmnopqrstuvwxyz",
        ".- -... -.-. -.. . ..-. --. .... .. .--- -.- .-.. -- -. --- .--. --.- .-. ... - ..- ...- .-- -..- -.-- --..".split())},
        **{d_: m for d_, m in zip("0123456789",
        "----- .---- ..--- ...-- ....- ..... -.... --... ---.. ----.".split())},
        "_": "..--.-", "{": "-.--.", "}": "-.--.-"}
    body = FLAGS["misc/morse_wav"]
    code = " / ".join(MORSE.get(ch, "?") for ch in body)
    _desc(d, "A captured signal, transcribed as Morse (letters sep by space, '/' between words). Decode to the flag text (expected format flag{...}).")
    _w(d, "signal.txt", code)

def _png(width, height, rgb_rows):
    def chunk(typ, data):
        c = typ + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", binascii.crc32(c) & 0xffffffff)
    raw = b"".join(b"\x00" + bytes(v for px in row for v in px) for row in rgb_rows)
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b"")

def gen_png_append(d):
    rows = [[((x*7) % 256, (y*5) % 256, (x+y) % 256) for x in range(32)] for y in range(32)]
    png = _png(32, 32, rows)
    zb = io.BytesIO()
    with zipfile.ZipFile(zb, "w") as z:
        z.writestr("flag.txt", FLAGS["forensic/png_append"])
    _desc(d, "The picture carries more than pixels. Something is appended after IEND.")
    _w(d, "capture.png", png + zb.getvalue())

def gen_lsb_stego(d):
    flag = FLAGS["forensic/lsb_stego"].encode() + b"\x00"
    bits = "".join(f"{b:08b}" for b in flag)
    W = H = 40
    npx = W * H
    assert len(bits) <= npx
    rows = []
    i = 0
    for y in range(H):
        row = []
        for x in range(W):
            base = (x * 3 + y * 2) % 254 + 1               # avoid 0/255 edges
            bit = int(bits[i]) if i < len(bits) else 0
            r = (base & ~1) | bit
            row.append((r, (x*2) % 256, (y*3) % 256)); i += 1
        rows.append(row)
    _desc(d, "The red channel's least significant bits hold a message (NUL-terminated). Recover the flag.")
    _w(d, "stego.png", _png(W, H, rows))

def gen_pycheck(d):
    flag = FLAGS["reverse/pycheck"]
    consts = [ord(c) ^ 0x5A for c in flag]
    src = (
        "import sys\n"
        f"ENC = {consts}\n"
        "KEY = 0x5A\n"
        "s = sys.argv[1] if len(sys.argv) > 1 else input('pass: ')\n"
        "if len(s) == len(ENC) and all((ord(c) ^ KEY) == e for c, e in zip(s, ENC)):\n"
        "    print('ACCESS GRANTED:', s)\n"
        "else:\n"
        "    print('DENIED')\n"
    )
    _desc(d, "check.py accepts exactly one password and prints it on success. Recover the accepted string (it is the flag).")
    _w(d, "check.py", src)

GEN = {
    "crypto/base_chain": gen_base_chain, "crypto/xor_crib": gen_xor_crib,
    "crypto/rsa_toy": gen_rsa_toy, "misc/matryoshka": gen_matryoshka,
    "misc/morse_wav": gen_morse_wav, "forensic/png_append": gen_png_append,
    "forensic/lsb_stego": gen_lsb_stego, "reverse/pycheck": gen_pycheck,
}

# ---------- reference solvers (prove solvability; not shown to agents) ------ #
def solve_base_chain(d):
    enc = (d / "message.txt").read_bytes()
    return binascii.unhexlify(base64.b64decode(enc)).decode()
def solve_xor_crib(d):
    import re
    ct = (d / "cipher.bin").read_bytes()
    crib = b"flag{"
    FLAG = re.compile(rb"flag\{[A-Za-z0-9_]{1,80}\}")   # real flags: no symbols
    best = None
    for L in range(1, 17):
        for off in range(len(ct) - len(crib) + 1):
            kb = {(off + i) % L: ct[off + i] ^ crib[i] for i in range(len(crib))}
            if len(kb) != min(L, len(crib)):
                continue
            key = bytes(kb.get(j, 0) for j in range(L))
            pt = bytes(ct[i] ^ key[i % L] for i in range(len(ct)))
            printable = sum(32 <= x < 127 or x in (9, 10, 13) for x in pt) / len(pt)
            if printable < 0.999:
                continue
            m = FLAG.search(pt)
            if m and (best is None or printable > best[0]):
                best = (printable, m.group(0).decode())
    if best:
        return best[1]
    raise RuntimeError("xor solve failed")

def solve_rsa_toy(d):
    import math
    kv = dict(l.split(" = ") for l in (d / "params.txt").read_text().strip().splitlines())
    n, e, c = int(kv["n"]), int(kv["e"]), int(kv["c"])
    a = math.isqrt(n)
    if a * a < n:
        a += 1
    while True:                                            # Fermat factorization
        b2 = a * a - n; b = math.isqrt(b2)
        if b * b == b2:
            break
        a += 1
    p, q = a - b, a + b
    dkey = pow(e, -1, (p - 1) * (q - 1))
    m = pow(c, dkey, n)
    return m.to_bytes((m.bit_length() + 7) // 8, "big").decode()
def solve_matryoshka(d):
    zb = zipfile.ZipFile(d / "outer.zip")
    tgz = zb.read("inner.tar.gz")
    with tarfile.open(fileobj=io.BytesIO(tgz)) as t:
        return t.extractfile("flag.txt").read().decode()
def solve_morse_wav(d):
    INV = None
    MORSE = {**{c: m for c, m in zip("abcdefghijklmnopqrstuvwxyz",
        ".- -... -.-. -.. . ..-. --. .... .. .--- -.- .-.. -- -. --- .--. --.- .-. ... - ..- ...- .-- -..- -.-- --..".split())},
        **{d_: m for d_, m in zip("0123456789",
        "----- .---- ..--- ...-- ....- ..... -.... --... ---.. ----.".split())},
        "_": "..--.-", "{": "-.--.", "}": "-.--.-"}
    inv = {v: k for k, v in MORSE.items()}
    code = (d / "signal.txt").read_text().strip()
    return "".join(inv.get(tok, "?") for tok in code.split(" / "))
def solve_png_append(d):
    data = (d / "capture.png").read_bytes()
    i = data.find(b"PK\x03\x04")
    return zipfile.ZipFile(io.BytesIO(data[i:])).read("flag.txt").decode()
def solve_lsb_stego(d):
    from PIL import Image
    im = Image.open(d / "stego.png").convert("RGB")
    px = list(im.getdata())
    bits = "".join(str(px[i][0] & 1) for i in range(len(px)))
    out = bytearray()
    for j in range(0, len(bits) - 7, 8):
        byte = int(bits[j:j+8], 2)
        if byte == 0:
            break
        out.append(byte)
    return out.decode("latin-1")
def solve_pycheck(d):
    src = (d / "check.py").read_text()
    import ast
    enc = None
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "ENC":
            enc = ast.literal_eval(node.value)
    return "".join(chr(e ^ 0x5A) for e in enc)

SOLVE = {
    "crypto/base_chain": solve_base_chain, "crypto/xor_crib": solve_xor_crib,
    "crypto/rsa_toy": solve_rsa_toy, "misc/matryoshka": solve_matryoshka,
    "misc/morse_wav": solve_morse_wav, "forensic/png_append": solve_png_append,
    "forensic/lsb_stego": solve_lsb_stego, "reverse/pycheck": solve_pycheck,
}

def build(out: Path):
    for tid, fn in GEN.items():
        fn(out / tid)
    return {tid: FLAGS[tid] for tid in GEN}

def selftest(out: Path):
    ok = True
    for tid in GEN:
        try:
            got = SOLVE[tid](out / tid)
            exp = FLAGS[tid]
            status = "PASS" if got == exp else f"FAIL got={got!r}"
            if got != exp:
                ok = False
        except Exception as e:
            status = f"ERROR {e!r}"; ok = False
        print(f"  {tid:24} {status}")
    return ok

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="research/clean_bench")
    ap.add_argument("--answer-key", default="data/answer_key_clean.json")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    flags = build(out)
    doc = {"_comment": "Gold for the CLEAN synthetic benchmark. Harness-only; never staged.",
           "flags": flags}
    Path(a.answer_key).parent.mkdir(parents=True, exist_ok=True)
    Path(a.answer_key).write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"generated {len(flags)} clean tasks -> {out}")
    print(f"answer-key -> {a.answer_key}")
    if a.selftest:
        print("selftest (reference solvers reproduce gold):")
        ok = selftest(out)
        print("ALL PASS" if ok else "SELFTEST FAILURES")
        raise SystemExit(0 if ok else 1)

if __name__ == "__main__":
    main()
