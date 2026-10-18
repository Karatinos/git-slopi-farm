"""Automated reconnaissance of attachments (ACI booster, blueprint §2.3/§4.2).

Before the agent starts reasoning, run cheap read-only tools over the genuine
attachments in the sandbox and hand the agent a compact digest: file types,
metadata (exiftool — often carries GPS/author/timestamps for OSINT), OCR text
from images (tesseract), decoded QR/barcodes (zbarimg), and flag-grep over
strings. This is the "interactive tools + summariser" lever the literature shows
matters more than a bigger model — it turns unreadable images into text the
model can act on, without the agent spending steps discovering the toolchain.

All tools operate ONLY on files already inside the isolated sandbox.
"""
from __future__ import annotations

from ..sandbox.base import Sandbox

_RECON_SH = r"""
set -e 2>/dev/null || true
maxfiles=40; n=0
for f in $(find . -maxdepth 3 -type f ! -name '_snippet.py' ! -name 'TASK.md' 2>/dev/null); do
  n=$((n+1)); [ "$n" -gt "$maxfiles" ] && { echo "...(more files omitted)"; break; }
  echo "=== $f ==="
  file -b "$f" 2>/dev/null
  case "$f" in
    *.png|*.jpg|*.jpeg|*.bmp|*.gif|*.webp)
      exiftool -s -GPSPosition -GPSLatitude -GPSLongitude -DateTimeOriginal -Model -Software -ImageDescription -UserComment "$f" 2>/dev/null | sed 's/^/  meta: /'
      if command -v tesseract >/dev/null 2>&1; then
        txt=$(tesseract "$f" stdout -l rus+eng 2>/dev/null | tr -s ' \n' ' \n' | grep -vE '^[[:space:]]*$' | head -c 600)
        [ -n "$txt" ] && printf '  ocr: %s\n' "$txt"
      fi
      if command -v zbarimg >/dev/null 2>&1; then
        qr=$(zbarimg -q --raw "$f" 2>/dev/null | head -c 400)
        [ -n "$qr" ] && printf '  qr/barcode: %s\n' "$qr"
      fi
      ;;
    *)
      strings -n 6 "$f" 2>/dev/null | grep -iE 'flag\{|ctf|secret|password|http' | head -5 | sed 's/^/  str: /'
      ;;
  esac
  # flag hunt everywhere
  strings -n 4 "$f" 2>/dev/null | grep -oiE 'flag\{[^}]{1,120}\}' | head -3 | sed 's/^/  FLAG?: /'
done
"""


def signal_level(digest: str) -> str:
    """Classify how much exploitable signal recon found -> 'high' | 'low'.

    Used by the scheduler to allocate effort: pour the step budget into tasks
    with a real lead (OCR text, QR, metadata, a flag candidate), and quickly
    conclude on opaque ones instead of burning budget flailing.
    """
    if not digest:
        return "low"
    d = digest.lower()
    if "flag?:" in d or "qr/barcode:" in d:
        return "high"
    # meaningful OCR / metadata / strings content
    ocr_lines = [ln for ln in digest.splitlines()
                 if ln.strip().startswith(("ocr:", "meta:", "str:"))]
    text_len = sum(len(ln) for ln in ocr_lines)
    if text_len >= 60:
        return "high"
    if "no readable content" in d or "recon failed" in d:
        return "low"
    return "low"


def run_recon(sandbox: Sandbox, max_chars: int = 5000) -> str:
    try:
        res = sandbox.run(_RECON_SH, timeout=90)
    except Exception as e:  # noqa: BLE001
        return f"(recon failed: {e})"
    out = (res.stdout or "").strip()
    if not out:
        return "(recon produced no readable content — files may be opaque binaries or images without text)"
    if len(out) > max_chars:
        out = out[:max_chars] + "\n...(recon truncated)"
    return out
