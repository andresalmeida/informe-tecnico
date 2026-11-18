#!/usr/bin/env python3
"""Compile an editable report specification with convergent navigation and pagination."""
import argparse
import hashlib
import json
import re
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from xml.sax.saxutils import escape

import deps
deps.check(('reportlab',), 'build_report.py')

from lifecycle import validate_lifecycle, status_label, draw_lifecycle_band
from closing import signature_rows, append_closing, keep_sections, FlexKeepTogether, FitFigure, SECTION_MAX_BLANK

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, PageBreak,
    LongTable, TableStyle, KeepTogether, Image, Flowable, IndexingFlowable, CondPageBreak,
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.graphics.shapes import Drawing, Rect, Line, Polygon

REF = re.compile(r"\{\{ref:([a-zA-Z0-9_-]+)\}\}")
# One grid for both header rows: entity and pagination share the same edge.
HEADER_BOUNDS = (0, .42, .71, 1)
NOTICE_LABELS = {"note": "Nota", "caution": "Precaución", "warning": "Advertencia"}
# Rules per document kind. "form": compact layout of label/value grids and short tables that stay whole.
# "choice": the message shown when the source has no marked choice (a fields item with options and a single selected).
# A form-like kind without elections (its weightiest decision is written, not ticked) leaves "choice" out.
KIND_RULES = {
    "ficha-proceso": {"form": True},
    "acta-baja": {"form": True},
    "informe-cierre": {"form": True},
    "informe": {},
    "acta-entrega": {"form": True},
    "acta-reunion": {"form": True},
    "informe-factibilidad": {
        "form": True,
        "choice": "informe-factibilidad requiere una viabilidad marcada: un bloque fields con options y selected"},
    "registro-requerimientos": {
        "form": True,
        "choice": "registro-requerimientos requiere al menos una elección marcada (tipo o prioridad): "
                  "añadir un elemento con options y selected a un bloque fields"},
    "alcance-proyecto": {"form": True},
    "acta-capacitacion": {
        "form": True,
        "choice": "acta-capacitacion requiere la modalidad marcada: un elemento de fields con options "
                  "(presencial o virtual) y selected, de una sola marca"},
    "plan-pruebas": {"form": True},
    "registro-riesgos": {"form": True},
    "propuesta-servicio": {"form": True},
    "decision-arquitectura": {
        "form": True,
        "choice": "decision-arquitectura requiere el estado marcado: añadir un elemento de fields con options "
                  "y selected de una sola marca"},
    "descripcion-arquitectura": {"form": True},
    "especificacion-requisitos": {"form": True},
    "ficha-modelo": {
        "form": True,
        "choice": "ficha-modelo requiere el estado del modelo marcado: un elemento de fields con options "
                  "y selected, de una sola marca"},
    "evaluacion-impacto-datos": {
        "form": True,
        "choice": "evaluacion-impacto-datos requiere la decisión marcada: añadir, en el apartado de conclusión, "
                  "un elemento de fields con options (por ejemplo, puede continuar, continúa con medidas, "
                  "no continúa hasta resolver, consultar a asesoría legal) y selected, de una sola marca"},
    "solicitud-cambio": {
        "form": True,
        "choice": "solicitud-cambio requiere la decisión marcada: un elemento de fields con options "
                  "y selected, de una sola marca"},
    "plan-proyecto": {"form": True},
    "traspaso-operacion": {"form": True},
    "notas-version": {"form": True},
}


# Spanish title capitalization keeps these connectors in lower case, except as the first word of a clause.
TITLE_CONNECTORS = frozenset("""a al ante bajo con contra de del desde e el en entre la las lo los ni o para por
    que se según sin sobre su sus tras u un una unos unas y""".split())
TITLE_EDGES = "()[]{}¿?¡!«»\"'“”‘’.,;:"
INDEX_TITLES = {"contents": "Contenido", "tables": "Índice de tablas", "figures": "Índice de figuras"}


def title_case(text):
    """Capitalize a heading as «Definición de Alcance»: connectors in lower case, first word of the title and of
    each clause in capitals. Words already written in capitals (API, TLS), with an inner capital (iOS) or with
    digits or symbols (v2, node.js) are kept as written. A title written entirely in capitals is normalized."""
    if text.upper() == text and any(ch.isalpha() for ch in text):
        text = text.lower()
    words, clause_start = [], True
    for word in text.split(" "):
        start, end = len(word)-len(word.lstrip(TITLE_EDGES)), len(word.rstrip(TITLE_EDGES))
        core = word[start:end]
        if not core:
            words.append(word)
            continue
        keep = (core.isupper() or any(ch.isupper() for ch in core[1:])
                or any(not ch.isalpha() and ch != "-" for ch in core))
        if keep:
            shown = core
        elif core.lower() in TITLE_CONNECTORS and not clause_start:
            shown = core.lower()
        else:
            shown = core[0].upper()+core[1:]
        words.append(word[:start]+shown+word[end:])
        clause_start = word.endswith((":", ".", "?", "!"))
    return " ".join(words)


def sentence_case(text):
    """Capitalize the first letter and leave every later character as the author wrote it."""
    for index, char in enumerate(text):
        if char.isalpha():
            return text[:index] + char.upper() + text[index + 1:]
    return text


def heading_text(text, mode):
    """Form headings. ``title`` keeps the historical capitalization; ``sentence`` is the default."""
    if mode == "title":
        return title_case(text)
    return sentence_case(text)


def heading_mode_for(spec):
    """Heading mode of any kind: sentence case by default, title case on request."""
    mode = (spec.get("format") or {}).get("heading_case", "sentence")
    require(mode in ("sentence", "title"), 'format.heading_case admite "sentence" o "title".')
    return mode


def format_for(spec):
    """Resolve the format profile; every kind defaults to the hybrid APA body unless ``institucional`` is asked."""
    config = spec.get("format", {})
    require(isinstance(config, dict), "format debe ser un objeto")
    profile = config.get("profile", "institucional-apa")
    require(profile in ("institucional", "institucional-apa"), "Perfil de formato desconocido")
    apa = profile == "institucional-apa"
    values = {"profile": profile, "body_size_pt": 11.0 if apa else 10.5,
              "line_spacing": 1.5 if apa else 14.5/10.5,
              "first_line_indent_mm": 12.7 if apa else 0.0,
              "paragraph_space_after_pt": 0.0 if apa else 8.0,
              "reference_indent_mm": 12.7,
              "table_line_spacing": 1.0 if apa else 12/9}
    require(config.get("heading_case", "sentence") in ("sentence", "title"),
            'format.heading_case admite "sentence" o "title".')
    if apa:
        values["justify"] = True  # the APA profile justifies the body; format.justify can turn it off
    require(not set(config)-set(values)-{"heading_case", "justify"}, "Campo de formato desconocido")
    if "justify" in config:
        require(isinstance(config["justify"], bool), "format.justify debe ser true o false")
        values["justify"] = config["justify"]
    for key in values.keys()-{"profile", "justify"}:
        value = config.get(key, values[key])
        require(isinstance(value, (int, float)) and not isinstance(value, bool), f"Formato no numérico: {key}")
        require(float(value) == float(value) and abs(float(value)) != float("inf"), f"Formato no finito: {key}")
        values[key] = float(value)
    require(8.5 <= values["body_size_pt"] <= 24, "Cuerpo fuera de 8,5..24 pt")
    require(1 <= values["line_spacing"] <= 3, "Interlineado fuera de 1..3")
    require(1 <= values["table_line_spacing"] <= 2, "Interlineado de tabla fuera de 1..2")
    require(0 <= values["first_line_indent_mm"] <= 30 and 0 <= values["reference_indent_mm"] <= 30,
            "Sangría fuera de 0..30 mm")
    require(0 <= values["paragraph_space_after_pt"] <= 30, "Espaciado de párrafo fuera de 0..30 pt")
    return values


SIGNATURE_SPACE = 11*mm
def is_signature_label(value):
    return str(value).strip().casefold() in ("firma", "firmas")


def fit_widths(widths, headers, rows, head_font, cell_font, size, padding=13):
    """Widen the columns whose longest word does not fit, taking the width from the columns with slack."""
    def longest(values, font):
        best = 0
        for text in values:
            for word in re.split(r"\s+", re.sub(r"<[^>]+>", "", str(text))):
                if word and not word.startswith("{{"):
                    best = max(best, pdfmetrics.stringWidth(word, font, size))
        return best + padding
    need = [max(longest([header], head_font), longest([row[i] for row in rows], cell_font))
            for i, header in enumerate(headers)]
    deficit = sum(max(0, n - w) for n, w in zip(need, widths))
    slack = sum(max(0, w - n) for n, w in zip(need, widths))
    if deficit == 0 or deficit > slack:
        return widths
    return [n if w < n else w - (w - n) * deficit / slack for n, w in zip(need, widths)]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def plain(value):
    return str(value) if value is not None else "No informado"


def pathsafe(base, value):
    path = Path(value)
    return path if path.is_absolute() else base / path


def balanced_header_lines(text, font, size, width):
    """Pick the space that leaves two header lines most equal, when both fit the width."""
    best, best_key = None, None
    for index, char in enumerate(text):
        if char != " ":
            continue
        left, right = text[:index], text[index + 1:]
        if not left or not right:
            continue
        left_w = pdfmetrics.stringWidth(left, font, size)
        right_w = pdfmetrics.stringWidth(right, font, size)
        if left_w > width or right_w > width:
            continue
        key = (round(abs(left_w - right_w), 2), abs(index - len(text) / 2))
        if best_key is None or key < best_key:
            best, best_key = (left, right), key
    return best


class Navigation(TableOfContents):
    def __init__(self, kind, style, tight=False):
        super().__init__()
        self.kind = kind
        # A tight index (compact kinds) packs its lines; the report keeps the airier default.
        self.levelStyles = [
            ParagraphStyle(f"index-{kind}-{i}", parent=style, leftIndent=i*11, firstLineIndent=0,
                           spaceBefore=(1.5 if i == 0 else .5) if tight else (5 if i == 0 else 2),
                           spaceAfter=0 if tight else style.spaceAfter, leading=12 if tight else style.leading)
            for i in range(3)
        ]
        self.dotsMinLevel = 0

    def notify(self, kind, stuff):
        if kind == self.kind:
            self.addEntry(*stuff)


class PageTotal(IndexingFlowable):
    def __init__(self):
        super().__init__()
        self.previous = 0
        self.current = 0

    def beforeBuild(self):
        self.previous, self.current = self.current, 0

    def isSatisfied(self):
        return self.previous == self.current

    def wrap(self, available_width, available_height):
        return 0, 0

    def draw(self):
        pass


class RegisteredTable(LongTable):
    """Retain the first-fragment anchor while repeating caption and headings."""
    keep_whole, page_height = False, 0
    blank_limit = None  # share of the page above which a table that fits on one page is split instead of moved
    blank_bonus = 0  # room already taken by the heading that travels with the table, counted as free for that rule

    def split(self, available_width, available_height):
        if self.keep_whole and self.wrap(available_width, available_height)[1] <= self.page_height and (
                self.blank_limit is None
                or available_height + self.blank_bonus <= self.blank_limit * self.page_height):
            return []
        parts = super().split(available_width, available_height)
        if self.keep_whole and self.blank_limit is not None and len(parts) == 2:
            parts = self.without_orphan_row(parts, available_width, available_height)
        if parts and hasattr(self, "entry"):
            parts[0].entry = self.entry
        return parts

    MIN_ROWS = 2  # a split never leaves fewer data rows than this on either page

    def without_orphan_row(self, parts, available_width, available_height):
        """Move the split earlier until both pages keep MIN_ROWS data rows; keep the table whole if that is impossible."""
        first, rest = parts
        repeated = self.repeatRows if isinstance(self.repeatRows, int) else len(self.repeatRows)
        first.wrap(available_width, available_height)
        heights = list(first._rowHeights)
        taken = len(heights) - repeated
        missing = self.MIN_ROWS - (len(rest._cellvalues) - repeated)
        if missing <= 0 and taken >= self.MIN_ROWS:
            return parts
        keep = taken - max(missing, 0)
        if keep < self.MIN_ROWS:
            return []
        retried = super().split(available_width, sum(heights[:repeated + keep]) + .5)
        if len(retried) == 2 and len(retried[1]._cellvalues) - repeated >= self.MIN_ROWS:
            return retried
        return []


