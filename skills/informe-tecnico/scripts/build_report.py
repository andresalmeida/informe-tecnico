#!/usr/bin/env python3
"""Compile an editable report specification with convergent navigation and pagination."""
import argparse
import hashlib
import json
import re
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, PageBreak,
    LongTable, TableStyle, KeepTogether, Image, Flowable, IndexingFlowable,
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.graphics.shapes import Drawing, Rect, Line, Polygon

REF = re.compile(r"\{\{ref:([a-zA-Z0-9_-]+)\}\}")
# One grid for both header rows: entity and pagination share the same edge.
HEADER_BOUNDS = (0, .42, .71, 1)


def format_for(spec):
    """Resolve an explicit profile; pre-0.3 sources retain their layout."""
    config = spec.get("format", {})
    require(isinstance(config, dict), "format debe ser un objeto")
    profile = config.get("profile", "institucional")
    require(profile in ("institucional", "institucional-apa"), "Perfil de formato desconocido")
    apa = profile == "institucional-apa"
    values = {"profile": profile, "body_size_pt": 11.0 if apa else 10.5,
              "line_spacing": 2.0 if apa else 14.5/10.5,
              "first_line_indent_mm": 12.7 if apa else 0.0,
              "paragraph_space_after_pt": 0.0 if apa else 8.0,
              "reference_indent_mm": 12.7,
              "table_line_spacing": 1.0 if apa else 12/9}
    require(not set(config)-set(values), "Campo de formato desconocido")
    for key in values.keys()-{"profile"}:
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


def require(condition, message):
    if not condition:
        raise ValueError(message)


def plain(value):
    return str(value) if value is not None else "No informado"


def pathsafe(base, value):
    path = Path(value)
    return path if path.is_absolute() else base / path


