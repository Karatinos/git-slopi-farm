"""Local interactive judge for 'Аккуратный подъём'.

Terrain families: cone, plateau-cone, cliff-cone (walls with |dh|>=2 forcing a
detour). Checks: protocol (5 numbers after every command incl. turns), no tipping
(|dh|<=1 on moves), SNP exactly at the unique peak, <=100 commands. Reports the
command count vs the omniscient optimum (BFS over (x,y,heading)).
"""
import random, subprocess, sys
from collections import deque

DX = [0, 1, 0, -1]; DY = [1, 0, -1, 0]
LOW = -10**6


def strict_maxima(H):
    out = []
    for (x, y), h in H.items():
        if all(H.get((x + DX[d], y + DY[d]), LOW) < h for d in range(4)):
            out.append((x, y))
    return out


def make(kind, rng, R=12):
    """Terrain respecting the statement's guarantee: exactly one strict local
    maximum (the peak), reachable from the start. Families exercise greedy
    ascent (cone), plateaus (equal neighbours), trenches (sideways detour) and
    bumps/rough (a higher neighbour that is +2, forcing a descent to go around)."""
    for _ in range(200):
        px, py = rng.randint(-4, 4), rng.randint(-4, 4)
        K = 40
        H = {}
        for x in range(-R, R + 1):
            for y in range(-R, R + 1):
                d = abs(x - px) + abs(y - py)
                H[(x, y)] = K - (d + 1) // 2 if kind == "plateau" else K - d
        if kind == "trench":
            w = rng.randint(2, 6)
            for x in range(-R, R + 1):
                if x != px and (px - R) <= x <= (px + R):
                    c = (x, py - w)
                    if c in H: H[c] -= 2
        if kind in ("bumps", "rough"):
            n = rng.randint(3, 12) if kind == "bumps" else len(H) // 3
            for c in rng.sample(sorted(H), n):
                if c != (px, py): H[c] += 1
        if strict_maxima(H) == [(px, py)]:
            return H, (px, py)
    return None, None


def neighbours(H, x, y):
    return [H.get((x + DX[d], y + DY[d]), LOW) for d in range(4)]


def optimum(H, start, hd, peak):
    q = deque([(start[0], start[1], hd, 0)]); seen = {(start[0], start[1], hd)}
    while q:
        x, y, h, c = q.popleft()
        if (x, y) == peak: return c
        moves = [(x, y, (h + 3) % 4), (x, y, (h + 1) % 4)]
        for k in (0, 2):
            d = (h + k) % 4; n = (x + DX[d], y + DY[d])
            if n in H and abs(H[n] - H[(x, y)]) <= 1: moves.append((n[0], n[1], h))
        for s in moves:
            if s not in seen: seen.add(s); q.append((*s, c + 1))
    return None


def run(binary, H, peak, start, hd):
    opt = optimum(H, start, hd, peak)
    if opt is None: return None
    p = subprocess.Popen([binary], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
    x, y = start; cmds = 0

    def view():
        n = neighbours(H, x, y)
        f, r, b, l = n[hd], n[(hd + 1) % 4], n[(hd + 2) % 4], n[(hd + 3) % 4]
        p.stdin.write(f"{H[(x, y)]} {f} {b} {l} {r}\n"); p.stdin.flush()

    view()
    while True:
        line = p.stdout.readline().strip()
        if not line: return ("NO_OUTPUT", cmds, opt)
        if line == "SNP":
            p.wait(timeout=5)
            return ("OK" if (x, y) == peak else f"WRONG_SNP at {(x,y)}", cmds, opt)
        cmds += 1
        if cmds > 400: p.kill(); return ("TOO_MANY", cmds, opt)
        if line == "RL": hd = (hd + 3) % 4
        elif line == "RR": hd = (hd + 1) % 4
        elif line in ("FW", "BW"):
            d = hd if line == "FW" else (hd + 2) % 4
            n = (x + DX[d], y + DY[d])
            if n not in H or abs(H[n] - H[(x, y)]) > 1:
                p.kill(); return (f"TIPPED {line} {H[(x,y)]}->{H.get(n)}", cmds, opt)
            x, y = n
        else:
            p.kill(); return (f"PE {line!r}", cmds, opt)
        view()


if __name__ == "__main__":
    binary = sys.argv[1]
    rng = random.Random(7)
    stats = {}
    worst = 0
    for kind in ("cone", "plateau", "trench", "bumps", "rough"):
        for t in range(150):
            H, peak = make(kind, rng)
            if H is None: continue
            start = (rng.randint(-10, 10), rng.randint(-10, 10)); hd = rng.randint(0, 3)
            res = run(binary, H, peak, start, hd)
            if res is None: continue
            verdict, cmds, opt = res
            key = (kind, verdict if verdict == "OK" else verdict.split()[0])
            stats[key] = stats.get(key, 0) + 1
            if verdict != "OK": print(kind, t, verdict, cmds, opt)
            elif cmds > 100: print(kind, t, "OVER100", cmds, opt)
            else: worst = max(worst, cmds - opt)
    print(stats); print("max(cmds - omniscient_opt) on OK runs:", worst)