class Document(BaseDocTemplate):
    def __init__(self, output, spec, styles, probe, **kwargs):
        self.spec, self.styles, self.probe = spec, styles, probe
        self.entries = []
        self.passes = 0
        super().__init__(str(output), **kwargs)
        self.addPageTemplates(PageTemplate(
            id="institutional", frames=[Frame(
                self.leftMargin, self.bottomMargin, self.width, self.height,
                leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
            )], onPage=self.decorate))

    def beforeDocument(self):
        self.entries = []
        self.passes += 1

    def afterPage(self):
        self.probe.current = self.page

    def afterFlowable(self, flowable):
        entry = getattr(flowable, "entry", None)
        if not entry:
            return
        key, label, kind, level = entry
        self.canv.bookmarkPage(key)
        # Outline levels are flattened so table/figure entries never invalidate
        # a following section hierarchy. The printed TOC preserves levels.
        self.canv.addOutlineEntry(label, key, level=0, closed=False)
        self.notify(kind, (level, escape(label), self.page, key))
        self.entries.append({"id": key, "label": label, "kind": kind,
                             "level": level, "page": self.page})

    def decorate(self, canvas, doc):
        m, brand = self.spec["document"], self.spec["brand"]
        accent = colors.HexColor(brand["accent"])
        ink = colors.HexColor(brand.get("ink", "#17232F"))
        x, w = self.leftMargin, self.width
        top = self.pagesize[1] - 17*mm
        h, meta_h = 20*mm, 10*mm
        columns = [x+w*fraction for fraction in HEADER_BOUNDS]
        title_w = columns[-2]-x
        canvas.saveState()
        canvas.setTitle(m["title"])
        canvas.setAuthor(m.get("author", brand["entity"]))
        canvas.setSubject(f'{m["code"]} | {m["version"]} | {m["status"]}')
        canvas.setStrokeColor(accent)
        canvas.setLineWidth(float(brand.get("border", .55)))
        canvas.rect(x, top-h-meta_h, w, h+meta_h)
        canvas.line(columns[-2], top-h-meta_h, columns[-2], top)
        canvas.line(x, top-h, x+w, top-h)
        canvas.line(columns[1], top-h-meta_h, columns[1], top-h)
        self.box_text(m.get("short_title") or m["title"], x+4*mm, top-h,
                      title_w-8*mm, h, self.styles["header"])
        if brand.get("logo"):
            from reportlab.lib.utils import ImageReader
            logo = ImageReader(str(pathsafe(self.spec["_base"], brand["logo"])))
            iw, ih = logo.getSize()
            maxw, maxh = w-title_w-8*mm, h-5*mm
            factor = min(maxw/iw, maxh/ih)
            canvas.drawImage(logo, x+title_w+(w-title_w-iw*factor)/2,
                             top-h+(h-ih*factor)/2, iw*factor, ih*factor, mask="auto")
        else:
            self.box_text(brand["entity"], x+title_w+3*mm, top-h,
                          w-title_w-6*mm, h, self.styles["entity"])
        values = [f'Actualización: {date.fromisoformat(m["date"]).strftime("%d/%m/%Y")}',
                  f'Versión: {m["version"]}',
                  f'Página {doc.page} de {self.probe.previous or "?"}']
        for i, value in enumerate(values):
            self.box_text(value, columns[i]+2*mm, top-h-meta_h,
                          columns[i+1]-columns[i]-4*mm, meta_h, self.styles["meta"])
        canvas.setStrokeColor(accent)
        canvas.line(x, 18*mm, x+w, 18*mm)
        self.box_text(brand.get("unit") or brand["entity"], x, 8*mm, w*.49, 9*mm,
                      self.styles["footer"])
        footer_text = m["code"]
        if m.get("show_status_in_footer", True) or m.get("lifecycle"):
            footer_text += f' · {status_label(m)}'
        self.box_text(footer_text, x+w*.51, 8*mm,
                      w*.49, 9*mm, self.styles["footer_right"],
                      extend_down=bool(m.get("lifecycle", {}).get("superseded_by_version")))
        if brand.get("frame", False):
            canvas.setStrokeColor(colors.HexColor(brand.get("rule", "#CFD6DD")))
            canvas.rect(12*mm, 6*mm, self.pagesize[0]-24*mm, self.pagesize[1]-12*mm)
        canvas.setFillColor(ink)
        draw_lifecycle_band(canvas, doc, m, self.styles)
        canvas.restoreState()

    def box_text(self, text, x, y, width, height, style, extend_down=False):
        p = Paragraph(escape(plain(text)), style)
        pw, ph = p.wrap(width, height)
        # A name that fits one line keeps the paragraph above. A longer entity name breaks at the
        # space that leaves the two lines most equal. A single long word keeps today's overflow.
        if style.name == "entity" and ph > style.leading + 0.5:
            avail = width - style.leftIndent - style.rightIndent
            pair = balanced_header_lines(str(text), style.fontName, style.fontSize, avail)
            if pair:
                p = Paragraph("<br/>".join(escape(plain(part)) for part in pair), style)
                pw, ph = p.wrap(width, height)
                require(ph <= style.leading * 2 + 0.5, f"Texto demasiado largo en encabezado/pie: {text}")
            elif " " in str(text):
                require(False, f"Texto demasiado largo en encabezado/pie: {text}")
        if extend_down:
            # A successor version may need a second footer line. Keep the first baseline aligned
            # with the unchanged unit footer, and the second above the 5 mm safety margin.
            require(ph <= 2*style.leading, f"Pie de ciclo de vida demasiado largo: acortar código o versión: {text}")
            bottom=y+(height+style.leading)/2-ph
            require(bottom >= 5*mm, "Pie de ciclo de vida fuera de margen: acortar código o versión")
            p.drawOn(self.canv, x, bottom)
        else:
            require(ph <= height-2*mm, f"Texto demasiado largo en encabezado/pie: {text}")
            p.drawOn(self.canv, x, y+(height-ph)/2)


def required_text(value, field):
    require(isinstance(value, str) and bool(value.strip()), f"Texto obligatorio: {field}")


def validate_notice(block, nested=False):
    fields = {"level", "title", "text"} | (set() if nested else {"type"})
    require(isinstance(block, dict) and not set(block)-fields, "Aviso: campos no admitidos")
    require(isinstance(block.get("level"), str) and block["level"] in NOTICE_LABELS,
            "Aviso: level debe ser note, caution o warning")
    required_text(block.get("text"), "notice.text")
    if "title" in block:
        required_text(block["title"], "notice.title")


def validate_procedure(block):
    require(not set(block)-{"type", "id", "title", "role", "prerequisites", "steps"},
            "Procedimiento: campos no admitidos")
    required_text(block.get("id"), "procedure.id")
    required_text(block.get("title"), "procedure.title")
    if "role" in block:
        required_text(block["role"], "procedure.role")
    prerequisites = block.get("prerequisites", [])
    require(isinstance(prerequisites, list), "Procedimiento: prerequisites debe ser lista")
    for item in prerequisites:
        required_text(item, "procedure.prerequisites")
    steps = block.get("steps")
    require(isinstance(steps, list) and bool(steps), "Procedimiento: steps debe ser lista no vacía")
    for step in steps:
        require(isinstance(step, dict) and not set(step)-{"action", "expected", "on_failure", "notice"},
                "Paso: campos no admitidos")
        for field in ("action", "expected"):
            required_text(step.get(field), f"step.{field}")
        if "on_failure" in step:
            required_text(step["on_failure"], "step.on_failure")
        if "notice" in step:
            validate_notice(step["notice"], nested=True)


def validate_fields(block):
    """Label/value grid. An item with options is a choice: exactly one mark, or, with multiple, any number of them."""
    require(not set(block)-{"type", "columns", "items"}, "Campos: campos no admitidos")
    columns = block.get("columns", 1)
    require(isinstance(columns, int) and not isinstance(columns, bool) and columns in (1, 2),
            "Campos: columns debe ser 1 o 2")
    items = block.get("items")
    require(isinstance(items, list) and 1 <= len(items) <= 16, "Campos: items debe ser una lista de 1 a 16")
    for item in items:
        require(isinstance(item, dict) and not set(item)-{"label", "value", "options", "selected", "multiple"},
                "Campo: claves no admitidas")
        required_text(item.get("label"), "fields.label")
        if "multiple" in item:
            require(isinstance(item["multiple"], bool), "Opciones: multiple debe ser true o false")
            require("options" in item, "Opciones: multiple solo se usa con options y selected")
        if "options" in item or "selected" in item:
            require("value" not in item, "Campo: usar value o options, no ambos")
            options = item.get("options")
            require(isinstance(options, list) and 2 <= len(options) <= 6,
                    "Opciones: options debe ser una lista de 2 a 6 textos")
            for option in options:
                required_text(option, "fields.options")
            require(len(set(options)) == len(options), "Opciones: textos repetidos")
            selected = item.get("selected")
            if item.get("multiple"):
                label = item["label"]
                require(isinstance(selected, list),
                        f"Opciones múltiples ({label}): selected debe ser una lista, vacía si no se marca ninguna opción")
                for mark in selected:
                    require(isinstance(mark, str) and mark in options,
                            f"Opciones múltiples ({label}): selected incluye {mark!r}, que no está en options")
                require(len(set(selected)) == len(selected),
                        f"Opciones múltiples ({label}): selected repite una opción; cada una se marca una sola vez")
            else:
                require(isinstance(selected, str) and selected in options,
                        "Opciones: selected debe ser exactamente una de las options"
                        + ("; para marcar varias, añadir multiple: true" if isinstance(selected, list) else ""))
        else:
            required_text(item.get("value"), "fields.value")


def validate_testcase(block):
    """An acceptance case is either unexecuted or has exactly one result."""
    allowed = {"type", "id", "title", "description", "preconditions", "expected", "steps",
               "options", "selected", "executed", "responsible", "observations"}
    require(not set(block)-allowed, "testcase: quitar campos no admitidos: " + ", ".join(sorted(set(block)-allowed)))
    for key in ("id", "title", "description", "preconditions", "expected", "responsible", "observations"):
        required_text(block.get(key), f"testcase.{key}")
    options = block.get("options")
    require(isinstance(options, list) and len(options) == 3,
            "testcase.options: indicar exactamente tres textos de resultado")
    for option in options:
        required_text(option, "testcase.options")
    require(len(set(options)) == 3, "testcase.options: usar textos distintos")
    executed = block.get("executed", False)
    require(isinstance(executed, bool), "testcase.executed: usar true o false")
    selected = block.get("selected")
    if executed:
        require(isinstance(selected, str) and selected in options,
                "testcase.selected: una prueba ejecutada requiere exactamente una de las options")
    else:
        require(selected is None, "testcase.selected: omitir o usar null mientras executed sea false")
    steps = block.get("steps")
    require(isinstance(steps, list) and bool(steps), "testcase.steps: añadir al menos un paso")
    for i, step in enumerate(steps, 1):
        require(isinstance(step, dict) and not set(step)-{"task", "activity", "expected", "actual"},
                f"testcase.steps[{i}]: usar solo task, activity, expected y actual")
        for key in ("task", "activity", "expected", "actual"):
            required_text(step.get(key), f"testcase.steps[{i}].{key}")


def testcase_for(block, doc, styles, p, markup, accent, rule, head_style, apa=False):
    """One row-splittable table: repeat the case sheet, keep the closing result with the last step."""
    label_style = ParagraphStyle("testcase-label", parent=styles["cell"], fontName=styles["h1"].fontName)
    def label(text):
        return Paragraph(markup(text), label_style)
    data = [[label(block["_label"]), "", "", "", ""]]
    for name, key in (("Descripción", "description"), ("Precondiciones", "preconditions"),
                      ("Resultado esperado", "expected")):
        data.append([label(name), "", p(block[key], "cell"), "", ""])
    data.append([Paragraph(markup(v), head_style) for v in
                 ("Paso", "Tarea", "Actividad", "Resultado esperado", "Resultado real")])
    header_rows = len(data)
    for i, step in enumerate(block["steps"], 1):
        data.append([p(str(i), "cell")] + [p(step[key], "cell") for key in
                    ("task", "activity", "expected", "actual")])
    closing = len(data)
    ink = styles["cell"].textColor
    choices = []
    for option in block["options"]:
        choices += [OptionLine(markup(option), option == block.get("selected"), styles["cell"], ink), Spacer(1, 2)]
    data += [[label("Resultado del caso"), "", choices[:-1], "", ""],
             [label("Responsable de aceptación"), "", p(block["responsible"], "cell"), "", ""],
             [label("Observaciones"), "", p(block["observations"], "cell"), "", ""]]
    # RegisteredTable transfers its destination only to the first fragment.
    # The bold 11 pt header «Paso» does not fit the original .07 column.
    weights = (.085, .165, .275, .25, .225) if apa else (.07, .17, .28, .25, .23)
    result = RegisteredTable(data, colWidths=[doc.width*w for w in weights],
                             repeatRows=header_rows, splitByRow=1, splitInRow=0,
                             hAlign="LEFT", spaceBefore=6, spaceAfter=10)
    commands = [("SPAN", (0, 0), (-1, 0)), ("VALIGN", (0, 0), (-1, -1), styles["table_valign"]),
                ("GRID", (0, 0), (-1, -1), .4, rule),
                ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F4F6F8")),
                ("NOSPLIT", (0, closing-1), (-1, -1))]
    if apa:
        commands += [("BOTTOMPADDING", (0, header_rows-2), (-1, header_rows-2), 8),
                     ("LINEABOVE", (0, header_rows-1), (-1, header_rows-1), .6, colors.black),
                     ("LINEBELOW", (0, header_rows-1), (-1, header_rows-1), .6, colors.black)]
    else:
        commands += [("BACKGROUND", (0, header_rows-1), (-1, header_rows-1), accent)]
    for row in list(range(1, header_rows-1)) + list(range(closing, len(data))):
        # Label spans two columns; the value takes the other three.
        commands += [("SPAN", (0, row), (1, row)), ("SPAN", (2, row), (-1, row))]
    result.setStyle(TableStyle(commands))
    result.wrap(doc.width, doc.height)
    heights = result._rowHeights
    header_height = sum(heights[:header_rows])
    for i, height in enumerate(heights[header_rows:closing], 1):
        needed = header_height + height + (sum(heights[closing:]) if i == len(block["steps"]) else 0)
        require(needed <= doc.height,
                f"testcase {block['id']}: la ficha y el paso {i} no caben en una página; "
                "acortar la ficha, dividir la actividad o reducir las observaciones")
    result.keep_whole, result.page_height = True, doc.height
    result.first_fragment_height = header_height + heights[header_rows]
    result.entry = (block["id"], block["_label"], "testcase", 0)
    return result


def append_testcase(story, case, doc):
    # A section's keepWithNext would move an entire oversized table to a fresh page,
    # leaving only the document title behind. Reserve just its first step instead.
    if case._height > doc.height and story and getattr(story[-1], "entry", (None, None, None))[2] == "section":
        heading = story.pop()
        heading.keepWithNext = False
        height = (heading.wrap(doc.width, doc.height)[1] + heading.getSpaceBefore()
                  + heading.getSpaceAfter() + case.getSpaceBefore() + case.first_fragment_height)
        story += [CondPageBreak(min(height, doc.height)), heading]
    story.append(case)


# The level of a risk is the cell the author wrote in the matrix. Nothing here interprets the words.
DEFAULT_RISK_RESPONSES = ("Mitigar", "Transferir", "Aceptar", "Evitar")
DEFAULT_RISK_STATES = ("Abierto", "En mitigación", "Materializado", "Cerrado")
DEFAULT_RISK_OPEN_STATES = ("Abierto", "En mitigación")
RISK_BLOCK_FIELDS = {"type", "id", "scale", "items", "responses", "states", "open_states", "summary_id",
                     "matrix_title", "register_title", "summary_title", "summary_table_title"}
RISK_ITEM_FIELDS = {"id", "cause", "event", "consequence", "probability", "impact", "response", "action", "owner", "state"}


