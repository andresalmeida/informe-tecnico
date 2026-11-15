"""sentence is the form default. title must keep reproducing the output recorded in tests/golden/heading-title.json.

The golden file was written from the engine just before the default changed (its page text and manifests were
checked equal, including pixels, against the previous commit). To refresh it after adding a form example:
    python tests/test_heading_case.py --update
"""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pdfplumber
from pypdf import PdfReader

_scripts = Path(__file__).resolve().parents[1] / "skills" / "informe-tecnico" / "scripts"
if str(_scripts) not in sys.path:
    sys.path.insert(0, str(_scripts))

from build_report import KIND_RULES, sentence_case

GOLDEN = Path(__file__).resolve().parent / "golden" / "heading-title.json"
SCRIPT = _scripts / "build_report.py"


def compile_pdf(script, source, pdf):
    result = subprocess.run(
        [sys.executable, str(script), str(source), "--output", str(pdf)],
        capture_output=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).decode()[-800:]
        raise AssertionError(f"{source.name}\n{detail}")


def manifest_body(pdf):
    data = json.loads(pdf.with_suffix(".manifest.json").read_text())
    for key in ("pdf_sha256", "source_sha256", "source"):
        data.pop(key, None)
    return data


def snapshot(pdf):
    """Layout-independent record of a PDF: page count, normalized text per page and the manifest body."""
    with pdfplumber.open(pdf) as document:
        texts = [hashlib.sha256(" ".join((page.extract_text() or "").split()).encode()).hexdigest()
                 for page in document.pages]
    body = json.dumps(manifest_body(pdf), sort_keys=True, ensure_ascii=False)
    return {"pages": len(texts), "text": texts, "manifest": hashlib.sha256(body.encode()).hexdigest()}


def title_snapshots(example, work):
    """Compile every form example with heading_case "title" and return its snapshot."""
    work.mkdir(parents=True, exist_ok=True)
    diagrams = work / "diagrams"
    if not diagrams.exists():
        diagrams.symlink_to(example.parent / "diagrams")
    result = {}
    for source in sorted(example.parent.glob("ejemplo*.json")):
        spec = json.loads(source.read_text())
        kind = spec["document"].get("kind", "informe")
        if not KIND_RULES[kind].get("form"):
            continue
        spec.setdefault("format", {})["heading_case"] = "title"
        titled = work / source.name
        titled.write_text(json.dumps(spec, ensure_ascii=False))
        pdf = work / f"{source.stem}.pdf"
        compile_pdf(SCRIPT, titled, pdf)
        result[source.stem] = snapshot(pdf)
    return result


def run_checks(example, root, checks, build, rejected_with):
    assert sentence_case("información de referencia") == "Información de referencia"
    assert sentence_case("INFORMACIÓN DE REFERENCIA") == "INFORMACIÓN DE REFERENCIA"
    assert sentence_case("Pruebas con API de pagos en iOS") == "Pruebas con API de pagos en iOS"
    assert sentence_case("qué se evalúa: el alcance") == "Qué se evalúa: el alcance"
    checks.append({"case": "heading-sentence-no-reescribe-el-resto"})

    informe = json.loads(example.read_text())
    titled_informe = json.loads(example.read_text())
    titled_informe.setdefault("format", {})["heading_case"] = "title"
    plain, plain_pdf = build("informe-sin-heading-case", informe)
    forced, forced_pdf = build("informe-heading-title", titled_informe)
    assert plain["labels"] == forced["labels"]
    assert plain["document"]["title"] == forced["document"]["title"]
    assert [page.extract_text() for page in PdfReader(plain_pdf).pages] == [
        page.extract_text() for page in PdfReader(forced_pdf).pages]
    checks.append({"case": "heading-case-no-cambia-el-informe"})

    unknown = json.loads((example.parent / "ejemplo-informe-factibilidad.json").read_text())
    unknown.setdefault("format", {})["heading_case"] = "upper"
    rejected_with("heading-case-valor-ajeno", unknown, 'format.heading_case admite "sentence" o "title".')

    recorded = json.loads(GOLDEN.read_text())
    current = title_snapshots(example, root / "heading-title")
    assert sorted(current) == sorted(recorded), (
        "Los ejemplos de formulario cambiaron: ejecutar python tests/test_heading_case.py --update", sorted(set(current) ^ set(recorded)))
    for stem, value in current.items():
        assert value == recorded[stem], stem
    checks.append({"case": "heading-case-title-conserva-lo-registrado", "examples": len(current)})


if __name__ == "__main__":
    import tempfile
    if sys.argv[1:] != ["--update"]:
        sys.exit("uso: python tests/test_heading_case.py --update")
    assets = Path(__file__).resolve().parents[1] / "skills" / "informe-tecnico" / "assets"
    with tempfile.TemporaryDirectory() as folder:
        values = title_snapshots(assets / "ejemplo.json", Path(folder))
    GOLDEN.parent.mkdir(exist_ok=True)
    GOLDEN.write_text(json.dumps(values, indent=1, sort_keys=True) + "\n")
    print(f"{len(values)} ejemplos registrados en {GOLDEN}")
