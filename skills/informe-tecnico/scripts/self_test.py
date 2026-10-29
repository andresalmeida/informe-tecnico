#!/usr/bin/env python3
"""Exercise pagination changes, continuation, profiles and failure behavior."""
import copy
import json
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw
from pypdf import PdfReader

from build_report import compile_report
from check_report import check, aligned_header


def table_by_id(spec, key):
    return next(block for section in spec["sections"] for block in section.get("blocks",[])
                if block.get("id")==key)


def main():
    example = Path(__file__).resolve().parents[1]/"assets"/"ejemplo.json"
    spec = json.loads(example.read_text())
    # A published catalog number must survive an insertion before its table.
    table_by_id(spec,"campos")["number"] = "136"
    checks = []
    with tempfile.TemporaryDirectory(prefix="informe-tecnico-") as temp:
        root = Path(temp)
        # Preserve relative figure paths when materializing specifications in temp.
        import shutil
        shutil.copytree(example.parent/"diagrams",root/"diagrams")
        def build(name, value):
            source, pdf = root/f"{name}.json", root/f"{name}.pdf"
            source.write_text(json.dumps(value,ensure_ascii=False))
            result = compile_report(source,pdf)
            validation = check(pdf)
            assert validation["ok"], validation
            # Inspect printed coordinates: opposite edges and the same baseline.
            import pdfplumber
            with pdfplumber.open(pdf) as printed:
                for page in printed.pages:
                    words = [w for w in page.extract_words() if w["top"] > page.height-18*72/25.4]
                    left = [w for w in words if w["x0"] < page.width/2]
                    right = [w for w in words if w["x0"] >= page.width/2]
                    assert left and right
                    assert abs(min(w["x0"] for w in left)-21*72/25.4) < .3
                    assert abs(max(w["x1"] for w in right)-(page.width-21*72/25.4)) < .3
                    assert abs(min(w["top"] for w in left)-min(w["top"] for w in right)) < .3
            return result,pdf

        baseline,pdf = build("base",spec)
        baseline_pages = {e["id"]:e["page"] for e in baseline["entries"]}
        text = [p.extract_text(extraction_mode="layout") for p in PdfReader(pdf).pages]
        continuation = [i+1 for i,t in enumerate(text) if "Campos y controles de la fuente documental" in t
                        and "Código" in t and "Definición" in t]
        assert len(continuation)>=2, continuation
        checks.append({"case":"table-continuation","pages":continuation})

        # Recreate the reported broken geometry and ensure the checker rejects it.
        from reportlab.pdfgen.canvas import Canvas
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import mm
        import pdfplumber
        bad_header = root/"misaligned-header.pdf"
        canvas = Canvas(str(bad_header),pagesize=A4)
        x,w = 21*mm,A4[0]-42*mm
        top = A4[1]-17*mm
        canvas.line(x+w*.71,top-20*mm,x+w*.71,top)
        canvas.line(x+w*.70,top-30*mm,x+w*.70,top-20*mm)
        canvas.line(x+w*.42,top-30*mm,x+w*.42,top-20*mm)
        canvas.save()
        with pdfplumber.open(bad_header) as broken:
            assert not aligned_header(broken.pages[0])
        checks.append({"case":"misaligned-header","rejected":True})

        changed = copy.deepcopy(spec)
        inserted = [{"id":f"extra-{i}","title":f"Sección de prueba para navegación {i:02d}",
                     "blocks":[{"type":"paragraph","text":"Contenido sintético para comprobar expansión del índice y desplazamiento de destinos."}]} for i in range(45)]
        changed["sections"][0:0] = inserted
        changed["sections"][0]["blocks"].append({"type":"paragraph","text":"Referencia de prueba: {{ref:campos}}."})
        changed["sections"][0]["blocks"].append({"type":"table","id":"ceros","title":"Conservación de valores", "number":"X-01",
            "headers":["Código","Texto"],"rows":[["0007","Ñandú, información y acción"]]})
        changed["changes"].append({"version":"0.3","date":"2026-10-28","summary":"Revisión sintética para probar índices.","author":"Prueba","affects":["campos"]})
        changed["document"]["version"] = "0.3"
        updated,updated_pdf = build("expanded",changed)
        new_pages = {e["id"]:e["page"] for e in updated["entries"]}
        assert updated["pages"]>baseline["pages"]
        assert new_pages["campos"]>baseline_pages["campos"]
        assert updated["labels"]["campos"].startswith("Tabla 136.")
        updated_text = " ".join(p.extract_text() for p in PdfReader(updated_pdf).pages)
        assert "0007" in updated_text and "Ñandú" in updated_text
        checks.append({"case":"expanded-index-and-cross-reference","before":baseline_pages["campos"],
                       "after":new_pages["campos"],"passes":updated["passes"]})

        profile = copy.deepcopy(spec)
        profile["brand"].update({"entity":"Organización de prueba","accent":"#EFE7D0",
                                  "frame":True,"border":1.1,"logo":"test-logo.png"})
        profile["document"].update({"paper":"Letter","status":"En revisión"})
        logo = Image.new("RGB",(300,100),"white")
        ImageDraw.Draw(logo).text((30,35),"TEST",fill="black")
        logo.save(root/"test-logo.png")
        variant,_ = build("profile",profile)
        assert variant["paper"] == "Letter"
        assert any(asset["path"]=="test-logo.png" for asset in variant["assets"])
        checks.append({"case":"letter-light-accent-frame-logo","pages":variant["pages"]})

        # Measure the PDF, rather than checking style variable values or wording.
        apa = {"schema_version":1, "brand":copy.deepcopy(spec["brand"]),
               "document":copy.deepcopy(spec["document"]),
               "changes":[{"version":"1.0","date":"2026-10-28","summary":"Prueba sintética.","author":"Prueba"}],
               "format":{"profile":"institucional-apa"},
               "sections":[{"id":"medidas","title":"Geometría de párrafos","blocks":[
                   {"type":"paragraph","text":"SANGRIA_INICIAL "+"El sistema conserva las relaciones entre datos y permite consultar los resultados de la operación. "*3},
                   {"type":"reference","runs":[{"text":"REFERENCIA_INICIAL. (2026). "},
                       {"text":"Título de referencia extenso para comprobar cursiva y sangría francesa en varias líneas de texto de la bibliografía.","italic":True},
                       {"text":" Editorial de prueba con información adicional de localización documental."}]},
                   {"type":"quotation","text":"CITA_INICIAL "+"Este contenido es sintético y sirve exclusivamente para medir la geometría del bloque impreso. "*4+
                    "\n\nCITA_SEGUNDA "+"El párrafo adicional conserva la sangría del bloque y añade sangría en su primera línea. "*2,
                    "citation":"(Documento de prueba, 2026, p. 1)"},
                   {"type":"figure","id":"imagen-apa","title":"Ejemplo de imagen","path":"test-logo.png", "max_height_mm":20},
                   {"type":"table","id":"tabla-apa","title":"Ejemplo de tabla","headers":["Campo","Valor"],
                    "rows":[[str(i),"Control de continuidad de tabla"] for i in range(36)],"source":"Datos sintéticos."},
               ]}]}
        measured, measured_pdf = build("apa",apa)
        def paragraph_lines(page, marker):
            words = page.extract_words()
            start = next(w for w in words if w["text"].startswith(marker))
            lines = {}
            for w in words:
                top = round(w["top"],1)
                if start["top"]-.1 <= w["top"] < start["top"]+65:
                    lines.setdefault(top,[]).append(w)
            return [min(ws,key=lambda w:w["x0"]) for _,ws in sorted(lines.items())]
        with pdfplumber.open(measured_pdf) as rendered:
            assert any(w["text"] == "Versión" for w in rendered.pages[1].extract_words()), "History header split inside a word"
            for marker, first, continuation in [("SANGRIA_INICIAL",36,0),("REFERENCIA_INICIAL",0,36),
                                                 ("CITA_INICIAL",36,36),("CITA_SEGUNDA",72,36)]:
                page = next(pg for pg in rendered.pages if marker in (pg.extract_text() or ""))
                lines = paragraph_lines(page,marker)
                assert len(lines)>=2
                assert abs(lines[0]["x0"]-21*mm-first)<.3, (marker,lines)
                assert abs(lines[1]["x0"]-21*mm-continuation)<.3, (marker,lines)
                assert abs(lines[1]["top"]-lines[0]["top"]-22)<.3, (marker,lines)
            image_page = rendered.pages[next(x["page"] for x in measured["entries"] if x["id"]=="imagen-apa")-1]
            title = next(w for w in image_page.extract_words() if w["text"]=="Ejemplo")
            assert title["top"] < image_page.images[0]["top"]
            assert any("Oblique" in c["fontname"] for pg in rendered.pages for c in pg.chars)
            continued = [pg for pg in rendered.pages if "Ejemplo de tabla" in (pg.extract_text() or "")]
            assert len(continued)>=2
        checks.append({"case":"apa-rendered-indent-spacing-italics-caption-and-table-continuation",
                       "indent_pt":36,"line_step_pt":22,"pages":measured["pages"]})

        # The custom-font path must embed true italic variants, not fake them.
        import reportlab
        font_dir = Path(reportlab.__file__).parent/"fonts"
        (root/"fonts").mkdir()
        fonts = {"normal":"Vera.ttf","bold":"VeraBd.ttf","italic":"VeraIt.ttf","bold_italic":"VeraBI.ttf"}
        for filename in fonts.values(): shutil.copy2(font_dir/filename,root/"fonts"/filename)
        custom = copy.deepcopy(apa)
        custom["brand"]["fonts"] = {role:"fonts/"+filename for role,filename in fonts.items()}
        custom_manifest, custom_pdf = build("apa-ttf",custom)
        assert sum(a["path"].endswith(".ttf") for a in custom_manifest["assets"])==4
        with pdfplumber.open(custom_pdf) as embedded:
            assert any("Oblique" in c["fontname"] for pg in embedded.pages for c in pg.chars)
        checks.append({"case":"apa-four-custom-font-variants","embedded":4})

        operations = {"schema_version":1, "brand":copy.deepcopy(spec["brand"]),
                      "document":copy.deepcopy(spec["document"]), "format":{"profile":"institucional-apa"},
                      "changes":[{"version":"1.0","date":"2026-10-29","summary":"Muestra sintética.",
                                  "author":"Prueba","affects":["operar"]}],
                      "sections":[{"id":"operacion","title":"Operación de prueba","blocks":[
                          {"type":"paragraph","text":"Consulte {{ref:operar}} y {{ref:finalizar}}."},
                          {"type":"notice","level":"note","text":"NOTA_TEST Aclaración de prueba."},
                          {"type":"procedure","id":"operar","title":"Operar el equipo de prueba",
                           "role":"Operador de prueba", "prerequisites":["Equipo simulado disponible."],
                           "steps":[{"action":f"ACCION_{i:02d} Seleccione el control de prueba y confirme la selección.",
                                     "expected":f"RESULTADO_{i:02d} El indicador muestra el estado seleccionado y el panel conserva el identificador del equipo de prueba.",
                                     "on_failure":"Conserve el estado actual y revise la selección antes de continuar."}
                                    for i in range(20)]},
                          {"type":"procedure","id":"finalizar","title":"Finalizar la consulta",
                           "steps":[{"action":"FIN_ACCION Pulse Cerrar.","expected":"FIN_RESULTADO La vista inicial queda visible."}]}]}]}
        operation_steps = operations["sections"][0]["blocks"][2]["steps"]
        operation_steps[4]["notice"] = {"level":"warning","title":"Equipo simulado",
                                        "text":"ADVERTENCIA_TEST Desconecte el equipo antes de retirar la cubierta."}
        operation_steps[8]["notice"] = {"level":"caution","text":"PRECAUCION_TEST Conserve los datos antes de sustituirlos."}
        operation_steps[0]["action"] += " El rótulo de prueba contiene <b>literal</b>."
        operation_steps[1]["expected"] += " Continúe con {{ref:finalizar}}."
        for profile_name in ("institucional-apa", "institucional"):
            operations["format"]["profile"] = profile_name
            operation_manifest, operation_pdf = build("procedures-"+profile_name, operations)
            destinations = {e["id"]:e["page"] for e in operation_manifest["entries"]}
            assert operation_manifest["labels"]["operar"].startswith("Procedimiento 1.")
            assert operation_manifest["labels"]["finalizar"].startswith("Procedimiento 2.")
            with pdfplumber.open(operation_pdf) as rendered:
                texts = [pg.extract_text() or "" for pg in rendered.pages]
                assert "<b>literal</b>" in " ".join(texts), "Input markup must remain literal"
                step_pages = []
                for i in range(20):
                    action_page = next(n for n,t in enumerate(texts) if f"ACCION_{i:02d}" in t)
                    expected_page = next(n for n,t in enumerate(texts) if f"RESULTADO_{i:02d}" in t)
                    assert action_page == expected_page, (profile_name,i,action_page,expected_page)
                    step_pages.append(action_page)
                assert len(set(step_pages)) >= 2, "Procedure must exercise page continuation"
                assert destinations["operar"] == step_pages[0]+1
                for marker, action in [("ADVERTENCIA_TEST","ACCION_04"),("PRECAUCION_TEST","ACCION_08")]:
                    page_n = next(n for n,t in enumerate(texts) if marker in t)
                    assert action in texts[page_n], "Notice separated from its action"
                    words = rendered.pages[page_n].extract_words()
                    notice_y = next(w["top"] for w in words if w["text"] == marker)
                    action_y = next(w["top"] for w in words if w["text"] == action)
                    assert notice_y < action_y
                for marker, label in [("NOTA_TEST","Nota."),("ADVERTENCIA_TEST","Advertencia:"),
                                      ("PRECAUCION_TEST","Precaución.")]:
                    assert any(marker in t and label in t for t in texts)
                # Body spacing also applies inside the operational blocks.
                page = rendered.pages[step_pages[1]]
                lines = paragraph_lines(page,"RESULTADO_01")
                assert abs(lines[1]["top"]-lines[0]["top"]-(22 if profile_name.endswith("apa") else 14.5)) < .3
            checks.append({"case":"procedures-navigation-pagination-notices-"+profile_name,
                           "step_pages":[p+1 for p in sorted(set(step_pages))], "pages":operation_manifest["pages"]})

        for name, mutate in [
            ("procedure-missing-expected",lambda b: b["steps"][0].pop("expected")),
            ("procedure-empty-action",lambda b: b["steps"][0].update(action="  ")),
            ("procedure-empty-steps",lambda b: b.update(steps=[])),
            ("procedure-executed-status",lambda b: b["steps"][0].update(checked=True)),
            ("notice-unknown-level",lambda b: b["steps"][4]["notice"].update(level="danger")),
            ("notice-empty-text",lambda b: b["steps"][4]["notice"].update(text=" ")),
            ("procedure-duplicate-id",lambda b: b.update(id="operacion")),
            ("procedure-unknown-reference",lambda b: b["steps"][0].update(expected="{{ref:missing-step}}")),
        ]:
            invalid = copy.deepcopy(operations)
            mutate(invalid["sections"][0]["blocks"][2])
            source = root/f"{name}.json"
            source.write_text(json.dumps(invalid))
            try:
                compile_report(source,root/f"{name}.pdf")
            except ValueError:
                checks.append({"case":name,"rejected":True})
            else:
                raise AssertionError(f"Expected rejection: {name}")

        for name, mutate in [
            ("unknown-reference",lambda x: x["sections"][0]["blocks"].append({"type":"paragraph","text":"{{ref:missing}}"})),
            ("duplicate-id",lambda x: x["sections"].append(copy.deepcopy(x["sections"][0]))),
            ("oversize-row",lambda x: table_by_id(x,"campos")["rows"].append(["LONG","Campo","Texto extenso "*3000,"Texto"])),
            ("unknown-format-profile",lambda x: x.update(format={"profile":"apa-inexistente"})),
            ("negative-indent",lambda x: x.update(format={"profile":"institucional-apa","first_line_indent_mm":-3})),
            ("missing-quote-citation",lambda x: x["sections"][0]["blocks"].append({"type":"quotation","text":"Palabras sintéticas de prueba "*20})),
            ("missing-italic-font",lambda x: (x.update(format={"profile":"institucional-apa"}),
                 x["brand"].update(fonts={"normal":"fonts/Vera.ttf","bold":"fonts/VeraBd.ttf"}))),
        ]:
            invalid=copy.deepcopy(spec)
            mutate(invalid)
            source=root/f"{name}.json"
            source.write_text(json.dumps(invalid))
            failed=False
            try:
                compile_report(source,root/f"{name}.pdf")
            except (ValueError, KeyError) as exc:
                failed=True
            except Exception as exc:
                from reportlab.platypus import LayoutError
                if isinstance(exc,LayoutError):
                    failed=True
                else:
                    raise
            assert failed, f"Expected rejection: {name}"
            checks.append({"case":name,"rejected":True})
    print(json.dumps({"ok":True,"checks":checks},ensure_ascii=False,indent=2))


if __name__ == "__main__":
    main()
