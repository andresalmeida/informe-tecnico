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

        for name, mutate in [
            ("unknown-reference",lambda x: x["sections"][0]["blocks"].append({"type":"paragraph","text":"{{ref:missing}}"})),
            ("duplicate-id",lambda x: x["sections"].append(copy.deepcopy(x["sections"][0]))),
            ("oversize-row",lambda x: table_by_id(x,"campos")["rows"].append(["LONG","Campo","Texto extenso "*3000,"Texto"])),
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
