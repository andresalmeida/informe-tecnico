#!/usr/bin/env python3
"""Structural PDF checks; visual and technical review remain necessary."""
import argparse
import hashlib
import json
import re
from datetime import date
from pathlib import Path

import pdfplumber
from pypdf import PdfReader


def aligned_header(page):
    """Read actual PDF geometry; entity and page cells must share a full divider."""
    unit = 72/25.4
    top, joint, bottom = 17*unit, 37*unit, 47*unit
    tolerance = .25
    vertical = [line for line in page.lines if abs(line["x0"]-line["x1"])<tolerance]
    # The shared divider must be one continuous line across both header rows.
    through = [line for line in vertical if abs(line["top"]-top)<tolerance
               and abs(line["bottom"]-bottom)<tolerance
               and 21*unit+tolerance < line["x0"] < page.width-21*unit-tolerance]
    lower_only = [line for line in vertical if abs(line["top"]-joint)<tolerance
                  and abs(line["bottom"]-bottom)<tolerance]
    return (len(through)==1 and len(lower_only)==1
            and lower_only[0]["x0"] < through[0]["x0"])


def check(pdf):
    manifest = json.loads(pdf.with_suffix(".manifest.json").read_text())
    reader = PdfReader(pdf)
    errors = []
    def expect(condition, message):
        if not condition:
            errors.append(message)
    expect(hashlib.sha256(pdf.read_bytes()).hexdigest() == manifest["pdf_sha256"],
           "El PDF no corresponde al manifiesto")
    n = len(reader.pages)
    expect(n == manifest["pages"], "Total distinto al manifiesto")
    expect(len(manifest["entries"]) == len(manifest["labels"]), "Faltan destinos de navegación")
    expect(len({e["id"] for e in manifest["entries"]}) == len(manifest["entries"]), "Destinos duplicados")
    expected_size = (595.276,841.89) if manifest["paper"] == "A4" else (612,792)
    texts = []
    m = manifest["document"]
    with pdfplumber.open(pdf) as document:
        for i, page in enumerate(document.pages,1):
            text = page.extract_text() or ""
            texts.append(text)
            expect(bool(text.strip()), f"Página {i} vacía")
            expect(f"Página {i} de {n}" in text, f"Paginación incorrecta en {i}")
            expect(f'Versión: {m["version"]}' in text, f"Versión ausente en {i}")
            expect(date.fromisoformat(m["date"]).strftime("%d/%m/%Y") in text, f"Fecha ausente en {i}")
            expect(m["code"] in text and m["status"] in text, f"Código/estado ausente en {i}")
            expect(abs(page.width-expected_size[0])<1 and abs(page.height-expected_size[1])<1,
                   f"Papel incorrecto en {i}")
            expect(aligned_header(page), f"Desfase de retícula de cabecera en {i}")
            expect("{{ref:" not in text and "Placeholder for table of contents" not in text,
                   f"Referencia sin resolver en {i}")
            outside = [c for c in page.chars if c.get("text","").strip() and
                       (c["x0"] < 20*72/25.4-1 or c["x1"] > page.width-20*72/25.4+1 or
                        c["top"] < 5*72/25.4 or c["bottom"] > page.height-5*72/25.4)]
            expect(not outside, f"Texto fuera de margen en {i}")
            small = [c for c in page.chars if c.get("text","").strip() and c["size"] < 8.4]
            expect(not small, f"Texto menor a 8,5 pt en {i}")
    for entry in manifest["entries"]:
        page_n = entry["page"]
        expect(1 <= page_n <= n, f'Destino fuera de rango: {entry["id"]}')
        if 1 <= page_n <= n:
            normalized = re.sub(r"\s+"," ",texts[page_n-1])
            expect(re.sub(r"\s+"," ",entry["label"]) in normalized,
                   f'Título ausente en destino: {entry["id"]}')
        index_pattern = (re.escape(re.sub(r"\s+", " ", entry["label"])) +
                         r"(?:\s*\.)+\s*" + str(page_n) + r"\b")
        index_text = re.sub(r"\s+", " ", " ".join(texts))
        expect(re.search(index_pattern,index_text) is not None,
               f'Página impresa de índice incorrecta: {entry["id"]}')
    outlined = []
    def visit(items):
        for item in items:
            if isinstance(item,list):
                visit(item)
            else:
                outlined.append((item.title,reader.get_destination_page_number(item)+1))
    visit(reader.outline)
    for entry in manifest["entries"]:
        expect((entry["label"],entry["page"]) in outlined, f'Marcador incorrecto: {entry["id"]}')
    links = 0
    for i, page in enumerate(reader.pages,1):
        for ref in page.get("/Annots",[]):
            annotation = ref.get_object()
            if annotation.get("/Subtype") != "/Link":
                continue
            dest = annotation.get("/Dest")
            if dest is not None:
                links += 1
                expect(isinstance(dest,list) and len(dest)>0, f"Enlace interno inválido en {i}")
                if isinstance(dest,list) and dest:
                    expect(any(dest[0] == pg.indirect_reference for pg in reader.pages),
                           f"Enlace sin página de destino en {i}")
    expect(links >= len(manifest["entries"]), "Faltan enlaces de índices")
    return {"ok":not errors,"pages":n,"entries":len(manifest["entries"]),
            "internal_links":links,"errors":errors,
            "limits":"Requiere revisión visual; no verifica hechos, semántica de tablas ni PDF/UA."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf",type=Path)
    args = parser.parse_args()
    result = check(args.pdf)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    raise SystemExit(0 if result["ok"] else 1)