class Navigation(TableOfContents):
    def __init__(self, kind, style):
        super().__init__()
        self.kind = kind
        self.levelStyles = [
            ParagraphStyle(f"index-{kind}-{i}", parent=style, leftIndent=i*11,
                           firstLineIndent=0, spaceBefore=5 if i == 0 else 2)
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
    def split(self, available_width, available_height):
        parts = super().split(available_width, available_height)
        if parts and hasattr(self, "entry"):
            parts[0].entry = self.entry
        return parts


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
        self.box_text(f'{m["code"]} · {m["status"]}', x+w*.51, 8*mm,
                      w*.49, 9*mm, self.styles["footer"])
        if brand.get("frame", False):
            canvas.setStrokeColor(colors.HexColor(brand.get("rule", "#CFD6DD")))
            canvas.rect(12*mm, 6*mm, self.pagesize[0]-24*mm, self.pagesize[1]-12*mm)
        canvas.setFillColor(ink)
        canvas.restoreState()

    def box_text(self, text, x, y, width, height, style):
        p = Paragraph(escape(plain(text)), style)
        pw, ph = p.wrap(width, height)
        require(ph <= height-2*mm, f"Texto demasiado largo en encabezado/pie: {text}")
        p.drawOn(self.canv, x, y+(height-ph)/2)


def registry(spec):
    labels, counters, table_n, figure_n = {}, [0, 0, 0], 0, 0
    used_numbers = {"table": set(), "figure": set()}
    for section in spec["sections"]:
        level = section.get("level", 1)
        require(1 <= level <= 3, "Nivel de sección fuera de 1..3")
        require(level == 1 or counters[level-2] > 0, "Salto de nivel de sección")
        counters[level-1] += 1
        for i in range(level, 3):
            counters[i] = 0
        section["_number"] = ".".join(map(str, counters[:level]))
        items = [(section, f'{section["_number"]} {section["title"]}')]
        for block in section.get("blocks", []):
            kind = block["type"]
            require(kind in ("paragraph", "list", "table", "figure", "note", "pagebreak", "reference", "quotation"),
                    f"Bloque no soportado: {kind}")
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
                separator = " " if spec.get("format", {}).get("profile") == "institucional-apa" else ". "
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
    root = ParagraphStyle("body", fontName=normal, fontSize=size, leading=leading,
                          firstLineIndent=layout["first_line_indent_mm"]*mm, alignment=TA_LEFT,
                          textColor=ink, spaceBefore=0, spaceAfter=layout["paragraph_space_after_pt"],
                          allowWidows=0, allowOrphans=0)
    def style(name, **kw):
        kw.setdefault("firstLineIndent", 0)
        kw.setdefault("leftIndent", 0)
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
    result["plain"] = style("plain")
    result["list"] = style("list", leftIndent=18, firstLineIndent=-18)
    result["reference"] = style("reference", leftIndent=layout["reference_indent_mm"]*mm,
                                firstLineIndent=-layout["reference_indent_mm"]*mm)
    result["quotation"] = style("quotation", leftIndent=12.7*mm)
    result["quotation_continued"] = style("quotation-continued", leftIndent=12.7*mm, firstLineIndent=12.7*mm)
    if apa:
        result.update({
            "h1": style("h1-apa", fontName=bold, alignment=TA_CENTER, keepWithNext=True),
            "h2": style("h2-apa", fontName=bold, keepWithNext=True),
            "h3": style("h3-apa", fontName=bold_italic, keepWithNext=True),
            "cell": style("cell-apa", leading=size*layout["table_line_spacing"]),
            "caption": style("caption-apa", keepWithNext=True),
            "small": style("notes-apa"),
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
    require(bool(spec["sections"]), "Documento sin secciones")
    require(bool(spec["changes"]), "Declarar al menos la revisión inicial real o demostrativa")
    require(spec["brand"].get("entity"), "Falta brand.entity")
    spec["brand"].setdefault("accent", "#155D86")
    require(spec["document"].get("paper", "A4") in ("A4", "Letter"), "paper: A4 o Letter")
    layout = format_for(spec)
    apa = layout["profile"] == "institucional-apa"
    labels = registry(spec)
    reference_labels = dict(labels)
    if apa:
        for section in spec["sections"]:
            for block in section.get("blocks", []):
                if block["type"] in ("table", "figure"):
                    reference_labels[block["id"]] = block["_number_label"]
    styles = styles_for(spec["brand"], base, layout)
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

    def table(headers, rows, widths=None, title=None, source_note=None, title_block=None):
        require(len(headers) >= 1, "Tabla sin columnas")
        for row in rows:
            require(len(row) == len(headers), "Fila con número de columnas incorrecto")
        if widths is None:
            widths = [1] * len(headers)
        require(len(widths) == len(headers) and all(float(v) > 0 for v in widths), "Anchos de tabla no válidos")
        widths = [doc.width*float(v)/sum(widths) for v in widths]
        data = []
        heading_row = 0
        if title:
            data.append([caption_for(title_block) if title_block else p(title, "caption")]+[""]*(len(headers)-1))
            heading_row = 1
        data.append([Paragraph(markup(v), head_style) for v in headers])
        data.extend([[p(v, "cell") for v in row] for row in rows])
        if source_note:
            note = (Paragraph(f'<i>Nota.</i> Fuente: {markup(source_note)}', styles["small"])
                    if apa else p(f"Fuente: {source_note}", "small"))
            data.append([note]+[""]*(len(headers)-1))
        result = RegisteredTable(data, colWidths=widths, repeatRows=heading_row+1,
                                 hAlign="LEFT", splitByRow=1, splitInRow=0,
                                 spaceBefore=7, spaceAfter=13)
        commands = [
            ("VALIGN", (0,0),(-1,-1),"TOP"),
            ("LEFTPADDING", (0,0),(-1,-1),6), ("RIGHTPADDING", (0,0),(-1,-1),6),
            ("TOPPADDING", (0,0),(-1,-1),6), ("BOTTOMPADDING", (0,0),(-1,-1),6),
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
        return result

    m = spec["document"]
    story = [probe, Spacer(1,22*mm), p(m["code"], "kicker"), p(m["title"], "title")]
    if m.get("subtitle"):
        story += [p(m["subtitle"], "plain")]
    story += [Spacer(1,12*mm), p(spec["brand"]["entity"], "h2"),
              p(spec["brand"].get("unit", ""), "plain"), Spacer(1,14*mm),
              p(f'Versión {m["version"]} · {m["date"]} · {m["status"]}', "small")]
    if m.get("notice"):
        story += [p(m["notice"], "small")]
    story += [PageBreak(), p("Control de cambios", "h1")]
    history = []
    for change in spec["changes"]:
        for key in ("version", "date", "summary", "author"):
            require(key in change, f"Cambio sin {key}")
        date.fromisoformat(change["date"])
        affects = "; ".join("{{ref:"+key+"}}" for key in change.get("affects", []))
        history.append([change["version"], change["date"], change["summary"]+("\n"+affects if affects else ""), change["author"]])
    story += [table(["Versión", "Fecha", "Cambio y localizador", "Responsable"], history, [1,1.5,5,2])]
    if m.get("control_note"):
        story += [p(m["control_note"], "small")]
    extra_index_started = False
    for title, kind, has in [("Contenido", "section", True),
                             ("Índice de tablas", "table", any(b["type"] == "table" for s in spec["sections"] for b in s.get("blocks", []))),
                             ("Índice de figuras", "figure", any(b["type"] == "figure" for s in spec["sections"] for b in s.get("blocks", [])))]:
        if has:
            if kind == "section" or not extra_index_started:
                story += [PageBreak()]
            if kind != "section":
                extra_index_started = True
            story += [p(title,"h1"), Navigation(kind, styles["index"])]
    story += [PageBreak()]
    for section_index, section in enumerate(spec["sections"]):
        if section.get("new_page") and section_index:
            story += [PageBreak()]
        heading = p(labels[section["id"]], f'h{section.get("level",1)}')
        heading.entry = (section["id"], labels[section["id"]], "section", section.get("level",1)-1)
        story += [heading]
        for block in section.get("blocks", []):
            kind = block["type"]
            if kind == "paragraph":
                story += [content_paragraph(block, "plain" if block.get("indent") is False else "body")]
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
            elif kind == "list":
                for i, item in enumerate(block["items"]):
                    story += [p(f'{i+1}. {item}' if block.get("ordered") else f'• {item}', "list" if apa else "body")]
            elif kind == "note":
                story += [p(block.get("label", "Nota"),"kicker"),p(block["text"],"small")]
            elif kind == "pagebreak":
                story += [PageBreak()]
            elif kind == "table":
                t = table(block["headers"],block["rows"],block.get("widths"),block["_label"],block.get("source"),block)
                t.entry = (block["id"],block["_label"],"table",0)
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
                story += [KeepTogether(components)]
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
    output.with_suffix(".manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    manifest = compile_report(args.source, args.output)
    print(json.dumps({"pdf":str(args.output),"pages":manifest["pages"],"passes":manifest["passes"]},ensure_ascii=False))
