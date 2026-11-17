"""La matriz de riesgos es un mapa de calor: el color sale del orden de los niveles, sin interpretar sus palabras."""
import json
import re

import pdfplumber

from build_report import risk_level_colors


def run_checks(example, root, checks, build):
    # El primer nivel es verde y el último rojo, con 2 a 5 niveles; los intermedios pasan por el amarillo.
    for niveles in (["A", "B"], ["A", "B", "C"], ["A", "B", "C", "D"], ["A", "B", "C", "D", "E"]):
        paleta = risk_level_colors([niveles])
        primero, ultimo = paleta[niveles[0]], paleta[niveles[-1]]
        assert primero.green > primero.red and ultimo.red > ultimo.green, niveles
        assert len({tuple(c.hexval() for c in [paleta[n]]) for n in niveles}) == len(niveles), "niveles con el mismo color"
    checks.append({"case": "mapa-calor-paleta-por-orden-de-niveles"})

    fuente = json.loads((example.parent / "ejemplo-registro-riesgos.json").read_text())
    bloque = next(b for s in fuente["sections"] for b in s.get("blocks", []) if b.get("type") == "risks")
    esperados = risk_level_colors(bloque["scale"]["matrix"])
    abiertos = [i["id"] for i in bloque["items"] if i["state"] in ("Abierto", "En mitigación")]
    cerrados = [i["id"] for i in bloque["items"] if i["state"] == "Cerrado"]
    assert abiertos and cerrados

    for perfil in ("institucional-apa", "institucional"):
        spec = json.loads(json.dumps(fuente))
        spec["format"] = {"profile": perfil}
        _, pdf = build("mapa-calor-" + perfil, spec)
        with pdfplumber.open(pdf) as impreso:
            rellenos = [tuple(r["non_stroking_color"]) for p in impreso.pages for r in p.rects
                        if r.get("fill") and r.get("non_stroking_color") and len(r["non_stroking_color"]) == 3]
            for nivel, color in esperados.items():
                esperado = (color.red, color.green, color.blue)
                assert any(all(abs(a-b) < .01 for a, b in zip(esperado, c)) for c in rellenos), (perfil, nivel)
            texto = " ".join((p.extract_text() or "") for p in impreso.pages)
        # La matriz lista los riesgos abiertos de cada celda y deja fuera el cerrado.
        matriz = re.search(r"Matriz de niveles(.*?)Respuestas admitidas", texto, re.S).group(1)
        assert all(rid in matriz for rid in abiertos), (perfil, abiertos)
        assert not any(rid in matriz for rid in cerrados), (perfil, cerrados)
        checks.append({"case": "mapa-calor-" + perfil, "niveles": len(esperados), "abiertos": len(abiertos)})
