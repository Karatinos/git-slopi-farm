"""
Автоматическая АТАКА (на ХОСТЕ) на подписывающий оракул ГОСТ Р 34.10-2012.
САМОДОСТАТОЧНЫЙ скрипт: ничего не импортирует из проекта — вся атака здесь.

Полная end-to-end атака на детерминированную симуляцию утечки bit-length nonce:
  1) подключается к оракулу по TCP (как nc), МНОГОПОТОЧНО шлёт SIGN;
  2) из двух меток времени САМА мерит задержку, сама калибрует квант и
     оценивает t = bit_length(нонса), а из него lz = w - t (ведущие нули);
  3) берёт подписи с lz >= L как HNP-образцы, СОХРАНЯЯ фактический lz каждой;
  4) решёткой (CVP: LLL/BKZ + Babai) восстанавливает ключ d;
  5) проверяет ТОЛЬКО по открытому ключу: d*G == Y.

Оптимизации:
  * B — переменная граница: каждая подпись входит в решётку со СВОИМ lz
        (не усечённым до L); в подвыборку берутся лучшие (с бОльшим lz).
  * C — быстрое умножение точки в координатах Якоби (проверка d*G==Y).
  * F — конвейер: решётка стартует, как только накопилось достаточно подписей,
        а сбор продолжается в фоне (фазы не ждут друг друга).
  Плюс кэш пула на диск и ограничение числа процессов решётки (против свопа).

Запуск:  python3 attack_client.py [L] [bkz]
Env:     ORACLE_HOST (127.0.0.1)  ORACLE_PORT (31337)
         HARVEST_THREADS (=CPU)   LATTICE_WORKERS (=min(CPU,4))
"""

import json
import os
import random
import re
import socket
import statistics
import sys
import threading
import time
from concurrent.futures import (ProcessPoolExecutor, ThreadPoolExecutor,
                                as_completed)
from fractions import Fraction

try:
    from fpylll import (IntegerMatrix, LLL as _FP_LLL, BKZ as _FP_BKZ,
                        CVP as _FP_CVP, FPLLL as _FPLLL)
    _HAVE_FPYLLL = True
except Exception:
    _HAVE_FPYLLL = False

BKZ_BLOCK = 0

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

_HERE = os.path.dirname(os.path.abspath(__file__))
HOST = os.environ.get("ORACLE_HOST", "127.0.0.1")
PORT = int(os.environ.get("ORACLE_PORT", "31337"))
TS_RE = re.compile(r"\[(\d\d):(\d\d):(\d\d)\.(\d+)\]")
_CPU = os.cpu_count() or 4
HARVEST_THREADS = int(os.environ.get("HARVEST_THREADS", str(_CPU)))
LATTICE_WORKERS = int(os.environ.get("LATTICE_WORKERS", str(min(_CPU, 4))))


# ================================================================== #
#  Быстрое умножение точки в координатах Якоби (проверка d*G == Y)     #
# ================================================================== #
def _jac_double(X, Y, Z, a, p):
    if Z == 0 or Y == 0:
        return (1, 1, 0)
    XX = (X * X) % p
    YY = (Y * Y) % p
    YYYY = (YY * YY) % p
    ZZ = (Z * Z) % p
    S = (2 * (((X + YY) ** 2 - XX - YYYY) % p)) % p
    M = (3 * XX + a * ((ZZ * ZZ) % p)) % p
    T = (M * M - 2 * S) % p
    Y3 = (M * ((S - T) % p) - 8 * YYYY) % p
    Z3 = ((Y + Z) ** 2 - YY - ZZ) % p
    return (T, Y3, Z3)


def _jac_add(X1, Y1, Z1, X2, Y2, Z2, a, p):
    if Z1 == 0:
        return (X2, Y2, Z2)
    if Z2 == 0:
        return (X1, Y1, Z1)
    Z1Z1 = (Z1 * Z1) % p
    Z2Z2 = (Z2 * Z2) % p
    U1 = (X1 * Z2Z2) % p
    U2 = (X2 * Z1Z1) % p
    S1 = ((Y1 * Z2) % p) * Z2Z2 % p
    S2 = ((Y2 * Z1) % p) * Z1Z1 % p
    if U1 == U2:
        if S1 != S2:
            return (1, 1, 0)
        return _jac_double(X1, Y1, Z1, a, p)
    H = (U2 - U1) % p
    I = (((2 * H) % p) ** 2) % p
    J = (H * I) % p
    r = (2 * (S2 - S1)) % p
    V = (U1 * I) % p
    X3 = (r * r - J - 2 * V) % p
    Y3 = (r * ((V - X3) % p) - 2 * S1 * J) % p
    Z3 = ((((Z1 + Z2) ** 2 - Z1Z1 - Z2Z2) % p) * H) % p
    return (X3, Y3, Z3)