def spanish_join(words, conjunction="y"):
    words = list(words)
    if len(words) <= 1:
        return "".join(words)
    if len(words) == 2:
        return f"{words[0]} {conjunction} {words[1]}"
    return ", ".join(words[:-1]) + f" {conjunction} " + words[-1]


def text_labels(value, field, low, high):
    require(isinstance(value, list), f"Riesgos: {field} debe ser una lista de etiquetas.")
    require(low <= len(value) <= high,
            f"Riesgos: {field} admite de {low} a {high} etiquetas y tiene {len(value)}. Ajustar la lista.")
    for item in value:
        require(isinstance(item, str) and item.strip(),
                f"Riesgos: {field} tiene una etiqueta vacía o que no es texto. Cada etiqueta es un texto.")
    require(len(set(value)) == len(value), f"Riesgos: {field} repite una etiqueta. Cada una debe ser distinta.")
    return value


def levels_in_matrix_order(matrix):
    """Level labels in the order they first appear, row by row. The author chooses that order by how they write the matrix."""
    order = []
    for row in matrix:
        for cell in row:
            if cell not in order:
                order.append(cell)
    return order


# Soft green, yellow and red: black text stays readable on them, and the level word is always printed beside the color.
RISK_RAMP = ((0xC6, 0xE0, 0xB4), (0xFF, 0xE6, 0x99), (0xF4, 0xA6, 0xA6))


def risk_level_colors(matrix):
    """Heat-map color of each level by its rank in the matrix order: the first level green, the last red."""
    order = levels_in_matrix_order(matrix)
    last = max(len(order) - 1, 1)
    result = {}
    for rank, level in enumerate(order):
        position = rank / last * 2
        low = min(int(position), 1)
        fraction = position - low
        rgb = [a + (b - a) * fraction for a, b in zip(RISK_RAMP[low], RISK_RAMP[low + 1])]
        result[level] = colors.Color(*[value / 255 for value in rgb])
    return result


def matrix_level(scale, probability, impact):
    return scale["matrix"][scale["probability"].index(probability)][scale["impact"].index(impact)]


def validate_risks(block):
    """Check a risks block and store the level of each item. A hand-written level is rejected."""
    require(isinstance(block, dict), "Riesgos: el bloque debe ser un objeto.")
    extra = set(block) - RISK_BLOCK_FIELDS
    require(not extra,
            "Riesgos: campos no admitidos (" + ", ".join(sorted(extra)) + "). "
            "El bloque admite id, scale, items y, para personalizar, responses, states, open_states, "
            "summary_id, matrix_title, register_title, summary_title y summary_table_title.")
    require(isinstance(block.get("id"), str) and re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", block.get("id", "")),
            "Riesgos: falta id, o no es válido. Debe empezar por una letra y seguir con letras, dígitos, guion o guion bajo.")
    for key in ("matrix_title", "register_title", "summary_title", "summary_table_title", "summary_id"):
        if key in block:
            require(isinstance(block[key], str) and block[key].strip(),
                    f"Riesgos: {key} debe ser un texto no vacío.")
    if "summary_id" in block:
        require(re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", block["summary_id"]),
                "Riesgos: summary_id no es válido. Debe empezar por una letra y seguir con letras, dígitos, guion o guion bajo.")
        require(block["summary_id"] != block["id"],
                "Riesgos: summary_id repite el id del bloque. Usar otro id para la tabla del resumen.")
    scale = block.get("scale")
    require(isinstance(scale, dict) and not set(scale) - {"probability", "impact", "matrix"},
            "Riesgos: scale admite solo probability, impact y matrix, y los tres son obligatorios.")
    probability = text_labels(scale.get("probability"), "scale.probability", 3, 5)
    impact = text_labels(scale.get("impact"), "scale.impact", 3, 5)
    matrix = scale.get("matrix")
    require(isinstance(matrix, list),
            "Riesgos: matrix debe ser una lista de listas, con una fila por cada etiqueta de probabilidad.")
    require(len(matrix) == len(probability),
            f"Riesgos: matrix tiene {len(matrix)} filas y la escala de probabilidad tiene {len(probability)}. "
            "Debe haber una fila por etiqueta de probabilidad, en el mismo orden.")
    for index, row in enumerate(matrix, 1):
        require(isinstance(row, list),
                f"Riesgos: la fila {index} de matrix debe ser una lista de {len(impact)} etiquetas, "
                f"una por cada impacto ({', '.join(impact)}).")
        require(len(row) == len(impact),
                f"Riesgos: la fila {index} de matrix tiene {len(row)} columnas y la escala de impacto tiene {len(impact)}. "
                "Deben coincidir, en el mismo orden.")
        for cell in row:
            require(isinstance(cell, str) and cell.strip(),
                    f"Riesgos: la fila {index} de matrix tiene una celda vacía o que no es texto. Cada celda es la etiqueta del nivel.")
    responses = text_labels(block.get("responses", list(DEFAULT_RISK_RESPONSES)), "responses", 1, 8)
    states = text_labels(block.get("states", list(DEFAULT_RISK_STATES)), "states", 1, 8)
    if "open_states" in block:
        open_states = text_labels(block["open_states"], "open_states", 1, 8)
    elif "states" in block:
        require(False,
                "Riesgos: al indicar states hay que indicar también open_states, "
                "la lista de estados que el resumen cuenta como abiertos.")
    else:
        open_states = list(DEFAULT_RISK_OPEN_STATES)
    for name in open_states:
        require(name in states,
                f"Riesgos: open_states incluye {name!r}, que no está en states ({', '.join(states)}). "
                "Corregir la lista o añadir ese estado a states.")
    items = block.get("items")
    require(isinstance(items, list) and 1 <= len(items) <= 24,
            "Riesgos: items debe ser una lista de 1 a 24 riesgos.")
    seen = set()
    for item in items:
        require(isinstance(item, dict), "Riesgos: cada elemento de items debe ser un objeto.")
        written = ({"level", "nivel"} & set(item))
        rid = item.get("id") if isinstance(item.get("id"), str) and item["id"].strip() else "sin id"
        require(not written,
                f"Riesgo {rid}: quitar {', '.join(sorted(written))}. "
                "El nivel se calcula con la probabilidad, el impacto y la matriz; no se escribe a mano.")
        unknown = set(item) - RISK_ITEM_FIELDS
        require(not unknown,
                f"Riesgo {rid}: campos no admitidos ({', '.join(sorted(unknown))}). "
                "Cada riesgo lleva id, cause, event, consequence, probability, impact, response, action, owner y state.")
        require(isinstance(item.get("id"), str) and re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", item.get("id", "")),
                f"Riesgo {rid}: el id no es válido. Debe empezar por una letra y seguir con letras, dígitos, guion o guion bajo.")
        rid = item["id"]
        require(rid not in seen, f"Riesgos: el id {rid} está repetido. Cada riesgo lleva un id distinto.")
        seen.add(rid)
        for key, name in (("cause", "la causa"), ("event", "el evento"), ("consequence", "la consecuencia"),
                          ("action", "la acción"), ("owner", "el responsable")):
            require(isinstance(item.get(key), str) and item[key].strip(),
                    f"Riesgo {rid}: falta {name}. Completar {key} con un texto.")
        for key, name, options in (("probability", "la probabilidad", probability),
                                   ("impact", "el impacto", impact),
                                   ("response", "la respuesta", responses),
                                   ("state", "el estado", states)):
            value = item.get(key)
            require(isinstance(value, str) and value in options,
                    f"Riesgo {rid}: {name} {value!r} no está entre las etiquetas admitidas ({', '.join(options)}). "
                    f"Corregir {key} o añadir la etiqueta a la lista correspondiente.")
        item["_level"] = matrix_level(scale, item["probability"], item["impact"])
    block["_responses"] = list(responses)
    block["_states"] = list(states)
    block["_open_states"] = list(open_states)


def bind_risk_block(block, section, counters, table_n, form, mode, separator=". "):
    """Number the register and the summary under the section that holds the block, and number their two tables."""
    parent = section.get("level", 1)
    require(parent in (1, 2),
            "Riesgos: colocar el bloque en una sección de nivel 1 o 2. El registro y el resumen se numeran un nivel por debajo.")
    def heading(key, default):
        counters[parent] += 1
        for index in range(parent + 1, 3):
            counters[index] = 0
        number = ".".join(map(str, counters[:parent + 1]))
        title = block.get(key, default)
        title = heading_text(title, mode)
        return f"{number}. {title}"
    block["_register_id"] = block["id"] + "-registro"
    block["_register_label"] = heading("register_title", "Registro de riesgos")
    block["_summary_heading_id"] = block["id"] + "-resumen-apartado"
    block["_summary_heading"] = heading("summary_title", "Resumen por nivel")
    block["_child_entry_level"] = parent
    table_n += 1
    matrix_title = block.get("matrix_title", "Matriz de niveles")
    block["_matrix_number_label"] = f"Tabla {table_n}"
    block["_matrix_title"] = matrix_title
    block["_matrix_label"] = f"Tabla {table_n}{separator}{matrix_title}"
    table_n += 1
    block["_summary_id"] = block.get("summary_id", block["id"] + "-resumen")
    summary_title = block.get("summary_table_title", "Riesgos abiertos por nivel")
    block["_summary_number_label"] = f"Tabla {table_n}"
    block["_summary_table_title"] = summary_title
    block["_summary_label"] = f"Tabla {table_n}{separator}{summary_title}"
    synthetic = [block["id"], block["_register_id"], block["_summary_heading_id"], block["_summary_id"]]
    require(len(set(synthetic)) == len(synthetic),
            "Riesgos: summary_id coincide con un id que el bloque reserva (" + ", ".join(synthetic) + "). Elegir otro.")
    return table_n


def open_risk_rows(block):
    """Counts of open risks per level, in matrix order, then the total. Closed and other states stay out of the count."""
    grouped = {level: [] for level in levels_in_matrix_order(block["scale"]["matrix"])}
    for item in block["items"]:
        if item["state"] in block["_open_states"]:
            grouped[item["_level"]].append(item["id"])
    rows = [[level, str(len(ids)), ", ".join(f"{{{{ref:{key}}}}}" for key in ids) or "Ninguno"]
            for level, ids in grouped.items()]
    total = sum(len(ids) for ids in grouped.values())
    rows.append(["Total de abiertos", str(total), ""])
    return rows


def risks_for(block, table, p, styles, markup, doc_width, rule, doc_height):
    """Print the scale, one card per risk and the open-risk summary. The level on each card is the one already calculated."""
    scale = block["scale"]
    parts = []
    intro = p(
        "Probabilidad, en el orden en que se escribió: " + spanish_join(scale["probability"]) + ". "
        "Impacto, en el orden en que se escribió: " + spanish_join(scale["impact"]) + ". "
        "La fila de la matriz es la probabilidad y la columna es el impacto. La celda es el nivel que corresponde a ese par, "
        "coloreada del verde al rojo según el orden en que aparecen los niveles, y lista los riesgos abiertos que le tocan.",
        "body")
    intro.keepWithNext = True
    parts.append(intro)
    matrix_caption = {"_label": block["_matrix_label"], "_number_label": block["_matrix_number_label"],
                      "title": block["_matrix_title"]}
    level_color = risk_level_colors(scale["matrix"])
    open_cells = {}
    for item in block["items"]:
        if item["state"] in block["_open_states"]:
            open_cells.setdefault((item["probability"], item["impact"]), []).append(item["id"])

    def heat_cell(probability, impact, level):
        ids = open_cells.get((probability, impact), [])
        return level + ("\n" + ", ".join(f"{{{{ref:{key}}}}}" for key in ids) if ids else "")

    matrix = table(["Probabilidad / Impacto", *scale["impact"]],
                   [[scale["probability"][i], *[heat_cell(scale["probability"][i], scale["impact"][j], level)
                                                for j, level in enumerate(row)]]
                    for i, row in enumerate(scale["matrix"])],
                   [1.7, *([1] * len(scale["impact"]))], block["_matrix_label"], None, matrix_caption)
    # Row 0 is the caption and row 1 the header; the matrix starts at row 2, after the probability column.
    heat = [("BACKGROUND", (j + 1, i + 2), (j + 1, i + 2), level_color[level])
            for i, row in enumerate(scale["matrix"]) for j, level in enumerate(row)]
    heat.append(("INNERGRID", (1, 2), (-1, -1), .8, colors.white))
    matrix.setStyle(TableStyle(heat))
    matrix.entry = (block["id"], block["_matrix_label"], "table", 0)
    parts.append(matrix)
    # Kept off the next heading: gluing this sentence to the first card pushed both to the next page
    # and left the matrix page short. The sentence stays with the scale it explains.
    parts.append(p(
        "Respuestas admitidas: " + spanish_join(block["_responses"]) + ". "
        "Estados admitidos: " + spanish_join(block["_states"]) + ". "
        "El resumen cuenta los estados " + spanish_join(block["_open_states"]) + ".",
        "body"))
    register = p(block["_register_label"], "h2")
    register.entry = (block["_register_id"], block["_register_label"], "section", block["_child_entry_level"])
    parts.append(register)
    label_style = ParagraphStyle("risk-label", parent=styles["cell"], fontName=styles["h1"].fontName)
    strong = ParagraphStyle("risk-strong", parent=styles["cell"], fontName=styles["h1"].fontName)
    shade = colors.HexColor("#F4F6F8")
    head = colors.HexColor("#E8EEF3")

    def text(value, style):
        return Paragraph(markup(value).replace("\n", "<br/>"), style)

    for item in block["items"]:
        data, commands = [], [
            ("VALIGN", (0, 0), (-1, -1), styles["table_valign"]),
            ("GRID", (0, 0), (-1, -1), .4, rule),
            ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("BACKGROUND", (0, 0), (1, 0), head), ("BACKGROUND", (2, 0), (3, 0), level_color[item["_level"]]),
            ("SPAN", (0, 0), (1, 0)), ("SPAN", (2, 0), (3, 0))]
        data.append([text(item["id"], strong), "", text("Nivel: " + item["_level"], strong), ""])
        full = [("Causa", item["cause"]), ("Evento", item["event"]), ("Consecuencia", item["consequence"])]
        for label, value in full:
            row = len(data)
            data.append([text(label, label_style), text(value, styles["cell"]), "", ""])
            commands += [("SPAN", (1, row), (3, row)), ("BACKGROUND", (0, row), (0, row), shade)]
        pairs = [("Probabilidad", item["probability"], "Impacto", item["impact"]),
                 ("Respuesta", item["response"], "Estado", item["state"])]
        for left, left_value, right, right_value in pairs:
            row = len(data)
            data.append([text(left, label_style), text(left_value, styles["cell"]),
                         text(right, label_style), text(right_value, styles["cell"])])
            commands += [("BACKGROUND", (0, row), (0, row), shade), ("BACKGROUND", (2, row), (2, row), shade)]
        for label, value in (("Responsable", item["owner"]), ("Acción", item["action"])):
            row = len(data)
            data.append([text(label, label_style), text(value, styles["cell"]), "", ""])
            commands += [("SPAN", (1, row), (3, row)), ("BACKGROUND", (0, row), (0, row), shade)]
        card = RegisteredTable(data, colWidths=[doc_width * w for w in (.24, .30, .18, .28)],
                               hAlign="LEFT", splitByRow=1, splitInRow=0, spaceBefore=2, spaceAfter=8)
        card.keep_whole, card.page_height = True, doc_height
        card.setStyle(TableStyle(commands))
        card.entry = (item["id"], item["id"], "risk", 0)
        parts.append(card)
    summary_heading = p(block["_summary_heading"], "h2")
    summary_heading.entry = (block["_summary_heading_id"], block["_summary_heading"], "section",
                             block["_child_entry_level"])
    parts.append(summary_heading)
    summary_caption = {"_label": block["_summary_label"], "_number_label": block["_summary_number_label"],
                       "title": block["_summary_table_title"]}
    summary = table(["Nivel", "Abiertos", "Cuáles"], open_risk_rows(block), [1.5, 1.1, 3.4],
                    block["_summary_label"], None, summary_caption)
    summary.setStyle(TableStyle([("BACKGROUND", (0, index + 2), (0, index + 2), level_color[level])
                                 for index, level in enumerate(levels_in_matrix_order(scale["matrix"]))]))
    summary.entry = (block["_summary_id"], block["_summary_label"], "table", 0)
    parts.append(summary)
    return parts


