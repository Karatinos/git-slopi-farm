#!/usr/bin/env python3
"""Generate a self-contained benchmark explorer (one HTML) to browse tasks.

Shows, per task: the statement the AGENT sees (redacted), staged files (agent-
visible), quarantined files (hidden from the agent), integrity label, and the
gold flag behind a spoiler. Covers both the clean synthetic benchmark and the
real Кубок tasks. File links are relative to the PROJECT ROOT, so serve it from
there:  python3 -m http.server 8000  →  http://localhost:8000/benchmark_explorer.html
"""
from __future__ import annotations
import html, json, os, sys
from pathlib import Path

HERE = Path(__file__).resolve()
FARM = HERE.parent.parent                      # .../farm
ROOT = FARM.parent                             # .../slopi-popi (project root)
sys.path.insert(0, str(FARM))
from farm.adapters.local_source import LocalSource  # noqa: E402

def rel(p) -> str:
    try:
        return os.path.relpath(str(p), str(ROOT))
    except Exception:
        return str(p)

def collect(path, answer_key_file, bench, integ=None):
    ak = {}
    akf = ROOT / answer_key_file
    if akf.exists():
        ak = json.loads(akf.read_text(encoding="utf-8")).get("flags", {})
    src = LocalSource(str(ROOT / path), answer_key=ak)
    recs = src.read()
    # map quarantined (relative to its own root) -> absolute-ish for linking
    q_by_task = {}
    for q in src.quarantined:
        # q is relative to the source root; task id is first two path parts
        parts = q.split("/")
        tid = f"{parts[0].lower()}/{parts[1]}" if len(parts) >= 2 else q
        q_by_task.setdefault(tid, []).append(q)
    out = []
    for r in recs:
        golds = ([r["gold"]] if isinstance(r["gold"], str) else []) + (r["extra"].get("gold_any") or [])
        label = (integ or {}).get(r["id"], {}).get("label", "clean" if bench == "clean" else "?")
        staged = [{"name": b, "path": rel(hp)} for hp, b in r["files"]]
        quar = [{"name": qp.split("/")[-1], "path": rel(ROOT / path / qp)}
                for qp in q_by_task.get(r["id"], [])]
        out.append({"bench": bench, "id": r["id"], "name": r["name"],
                    "category": r["category"], "label": label,
                    "statement": (r["statement"] or "")[:2500],
                    "staged": staged, "quarantined": quar,
                    "gold": [g for g in golds if g]})
    return out

def main():
    integ = {}
    f = ROOT / "farm/data/benchmark_integrity.json"
    if f.exists():
        integ = json.loads(f.read_text(encoding="utf-8")).get("per_task", {})
    data = []
    data += collect("farm/research/clean_bench", "farm/data/answer_key_clean.json", "clean")
    data += collect("tasks/Кубок Федерации. Отборочный CTF TB",
                    "farm/data/answer_key.json", "kubok", integ)
    payload = json.dumps(data, ensure_ascii=False)
    tpl = TEMPLATE.replace("/*DATA*/", payload)
    outp = ROOT / "benchmark_explorer.html"
    outp.write_text(tpl, encoding="utf-8")
    print("wrote", outp, f"({len(data)} tasks)")

