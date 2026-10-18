#!/usr/bin/env python3
"""
OpenRouter preflight for slopi-farm. Run in a REAL terminal (NOT the Claude sandbox):
    export OPENROUTER_API_KEY=sk-or-v1-...   # or pass as first arg
    python3 preflight_openrouter.py
Writes a report to farm/data/preflight_result.json (readable by Claude).
Cost: one tiny completion (~$0.0001) + one small reasoning probe (~a few $0.0001).
"""
import os, sys, json, time, urllib.request, urllib.error

BASE = "https://openrouter.ai/api/v1"
KEY  = os.environ.get("OPENROUTER_API_KEY") or (sys.argv[1] if len(sys.argv) > 1 else "")
OUT  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "preflight_result.json")
report = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "steps": {}}

def done(code=0):
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(report, open(OUT, "w"), ensure_ascii=False, indent=2)
    print("\n== wrote", OUT, "==")
    sys.exit(code)

if not KEY:
    report["fatal"] = "No OPENROUTER_API_KEY in env and none passed as arg 1."
    print(report["fatal"]); done(2)

def call(path, data=None, timeout=90):
    hdr = {"Authorization": "Bearer " + KEY, "Content-Type": "application/json",
           "HTTP-Referer": "https://localhost/slopi-farm", "X-Title": "slopi-farm-preflight"}
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(BASE + path, data=body, headers=hdr,
                                 method="POST" if data is not None else "GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        try: payload = json.loads(e.read().decode() or "{}")
        except Exception: payload = {}
        return e.code, payload
    except Exception as e:
        return 0, {"error": repr(e)}

# 1) key / credits
print("[1] checking key + credits ...")
s, d = call("/key")
report["steps"]["key"] = {"http": s, "data": d.get("data", d)}
print("    HTTP", s, json.dumps(d.get("data", d))[:300])

# 2) list deepseek models (free)
print("[2] listing deepseek models ...")
s, d = call("/models")
ds = []
if s == 200:
    for m in d.get("data", []):
        mid = m.get("id", "")
        if "deepseek" in mid.lower():
            pr = m.get("pricing", {})
            ds.append({"id": mid,
                       "ctx": m.get("context_length"),
                       "in": pr.get("prompt"), "out": pr.get("completion"),
                       "supported": m.get("supported_parameters", [])})
report["steps"]["models_http"] = s
report["steps"]["deepseek_models"] = ds
for m in ds:
    print("   ", m["id"], "| ctx", m["ctx"], "| in", m["in"], "out", m["out"],
          "| reasoning" if "reasoning" in (m["supported"] or []) else "")
print("    total deepseek models:", len(ds))

# pick a 'flash'/cheap deepseek slug for the ping
def pick(models):
    for m in models:
        if "flash" in m["id"].lower(): return m["id"]
    for m in models:
        if "chat" in m["id"].lower(): return m["id"]
    return models[0]["id"] if models else None
slug = pick(ds)
report["chosen_slug"] = slug
print("    chosen slug for ping:", slug)

if not slug:
    report["fatal"] = "No deepseek model slug found."
    done(1)

# 3) one tiny completion
print("[3] tiny completion ...")
s, d = call("/chat/completions", {
    "model": slug,
    "messages": [{"role": "user", "content": "Reply with exactly: OK"}],
    "max_tokens": 10, "temperature": 0,
})
ok = False; msg = ""
if s == 200:
    try:
        msg = d["choices"][0]["message"]["content"]
        ok = "OK" in (msg or "").upper()
    except Exception as e:
        msg = "parse error " + repr(e)
report["steps"]["ping"] = {"http": s, "content": msg,
                           "usage": d.get("usage"), "ok": ok,
                           "error": d.get("error")}
print("    HTTP", s, "| content:", repr(msg), "| usage:", d.get("usage"), "| err:", d.get("error"))

# 4) reasoning toggle probe
print("[4] reasoning probe ...")
s, d = call("/chat/completions", {
    "model": slug,
    "messages": [{"role": "user", "content": "What is 17*23? Think, then give only the number."}],
    "max_tokens": 400, "temperature": 0,
    "reasoning": {"effort": "low"},
})
rc = None; content = ""
if s == 200:
    try:
        ch = d["choices"][0]["message"]
        content = ch.get("content", "")
        rc = ch.get("reasoning") or ch.get("reasoning_details")
    except Exception as e:
        content = "parse error " + repr(e)
report["steps"]["reasoning"] = {"http": s,
                                "has_reasoning_field": bool(rc),
                                "reasoning_preview": (str(rc)[:200] if rc else None),
                                "content": content, "usage": d.get("usage"),
                                "error": d.get("error")}
print("    HTTP", s, "| reasoning_returned:", bool(rc), "| answer:", repr(content[:60]),
      "| err:", d.get("error"))

report["verdict"] = {
    "key_ok": report["steps"]["key"].get("http") == 200,
    "models_ok": report["steps"].get("models_http") == 200,
    "ping_ok": report["steps"]["ping"].get("ok") is True,
    "reasoning_ok": report["steps"]["reasoning"].get("has_reasoning_field") is True,
}
print("\nVERDICT:", json.dumps(report["verdict"]))
done(0)
