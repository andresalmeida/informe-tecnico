"""Cada muestra publicada en docs/ debe coincidir con la compilación actual del JSON que dice su manifiesto."""
import hashlib
import json
from pathlib import Path

import pdfplumber

from build_report import compile_report


def paginas(pdf):
    """Número de páginas y hash del texto normalizado de cada una."""
    with pdfplumber.open(pdf) as documento:
        return [hashlib.sha256(" ".join((pagina.extract_text() or "").split()).encode()).hexdigest()
                for pagina in documento.pages]


def run_checks(example, root, checks, build):
    docs = example.parents[3] / "docs"
    carpeta = root / "muestras"
    carpeta.mkdir()
    desactualizadas, comparadas = [], 0
    for manifiesto in sorted(docs.glob("muestra-*.manifest.json")):
        origen = example.parent / json.loads(manifiesto.read_text())["source"]
        assert origen.is_file(), f"{manifiesto.name}: el manifiesto cita {origen.name}, que no existe"
        publicada = docs / manifiesto.name.replace(".manifest.json", ".pdf")
        nueva = carpeta / publicada.name
        compile_report(origen, nueva)
        comparadas += 1
        if paginas(nueva) != paginas(publicada):
            desactualizadas.append(publicada.name)
    assert not desactualizadas, ("Muestras desactualizadas; regenerarlas con build_report.py", desactualizadas)
    checks.append({"case": "muestras-al-dia-con-su-fuente", "muestras": comparadas})
