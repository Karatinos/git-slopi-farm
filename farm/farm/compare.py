"""Aggregate farm runs into a KPI comparison (table + chart).

    python -m farm.compare --labels clean_p1 clean_p2 ... --out data/runs/compare
    python -m farm.compare --glob 'clean_p*'            # all matching runs

Reads data/runs/outcomes_<label>.json, computes per-run KPIs (solve-rate,
spend, cost-per-flag, median time-to-flag, escalation-rate) and writes
<out>.md and <out>.png (two single-axis panels: solve-rate and cost-per-flag).
"""
from __future__ import annotations
import argparse, glob as _glob, json, statistics
from pathlib import Path
from .config import DATA_DIR

RUNS = DATA_DIR / "runs"
INK, MUT, ACC1, ACC2, GRID = "#14181f", "#5b6472", "#1f6feb", "#2f9e63", "#e2e6ec"


def kpis(rows):
    tasks = len(rows)
    correct = [r for r in rows if r.get("correct")]
    graded = [r for r in rows if r.get("grade") in ("correct", "incorrect")]
    spend = sum(r.get("cost_usd", 0) for r in rows)
    ttf = [r.get("wall_seconds", 0) for r in correct if r.get("wall_seconds")]
    esc = sum(1 for r in rows if r.get("escalated"))
    return {
        "tasks": tasks, "correct": len(correct), "graded": len(graded),
        "solve_rate": (len(correct) / len(graded)) if graded else 0.0,
        "spend": spend,
        "cost_per_flag": (spend / len(correct)) if correct else float("nan"),
        "median_ttf": statistics.median(ttf) if ttf else 0.0,
        "escalation_rate": (esc / tasks) if tasks else 0.0,
    }


def load(label):
    p = RUNS / f"outcomes_{label}.json"
    return json.loads(p.read_text(encoding="utf-8"))


def chart(labels, K, out_png):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
    x = range(len(labels))
    sr = [K[l]["solve_rate"] * 100 for l in labels]
    cpf = [0 if K[l]["cost_per_flag"] != K[l]["cost_per_flag"] else K[l]["cost_per_flag"] for l in labels]
    for ax, vals, color, title, fmt in (
        (ax1, sr, ACC1, "Solve-rate (%)", lambda v: f"{v:.0f}%"),
        (ax2, cpf, ACC2, "Cost per flag ($)", lambda v: f"${v:.4f}")):
        bars = ax.bar(x, vals, color=color, width=0.62, zorder=3)
        ax.set_title(title, color=INK, fontsize=12, fontweight="bold", loc="left", pad=10)
        ax.set_xticks(list(x)); ax.set_xticklabels(labels, color=MUT, fontsize=10)
        ax.tick_params(axis="y", colors=MUT, labelsize=9)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        for s in ("left", "bottom"):
            ax.spines[s].set_color(GRID)
        ax.grid(axis="y", color=GRID, linewidth=1, zorder=0)
        ax.set_axisbelow(True)
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, b.get_height(), fmt(v),
                    ha="center", va="bottom", color=INK, fontsize=9, fontweight="bold")
        ax.margins(y=0.18)
    fig.suptitle("Farm prototype comparison", color=INK, fontsize=14,
                 fontweight="bold", x=0.02, ha="left")
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(out_png, dpi=150, facecolor="white")
    return out_png


def md(labels, K):
    L = ["# Prototype comparison", "",
         "| prototype | solve-rate | correct/graded | spend $ | cost/flag $ | median TTF s | escalation |",
         "|---|---|---|---|---|---|---|"]
    for l in labels:
        k = K[l]
        cpf = "-" if k["cost_per_flag"] != k["cost_per_flag"] else f"{k['cost_per_flag']:.4f}"
        L.append(f"| {l} | {k['solve_rate']:.0%} | {k['correct']}/{k['graded']} | "
                 f"{k['spend']:.4f} | {cpf} | {k['median_ttf']:.0f} | {k['escalation_rate']:.0%} |")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(prog="farm.compare")
    ap.add_argument("--labels", nargs="*", default=None)
    ap.add_argument("--glob", default=None, help="label glob, e.g. 'clean_p*'")
    ap.add_argument("--out", default=str(RUNS / "compare"))
    a = ap.parse_args()
    labels = a.labels or []
    if a.glob:
        labels += sorted(Path(p).stem.replace("outcomes_", "")
                         for p in _glob.glob(str(RUNS / f"outcomes_{a.glob}.json")))
    labels = list(dict.fromkeys(labels))
    if not labels:
        raise SystemExit("no runs matched")
    K = {l: kpis(load(l)) for l in labels}
    Path(a.out + ".md").write_text(md(labels, K), encoding="utf-8")
    png = chart(labels, K, a.out + ".png")
    print(md(labels, K))
    print("chart ->", png)
    print("table ->", a.out + ".md")


if __name__ == "__main__":
    main()
