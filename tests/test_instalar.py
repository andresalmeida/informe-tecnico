"""tools/instalar.py instala una referencia de git, respalda lo anterior y deja copias idénticas."""
import contextlib
import importlib.util
import io
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]


def cargar():
    spec = importlib.util.spec_from_file_location("instalar", RAIZ / "tools" / "instalar.py")
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def silenciosa(funcion, argumentos):
    """Las instalaciones imprimen su resultado; la salida de self_test es solo su JSON."""
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        funcion(argumentos)


def run_checks(example, root, checks, build):
    herramienta = cargar()
    base = root / "instalar" / "skills"
    respaldos = root / "instalar" / "respaldos"
    comun = ["--ref", "HEAD", "--destino", str(base), "--respaldos", str(respaldos)]
    texto = subprocess.run(["git", "show", f"HEAD:skills/{herramienta.NOMBRE}/SKILL.md"], cwd=RAIZ,
                           capture_output=True, check=True).stdout.decode()
    esperada = re.search(r'^\s*version:\s*"([^"]+)"', texto, re.M).group(1)

    silenciosa(herramienta.main, comun + ["--simular"])
    assert not base.exists(), "--simular no debe escribir"
    checks.append({"case": "instalar-simular-no-escribe"})

    silenciosa(herramienta.main, comun)
    destino = base / herramienta.NOMBRE
    assert herramienta.version_de(destino) == esperada
    assert (destino / "SKILL.md").is_file() and (destino / "LICENSE").is_file()
    assert not any(destino.rglob("__pycache__")) and not any(destino.rglob("test_*.py"))
    assert not respaldos.exists(), "la primera instalación no tiene qué respaldar"
    checks.append({"case": "instalar-copia-la-referencia", "version": esperada})

    silenciosa(herramienta.main, comun)
    assert not respaldos.exists(), "una copia al día no se respalda otra vez"
    checks.append({"case": "instalar-copia-al-dia-no-respalda"})

    (destino / "SKILL.md").write_text("copia alterada")
    silenciosa(herramienta.main, comun)
    assert len(list(respaldos.glob("*.tar.gz"))) == 1
    assert herramienta.version_de(destino) == esperada
    checks.append({"case": "instalar-reemplaza-y-respalda"})

    otro = root / "instalar" / ".otro" / "skills"
    ambos = ["--ref", "HEAD", "--destino", str(base), "--destino", str(otro), "--respaldos", str(respaldos)]
    silenciosa(herramienta.main, ["--ref", "HEAD", "--destino", str(otro), "--respaldos", str(respaldos)])
    for carpeta in (base, otro):
        (carpeta / herramienta.NOMBRE / "SKILL.md").write_text("alterada en " + carpeta.parent.name)
    antes = len(list(respaldos.glob("*.tar.gz")))
    silenciosa(herramienta.main, ambos)
    assert len(list(respaldos.glob("*.tar.gz"))) == antes + 2, "dos destinos distintos en el mismo segundo no comparten respaldo"
    checks.append({"case": "instalar-un-respaldo-por-destino"})

    try:
        silenciosa(herramienta.main, ["--ref", "no-existe-esta-referencia", "--destino", str(base)])
    except SystemExit as salida:
        assert salida.code == 2
    else:
        raise AssertionError("una referencia inexistente debe fallar")
    checks.append({"case": "instalar-referencia-inexistente-falla"})
