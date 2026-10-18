"""Progress / metrics report generation (PDF).

A small reportlab wrapper so the farm can emit self-contained PDF progress
reports into progress/. Supports headings, paragraphs, bullet lists, tables and
embedded matplotlib charts. Kept dependency-light and defensive so a report is
always produced even if a chart fails.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import List, Optional, Sequence

import os

import matplotlib
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, ListFlowable,
    ListItem, HRFlowable,
)

_ACCENT = colors.HexColor("#0f766e")
_MUTED = colors.HexColor("#64748b")
_BG = colors.HexColor("#f1f5f9")

# reportlab's built-in fonts have no Cyrillic glyphs, so Russian text renders as
# tofu boxes. Register the DejaVu TTFs that ship with matplotlib (Unicode) and
# use them everywhere. Font family name is "DVSans" / "DVMono".
_FONT_SANS = "DVSans"
_FONT_MONO = "DVMono"
_registered = False


def _register_fonts() -> None:
    global _registered
    if _registered:
        return
    ttf = os.path.join(os.path.dirname(matplotlib.__file__),
                       "mpl-data", "fonts", "ttf")
    try:
        pdfmetrics.registerFont(TTFont(_FONT_SANS, os.path.join(ttf, "DejaVuSans.ttf")))
        pdfmetrics.registerFont(TTFont(_FONT_SANS + "-Bold",
                                       os.path.join(ttf, "DejaVuSans-Bold.ttf")))
        pdfmetrics.registerFont(TTFont(_FONT_SANS + "-Oblique",
                                       os.path.join(ttf, "DejaVuSans-Oblique.ttf")))
        pdfmetrics.registerFont(TTFont(_FONT_MONO,
                                       os.path.join(ttf, "DejaVuSansMono.ttf")))
        pdfmetrics.registerFontFamily(
            _FONT_SANS, normal=_FONT_SANS, bold=_FONT_SANS + "-Bold",
            italic=_FONT_SANS + "-Oblique", boldItalic=_FONT_SANS + "-Bold")
        _registered = True
    except Exception:  # noqa: BLE001 - fall back to core fonts if TTFs missing
        _registered = True


def _styles():
    _register_fonts()
    ss = getSampleStyleSheet()
    ss.add(ParagraphStyle("HeroTitle", parent=ss["Title"], fontName=_FONT_SANS + "-Bold",
                          fontSize=24, textColor=_ACCENT, spaceAfter=4, leading=28))
    ss.add(ParagraphStyle("Sub", parent=ss["Normal"], fontName=_FONT_SANS,
                          fontSize=10, textColor=_MUTED, spaceAfter=14))
    ss.add(ParagraphStyle("H2", parent=ss["Heading2"], fontName=_FONT_SANS + "-Bold",
                          fontSize=14, textColor=_ACCENT, spaceBefore=14, spaceAfter=6))
    ss.add(ParagraphStyle("H3", parent=ss["Heading3"], fontName=_FONT_SANS + "-Bold",
                          fontSize=11.5, textColor=colors.HexColor("#334155"),
                          spaceBefore=8, spaceAfter=4))
    ss.add(ParagraphStyle("Body", parent=ss["Normal"], fontName=_FONT_SANS,
                          fontSize=10, leading=15, alignment=TA_LEFT, spaceAfter=6))
    ss.add(ParagraphStyle("Mono", parent=ss["Code"], fontName=_FONT_MONO,
                          fontSize=8.5, leading=11,
                          textColor=colors.HexColor("#0f172a"),
                          backColor=_BG, borderPadding=6))
    ss.add(ParagraphStyle("KPIval", parent=ss["Normal"], fontName=_FONT_SANS + "-Bold",
                          fontSize=18, textColor=_ACCENT, alignment=1, leading=20))
    ss.add(ParagraphStyle("KPIlbl", parent=ss["Normal"], fontName=_FONT_SANS,
                          fontSize=7.5, textColor=_MUTED, alignment=1))
    return ss


class ProgressReport:
    def __init__(self, title: str, subtitle: str = ""):
        self.title = title
        self.subtitle = subtitle
        self.ss = _styles()
        self.flow: List = []
        self.flow.append(Paragraph(title, self.ss["HeroTitle"]))
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        sub = f"slopi-farm · {stamp}" + (f" · {subtitle}" if subtitle else "")
        self.flow.append(Paragraph(sub, self.ss["Sub"]))
        self.flow.append(HRFlowable(width="100%", color=_ACCENT, thickness=1.2,
                                    spaceAfter=10))

    def h2(self, text: str) -> "ProgressReport":
        self.flow.append(Paragraph(text, self.ss["H2"]))
        return self

    def h3(self, text: str) -> "ProgressReport":
        self.flow.append(Paragraph(text, self.ss["H3"]))
        return self

    def para(self, text: str) -> "ProgressReport":
        self.flow.append(Paragraph(text, self.ss["Body"]))
        return self

    def code(self, text: str) -> "ProgressReport":
        safe = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        safe = safe.replace("\n", "<br/>").replace(" ", "&nbsp;")
        self.flow.append(Paragraph(safe, self.ss["Mono"]))
        self.flow.append(Spacer(1, 6))
        return self

    def bullets(self, items: Sequence[str]) -> "ProgressReport":
        lis = [ListItem(Paragraph(i, self.ss["Body"]), leftIndent=6)
               for i in items]
        self.flow.append(ListFlowable(lis, bulletType="bullet",
                                      bulletColor=_ACCENT, start="•"))
        self.flow.append(Spacer(1, 4))
        return self

    def kpis(self, pairs: Sequence[tuple]) -> "ProgressReport":
        """pairs: [(value, label), ...] rendered as a row of KPI cards."""
        cells = []
        for val, lbl in pairs:
            inner = Table([[Paragraph(str(val), self.ss["KPIval"])],
                           [Paragraph(lbl, self.ss["KPIlbl"])]])
            inner.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), _BG),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]))
            cells.append(inner)
        row = Table([cells], colWidths=[(17 * cm) / len(cells)] * len(cells))
        row.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 3),
                                 ("RIGHTPADDING", (0, 0), (-1, -1), 3)]))
        self.flow.append(row)
        self.flow.append(Spacer(1, 10))
        return self

    def table(self, header: Sequence[str], rows: Sequence[Sequence],
              col_widths: Optional[Sequence[float]] = None) -> "ProgressReport":
        data = [[Paragraph(str(h), self.ss["KPIlbl"]) for h in header]]
        for r in rows:
            data.append([Paragraph(str(c), self.ss["Body"]) for c in r])
        t = Table(data, colWidths=col_widths, repeatRows=1)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), _ACCENT),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTSIZE", (0, 0), (-1, 0), 8),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e1")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, _BG]),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]))
        self.flow.append(t)
        self.flow.append(Spacer(1, 10))
        return self

    def image(self, path: Path, width_cm: float = 16) -> "ProgressReport":
        try:
            img = Image(str(path))
            ratio = img.imageHeight / float(img.imageWidth)
            img.drawWidth = width_cm * cm
            img.drawHeight = width_cm * cm * ratio
            self.flow.append(img)
            self.flow.append(Spacer(1, 8))
        except Exception:  # noqa: BLE001
            self.para(f"[chart unavailable: {path.name}]")
        return self

    def hr(self) -> "ProgressReport":
        self.flow.append(HRFlowable(width="100%", color=_MUTED, thickness=0.4,
                                    spaceBefore=6, spaceAfter=6))
        return self

    def save(self, path: Path) -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        doc = SimpleDocTemplate(
            str(path), pagesize=A4,
            leftMargin=2 * cm, rightMargin=2 * cm,
            topMargin=1.6 * cm, bottomMargin=1.6 * cm,
            title=self.title, author="slopi-farm")
        doc.build(self.flow)
        return path
