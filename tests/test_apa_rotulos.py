"""Los bloques que calculan (cotización, riesgos, requisitos, EDT, impacto) también pasan el comprobador con el perfil APA."""
import copy
import json
import re

KINDS_CON_BLOQUES_CALCULADOS = [
    "ejemplo-propuesta-servicio.json",
    "ejemplo-registro-riesgos.json",
    "ejemplo-especificacion-requisitos.json",
    "ejemplo-plan-proyecto.json",
    "ejemplo-solicitud-cambio.json",
    "ejemplo-evaluacion-impacto-datos.json",
]


def run_checks(example, root, checks, build):
    for name in KINDS_CON_BLOQUES_CALCULADOS:
        spec = json.loads((example.parent / name).read_text())
        apa = copy.deepcopy(spec)
        apa.setdefault("format", {})["profile"] = "institucional-apa"
        manifest, _ = build("apa-" + name.replace(".json", ""), apa)
        tables = [entry["label"] for entry in manifest["entries"] if entry["kind"] == "table"]
        assert tables and not any(re.match(r"Tabla \d+\. ", label) for label in tables), (name, tables)
        checks.append({"case": "apa-rotulos-" + name.replace("ejemplo-", "").replace(".json", ""), "tablas": len(tables)})
