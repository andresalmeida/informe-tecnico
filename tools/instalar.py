#!/usr/bin/env python3
"""Instala la skill informe-tecnico desde una referencia de git en Claude Code y en Codex.

Uso, desde el repositorio clonado:

    python tools/instalar.py                    # la versión publicada (main) en las carpetas que existan
    python tools/instalar.py --ref v0.8.0       # una etiqueta o una rama
    python tools/instalar.py --destino claude   # solo en Claude Code (claude, codex o la ruta de una carpeta skills)
    python tools/instalar.py --simular          # muestra lo que haría, sin escribir nada

Instala lo que hay en la referencia (nunca lo que tengas sin commitear), copia la licencia, deja un respaldo de la
versión anterior y comprueba que todas las copias quedaron idénticas. Antes de instalar la última versión, ejecuta
`git fetch`.
"""
import argparse
import filecmp
import io
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from datetime import datetime
from pathlib import Path

NOMBRE = "informe-tecnico"
RAIZ = Path(__file__).resolve().parents[1]
CARPETAS = {"claude": Path.home() / ".claude" / "skills", "codex": Path.home() / ".codex" / "skills"}
RESPALDOS = Path.home() / ".cache" / "informe-tecnico" / "respaldos"


def fallar(mensaje):
    sys.stderr.write(mensaje + "\n")
    raise SystemExit(2)


def extraer(ref, carpeta):
    """Extrae skills/informe-tecnico y la licencia de `ref` en `carpeta/informe-tecnico`."""
    resultado = subprocess.run(["git", "archive", ref, f"skills/{NOMBRE}"], cwd=RAIZ, capture_output=True)
    if resultado.returncode != 0:
        fallar(f"No se pudo leer «{ref}» con git: {resultado.stderr.decode().strip()}")
    temporal = Path(carpeta) / "extraido"
    temporal.mkdir()
    with tarfile.open(fileobj=io.BytesIO(resultado.stdout)) as archivo:
        if hasattr(tarfile, "data_filter"):
            archivo.extractall(temporal, filter="data")
        else:
            archivo.extractall(temporal)
    origen = temporal / "skills" / NOMBRE
    licencia = subprocess.run(["git", "show", f"{ref}:LICENSE"], cwd=RAIZ, capture_output=True)
    if licencia.returncode == 0:
        (origen / "LICENSE").write_bytes(licencia.stdout)
    return origen


def version_de(carpeta):
    texto = (Path(carpeta) / "SKILL.md").read_text(encoding="utf-8")
    encontrada = re.search(r'^\s*version:\s*"([^"]+)"', texto, re.M)
    return encontrada.group(1) if encontrada else "desconocida"


def iguales(a, b):
    """True si dos carpetas tienen los mismos archivos con el mismo contenido."""
    comparacion = filecmp.dircmp(a, b)
    if comparacion.left_only or comparacion.right_only or comparacion.funny_files:
        return False
    if filecmp.cmpfiles(a, b, comparacion.common_files, shallow=False)[1:] != ([], []):
        return False
    return all(iguales(Path(a) / sub, Path(b) / sub) for sub in comparacion.common_dirs)


def respaldar(instalada, respaldos):
    respaldos.mkdir(parents=True, exist_ok=True)
    nombre = f"{NOMBRE}-{version_de(instalada)}-{datetime.now():%Y%m%d-%H%M%S}.tar.gz"
    with tarfile.open(respaldos / nombre, "w:gz") as archivo:
        archivo.add(instalada, arcname=NOMBRE)
    return respaldos / nombre


def destinos_de(nombres):
    if not nombres:
        encontrados = [base for base in CARPETAS.values() if base.is_dir()]
        if not encontrados:
            fallar("No hay carpetas ~/.claude/skills ni ~/.codex/skills. Indica una con --destino.")
        return encontrados
    bases = []
    for nombre in nombres:
        base = CARPETAS.get(nombre, Path(nombre).expanduser())
        if nombre in CARPETAS and not base.parent.is_dir():
            fallar(f"No existe {base.parent}: ese agente no está instalado en este equipo.")
        bases.append(base)
    return bases


def instalar(origen, base, respaldos, simular):
    """Copia `origen` en `base/informe-tecnico`. Devuelve una descripción de lo que hizo."""
    destino = base / NOMBRE
    nueva = version_de(origen)
    if destino.is_dir():
        if iguales(origen, destino):
            return f"{destino}: ya estaba al día ({nueva})"
        anterior = version_de(destino)
        if simular:
            return f"{destino}: se reemplazaría {anterior} por {nueva}, con respaldo"
        copia = respaldar(destino, respaldos)
        shutil.rmtree(destino)
        detalle = f"{anterior} reemplazada por {nueva}, respaldo en {copia}"
    else:
        if simular:
            return f"{destino}: se instalaría {nueva}"
        base.mkdir(parents=True, exist_ok=True)
        detalle = f"{nueva} instalada"
    shutil.copytree(origen, destino, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    return f"{destino}: {detalle}"


def main(argumentos=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--ref", default="main", help="rama, etiqueta o commit de git (por omisión, main)")
    parser.add_argument("--destino", action="append", default=[],
                        help="claude, codex o la ruta de una carpeta skills; se puede repetir")
    parser.add_argument("--simular", action="store_true", help="no escribe nada")
    parser.add_argument("--respaldos", type=Path, default=RESPALDOS, help="carpeta de los respaldos")
    opciones = parser.parse_args(argumentos)
    bases = destinos_de(opciones.destino)
    with tempfile.TemporaryDirectory() as carpeta:
        origen = extraer(opciones.ref, carpeta)
        for base in bases:
            print(instalar(origen, base, opciones.respaldos, opciones.simular))
        if not opciones.simular:
            copias = [base / NOMBRE for base in bases]
            malas = [copia for copia in copias if not iguales(origen, copia)]
            if malas:
                fallar("Las copias no quedaron idénticas a la referencia: " + ", ".join(map(str, malas)))
            print(f"Versión {version_de(origen)} de «{opciones.ref}» en {len(copias)} destino(s), todas idénticas.")


if __name__ == "__main__":
    main()