def fast_multiply(k, P, a, p):
    if P is None or k == 0:
        return None
    RX, RY, RZ = 1, 1, 0
    QX, QY, QZ = P[0] % p, P[1] % p, 1
    while k > 0:
        if k & 1:
            RX, RY, RZ = _jac_add(RX, RY, RZ, QX, QY, QZ, a, p)
        QX, QY, QZ = _jac_double(QX, QY, QZ, a, p)
        k >>= 1
    if RZ == 0:
        return None
    zinv = pow(RZ, p - 2, p)
    zinv2 = (zinv * zinv) % p
    return ((RX * zinv2) % p, ((RY * zinv2) % p) * zinv % p)


# ================================================================== #
#  Решётка: целочисленный LLL (Cohen 2.6.7) + Грам-Шмидт + Бабай      #
# ================================================================== #
def lll_int(basis, delta_num=99, delta_den=100):
    nv = len(basis)
    dim = len(basis[0])
    b = [None] + [list(map(int, row)) for row in basis]
    d = [0] * (nv + 1)
    d[0] = 1
    lam = [[0] * (nv + 1) for _ in range(nv + 1)]

    def dot(u, v):
        return sum(x * y for x, y in zip(u, v))

    def RED(k, l):
        if 2 * abs(lam[k][l]) <= d[l]:
            return
        qq = (2 * lam[k][l] + d[l]) // (2 * d[l])
        b[k] = [b[k][t] - qq * b[l][t] for t in range(dim)]
        lam[k][l] -= qq * d[l]
        for i in range(1, l):
            lam[k][i] -= qq * lam[l][i]

    def SWAP(k, kmax):
        b[k], b[k - 1] = b[k - 1], b[k]
        for j in range(1, k - 1):
            lam[k][j], lam[k - 1][j] = lam[k - 1][j], lam[k][j]
        lm = lam[k][k - 1]
        Bn = (d[k - 2] * d[k] + lm * lm) // d[k - 1]
        for i in range(k + 1, kmax + 1):
            t = lam[i][k]
            lam[i][k] = (d[k] * lam[i][k - 1] - lm * t) // d[k - 1]
            lam[i][k - 1] = (Bn * t + lm * lam[i][k]) // d[k]
        d[k - 1] = Bn

    kmax = 1
    d[1] = dot(b[1], b[1])
    k = 2
    while k <= nv:
        if k > kmax:
            kmax = k
            for j in range(1, k + 1):
                u = dot(b[k], b[j])
                for i in range(1, j):
                    u = (d[i] * u - lam[k][i] * lam[j][i]) // d[i - 1]
                if j < k:
                    lam[k][j] = u
                else:
                    d[k] = u
        while True:
            RED(k, k - 1)
            if delta_den * d[k] * d[k - 2] < \
               delta_num * d[k - 1] * d[k - 1] - delta_den * lam[k][k - 1] ** 2:
                SWAP(k, kmax)
                k = max(2, k - 1)
            else:
                for l in range(k - 2, 0, -1):
                    RED(k, l)
                k += 1
                break
    return [b[i] for i in range(1, nv + 1)]


def _gram_schmidt(basis):
    dim = len(basis[0])
    Bstar, norms = [], []
    for row in basis:
        v = [Fraction(x) for x in row]
        for bs, nrm in zip(Bstar, norms):
            mu = sum(Fraction(row[k]) * bs[k] for k in range(dim)) / nrm
            v = [v[k] - mu * bs[k] for k in range(dim)]
        Bstar.append(v)
        norms.append(sum(x * x for x in v))
    return Bstar, norms


def babai_nearest_plane(basis, target):
    dim = len(target)
    Bstar, norms = _gram_schmidt(basis)
    b = [Fraction(x) for x in target]
    for i in range(len(basis) - 1, -1, -1):
        c = round(sum(b[k] * Bstar[i][k] for k in range(dim)) / norms[i])
        b = [b[k] - c * basis[i][k] for k in range(dim)]
    return [int(target[k] - b[k]) for k in range(dim)]


