"""sentence is the form default. title must match the motor and the examples at ee2155d."""
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

BASE = "ee2155d"


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


def page_view(pdf):
    with pdfplumber.open(pdf) as document:
        return [(page.extract_text(),
                 hashlib.sha256(page.to_image(resolution=50).original.tobytes()).hexdigest())
                for page in document.pages]


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

    repo = example.parents[3]
    archive = subprocess.run(["git", "archive", BASE, "skills"], cwd=repo, check=True, capture_output=True).stdout
    base_root = root / "heading-base"
    base_root.mkdir()
    subprocess.run(["tar", "-x", "-C", str(base_root)], input=archive, check=True)
    base_skill = base_root / "skills" / "informe-tecnico"
    current_script = Path(__file__).resolve().parents[1] / "skills" / "informe-tecnico" / "scripts" / "build_report.py"
    work = root / "heading-title"
    work.mkdir()
    (work / "diagrams").symlink_to(example.parent / "diagrams")
    compared = []
    for source in sorted(example.parent.glob("ejemplo*.json")):
        spec = json.loads(source.read_text())
        kind = spec["document"].get("kind", "informe")
        if not KIND_RULES[kind].get("form"):
            continue
        base_source = base_skill / "assets" / source.name
        assert base_source.is_file(), source.name
        spec.setdefault("format", {})["heading_case"] = "title"
        titled_source = work / source.name
        titled_source.write_text(json.dumps(spec, ensure_ascii=False))
        before = root / "heading-before" / f"{source.stem}.pdf"
        after = root / "heading-after" / f"{source.stem}.pdf"
        before.parent.mkdir(exist_ok=True)
        after.parent.mkdir(exist_ok=True)
        compile_pdf(base_skill / "scripts" / "build_report.py", base_source, before)
        compile_pdf(current_script, titled_source, after)
        assert manifest_body(before) == manifest_body(after), source.name
        before_pages, after_pages = page_view(before), page_view(after)
        assert [text for text, _ in before_pages] == [text for text, _ in after_pages], source.name
        assert [pixel for _, pixel in before_pages] == [pixel for _, pixel in after_pages], source.name
        compared.append(source.stem)
    checks.append({"case": "heading-case-title-identico-a-ee2155d", "examples": len(compared)})