QUOTE_FIELDS = {"type", "id", "title", "currency", "tax_rate", "tax_name", "items", "decimal", "thousands"}
QUOTE_ITEM_FIELDS = {"concept", "quantity", "unit_price"}
QUOTE_CALCULATED = {"subtotal", "tax", "total", "amount", "importe"}


def format_amount(value, decimal, thousands, places=2, trim=False):
    """Fixed separators, half-up, independent of the system locale."""
    number = value if isinstance(value, Decimal) else Decimal(value)
    sign = "-" if number < 0 else ""
    quantum = Decimal("1").scaleb(-places)
    quantized = abs(number).quantize(quantum, rounding=ROUND_HALF_UP)
    whole, frac = f"{quantized:.{places}f}".split(".")
    groups = []
    while whole:
        groups.append(whole[-3:])
        whole = whole[:-3]
    grouped = (thousands or "").join(reversed(groups))
    if trim:
        frac = frac.rstrip("0")
        return sign + grouped + (decimal + frac if frac else "")
    return sign + grouped + decimal + frac


def as_money(value, label):
    require(isinstance(value, (int, float)) and not isinstance(value, bool),
            f"Cotización: {label} no es un número. Quitar el texto y escribir la cifra.")
    number = Decimal(str(value))
    require(number.as_tuple().exponent >= -2,
            f"Cotización: {label} admite hasta 2 decimales. Redondear la cifra antes de escribirla.")
    return number