def _solve_cvp(basis, target):
    if _HAVE_FPYLLL:
        M = IntegerMatrix.from_matrix([list(map(int, row)) for row in basis])
        maxbits = max(abs(x) for row in basis for x in row).bit_length()
        if maxbits > 200:
            _FPLLL.set_precision(maxbits)
            _FP_LLL.reduction(M, method="heuristic", float_type="mpfr")
            if BKZ_BLOCK >= 2:
                _FP_BKZ.reduction(M, _FP_BKZ.Param(
                    block_size=min(len(basis), BKZ_BLOCK), float_type="mpfr"))
        else:
            _FP_LLL.reduction(M)
            if BKZ_BLOCK >= 2:
                _FP_BKZ.reduction(M, _FP_BKZ.Param(
                    block_size=min(len(basis), BKZ_BLOCK)))
        return list(_FP_CVP.closest_vector(M, tuple(int(x) for x in target)))
    return babai_nearest_plane(lll_int(basis), target)


def recover_key(data, q, p, a, G, Y):
    """Одна попытка HNP-решётки с ПЕРЕМЕННОЙ границей: каждая подпись входит со
    своим lz (числом ведущих нулей нонса). Возврат d или None."""
    m = q.bit_length()
    A_l, t_l, w_l = [], [], []
    for s in data:
        lz = s["lz"]
        B = 1 << (m - lz)                      # нонс i лежит в [0, B)
        half = B >> 1
        wsc = max(1, q // B)                   # вес строки ~ 2^lz (балансировка)
        e_inv = pow(s["e"], -1, q)
        A_l.append((-e_inv * s["r"]) % q)
        U = (e_inv * s["s"]) % q
        t_l.append((half - U) % q)
        w_l.append(wsc)

    n = len(data)
    dim = n + 1
    basis = [[w_l[i] * A_l[i] for i in range(n)] + [1]]
    for i in range(n):
        row = [0] * dim
        row[i] = w_l[i] * q
        basis.append(row)
    target = [w_l[i] * t_l[i] for i in range(n)] + [0]

    closest = _solve_cvp(basis, target)
    d_cand = closest[-1] % q
    if fast_multiply(d_cand, G, a, p) == tuple(Y):
        return d_cand
    return None


# ================================================================== #
#  Транспорт: разговор с оракулом по TCP                               #
# ================================================================== #
def _connect():
    s = socket.create_connection((HOST, PORT))
    f = s.makefile("rwb")
    f.readline()                                 # баннер
    return s, f


def _read_block(f):
    lines = []
    for raw in f:
        line = raw.decode("utf-8", "replace").rstrip("\r\n")
        if line.strip() == "END":
            break
        lines.append(line)
    return lines


def get_pubkey(f):
    """Все параметры атаки берём ТОЛЬКО из публичного ответа оракула."""
    f.write(b"PUBKEY\n")
    f.flush()
    d = {}
    for line in _read_block(f):
        if "=" in line:
            k, v = line.split("=", 1)
            d[k.strip()] = v.strip()
    p = int(d["p"], 16)
    a = int(d["a"], 16)
    q = int(d["q"], 16)
    G = (int(d["Gx"], 16), int(d["Gy"], 16))
    Y = (int(d["Yx"], 16), int(d["Yy"], 16))
    return p, a, q, G, Y, d.get("curve", "?")


def _ts_to_us(h, mnt, s, frac):
    micros = int((frac + "000000")[:6])
    return (((h * 60 + mnt) * 60 + s) * 1_000_000) + micros


def sign_once(f, msg=None):
    f.write((("SIGN " + msg) if msg else "SIGN").encode() + b"\n")
    f.flush()
    stamps, kv = [], {}
    for line in _read_block(f):
        m = TS_RE.search(line)
        if m:
            stamps.append(_ts_to_us(int(m.group(1)), int(m.group(2)),
                                    int(m.group(3)), m.group(4)))
        elif "=" in line:
            k, v = line.split("=", 1)
            kv[k.strip()] = v.strip()
    elapsed_ms = ((stamps[-1] - stamps[0]) % 86_400_000_000) / 1000.0
    return int(kv["r"], 16), int(kv["s"], 16), int(kv["e"], 16), elapsed_ms


# ================================================================== #
#  Кэш собранного пула на диск (хранит фактический lz каждой подписи)  #
# ================================================================== #
def _pool_path(curve, L):
    return os.path.join(_HERE, f"pool_{curve}_L{L}.json")


def save_pool(path, q, Y, p, a, G, L, pool):
    obj = {"q": hex(q), "Y": [hex(Y[0]), hex(Y[1])],
           "p": hex(p), "a": hex(a), "G": [hex(G[0]), hex(G[1])], "L": L,
           "samples": [{"r": hex(s["r"]), "s": hex(s["s"]),
                        "e": hex(s["e"]), "lz": s["lz"]} for s in pool]}
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fp:
        json.dump(obj, fp)
    os.replace(tmp, path)


def load_pool(path, q, Y, L):
    if not os.path.exists(path):
        return None
    try:
        d = json.load(open(path, encoding="utf-8"))
        if (int(d["q"], 16) != q or d["L"] != L
                or int(d["Y"][0], 16) != Y[0] or int(d["Y"][1], 16) != Y[1]):
            return None
        return [{"r": int(s["r"], 16), "s": int(s["s"], 16),
                 "e": int(s["e"], 16), "lz": s["lz"]} for s in d["samples"]]
    except Exception:
        return None


# ================================================================== #
#  Сбор: калибровка + МНОГОПОТОЧНЫЙ сбор в общий пул (для конвейера)   #
# ================================================================== #
def calibrate_step(elapseds, w):
    seed = sorted(elapseds)[int(len(elapseds) * 0.97)] / w
    step = max(seed, 1e-4)
    for _ in range(6):
        ts = [max(1, round(e / step)) for e in elapseds]
        step = statistics.median(e / t for e, t in zip(elapseds, ts))
    return step


def harvest_into(pool, lock, need, threads, w, L,
                 solved, stop, path, q, Y, p, a, G):
    """Наполняет общий список pool (под lock) — работает ПАРАЛЛЕЛЬНО с решёткой."""
    s0, f0 = _connect()
    print(f"  разогрев 150 подписей для калибровки кванта...", flush=True)
    raw = [sign_once(f0) for _ in range(150)]
    step = calibrate_step([r[3] for r in raw], w)
    print(f"  оценён квант ≈ {step:.4f} мс/шаг; сбор в {threads} поток(ов)",
          flush=True)
    total = [150]
    t0 = time.time()

    def add(r, s, e, el):
        lz = w - round(el / step)
        if lz >= L:
            with lock:
                if len(pool) < need:
                    pool.append({"r": r, "s": s, "e": e, "lz": lz})

    for (r, s, e, el) in raw:
        add(r, s, e, el)

    def collector(f):
        while not (solved.is_set() or stop.is_set()):
            with lock:
                if len(pool) >= need:
                    break
            try:
                r, s, e, el = sign_once(f)
            except Exception:
                break
            with lock:
                total[0] += 1
                n = total[0]
            add(r, s, e, el)
            if n % 500 == 0:
                with lock:
                    have = len(pool)
                print(f"  запрошено {n}, годных {have}/{need} "
                      f"({time.time()-t0:.0f} с)", flush=True)
        try:
            f.write(b"QUIT\n")
            f.flush()
        except Exception:
            pass

    conns = [(s0, f0)] + [_connect() for _ in range(max(0, threads - 1))]
    with ThreadPoolExecutor(max_workers=len(conns)) as tex:
        futs = [tex.submit(collector, f) for (_, f) in conns]
        for fut in futs:
            fut.result()
    for (s, f) in conns:
        try:
            s.close()
        except Exception:
            pass
    with lock:
        snap = list(pool)
    save_pool(path, q, Y, p, a, G, L, snap)
    if not solved.is_set():
        print(f"  сбор завершён: {len(snap)} образцов, сохранено в "
              f"{os.path.basename(path)}", flush=True)


# ================================================================== #
#  Параллельный движок решётки                                        #
# ================================================================== #
_CTX = {}


def _init(q, p, a, G, Y, bkz):
    global BKZ_BLOCK
    BKZ_BLOCK = bkz
    _CTX.update(q=q, p=p, a=a, G=G, Y=Y)


def _worker(subset):
    d = recover_key(subset, _CTX["q"], _CTX["p"], _CTX["a"], _CTX["G"], _CTX["Y"])
    return d, len(subset)


def _pick_subset(pool, size, rng):
    """B — приоритет лучших подписей: берём из верхушки по lz со случайностью."""
    if len(pool) <= size:
        return list(pool)
    ranked = sorted(pool, key=lambda s: s["lz"], reverse=True)
    cand = ranked[:min(len(ranked), max(size * 2, size + 8))]
    return rng.sample(cand, size)


# ================================================================== #
def main():
    L_arg = int(sys.argv[1]) if len(sys.argv) > 1 else None
    bkz = int(sys.argv[2]) if len(sys.argv) > 2 else 0

    print("=" * 60)
    print("АТАКА (хост) на оракул ГОСТ — bit-length nonce через решётку (B+C+F)")
    print("=" * 60)
    print(f"оракул      : {HOST}:{PORT}")

    ps, pf = _connect()
    p, a, q, G, Y, curve = get_pubkey(pf)
    try:
        pf.write(b"QUIT\n")
        pf.flush()
    except Exception:
        pass
    ps.close()
    w = q.bit_length()

    L_req = L_arg if L_arg is not None else (6 if w > 64 else 3)
    L = min(L_req, w - 1)
    subset = min(max(6, (w + L - 1) // L + 3), w)
    need = subset + max(4, subset // 2)
    print(f"кривая      : {curve}   bitlen(q) = {w}")
    print(f"leak L      : {L}  (порог отбора; в решётку идёт фактический lz)")
    print(f"подвыборка  : ~{subset}   пул образцов: {need}")
    print(f"решатель    : {'fpylll' if _HAVE_FPYLLL else 'чистый Python'}"
          f"   BKZ = {bkz or 'выкл'}")
    print(f"потоки сбора : {HARVEST_THREADS}   воркеры решётки: {LATTICE_WORKERS}\n")

    path = _pool_path(curve, L)
    cached = load_pool(path, q, Y, L)
    pool = list(cached) if cached else []
    lock = threading.Lock()
    solved = threading.Event()
    stop_h = threading.Event()

    ht = None
    if len(pool) < need:
        print("Сбор подписей идёт ПАРАЛЛЕЛЬНО с решёткой (конвейер):")
        ht = threading.Thread(
            target=harvest_into,
            args=(pool, lock, need, HARVEST_THREADS, w, L,
                  solved, stop_h, path, q, Y, p, a, G), daemon=True)
        ht.start()
    else:
        print(f"Загружен пул из {os.path.basename(path)}: "
              f"{len(pool)} образцов (сбор пропущен).")

    workers = max(1, LATTICE_WORKERS)
    print(f"Решётка: {workers} процесс(ов), старт по мере накопления подписей.\n")
    ex = ProcessPoolExecutor(max_workers=workers, initializer=_init,
                             initargs=(q, p, a, G, Y, bkz))

    def _kill():
        for pr in list(getattr(ex, "_processes", {}).values()):
            try:
                pr.kill()
            except Exception:
                pass
        ex.shutdown(wait=False, cancel_futures=True)

    d_rec, attempt = None, 0
    t_start = time.time()
    try:
        while d_rec is None:
            with lock:
                have = len(pool)
            if have < subset:                    # ждём накопления для конвейера
                if ht is None or not ht.is_alive():
                    print("[!] образцов недостаточно, а сбор не идёт — стоп.")
                    break
                time.sleep(0.3)
                continue
            with lock:
                snap = list(pool)
            futs = [ex.submit(_worker,
                              _pick_subset(snap, subset,
                                           random.Random(random.randrange(1 << 30))))
                    for _ in range(workers)]
            for fut in as_completed(futs):
                attempt += 1
                d, sz = fut.result()
                print(f"  попытка {attempt} (размер {sz}, "
                      f"{time.time()-t_start:.0f} с): "
                      f"{'УСПЕХ' if d else 'неудача'}", flush=True)
                if d is not None:
                    d_rec = d
                    break
    except KeyboardInterrupt:
        solved.set()
        stop_h.set()
        _kill()
        print(f"\n[STOP] после {attempt} попыток, {time.time()-t_start:.0f} с."
              f"  (пул сохранится/уже сохранён — рестарт начнёт с решётки)")
        os._exit(0)

    solved.set()
    stop_h.set()
    if d_rec is not None:
        with lock:
            snap = list(pool)
        try:
            save_pool(path, q, Y, p, a, G, L, snap)  # сохранить даже частичный пул
        except Exception:
            pass
    _kill()

    if d_rec is None:
        print("\n[FAIL] ключ не восстановлен.")
        os._exit(1)
    print("\n" + "-" * 60)
    print("[OK] d*G == Y — секретный ключ восстановлен.")
    print(f"     (попытка {attempt}, {time.time()-t_start:.1f} с)")
    print(f"  dec : {d_rec}")
    print(f"  hex : {hex(d_rec)}")
    sys.stdout.flush()
    os._exit(0)


if __name__ == "__main__":
    main()
