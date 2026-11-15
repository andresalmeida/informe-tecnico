"""Tell the user what to install when the engine's Python dependencies are missing."""
import sys

SPECS = {
    'reportlab': 'reportlab>=4.4,<5',
    'pypdf': 'pypdf>=6,<7',
    'pdfplumber': 'pdfplumber>=0.11,<1',
    'PIL': 'Pillow>=11,<13',
    'svglib': 'svglib',
    'docx': 'python-docx',
}
CORE = ('reportlab', 'pypdf', 'pdfplumber', 'PIL')


def missing_modules(modules):
    missing = []
    for name in modules:
        try:
            __import__(name)
        except ImportError:
            missing.append(name)
    return missing


def message(missing, script):
    names = ', '.join(SPECS[name].split('>')[0] for name in missing)
    wanted = list(CORE) + [name for name in missing if name not in CORE]
    install = ' '.join('"%s"' % SPECS[name] for name in wanted)
    return (
        'Faltan dependencias de Python para ejecutar %s: %s.\n'
        'El intérprete que se usó es %s.\n'
        'Si ya tienes un entorno con estas dependencias, repite el comando con su intérprete.\n'
        'Si no, crea un entorno virtual fuera de la carpeta de la skill y repite el comando con ese intérprete:\n'
        '  python3 -m venv ~/.cache/informe-venv\n'
        '  ~/.cache/informe-venv/bin/python -m pip install %s\n'
        '  ~/.cache/informe-venv/bin/python %s ...\n'
        'Más detalle en SKILL.md, apartado «Renderizar».\n'
    ) % (script, names, sys.executable, install, sys.argv[0] or script)


def check(modules, script):
    """Exit with code 2 and a short instruction instead of a traceback."""
    missing = missing_modules(modules)
    if missing:
        sys.stderr.write(message(missing, script))
        raise SystemExit(2)
