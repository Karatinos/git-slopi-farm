"""inspect_image — turn an image into structured text a text-only model can use.

DeepSeek models are text-only, so a figure (a map with coordinates, a chart, a
schematic) must be converted into data. This module holds the helper script that
runs INSIDE the sandbox (python3 + PIL + numpy + tesseract; OpenCV when present)
and prints:

  * OCR text items with pixel positions and colour (tesseract TSV),
  * coloured filled regions / strokes (connected components per colour, neutral
    white/grey/black treated as background) with polygon vertices in pixels,
  * point markers (small dark saturated blobs),
  * a pixel->figure-units affine fit from "(x, y)"-style labels paired with their
    nearest markers, flagging labels that disagree with the fit (OCR slips such
    as a dropped minus sign) and giving every marker/vertex in figure units.
"""

SCRIPT = r'''
import sys, re, subprocess
from PIL import Image
import numpy as np
try:
    import cv2
except Exception:
    cv2 = None

path = sys.argv[1]
im = Image.open(path).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(int)
print(f"IMAGE {path}: {W}x{H} px (x right, y DOWN; origin top-left)")

# ---------------- OCR ----------------
items = []
try:
    tsv = subprocess.run(["tesseract", path, "stdout", "-l", "rus+eng", "--psm", "11", "tsv"],
                         capture_output=True, text=True, timeout=60).stdout
    words = []
    for ln in tsv.splitlines()[1:]:
        p = ln.split("\t")
        if len(p) < 12 or not p[11].strip() or float(p[10]) < 20:
            continue
        x, y, w, h = map(int, p[6:10])
        words.append([y, x, w, h, p[11]])
    words.sort()
    for y, x, w, h, t in words:
        for L in items:
            if abs(L["y"] - y) <= max(4, h // 2) and 0 <= x - L["x2"] <= max(12, h):
                L["t"] += " " + t; L["x2"] = x + w; break
        else:
            items.append({"y": y, "x": x, "x2": x + w, "h": h, "t": t})
    print(f"\nOCR TEXT ({len(items)} items): text @ (x_center, y_center) px")
    for L in sorted(items, key=lambda L: (L["y"], L["x"])):
        L["cx"], L["cy"] = (L["x"] + L["x2"]) // 2, L["y"] + L["h"] // 2
        print(f"  {L['t']!r} @ ({L['cx']}, {L['cy']})")
except Exception as e:
    print("OCR failed:", e)

# ---------------- colour segmentation (HSV) ----------------
hsv = np.asarray(im.convert("HSV")).astype(int)
Hh, S, V = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]

def comps(mask):
    if cv2 is None:
        return []
    n, lab, st, cen = cv2.connectedComponentsWithStats(mask.astype(np.uint8), 8)
    return [(lab == i, st[i], cen[i]) for i in range(1, n)]

def polygon(m):
    # convex hull first: labels/lines drawn over a fill cut notches into it
    if cv2 is None:
        return []
    cs, _ = cv2.findContours(m.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cc = cv2.convexHull(max(cs, key=cv2.contourArea))
    ap = cv2.approxPolyDP(cc, 0.02 * cv2.arcLength(cc, True), True)
    return [tuple(int(t) for t in p[0]) for p in ap]

def hue_name(h):
    d = h * 360 / 255
    for lim, nm in ((15, "red"), (45, "orange"), (70, "yellow"), (160, "green"),
                    (200, "cyan"), (260, "blue"), (300, "purple"), (345, "pink"), (361, "red")):
        if d < lim:
            return nm

# markers: compact saturated blobs (points), any hue. Morphological opening
# removes the thin outline strokes the dots are drawn on, keeping the dots.
mk_mask = (S >= 90) & (V >= 60)
if cv2 is not None:
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mk_mask = cv2.morphologyEx(mk_mask.astype(np.uint8), cv2.MORPH_OPEN, k).astype(bool)
markers = []
for m, st, cen in comps(mk_mask):
    x, y, w, h, area = [int(t) for t in st]
    if 4 <= w <= 22 and 4 <= h <= 22 and area >= 0.45 * w * h and abs(w - h) <= 5:
        markers.append((float(cen[0]), float(cen[1]), hue_name(int(np.median(Hh[m])))))

# filled regions: pastel fills (low saturation, bright), grouped by hue bin
fill_mask = (S >= 10) & (S < 90) & (V >= 190)
regions = []
for hb in range(0, 256, 16):
    hm = fill_mask & (Hh >= hb) & (Hh < hb + 16)
    if hm.sum() < 400:
        continue
    for m, st, cen in comps(hm):
        x, y, w, h, area = [int(t) for t in st]
        if area < 400:
            continue
        regions.append({"hue": hue_name(hb + 8), "area": area, "bbox": (x, y, w, h),
                        "c": (float(cen[0]), float(cen[1])), "poly": polygon(m)})

def dist_to_poly(px, py, poly):
    if len(poly) < 2:
        return 1e9
    best = 1e9
    for i in range(len(poly)):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % len(poly)]
        dx, dy = x2 - x1, y2 - y1
        t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy or 1)))
        best = min(best, ((px - x1 - t * dx) ** 2 + (py - y1 - t * dy) ** 2) ** 0.5)
    return best

print(f"\nFILLED REGIONS ({len(regions)}):")
for i, r in enumerate(sorted(regions, key=lambda r: -r["area"])):
    r["id"] = i
    print(f"  region#{i} {r['hue']} fill area={r['area']} bbox={r['bbox']} "
          f"centroid=({r['c'][0]:.0f},{r['c'][1]:.0f}) vertices_px={r['poly']}")
print(f"\nMARKERS (points): {len(markers)}")
mk_region = []
for x, y, hn in sorted(markers, key=lambda t: (t[1], t[0])):
    near = min(regions, key=lambda r: dist_to_poly(x, y, r["poly"])) if regions else None
    dd = dist_to_poly(x, y, near["poly"]) if near else 1e9
    tag = f" on region#{near['id']} ({near['hue']})" if near and dd <= 12 else ""
    mk_region.append((x, y, hn, near["id"] if near and dd <= 12 else None))
    print(f"  {hn} marker @ ({x:.0f}, {y:.0f}){tag}")
markers = [(x, y, hn) for x, y, hn, _ in mk_region]

# ---------------- label <-> marker affine fit ----------------
num = r"[-−–]?\s*\d+(?:[.,]\d+)?"
pairs = []
for L in items:
    m = re.search(r"\(\s*(" + num + r")\s*[,;]\s*(" + num + r")\s*\)", L["t"])
    if not m or not markers:
        continue
    fx, fy = (float(g.replace("−", "-").replace("–", "-").replace(" ", "").replace(",", "."))
              for g in m.groups())
    mk = min(markers, key=lambda k: (k[0] - L["cx"]) ** 2 + (k[1] - L["cy"]) ** 2)
    pairs.append((L["t"], fx, fy, mk[0], mk[1]))
if len(pairs) >= 4:
    P = np.array([[p[3], p[4], 1.0] for p in pairs]); X = np.array([p[1] for p in pairs]); Y = np.array([p[2] for p in pairs])
    def robust(Z):
        keep = np.ones(len(Z), bool)
        for _ in range(3):
            coef, *_ = np.linalg.lstsq(P[keep], Z[keep], rcond=None)
            res = np.abs(P @ coef - Z)
            thr = max(1.0, 3 * np.median(res[keep]) + 1e-9)
            keep = res <= thr
        return coef, P @ coef
    cx, px = robust(X); cy, py = robust(Y)
    print("\nLABEL <-> MARKER FIT (pixel -> figure units, least squares, outliers flagged):")
    for (t, fx, fy, mx, my), ex, ey in zip(pairs, px, py):
        bad = abs(ex - fx) > 2 or abs(ey - fy) > 2
        flag = f"   <-- DISAGREES: fit predicts ({ex:.1f}, {ey:.1f}); OCR likely misread" if bad else ""
        print(f"  label {t!r} marker_px=({mx:.0f},{my:.0f}) fit=({ex:.1f}, {ey:.1f}){flag}")
    to_units = lambda x, y: tuple(round(float(v), 1) for v in
                                  (cx[0] * x + cx[1] * y + cx[2], cy[0] * x + cy[1] * y + cy[2]))
    print("  markers in figure units:")
    for x, y, hn, rid in mk_region:
        print(f"    {hn} marker px=({x:.0f},{y:.0f}) -> {to_units(x, y)}"
              + (f" on region#{rid}" if rid is not None else ""))
    for r in regions:
        if r["poly"]:
            print(f"  region#{r['id']} ({r['hue']}) vertices in figure units:",
                  [to_units(*p) for p in r["poly"]])
print("\nHint: labels flagged as DISAGREES are OCR slips — trust the fit. Verify "
      "the reconstructed geometry against the picture's layout before using it.")
'''


def run_inspect(sandbox, path: str, max_chars: int = 7000) -> str:
    sandbox.write_file("_inspect_image.py", SCRIPT)
    res = sandbox.run(f"python3 _inspect_image.py {_q(path)}")
    out = (res.stdout or "") + (("\n[stderr] " + res.stderr[-800:]) if res.exit_code else "")
    return out[:max_chars]


def _q(s: str) -> str:
    return "'" + s.replace("'", "'\"'\"'") + "'"
