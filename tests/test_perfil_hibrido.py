"""El perfil por omisión (institucional-apa) vale para todos los tipos: justificado, títulos a la izquierda con punto,
tablas con reglas mínimas, palabras enteras en las celdas, y `institucional` conserva la composición compacta."""
import copy
import json

import pdfplumber

MM = 72/25.4
MARGEN = 21*MM


def texto_largo(marca):
    return marca + " " + "El sistema conserva las relaciones entre datos y permite consultar los resultados de la operación. "*4


def fuente(base, formato):
    spec = {"schema_version": 1, "brand": copy.deepcopy(base["brand"]), "document": copy.deepcopy(base["document"]),
            "changes": [{"version": "1.0", "date": "2026-10-28", "summary": "Prueba sintética.", "author": "Prueba"}],
            "sections": [{"id": "medidas", "title": "Geometría de párrafos", "blocks": [
                {"type": "paragraph", "text": texto_largo("PARRAFO_UNO")},
                {"type": "table", "id": "estrecha", "title": "Columna estrecha", "headers": ["Código", "Estado"],
                 "widths": [12, 1], "rows": [["A-1", "Confirmación"], ["A-2", "Pendiente"]]},
            ]}]}
    if formato is not None:
        spec["format"] = formato
    return spec


def lineas(pagina, marca):
    palabras = pagina.extract_words()
    inicio = next(w for w in palabras if w["text"].startswith(marca))
    filas = {}
    for w in palabras:
        if inicio["top"]-.1 <= w["top"] < inicio["top"]+75:
            filas.setdefault(round(w["top"], 1), []).append(w)
    return [sorted(ws, key=lambda w: w["x0"]) for _, ws in sorted(filas.items())]


