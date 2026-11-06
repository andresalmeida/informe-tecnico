#!/usr/bin/env python3
"""Export an institutional meeting record as an editable Word document."""
import argparse
import json
from datetime import date
from pathlib import Path

from docx import Document
from docx.document import Document as WordDocument
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Mm, Pt, RGBColor

from build_report import REF, format_for, pathsafe, plain, registry, require


def element(tag, **attributes):
    node = OxmlElement(f"w:{tag}")
    for key, value in attributes.items():
        node.set(qn(f"w:{key}"), str(value))
    return node


def word_table(container, width, weights, row_count, border):
    table = container.add_table(rows=row_count, cols=len(weights)) if isinstance(
        container, WordDocument
    ) else container.add_table(rows=row_count, cols=len(weights), width=width)
    table.autofit = False
    for column, weight in zip(table.columns, weights):
        column.width = round(width * weight / sum(weights))
        for cell in column.cells:
            cell.width = column.width
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    properties = table._tbl.tblPr
    borders = element("tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        borders.append(element(side, val="single", sz=4, color=border))
    properties.append(borders)
    for row in table.rows:
        row._tr.get_or_add_trPr().append(element("cantSplit"))
    return table


def cell_text(cell, value, size=9.5, bold=False, alignment=WD_ALIGN_PARAGRAPH.LEFT):
    paragraph = cell.paragraphs[0]
    paragraph.alignment = alignment
    paragraph.paragraph_format.space_before = Pt(3)
    paragraph.paragraph_format.space_after = Pt(3)
    paragraph.paragraph_format.line_spacing = 1.12
    run = paragraph.add_run(value)
    run.font.size = Pt(size)
    run.bold = bold
    return paragraph


def page_field(paragraph, instruction):
    field = element("fldSimple", instr=instruction)
    run = element("r")
    properties = element("rPr")
    properties.append(element("sz", val=18))
    run.append(properties)
    value = element("t")
    value.text = "1"
    run.append(value)
    field.append(run)
    paragraph._p.append(field)


def bookmark(paragraph, number):
    paragraph._p.insert(1, element("bookmarkStart", id=number, name=f"acta_{number}"))
    paragraph._p.append(element("bookmarkEnd", id=number))


def add_text(paragraph, value, labels, anchors, bold=False, italic=False):
    pieces = REF.split(plain(value))
    for index, part in enumerate(pieces):
        if index % 2 == 0:
            run = paragraph.add_run(part)
            run.bold = bold or None
            run.italic = italic or None
        else:
            require(part in labels, f"Referencia inexistente: {part}")
            link = element("hyperlink", anchor=f"acta_{anchors[part]}")
            run = element("r")
            props = element("rPr")
            props.append(element("rStyle", val="Hyperlink"))
            run.append(props)
            content = element("t")
            content.text = labels[part]
            run.append(content)
            link.append(run)
            paragraph._p.append(link)


def build_acta_docx(source, output):
    spec = json.loads(source.read_text(encoding="utf-8"))
    metadata, brand = spec["document"], spec["brand"]
    require(spec.get("schema_version") == 1, "schema_version debe ser 1")
    require(metadata.get("kind") == "acta-reunion", "La salida DOCX admite acta-reunion")
    for key in ("title", "code", "version", "status", "date"):
        require(isinstance(metadata.get(key), str) and metadata[key].strip(), f"Falta document.{key}")
    require(spec.get("sections"), "El acta requiere secciones")
    layout = format_for(spec)
    require(layout["profile"] == "institucional", "Usar el perfil institucional para el acta DOCX")
    labels = registry(spec)
    anchors = {key: number for number, key in enumerate(labels, 1)}
    updated = date.fromisoformat(metadata["date"]).strftime("%d/%m/%Y")
    accent = brand.get("accent", "#155D86").lstrip("#")
    RGBColor.from_string(accent)
    require(metadata.get("paper", "A4") in ("A4", "Letter"), "Papel no admitido")
    doc = Document()
    doc.core_properties.title = metadata["title"]
    doc.core_properties.author = metadata.get("author", "")
    page = doc.sections[0]
    page.page_width, page.page_height = (
        (Mm(215.9), Mm(279.4)) if metadata.get("paper") == "Letter" else (Mm(210), Mm(297))
    )
    page.left_margin = page.right_margin = Mm(21)
    page.top_margin, page.bottom_margin = Mm(39), Mm(20)
    page.header_distance, page.footer_distance = Mm(13), Mm(9)
    width = page.page_width - page.left_margin - page.right_margin
    normal = doc.styles["Normal"]
    normal.font.name = "Arial"
    normal.font.size = Pt(layout["body_size_pt"])
    normal.font.color.rgb = RGBColor(24, 36, 48)
    normal.paragraph_format.line_spacing = layout["line_spacing"]
    normal.paragraph_format.space_after = Pt(layout["paragraph_space_after_pt"])
    for style_name, size in (("Title", 21), ("Heading 1", 13), ("Heading 2", 11), ("Heading 3", 10.5)):
        style = doc.styles[style_name]
        style.font.name, style.font.size, style.font.bold = "Arial", Pt(size), True
        style.font.color.rgb = RGBColor(0, 0, 0)
        style.paragraph_format.space_before = Pt(8 if style_name != "Title" else 0)
        style.paragraph_format.space_after = Pt(4)
        style.paragraph_format.keep_with_next = True
        borders = style.element.get_or_add_pPr().find(qn("w:pBdr"))
        if borders is not None:
            borders.getparent().remove(borders)
    header = word_table(page.header, width, (42, 29, 29), 2, accent)
    page.header.paragraphs[0]._p.getparent().remove(page.header.paragraphs[0]._p)
    cell_text(header.cell(0, 0).merge(header.cell(0, 1)), metadata.get("short_title") or metadata["title"], 10, True)
    cell = header.cell(0, 2)
    if brand.get("logo"):
        paragraph = cell_text(cell, "", alignment=WD_ALIGN_PARAGRAPH.CENTER)
        paragraph.add_run().add_picture(str(pathsafe(source.parent, brand["logo"])), height=Mm(10))
    else:
        cell_text(cell, brand["entity"], 9.5, True, WD_ALIGN_PARAGRAPH.CENTER)
    for cell, label in zip(header.rows[1].cells, (f"Actualización {updated}", f'Versión {metadata["version"]}', "Página ")):
        cell_text(cell, label, 9, alignment=WD_ALIGN_PARAGRAPH.CENTER)
    paging = header.cell(1, 2).paragraphs[0]
    page_field(paging, "PAGE")
    paging.add_run(" de ").font.size = Pt(9)
    page_field(paging, "NUMPAGES")
    footer = page.footer.paragraphs[0]
    footer.style = normal
    footer.paragraph_format.tab_stops.add_tab_stop(width, WD_TAB_ALIGNMENT.RIGHT)
    footer.paragraph_format.space_after = Pt(0)
    footer.add_run(f'{brand.get("unit") or brand["entity"]}\t{metadata["code"]} · {metadata["status"]}').font.size = Pt(9)

    doc.add_paragraph(metadata["title"], "Title")
    if metadata.get("subtitle"):
        doc.add_paragraph(metadata["subtitle"])
    for index, section in enumerate(spec["sections"]):
        heading = doc.add_heading(labels[section["id"]], level=section.get("level", 1))
        heading.paragraph_format.page_break_before = index > 0 and section.get("new_page", False)
        bookmark(heading, anchors[section["id"]])
        for block in section.get("blocks", []):
            kind = block["type"]
            if kind == "paragraph":
                paragraph = doc.add_paragraph()
                if block.get("indent") is not False:
                    paragraph.paragraph_format.first_line_indent = Mm(layout["first_line_indent_mm"])
                for run in block.get("runs", [{"text": block.get("text", "")}]):
                    add_text(paragraph, run["text"], labels, anchors, run.get("bold"), run.get("italic"))
            elif kind == "list":
                style = "List Number" if block.get("ordered") else "List Bullet"
                for item in block["items"]:
                    add_text(doc.add_paragraph(style=style), item, labels, anchors)
            elif kind == "table":
                caption = doc.add_paragraph(labels[block["id"]], "Caption")
                caption.paragraph_format.keep_with_next = True
                bookmark(caption, anchors[block["id"]])
                headers = block["headers"]
                weights = block.get("widths") or [1] * len(headers)
                require(headers and len(weights) == len(headers) and all(float(w) > 0 for w in weights),
                        f"Anchos de tabla no válidos: {block['id']}")
                rows = block["rows"]
                require(all(len(row) == len(headers) for row in rows), f"Fila incompleta: {block['id']}")
                table = word_table(doc, width, [float(w) for w in weights], len(rows) + 1, "D9D9D9")
                table.rows[0]._tr.get_or_add_trPr().append(element("tblHeader"))
                for i, row in enumerate([headers, *rows]):
                    for cell, value in zip(table.rows[i].cells, row):
                        paragraph = cell_text(cell, "", 9.5)
                        add_text(paragraph, value, labels, anchors, bold=i == 0)
                        for run in paragraph.runs:
                            run.font.size = Pt(9.5)
                        if i == 0:
                            cell._tc.get_or_add_tcPr().append(element("shd", fill="E8EFF6"))
                if block.get("source"):
                    add_text(doc.add_paragraph(style="Caption"), block["source"], labels, anchors)
            elif kind == "pagebreak":
                doc.add_page_break()
            else:
                raise ValueError(f"Bloque no admitido en acta DOCX: {kind}")
    output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    build_acta_docx(args.source, args.output)