TEMPLATE = r"""<!doctype html><html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>slopi-farm · benchmark explorer</title>
<style>
:root{--bg:#0f1420;--panel:#161d2b;--card:#1b2435;--ink:#e6edf3;--mut:#9aa7b8;--faint:#6b7889;
--line:#2a3550;--accent:#4a9eff;--good:#3fb96b;--warn:#e0a23c;--bad:#e5556b;--pill:#223052;}
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif;background:var(--bg);color:var(--ink);font-size:15px}
header{padding:14px 20px;border-bottom:1px solid var(--line);display:flex;gap:16px;align-items:center;flex-wrap:wrap;position:sticky;top:0;background:var(--bg);z-index:5}
h1{font-size:17px;margin:0;font-weight:700}
.sub{color:var(--mut);font-size:13px}
input,select{background:var(--panel);border:1px solid var(--line);color:var(--ink);border-radius:8px;padding:7px 10px;font-size:14px}
.wrap{display:grid;grid-template-columns:320px 1fr;gap:0;height:calc(100vh - 59px)}
.list{overflow:auto;border-right:1px solid var(--line);padding:8px}
.detail{overflow:auto;padding:20px 26px}
.cat{color:var(--faint);font-size:11px;text-transform:uppercase;letter-spacing:.5px;margin:12px 6px 4px}
.item{padding:8px 10px;border-radius:8px;cursor:pointer;display:flex;justify-content:space-between;gap:8px;align-items:center}
.item:hover{background:var(--panel)}.item.sel{background:var(--card);outline:1px solid var(--line)}
.name{font-size:14px}
.tag{font-size:10px;font-weight:700;padding:2px 7px;border-radius:20px;white-space:nowrap}
.t-clean{background:#123224;color:var(--good)} .t-needs{background:#3a2e12;color:var(--warn)}
.t-writeup{background:#3a1720;color:var(--bad)} .t-unknown{background:var(--pill);color:var(--mut)}
.bench{font-size:10px;color:var(--faint)}
h2{font-size:22px;margin:0 0 2px} .meta{color:var(--mut);font-size:13px;margin-bottom:14px}
.sec{margin:16px 0}
.sec h3{font-size:12px;text-transform:uppercase;letter-spacing:.5px;color:var(--faint);margin:0 0 7px}
.stmt{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px;white-space:pre-wrap;color:#cdd8e6;font-size:13.5px;max-height:320px;overflow:auto}
.files{display:flex;flex-direction:column;gap:5px}
a.file{color:var(--accent);text-decoration:none;background:var(--card);border:1px solid var(--line);border-radius:8px;padding:7px 11px;font-size:13.5px;display:flex;justify-content:space-between}
a.file:hover{border-color:var(--accent)}
.q a.file{color:var(--bad);border-style:dashed}
.note{color:var(--mut);font-size:12.5px;margin:4px 0 8px}
.gold{margin-top:6px}
.spoiler{background:#0c1a12;border:1px solid #1d3a28;color:#6b7889;border-radius:8px;padding:9px 12px;cursor:pointer;font-family:ui-monospace,Menlo,monospace;font-size:13px}
.spoiler.on{color:var(--good)}
.empty{color:var(--faint);font-size:13px;font-style:italic}
.kpill{display:inline-block;background:var(--pill);color:var(--mut);border-radius:6px;padding:1px 7px;font-size:11px;margin-left:6px}
</style></head><body>
<header>
  <div><h1>slopi-farm · benchmark explorer</h1><div class="sub">что видит агент · что в карантине · флаг под спойлером</div></div>
  <input id="q" placeholder="поиск по названию…" style="margin-left:auto;width:220px">
  <select id="fb"><option value="">все наборы</option><option value="clean">clean_bench</option><option value="kubok">Кубок</option></select>
  <select id="fl"><option value="">все классы</option><option value="clean-offline">clean-offline</option><option value="needs-remote/web">needs-remote/web</option><option value="writeup-only/no-artifact">writeup-only</option></select>
</header>
<div class="wrap">
  <div class="list" id="list"></div>
  <div class="detail" id="detail"><p class="empty">Выбери задачу слева.</p></div>
</div>
<script>
const DATA = /*DATA*/;
const LB={"clean":"t-clean","clean-offline":"t-clean","needs-remote/web":"t-needs","writeup-only/no-artifact":"t-writeup"};
const enc = p => p.split("/").map(encodeURIComponent).join("/");
let sel=null;
function render(){
  const q=document.getElementById("q").value.toLowerCase();
  const fb=document.getElementById("fb").value, fl=document.getElementById("fl").value;
  const list=document.getElementById("list"); list.innerHTML="";
  const groups={};
  DATA.filter(t=>(!q||((t.name+t.id).toLowerCase().includes(q)))&&(!fb||t.bench===fb)&&(!fl||t.label===fl))
      .forEach(t=>{(groups[t.bench+" · "+t.category]??=[]).push(t)});
  Object.keys(groups).sort().forEach(g=>{
    const h=document.createElement("div");h.className="cat";h.textContent=g;list.appendChild(h);
    groups[g].forEach(t=>{
      const d=document.createElement("div");d.className="item"+(sel===t?" sel":"");
      d.innerHTML=`<span class="name">${t.name}</span><span class="tag ${LB[t.label]||'t-unknown'}">${t.label}</span>`;
      d.onclick=()=>{sel=t;render();detail(t)};list.appendChild(d);
    });
  });
}
function filelist(arr){ if(!arr.length) return '<div class="empty">—</div>';
  return '<div class="files">'+arr.map(f=>`<a class="file" href="${enc(f.path)}" target="_blank">${f.name}<span class="bench">открыть ↗</span></a>`).join("")+'</div>';}
function detail(t){
  const d=document.getElementById("detail");
  const gold = t.gold.length? `<div class="gold"><div class="spoiler" onclick="this.classList.toggle('on');this.textContent=this.classList.contains('on')?${JSON.stringify(t.gold.join('  |  '))}:'🔒 показать флаг ('+${t.gold.length}+')'">🔒 показать флаг (${t.gold.length})</div></div>`
     : '<div class="empty">нет золотого флага (unscored)</div>';
  d.innerHTML=`<h2>${t.name} <span class="kpill">${t.bench}</span></h2>
    <div class="meta">${t.id} · класс: <b>${t.label}</b></div>
    <div class="sec"><h3>Условие (что видит агент, флаг вырезан)</h3><div class="stmt">${(t.statement||'—').replace(/</g,'&lt;')}</div></div>
    <div class="sec"><h3>Файлы агенту (staged · ${t.staged.length})</h3>${filelist(t.staged)}</div>
    <div class="sec"><h3>Карантин — скрыто от агента (${t.quarantined.length})</h3>
      <div class="note">решения/разборы: агент их НЕ видит; тебе — для проверки</div>${filelist(t.quarantined)}</div>
    <div class="sec"><h3>Золотой флаг (ответ)</h3>${gold}</div>`;
}
document.getElementById("q").oninput=render;
document.getElementById("fb").onchange=render;
document.getElementById("fl").onchange=render;
render();
</script></body></html>"""

if __name__ == "__main__":
    main()
