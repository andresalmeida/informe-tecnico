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

    # Las celdas se centran en vertical con el perfil por omisión y quedan arriba en `institucional`.
    centrada = fuente(base, None)
    centrada["sections"][0]["blocks"] = [{"type": "table", "id": "centro", "title": "Celdas",
        "headers": ["Largo", "Corto"], "rows": [["LINEA_A\nLINEA_B\nLINEA_C\nLINEA_D", "CENTRO"]]}]
    for perfil, centrado in (("institucional-apa", True), ("institucional", False)):
        centrada["format"] = {"profile": perfil}
        _, pdf = build("celda-vertical-" + perfil, centrada)
        with pdfplumber.open(pdf) as impreso:
            palabras = {w["text"]: w for p in impreso.pages for w in p.extract_words()
                        if w["text"] in ("LINEA_A", "LINEA_D", "CENTRO")}
        medio_largo = (palabras["LINEA_A"]["top"]+palabras["LINEA_D"]["bottom"])/2
        medio_corto = (palabras["CENTRO"]["top"]+palabras["CENTRO"]["bottom"])/2
        if centrado:
            assert abs(medio_largo-medio_corto) < 2, (medio_largo, medio_corto)
        else:
            assert abs(palabras["CENTRO"]["top"]-palabras["LINEA_A"]["top"]) < 1.5
        checks.append({"case": "celda-" + ("centrada" if centrado else "arriba") + "-" + perfil})

    # Una sección que se cortaría pasa entera a la página siguiente si el hueco que deja es de a lo sumo el 35 %.
    def con_relleno(cantidad):
        spec = fuente(base, None)
        spec["sections"] = [
            {"id": "relleno", "title": "Relleno", "blocks": [
                {"type": "paragraph", "text": texto_largo(f"RELLENO_{i:02d}")[:210]} for i in range(cantidad)]},
            {"id": "cortable", "title": "Sección cortable", "blocks": [
                {"type": "paragraph", "text": "Introducción de la sección que podría cortarse."},
                {"type": "list", "ordered": True,
                 "items": [f"PUNTO_{i:02d} elemento de la lista de prueba." for i in range(16)]}]}]
        return spec

    def posiciones(nombre, cantidad):
        _, pdf = build(nombre, con_relleno(cantidad))
        with pdfplumber.open(pdf) as impreso:
            hallado = {}
            for n, pagina in enumerate(impreso.pages):
                for w in pagina.extract_words():
                    if w["text"] == "cortable":
                        hallado["titulo"] = (n, w["top"])
                    if w["text"] == "PUNTO_15":
                        hallado["ultimo"] = (n, w["top"])
                    if w["text"] == "RELLENO_00":
                        hallado["relleno"] = (n, w["top"])
            hallado["fondo"] = impreso.pages[0].height-25*MM
        return hallado

    sin_relleno = posiciones("seccion-medida-0", 0)
    con_cuatro = posiciones("seccion-medida-4", 4)
    alto_relleno = (con_cuatro["titulo"][1]-sin_relleno["titulo"][1])/4
    fondo = sin_relleno["fondo"]
    util = fondo-58*MM

    def cantidad_para(hueco):
        return round((fondo-hueco*util-sin_relleno["titulo"][1])/alto_relleno)

    movida = posiciones("seccion-hueco-chico", cantidad_para(.30))
    assert movida["relleno"][0] == 0 and movida["titulo"][0] == 1 and movida["ultimo"][0] == 1, movida
    assert movida["titulo"][1] < 58*MM+60, "la sección arranca arriba de la página siguiente"
    cortada = posiciones("seccion-hueco-grande", cantidad_para(.50))
    assert cortada["titulo"][0] == 0 and cortada["ultimo"][0] == 1, cortada
    checks.append({"case": "seccion-que-se-cortaria-pasa-entera-salvo-hueco-grande"})

    # Una tabla que cabe en una página, pero no en el espacio que queda, se parte si ese espacio pasa del 35 % y se
    # mueve entera si es menor; un fragmento nunca queda con menos de tres filas.
    def con_tabla(cantidad):
        spec = fuente(base, None)
        spec["sections"] = [
            {"id": "relleno", "title": "Relleno", "blocks": [
                {"type": "paragraph", "text": texto_largo(f"RELLENO_{i:02d}")[:210]} for i in range(cantidad)]},
            {"id": "tabla", "title": "Sección con tabla", "blocks": [
                {"type": "table", "id": "larga", "title": "Tabla larga", "headers": ["Número", "Detalle"],
                 "rows": [[f"FILA_{i:02d}", "Detalle de la fila de prueba"] for i in range(16)]}]}]
        return spec

    def tabla_en(nombre, cantidad):
        _, pdf = build(nombre, con_tabla(cantidad))
        with pdfplumber.open(pdf) as impreso:
            por_pagina = [[w["text"] for w in p.extract_words()] for p in impreso.pages]
            titulo = next((w["top"] for p in impreso.pages[:1] for w in p.extract_words() if w["text"] == "tabla"), None)
        return por_pagina, titulo

    pagina_cero, y_cero = tabla_en("tabla-medida-0", 0)
    _, y_cuatro = tabla_en("tabla-medida-4", 4)
    alto_relleno = (y_cuatro-y_cero)/4

    def cantidad_tabla(hueco):
        return round((fondo-hueco*util-y_cero)/alto_relleno)

    partida, _ = tabla_en("tabla-hueco-grande", cantidad_tabla(.50))
    con_filas = [sum(1 for t in pag if t.startswith("FILA_")) for pag in partida]
    assert len(partida) >= 2 and con_filas[0] >= 3 and con_filas[1] >= 3 and sum(con_filas) == 16, con_filas
    assert all("Número" in pag for pag in partida[:2]), "el encabezado se repite en la página que continúa"
    entera, _ = tabla_en("tabla-hueco-chico", cantidad_tabla(.25))
    filas_por_pagina = [sum(1 for t in pag if t.startswith("FILA_")) for pag in entera]
    assert sorted(filas_por_pagina)[-1] == 16 and filas_por_pagina.count(0) == len(filas_por_pagina)-1, filas_por_pagina
    checks.append({"case": "tabla-se-parte-solo-con-hueco-grande-y-sin-filas-sueltas", "filas": con_filas})

    # Una figura a la que le faltan pocos puntos para caber en una página aún vacía en su mayor parte se ajusta
    # (nunca menos del 88 %) en lugar de dejar el hueco: la Figura 1 del informe de muestra queda con su sección.
    informe = json.loads((example.parent / "ejemplo.json").read_text())
    manifiesto, pdf = build("figura-ajustada", informe)
    paginas = {e["id"]: e["page"] for e in manifiesto["entries"]}
    assert paginas["flujo"] == paginas["modelo"], "la figura queda en la página de su sección"
    from PIL import Image
    with Image.open(example.parent / "diagrams" / "ciclo-revision.png") as imagen:
        nominal = min(168*MM/imagen.width, 115*MM/imagen.height)*imagen.height
    with pdfplumber.open(pdf) as impreso:
        alto = impreso.pages[paginas["flujo"]-1].images[0]["height"]
    assert .88*nominal-1 <= alto < nominal-1, (alto, nominal)
    checks.append({"case": "figura-se-ajusta-sin-pasar-del-12-por-ciento", "escala": round(alto/nominal, 3)})