def validate_quote(block):
    """Check a quote and store line amounts, tax and total. Hand-written totals are rejected."""
    require(isinstance(block, dict), "Cotización: el bloque debe ser un objeto.")
    written = QUOTE_CALCULATED & set(block)
    require(not written,
            "Cotización: quitar " + ", ".join(sorted(written)) + ". "
            "El motor calcula el importe de cada línea, el subtotal, el impuesto y el total.")
    extra = set(block) - QUOTE_FIELDS
    require(not extra, "Cotización: campos no admitidos (" + ", ".join(sorted(extra)) + ").")
    require(isinstance(block.get("id"), str) and re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", block.get("id", "")),
            "Cotización: falta id, o no es válido. Debe empezar por una letra y seguir con letras, dígitos, guion o guion bajo.")
    require(isinstance(block.get("title"), str) and block["title"].strip(),
            "Cotización: falta title. Es el título de la tabla.")
    currency = block.get("currency")
    require(isinstance(currency, str) and currency.strip(),
            "Cotización: la moneda está vacía. Indicar el código o el nombre que usa la entidad, por ejemplo USD.")
    block["_currency"] = currency.strip()
    decimal = block.get("decimal", ",")
    thousands = block.get("thousands", ".")
    require(decimal in (",", "."), "Cotización: decimal debe ser ',' o '.'.")
    require(thousands in ("", ".", ",", " "),
            "Cotización: thousands debe ser '.', ',', un espacio o una cadena vacía.")
    require(not thousands or decimal != thousands,
            "Cotización: el separador decimal y el de miles son el mismo carácter. Elegir dos distintos.")
    block["_decimal"], block["_thousands"] = decimal, thousands
    require("tax_rate" in block,
            'Cotización: falta tax_rate. Indicar una fracción entre 0 y 1 o null si el impuesto está por confirmar; '
            'por ejemplo "tax_rate": 0.15 o "tax_rate": null.')
    rate = None
    if block["tax_rate"] is not None:
        require(isinstance(block["tax_rate"], (int, float)) and not isinstance(block["tax_rate"], bool),
                "Cotización: tax_rate no es un número ni null. Indicar una fracción entre 0 y 1, por ejemplo 0,15 para el 15 %, o null si está por confirmar.")
        rate = Decimal(str(block["tax_rate"]))
        require(Decimal("0") <= rate <= Decimal("1"),
                f"Cotización: tax_rate {block['tax_rate']!r} está fuera de 0 a 1. "
                "0,15 equivale al 15 %. La tasa es un dato de la entidad; el motor no la completa.")
        require(rate.as_tuple().exponent >= -4,
                "Cotización: tax_rate admite hasta 4 decimales. Redondear la fracción.")
    block["_rate"] = rate
    tax_name = block.get("tax_name", "Impuesto")
    require(isinstance(tax_name, str) and tax_name.strip(),
            "Cotización: tax_name debe ser un texto no vacío. Es el nombre con el que la entidad llama a la tasa.")
    block["_tax_name"] = tax_name.strip()
    items = block.get("items")
    require(isinstance(items, list) and 1 <= len(items) <= 24,
            "Cotización: items debe ser una lista de 1 a 24 conceptos.")
    subtotal = Decimal("0.00")
    for index, item in enumerate(items, 1):
        require(isinstance(item, dict), f"Cotización: el concepto {index} debe ser un objeto.")
        item_written = QUOTE_CALCULATED & set(item)
        require(not item_written,
                f"Cotización, concepto {index}: quitar {', '.join(sorted(item_written))}. "
                "El importe de la línea lo calcula el motor.")
        unknown = set(item) - QUOTE_ITEM_FIELDS
        require(not unknown,
                f"Cotización, concepto {index}: campos no admitidos ({', '.join(sorted(unknown))}). "
                "Cada concepto lleva concept, quantity y unit_price.")
        require(isinstance(item.get("concept"), str) and item["concept"].strip(),
                f"Cotización, concepto {index}: falta el concepto. Completar concept con un texto.")
        quantity = as_money(item.get("quantity"), f"la cantidad del concepto {index}")
        require(quantity > 0,
                f"Cotización, concepto {index}: la cantidad debe ser un número mayor que cero.")
        price = as_money(item.get("unit_price"), f"el precio unitario del concepto {index}")
        require(price >= 0,
                f"Cotización, concepto {index}: el precio unitario no puede ser negativo. "
                "Un concepto sin cargo lleva 0.")
        item["_quantity"] = quantity
        item["_unit_price"] = price
        item["_amount"] = (quantity * price).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        subtotal += item["_amount"]
    block["_subtotal"] = subtotal
    block["_tax"] = None if rate is None else (subtotal * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    block["_total"] = subtotal if rate is None else subtotal + block["_tax"]


def quote_for(block, table):
    decimal, thousands = block["_decimal"], block["_thousands"]
    money = lambda value: format_amount(value, decimal, thousands)
    rows = [[item["concept"],
             format_amount(item["_quantity"], decimal, thousands, trim=True),
             money(item["_unit_price"]), money(item["_amount"])] for item in block["items"]]
    rows.append(["", "", "Subtotal", money(block["_subtotal"])])
    if block["_rate"] is None:
        rows.append(["", "", block["_tax_name"], "Por confirmar"])
        rows.append(["", "", f'Total antes de impuestos ({block["_currency"]})', money(block["_total"])])
    else:
        percent = format_amount(block["_rate"] * 100, decimal, thousands, trim=True)
        rows.append(["", "", f'{block["_tax_name"]}, {percent} %', money(block["_tax"])])
        rows.append(["", "", f'Total ({block["_currency"]})', money(block["_total"])])
    caption = {"_label": block["_label"], "_number_label": block["_number_label"], "title": block["title"]}
    quoted = table(["Concepto", "Cantidad", f'Precio ({block["_currency"]})', f'Importe ({block["_currency"]})'],
                   rows, [3.4, 1, 1.6, 1.5], block["_label"], None, caption)
    quoted.entry = (block["id"], block["_label"], "table", 0)
    return quoted


DEFAULT_REQUIREMENT_PRIORITIES = ("Alta", "Media", "Baja")
DEFAULT_REQUIREMENT_METHODS = ("Prueba", "Inspección", "Análisis", "Demostración", "Por definir")
DEFAULT_REQUIREMENT_STATES = ("Propuesto", "Aprobado", "Rechazado")
DEFAULT_REQUIREMENT_VERIFIED = ("Aprobado",)
REQUIREMENT_PLACEHOLDER = "Por definir"
REQUIREMENT_FIELDS = {"type", "id", "title", "items", "priorities", "methods", "states", "verified_states", "matrix"}
REQUIREMENT_ITEM_FIELDS = {"id", "statement", "priority", "source", "method", "tests", "deliverable", "state"}
REQUIREMENT_HANDWRITTEN = {"rows", "headers", "matrix_rows", "trazabilidad"}


def requirement_labels(value, field, low, high):
    require(isinstance(value, list), f"Requisitos: {field} debe ser una lista de etiquetas.")
    require(low <= len(value) <= high,
            f"Requisitos: {field} admite de {low} a {high} etiquetas y tiene {len(value)}. Ajustar la lista.")
    for item in value:
        require(isinstance(item, str) and item.strip(),
                f"Requisitos: {field} tiene una etiqueta vacía o que no es texto. Cada etiqueta es un texto.")
    require(len(set(value)) == len(value), f"Requisitos: {field} repite una etiqueta. Cada una debe ser distinta.")
    return value


def validate_requirements(block, seen_ids, items_so_far, matrix_seen):
    """Check a requirements block. A source block stores items. A matrix block prints those same items and rejects hand-written rows."""
    require(isinstance(block, dict), "Requisitos: el bloque debe ser un objeto.")
    written = REQUIREMENT_HANDWRITTEN & set(block)
    require(not written,
            "Requisitos: quitar " + ", ".join(sorted(written)) + ". "
            "La matriz de trazabilidad la calcula el motor a partir de los requisitos; no se escribe a mano.")
    extra = set(block) - REQUIREMENT_FIELDS
    require(not extra,
            "Requisitos: campos no admitidos (" + ", ".join(sorted(extra)) + "). "
            "El bloque admite id, title, items y matrix, y para personalizar priorities, methods, states y verified_states.")
    require(isinstance(block.get("id"), str) and re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", block.get("id", "")),
            "Requisitos: falta id, o no es válido. Debe empezar por una letra y seguir con letras, dígitos, guion o guion bajo.")
    require(block["id"] not in seen_ids,
            f"Requisitos: el id {block['id']} está repetido. Cada bloque y cada requisito llevan un id distinto.")
    seen_ids.add(block["id"])
    is_matrix = block.get("matrix", False)
    require(isinstance(is_matrix, bool), "Requisitos: matrix debe ser true o false.")
    if is_matrix:
        require("items" not in block,
                "Requisitos: el bloque de la matriz no lleva items. Quitar items. "
                "Los requisitos van en los bloques anteriores y la matriz sale de ellos.")
        require(isinstance(block.get("title"), str) and block["title"].strip(),
                "Requisitos: la matriz necesita title. Es el título de la tabla.")
        require(not matrix_seen,
                "Requisitos: ya hay una matriz. Dejar un solo bloque con matrix true.")
        require(items_so_far,
                "Requisitos: la matriz está antes de los requisitos, o no hay ninguno. "
                "Colocar el bloque con matrix después de los bloques que traen items.")
        block["_rows"] = [[
            "{{ref:%s}}" % item["id"], item["source"], item["deliverable"],
            ", ".join(item["tests"]), item["method"], item["state"],
        ] for item in items_so_far]
        return True
    require("title" not in block or (isinstance(block.get("title"), str) and block["title"].strip()),
            "Requisitos: title debe ser un texto no vacío.")
    priorities = requirement_labels(block.get("priorities", list(DEFAULT_REQUIREMENT_PRIORITIES)), "priorities", 1, 8)
    methods = requirement_labels(block.get("methods", list(DEFAULT_REQUIREMENT_METHODS)), "methods", 1, 8)
    states = requirement_labels(block.get("states", list(DEFAULT_REQUIREMENT_STATES)), "states", 1, 8)
    if "verified_states" in block:
        verified = requirement_labels(block["verified_states"], "verified_states", 1, 8)
    elif "states" in block:
        require(False,
                "Requisitos: al indicar states hay que indicar también verified_states, "
                "la lista de estados que exigen método y caso distintos de Por definir.")
    else:
        verified = list(DEFAULT_REQUIREMENT_VERIFIED)
    for name in verified:
        require(name in states,
                f"Requisitos: verified_states incluye {name!r}, que no está en states ({', '.join(states)}). "
                "Corregir la lista o añadir ese estado a states.")
    if matrix_seen:
        require(False,
                "Requisitos: hay un bloque con items después de la matriz. "
                "Mover esos requisitos antes del bloque con matrix.")
    raw_items = block.get("items")
    require(isinstance(raw_items, list) and 1 <= len(raw_items) <= 24,
            "Requisitos: items debe ser una lista de 1 a 24 requisitos.")
    for item in raw_items:
        require(isinstance(item, dict), "Requisitos: cada elemento de items debe ser un objeto.")
        rid = item.get("id") if isinstance(item.get("id"), str) and item["id"].strip() else "sin id"
        unknown = set(item) - REQUIREMENT_ITEM_FIELDS
        require(not unknown,
                f"Requisito {rid}: campos no admitidos ({', '.join(sorted(unknown))}). "
                "Cada requisito lleva id, statement, priority, source, method, tests, deliverable y state.")
        require(isinstance(item.get("id"), str) and re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", item.get("id", "")),
                f"Requisito {rid}: el id no es válido. Debe empezar por una letra y seguir con letras, dígitos, guion o guion bajo.")
        rid = item["id"]
        require(rid not in seen_ids,
                f"Requisitos: el id {rid} está repetido. Cada requisito lleva un id distinto.")
        seen_ids.add(rid)
        statement = item.get("statement")
        require(isinstance(statement, str) and statement.strip(),
                f"Requisito {rid}: falta el enunciado. Completar statement con un texto.")
        statement = statement.strip()
        require(statement.startswith("El sistema debe"),
                f"Requisito {rid}: el enunciado debe empezar por 'El sistema debe'. Es una sola exigencia.")
        require(statement.endswith(".") and statement.count(".") == 1,
                f"Requisito {rid}: el enunciado es una sola oración y termina en un punto.")
        for key, name, options in (("priority", "la prioridad", priorities),
                                   ("method", "el método", methods),
                                   ("state", "el estado", states)):
            value = item.get(key)
            require(isinstance(value, str) and value in options,
                    f"Requisito {rid}: {name} {value!r} no está entre las etiquetas admitidas ({', '.join(options)}). "
                    f"Corregir {key} o añadir la etiqueta a la lista correspondiente.")
        require(isinstance(item.get("source"), str) and item["source"].strip(),
                f"Requisito {rid}: falta la fuente. Completar source con el código o el apartado de donde sale.")
        require(isinstance(item.get("deliverable"), str) and item["deliverable"].strip(),
                f"Requisito {rid}: falta el entregable. Completar deliverable con su código, o con Por definir si aún no existe.")
        tests = item.get("tests")
        require(isinstance(tests, list) and tests and not isinstance(tests, str),
                f"Requisito {rid}: falta tests. Es una lista de casos, o exactamente ['Por definir'].")
        if tests == [REQUIREMENT_PLACEHOLDER]:
            placeholder = True
        else:
            placeholder = False
            for case in tests:
                require(isinstance(case, str) and re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", case),
                        f"Requisito {rid}: el caso {case!r} no es un identificador. "
                        "Cada caso es un id, o tests es exactamente ['Por definir'].")
        if item["state"] in verified:
            require(item["method"] != REQUIREMENT_PLACEHOLDER,
                    f"Requisito {rid}: está en {item['state']} y el método es 'Por definir'. "
                    "Indicar un método de verificación, o cambiar el estado.")
            require(not placeholder,
                    f"Requisito {rid}: está en {item['state']} y los casos son 'Por definir'. "
                    "Indicar los identificadores de los casos, o cambiar el estado.")
            require(item["deliverable"].strip() != REQUIREMENT_PLACEHOLDER,
                    f"Requisito {rid}: está en {item['state']} y el entregable es 'Por definir'. "
                    "Indicar el entregable, o cambiar el estado.")
        items_so_far.append(item)
    block["_priorities"] = list(priorities)
    block["_methods"] = list(methods)
    block["_states"] = list(states)
    block["_verified"] = list(verified)
    return False


def requirements_for(block, table, p, styles, markup, doc_width, rule, doc_height):
    """Print requirement cards, or the traceability matrix calculated from those cards."""
    if block.get("matrix"):
        caption = {"_label": block["_label"], "_number_label": block["_number_label"], "title": block["title"]}
        has_hole = any(REQUIREMENT_PLACEHOLDER in str(cell) for row in block["_rows"] for cell in row)
        intro = p(
            "Cada fila sale del requisito del mismo identificador."
            + (" Una celda en Por definir es un hueco: ese requisito no está terminado." if has_hole else ""),
            "body")
        intro.keepWithNext = True
        grid = table(
            ["Requisito", "Fuente", "Entregable", "Casos", "Método", "Estado"],
            block["_rows"], [1.15, 1.7, 0.85, 0.9, 1.15, 1.05], block["_label"], None, caption)
        grid.entry = (block["id"], block["_label"], "table", 0)
        return [intro, grid]
    parts = [p(
        "Prioridades admitidas: " + spanish_join(block["_priorities"]) + ". "
        "Métodos de verificación: " + spanish_join(block["_methods"]) + ". "
        "Estados: " + spanish_join(block["_states"]) + ". "
        "En " + spanish_join(block["_verified"]) + " el método, el caso y el entregable no pueden ser Por definir.",
        "body")]
    label_style = ParagraphStyle("requirement-label", parent=styles["cell"], fontName=styles["h1"].fontName)
    strong = ParagraphStyle("requirement-strong", parent=styles["cell"], fontName=styles["h1"].fontName)
    shade = colors.HexColor("#F4F6F8")
    head = colors.HexColor("#E8EEF3")

    def text(value, style):
        return Paragraph(markup(value).replace("\n", "<br/>"), style)

    for item in block["items"]:
        data, commands = [], [
            ("VALIGN", (0, 0), (-1, -1), styles["table_valign"]),
            ("GRID", (0, 0), (-1, -1), .4, rule),
            ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("BACKGROUND", (0, 0), (-1, 0), head),
            ("SPAN", (0, 0), (1, 0)), ("SPAN", (2, 0), (3, 0))]
        data.append([text(item["id"], strong), "", text("Prioridad: " + item["priority"], strong), ""])
        for label, value in (("Enunciado", item["statement"]), ("Fuente", item["source"])):
            row = len(data)
            data.append([text(label, label_style), text(value, styles["cell"]), "", ""])
            commands += [("SPAN", (1, row), (3, row)), ("BACKGROUND", (0, row), (0, row), shade)]
        pairs = [("Método", item["method"], "Estado", item["state"]),
                 ("Entregable", item["deliverable"], "Casos", ", ".join(item["tests"]))]
        for left, left_value, right, right_value in pairs:
            row = len(data)
            data.append([text(left, label_style), text(left_value, styles["cell"]),
                         text(right, label_style), text(right_value, styles["cell"])])
            commands += [("BACKGROUND", (0, row), (0, row), shade), ("BACKGROUND", (2, row), (2, row), shade)]
        card = RegisteredTable(data, colWidths=[doc_width * w for w in (.24, .30, .18, .28)],
                               hAlign="LEFT", splitByRow=1, splitInRow=0, spaceBefore=2, spaceAfter=8)
        card.keep_whole, card.page_height = True, doc_height
        card.setStyle(TableStyle(commands))
        card.entry = (item["id"], item["id"], "requirement", 0)
        parts.append(card)
    return parts


IMPACT_FIELDS = {"type", "id", "title", "rows"}
IMPACT_ROW_FIELDS = {"aspect", "before", "after", "unit"}
IMPACT_CALCULATED = {"difference", "diferencia", "delta"}
IMPACT_PLACEHOLDER = "Por estimar"


def impact_value(value, where):
    """A number, or the exact gap token. The difference is not accepted as input."""
    if value == IMPACT_PLACEHOLDER:
        return None
    require(isinstance(value, (int, float)) and not isinstance(value, bool),
            f"Impacto, {where}: antes y después son un número o exactamente 'Por estimar'.")
    number = Decimal(str(value))
    require(number.as_tuple().exponent >= -2,
            f"Impacto, {where}: el número admite hasta 2 decimales.")
    return number


def impact_text(value):
    if value is None:
        return IMPACT_PLACEHOLDER
    return format_amount(value, ",", ".", places=2, trim=True)


def validate_impact(block):
    """Check a before/after table and store the difference of each row. Hand-written differences are rejected."""
    require(isinstance(block, dict), "Impacto: el bloque debe ser un objeto.")
    written = IMPACT_CALCULATED & set(block)
    require(not written,
            "Impacto: quitar " + ", ".join(sorted(written)) + ". "
            "La diferencia de cada fila la calcula el motor.")
    extra = set(block) - IMPACT_FIELDS
    require(not extra, "Impacto: campos no admitidos (" + ", ".join(sorted(extra)) + ").")
    require(isinstance(block.get("id"), str) and re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", block.get("id", "")),
            "Impacto: falta id, o no es válido. Debe empezar por una letra y seguir con letras, dígitos, guion o guion bajo.")
    require(isinstance(block.get("title"), str) and block["title"].strip(),
            "Impacto: falta title. Es el título de la tabla.")
    rows = block.get("rows")
    require(isinstance(rows, list) and 1 <= len(rows) <= 12,
            "Impacto: rows debe ser una lista de 1 a 12 filas.")
    for index, row in enumerate(rows, 1):
        require(isinstance(row, dict), f"Impacto, fila {index}: debe ser un objeto.")
        row_written = IMPACT_CALCULATED & set(row)
        require(not row_written,
                f"Impacto, fila {index}: quitar {', '.join(sorted(row_written))}. "
                "La diferencia la calcula el motor.")
        unknown = set(row) - IMPACT_ROW_FIELDS
        require(not unknown,
                f"Impacto, fila {index}: campos no admitidos ({', '.join(sorted(unknown))}). "
                "Cada fila lleva aspect, before, after y unit.")
        require(isinstance(row.get("aspect"), str) and row["aspect"].strip(),
                f"Impacto, fila {index}: falta el aspecto. Completar aspect con un texto.")
        require(isinstance(row.get("unit"), str) and row["unit"].strip(),
                f"Impacto, fila {index}: falta la unidad. Completar unit, por ejemplo días-persona.")
        before = impact_value(row.get("before"), f"el antes de la fila {index}")
        after = impact_value(row.get("after"), f"el después de la fila {index}")
        row["_before_text"] = impact_text(before)
        row["_after_text"] = impact_text(after)
        if before is None or after is None:
            row["_difference_text"] = IMPACT_PLACEHOLDER
        else:
            row["_difference_text"] = impact_text(after - before)


def impact_for(block, table):
    rows = [[row["aspect"], row["_before_text"], row["_after_text"], row["_difference_text"], row["unit"]]
            for row in block["rows"]]
    caption = {"_label": block["_label"], "_number_label": block["_number_label"], "title": block["title"]}
    quoted = table(["Aspecto", "Antes", "Después", "Diferencia", "Unidad"],
                   rows, [2.2, 1.15, 1.25, 1.25, 1.45], block["_label"], None, caption)
    quoted.entry = (block["id"], block["_label"], "table", 0)
    return quoted


WBS_FIELDS = {"type", "id", "title", "unit", "nodes"}
WBS_NODE_FIELDS = {"id", "title", "effort", "children"}
WBS_CALCULATED = {"total", "subtotal"}
WBS_PLACEHOLDER = "Por estimar"
WBS_MAX_DEPTH = 4
WBS_MAX_NODES = 40


def wbs_amount(value, where):
    require(isinstance(value, (int, float)) and not isinstance(value, bool),
            f"EDT, {where}: el esfuerzo es un número o exactamente 'Por estimar'.")
    number = Decimal(str(value))
    require(number.as_tuple().exponent >= -2,
            f"EDT, {where}: el esfuerzo admite hasta 2 decimales.")
    require(number >= 0,
            f"EDT, {where}: el esfuerzo no puede ser negativo. Si todavía no se estima, escribir 'Por estimar'.")
    return number


def wbs_text(value):
    return format_amount(value, ",", ".", places=2, trim=True)


def validate_wbs(block):
    """Check a work-breakdown tree. Effort lives on leaves. Branch totals and the grand total are calculated."""
    require(isinstance(block, dict), "EDT: el bloque debe ser un objeto.")
    written = WBS_CALCULATED & set(block)
    require(not written,
            "EDT: quitar " + ", ".join(sorted(written)) + ". "
            "El motor calcula el total de cada rama y el total general.")
    extra = set(block) - WBS_FIELDS
    require(not extra, "EDT: campos no admitidos (" + ", ".join(sorted(extra)) + ").")
    require(isinstance(block.get("id"), str) and re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", block.get("id", "")),
            "EDT: falta id, o no es válido. Debe empezar por una letra y seguir con letras, dígitos, guion o guion bajo.")
    require(isinstance(block.get("title"), str) and block["title"].strip(),
            "EDT: falta title. Es el título de la tabla.")
    unit = block.get("unit", "días-persona")
    require(isinstance(unit, str) and unit.strip(),
            "EDT: unit debe ser un texto no vacío. Por omisión es días-persona.")
    block["_unit"] = unit.strip()
    nodes = block.get("nodes")
    require(isinstance(nodes, list) and nodes,
            "EDT: nodes debe ser una lista con al menos un paquete.")
    seen, count = set(), 0

    def walk(items, depth):
        nonlocal count
        require(depth < WBS_MAX_DEPTH,
                f"EDT: un paquete queda en el nivel {depth + 1}. La EDT admite {WBS_MAX_DEPTH} niveles.")
        subtotal = Decimal("0")
        for node in items:
            require(isinstance(node, dict), "EDT: cada paquete debe ser un objeto.")
            node_written = WBS_CALCULATED & set(node)
            require(not node_written,
                    "EDT: quitar " + ", ".join(sorted(node_written)) + " de " + str(node.get("id", "un paquete")) + ". "
                    "El total de la rama lo calcula el motor.")
            unknown = set(node) - WBS_NODE_FIELDS
            require(not unknown,
                    "EDT: campos no admitidos (" + ", ".join(sorted(unknown)) + ") en "
                    + str(node.get("id", "un paquete")) + ". Un paquete lleva id, title y effort, o id, title y children.")
            node_id = node.get("id")
            require(isinstance(node_id, str) and re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", node_id),
                    f"EDT: el identificador {node_id!r} no es válido. "
                    "Debe empezar por una letra y seguir con letras, dígitos, guion o guion bajo.")
            require(node_id not in seen, f"EDT: el identificador {node_id} está repetido.")
            seen.add(node_id)
            require(isinstance(node.get("title"), str) and node["title"].strip(),
                    f"EDT: falta el título del paquete {node_id}.")
            count += 1
            require(count <= WBS_MAX_NODES,
                    f"EDT: admite hasta {WBS_MAX_NODES} paquetes y tiene {count}.")
            has_children, has_effort = "children" in node, "effort" in node
            require(has_children ^ has_effort,
                    f"EDT: el paquete {node_id} necesita effort o children, no las dos cosas y no ninguna. "
                    "El esfuerzo se escribe solo en las hojas.")
            node["_depth"] = depth
            if has_children:
                children = node["children"]
                require(isinstance(children, list) and children,
                        f"EDT: la rama {node_id} necesita al menos un paquete hijo.")
                node["_leaf"] = False
                node["_sum"] = walk(children, depth + 1)
                node["_effort_text"] = wbs_text(node["_sum"])
            else:
                node["_leaf"] = True
                if node["effort"] == WBS_PLACEHOLDER:
                    node["_sum"] = Decimal("0")
                    node["_effort_text"] = WBS_PLACEHOLDER
                else:
                    number = wbs_amount(node["effort"], f"el paquete {node_id}")
                    node["_sum"] = number
                    node["_effort_text"] = wbs_text(number)
            subtotal += node["_sum"]
        return subtotal

    block["_total"] = walk(nodes, 0)
    block["_total_text"] = wbs_text(block["_total"])
    flat = []

    def flatten(items):
        for node in items:
            flat.append(node)
            if not node["_leaf"]:
                flatten(node["children"])

    flatten(nodes)
    block["_flat"] = flat


def wbs_for(block, styles, markup, doc_width, accent, rule, head_style, doc_height, apa=False, caption=None):
    from reportlab.platypus import Paragraph, TableStyle
    unit = block["_unit"]
    intro = Paragraph(
        markup(f"Unidad: {unit}. El esfuerzo va en las hojas. "
               "«Por estimar» queda visible y fuera de la suma."),
        styles["body"])
    intro.keepWithNext = True
    headers = ["Identificador", "Paquete de trabajo", f"Esfuerzo ({unit})"]
    data = [[Paragraph(markup(header), head_style) for header in headers]]
    made = 0

    def indented(text, depth, bold):
        nonlocal made
        made += 1
        style = ParagraphStyle(
            f"wbs-cell-{made}", parent=styles["cell"], leftIndent=depth * 9,
            fontName=styles["h1"].fontName if bold else styles["cell"].fontName)
        return Paragraph(markup(text), style)

    for node in block["_flat"]:
        data.append([
            Paragraph(markup(node["id"]), styles["cell"]),
            indented(node["title"], node["_depth"], not node["_leaf"]),
            Paragraph(markup(node["_effort_text"]), styles["cell"]),
        ])
    data.append([
        Paragraph("", styles["cell"]),
        indented("Total", 0, True),
        Paragraph(markup(block["_total_text"]), ParagraphStyle(
            "wbs-total", parent=styles["cell"], fontName=styles["h1"].fontName)),
    ])
    weights = [1.35, 4.15, 1.7]
    widths = [doc_width * weight / sum(weights) for weight in weights]
    result = RegisteredTable(data, colWidths=widths, repeatRows=1, hAlign="LEFT",
                             splitByRow=1, splitInRow=0, spaceBefore=2, spaceAfter=8)
    result.keep_whole, result.page_height = True, doc_height
    commands = [
        ("VALIGN", (0, 0), (-1, -1), styles["table_valign"]),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]
    if apa:
        # Sparse horizontal rules, as in every APA table: above and below the header, above and below the total.
        commands += [("LINEABOVE", (0, 0), (-1, 0), .6, colors.black), ("LINEBELOW", (0, 0), (-1, 0), .6, colors.black),
                     ("LINEABOVE", (0, -1), (-1, -1), .4, colors.black), ("LINEBELOW", (0, -1), (-1, -1), .6, colors.black)]
    else:
        commands += [("BACKGROUND", (0, 0), (-1, 0), accent),
                     ("LINEBELOW", (0, 0), (-1, -1), .3, rule),
                     ("ROWBACKGROUNDS", (0, 1), (-1, -2), [colors.white, colors.HexColor("#F4F6F8")]),
                     ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#E6EEF3"))]
    result.setStyle(TableStyle(commands))
    caption = caption or Paragraph(markup(block["_label"]), styles["caption"])
    caption.keepWithNext = True
    result.entry = (block["id"], block["_label"], "table", 0)
    return [intro, caption, result]


def document_has(spec, kind_name):
    blocks = [block for section in spec["sections"] for block in section.get("blocks", [])]
    if any(block.get("type") == kind_name for block in blocks):
        return True
    # risks prints the matrix and the summary; quote prints the priced table;
    # requirements prints the traceability matrix when matrix is true;
    # impact prints the before/after table.
    return kind_name == "table" and any(
        block.get("type") in ("risks", "quote", "impact", "wbs") or (block.get("type") == "requirements" and block.get("matrix"))
        for block in blocks)


class OptionLine(Flowable):
    """One state of a choice: a vector box, crossed when selected, beside its label.

    Drawn as vector so it never depends on a font having ballot-box glyphs.
    """
    BOX, GAP = 9.0, 6.0

    def __init__(self, markup, selected, style, ink):
        super().__init__()
        self.paragraph = Paragraph(f"<b>{markup}</b>" if selected else markup, style)
        self.selected, self.ink, self.style = selected, ink, style

    def wrap(self, width, height):
        _, self.text_h = self.paragraph.wrap(width-self.BOX-self.GAP, height)
        self.width, self.height = width, max(self.text_h, self.BOX)
        return self.width, self.height

    def draw(self):
        c = self.canv
        # The first baseline sits one font size below the top; centre the box on the lettering.
        y = self.height-self.style.fontSize*.70-self.BOX/2
        c.saveState()
        c.setStrokeColor(self.ink)
        c.setLineWidth(.8)
        c.rect(0, y, self.BOX, self.BOX, stroke=1, fill=0)
        if self.selected:
            c.setLineWidth(1.2)
            inset = 1.9
            c.line(inset, y+inset, self.BOX-inset, y+self.BOX-inset)
            c.line(inset, y+self.BOX-inset, self.BOX-inset, y+inset)
        c.restoreState()
        self.paragraph.drawOn(c, self.BOX+self.GAP, self.height-self.text_h)


def registry(spec):
    # A form prints «1. Título»; heading_case chooses the capitals. Other kinds keep «1 Título» as written.
    form = KIND_RULES[spec["document"].get("kind", "informe")].get("form", False)
    mode = heading_mode_for(spec)
    # In the APA profile the printed caption is «Tabla 1» above the title, so the label has no period.
    separator = " " if format_for(spec)["profile"] == "institucional-apa" else ". "
    labels, counters, table_n, figure_n, procedure_n = {}, [0, 0, 0], 0, 0, 0
    used_numbers = {"table": set(), "figure": set()}
    seen_requirement_ids, requirement_items, matrix_seen = set(), [], False
    for section in spec["sections"]:
        level = section.get("level", 1)
        require(1 <= level <= 3, "Nivel de sección fuera de 1..3")
        require(level == 1 or counters[level-2] > 0, "Salto de nivel de sección")
        counters[level-1] += 1
        for i in range(level, 3):
            counters[i] = 0
        section["_number"] = ".".join(map(str, counters[:level]))
        shown = heading_text(section["title"], mode)
        items = [(section, f'{section["_number"]}. {shown}')]
        for block in section.get("blocks", []):
            kind = block["type"]
            require(kind in ("paragraph", "list", "table", "figure", "note", "pagebreak", "reference", "quotation",
                             "procedure", "notice", "fields", "testcase", "risks", "quote", "requirements", "impact", "wbs"),
                    f"Bloque no soportado: {kind}")
            if kind == "fields":
                validate_fields(block)
            if kind == "testcase":
                validate_testcase(block)
                block["_label"] = f'Caso {block["id"]}. {block["title"]}'
                items.append((block, block["_label"]))
            if kind == "risks":
                validate_risks(block)
                table_n = bind_risk_block(block, section, counters, table_n, form, mode, separator)
                items.append(({"id": block["id"]}, block["_matrix_label"]))
                items.append(({"id": block["_register_id"]}, block["_register_label"]))
                items.append(({"id": block["_summary_heading_id"]}, block["_summary_heading"]))
                items.append(({"id": block["_summary_id"]}, block["_summary_label"]))
                for risk in block["items"]:
                    items.append((risk, risk["id"]))
            if kind == "quote":
                validate_quote(block)
                table_n += 1
                block["_number_label"] = f"Tabla {table_n}"
                block["_label"] = f'Tabla {table_n}{separator}{block["title"]}'
                items.append((block, block["_label"]))
            if kind == "impact":
                validate_impact(block)
                table_n += 1
                block["_number_label"] = f"Tabla {table_n}"
                block["_label"] = f'Tabla {table_n}{separator}{block["title"]}'
                items.append((block, block["_label"]))
            if kind == "wbs":
                validate_wbs(block)
                table_n += 1
                block["_number_label"] = f"Tabla {table_n}"
                block["_label"] = f'Tabla {table_n}{separator}{block["title"]}'
                items.append((block, block["_label"]))
            if kind == "requirements":
                matrix_seen = validate_requirements(block, seen_requirement_ids, requirement_items, matrix_seen) or matrix_seen
                if block.get("matrix"):
                    table_n += 1
                    block["_number_label"] = f"Tabla {table_n}"
                    block["_label"] = f'Tabla {table_n}{separator}{block["title"]}'
                    items.append((block, block["_label"]))
                else:
                    for requirement in block["items"]:
                        items.append((requirement, requirement["id"]))
            if kind == "notice":
                validate_notice(block)
            if kind == "procedure":
                validate_procedure(block)
                procedure_n += 1
                block["_number_label"] = f"Procedimiento {procedure_n}"
                block["_label"] = f'{block["_number_label"]}. {block["title"]}'
                items.append((block, block["_label"]))
            if kind in ("table", "figure"):
                if kind == "table":
                    table_n += 1
                    number = block.get("number", str(table_n))
                else:
                    figure_n += 1
                    number = block.get("number", str(figure_n))
                require(str(number) not in used_numbers[kind], f"Número duplicado: {kind} {number}")
                used_numbers[kind].add(str(number))
                block["_number_label"] = f'{"Tabla" if kind == "table" else "Figura"} {number}'
                block["_label"] = block["_number_label"] + separator + block["title"]
                items.append((block, block["_label"]))
        for item, label in items:
            key = item["id"]
            require(re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", key), f"ID no válido: {key}")
            require(key not in labels, f"ID duplicado: {key}")
            labels[key] = label
    return labels


def styles_for(brand, base, layout=None):
    layout = layout or format_for({})
    apa = layout["profile"] == "institucional-apa"
    normal, bold, italic, bold_italic = "Helvetica", "Helvetica-Bold", "Helvetica-Oblique", "Helvetica-BoldOblique"
    if brand.get("fonts"):
        require({"normal", "bold"} <= set(brand["fonts"]) <= {"normal", "bold", "italic", "bold_italic"},
                "fonts requiere normal/bold y admite italic/bold_italic")
        if apa:
            require({"italic", "bold_italic"} <= set(brand["fonts"]),
                    "El perfil APA con TTF requiere las cuatro variantes de fuente")
        normal, bold = "Institutional", "Institutional-Bold"
        italic, bold_italic = normal, bold
        for role, name in [("normal", normal), ("bold", bold), ("italic", "Institutional-Italic"),
                           ("bold_italic", "Institutional-BoldItalic")]:
            if role in brand["fonts"]:
                pdfmetrics.registerFont(TTFont(name, str(pathsafe(base, brand["fonts"][role]))))
                if role == "italic": italic = name
                if role == "bold_italic": bold_italic = name
        pdfmetrics.registerFontFamily(normal, normal=normal, bold=bold, italic=italic, boldItalic=bold_italic)
    ink = colors.HexColor(brand.get("ink", "#17232F"))
    accent = colors.HexColor(brand["accent"])
    size = layout["body_size_pt"]
    leading = size*layout["line_spacing"]
    body_alignment = TA_JUSTIFY if layout.get("justify") else TA_LEFT
    root = ParagraphStyle("body", fontName=normal, fontSize=size, leading=leading,
                          firstLineIndent=layout["first_line_indent_mm"]*mm, alignment=body_alignment,
                          textColor=ink, spaceBefore=0, spaceAfter=layout["paragraph_space_after_pt"],
                          allowWidows=0, allowOrphans=0)
    def style(name, **kw):
        kw.setdefault("firstLineIndent", 0)
        kw.setdefault("leftIndent", 0)
        kw.setdefault("alignment", TA_LEFT)  # only body text follows the justification setting
        return ParagraphStyle(name, parent=root, **kw)
    result = {"body": root,
            "h1": style("h1", fontName=bold, fontSize=16, leading=20, spaceBefore=15,
                        spaceAfter=12, keepWithNext=True),
            "h2": style("h2", fontName=bold, fontSize=12, leading=16, spaceBefore=12,
                        spaceAfter=8, keepWithNext=True),
            "h3": style("h3", fontName=bold, fontSize=11, leading=14, spaceBefore=10,
                        spaceAfter=7, keepWithNext=True),
            "title": style("title", fontName=bold, fontSize=29, leading=35, spaceAfter=20),
            "kicker": style("kicker", fontName=bold, fontSize=9, leading=13,
                            textColor=accent, spaceAfter=13),
            "cell": style("cell", fontSize=9, leading=12, spaceAfter=0),
            "caption": style("caption", fontName=bold, fontSize=9.5, leading=13, spaceAfter=0),
            "small": style("small", fontSize=8.5, leading=12, spaceAfter=8),
            "index": style("index", fontSize=10, leading=14, spaceAfter=3),
            "header": style("header", fontName=bold, fontSize=10, leading=13, spaceAfter=0),
            "entity": style("entity", fontName=bold, fontSize=9.5, leading=12,
                            alignment=TA_CENTER, spaceAfter=0),
            "meta": style("meta", fontSize=8.5, leading=11, alignment=TA_CENTER, spaceAfter=0),
            "footer": style("footer", fontSize=8.5, leading=11, spaceAfter=0)}
    result["footer_right"] = ParagraphStyle("footer-right", parent=result["footer"], alignment=TA_RIGHT)
    result["plain"] = style("plain")
    result["list"] = style("list", leftIndent=18, firstLineIndent=-18, alignment=body_alignment)
    result["reference"] = style("reference", leftIndent=layout["reference_indent_mm"]*mm,
                                firstLineIndent=-layout["reference_indent_mm"]*mm)
    result["quotation"] = style("quotation", leftIndent=12.7*mm, alignment=body_alignment)
    result["quotation_continued"] = style("quotation-continued", leftIndent=12.7*mm, firstLineIndent=12.7*mm,
                                          alignment=body_alignment)
    result["procedure_title"] = style("procedure-title", fontName=bold, spaceBefore=10,
                                       spaceAfter=6, keepWithNext=True)
    result["procedure_action"] = style("procedure-action", leftIndent=18, firstLineIndent=-18,
                                        keepWithNext=True)
    result["procedure_detail"] = style("procedure-detail", leftIndent=18)
    result["procedure_context"] = style("procedure-context", keepWithNext=True)
    for name, indent in (("bulleted", 12), ("ordered", 20)):
        result[name] = style(name, leftIndent=indent, bulletIndent=0, bulletFontName=normal,
                             bulletFontSize=size, spaceAfter=3, alignment=body_alignment)
    result["table_valign"] = "MIDDLE" if apa else "TOP"  # a Word-like "center left" cell in the default profile
    result["notice"] = style("notice", leftIndent=8, rightIndent=8, spaceBefore=10, spaceAfter=10,
                              borderWidth=.55, borderColor=ink, borderPadding=6)
    if apa:
        result.update({
            "cell": style("cell-apa", leading=size*layout["table_line_spacing"]),
            "caption": style("caption-apa", keepWithNext=True),
            "small": style("notes-apa"),
            "note_label": ParagraphStyle("note-label", parent=result["kicker"], spaceBefore=10, spaceAfter=4),
        })
    return result


def flow_figure(block, width, styles, accent):
    nodes = block["nodes"]
    require(2 <= len(nodes) <= 5, "Flujo simple: usar 2..5 nodos; para otros casos proporcionar path")
    gap, box_h, pad = 7*mm, 20*mm, 3*mm
    box_w = (width-gap*(len(nodes)-1))/len(nodes)
    drawing = Drawing(width, 34*mm)
    for i, text in enumerate(nodes):
        x, y = i*(box_w+gap), 8*mm
        drawing.add(Rect(x, y, box_w, box_h, strokeColor=accent,
                         fillColor=colors.white, strokeWidth=.7))
        p = Paragraph(escape(plain(text)), styles["cell"])
        _, ph = p.wrap(box_w-2*pad, box_h-2*pad)
        require(ph <= box_h-2*pad, f"Rótulo de figura demasiado largo: {text}")
        # Render paragraphs as flowables on the vector drawing canvas.
        drawing.__dict__.setdefault("_paragraphs", []).append((p, x+pad, y+(box_h-ph)/2))
        if i < len(nodes)-1:
            start, end, cy = x+box_w+1.2*mm, x+box_w+gap-1.2*mm, y+box_h/2
            drawing.add(Line(start, cy, end, cy, strokeColor=accent, strokeWidth=.8))
            drawing.add(Polygon([end,cy,end-1.8*mm,cy+1*mm,end-1.8*mm,cy-1*mm],
                                strokeColor=accent, fillColor=accent))
    class LabeledDrawing(Flowable):
        def wrap(self, aw, ah):
            return drawing.width, drawing.height
        def draw(self):
            from reportlab.graphics import renderPDF
            renderPDF.draw(drawing, self.canv, 0, 0)
            for p, x, y in drawing.__dict__["_paragraphs"]:
                p.drawOn(self.canv, x, y)
    return LabeledDrawing()


def compile_report(source, output):
    raw = source.read_bytes()
    spec = json.loads(raw)
    base = source.resolve().parent
    spec["_base"] = base
    require(spec.get("schema_version") == 1, "schema_version debe ser 1")
    for key in ("document", "brand", "sections", "changes"):
        require(key in spec, f"Falta {key}")
    for key in ("title", "code", "version", "date", "status"):
        require(isinstance(spec["document"].get(key), str) and spec["document"][key].strip(),
                f"Falta document.{key}")
    date.fromisoformat(spec["document"]["date"])
    validate_lifecycle(spec["document"])
    require(bool(spec["sections"]), "Documento sin secciones")
    require(bool(spec["changes"]), "Declarar al menos la revisión inicial real o demostrativa")
    require(spec["brand"].get("entity"), "Falta brand.entity")
    spec["brand"].setdefault("accent", "#155D86")
    require(spec["document"].get("paper", "A4") in ("A4", "Letter"), "paper: A4 o Letter")
    document_kind = spec["document"].get("kind", "informe")
    require(document_kind in KIND_RULES, "Tipo de documento desconocido")
    rules = KIND_RULES[document_kind]
    form = rules.get("form", False)
    show_changes = spec["document"].get("show_changes", False)
    require(isinstance(show_changes, bool), "document.show_changes debe ser booleano")
    require(not (show_changes and document_kind == "informe"),
            "document.show_changes no aplica al informe, que ya imprime su control de cambios")
    indexes = spec["document"].get("indexes", [])
    require(isinstance(indexes, list) and all(item in INDEX_TITLES for item in indexes)
            and len(set(indexes)) == len(indexes),
            "document.indexes admite una lista sin repetir de: contents, tables, figures")
    require(not indexes or form, "document.indexes aplica solo a los tipos de formulario; el informe ya trae sus índices")
    for key, kind_name in (("tables", "table"), ("figures", "figure")):
        require(key not in indexes or document_has(spec, kind_name),
                f"document.indexes pide {key} pero el documento no tiene {'tablas' if key == 'tables' else 'figuras'}: quitarlo de la lista")
    layout = format_for(spec)
    mode = heading_mode_for(spec)
    for key in ("title", "short_title"):
        if spec["document"].get(key):
            spec["document"][key] = heading_text(spec["document"][key], mode)
    apa = layout["profile"] == "institucional-apa"
    labels = registry(spec)
    if "choice" in rules:
        # The weightiest decision is a single-mark choice: a multiple one (a list of marks) does not stand for it.
        require(any("options" in item and not item.get("multiple") for section in spec["sections"]
                    for block in section.get("blocks", []) if block["type"] == "fields" for item in block["items"]),
                rules["choice"])
    reference_labels = dict(labels)
    if apa:
        for section in spec["sections"]:
            for block in section.get("blocks", []):
                if block["type"] in ("table", "figure", "procedure", "quote", "impact", "wbs"):
                    reference_labels[block["id"]] = block["_number_label"]
                if block["type"] == "risks":
                    reference_labels[block["id"]] = block["_matrix_number_label"]
                    reference_labels[block["_summary_id"]] = block["_summary_number_label"]
                if block["type"] == "requirements" and block.get("matrix"):
                    reference_labels[block["id"]] = block["_number_label"]
    styles = styles_for(spec["brand"], base, layout)
    if document_kind == "acta-reunion":
        styles["header"].alignment = TA_CENTER
    if document_kind != "informe":
        styles["h1"] = ParagraphStyle("acta-heading", parent=styles["h1"], spaceBefore=9, spaceAfter=6)
    accent = colors.HexColor(spec["brand"]["accent"])
    rule = colors.HexColor(spec["brand"].get("rule", "#CED6DD"))
    # Choose black or white via WCAG relative luminance, independent of hue.
    linear = lambda c: c/12.92 if c <= .04045 else ((c+.055)/1.055)**2.4
    luminance = sum(k*linear(c) for k,c in zip((.2126,.7152,.0722), (accent.red,accent.green,accent.blue)))
    head_ink = colors.black if (luminance+.05)/.05 >= 1.05/(luminance+.05) else colors.white
    head_style = ParagraphStyle("column", parent=styles["cell"],
                                fontName=styles["h2" if apa else "caption"].fontName,
                                textColor=colors.black if apa else head_ink,
                                alignment=TA_CENTER if apa else TA_LEFT)
    probe = PageTotal()
    paper = A4 if spec["document"].get("paper", "A4") == "A4" else letter
    output.parent.mkdir(parents=True, exist_ok=True)
    doc = Document(output, spec, styles, probe, pagesize=paper, leftMargin=21*mm,
                   rightMargin=21*mm, topMargin=58*mm, bottomMargin=25*mm)
    if apa:
        # keepWithNext groups (a heading with its table, a sentence with its list) yield when much of the page is free.
        doc.keepTogetherClass = lambda flowables: FlexKeepTogether(flowables, limit=SECTION_MAX_BLANK * doc.height)

    # A form-like report packs its rows and the space between tables more tightly.
    pad, before, after = (4, 6, 10) if form else (6, 7, 13)

    def markup(value):
        text = escape(plain(value))
        def link(match):
            key = match.group(1)
            require(key in labels, f"Referencia desconocida: {key}")
            return f'<link href="#{key}" color="{spec["brand"]["accent"]}">{escape(reference_labels[key])}</link>'
        return REF.sub(link, text)

    def p(value, role="body"):
        return Paragraph(markup(value).replace("\n", "<br/>"), styles[role])

    def content_paragraph(block, role):
        require(bool(block.get("text")) != bool(block.get("runs")), "Usar text o runs, no ambos ni vacíos")
        if block.get("runs"):
            require(isinstance(block["runs"], list), "runs debe ser una lista")
            pieces = []
            for run in block["runs"]:
                require(isinstance(run, dict) and not set(run)-{"text", "italic", "bold"}, "Tramo de texto no válido")
                require(isinstance(run.get("text"), str), "Cada tramo requiere text")
                piece = markup(run["text"]).replace("\n", "<br/>")
                for flag, tag in [("italic", "i"), ("bold", "b")]:
                    require(isinstance(run.get(flag, False), bool), "Los estilos de tramo son booleanos")
                    if run.get(flag): piece = f"<{tag}>{piece}</{tag}>"
                pieces.append(piece)
            return Paragraph("".join(pieces), styles[role])
        return p(block["text"], role)

    def caption_for(block):
        if not apa:
            return p(block["_label"], "caption")
        return Paragraph(f'<b>{markup(block["_number_label"])}</b><br/><i>{markup(block["title"])}</i>',
                         styles["caption"])

    def notice_for(block):
        label = NOTICE_LABELS[block["level"]]
        title = f': {markup(block["title"])}' if block.get("title") else ""
        return Paragraph(f'<b>{label}{title}.</b> {markup(block["text"]).replace(chr(10), "<br/>")}',
                         styles["notice"])

    def procedure_for(block):
        heading = p(block["_label"], "procedure_title")
        heading.entry = (block["id"], block["_label"], "procedure", 0)
        parts = [heading]
        if block.get("role"):
            parts += [Paragraph(f'<b>Rol:</b> {markup(block["role"])}', styles["procedure_context"])]
        if block.get("prerequisites"):
            parts += [p("Condiciones iniciales:", "procedure_context")]
            for item in block["prerequisites"]:
                parts += [Paragraph(f'• {markup(item)}',
                                    ParagraphStyle("procedure-prerequisite", parent=styles["list"], keepWithNext=True))]
        for i, step in enumerate(block["steps"], 1):
            group = [notice_for(step["notice"])] if step.get("notice") else []
            group += [Paragraph(f'<b>{i}.</b> {markup(step["action"])}', styles["procedure_action"]),
                      Paragraph(f'<b>Resultado esperado:</b> {markup(step["expected"])}', styles["procedure_detail"])]
            if step.get("on_failure"):
                group += [Paragraph(f'<b>Si no se obtiene:</b> {markup(step["on_failure"])}', styles["procedure_detail"])]
            # A step moves intact when it fits a page; a long procedure can span pages.
            parts += [KeepTogether(group), Spacer(1,6)]
        return parts

    def table(headers, rows, widths=None, title=None, source_note=None, title_block=None):
        require(len(headers) >= 1, "Tabla sin columnas")
        for row in rows:
            require(len(row) == len(headers), "Fila con número de columnas incorrecto")
        if widths is None:
            widths = [1] * len(headers)
        require(len(widths) == len(headers) and all(float(v) > 0 for v in widths), "Anchos de tabla no válidos")
        widths = [doc.width*float(v)/sum(widths) for v in widths]
        if apa:
            widths = fit_widths(widths, headers, rows, head_style.fontName, styles["cell"].fontName,
                                styles["cell"].fontSize)
        data = []
        heading_row = 0
        if title:
            data.append([caption_for(title_block) if title_block else p(title, "caption")]+[""]*(len(headers)-1))
            heading_row = 1
        data.append([Paragraph(markup(v), head_style) for v in headers])
        signature_columns = {i for i, header in enumerate(headers) if is_signature_label(header)}
        def body_cell(row, i, value):
            # An empty cell of a signature column or row reserves the room to sign (often electronically): no printed line.
            if not str(value).strip() and (i in signature_columns or is_signature_label(row[0])):
                return [Spacer(1, SIGNATURE_SPACE)]
            return p(value, "cell")
        data.extend([[body_cell(row, i, v) for i, v in enumerate(row)] for row in rows])
        if source_note:
            note = (Paragraph(f'<i>Nota.</i> Fuente: {markup(source_note)}', styles["small"])
                    if apa else p(f"Fuente: {source_note}", "small"))
            data.append([note]+[""]*(len(headers)-1))
        result = RegisteredTable(data, colWidths=widths, repeatRows=heading_row+1,
                                 hAlign="LEFT", splitByRow=1, splitInRow=0,
                                 spaceBefore=before, spaceAfter=after)
        commands = [
            ("VALIGN", (0,0),(-1,-1),styles["table_valign"]),
            ("LEFTPADDING", (0,0),(-1,-1),6), ("RIGHTPADDING", (0,0),(-1,-1),6),
            ("TOPPADDING", (0,0),(-1,-1),pad), ("BOTTOMPADDING", (0,0),(-1,-1),pad),
            ("BACKGROUND", (0,heading_row),(-1,heading_row),accent),
            ("LINEBELOW", (0,heading_row),(-1,-1),.3,rule),
            ("ROWBACKGROUNDS", (0,heading_row+1),(-1,-1),[colors.white,colors.HexColor("#F4F6F8")]),
        ]
        if apa:
            # Sparse horizontal rules; preserve whitespace instead of boxing every cell.
            commands = [c for c in commands if c[0] not in ("BACKGROUND", "LINEBELOW", "ROWBACKGROUNDS")]
            commands += [("LINEABOVE", (0,heading_row),(-1,heading_row),.6,colors.black),
                         ("LINEBELOW", (0,heading_row),(-1,heading_row),.6,colors.black),
                         ("LINEBELOW", (0,len(data)-2 if source_note else -1),(-1,len(data)-2 if source_note else -1),.6,colors.black)]
        if title:
            commands += [("SPAN",(0,0),(-1,0)), ("BACKGROUND",(0,0),(-1,0),colors.white),
                         ("LEFTPADDING",(0,0),(-1,0),0)]
        if source_note:
            commands += [("SPAN",(0,-1),(-1,-1)), ("BACKGROUND",(0,-1),(-1,-1),colors.white),
                         ("LEFTPADDING",(0,-1),(-1,-1),0)]
        result.setStyle(TableStyle(commands))
        # A form-like report keeps each table whole when it fits on one page.
        result.keep_whole, result.page_height = form, doc.height
        result.blank_limit = SECTION_MAX_BLANK if apa else None
        result._closing_signature = signature_rows(headers, rows)
        return result

    def fields_for(block):
        """Label/value grid; a choice stacks its options, the marked ones crossed."""
        per_row = block.get("columns", 1)
        # An 11 pt bold label such as «Requerimiento» needs the wider label column of the APA profile.
        weights = [.24, .76] if per_row == 1 else ([.20, .30, .20, .30] if apa else [.18, .32, .18, .32])
        label_style = ParagraphStyle("field-label", parent=styles["cell"], fontName=styles["h1"].fontName)
        ink = colors.HexColor(spec["brand"].get("ink", "#17232F"))
        data, commands = [], [
            ("VALIGN", (0,0),(-1,-1),styles["table_valign"]), ("GRID", (0,0),(-1,-1),.5,rule),
            ("LEFTPADDING", (0,0),(-1,-1),6), ("RIGHTPADDING", (0,0),(-1,-1),6),
            ("TOPPADDING", (0,0),(-1,-1),5), ("BOTTOMPADDING", (0,0),(-1,-1),5)]
        items = block["items"]
        for row_index, start in enumerate(range(0, len(items), per_row)):
            row = []
            chunk = items[start:start+per_row]
            for i, item in enumerate(chunk):
                if "options" in item:
                    lines = []
                    # A single choice carries one mark; a multiple one carries a list of them, possibly empty.
                    marks = item["selected"] if item.get("multiple") else [item["selected"]]
                    for option in item["options"]:
                        lines += [OptionLine(markup(option), option in marks, styles["cell"], ink),
                                  Spacer(1, 2)]
                    value = lines[:-1]
                else:
                    value = p(item["value"], "cell")
                row += [Paragraph(markup(item["label"]), label_style), value]
                commands.append(("BACKGROUND", (2*i,row_index),(2*i,row_index), colors.HexColor("#F4F6F8")))
            if len(chunk) < per_row:
                # An odd last item takes the remaining width instead of leaving empty cells.
                row += [""]*(2*per_row-len(row))
                commands.append(("SPAN", (1,row_index),(-1,row_index)))
            data.append(row)
        grid = RegisteredTable(data, colWidths=[doc.width*w for w in weights], hAlign="LEFT",
                               splitByRow=1, splitInRow=0, spaceBefore=before, spaceAfter=after)
        grid.keep_whole, grid.page_height = True, doc.height  # a grid stays on one page whenever it fits
        grid.setStyle(TableStyle(commands))
        return grid

    m = spec["document"]
    # The APA header is 11 pt bold: reserve enough width to keep «Versión» whole.
    history_widths = [1.4,1.5,4.6,2] if apa else [1,1.5,5,2]
    history = []
    for change in spec["changes"]:
        for key in ("version", "date", "summary", "author"):
            require(key in change, f"Cambio sin {key}")
        date.fromisoformat(change["date"])
        affects = "; ".join("{{ref:"+key+"}}" for key in change.get("affects", []))
        history.append([change["version"], date.fromisoformat(change["date"]).strftime("%d/%m/%Y"),
                        change["summary"]+("\n"+affects if affects else ""), change["author"]])
    if document_kind == "informe":
        story = [probe, Spacer(1,22*mm), p(m["code"], "kicker"), p(m["title"], "title")]
        if m.get("subtitle"):
            story += [p(m["subtitle"], "plain")]
        story += [Spacer(1,12*mm), p(spec["brand"]["entity"], "h2"),
                  p(spec["brand"].get("unit", ""), "plain"), Spacer(1,14*mm),
                  p(f'Versión {m["version"]} · {date.fromisoformat(m["date"]).strftime("%d/%m/%Y")} · {m["status"]}', "small")]
        if m.get("notice"):
            story += [p(m["notice"], "small")]
        story += [PageBreak(), p(heading_text("Histórico de revisiones", mode), "h1")]
        story += [table(["Versión", "Fecha", "Cambio y localizador", "Responsable"], history, history_widths)]
        if m.get("control_note"):
            story += [p(m["control_note"], "small")]
        extra_index_started = False
        for title, kind, has in [("Contenido", "section", True),
                                 ("Índice de tablas", "table", any(b["type"] == "table" for s in spec["sections"] for b in s.get("blocks", []))),
                                 ("Índice de figuras", "figure", any(b["type"] == "figure" for s in spec["sections"] for b in s.get("blocks", []))),
                                 ("Índice de procedimientos", "procedure", any(b["type"] == "procedure" for s in spec["sections"] for b in s.get("blocks", [])))]:
            if has:
                if kind == "section" or not extra_index_started:
                    story += [PageBreak()]
                if kind != "section":
                    extra_index_started = True
                story += [p(title,"h1"), Navigation(kind, styles["index"])]
        story += [PageBreak()]
    else:
        story = [probe, p(m["title"], "h1")]
        if m.get("subtitle"):
            story += [p(m["subtitle"], "plain")]
        if m.get("notice"):
            story += [p(m["notice"], "small")]
        # Optional indexes of a form-like kind sit under the title, before the first section.
        for name, kind_name in (("contents", "section"), ("tables", "table"), ("figures", "figure")):
            if name in indexes:
                story += [p(heading_text(INDEX_TITLES[name], mode), "h2"), Navigation(kind_name, styles["index"], tight=True)]
    section_starts = []
    for section_index, section in enumerate(spec["sections"]):
        if section.get("new_page") and section_index:
            story += [PageBreak()]
        section_starts.append(len(story))
        heading = p(labels[section["id"]], f'h{section.get("level",1)}')
        heading.entry = (section["id"], labels[section["id"]], "section", section.get("level",1)-1)
        story += [heading]
        blocks = section.get("blocks", [])
        for block_index, block in enumerate(blocks):
            kind = block["type"]
            if kind == "paragraph":
                paragraph = content_paragraph(block, "plain" if block.get("indent") is False else "body")
                # In a form-like report a sentence that introduces a list never ends a page on its own.
                if form and block_index+1 < len(blocks) and blocks[block_index+1]["type"] == "list":
                    paragraph.keepWithNext = True
                story += [paragraph]
            elif kind == "reference":
                story += [content_paragraph(block, "reference")]
            elif kind == "quotation":
                require(isinstance(block.get("text"), str) and len(block["text"].split()) >= 40,
                        "Cita en bloque: requiere al menos 40 palabras")
                require(isinstance(block.get("citation"), str) and bool(block["citation"].strip()),
                        "Cita en bloque: falta cita y localizador")
                paragraphs = [part.strip() for part in block["text"].split("\n\n") if part.strip()]
                for i, part in enumerate(paragraphs):
                    if i == len(paragraphs)-1: part += " "+block["citation"]
                    story += [p(part, "quotation" if i == 0 else "quotation_continued")]
            elif kind == "list" and form:
                # Hanging marker: wrapped lines align with the text. A short list stays whole; a longer one
                # may break between pages but never leaves a single item on either side.
                ordered, items = block.get("ordered", False), block["items"]
                for i, item in enumerate(items):
                    entry = Paragraph(markup(item).replace("\n", "<br/>"), styles["ordered" if ordered else "bulleted"],
                                      bulletText=f"{i+1}." if ordered else "•")
                    entry.keepWithNext = i < len(items)-1 if len(items) <= 3 else i in (0, len(items)-2)
                    story += [entry]
                story += [Spacer(1, 6)]
            elif kind == "list":
                for i, item in enumerate(block["items"]):
                    story += [p(f'{i+1}. {item}' if block.get("ordered") else f'• {item}', "list" if apa else "body")]
            elif kind == "fields":
                grid = fields_for(block)
                # A grid stays with the table, list or sentence that details it.
                if form and block_index+1 < len(blocks) and blocks[block_index+1]["type"] in ("table", "list", "paragraph"):
                    grid.keepWithNext = True
                story += [grid]
            elif kind == "note":
                story += [p(block.get("label", "Nota"), "note_label" if apa else "kicker"), p(block["text"],"small")]
            elif kind == "notice":
                story += [notice_for(block)]
            elif kind == "procedure":
                story += procedure_for(block)
            elif kind == "testcase":
                append_testcase(story, testcase_for(block, doc, styles, p, markup, accent, rule, head_style, apa), doc)
            elif kind == "risks":
                story += risks_for(block, table, p, styles, markup, doc.width, rule, doc.height)
            elif kind == "quote":
                story += [quote_for(block, table)]
            elif kind == "impact":
                story += [impact_for(block, table)]
            elif kind == "wbs":
                story += wbs_for(block, styles, markup, doc.width, accent, rule, head_style, doc.height,
                                 apa, caption_for(block) if apa else None)
            elif kind == "requirements":
                story += requirements_for(block, table, p, styles, markup, doc.width, rule, doc.height)
            elif kind == "pagebreak":
                story += [PageBreak()]
            elif kind == "table":
                t = table(block["headers"],block["rows"],block.get("widths"),block["_label"],block.get("source"),block)
                t.entry = (block["id"],block["_label"],"table",0)
                # In a form-like report a table stays with the sentence or list that explains it (a legend, a note).
                if form and block_index+1 < len(blocks) and blocks[block_index+1]["type"] in ("paragraph", "list"):
                    t.keepWithNext = True
                story += [t]
            elif kind == "figure":
                if block.get("path"):
                    path = pathsafe(base, block["path"])
                    if path.suffix.lower() == ".svg":
                        from svglib.svglib import svg2rlg
                        figure = svg2rlg(str(path))
                        require(figure is not None, f"SVG no válido: {path}")
                        factor = min(doc.width/figure.width, float(block.get("max_height_mm",120))*mm/figure.height)
                        figure.scale(factor,factor)
                        figure.width *= factor
                        figure.height *= factor
                    else:
                        figure = Image(str(path))
                        factor = min(doc.width/figure.imageWidth, float(block.get("max_height_mm",120))*mm/figure.imageHeight)
                        figure.drawWidth, figure.drawHeight = figure.imageWidth*factor, figure.imageHeight*factor
                else:
                    figure = flow_figure(block,doc.width,styles,accent)
                caption = caption_for(block)
                caption.entry = (block["id"],block["_label"],"figure",0)
                # Register on the figure itself (KeepTogether children enter the frame).
                figure.entry = caption.entry
                del caption.entry
                components = ([caption, Spacer(1,3*mm), figure] if apa else
                              [figure, Spacer(1,3*mm), caption])
                if apa:
                    notes = block.get("description", "")
                    if block.get("source"): notes += f' Fuente: {block["source"]}'
                    if notes.strip(): components += [Paragraph(f'<i>Nota.</i> {markup(notes.strip())}', styles["small"])]
                    components += [Spacer(1,styles["body"].leading)]
                else:
                    if block.get("description"):
                        components += [p(block["description"],"small")]
                    if block.get("source"):
                        components += [p(f'Fuente: {block["source"]}',"small")]
                if story and getattr(story[-1], "entry", (None, None, None))[2] == "section":
                    # A figure opening its section carries the heading: reportlab does not chain a heading to a
                    # KeepTogether, and the heading would be left alone at the foot of the page.
                    components = [story.pop()] + components
                story += [FitFigure(components, figure, SECTION_MAX_BLANK * doc.height) if apa else KeepTogether(components)]
    if apa:
        keep_sections(story, section_starts, doc.height)
    if show_changes:
        dated = history
        closing = [p(heading_text("Histórico de revisiones", mode), "h1"),
                   table(["Versión", "Fecha", "Cambio y localizador", "Responsable"], dated, history_widths)]
        story = append_closing(story, closing, doc.width, doc.height, flexible=apa) if form else story + closing
    doc.multiBuild(story, maxPasses=10)
    assets = []
    asset_values = ([spec["brand"]["logo"]] if spec["brand"].get("logo") else [])
    asset_values += list(spec["brand"].get("fonts", {}).values())
    asset_values += [b["path"] for s in spec["sections"] for b in s.get("blocks",[]) if b.get("path")]
    for value in asset_values:
        asset_path = pathsafe(base,value)
        assets.append({"path":value,"sha256":hashlib.sha256(asset_path.read_bytes()).hexdigest()})
    manifest = {"schema_version":1, "source":source.name, "source_sha256":hashlib.sha256(raw).hexdigest(),
                "pdf_sha256":hashlib.sha256(output.read_bytes()).hexdigest(), "assets":assets,
                "pages":doc.page, "passes":doc.passes, "paper":m.get("paper","A4"),
                "document":m, "format":layout, "entries":doc.entries, "labels":labels,
                "reference_labels":reference_labels}
    if "lifecycle" in m:
        manifest["lifecycle"] = m["lifecycle"]
    output.with_suffix(".manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    manifest = compile_report(args.source, args.output)
    print(json.dumps({"pdf":str(args.output),"pages":manifest["pages"],"passes":manifest["passes"]},ensure_ascii=False))