def run_checks(example, root, checks, build, rejected_with):
    base = json.loads((example.parent / "ejemplo-acta-reunion.json").read_text())

    # Sin `format` rige el perfil por omisión, en un tipo de formulario y en el informe.
    for tipo in ("acta-reunion", "informe"):
        sin_formato = fuente(base, None)
        sin_formato["document"]["kind"] = tipo
        if tipo == "informe":
            sin_formato["document"]["show_changes"] = False
        manifiesto, pdf = build("perfil-por-omision-" + tipo, sin_formato)
        assert manifiesto["format"]["profile"] == "institucional-apa", manifiesto["format"]
        assert manifiesto["format"]["justify"] is True and manifiesto["format"]["line_spacing"] == 1.5
        with pdfplumber.open(pdf) as impreso:
            pagina = next(p for p in impreso.pages if "PARRAFO_UNO" in (p.extract_text() or ""))
            filas = lineas(pagina, "PARRAFO_UNO")
            assert abs(filas[0][0]["x0"]-MARGEN-36) < .5, "sangría de primera línea de 12,7 mm"
            # Justificado: toda línea menos la última llega al margen derecho; la última queda corta.
            derecha = pagina.width-MARGEN
            assert all(abs(fila[-1]["x1"]-derecha) < .8 for fila in filas[:-1]), [f[-1]["x1"] for f in filas]
            assert filas[-1][-1]["x1"] < derecha-5
            # Título a la izquierda y numerado con punto.
            titulo = next(w for w in pagina.extract_words() if w["text"] == "Geometría")
            assert abs(titulo["x0"]-MARGEN-14.5) < 8, "el número y su punto preceden al título, a la izquierda"
            assert "1. Geometría de párrafos" in " ".join((pagina.extract_text() or "").split())
            # Una columna estrecha no parte la palabra más larga de sus celdas.
            palabras = [w["text"] for p in impreso.pages for w in p.extract_words()]
            assert "Confirmación" in palabras and "Pendiente" in palabras, "palabra partida en una celda estrecha"
        checks.append({"case": "perfil-por-omision-" + tipo, "paginas": manifiesto["pages"]})

    # `justify: false` deja el margen derecho irregular; los demás valores del perfil no cambian.
    irregular, pdf = build("perfil-sin-justificar", fuente(base, {"profile": "institucional-apa", "justify": False}))
    assert irregular["format"]["justify"] is False
    with pdfplumber.open(pdf) as impreso:
        pagina = next(p for p in impreso.pages if "PARRAFO_UNO" in (p.extract_text() or ""))
        derecha = pagina.width-MARGEN
        assert any(abs(fila[-1]["x1"]-derecha) > 1.5 for fila in lineas(pagina, "PARRAFO_UNO")[:-1])
    checks.append({"case": "perfil-justify-falso"})
    rejected_with("justify-no-booleano", fuente(base, {"profile": "institucional-apa", "justify": "si"}),
                  "format.justify debe ser true o false")

    # `institucional` es la composición compacta: sin sangría, sin justificar, interlineado sencillo.
    compacto, pdf = build("perfil-institucional-compacto", fuente(base, {"profile": "institucional"}))
    assert compacto["format"]["profile"] == "institucional" and "justify" not in compacto["format"]
    with pdfplumber.open(pdf) as impreso:
        pagina = next(p for p in impreso.pages if "PARRAFO_UNO" in (p.extract_text() or ""))
        filas = lineas(pagina, "PARRAFO_UNO")
        assert abs(filas[0][0]["x0"]-MARGEN) < .5
        assert abs(filas[1][0]["top"]-filas[0][0]["top"]-14.5) < .3
    checks.append({"case": "perfil-institucional-compacto"})

    # La EDT y los pasos del caso de prueba usan reglas mínimas, sin cabecera de color, con el perfil por omisión.
    for nombre, perfil, con_relleno in (("ejemplo-plan-proyecto.json", "institucional-apa", False),
                                        ("ejemplo-plan-proyecto.json", "institucional", True),
                                        ("ejemplo-plan-pruebas.json", "institucional-apa", False),
                                        ("ejemplo-plan-pruebas.json", "institucional", True)):
        spec = json.loads((example.parent / nombre).read_text())
        spec["brand"]["accent"] = "#7A2E1D"
        spec["format"] = {"profile": perfil}
        manifiesto, pdf = build(f"relleno-{nombre.replace('ejemplo-', '').replace('.json', '')}-{perfil}", spec)
        acento = (0x7A/255, 0x2E/255, 0x1D/255)
        with pdfplumber.open(pdf) as impreso:
            rellenos = [r for p in impreso.pages for r in p.rects
                        if r.get("fill") and r.get("non_stroking_color") and len(r["non_stroking_color"]) == 3
                        and all(abs(a-b) < .01 for a, b in zip(r["non_stroking_color"], acento))
                        and r["height"] > 8]  # the header band, not the thin rules of the page frame
        assert bool(rellenos) == con_relleno, (nombre, perfil, len(rellenos))
        checks.append({"case": f"cabecera-{'con' if con_relleno else 'sin'}-relleno-{nombre.replace('ejemplo-', '').replace('.json', '')}-{perfil}"})

    # Una celda vacía de firma reserva altura y no imprime raya: en la columna «Firma» y en la fila «Firma».
    firmas = fuente(base, None)
    firmas["sections"][0]["blocks"] = [
        {"type": "table", "id": "columna", "title": "Firma en columna", "headers": ["Función", "Firma", "Fecha"],
         "rows": [["FILA_A", "", "Pendiente"], ["FILA_B", "", "Pendiente"]]},
        {"type": "table", "id": "fila", "title": "Firma en fila", "headers": ["", "Parte solicitante", "Equipo ejecutor"],
         "rows": [["Nombre", "Ana", "Luis"], ["Firma", "", ""], ["Fecha", "FILA_C", "FILA_D"]]},
    ]
    manifiesto, pdf = build("firma-celda-vacia", firmas)
    with pdfplumber.open(pdf) as impreso:
        texto = " ".join((p.extract_text() or "") for p in impreso.pages)
        assert "____" not in texto
        palabras = [w for p in impreso.pages for w in p.extract_words()]
        top = {w["text"]: w["top"] for w in palabras if w["text"] in ("FILA_A", "FILA_B", "Nombre", "FILA_C")}
        assert top["FILA_B"]-top["FILA_A"] >= 11*MM, "la fila de firma reserva al menos 11 mm"
        assert top["FILA_C"]-top["Nombre"] >= 11*MM, "la fila «Firma» reserva al menos 11 mm"
    checks.append({"case": "firma-celda-vacia-reserva-altura"})
