"""A long entity name breaks into two lines of similar width. A short name stays one line."""
import json

import pdfplumber


def entity_lines(pdf):
    with pdfplumber.open(pdf) as document:
        page = document.pages[0]
        words = [word for word in page.extract_words() if word["top"] < 80 and word["x0"] > page.width * 0.68]
        lines = {}
        for word in words:
            lines.setdefault(round(word["top"]), []).append(word)
        return [" ".join(word["text"] for word in sorted(lines[top], key=lambda item: item["x0"]))
                for top in sorted(lines)]


def with_entity(example, name):
    spec = json.loads((example.parent / "ejemplo-decision-arquitectura.json").read_text())
    spec["brand"]["entity"] = name
    spec["brand"].pop("logo", None)
    return spec


def run_checks(example, root, checks, build, rejected_with):
    short, short_pdf = build("entidad-una-linea", with_entity(example, "Entidad de demostración"))
    assert entity_lines(short_pdf) == ["Entidad de demostración"], entity_lines(short_pdf)
    checks.append({"case": "entidad-una-linea", "pages": short["pages"]})

    balanced, balanced_pdf = build("entidad-dos-lineas", with_entity(example, "Estudio de Software Ejemplo"))
    assert entity_lines(balanced_pdf) == ["Estudio de", "Software Ejemplo"], entity_lines(balanced_pdf)
    checks.append({"case": "entidad-dos-lineas-equilibradas", "pages": balanced["pages"]})

    three, three_pdf = build("entidad-tres-palabras", with_entity(example, "Oficina de Proyectos Especiales"))
    assert entity_lines(three_pdf) == ["Oficina de Proyectos", "Especiales"], entity_lines(three_pdf)
    checks.append({"case": "entidad-tres-palabras", "pages": three["pages"]})

    six, six_pdf = build("entidad-seis-palabras",
                         with_entity(example, "Estudio de Software Ejemplo para Reservas"))
    assert entity_lines(six_pdf) == ["Estudio de Software", "Ejemplo para Reservas"], entity_lines(six_pdf)
    checks.append({"case": "entidad-seis-palabras", "pages": six["pages"]})

    word = "Supercalifragilisticoespialidoso"
    one_word, one_word_pdf = build("entidad-una-palabra", with_entity(example, word))
    # ReportLab already breaks a word that does not fit; the pieces still spell that word.
    assert "".join(entity_lines(one_word_pdf)) == word, entity_lines(one_word_pdf)
    checks.append({"case": "entidad-una-palabra-larga", "pages": one_word["pages"]})

    rejected_with("entidad-demasiado-larga",
                  with_entity(example, "Dirección General de Ingeniería de Software de Reservas en Línea"),
                  "Texto demasiado largo en encabezado/pie")
