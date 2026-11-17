#!/usr/bin/env python3
"""Exercise pagination changes, continuation, profiles and failure behavior."""
import copy
import json
import sys
import tempfile
from pathlib import Path

_scripts = Path(__file__).resolve().parents[1] / "skills" / "informe-tecnico" / "scripts"
if str(_scripts) not in sys.path:
    sys.path.insert(0, str(_scripts))

import deps
deps.check(('reportlab', 'pypdf', 'pdfplumber', 'PIL'), 'self_test.py')

from PIL import Image, ImageDraw
from pypdf import PdfReader

from build_report import compile_report
from check_report import check, aligned_header


def table_by_id(spec, key):
    return next(block for section in spec["sections"] for block in section.get("blocks",[])
                if block.get("id")==key)


def main():
    example = Path(__file__).resolve().parents[1]/"skills"/"informe-tecnico"/"assets"/"ejemplo.json"
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

        for kind, expected_pages in (("acta-entrega", 4), ("acta-reunion", 2)):
            sample = json.loads((example.parent/f"ejemplo-{kind}.json").read_text())
            acta, acta_pdf = build(kind, sample)
            assert acta["pages"] == expected_pages
            assert check(acta_pdf)["internal_links"] > 0
            checks.append({"case":kind, "pages":acta["pages"]})

        meeting_destinations = {entry["id"]: entry["page"] for entry in acta["entries"]}
        assert meeting_destinations["agenda"] == 1
        assert meeting_destinations["detalle"] == meeting_destinations["acuerdos"] == meeting_destinations["matriz-casos"] == 2
        table_by_id(sample, "acuerdos")["rows"].extend(
            [f"A-{i:02d}", "T02", "Comprobar el resultado de la revisión asignada.", "Nora Vidal", "06/11/2026"]
            for i in range(3, 51)
        )
        extended, extended_pdf = build("acta-reunion-extensa", sample)
        pages = [page.extract_text() for page in PdfReader(extended_pdf).pages]
        assert extended["pages"] > 1
        assert sum("Registro de acuerdos" in page for page in pages) >= 2
        assert any("A-50" in page and "Registro de acuerdos" in page for page in pages)
        checks.append({"case":"acta-reunion-continuation", "pages":extended["pages"]})

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
        assert updated["labels"]["campos"].startswith("Tabla 136 ")  # APA labels carry no period
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
                assert abs(lines[1]["top"]-lines[0]["top"]-16.5)<.3, (marker,lines)  # 1.5 x 11 pt
            image_page = rendered.pages[next(x["page"] for x in measured["entries"] if x["id"]=="imagen-apa")-1]
            title = next(w for w in image_page.extract_words() if w["text"]=="Ejemplo")
            assert title["top"] < image_page.images[0]["top"]
            assert any("Oblique" in c["fontname"] for pg in rendered.pages for c in pg.chars)
            continued = [pg for pg in rendered.pages if "Ejemplo de tabla" in (pg.extract_text() or "")]
            assert len(continued)>=2
        checks.append({"case":"apa-rendered-indent-spacing-italics-caption-and-table-continuation",
                       "indent_pt":36,"line_step_pt":16.5,"pages":measured["pages"]})

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
                assert abs(lines[1]["top"]-lines[0]["top"]-(16.5 if profile_name.endswith("apa") else 14.5)) < .3
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
            ("unknown-document-kind",lambda x: x["document"].update(kind="acta-inexistente")),
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

        # ---- Informe de factibilidad: diseño de formulario, elecciones y figura opcional ----
        feasibility_source = json.loads((example.parent/"ejemplo-informe-factibilidad.json").read_text())

        def find_block(source, block_id=None, section_id=None, kind=None):
            for section in source["sections"]:
                if section_id and section["id"] != section_id:
                    continue
                for item in section.get("blocks", []):
                    if (block_id and item.get("id") == block_id) or (kind and item["type"] == kind):
                        return item
            raise KeyError((block_id, section_id, kind))

        def choices(source):
            return [item for section in source["sections"] for b in section.get("blocks", [])
                    if b["type"] == "fields" for item in b["items"] if "options" in item]

        feasibility, feasibility_pdf = build("informe-factibilidad", feasibility_source)
        assert feasibility["pages"] == 6, feasibility["pages"]
        assert feasibility["document"]["kind"] == "informe-factibilidad"
        pages_of = {entry["id"]: entry["page"] for entry in feasibility["entries"]}
        expected_choices = choices(feasibility_source)
        assert len(expected_choices) == 3
        with pdfplumber.open(feasibility_pdf) as printed:
            texts = [pg.extract_text() or "" for pg in printed.pages]
            # One drawn cross per choice (each cross is two strokes) and one box per option.
            strokes = sum(1 for pg in printed.pages for line in pg.lines
                          if abs(line["x0"]-line["x1"]) > 1 and abs(line["top"]-line["bottom"]) > 1)
            boxes = sum(1 for pg in printed.pages for rect in pg.rects
                        if abs(rect["width"]-9) < .3 and abs(rect["height"]-9) < .3)
            assert strokes == 2*len(expected_choices), strokes
            assert boxes == sum(len(item["options"]) for item in expected_choices), boxes
            # The marked option is printed in bold and the others are not. Option text starts
            # at the same x in every one-column grid, so each printed line is read from there.
            lines = {}
            for number, pg in enumerate(printed.pages):
                for c in pg.chars:
                    if abs(c["size"]-11) < .1 and c["x0"] > 190:  # table text at body size
                        lines.setdefault((number, round(c["top"])), []).append(c)
            printed_lines = [("".join(c["text"] for c in sorted(chars, key=lambda c: c["x0"])),
                              all("Bold" in c["fontname"] for c in chars)) for chars in lines.values()]
            for item in expected_choices:
                for option in item["options"]:
                    found = [bold for text, bold in printed_lines if text == option]
                    assert found == [option == item["selected"]], (option, found)
            # A table or grid that fits on a page is never cut, and its title stays with its rows.
            for table_id, last_cell in (("humanos", "Otro: responsable de operaciones"), ("tecnicos", "Otro: certificado TLS"),
                                        ("externos", "Especialista en seguridad"), ("fases", "Implementación y despliegue"),
                                        ("firmas", "Aprobado por")):
                assert last_cell in texts[pages_of[table_id]-1], (table_id, pages_of[table_id])
            assert "Histórico de revisiones" in texts[-1] and "Marta Quiroga" in texts[-1]
            # The closing splits from its history only when more than 40 % of the page would stay empty.
            assert feasibility["pages"]-1 <= pages_of["aprobaciones"] <= feasibility["pages"], "Las firmas cierran el cuerpo"
        assert check(feasibility_pdf)["internal_links"] >= 2
        checks.append({"case": "informe-factibilidad", "pages": feasibility["pages"], "choices": len(expected_choices)})

        # Without the figure the type compiles too, once its reference is removed with it.
        bare = copy.deepcopy(feasibility_source)
        for section in bare["sections"]:
            section["blocks"] = [b for b in section.get("blocks", []) if b["type"] != "figure"]
        impact = find_block(bare, section_id="impacto", kind="paragraph")
        impact["text"] = impact["text"].split(" Los componentes nuevos")[0]
        no_figure, _ = build("informe-factibilidad-sin-figura", bare)
        assert "arquitectura" not in no_figure["labels"] and not no_figure["assets"]
        assert 4 <= no_figure["pages"] <= feasibility["pages"], no_figure["pages"]
        checks.append({"case": "informe-factibilidad-sin-figura", "pages": no_figure["pages"]})

        # Choosing "No" in the external resources grid removes the profile table with it.
        internal = copy.deepcopy(feasibility_source)
        external_grid = next(item for item in choices(internal) if item["label"] == "Recursos externos")
        external_grid["selected"] = external_grid["options"][0]
        for section in internal["sections"]:
            section["blocks"] = [b for b in section.get("blocks", []) if b.get("id") != "externos"]
        no_external, _ = build("informe-factibilidad-sin-externos", internal)
        assert "externos" not in no_external["labels"], no_external["labels"]
        assert 4 <= no_external["pages"] <= 6, no_external["pages"]
        checks.append({"case": "informe-factibilidad-sin-externos", "pages": no_external["pages"]})

        # Identity, code prefix and signers are configurable, with and without a logo.
        for with_logo in (False, True):
            custom = copy.deepcopy(feasibility_source)
            custom["brand"].update(entity="Organización de prueba", unit="Oficina de Proyectos", accent="#7A2E1D")
            custom["document"].update(code="ACME-FAC-07", paper="Letter", status="En revisión")
            find_block(custom, "firmas")["rows"][0][:2] = ["Elaborado por", "Persona de prueba\nCargo de prueba"]
            if with_logo:
                custom["brand"]["logo"] = "test-logo.png"
            personalized, personalized_pdf = build("informe-factibilidad-"+("logo" if with_logo else "sin-logo"), custom)
            first_page = PdfReader(personalized_pdf).pages[0].extract_text()
            assert personalized["paper"] == "Letter" and "ACME-FAC-07" in first_page
            assert "Oficina de Proyectos" in first_page and "Persona de prueba" in " ".join(
                p.extract_text() for p in PdfReader(personalized_pdf).pages)
            assert ("Organización de prueba" in first_page) != with_logo
            assert any(a["path"] == "test-logo.png" for a in personalized["assets"]) == with_logo
            checks.append({"case": "informe-factibilidad-personalizado", "logo": with_logo, "pages": personalized["pages"]})

        # show_changes prints the history of a compact type; the report already has its own.
        entrega = json.loads((example.parent/"ejemplo-acta-entrega.json").read_text())
        entrega["document"]["show_changes"] = True
        history, history_pdf = build("acta-entrega-historial", entrega)
        assert "Histórico de revisiones" in " ".join(p.extract_text() for p in PdfReader(history_pdf).pages)
        checks.append({"case": "show-changes", "pages": history["pages"]})

        def rejected(name, source):
            path = root/f"{name}.json"
            path.write_text(json.dumps(source, ensure_ascii=False))
            try:
                compile_report(path, root/f"{name}.pdf")
            except ValueError:
                checks.append({"case": name, "rejected": True})
            else:
                raise AssertionError(f"Expected rejection: {name}")

        def feasibility_variant(mutate):
            variant = copy.deepcopy(feasibility_source)
            mutate(variant)
            return variant

        def without_choices(x):
            for item in choices(x):
                item["value"] = item.pop("selected")
                del item["options"]

        viability = lambda x: choices(x)[0]
        reference = lambda x: find_block(x, section_id="referencia", kind="fields")
        for name, mutate in [
            ("viabilidad-fuera-de-las-opciones", lambda x: viability(x).update(selected="Viable")),
            ("viabilidad-sin-marca", lambda x: viability(x).pop("selected")),
            ("viabilidad-nula", lambda x: viability(x).update(selected=None)),
            ("viabilidad-con-dos-marcas", lambda x: viability(x).update(selected=["Factible", "No factible"])),
            ("opciones-repetidas", lambda x: viability(x).update(options=["Factible", "Factible", "No factible"])),
            ("opciones-con-una-sola", lambda x: viability(x).update(options=["Factible"], selected="Factible")),
            ("opciones-siete", lambda x: viability(x).update(options=[f"Opción {i}" for i in range(7)], selected="Opción 0")),
            ("opcion-vacia", lambda x: viability(x).update(options=["Factible", " "])),
            ("valor-y-opciones", lambda x: viability(x).update(value="Factible")),
            ("sin-ninguna-eleccion", without_choices),
            ("campos-clave-de-bloque", lambda x: reference(x).update(title="Ficha")),
            ("campos-clave-de-elemento", lambda x: reference(x)["items"][0].update(hint="Ayuda")),
            ("campos-columnas-tres", lambda x: reference(x).update(columns=3)),
            ("campos-columnas-booleano", lambda x: reference(x).update(columns=True)),
            ("campos-sin-elementos", lambda x: reference(x).update(items=[])),
            ("campos-diecisiete-elementos", lambda x: reference(x).update(
                items=[{"label": f"Campo {i}", "value": "Valor"} for i in range(17)])),
            ("campos-etiqueta-vacia", lambda x: reference(x)["items"][0].update(label=" ")),
            ("campos-valor-vacio", lambda x: reference(x)["items"][0].update(value="")),
            ("campos-sin-valor", lambda x: reference(x)["items"][0].pop("value")),
            ("campos-referencia-desconocida", lambda x: reference(x)["items"][0].update(value="{{ref:inexistente}}")),
            ("historial-no-booleano", lambda x: x["document"].update(show_changes="sí")),
        ]:
            rejected(name, feasibility_variant(mutate))
        informe = json.loads(example.read_text())
        informe["document"]["show_changes"] = True
        rejected("historial-en-informe", informe)

        # ---- Registro de requerimientos: elecciones en dos columnas, secciones opcionales y su regla propia ----
        registro_source = json.loads((example.parent/"ejemplo-registro-requerimientos.json").read_text())

        def printed_choice_lines(printed):
            """Option texts of every grid, one segment per cell, each with whether all its letters are bold."""
            segments = []
            for number, pg in enumerate(printed.pages):
                rows = {}
                for c in pg.chars:
                    if abs(c["size"]-11) < .1 and c["x0"] > 160:  # table text at body size
                        rows.setdefault((number, round(c["top"])), []).append(c)
                for chars in rows.values():
                    chars.sort(key=lambda c: c["x0"])
                    current = [chars[0]]
                    for c in chars[1:]:
                        if c["x0"]-current[-1]["x1"] > 8:  # a gap this wide separates two cells
                            segments.append(current)
                            current = []
                        current.append(c)
                    segments.append(current)
            return [("".join(c["text"] for c in segment), all("Bold" in c["fontname"] for c in segment))
                    for segment in segments]

        def marks_of(item):
            """The options a choice marks: one for a single choice, a list (possibly empty) for a multiple one."""
            return item["selected"] if item.get("multiple") else [item["selected"]]

        def assert_choices(pdf_path, source):
            expected = choices(source)
            with pdfplumber.open(pdf_path) as printed:
                strokes = sum(1 for pg in printed.pages for line in pg.lines
                              if abs(line["x0"]-line["x1"]) > 1 and abs(line["top"]-line["bottom"]) > 1)
                boxes = sum(1 for pg in printed.pages for rect in pg.rects
                            if abs(rect["width"]-9) < .3 and abs(rect["height"]-9) < .3)
                assert strokes == 2*sum(len(marks_of(item)) for item in expected), strokes
                assert boxes == sum(len(item["options"]) for item in expected), boxes
                lines = printed_choice_lines(printed)
                for item in expected:
                    for option in item["options"]:
                        found = [bold for text, bold in lines if text == option]
                        assert found == [option in marks_of(item)], (option, found)
            return len(expected)

        registro, registro_pdf = build("registro-requerimientos", registro_source)
        assert registro["pages"] == 2, registro["pages"]
        assert registro["document"]["kind"] == "registro-requerimientos"
        assert assert_choices(registro_pdf, registro_source) == 3
        registro_pages = {entry["id"]: entry["page"] for entry in registro["entries"]}
        with pdfplumber.open(registro_pdf) as printed:
            texts = [pg.extract_text() or "" for pg in printed.pages]
            # The signature table stays whole and on the last page, with the history after it.
            assert "Aprobado por" in texts[registro_pages["firmas"]-1] and "Pendiente" in texts[registro_pages["firmas"]-1]
            assert registro_pages["aprobaciones"] == registro["pages"], "Las firmas quedan en la última página"
            assert "Histórico de revisiones" in texts[-1]
            # The observations stay on the page of the assignment grid they follow.
            assert ("Asignado a" in texts[registro_pages["recepcion"]-1]
                    and "Observaciones iniciales." in texts[registro_pages["recepcion"]-1])
        assert check(registro_pdf)["internal_links"] >= 2
        checks.append({"case": "registro-requerimientos", "pages": registro["pages"], "choices": 3})

        # Optional parts disappear with no text left that names them, and the numbering closes up.
        without_extra = copy.deepcopy(registro_source)
        without_extra["sections"] = [x for x in without_extra["sections"] if x["id"] != "adicional"]
        no_extra, no_extra_pdf = build("registro-sin-informacion-adicional", without_extra)
        assert "adicional" not in no_extra["labels"] and no_extra["labels"]["recepcion"].startswith("3")
        assert "Documentos adjuntos" not in " ".join(p.extract_text() for p in PdfReader(no_extra_pdf).pages)
        assert no_extra["pages"] == 2, no_extra["pages"]
        checks.append({"case": "registro-sin-informacion-adicional", "pages": no_extra["pages"]})

        without_notes = copy.deepcopy(registro_source)
        reception = find_block(without_notes, section_id="recepcion", kind="paragraph")
        next(x for x in without_notes["sections"] if x["id"] == "recepcion")["blocks"].remove(reception)
        no_notes, no_notes_pdf = build("registro-sin-observaciones", without_notes)
        assert "Observaciones iniciales." not in " ".join(p.extract_text() for p in PdfReader(no_notes_pdf).pages)
        assert no_notes["pages"] == 2, no_notes["pages"]
        checks.append({"case": "registro-sin-observaciones", "pages": no_notes["pages"]})

        # A priority nobody has given is declared with its own marked option.
        pending = copy.deepcopy(registro_source)
        priority = next(item for item in choices(pending) if item["label"] == "Prioridad")
        priority.update(options=["Alta", "Media", "Baja", "Por confirmar"], selected="Por confirmar")
        pending_manifest, pending_pdf = build("registro-prioridad-por-confirmar", pending)
        assert assert_choices(pending_pdf, pending) == 3
        checks.append({"case": "registro-prioridad-por-confirmar", "pages": pending_manifest["pages"]})

        # Identity, code prefix, paper and signers are configurable, with and without a logo.
        for with_logo in (False, True):
            custom = copy.deepcopy(registro_source)
            custom["brand"].update(entity="Organización de prueba", unit="Oficina de Proyectos", accent="#7A2E1D")
            custom["document"].update(code="ACME-REQ-07", paper="Letter", status="En revisión")
            find_block(custom, "firmas")["rows"][0][:2] = ["Elaborado por", "Persona de prueba\nCargo de prueba"]
            if with_logo:
                custom["brand"]["logo"] = "test-logo.png"
            personalized, personalized_pdf = build("registro-"+("logo" if with_logo else "sin-logo"), custom)
            first_page = PdfReader(personalized_pdf).pages[0].extract_text()
            assert personalized["paper"] == "Letter" and "ACME-REQ-07" in first_page
            assert "Oficina de Proyectos" in first_page and "Persona de prueba" in " ".join(
                p.extract_text() for p in PdfReader(personalized_pdf).pages)
            assert ("Organización de prueba" in first_page) != with_logo
            assert any(a["path"] == "test-logo.png" for a in personalized["assets"]) == with_logo
            assert assert_choices(personalized_pdf, custom) == 3
            checks.append({"case": "registro-personalizado", "logo": with_logo, "pages": personalized["pages"]})

        # Each form kind states its own message when the source has no marked choice.
        def rejected_with(name, source, message):
            path = root/f"{name}.json"
            path.write_text(json.dumps(source, ensure_ascii=False))
            try:
                compile_report(path, root/f"{name}.pdf")
            except ValueError as error:
                assert message in str(error), (name, str(error))
                checks.append({"case": name, "rejected": True})
            else:
                raise AssertionError(f"Expected rejection: {name}")

        no_choices = copy.deepcopy(registro_source)
        without_choices(no_choices)
        rejected_with("registro-sin-ninguna-eleccion", no_choices, "registro-requerimientos requiere al menos una elección marcada")
        other_kind = copy.deepcopy(no_choices)
        other_kind["document"]["kind"] = "informe-factibilidad"
        rejected_with("factibilidad-sin-ninguna-eleccion", other_kind, "informe-factibilidad requiere una viabilidad marcada")
        for name, mutate in [
            ("registro-tipo-fuera-de-las-opciones", lambda x: choices(x)[0].update(selected="Hardware")),
            ("registro-prioridad-con-dos-marcas", lambda x: choices(x)[1].update(selected=["Alta", "Media"])),
        ]:
            variant = copy.deepcopy(registro_source)
            mutate(variant)
            rejected(name, variant)

        # ---- Títulos, numeración e índices opcionales de los tipos de formulario ----
        from build_report import title_case
        for written, printed in [
            ("definición de alcance", "Definición de Alcance"),
            ("Evaluación de factibilidad técnica y operativa", "Evaluación de Factibilidad Técnica y Operativa"),
            ("INFORMACIÓN DE REFERENCIA", "Información de Referencia"),
            ("Pruebas con API de pagos en iOS", "Pruebas con API de Pagos en iOS"),
            ("Anexo A", "Anexo A"),
            ("qué se evalúa: el alcance", "Qué se Evalúa: El Alcance"),
            ("Costo-beneficio de la opción v2", "Costo-beneficio de la Opción v2"),
            ("(opcional) criterios de aceptación", "(Opcional) Criterios de Aceptación"),
        ]:
            assert title_case(written) == printed, (written, title_case(written))
        checks.append({"case": "titulos-con-mayuscula-de-titulo", "samples": 8})

        # Every kind prints «1. Título» and «2.1. Título», the informe included.
        assert feasibility["labels"]["referencia"] == "1. Información de referencia", feasibility["labels"]["referencia"]
        assert feasibility["labels"]["impacto"] == "2.1. Impacto en procesos y sistemas existentes"
        assert feasibility["labels"]["tiempo"].startswith("5. ") and feasibility["labels"]["tiempo"].endswith("tiempo")
        first_label = next(iter(baseline["labels"].values()))
        assert first_label[:3] == "1. ", first_label
        first_page_text = PdfReader(feasibility_pdf).pages[0].extract_text()
        assert "Informe de factibilidad técnica y operativa" in first_page_text
        assert "1. Información de referencia" in first_page_text
        checks.append({"case": "numeracion-con-punto-en-todos-los-tipos"})

        # The optional indexes list every section, table and figure with the page where it is printed.
        complete_source = json.loads((example.parent/"ejemplo-informe-factibilidad-completo.json").read_text())
        complete, complete_pdf = build("informe-factibilidad-completo", complete_source)
        assert 6 <= complete["pages"] <= 8, complete["pages"]
        with pdfplumber.open(complete_pdf) as printed:
            first_page = printed.pages[0].extract_text()
            assert all(title in first_page for title in ("Contenido", "Índice de tablas", "Índice de figuras")), first_page
            first_lines = first_page.split("\n")
            for entry in complete["entries"]:
                line = next((ln for ln in first_lines if ln.startswith(entry["label"])), None)
                assert line is not None, entry["label"]
                assert line.rstrip().endswith(str(entry["page"])), (line, entry["page"])
        assert "introduccion" in complete["labels"] and "introduccion" not in feasibility["labels"]
        checks.append({"case": "informe-factibilidad-completo", "pages": complete["pages"], "entries": len(complete["entries"])})
        for name, mutate in [
            ("indices-en-el-informe", lambda x: x["document"].update(indexes=["contents"])),
        ]:
            variant = copy.deepcopy(spec)
            mutate(variant)
            rejected(name, variant)
        no_figures = copy.deepcopy(bare)
        for name, indexes_value, source in [
            ("indices-con-nombre-desconocido", ["resumen"], feasibility_source),
            ("indices-repetidos", ["contents", "contents"], feasibility_source),
            ("indices-no-es-lista", "contents", feasibility_source),
            ("indices-de-figuras-sin-figuras", ["figures"], no_figures),
        ]:
            variant = copy.deepcopy(source)
            variant["document"]["indexes"] = indexes_value
            rejected(name, variant)

        # ---- Alcance del proyecto: formulario sin elecciones, matriz de responsabilidades y dos firmas ----
        alcance_source = json.loads((example.parent/"ejemplo-alcance-proyecto.json").read_text())
        alcance, alcance_pdf = build("alcance-proyecto", alcance_source)
        assert alcance["document"]["kind"] == "alcance-proyecto"
        assert alcance["pages"] == 8, alcance["pages"]
        assert choices(alcance_source) == [], "El alcance no tiene elecciones: su decisión de más peso se escribe"
        assert "perimetro" in alcance["labels"] and any(a["path"].endswith("alcance-pagos.png") for a in alcance["assets"])
        alcance_pages = {entry["id"]: entry["page"] for entry in alcance["entries"]}
        with pdfplumber.open(alcance_pdf) as printed:
            texts = [pg.extract_text() or "" for pg in printed.pages]
            # Every table is whole: its first and last row print on the page where its title is registered.
            for table_id in ("entregas", "lista-condiciones", "fases", "responsables", "partes", "firmas"):
                rows = find_block(alcance_source, table_id)["rows"]
                for cell in (rows[0][0], rows[-1][0]):
                    assert cell.split("\n")[0][:18] in texts[alcance_pages[table_id]-1], (table_id, cell)
            # The legend of the matrix prints on the page of its table, and each pair of signatures stays together.
            assert "responsable de hacer la actividad" in texts[alcance_pages["responsables"]-1]
            acceptance = texts[alcance_pages["partes"]-1]
            assert all(name in acceptance for name in ("Soledad Paredes", "Iván Salas", "Pendiente"))
            assert alcance_pages["firmas"] == alcance["pages"], "Las firmas de responsabilidad cierran el documento"
            assert "Histórico de revisiones" in texts[-1]
            # E1 to E4 are components in the figure; E5 is training during implementation.
            svg_text = (example.parent/"diagrams"/"alcance-pagos.svg").read_text()
            assert all(f"E{n}" in svg_text for n in range(1, 5))
            assert [row[0] for row in find_block(alcance_source, "entregas")["rows"]] == ["E1", "E2", "E3", "E4", "E5"]
            assert "E5" not in svg_text
            assert any("E5" in row[0] for row in find_block(alcance_source, "responsables")["rows"])
            assert "E5" in find_block(alcance_source, "fases")["rows"][-1][2]
        assert check(alcance_pdf)["internal_links"] >= 2
        checks.append({"case": "alcance-proyecto", "pages": alcance["pages"], "figure": True})

        # Matrix content: every activity has at least one R and exactly one A, and only R, A, C, I or R/A.
        matrix = find_block(alcance_source, "responsables")
        for row in matrix["rows"]:
            marks = row[1:]
            assert set(marks) <= {"R", "A", "C", "I", "R/A"}, row
            assert sum(mark in ("A", "R/A") for mark in marks) == 1, row
            assert any(mark in ("R", "R/A") for mark in marks), row
        checks.append({"case": "alcance-matriz-una-sola-A", "activities": len(matrix["rows"])})

        # The chained examples share their figures: weeks, effort, phases, conditions, codes and people.
        fase_rows = lambda source: [row[:2] for row in find_block(source, "fases")["rows"]]
        total_of = lambda source, section_id: find_block(source, section_id=section_id, kind="fields")["items"][0]["value"].split(".")[0]
        assert fase_rows(alcance_source) == fase_rows(feasibility_source)
        assert (total_of(alcance_source, "cronograma") == total_of(feasibility_source, "tiempo")
                == "7 semanas, con 50 días-persona del equipo interno")
        feasibility_conditions = find_block(feasibility_source, section_id="conclusiones", kind="list")["items"]
        scope_conditions = find_block(alcance_source, "lista-condiciones")["rows"]
        assert len(scope_conditions) == len(feasibility_conditions) == 3
        for keyword in ("seguridad", "API", "cancelación"):
            assert any(keyword in item for item in feasibility_conditions)
            assert any(keyword in row[0] for row in scope_conditions), keyword
        reference_values = " ".join(item["value"] for section in alcance_source["sections"] if section["id"] == "referencia"
                                    for b in section["blocks"] if b["type"] == "fields" for item in b["items"])
        assert feasibility_source["document"]["code"] in reference_values and registro_source["document"]["code"] in reference_values
        everyone = json.dumps(alcance_source, ensure_ascii=False)
        for person in ("Marta Quiroga", "Iván Salas", "Lucía Ferrer", "Rafael Mena", "Soledad Paredes"):
            assert person in everyone and (person in json.dumps(feasibility_source, ensure_ascii=False)
                                           or person in json.dumps(registro_source, ensure_ascii=False)), person
        checks.append({"case": "alcance-coherente-con-factibilidad-y-registro"})

        # Optional figure: without it the type compiles once the sentence that calls it goes with it.
        bare_scope = copy.deepcopy(alcance_source)
        for section in bare_scope["sections"]:
            section["blocks"] = [b for b in section.get("blocks", []) if b["type"] != "figure"]
        architecture = find_block(bare_scope, section_id="arquitectura", kind="paragraph")
        architecture["text"] = architecture["text"].split(" El perímetro, con lo que")[0]
        no_scope_figure, _ = build("alcance-sin-figura", bare_scope)
        assert "perimetro" not in no_scope_figure["labels"] and not no_scope_figure["assets"]
        assert 4 <= no_scope_figure["pages"] <= alcance["pages"], no_scope_figure["pages"]
        checks.append({"case": "alcance-sin-figura", "pages": no_scope_figure["pages"]})

        # Optional conditions: an approval without them drops the section and the sentence that cites it.
        unconditional = copy.deepcopy(alcance_source)
        unconditional["sections"] = [x for x in unconditional["sections"] if x["id"] != "condiciones"]
        background = find_block(unconditional, section_id="referencia", kind="paragraph")
        background["runs"][1]["text"] = background["runs"][1]["text"].replace(
            " aprobó, el 13/11/2026, continuar con tres condiciones ({{ref:condiciones}}).", " aprobó, el 13/11/2026, continuar.")
        assert "condiciones" not in background["runs"][1]["text"]
        no_conditions, no_conditions_pdf = build("alcance-sin-condiciones", unconditional)
        no_conditions_text = " ".join(p.extract_text() for p in PdfReader(no_conditions_pdf).pages)
        assert "condiciones" not in no_conditions["labels"] and "lista-condiciones" not in no_conditions["labels"]
        assert "Condiciones de la Aprobación" not in no_conditions_text and "tres condiciones" not in no_conditions_text
        assert not any(label.startswith("4.1.") for label in no_conditions["labels"].values())
        assert 5 <= no_conditions["pages"] <= alcance["pages"], no_conditions["pages"]
        checks.append({"case": "alcance-sin-condiciones", "pages": no_conditions["pages"]})

        # The labels of the two parties are generic: replacing them in the source needs no other change.
        renamed = json.dumps(alcance_source, ensure_ascii=False)
        for generic, own in (("Parte solicitante", "Cliente"), ("parte solicitante", "cliente"),
                             ("Equipo ejecutor", "Proveedor"), ("Solicitante", "Cliente")):
            renamed = renamed.replace(generic, own)
        renamed_source = json.loads(renamed)
        relabeled, relabeled_pdf = build("alcance-con-rotulos-propios", renamed_source)
        relabeled_text = " ".join(p.extract_text() for p in PdfReader(relabeled_pdf).pages)
        assert "Proveedor" in relabeled_text and "Cliente" in relabeled_text
        assert "olicitante" not in relabeled_text and "jecutor" not in relabeled_text
        checks.append({"case": "alcance-con-rotulos-propios", "pages": relabeled["pages"]})

        # Identity, code prefix, paper and signers are configurable, with and without a logo.
        for with_logo in (False, True):
            custom = copy.deepcopy(alcance_source)
            custom["brand"].update(entity="Organización de prueba", unit="Oficina de Proyectos", accent="#7A2E1D")
            custom["document"].update(code="ACME-ALC-07", paper="Letter", status="En revisión")
            find_block(custom, "firmas")["rows"][0][:2] = ["Elaborado por", "Persona de prueba\nCargo de prueba"]
            if with_logo:
                custom["brand"]["logo"] = "test-logo.png"
            personalized, personalized_pdf = build("alcance-"+("logo" if with_logo else "sin-logo"), custom)
            first_page = PdfReader(personalized_pdf).pages[0].extract_text()
            assert personalized["paper"] == "Letter" and "ACME-ALC-07" in first_page
            assert "Oficina de Proyectos" in first_page and "Persona de prueba" in " ".join(
                p.extract_text() for p in PdfReader(personalized_pdf).pages)
            assert ("Organización de prueba" in first_page) != with_logo
            assert any(a["path"] == "test-logo.png" for a in personalized["assets"]) == with_logo
            checks.append({"case": "alcance-personalizado", "logo": with_logo, "pages": personalized["pages"]})

        # The type asks for no choice, but a choice it carries still follows the family rules.
        broken_choice = copy.deepcopy(alcance_source)
        find_block(broken_choice, section_id="referencia", kind="fields")["items"].append(
            {"label": "Fase", "options": ["Planificación", "Ejecución"], "selected": "Cierre"})
        rejected("alcance-eleccion-fuera-de-las-opciones", broken_choice)

        # A table of a form-like kind stays with the legend that follows it. Filler before the matrix moves the
        # page break across the span where the legend used to end up alone on the next page.
        previous_section = [s["id"] for s in alcance_source["sections"]].index("matriz")-1
        for filler in (15, 16, 17, 18, 19):
            padded = copy.deepcopy(alcance_source)
            padded["sections"][previous_section]["blocks"] += [
                {"type": "paragraph", "text": f"Relleno {i}."} for i in range(filler)]
            padded_source = root/f"alcance-leyenda-{filler}.json"
            padded_source.write_text(json.dumps(padded, ensure_ascii=False))
            compile_report(padded_source, root/f"alcance-leyenda-{filler}.pdf")
            with pdfplumber.open(root/f"alcance-leyenda-{filler}.pdf") as printed:
                page_texts = [pg.extract_text() or "" for pg in printed.pages]
            legend_page = next(i for i, text in enumerate(page_texts) if "R: responsable de hacer" in text)
            assert "Puesta en producción" in page_texts[legend_page], f"La leyenda quedó sola con {filler} párrafos de relleno"
        checks.append({"case": "tabla-con-su-leyenda", "filler": [15, 19]})

        # ---- Selección múltiple en fields: varias casillas marcadas, ninguna o todas ----
        multiple_source = copy.deepcopy(registro_source)
        materials = ["Manual", "Ficha técnica", "Presentación", "Acceso al sistema", "Otro: guía rápida"]
        find_block(multiple_source, section_id="datos", kind="fields")["items"] += [
            {"label": "Entregado", "options": ["Acta", "Informe", "Anexo"], "multiple": True, "selected": ["Acta", "Anexo"]},
            {"label": "Pendiente", "options": ["Rúbrica", "Sello"], "multiple": True, "selected": []}]
        find_block(multiple_source, section_id="descripcion", kind="fields")["items"].append(
            {"label": "Materiales", "options": materials, "multiple": True, "selected": [materials[0], materials[2], materials[4]]})
        multiple, multiple_pdf = build("seleccion-multiple", multiple_source)
        assert assert_choices(multiple_pdf, multiple_source) == 6
        multiple_marks = sum(len(marks_of(item)) for item in choices(multiple_source))
        assert multiple_marks == 3+2+0+3, multiple_marks  # three single choices, then 2, none and 3 marks
        assert multiple["pages"] == registro["pages"], (multiple["pages"], registro["pages"])
        checks.append({"case": "seleccion-multiple", "marks": multiple_marks, "pages": multiple["pages"]})

        # Marking every option, or none, is allowed; the marks follow the list, not the order of the options.
        everything = copy.deepcopy(multiple_source)
        choices(everything)[3]["selected"] = ["Anexo", "Acta", "Informe"]
        choices(everything)[4]["selected"] = ["Sello", "Rúbrica"]
        build("seleccion-multiple-todas", everything)
        assert assert_choices(root/"seleccion-multiple-todas.pdf", everything) == 6
        checks.append({"case": "seleccion-multiple-todas-las-opciones"})

        # A single choice that says multiple: false prints exactly as one that omits it.
        explicit = copy.deepcopy(registro_source)
        for item in choices(explicit):
            item["multiple"] = False
        explicit_manifest, explicit_pdf = build("seleccion-simple-explicita", explicit)
        assert [pg.extract_text() for pg in PdfReader(explicit_pdf).pages] == [pg.extract_text() for pg in PdfReader(registro_pdf).pages]
        assert explicit_manifest["entries"] == registro["entries"] and explicit_manifest["pages"] == registro["pages"]
        assert assert_choices(explicit_pdf, explicit) == 3
        checks.append({"case": "seleccion-simple-con-multiple-falso"})

        # Each rule of the multiple choice rejects with a message that says what to fix.
        multi = lambda x: choices(x)[3]
        for name, mutate, message in [
            ("multiple-selected-texto", lambda x: multi(x).update(selected="Acta"), "selected debe ser una lista"),
            ("multiple-sin-selected", lambda x: multi(x).pop("selected"), "selected debe ser una lista"),
            ("multiple-selected-nulo", lambda x: multi(x).update(selected=None), "selected debe ser una lista"),
            ("multiple-marca-fuera-de-las-opciones", lambda x: multi(x).update(selected=["Acta", "Boletín"]), "que no está en options"),
            ("multiple-marca-no-es-texto", lambda x: multi(x).update(selected=[1]), "que no está en options"),
            ("multiple-marca-repetida", lambda x: multi(x).update(selected=["Acta", "Acta"]), "repite una opción"),
            ("multiple-no-booleano", lambda x: multi(x).update(multiple="sí"), "multiple debe ser true o false"),
            ("multiple-sin-opciones", lambda x: (multi(x).pop("options"), multi(x).pop("selected")), "multiple solo se usa con options"),
            ("multiple-con-valor", lambda x: multi(x).update(value="Acta"), "usar value o options, no ambos"),
            ("multiple-opciones-repetidas", lambda x: multi(x).update(options=["Acta", "Acta", "Anexo"]), "textos repetidos"),
            ("multiple-una-sola-opcion", lambda x: multi(x).update(options=["Acta"], selected=["Acta"]), "de 2 a 6 textos"),
            ("multiple-siete-opciones", lambda x: multi(x).update(options=[f"Opción {i}" for i in range(7)], selected=[]), "de 2 a 6 textos"),
            ("simple-con-lista-sugiere-multiple", lambda x: choices(x)[0].update(selected=["Software", "Recursos"]), "multiple: true"),
            ("simple-con-multiple-falso-y-lista", lambda x: choices(x)[0].update(multiple=False, selected=["Software"]), "exactamente una de las options"),
        ]:
            variant = copy.deepcopy(multiple_source)
            mutate(variant)
            rejected_with(name, variant, message)

        # A multiple choice never stands for the single mark a kind demands: viabilidad and tipo stay required.
        for source, kind, message in [(feasibility_source, "informe-factibilidad", "informe-factibilidad requiere una viabilidad marcada"),
                                      (registro_source, "registro-requerimientos", "registro-requerimientos requiere al menos una elección marcada")]:
            only_multiple = copy.deepcopy(source)
            for item in choices(only_multiple):
                item["multiple"], item["selected"] = True, [item["selected"]]
            rejected_with(f"{kind}-solo-con-elecciones-multiples", only_multiple, message)

        # ---- Acta de capacitación: modalidad de una sola marca, materiales de varias, asistentes en blanco ----
        import re
        from datetime import date, timedelta
        acta_source = json.loads((example.parent/"ejemplo-acta-capacitacion.json").read_text())
        capacitacion, capacitacion_pdf = build("acta-capacitacion", acta_source)
        assert capacitacion["document"]["kind"] == "acta-capacitacion"
        assert capacitacion["pages"] == 5, capacitacion["pages"]
        by_label = lambda source, label: next(item for item in choices(source) if item["label"] == label)
        assert [item["label"] for item in choices(acta_source)] == ["Modalidad", "Materiales"]
        assert not by_label(acta_source, "Modalidad").get("multiple") and by_label(acta_source, "Materiales")["multiple"]
        assert len(by_label(acta_source, "Materiales")["selected"]) == 4  # several marks, and one option left empty
        assert assert_choices(capacitacion_pdf, acta_source) == 2
        acta_pages = {entry["id"]: entry["page"] for entry in capacitacion["entries"]}
        attendees = find_block(acta_source, "lista-asistentes")["rows"]
        with pdfplumber.open(capacitacion_pdf) as printed:
            texts = [pg.extract_text() or "" for pg in printed.pages]
            # The attendee table may split when much of the page is free, repeating its title and header; each
            # number prints once, in the page of its title or the next one.
            first = acta_pages["lista-asistentes"]-1
            roll = "\n".join(texts[first:first+2])
            assert all(len(re.findall(rf"(?m)^{n}( |$)", roll)) == 1 for n in range(1, len(attendees)+1)), roll
            assert "____" not in roll, "the signature cell is left empty: no printed line"
            for table_id, first, last in (("evaluacion-aspectos", "Claridad de la exposición", "Práctica guiada con el módulo"),
                                          ("constancia-firma", "Instructor", "Arquitecta de software"),
                                          ("firmas", "Elaborado por", "Aprobado por")):
                assert first in texts[acta_pages[table_id]-1] and last in texts[acta_pages[table_id]-1], table_id
            assert 0 <= acta_pages["comentarios"]-acta_pages["evaluacion-aspectos"] <= 1  # a small table may go to the next page
            # The signatures of responsibility close the document, before the history.
            assert capacitacion["pages"]-1 <= acta_pages["firmas"] <= capacitacion["pages"] and "Histórico de revisiones" in texts[-1]
        assert check(capacitacion_pdf)["internal_links"] >= 2
        checks.append({"case": "acta-capacitacion", "pages": capacitacion["pages"], "choices": 2})

        # The roll: consecutive numbers, a signature line in every row, two rows with no name, and a blank evaluation.
        assert [row[0] for row in attendees] == [str(n) for n in range(1, len(attendees)+1)]
        blank_rows = [row for row in attendees if not row[1] and not row[2]]
        assert len(blank_rows) == 2 and all(row[3] == "" for row in attendees)
        evaluation = find_block(acta_source, "evaluacion-aspectos")
        assert evaluation["headers"][1:] == ["1", "2", "3", "4", "5"]
        assert all(cell == "" for row in evaluation["rows"] for cell in row[1:])
        checks.append({"case": "acta-asistentes-en-blanco-y-evaluacion-en-blanco", "rows": len(attendees)})

        # The chained examples share the project, the people, the code of the scope and the calendar.
        grid = {item["label"]: item["value"] for b in next(x for x in acta_source["sections"] if x["id"] == "informacion")["blocks"]
                if b["type"] == "fields" for item in b["items"] if "value" in item}
        scope = {item["label"]: item["value"] for b in next(x for x in alcance_source["sections"] if x["id"] == "referencia")["blocks"]
                 if b["type"] == "fields" for item in b["items"]}
        assert acta_source["document"]["code"] == grid["N.º de acta"] == "DEMO-CAP-01"
        assert grid["Alcance asociado"] == alcance_source["document"]["code"]
        assert grid["Proyecto"] == scope["Nombre del proyecto"]
        for label in ("Parte solicitante", "Equipo ejecutor", "Líder de proyecto"):
            assert grid[label] == scope[label], label
        assert grid["Instructores"].split("\n")[0] == scope["Líder técnico"]
        scope_signers = {row[0]: row[1] for row in find_block(alcance_source, "firmas")["rows"]}
        acta_signers = {row[0]: row[1] for row in find_block(acta_source, "firmas")["rows"]}
        assert acta_signers["Revisado por"] == scope_signers["Revisado por"] and acta_signers["Aprobado por"] == scope_signers["Aprobado por"]
        assert acta_signers["Elaborado por"].replace("\n", ", ").lower() == scope["Líder de proyecto"].lower()
        assert find_block(acta_source, "constancia-firma")["rows"][0][1].split("\n")[0] == grid["Instructores"].split(",")[0]
        everyone_in_the_chain = " ".join(json.dumps(x, ensure_ascii=False) for x in (feasibility_source, registro_source, alcance_source))
        assert all(row[1] in everyone_in_the_chain for row in attendees[:1])  # the sponsor attends
        # The session comes after the tests of the schedule and not after the date of the document.
        phases = find_block(alcance_source, "fases")["rows"]
        tests_row = next(i for i, row in enumerate(phases) if row[0].startswith("Pruebas"))
        weeks_to_tests_end = sum(int(row[1].split()[0]) for row in phases[:tests_row+1])
        session = date(*reversed([int(part) for part in grid["Fecha de capacitación"].split("/")]))
        assert session > date.fromisoformat(alcance_source["document"]["date"])+timedelta(weeks=weeks_to_tests_end), session
        assert session <= date.fromisoformat(acta_source["document"]["date"])
        assert [c["date"] for c in acta_source["changes"]] == sorted(c["date"] for c in acta_source["changes"])
        assert date.fromisoformat(acta_source["changes"][-1]["date"]) == date.fromisoformat(acta_source["document"]["date"])
        checks.append({"case": "acta-capacitacion-coherente-con-el-alcance", "session": session.isoformat()})

        # Every optionality of the guide has its case: the line «Otro», no material, a virtual or mixed session.
        no_other = copy.deepcopy(acta_source)
        by_label(no_other, "Materiales").update(options=by_label(no_other, "Materiales")["options"][:4])
        by_label(no_other, "Materiales")["selected"] = by_label(no_other, "Materiales")["selected"][:3]
        no_other_manifest, no_other_pdf = build("acta-sin-otro-material", no_other)
        assert assert_choices(no_other_pdf, no_other) == 2
        assert "guía rápida" not in " ".join(p.extract_text() for p in PdfReader(no_other_pdf).pages)
        assert no_other_manifest["pages"] == capacitacion["pages"]
        checks.append({"case": "acta-sin-linea-otro", "pages": no_other_manifest["pages"]})

        nothing_delivered = copy.deepcopy(acta_source)
        by_label(nothing_delivered, "Materiales")["selected"] = []
        _, nothing_pdf = build("acta-sin-materiales-marcados", nothing_delivered)
        assert assert_choices(nothing_pdf, nothing_delivered) == 2  # only the cross of the modality remains
        checks.append({"case": "acta-ningun-material-marcado"})

        for name, mode, extra in (("virtual", "Virtual", None), ("mixta", "Mixta", "Mixta")):
            remote = copy.deepcopy(acta_source)
            find_block(remote, section_id="informacion", kind="fields")["items"][5]["value"] = (
                "Plataforma de videollamadas de la entidad; enlace en la invitación del 05/01/2027")
            modality = by_label(remote, "Modalidad")
            if extra:
                modality["options"].append(extra)
            modality["selected"] = mode
            remote_manifest, remote_pdf = build(f"acta-{name}", remote)
            assert assert_choices(remote_pdf, remote) == 2
            assert remote_manifest["pages"] == capacitacion["pages"]
            checks.append({"case": f"acta-modalidad-{name}", "pages": remote_manifest["pages"]})

        # More attendees than rows: the table breaks across pages with its title and header repeated, nothing else moves.
        crowded = copy.deepcopy(acta_source)
        rows = [[str(n), f"Asistente de prueba {n}", "Cargo de prueba", ""] for n in range(1, 29)]
        rows += [["29", "", "", ""], ["30", "", "", ""]]
        find_block(crowded, "lista-asistentes")["rows"] = rows
        crowded_manifest, crowded_pdf = build("acta-muchos-asistentes", crowded)
        crowded_texts = [pg.extract_text() or "" for pg in PdfReader(crowded_pdf).pages]
        roll_pages = [i for i, text in enumerate(crowded_texts) if "Asistentes a la capacitación" in text and "Nombre y apellido" in text]
        assert len(roll_pages) >= 2 and crowded_manifest["pages"] > capacitacion["pages"], (roll_pages, crowded_manifest["pages"])
        assert "Asistente de prueba 28" in crowded_texts[roll_pages[-1]]
        roll_text = "\n".join(crowded_texts[roll_pages[0]:roll_pages[-1]+1])
        assert all(re.search(rf"(?m)^{n}( |$)", roll_text) for n in range(1, 31)), "Every row keeps its number across the pages"
        crowded_pages = {entry["id"]: entry["page"] for entry in crowded_manifest["entries"]}
        assert crowded_pages["firmas"] == crowded_manifest["pages"], "Las firmas de responsabilidad siguen cerrando el documento"
        checks.append({"case": "acta-muchos-asistentes", "roll_pages": [i+1 for i in roll_pages], "pages": crowded_manifest["pages"]})

        # Fewer attendees: the unused rows go, two stay blank, and a guest who did not come keeps their row.
        small = copy.deepcopy(acta_source)
        find_block(small, "lista-asistentes")["rows"] = [
            ["1", "Soledad Paredes", "Jefa de operaciones de reservas", ""],
            ["2", "Teresa Villalba", "Coordinadora de reservas", "No asistió"],
            ["3", "", "", ""], ["4", "", "", ""]]
        small_manifest, small_pdf = build("acta-pocos-asistentes", small)
        small_text = " ".join(p.extract_text() for p in PdfReader(small_pdf).pages)
        assert "No asistió" in small_text and small_manifest["pages"] <= capacitacion["pages"]
        checks.append({"case": "acta-pocos-asistentes", "pages": small_manifest["pages"]})

        # Identity, code prefix, paper and signers are configurable, with and without a logo.
        for with_logo in (False, True):
            custom = copy.deepcopy(acta_source)
            custom["brand"].update(entity="Organización de prueba", unit="Oficina de Proyectos", accent="#7A2E1D")
            custom["document"].update(code="ACME-CAP-07", paper="Letter", status="En revisión")
            find_block(custom, "firmas")["rows"][0][:2] = ["Elaborado por", "Persona de prueba\nCargo de prueba"]
            if with_logo:
                custom["brand"]["logo"] = "test-logo.png"
            personalized, personalized_pdf = build("acta-capacitacion-"+("logo" if with_logo else "sin-logo"), custom)
            first_page = PdfReader(personalized_pdf).pages[0].extract_text()
            assert personalized["paper"] == "Letter" and "ACME-CAP-07" in first_page
            assert "Oficina de Proyectos" in first_page and "Persona de prueba" in " ".join(
                p.extract_text() for p in PdfReader(personalized_pdf).pages)
            assert ("Organización de prueba" in first_page) != with_logo
            assert any(a["path"] == "test-logo.png" for a in personalized["assets"]) == with_logo
            assert assert_choices(personalized_pdf, custom) == 2
            checks.append({"case": "acta-capacitacion-personalizada", "logo": with_logo, "pages": personalized["pages"]})

        # The labels of the two parties are generic: replacing them in the source needs no other change.
        renamed = json.dumps(acta_source, ensure_ascii=False)
        for generic, own in (("Parte solicitante", "Cliente"), ("Equipo ejecutor", "Proveedor")):
            renamed = renamed.replace(generic, own)
        relabeled_acta, relabeled_acta_pdf = build("acta-con-rotulos-propios", json.loads(renamed))
        relabeled_text = " ".join(p.extract_text() for p in PdfReader(relabeled_acta_pdf).pages)
        assert "Proveedor" in relabeled_text and "Cliente" in relabeled_text
        assert "olicitante" not in relabeled_text and "jecutor" not in relabeled_text
        checks.append({"case": "acta-con-rotulos-propios", "pages": relabeled_acta["pages"]})

        # The rule of the type: the modality is the single mark it demands, and a multiple choice does not replace it.
        no_modality = copy.deepcopy(acta_source)
        find_block(no_modality, section_id="informacion", kind="fields")["items"].remove(by_label(no_modality, "Modalidad"))
        rejected_with("acta-sin-modalidad", no_modality, "acta-capacitacion requiere la modalidad marcada")
        for name, mutate, message in [
            ("acta-modalidad-con-dos-marcas", lambda x: by_label(x, "Modalidad").update(selected=["Presencial", "Virtual"]), "multiple: true"),
            ("acta-modalidad-fuera-de-las-opciones", lambda x: by_label(x, "Modalidad").update(selected="Híbrida"), "exactamente una de las options"),
            ("acta-material-fuera-de-las-opciones", lambda x: by_label(x, "Materiales").update(selected=["Videos"]), "que no está en options"),
            ("acta-material-con-una-sola-marca-como-texto", lambda x: by_label(x, "Materiales").update(selected="Manual de usuario del módulo"),
             "selected debe ser una lista"),
        ]:
            variant = copy.deepcopy(acta_source)
            mutate(variant)
            rejected_with(name, variant, message)

        from test_acta_entrega_cadena import run_checks as check_delivery_chain
        check_delivery_chain(example, checks, build, rejected_with)

        from test_plan_pruebas import run_checks
        run_checks(example, checks, build, rejected_with)

        # ---- Registro de riesgos: el nivel se calcula y el resumen cuenta solo los abiertos ----
        from build_report import matrix_level, open_risk_rows, validate_risks
        risk_source = json.loads((example.parent/"ejemplo-registro-riesgos.json").read_text())
        risks, risks_pdf = build("registro-riesgos", risk_source)
        assert risks["pages"] == 5, risks["pages"]
        assert risks["document"]["kind"] == "registro-riesgos"
        assert choices(risk_source) == [], "El registro de riesgos no tiene elecciones: el nivel lo calcula el motor"
        risk_block = find_block(risk_source, "matriz-niveles")
        checked = copy.deepcopy(risk_block)
        validate_risks(checked)
        assert open_risk_rows(checked) == [
            ["Bajo", "1", "{{ref:R-06}}"],
            ["Medio", "3", "{{ref:R-02}}, {{ref:R-04}}, {{ref:R-08}}"],
            ["Alto", "2", "{{ref:R-01}}, {{ref:R-03}}"],
            ["Crítico", "1", "{{ref:R-05}}"],
            ["Total de abiertos", "7", ""],
        ]
        risk_pages = {entry["id"]: entry["page"] for entry in risks["entries"]}
        with pdfplumber.open(risks_pdf) as printed:
            risk_texts = [pg.extract_text() or "" for pg in printed.pages]
        for item in risk_block["items"]:
            level = matrix_level(risk_block["scale"], item["probability"], item["impact"])
            assert checked["items"][risk_block["items"].index(item)]["_level"] == level
            card = next(text for text in risk_texts if item["cause"][:48] in text)
            assert item["id"] in card and f"Nivel: {level}" in card, (item["id"], level)
            assert "Acción" in card, item["id"]
        summary = next(text for text in risk_texts if "Riesgos abiertos por nivel" in text)
        for piece in ("Bajo", "Medio", "Alto", "Crítico", "Total de abiertos", "7",
                      "R-06", "R-02", "R-04", "R-08", "R-01", "R-03", "R-05"):
            assert piece in summary, piece
        matrix_page = next(text for text in risk_texts if "Matriz de niveles" in text)
        assert "Probabilidad / Impacto" in matrix_page and "Crítico" in matrix_page
        assert risk_pages["firmas"] == risk_pages["seguimiento"] == risks["pages"]
        assert "Histórico de revisiones" in risk_texts[-1] and "Pendiente" in risk_texts[-1]
        assert "Cerrado" in next(text for text in risk_texts if "R-07" in text and "Nivel:" in text)
        checks.append({"case": "registro-riesgos", "pages": risks["pages"], "open": 7})

        # The chain of examples shares codes, people, dates and the figures already stated.
        feasibility_text = json.dumps(feasibility_source, ensure_ascii=False)
        scope_text = json.dumps(alcance_source, ensure_ascii=False)
        risk_text = json.dumps(risk_source, ensure_ascii=False)
        for shared in ("DEMO-FAC-01", "DEMO-ALC-01", "DEMO-REQ-014", "Marta Quiroga", "Julián Benítez",
                       "Camila Ortega", "Soledad Paredes", "Rafael Mena", "Lucía Ferrer",
                       "27/10/2026", "09/11/2026", "13/11/2026", "16/11/2026",
                       "5 segundos", "15 minutos", "360 píxeles", "3 días", "100 confirmaciones"):
            assert shared in risk_text, shared
            assert shared in feasibility_text or shared in scope_text, shared
        assert "7 semanas" in feasibility_text and "7 semanas" in scope_text and "siete semanas" in risk_text
        assert "arquitecta de software" in risk_text and "arquitecta de software" in feasibility_text
        assert "jefa de operaciones de reservas" in risk_text and "jefa de operaciones de reservas" in scope_text
        checks.append({"case": "registro-riesgos-coherente-con-factibilidad-y-alcance"})

        # No state change: the follow-up table goes away and one sentence stays.
        quiet = copy.deepcopy(risk_source)
        follow = next(section for section in quiet["sections"] if section["id"] == "seguimiento")
        follow["blocks"] = [block for block in follow["blocks"] if block["type"] != "table"]
        follow["blocks"][0]["text"] = "En el corte del 16/11/2026 no cambió ningún riesgo."
        follow["blocks"] = follow["blocks"][:1]
        quiet_result, quiet_pdf = build("registro-sin-cambios", quiet)
        quiet_text = " ".join(page.extract_text() or "" for page in PdfReader(quiet_pdf).pages)
        assert "cambios" not in quiet_result["labels"] and "no cambió ningún riesgo" in quiet_text
        assert quiet_result["pages"] <= risks["pages"]
        assert any(entry["id"] == "firmas" and entry["page"] == quiet_result["pages"] for entry in quiet_result["entries"])
        checks.append({"case": "registro-sin-cambios", "pages": quiet_result["pages"]})

        # A 5 by 5 scale compiles, and the levels of the same pairs stay where the matrix puts them.
        wider = copy.deepcopy(risk_source)
        wider_block = find_block(wider, "matriz-niveles")
        wider_block["scale"] = {
            "probability": ["Muy baja", "Baja", "Media", "Alta", "Muy alta"],
            "impact": ["Muy bajo", "Bajo", "Medio", "Alto", "Muy alto"],
            "matrix": [
                ["Bajo", "Bajo", "Bajo", "Medio", "Medio"],
                ["Bajo", "Bajo", "Bajo", "Medio", "Alto"],
                ["Bajo", "Bajo", "Medio", "Alto", "Alto"],
                ["Medio", "Medio", "Alto", "Crítico", "Crítico"],
                ["Alto", "Alto", "Alto", "Crítico", "Crítico"],
            ],
        }
        wider_result, wider_pdf = build("registro-escala-cinco", wider)
        wider_text = " ".join(page.extract_text() or "" for page in PdfReader(wider_pdf).pages)
        assert "Muy baja" in wider_text and "Muy alto" in wider_text
        assert matrix_level(wider_block["scale"], "Alta", "Alto") == "Crítico"
        assert "Nivel: Crítico" in wider_text
        checks.append({"case": "registro-escala-cinco", "pages": wider_result["pages"]})

        # The entity's own words replace the default responses and states.
        renamed_risks = copy.deepcopy(risk_source)
        renamed_block = find_block(renamed_risks, "matriz-niveles")
        renamed_block["responses"] = ["Mitigar", "Vigilar", "Transferir", "Aceptar", "Evitar"]
        renamed_block["states"] = ["Vigente", "En curso", "Ocurrido", "Cerrado"]
        renamed_block["open_states"] = ["Vigente", "En curso"]
        state_of = {"Abierto": "Vigente", "En mitigación": "En curso", "Cerrado": "Cerrado"}
        for item in renamed_block["items"]:
            item["state"] = state_of[item["state"]]
        renamed_block["items"][1]["response"] = "Vigilar"
        renamed_result, renamed_pdf = build("registro-estados-propios", renamed_risks)
        renamed_text = " ".join(page.extract_text() or "" for page in PdfReader(renamed_pdf).pages)
        assert "Vigilar" in renamed_text and "Vigente" in renamed_text and "En curso" in renamed_text
        assert "Materializado" not in renamed_text
        checks.append({"case": "registro-estados-propios", "pages": renamed_result["pages"]})

        for with_logo in (False, True):
            custom = copy.deepcopy(risk_source)
            custom["brand"].update(entity="Organización de prueba", unit="Oficina de Proyectos", accent="#7A2E1D")
            custom["document"].update(code="ACME-RIE-07", paper="Letter", status="En revisión")
            find_block(custom, "firmas")["rows"][0][:2] = ["Elaborado por", "Persona de prueba\nCargo de prueba"]
            if with_logo:
                custom["brand"]["logo"] = "test-logo.png"
            personalized, personalized_pdf = build("registro-"+("logo" if with_logo else "sin-logo"), custom)
            first_page = PdfReader(personalized_pdf).pages[0].extract_text()
            assert personalized["paper"] == "Letter" and "ACME-RIE-07" in first_page
            assert "Oficina de Proyectos" in first_page and "Persona de prueba" in " ".join(
                page.extract_text() or "" for page in PdfReader(personalized_pdf).pages)
            assert ("Organización de prueba" in first_page) != with_logo
            assert any(asset["path"] == "test-logo.png" for asset in personalized["assets"]) == with_logo
            checks.append({"case": "registro-personalizado", "logo": with_logo, "pages": personalized["pages"]})

        indexed = copy.deepcopy(risk_source)
        indexed["document"]["indexes"] = ["tables"]
        indexed_result, indexed_pdf = build("registro-con-indice-de-tablas", indexed)
        indexed_text = PdfReader(indexed_pdf).pages[0].extract_text()
        assert "Índice de tablas" in indexed_text and "Matriz de niveles" in indexed_text
        checks.append({"case": "registro-con-indice-de-tablas", "pages": indexed_result["pages"]})

        broken_choice = copy.deepcopy(risk_source)
        find_block(broken_choice, section_id="referencia", kind="fields")["items"].append(
            {"label": "Fase", "options": ["Planificación", "Ejecución"], "selected": "Cierre"})
        rejected_with("registro-eleccion-fuera-de-las-opciones", broken_choice, "exactamente una de las options")

        def break_risk(name, mutate, message):
            variant = copy.deepcopy(risk_source)
            mutate(find_block(variant, "matriz-niveles"))
            rejected_with(name, variant, message)

        break_risk("riesgo-probabilidad-fuera-de-la-escala",
                   lambda block: block["items"][0].update(probability="Imposible"), "la probabilidad 'Imposible'")
        break_risk("riesgo-impacto-fuera-de-la-escala",
                   lambda block: block["items"][0].update(impact="Enorme"), "el impacto 'Enorme'")
        break_risk("riesgo-matriz-con-pocas-filas",
                   lambda block: block["scale"].update(matrix=block["scale"]["matrix"][:2]), "matrix tiene 2 filas")
        break_risk("riesgo-matriz-con-pocas-columnas",
                   lambda block: block["scale"].update(matrix=[row[:2] for row in block["scale"]["matrix"]]),
                   "tiene 2 columnas")
        break_risk("riesgo-escala-de-dos",
                   lambda block: block["scale"].update(probability=["Baja", "Media"]), "de 3 a 5 etiquetas y tiene 2")
        break_risk("riesgo-escala-de-seis",
                   lambda block: block["scale"].update(probability=[f"P{i}" for i in range(6)]), "de 3 a 5 etiquetas y tiene 6")
        break_risk("riesgo-id-repetido",
                   lambda block: block["items"][1].update(id="R-01"), "el id R-01 está repetido")
        break_risk("riesgo-estado-desconocido",
                   lambda block: block["items"][0].update(state="Archivado"), "el estado 'Archivado'")
        break_risk("riesgo-respuesta-desconocida",
                   lambda block: block["items"][0].update(response="Ignorar"), "la respuesta 'Ignorar'")
        break_risk("riesgo-nivel-escrito-a-mano",
                   lambda block: block["items"][0].update(level="Alto"), "no se escribe a mano")
        break_risk("riesgo-nivel-en-espanol-escrito-a-mano",
                   lambda block: block["items"][0].update(nivel="Alto"), "quitar nivel")
        break_risk("riesgo-sin-causa",
                   lambda block: block["items"][0].update(cause="  "), "falta la causa")
        break_risk("riesgo-estados-sin-abiertos",
                   lambda block: block.update(states=["Vigente", "Cerrado"]), "indicar también open_states")
        break_risk("riesgo-abiertos-fuera-de-los-estados",
                   lambda block: block.update(open_states=["Vigente"]), "open_states incluye 'Vigente'")

        # ---- Propuesta de servicio: el motor calcula la cotización y no copia el esfuerzo interno ----
        from datetime import date
        from decimal import Decimal
        from build_report import format_amount, validate_quote
        proposal_source = json.loads((example.parent/"ejemplo-propuesta-servicio.json").read_text())
        proposal, proposal_pdf = build("propuesta-servicio", proposal_source)
        assert proposal["pages"] == 5, proposal["pages"]
        assert proposal["document"]["kind"] == "propuesta-servicio"
        assert choices(proposal_source) == []
        quote = copy.deepcopy(find_block(proposal_source, "cotizacion"))
        validate_quote(quote)
        assert quote["items"][1]["_amount"] == Decimal("3600.00")
        assert quote["_subtotal"] == Decimal("23100.00")
        assert quote["_tax"] == Decimal("3465.00")
        assert quote["_total"] == Decimal("26565.00")
        assert format_amount(quote["_total"], ",", ".") == "26.565,00"
        proposal_pages = {entry["id"]: entry["page"] for entry in proposal["entries"]}
        with pdfplumber.open(proposal_pdf) as printed:
            proposal_texts = [pg.extract_text() or "" for pg in printed.pages]
        proposal_text = " ".join(proposal_texts)
        for piece in ("26.565,00", "23.100,00", "3.465,00", "3.600,00", "16.000,00", "1.800,00"):
            assert piece in proposal_text, piece
        assert proposal_texts[0].count("26.565,00") >= 1
        quote_page = next(text for text in proposal_texts if "Cotización del módulo de pagos" in text)
        assert "26.565,00" in quote_page and "16.000,00" in quote_page and "Impuesto, 15 %" in quote_page
        assert "días-persona" not in proposal_text and "webhook" not in proposal_text and "SDK" not in proposal_text
        assert proposal_pages["firmas"] == proposal["pages"]
        assert "Histórico de revisiones" in proposal_texts[-1] and "Pendiente" in proposal_texts[-1]
        checks.append({"case": "propuesta-servicio", "pages": proposal["pages"], "total": "26565.00"})

        feasibility_date = date.fromisoformat(feasibility_source["document"]["date"])
        proposal_date = date.fromisoformat(proposal_source["document"]["date"])
        scope_date = date.fromisoformat(alcance_source["document"]["date"])
        assert feasibility_date < proposal_date < scope_date
        proposal_json = json.dumps(proposal_source, ensure_ascii=False)
        scope_json = json.dumps(alcance_source, ensure_ascii=False)
        feasibility_json = json.dumps(feasibility_source, ensure_ascii=False)
        risk_json = json.dumps(risk_source, ensure_ascii=False)
        for shared in ("DEMO-REQ-014", "DEMO-RIE-01", "7 semanas", "Soledad Paredes", "Iván Salas",
                       "Marta Quiroga", "27/10/2026", "15 minutos", "5 segundos", "360 píxeles",
                       "pagos en efectivo", "pagos recurrentes"):
            assert shared in proposal_json, shared
        assert "DEMO-RIE-01" in risk_json and "jefa de operaciones de reservas" in scope_json
        assert "7 semanas" in feasibility_json and "arquitecta de software" in feasibility_json
        assert "días-persona" not in proposal_json and "50 días-persona" in feasibility_json
        checks.append({"case": "propuesta-coherente-y-sin-esfuerzo-interno"})

        unpriced = copy.deepcopy(proposal_source)
        investment = next(section for section in unpriced["sections"] if section["id"] == "inversion")
        investment["blocks"] = [{"type": "paragraph", "text": "Por estimar. La entidad no ha fijado el precio."}]
        unpriced["sections"][0]["blocks"][0]["text"] = (
            "Se propone el cobro con tarjeta de cada reserva, en 7 semanas. La inversión: Por estimar. "
            "Operaciones de reservas confirma el plazo de cancelación.")
        unpriced_result, unpriced_pdf = build("propuesta-sin-cotizacion", unpriced)
        unpriced_text = " ".join(page.extract_text() or "" for page in PdfReader(unpriced_pdf).pages)
        assert "cotizacion" not in unpriced_result["labels"] and "Por estimar" in unpriced_text
        assert "26.565,00" not in unpriced_text and unpriced_result["pages"] <= proposal["pages"]
        checks.append({"case": "propuesta-sin-cotizacion", "pages": unpriced_result["pages"]})

        swapped = copy.deepcopy(proposal_source)
        swapped_quote = find_block(swapped, "cotizacion")
        swapped_quote["decimal"] = "."
        swapped_quote["thousands"] = ","
        _, swapped_pdf = build("propuesta-separadores", swapped)
        swapped_text = " ".join(page.extract_text() or "" for page in PdfReader(swapped_pdf).pages)
        assert "26,565.00" in swapped_text and "3,465.00" in swapped_text
        checks.append({"case": "propuesta-separadores"})

        cents = copy.deepcopy(proposal_source)
        cents_quote = find_block(cents, "cotizacion")
        cents_quote["items"] = [{"concept": "Ajuste", "quantity": 3, "unit_price": 10.10}]
        cents_quote["tax_rate"] = 0.1
        cents_checked = copy.deepcopy(cents_quote)
        validate_quote(cents_checked)
        assert cents_checked["items"][0]["_amount"] == Decimal("30.30")
        assert cents_checked["_tax"] == Decimal("3.03") and cents_checked["_total"] == Decimal("33.33")
        _, cents_pdf = build("propuesta-centimos", cents)
        cents_text = " ".join(page.extract_text() or "" for page in PdfReader(cents_pdf).pages)
        assert "30,30" in cents_text and "3,03" in cents_text and "33,33" in cents_text
        checks.append({"case": "propuesta-centimos"})

        for with_logo in (False, True):
            custom = copy.deepcopy(proposal_source)
            custom["brand"].update(entity="Organización de prueba", unit="Oficina Comercial", accent="#7A2E1D")
            custom["document"].update(code="ACME-PRO-07", paper="Letter", status="En revisión")
            find_block(custom, "firmas")["rows"][0][1] = "Persona de prueba\nCargo de prueba"
            if with_logo:
                custom["brand"]["logo"] = "test-logo.png"
            personalized, personalized_pdf = build("propuesta-"+("logo" if with_logo else "sin-logo"), custom)
            first_page = PdfReader(personalized_pdf).pages[0].extract_text()
            assert personalized["paper"] == "Letter" and "ACME-PRO-07" in first_page
            assert "Oficina Comercial" in first_page and "Persona de prueba" in " ".join(
                page.extract_text() or "" for page in PdfReader(personalized_pdf).pages)
            assert ("Organización de prueba" in first_page) != with_logo
            assert any(asset["path"] == "test-logo.png" for asset in personalized["assets"]) == with_logo
            checks.append({"case": "propuesta-personalizada", "logo": with_logo, "pages": personalized["pages"]})

        indexed_proposal = copy.deepcopy(proposal_source)
        indexed_proposal["document"]["indexes"] = ["tables"]
        indexed_proposal_result, indexed_proposal_pdf = build("propuesta-con-indice", indexed_proposal)
        assert "Índice de tablas" in PdfReader(indexed_proposal_pdf).pages[0].extract_text()
        checks.append({"case": "propuesta-con-indice", "pages": indexed_proposal_result["pages"]})

        broken_proposal = copy.deepcopy(proposal_source)
        find_block(broken_proposal, section_id="condiciones", kind="fields")["items"].append(
            {"label": "Moneda", "options": ["USD", "EUR"], "selected": "Peso"})
        rejected_with("propuesta-eleccion-fuera-de-las-opciones", broken_proposal, "exactamente una de las options")

        def break_quote(name, mutate, message):
            variant = copy.deepcopy(proposal_source)
            mutate(find_block(variant, "cotizacion"))
            rejected_with(name, variant, message)

        break_quote("cotizacion-cantidad-no-numerica",
                    lambda block: block["items"][0].update(quantity="dos"), "no es un número")
        break_quote("cotizacion-cantidad-cero",
                    lambda block: block["items"][0].update(quantity=0), "mayor que cero")
        break_quote("cotizacion-cantidad-booleana",
                    lambda block: block["items"][0].update(quantity=True), "no es un número")
        break_quote("cotizacion-precio-negativo",
                    lambda block: block["items"][0].update(unit_price=-1), "no puede ser negativo")
        break_quote("cotizacion-tasa-fuera-de-rango",
                    lambda block: block.update(tax_rate=1.5), "fuera de 0 a 1")
        break_quote("cotizacion-tasa-texto",
                    lambda block: block.update(tax_rate="0.15"), "tax_rate no es un número")
        break_quote("cotizacion-moneda-vacia",
                    lambda block: block.update(currency="  "), "la moneda está vacía")
        break_quote("cotizacion-total-escrito-a-mano",
                    lambda block: block.update(total=26565), "quitar total")
        break_quote("cotizacion-subtotal-en-la-linea",
                    lambda block: block["items"][0].update(subtotal=16000), "quitar subtotal")

        from test_decision_arquitectura import run_checks as check_adr
        check_adr(example, checks, build, rejected_with)

        from test_descripcion_arquitectura import run_checks as check_architecture
        check_architecture(example, checks, build, rejected_with)

        # ---- Especificación de requisitos: la matriz sale de las fichas ----
        from datetime import date
        ers_source = json.loads((example.parent/"ejemplo-especificacion-requisitos.json").read_text())
        atp_source = json.loads((example.parent/"ejemplo-plan-pruebas.json").read_text())
        alcance_chain = json.loads((example.parent/"ejemplo-alcance-proyecto.json").read_text())
        cap_source = json.loads((example.parent/"ejemplo-acta-capacitacion.json").read_text())
        entrega_source = json.loads((example.parent/"ejemplo-acta-entrega.json").read_text())
        ers, ers_pdf = build("especificacion-requisitos", ers_source)
        assert ers["pages"] == 7, ers["pages"]
        assert ers["document"]["kind"] == "especificacion-requisitos"
        assert choices(ers_source) == []
        ers_text = " ".join(page.extract_text() or "" for page in PdfReader(ers_pdf).pages)
        ers_items = [item for block in (
            find_block(ers_source, "requisitos-funcionales"),
            find_block(ers_source, "requisitos-no-funcionales")) for item in block["items"]]
        atp_ids = {block["id"] for section in atp_source["sections"] for block in section.get("blocks", [])
                   if block.get("type") == "testcase"}
        deliverables = {row[0] for row in find_block(alcance_chain, "entregas")["rows"]}
        ers_flat = " ".join(ers_text.split())
        for item in ers_items:
            assert item["id"] in ers_flat and item["deliverable"] in ers_flat
            assert " ".join(item["statement"].split()) in ers_flat
            for case in item["tests"]:
                if case != "Por definir":
                    assert case in atp_ids, case
                    assert case in ers_flat
            assert item["deliverable"] in deliverables
        assert "Por definir" in ers_text and "Propuesto" in ers_text
        matrix_page = next(page.extract_text() or "" for page in PdfReader(ers_pdf).pages
                           if "Matriz de trazabilidad" in (page.extract_text() or ""))
        assert "RF-07" in matrix_page and "Por definir" in matrix_page and "E5" in matrix_page
        assert "RF-01" in matrix_page and "CP-03" in matrix_page
        last = PdfReader(ers_pdf).pages[-1].extract_text() or ""
        assert "Histórico de revisiones" in last and "Pendiente" in last and "Marta Quiroga" in last
        checks.append({"case": "especificacion-requisitos", "pages": ers["pages"], "requirements": len(ers_items)})

        assert date.fromisoformat(alcance_chain["document"]["date"]) < date.fromisoformat(ers_source["document"]["date"])
        assert date.fromisoformat(atp_source["document"]["date"]) < date.fromisoformat(ers_source["document"]["date"])
        assert date.fromisoformat(ers_source["document"]["date"]) < date.fromisoformat(cap_source["document"]["date"])
        assert date.fromisoformat(cap_source["document"]["date"]) < date.fromisoformat(entrega_source["document"]["date"])
        ers_json = json.dumps(ers_source, ensure_ascii=False)
        for shared in ("DEMO-REQ-014", "27/10/2026", "95 %", "5 segundos", "360 píxeles",
                       "Soledad Paredes", "DEMO-CAP-01", "07/01/2027", "DEMO-RIE-01", "DEMO-ALC-01"):
            assert shared in ers_json, shared
        checks.append({"case": "especificacion-coherente-con-la-cadena"})

        without_glossary = copy.deepcopy(ers_source)
        purpose = next(section for section in without_glossary["sections"] if section["id"] == "proposito")
        purpose["blocks"] = [block for block in purpose["blocks"] if block.get("type") != "table"]
        no_glossary, no_glossary_pdf = build("especificacion-sin-glosario", without_glossary)
        no_glossary_text = " ".join(page.extract_text() or "" for page in PdfReader(no_glossary_pdf).pages)
        assert "Campos alojados" not in no_glossary_text and "RF-01" in no_glossary_text
        assert no_glossary["pages"] <= ers["pages"]
        checks.append({"case": "especificacion-sin-glosario", "pages": no_glossary["pages"]})

        functional_only = copy.deepcopy(ers_source)
        functional_only["sections"] = [section for section in functional_only["sections"]
                                       if section["id"] != "no-funcionales"]
        only_rf, only_rf_pdf = build("especificacion-solo-funcionales", functional_only)
        only_text = " ".join(page.extract_text() or "" for page in PdfReader(only_rf_pdf).pages)
        assert "RNF-01" not in only_text and "RF-07" in only_text
        checks.append({"case": "especificacion-solo-funcionales", "pages": only_rf["pages"]})

        renamed = copy.deepcopy(ers_source)
        functional = find_block(renamed, "requisitos-funcionales")
        functional["priorities"] = ["Esencial", "Alta", "Media", "Baja"]
        functional["items"][0]["priority"] = "Esencial"
        _, renamed_pdf = build("especificacion-prioridad-propia", renamed)
        assert "Esencial" in " ".join(page.extract_text() or "" for page in PdfReader(renamed_pdf).pages)
        checks.append({"case": "especificacion-prioridad-propia"})

        for with_logo in (False, True):
            custom = copy.deepcopy(ers_source)
            custom["brand"].update(entity="Organización de prueba", unit="Oficina de Requisitos", accent="#7A2E1D")
            custom["document"].update(code="ACME-ERS-03", paper="Letter", status="En revisión")
            find_block(custom, "firmas")["rows"][0][1] = "Persona de prueba\nCargo de prueba"
            if with_logo:
                custom["brand"]["logo"] = "test-logo.png"
            personalized, personalized_pdf = build("especificacion-"+("logo" if with_logo else "sin-logo"), custom)
            first_page = PdfReader(personalized_pdf).pages[0].extract_text() or ""
            assert personalized["paper"] == "Letter" and "ACME-ERS-03" in first_page
            assert "Oficina de Requisitos" in first_page
            assert ("Organización de prueba" in first_page) != with_logo
            assert any(asset["path"] == "test-logo.png" for asset in personalized["assets"]) == with_logo
            checks.append({"case": "especificacion-personalizada", "logo": with_logo, "pages": personalized["pages"]})

        indexed_ers = copy.deepcopy(ers_source)
        indexed_ers["document"]["indexes"] = ["tables"]
        indexed_ers_result, indexed_ers_pdf = build("especificacion-con-indice", indexed_ers)
        assert "Índice de tablas" in (PdfReader(indexed_ers_pdf).pages[0].extract_text() or "")
        checks.append({"case": "especificacion-con-indice", "pages": indexed_ers_result["pages"]})

        broken_ers = copy.deepcopy(ers_source)
        find_block(broken_ers, section_id="referencia", kind="fields")["items"].append(
            {"label": "Idioma", "options": ["Español", "Inglés"], "selected": "Francés"})
        rejected_with("especificacion-eleccion-fuera-de-las-opciones", broken_ers, "exactamente una de las options")

        def break_requirements(name, mutate, message):
            variant = copy.deepcopy(ers_source)
            mutate(variant)
            rejected_with(name, variant, message)

        break_requirements("requisito-id-repetido",
                           lambda source: find_block(source, "requisitos-funcionales")["items"][1].update(id="RF-01"),
                           "está repetido")
        break_requirements("requisito-prioridad-fuera-de-la-lista",
                           lambda source: find_block(source, "requisitos-funcionales")["items"][0].update(priority="Urgente"),
                           "no está entre las etiquetas")
        break_requirements("requisito-aprobado-sin-metodo",
                           lambda source: find_block(source, "requisitos-funcionales")["items"][0].update(method="Por definir"),
                           "el método es 'Por definir'")
        break_requirements("requisito-aprobado-sin-caso",
                           lambda source: find_block(source, "requisitos-funcionales")["items"][0].update(tests=["Por definir"]),
                           "los casos son 'Por definir'")
        break_requirements("requisito-enunciado-sin-forma",
                           lambda source: find_block(source, "requisitos-funcionales")["items"][0].update(statement="Confirmar la reserva."),
                           "debe empezar por")
        break_requirements("requisito-dos-oraciones",
                           lambda source: find_block(source, "requisitos-funcionales")["items"][0].update(
                               statement="El sistema debe cobrar. El sistema debe registrar."),
                           "una sola oración")
        break_requirements("requisito-estados-sin-verificados",
                           lambda source: find_block(source, "requisitos-funcionales").update(
                               states=["Borrador", "Cerrado"]),
                           "verified_states")
        break_requirements("matriz-escrita-a-mano",
                           lambda source: find_block(source, "matriz-trazabilidad").update(
                               rows=[["RF-01", "otra fuente", "E9", "CP-99", "Prueba", "Aprobado"]]),
                           "no se escribe a mano")
        break_requirements("matriz-antes-de-los-requisitos",
                           lambda source: source["sections"].insert(0, source["sections"].pop(
                               next(i for i, section in enumerate(source["sections"]) if section["id"] == "trazabilidad"))),
                           "la matriz está antes")

        # ---- Ficha de modelo: una casilla de estado y cifras con procedencia ----
        mod_source = json.loads((example.parent/"ejemplo-ficha-modelo.json").read_text())
        risk_chain = json.loads((example.parent/"ejemplo-registro-riesgos.json").read_text())
        mod, mod_pdf = build("ficha-modelo", mod_source)
        assert mod["pages"] == 4, mod["pages"]
        assert mod["document"]["kind"] == "ficha-modelo"
        mod_choices = choices(mod_source)
        assert len(mod_choices) == 1 and mod_choices[0]["selected"] == "En validación"
        mod_text = " ".join(" ".join((page.extract_text() or "").split()) for page in PdfReader(mod_pdf).pages)
        for piece in ("sintéticos", "demostración", "DEMO-ATP-01", "0,80", "+0,04", "-0,04",
                      "Por confirmar", "canal telefónico", "DEMO-RIE-01", "Soledad Paredes", "DEMO-EID-01"):
            assert piece in mod_text, piece
        assert "impacto en datos: Por confirmar" not in mod_text, "La ficha cita la evaluación de impacto por su código"
        with pdfplumber.open(mod_pdf) as printed:
            diagonals = [line for page in printed.pages for line in page.lines
                         if abs(line["x0"] - line["x1"]) > 1 and abs(line["top"] - line["bottom"]) > 1]
        assert len(diagonals) == 2, len(diagonals)
        def spanish_number(text):
            return float(text.replace("+", "").replace(",", "."))
        group_rows = find_block(mod_source, "grupos")["rows"]
        sizes = [int(row[1]) for row in group_rows]
        values = [spanish_number(row[2]) for row in group_rows]
        overall = spanish_number(find_block(mod_source, "metricas")["rows"][0][1])
        assert abs(sum(size * value for size, value in zip(sizes, values)) / sum(sizes) - overall) < 1e-9
        for row, value in zip(group_rows, values):
            assert abs(spanish_number(row[3]) - (value - overall)) < 1e-9
        assert sum(sizes) == 100
        last_mod = PdfReader(mod_pdf).pages[-1].extract_text() or ""
        assert "Histórico de revisiones" in last_mod and "Pendiente" in last_mod and "Rafael Mena" in last_mod
        assert date.fromisoformat(atp_source["document"]["date"]) < date.fromisoformat(mod_source["document"]["date"])
        assert date.fromisoformat(mod_source["document"]["date"]) < date.fromisoformat(entrega_source["document"]["date"])
        risk_ids = {item["id"] for section in risk_chain["sections"] for block in section.get("blocks", [])
                    if block.get("type") == "risks" for item in block.get("items", [])}
        assert {"R-06", "R-08"} <= risk_ids
        checks.append({"case": "ficha-modelo", "pages": mod["pages"], "overall": overall})

        for with_logo in (False, True):
            custom = copy.deepcopy(mod_source)
            custom["brand"].update(entity="Organización de prueba", unit="Oficina de Modelos", accent="#7A2E1D")
            custom["document"].update(code="ACME-MOD-02", paper="Letter", status="En revisión")
            find_block(custom, "firmas")["rows"][0][1] = "Persona de prueba\nCargo de prueba"
            if with_logo:
                custom["brand"]["logo"] = "test-logo.png"
            personalized, personalized_pdf = build("ficha-"+("logo" if with_logo else "sin-logo"), custom)
            first_page = PdfReader(personalized_pdf).pages[0].extract_text() or ""
            assert personalized["paper"] == "Letter" and "ACME-MOD-02" in first_page
            assert "Oficina de Modelos" in first_page
            assert ("Organización de prueba" in first_page) != with_logo
            checks.append({"case": "ficha-personalizada", "logo": with_logo, "pages": personalized["pages"]})

        unmarked = copy.deepcopy(mod_source)
        without_choices(unmarked)
        rejected_with("ficha-sin-estado", unmarked, "estado del modelo")
        invalid_state = copy.deepcopy(mod_source)
        choices(invalid_state)[0]["selected"] = "En producción"
        rejected_with("ficha-estado-fuera-de-las-opciones", invalid_state, "exactamente una de las options")

        # ---- Evaluación de impacto en datos: tamizaje, dos casillas, riesgos de las personas y variante breve ----
        import re
        from datetime import date
        from build_report import levels_in_matrix_order, matrix_level, open_risk_rows, validate_risks
        eid_source = json.loads((example.parent/"ejemplo-evaluacion-impacto-datos.json").read_text())
        arq_source = json.loads((example.parent/"ejemplo-descripcion-arquitectura.json").read_text())

        def field_value(source, label):
            return next(item["value"] for section in source["sections"] for b in section.get("blocks", [])
                        if b["type"] == "fields" for item in b["items"] if item.get("label") == label)

        def flat(text):
            return " ".join((text or "").split())

        eid, eid_pdf = build("evaluacion-impacto-datos", eid_source)
        assert eid["pages"] == 10, eid["pages"]
        assert eid["document"]["kind"] == "evaluacion-impacto-datos"
        eid_choices = choices(eid_source)
        assert [item["label"] for item in eid_choices] == ["Conclusión del tamizaje", "Decisión"]
        assert [item["selected"] for item in eid_choices] == [
            "Evaluación completa por confirmar", "Consultar a asesoría legal o a la autoridad"]
        assert assert_choices(eid_pdf, eid_source) == 2
        eid_pages = {entry["id"]: entry["page"] for entry in eid["entries"]}
        with pdfplumber.open(eid_pdf) as printed:
            eid_texts = [flat(pg.extract_text()) for pg in printed.pages]
        # Every table is whole: its first and last row print on the page where its title is registered.
        for table_id, column in (("preguntas", 1), ("datos-tratados", 0), ("medidas", 0), ("firmas", 0)):
            rows = find_block(eid_source, table_id)["rows"]
            for row in (rows[0], rows[-1]):
                assert flat(row[column].split("\n")[0])[:12] in eid_texts[eid_pages[table_id]-1], (table_id, row)
        assert eid_pages["firmas"] == eid["pages"] and "Histórico de revisiones" in eid_texts[-1]
        assert "Pendiente" in eid_texts[-1] and check(eid_pdf)["internal_links"] >= 10
        metadata = PdfReader(eid_pdf).metadata
        assert metadata.author == "Entidad de demostración" and eid_source["document"]["code"] in metadata.subject

        # The risk block carries the persons' vocabulary: levels come from the matrix, each card is whole and the
        # closed risk stays out of the count of open ones.
        eid_block = find_block(eid_source, "matriz-riesgos")
        checked_block = copy.deepcopy(eid_block)
        validate_risks(checked_block)
        assert open_risk_rows(checked_block) == [
            ["Bajo", "2", "{{ref:RD-02}}, {{ref:RD-04}}"],
            ["Medio", "2", "{{ref:RD-01}}, {{ref:RD-05}}"],
            ["Alto", "1", "{{ref:RD-03}}"],
            ["Muy alto", "0", "Ninguno"],
            ["Total de abiertos", "5", ""],
        ]
        assert all(item["id"].startswith("RD-") for item in eid_block["items"]), "Prefijo propio, distinto de R-nn"
        for position, item in enumerate(eid_block["items"]):
            level = matrix_level(eid_block["scale"], item["probability"], item["impact"])
            assert checked_block["items"][position]["_level"] == level
            page_text = eid_texts[eid_pages[item["id"]]-1]
            assert f'{item["id"]} Nivel: {level}' in page_text, (item["id"], level)
            # The label cell is centered, so text extraction can interleave it between lines: compare word by word.
            assert all(word in page_text for word in flat(item["cause"])[:30].split() + flat(item["action"])[-20:].split()[1:]), item["id"]
        assert [item["id"] for item in eid_block["items"] if item["state"] == "Cerrado"] == ["RD-06"]
        summary_text = eid_texts[eid_pages["resumen-riesgos"]-1]
        assert "Total de abiertos 5" in summary_text and "Muy alto 0 Ninguno" in summary_text
        assert "Riesgos abiertos para las personas, por nivel" in summary_text
        assert "Materializado" not in " ".join(eid_texts) and "Respuestas admitidas: Reducir" in " ".join(eid_texts)
        # The residual risk is the highest level among the open ones.
        order = levels_in_matrix_order(eid_block["scale"]["matrix"])
        open_items = [item for item in checked_block["items"] if item["state"] in checked_block["_open_states"]]
        highest = max((item["_level"] for item in open_items), key=order.index)
        residual = field_value(eid_source, "Riesgo residual")
        assert residual.startswith(highest) and all(item["id"] in residual for item in open_items if item["_level"] == highest)

        # Measures and risks reference each other: every risk has a measure, every measure cites a risk of the document.
        measures = find_block(eid_source, "medidas")["rows"]
        cited_risks = {key for row in measures for key in re.findall(r"\{\{ref:([A-Za-z0-9_-]+)\}\}", row[1])}
        risk_ids = {item["id"] for item in eid_block["items"]}
        assert cited_risks == risk_ids, cited_risks ^ risk_ids
        assert [row[0][:4] for row in measures] == [f"M-{i:02d}" for i in range(1, len(measures)+1)]
        assert {row[3] for row in measures} <= {"Implementada", "Prevista", "Pendiente"}
        for item in eid_block["items"]:
            if item["state"] in ("Abierto", "En reducción"):
                measure_states = {row[3] for row in measures if "{{ref:" + item["id"] + "}}" in row[1]}
                expected_state = "En reducción" if measure_states & {"Prevista", "Implementada"} else "Abierto"
                assert item["state"] == expected_state, (item["id"], item["state"], measure_states)
        assert "Implementada" not in {row[3] for row in measures}, "Antes de construir ninguna medida técnica está implementada"
        mentioned = set(re.findall(r"M-\d\d", " ".join(item["action"] for item in eid_block["items"])
                                   + " " + field_value(eid_source, "Alternativas menos intrusivas")))
        assert mentioned <= {row[0][:4] for row in measures}, mentioned
        people = ("Marta Quiroga", "Soledad Paredes", "Iván Salas", "Lucía Ferrer", "Rafael Mena", "Julián Benítez",
                  "Camila Ortega", "Diego Arce")
        by_role = (field_value(eid_source, "Responsable del tratamiento") + field_value(eid_source, "Encargados del tratamiento")
                   + " ".join(row[2] for row in measures) + " ".join(item["owner"] for item in eid_block["items"]))
        assert not any(name in by_role for name in people), "Responsables por rol, no por persona"

        # The tamizaje conclusion is the one the rule gives with the answers of the table.
        def tamizaje_conclusion(answers):
            assert len(answers) == 7 and set(answers) <= {"Sí", "No", "Por confirmar"}, answers
            if answers[0] == "No":
                return "Evaluación completa no necesaria"
            if "Sí" in answers[1:]:
                return "Evaluación completa necesaria"
            if answers[0] == "Sí" and set(answers[1:]) == {"No"}:
                return "Evaluación completa no necesaria"
            return "Evaluación completa por confirmar"

        for answers, expected in [
            (["No"]*7, "Evaluación completa no necesaria"),
            (["Sí"] + ["No"]*6, "Evaluación completa no necesaria"),
            (["Sí", "No", "Sí", "No", "No", "No", "No"], "Evaluación completa necesaria"),
            (["Por confirmar", "Sí"] + ["No"]*5, "Evaluación completa necesaria"),
            (["Sí", "Por confirmar"] + ["No"]*5, "Evaluación completa por confirmar"),
            (["Por confirmar"] + ["No"]*6, "Evaluación completa por confirmar"),
        ]:
            assert tamizaje_conclusion(answers) == expected, (answers, expected)
        eid_answers = [row[2] for row in find_block(eid_source, "preguntas")["rows"]]
        assert tamizaje_conclusion(eid_answers) == eid_choices[0]["selected"]
        checks.append({"case": "eid-regla-del-tamizaje", "answers": eid_answers})

        # Fields nobody confirmed stay «Por confirmar con asesoría legal», and the decision does not say it can go ahead.
        for label in ("Marco normativo aplicable", "Autoridad de protección de datos", "Base de licitud",
                      "Retención y supresión", "Transferencias fuera del país"):
            assert field_value(eid_source, label).startswith("Por confirmar con asesoría legal"), label
        assert field_value(eid_source, "Delegado de protección de datos") == "Por confirmar"
        assert field_value(eid_source, "Volumen aproximado").startswith("Por estimar")
        assert eid_choices[1]["selected"] != "Continúa sin medidas adicionales"
        notice = [b for s in eid_source["sections"] if s["id"] == "referencia" for b in s["blocks"] if b["type"] == "note"]
        assert len(notice) == 1 and "No es asesoría legal" in notice[0]["text"]
        eid_text = json.dumps(eid_source, ensure_ascii=False)
        for claim in ("cumple con", "es lícito", "conforme a la ley", "obligatoria por ley"):
            assert claim not in eid_text, claim
        assert [change["summary"] for change in eid_source["changes"]] == ["Primera versión."]
        assert eid_source["document"]["status"] == "Demostración" and eid_source["document"]["version"] == "0.1"
        checks.append({"case": "evaluacion-impacto-datos", "pages": eid["pages"], "open": 5})

        # The chain: codes cited exist, the cited risks of the project register are the ones stated there, the dates
        # fall between the architecture description and the build, and people and roles repeat those of the chain.
        chain_codes = {json.loads(path.read_text())["document"]["code"] for path in example.parent.glob("ejemplo-*.json")}
        assert set(re.findall(r"DEMO-[A-Z]{3}-\d{2,3}", eid_text)) <= chain_codes, "Código citado que no existe"
        project_risks = {item["id"]: item for item in find_block(risk_source, "matriz-niveles")["items"]}
        for risk_id in re.findall(r"(R-\d\d)(?: de|, [a-zA-Z ]+ de) DEMO-RIE-01", eid_text) + ["R-07"]:
            assert risk_id in project_risks, risk_id
        assert project_risks["R-07"]["state"] == "Cerrado" and "09/11/2026" in eid_text
        eid_date = date.fromisoformat(eid_source["document"]["date"])
        assert date.fromisoformat(arq_source["document"]["date"]) < eid_date < date(2026, 11, 23)
        assert "23/11/2026" in json.dumps(alcance_source, ensure_ascii=False)
        assert eid_date < date.fromisoformat(mod_source["document"]["date"])
        assert eid_source["document"]["code"] in field_value(mod_source, "Datos personales"), "La ficha cita esta evaluación"
        review_day, review_month, review_year = map(int, field_value(eid_source, "Fecha de revisión").split(",")[0].split("/"))
        assert date(review_year, review_month, review_day) > eid_date
        for person in ("Marta Quiroga", "Soledad Paredes"):
            assert person in eid_text and person in json.dumps(alcance_source, ensure_ascii=False), person
        assert "Arquitecta de software" in eid_text and "Jefa de operaciones de reservas" in eid_text
        for phrase in ("campos alojados", "15 minutos", "DEMO-REQ-014"):
            assert phrase in eid_text and phrase in json.dumps(feasibility_source, ensure_ascii=False) + json.dumps(
                registro_source, ensure_ascii=False) + json.dumps(alcance_source, ensure_ascii=False), phrase
        checks.append({"case": "eid-coherente-con-la-cadena"})

        # Identity, code, paper and signers are configurable, with and without a logo.
        for with_logo in (False, True):
            custom = copy.deepcopy(eid_source)
            custom["brand"].update(entity="Organización de prueba", unit="Oficina de Datos", accent="#7A2E1D")
            custom["document"].update(code="ACME-EID-03", paper="Letter", status="En revisión")
            find_block(custom, "firmas")["rows"][0][1] = "Persona de prueba\nCargo de prueba"
            if with_logo:
                custom["brand"]["logo"] = "test-logo.png"
            personalized, personalized_pdf = build("eid-"+("logo" if with_logo else "sin-logo"), custom)
            first_page = PdfReader(personalized_pdf).pages[0].extract_text() or ""
            assert personalized["paper"] == "Letter" and "ACME-EID-03" in first_page
            assert "Oficina de Datos" in first_page
            assert ("Organización de prueba" in first_page) != with_logo
            assert any(asset["path"] == "test-logo.png" for asset in personalized["assets"]) == with_logo
            assert assert_choices(personalized_pdf, custom) == 2
            checks.append({"case": "eid-personalizada", "logo": with_logo, "pages": personalized["pages"]})

        indexed_eid = copy.deepcopy(eid_source)
        indexed_eid["document"]["indexes"] = ["contents", "tables"]
        indexed_eid_result, indexed_eid_pdf = build("eid-con-indices", indexed_eid)
        indexed_first = PdfReader(indexed_eid_pdf).pages[0].extract_text() or ""
        assert "Contenido" in indexed_first and "Índice de tablas" in indexed_first
        assert "Matriz de niveles de riesgo para las personas" in indexed_first
        checks.append({"case": "eid-con-indices", "pages": indexed_eid_result["pages"]})

        # Optional part 1, the brief variant: with a tamizaje that rules out the full evaluation only the reference,
        # the tamizaje, the decision and the signatures stay, and the sections are renumbered.
        brief = copy.deepcopy(eid_source)
        brief["sections"] = [s for s in brief["sections"]
                             if s["id"] in ("referencia", "tamizaje", "conclusion", "responsabilidad")]
        for index, row in enumerate(find_block(brief, "preguntas")["rows"]):
            row[2] = "Sí" if index == 0 else "No"
            row[3] = "Consta en los documentos del proyecto."
        choices(brief)[0]["selected"] = "Evaluación completa no necesaria"
        assert tamizaje_conclusion([row[2] for row in find_block(brief, "preguntas")["rows"]]) == choices(brief)[0]["selected"]
        find_block(brief, section_id="referencia", kind="paragraph")["text"] = (
            "El tamizaje descarta la evaluación completa del módulo de pagos, así que este documento queda con la "
            "información de referencia, el tamizaje, la decisión y las firmas.")
        find_block(brief, section_id="tamizaje", kind="paragraph")["text"] = (
            "El tamizaje concluye que la evaluación completa no es necesaria: el tratamiento usa datos personales y "
            "ninguna otra pregunta tiene un Sí ni un Por confirmar.")
        find_block(brief, section_id="conclusion", kind="paragraph")["text"] = (
            "Continúa sin medidas adicionales. El tamizaje descarta la evaluación completa y no hay riesgos que valorar.")
        choices(brief)[1]["selected"] = "Continúa sin medidas adicionales"
        next(item for b in find_block(brief, section_id="conclusion", kind="fields")["items"]
             for item in [b] if item["label"] == "Riesgo residual")["value"] = "No aplica. No se elaboró la evaluación completa."
        brief_result, brief_pdf = build("evaluacion-impacto-datos-breve", brief)
        assert brief_result["labels"]["conclusion"].startswith("3. ") and brief_result["labels"]["responsabilidad"].startswith("4. ")
        brief_text = " ".join(flat(pg.extract_text()) for pg in PdfReader(brief_pdf).pages)
        for gone in ("Descripción del Tratamiento", "Necesidad y Proporcionalidad", "Matriz de niveles", "Medidas y Salvaguardas",
                     "Supervisión Humana", "RD-0"):
            assert gone not in brief_text, gone
        assert "Preguntas del tamizaje" in brief_text and "No aplica. No se elaboró" in brief_text
        assert "propone consultar" not in brief_text, "La apertura del documento completo se reescribe"
        assert brief_result["pages"] == 3, brief_result["pages"]
        assert assert_choices(brief_pdf, brief) == 2
        assert any(entry["id"] == "firmas" and entry["page"] == brief_result["pages"] for entry in brief_result["entries"])
        checks.append({"case": "eid-variante-breve", "pages": brief_result["pages"]})
        stale = copy.deepcopy(brief)
        find_block(stale, section_id="conclusion", kind="paragraph")["text"] += " Ver {{ref:medidas}}."
        rejected_with("eid-breve-con-referencia-a-un-apartado-eliminado", stale, "Referencia desconocida: medidas")

        # Optional part 2, human supervision: «No aplica» in the example; when there are automated decisions the section
        # carries who decides, how it is challenged and the model sheet by its code, and the tamizaje says so.
        automated = copy.deepcopy(eid_source)
        find_block(automated, "preguntas")["rows"][3][2] = "Sí"
        choices(automated)[0]["selected"] = "Evaluación completa necesaria"
        assert tamizaje_conclusion([row[2] for row in find_block(automated, "preguntas")["rows"]]) == choices(automated)[0]["selected"]
        next(s for s in automated["sections"] if s["id"] == "supervision")["blocks"] = [{"type": "fields", "items": [
            {"label": "Decisiones automatizadas", "value": "Sí. Un modelo marca los pagos que Operaciones de reservas revisa en la conciliación diaria."},
            {"label": "Quién decide", "value": "Una persona de operaciones de reservas. El modelo recomienda y no decide."},
            {"label": "Cómo se impugna", "value": "La persona afectada pide la revisión por el canal de Operaciones de reservas. Plazo y responsable: Por confirmar con asesoría legal."},
            {"label": "Ficha de modelo", "value": mod_source["document"]["code"]}]}]
        automated_result, automated_pdf = build("eid-con-decisiones-automatizadas", automated)
        automated_text = " ".join(flat(pg.extract_text()) for pg in PdfReader(automated_pdf).pages)
        assert "Quién decide" in automated_text and "Cómo se impugna" in automated_text and "DEMO-MOD-01" in automated_text
        assert assert_choices(automated_pdf, automated) == 2
        assert automated_result["pages"] in (eid["pages"], eid["pages"]+1), automated_result["pages"]
        checks.append({"case": "eid-con-decisiones-automatizadas", "pages": automated_result["pages"]})

        # Rejections: the family rule for the single-mark decision, and the traps of the persons' vocabulary.
        unmarked_eid = copy.deepcopy(eid_source)
        without_choices(unmarked_eid)
        rejected_with("eid-sin-ninguna-eleccion", unmarked_eid, "evaluacion-impacto-datos requiere la decisión marcada")
        wrong_decision = copy.deepcopy(eid_source)
        choices(wrong_decision)[1]["selected"] = "Aprobar"
        rejected_with("eid-decision-fuera-de-las-opciones", wrong_decision, "exactamente una de las options")
        two_decisions = copy.deepcopy(eid_source)
        choices(two_decisions)[1]["selected"] = ["Continúa sin medidas adicionales", "Continúa con medidas"]
        rejected_with("eid-decision-con-dos-marcas", two_decisions, "multiple")

        def break_eid_risks(name, mutate, message):
            variant = copy.deepcopy(eid_source)
            mutate(find_block(variant, "matriz-riesgos"))
            rejected_with(name, variant, message)

        break_eid_risks("eid-estados-propios-sin-abiertos", lambda block: block.pop("open_states"), "indicar también open_states")
        break_eid_risks("eid-probabilidad-de-otra-escala", lambda block: block["items"][0].update(probability="Media"),
                        "la probabilidad 'Media'")
        break_eid_risks("eid-estado-copiado-de-un-registro-de-proyecto",
                        lambda block: block["items"][0].update(state="En mitigación"), "el estado 'En mitigación'")
        break_eid_risks("eid-respuesta-copiada-de-un-registro-de-proyecto",
                        lambda block: block["items"][0].update(response="Mitigar"), "la respuesta 'Mitigar'")
        unknown_measure_risk = copy.deepcopy(eid_source)
        find_block(unknown_measure_risk, "medidas")["rows"][0][1] = "{{ref:RD-09}}"
        rejected_with("eid-medida-con-un-riesgo-inexistente", unknown_measure_risk, "Referencia desconocida: RD-09")

        from test_lifecycle import run_checks as check_lifecycle
        check_lifecycle(example, root, checks, build, rejected_with)

        from test_cierre import run_checks as check_cierre
        check_cierre(example, root, checks, build, rejected_with)

        from test_baja import run_checks as check_baja
        check_baja(example, root, checks, build, rejected_with)

        from test_proceso import run_checks as check_proceso
        check_proceso(example, root, checks, build, rejected_with)

        # ---- Solicitud de cambio: la diferencia sale del antes y el después ----
        scm_source = json.loads((example.parent/"ejemplo-solicitud-cambio.json").read_text())
        alcance_source = json.loads((example.parent/"ejemplo-alcance-proyecto.json").read_text())
        scm, scm_pdf = build("solicitud-cambio", scm_source)
        assert scm["pages"] == 4, scm["pages"]
        assert scm["document"]["kind"] == "solicitud-cambio"
        scm_choices = choices(scm_source)
        assert len(scm_choices) == 1 and scm_choices[0]["selected"] == "Diferida"
        scm_text = " ".join(" ".join((page.extract_text() or "").split()) for page in PdfReader(scm_pdf).pages)
        for piece in ("DEMO-SCM-01", "DEMO-ALC-01", "versión 0.2", "20/11/2026", "Soledad Paredes",
                      "pagos recurrentes", "50", "Por estimar", "R-04", "R-08", "CP-01", "DEMO-FAC-01",
                      "Por registrar", "Lucía Ferrer"):
            assert piece in scm_text, piece
        with pdfplumber.open(scm_pdf) as printed:
            scm_diagonals = [line for page in printed.pages for line in page.lines
                             if abs(line["x0"] - line["x1"]) > 1 and abs(line["top"] - line["bottom"]) > 1]
        assert len(scm_diagonals) == 2, len(scm_diagonals)
        impact_rows = find_block(scm_source, "diferencia")["rows"]
        assert impact_rows[0]["before"] == 50 and impact_rows[0]["after"] == 50
        assert impact_rows[1]["after"] == "Por estimar"
        assert "50 días-persona" in json.dumps(alcance_source, ensure_ascii=False)
        assert "pagos recurrentes" in json.dumps(alcance_source, ensure_ascii=False)
        assert alcance_source["document"]["version"] == "0.2"
        assert alcance_source["document"]["date"] < scm_source["document"]["date"] < entrega_source["document"]["date"]
        assert "23/11/2026" in scm_text and "10/01/2027" in scm_text
        last_scm = PdfReader(scm_pdf).pages[-1].extract_text() or ""
        assert "Histórico de revisiones" in last_scm and "Pendiente" in last_scm and "7. Firmas" in last_scm
        checks.append({"case": "solicitud-cambio", "pages": scm["pages"]})

        no_impact = copy.deepcopy(scm_source)
        for section in no_impact["sections"]:
            section["blocks"] = [block for block in section["blocks"] if block.get("type") != "impact"]
        no_impact_built, no_impact_pdf = build("solicitud-sin-impacto", no_impact)
        no_impact_text = " ".join((page.extract_text() or "") for page in PdfReader(no_impact_pdf).pages)
        assert "días-persona" not in no_impact_text
        checks.append({"case": "solicitud-sin-impacto", "pages": no_impact_built["pages"]})

        half = copy.deepcopy(scm_source)
        find_block(half, "diferencia")["rows"][0]["after"] = 52.5
        _, half_pdf = build("solicitud-diferencia", half)
        assert "2,5" in " ".join((page.extract_text() or "") for page in PdfReader(half_pdf).pages)

        indexed = copy.deepcopy(scm_source)
        indexed["document"]["indexes"] = ["tables"]
        indexed_built, _ = build("solicitud-indice", indexed)
        assert any(entry["id"] == "diferencia" for entry in indexed_built["entries"])

        for with_logo in (False, True):
            custom = copy.deepcopy(scm_source)
            custom["brand"].update(entity="Organización de prueba", unit="Oficina de Cambios", accent="#7A2E1D")
            custom["document"].update(code="ACME-SCM-02", paper="Letter", status="En revisión")
            find_block(custom, "responsables")["rows"][0][1] = "Persona de prueba\nCargo de prueba"
            if with_logo:
                custom["brand"]["logo"] = "test-logo.png"
            personalized, personalized_pdf = build("solicitud-"+("logo" if with_logo else "sin-logo"), custom)
            first_page = PdfReader(personalized_pdf).pages[0].extract_text() or ""
            assert personalized["paper"] == "Letter" and "ACME-SCM-02" in first_page
            assert "Oficina de Cambios" in first_page
            assert ("Organización de prueba" in first_page) != with_logo
            checks.append({"case": "solicitud-personalizada", "logo": with_logo, "pages": personalized["pages"]})

        unmarked = copy.deepcopy(scm_source)
        without_choices(unmarked)
        rejected_with("solicitud-sin-decision", unmarked, "decisión marcada")
        invalid_decision = copy.deepcopy(scm_source)
        choices(invalid_decision)[0]["selected"] = "Aplazada"
        rejected_with("solicitud-decision-fuera-de-las-opciones", invalid_decision, "exactamente una de las options")

        def break_impact(name, mutate, message):
            variant = copy.deepcopy(scm_source)
            mutate(variant)
            rejected_with(name, variant, message)

        break_impact("impacto-diferencia-escrita",
                     lambda source: find_block(source, "diferencia")["rows"][0].update(difference=0),
                     "difference")
        break_impact("impacto-antes-no-numerico",
                     lambda source: find_block(source, "diferencia")["rows"][0].update(before="luego"),
                     "Por estimar")
        break_impact("impacto-tres-decimales",
                     lambda source: find_block(source, "diferencia")["rows"][0].update(after=1.234),
                     "2 decimales")

        # ---- Plan de proyecto: la EDT suma las hojas y deja fuera Por estimar ----
        ppr_source = json.loads((example.parent/"ejemplo-plan-proyecto.json").read_text())
        ppr, ppr_pdf = build("plan-proyecto", ppr_source)
        assert ppr["pages"] == 5, ppr["pages"]
        assert ppr["document"]["kind"] == "plan-proyecto"
        assert choices(ppr_source) == []
        ppr_text = " ".join(" ".join((page.extract_text() or "").split()) for page in PdfReader(ppr_pdf).pages)
        assert "El total de cada rama y el total general los calcula el motor." not in ppr_text
        assert "«Por estimar» queda visible y fuera de la suma." in ppr_text
        for piece in ("DEMO-PPR-01", "DEMO-ALC-01", "DEMO-SCM-01", "50", "Por estimar", "E5-3",
                      "23/11/2026", "10/01/2027", "R-04", "R-05", "R-08", "Camila Ortega",
                      "07/01/2027", "T-"):
            assert piece in ppr_text, piece

        def wbs_leaves(nodes):
            found = []
            for node in nodes:
                found.extend(wbs_leaves(node["children"]) if "children" in node else [node])
            return found

        wbs_nodes = find_block(ppr_source, "desglose")["nodes"]
        wbs_leaf_rows = wbs_leaves(wbs_nodes)
        assert sum(node["effort"] for node in wbs_leaf_rows if node["effort"] != "Por estimar") == 50
        assert any(node["effort"] == "Por estimar" for node in wbs_leaf_rows)
        assert {node["id"] for node in wbs_nodes} == {"E1", "E2", "E3", "E4", "E5"}
        alcance_codes = {row[0] for row in find_block(alcance_source, "entregas")["rows"]}
        assert {node["id"] for node in wbs_nodes} <= alcance_codes
        assert "50 días-persona" in json.dumps(alcance_source, ensure_ascii=False)
        risk_ids = {item["id"] for section in risk_chain["sections"] for block in section.get("blocks", [])
                    if block.get("type") == "risks" for item in block.get("items", [])}
        assert {"R-04", "R-05", "R-08"} <= risk_ids
        assert alcance_source["document"]["date"] < scm_source["document"]["date"] < ppr_source["document"]["date"]
        assert ppr_source["document"]["date"] < entrega_source["document"]["date"]
        last_ppr = PdfReader(ppr_pdf).pages[-1].extract_text() or ""
        assert "Histórico de revisiones" in last_ppr and "Pendiente" in last_ppr and "9. Firmas" in last_ppr
        checks.append({"case": "plan-proyecto", "pages": ppr["pages"], "total": 50})

        no_gap = copy.deepcopy(ppr_source)
        find_block(no_gap, "desglose")["nodes"][4]["children"].pop()
        no_gap_built, no_gap_pdf = build("plan-sin-hueco", no_gap)
        no_gap_text = " ".join((page.extract_text() or "") for page in PdfReader(no_gap_pdf).pages)
        assert "Guía del plazo" not in no_gap_text and "50" in no_gap_text
        checks.append({"case": "plan-sin-hueco", "pages": no_gap_built["pages"]})

        indexed_plan = copy.deepcopy(ppr_source)
        indexed_plan["document"]["indexes"] = ["tables"]
        indexed_plan_built, _ = build("plan-indice", indexed_plan)
        assert any(entry["id"] == "desglose" for entry in indexed_plan_built["entries"])

        for with_logo in (False, True):
            custom = copy.deepcopy(ppr_source)
            custom["brand"].update(entity="Organización de prueba", unit="Oficina de Planes", accent="#7A2E1D")
            custom["document"].update(code="ACME-PPR-02", paper="Letter", status="En revisión")
            find_block(custom, "responsables")["rows"][0][1] = "Persona de prueba\nCargo de prueba"
            if with_logo:
                custom["brand"]["logo"] = "test-logo.png"
            personalized, personalized_pdf = build("plan-"+("logo" if with_logo else "sin-logo"), custom)
            first_page = PdfReader(personalized_pdf).pages[0].extract_text() or ""
            assert personalized["paper"] == "Letter" and "ACME-PPR-02" in first_page
            assert "Oficina de Planes" in first_page
            assert ("Organización de prueba" in first_page) != with_logo
            checks.append({"case": "plan-personalizado", "logo": with_logo, "pages": personalized["pages"]})

        bad_choice = copy.deepcopy(ppr_source)
        find_block(bad_choice, section_id="referencia", kind="fields")["items"].append(
            {"label": "Estado", "options": ["Borrador", "Aprobado"], "selected": "Cerrado"})
        rejected_with("plan-eleccion-fuera-de-las-opciones", bad_choice, "exactamente una de las options")

        def break_wbs(name, mutate, message):
            variant = copy.deepcopy(ppr_source)
            mutate(variant)
            rejected_with(name, variant, message)

        break_wbs("edt-id-repetido",
                  lambda source: find_block(source, "desglose")["nodes"][0]["children"][1].update(id="E1-1"),
                  "está repetido")
        break_wbs("edt-total-escrito",
                  lambda source: find_block(source, "desglose").update(total=50),
                  "quitar total")
        break_wbs("edt-esfuerzo-en-rama",
                  lambda source: find_block(source, "desglose")["nodes"][0].update(effort=20),
                  "no las dos")
        break_wbs("edt-hoja-sin-esfuerzo",
                  lambda source: find_block(source, "desglose")["nodes"][0]["children"][0].pop("effort"),
                  "no las dos")
        break_wbs("edt-esfuerzo-negativo",
                  lambda source: find_block(source, "desglose")["nodes"][0]["children"][0].update(effort=-1),
                  "no puede ser negativo")

        # ---- Traspaso a operación: comprobaciones pendientes y sin secretos ----
        tra_source = json.loads((example.parent/"ejemplo-traspaso-operacion.json").read_text())
        tra, tra_pdf = build("traspaso-operacion", tra_source)
        assert tra["pages"] == 4, tra["pages"]
        assert tra["document"]["kind"] == "traspaso-operacion"
        assert choices(tra_source) == []
        tra_text = " ".join(" ".join((page.extract_text() or "").split()) for page in PdfReader(tra_pdf).pages)
        for piece in ("DEMO-TRA-01", "1.0.0", "08/01/2027", "04/01/2027", "10/01/2027", "R-08", "R-05",
                      "Pendiente", "Por confirmar", "Diego Arce", "DEMO-ENT-01", "DEMO-CAP-01",
                      "depósito de secretos", "no lleva claves"):
            assert piece in tra_text, piece
        checks_table = find_block(tra_source, "comprobaciones")["rows"]
        assert checks_table and all(row[-1] == "Pendiente" for row in checks_table)
        assert "Diego Arce" in json.dumps(entrega_source, ensure_ascii=False)
        atp_cases = {block["id"]: block for section in atp_source["sections"] for block in section.get("blocks", [])
                     if block.get("type") == "testcase"}
        for case_id in ("CP-01", "CP-02", "CP-05"):
            assert case_id in atp_cases and atp_cases[case_id]["executed"] is False
        assert ppr_source["document"]["date"] < tra_source["document"]["date"] == entrega_source["document"]["date"]
        cap_source = json.loads((example.parent/"ejemplo-acta-capacitacion.json").read_text())
        assert cap_source["document"]["date"] < tra_source["document"]["date"]
        last_tra = PdfReader(tra_pdf).pages[-1].extract_text() or ""
        assert "Histórico de revisiones" in last_tra and "Pendiente" in last_tra and "9. Firmas" in last_tra
        checks.append({"case": "traspaso-operacion", "pages": tra["pages"]})

        no_checks = copy.deepcopy(tra_source)
        no_checks["sections"] = [section for section in no_checks["sections"] if section["id"] != "verificacion"]
        no_checks_built, no_checks_pdf = build("traspaso-sin-comprobaciones", no_checks)
        no_checks_text = " ".join((page.extract_text() or "") for page in PdfReader(no_checks_pdf).pages)
        assert "Inspección externa" not in no_checks_text
        checks.append({"case": "traspaso-sin-comprobaciones", "pages": no_checks_built["pages"]})

        for with_logo in (False, True):
            custom = copy.deepcopy(tra_source)
            custom["brand"].update(entity="Organización de prueba", unit="Oficina de Operación", accent="#7A2E1D")
            custom["document"].update(code="ACME-TRA-02", paper="Letter", status="En revisión")
            find_block(custom, "responsables")["rows"][0][1] = "Persona de prueba\nCargo de prueba"
            if with_logo:
                custom["brand"]["logo"] = "test-logo.png"
            personalized, personalized_pdf = build("traspaso-"+("logo" if with_logo else "sin-logo"), custom)
            first_page = PdfReader(personalized_pdf).pages[0].extract_text() or ""
            assert personalized["paper"] == "Letter" and "ACME-TRA-02" in first_page
            assert "Oficina de Operación" in first_page
            assert ("Organización de prueba" in first_page) != with_logo
            checks.append({"case": "traspaso-personalizado", "logo": with_logo, "pages": personalized["pages"]})

        bad_handover = copy.deepcopy(tra_source)
        find_block(bad_handover, section_id="referencia", kind="fields")["items"].append(
            {"label": "Estado", "options": ["Preparado", "Hecho"], "selected": "Cerrado"})
        rejected_with("traspaso-eleccion-fuera-de-las-opciones", bad_handover, "exactamente una de las options")

        # ---- Notas de versión: lo entregado, sin adelantar pruebas ni el pedido diferido ----
        nov_source = json.loads((example.parent/"ejemplo-notas-version.json").read_text())
        nov, nov_pdf = build("notas-version", nov_source)
        assert nov["pages"] == 3, nov["pages"]
        assert nov["document"]["kind"] == "notas-version"
        assert choices(nov_source) == []
        nov_text = " ".join(" ".join((page.extract_text() or "").split()) for page in PdfReader(nov_pdf).pages)
        for piece in ("DEMO-NOV-01", "1.0.0", "08/01/2027", "DEMO-SCM-01", "diferida", "Por registrar",
                      "R-05", "R-04", "CP-01", "CP-05", "Sin ejecutar", "17/11/2026"):
            assert piece in nov_text, piece
        assert tra_source["document"]["date"] == nov_source["document"]["date"] == entrega_source["document"]["date"]
        listed_cases = {row[0] for row in find_block(nov_source, "casos")["rows"]}
        assert listed_cases == {"CP-01", "CP-02", "CP-03", "CP-04", "CP-05"}
        assert all(atp_cases[case_id]["executed"] is False for case_id in listed_cases)
        assert choices(scm_source)[0]["selected"] == "Diferida"
        change_types = {row[0] for row in find_block(nov_source, "lista")["rows"]}
        assert change_types == {"Nuevo"}
        last_nov = PdfReader(nov_pdf).pages[-1].extract_text() or ""
        assert "Histórico de revisiones" in last_nov and "Iván Salas" in last_nov  # the history may sit alone on the last page
        checks.append({"case": "notas-version", "pages": nov["pages"]})

        no_problems = copy.deepcopy(nov_source)
        no_problems["sections"] = [section for section in no_problems["sections"] if section["id"] != "problemas"]
        no_problems_built, no_problems_pdf = build("notas-sin-problemas", no_problems)
        no_problems_text = " ".join((page.extract_text() or "") for page in PdfReader(no_problems_pdf).pages)
        assert "Problemas que siguen abiertos" not in no_problems_text
        checks.append({"case": "notas-sin-problemas", "pages": no_problems_built["pages"]})

        for with_logo in (False, True):
            custom = copy.deepcopy(nov_source)
            custom["brand"].update(entity="Organización de prueba", unit="Oficina de Versiones", accent="#7A2E1D")
            custom["document"].update(code="ACME-NOV-02", paper="Letter", status="En revisión")
            if with_logo:
                custom["brand"]["logo"] = "test-logo.png"
            personalized, personalized_pdf = build("notas-"+("logo" if with_logo else "sin-logo"), custom)
            first_page = PdfReader(personalized_pdf).pages[0].extract_text() or ""
            assert personalized["paper"] == "Letter" and "ACME-NOV-02" in first_page
            assert "Oficina de Versiones" in first_page
            assert ("Organización de prueba" in first_page) != with_logo
            checks.append({"case": "notas-personalizadas", "logo": with_logo, "pages": personalized["pages"]})

        bad_notes = copy.deepcopy(nov_source)
        find_block(bad_notes, section_id="referencia", kind="fields")["items"].append(
            {"label": "Estado", "options": ["Borrador", "Publicada"], "selected": "Retirada"})
        rejected_with("notas-eleccion-fuera-de-las-opciones", bad_notes, "exactamente una de las options")

        from test_closing import run_checks as check_closing
        check_closing(example, root, checks, build)

        from test_quote_pending import run_checks as check_quote_pending
        check_quote_pending(example, root, checks, build, rejected_with)

        from test_risk_headings import run_checks as check_risk_headings
        check_risk_headings(example, root, checks, build)

        from test_deps import run_checks as check_deps
        check_deps(example, root, checks, build)

        from test_instalar import run_checks as check_instalar
        check_instalar(example, root, checks, build)

        from test_apa_rotulos import run_checks as check_apa_rotulos
        check_apa_rotulos(example, root, checks, build)

        from test_perfil_hibrido import run_checks as check_perfil_hibrido
        check_perfil_hibrido(example, root, checks, build, rejected_with)

        from test_mapa_calor import run_checks as check_mapa_calor
        check_mapa_calor(example, root, checks, build)

        from test_muestras import run_checks as check_muestras
        check_muestras(example, root, checks, build)

        from test_heading_case import run_checks as check_heading_case
        check_heading_case(example, root, checks, build, rejected_with)

        from test_header_name import run_checks as check_header_name
        check_header_name(example, root, checks, build, rejected_with)

        print(json.dumps({"ok":True,"checks":checks},ensure_ascii=False,indent=2))


if __name__ == "__main__":
    main()
