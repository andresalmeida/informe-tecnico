#!/usr/bin/env python3
"""Comprueba que los ejemplos de los tipos existentes salen idénticos tras un cambio en el motor.

Uso, desde la raíz del repositorio y con el intérprete que tiene las dependencias del motor:

    python tools/regresion.py <commit-base> [ejemplo ...]

Compila cada ejemplo con el motor del commit base (extraído con `git archive`) y con el motor del árbol de
trabajo, y compara tres cosas: el manifiesto sin el hash del PDF, el texto de cada página y los píxeles de cada
página a 50 ppp. Sin ejemplos indicados, compara todos los que existen en el commit base: así cubre cada tipo
anterior y deja fuera el tipo nuevo, que el commit base no tiene. Con nombres indicados, compara solo esos
(por ejemplo, cuando un cambio de convención de la familia debe alterar la salida de unos tipos y no de otros).
Devuelve un código de salida distinto de cero si algo difiere. No necesita Poppler.
"""
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pdfplumber

SKILL = Path("skills/informe-tecnico")


def compile_example(skill, name, folder):
    folder.mkdir(parents=True, exist_ok=True)
    pdf = folder/f"{name}.pdf"
    subprocess.run([sys.executable, str(skill/"scripts/build_report.py"), str(skill/"assets"/f"{name}.json"),
                    "--output", str(pdf)], check=True, capture_output=True)
    return pdf


def manifest(pdf):
    data = json.loads(pdf.with_suffix(".manifest.json").read_text())
    data.pop("pdf_sha256", None)
    return data


def pages(pdf):
    """Text and a hash of the 50 ppp raster of every page."""
    with pdfplumber.open(pdf) as document:
        return [(page.extract_text(), hashlib.sha256(page.to_image(resolution=50).original.tobytes()).hexdigest())
                for page in document.pages]


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    base_commit, names = sys.argv[1], sys.argv[2:]
    with tempfile.TemporaryDirectory(prefix="regresion-") as temp:
        root = Path(temp)
        archive = subprocess.run(["git", "archive", base_commit, "skills"], check=True, capture_output=True).stdout
        (root/"base").mkdir()
        subprocess.run(["tar", "-x", "-C", str(root/"base")], input=archive, check=True)
        base_skill = root/"base"/SKILL
        names = names or sorted(path.stem for path in (base_skill/"assets").glob("ejemplo*.json"))
        identical = True
        for name in names:
            before = compile_example(base_skill, name, root/"antes")
            after = compile_example(SKILL, name, root/"despues")
            same_manifest = manifest(before) == manifest(after)
            printed_before, printed_after = pages(before), pages(after)
            same_text = [t for t, _ in printed_before] == [t for t, _ in printed_after]
            same_pixels = [h for _, h in printed_before] == [h for _, h in printed_after]
            print(f"{name:34} páginas {len(printed_before)}/{len(printed_after)}  manifiesto {same_manifest}  "
                  f"texto {same_text}  píxeles {same_pixels}")
            identical &= same_manifest and same_text and same_pixels
        print("REGRESIÓN", "IDÉNTICA" if identical else "CON DIFERENCIAS")
        sys.exit(0 if identical else 1)


if __name__ == "__main__":
    main()
