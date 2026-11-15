#!/usr/bin/env python3
"""Compone docs/muestras-collage.png con la primera página de las seis muestras del núcleo.

Uso, desde la raíz del repositorio:

    python tools/collage.py

Usa Poppler (pdftoppm) si está instalado y, si no, pdfplumber. Hay que regenerarlo solo cuando cambia el aspecto
de la primera página de alguna de esas muestras.
"""
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

RAIZ = Path(__file__).resolve().parents[1]
MUESTRAS = ["acta-reunion", "informe-factibilidad", "propuesta-servicio", "alcance-proyecto", "plan-pruebas",
            "acta-entrega"]
ANCHO, ESPACIO, COLUMNAS, DPI = 540, 44, 3, 110


def primera_pagina(pdf, carpeta):
    if shutil.which("pdftoppm"):
        destino = Path(carpeta) / pdf.stem
        subprocess.run(["pdftoppm", "-r", str(DPI), "-png", "-f", "1", "-l", "1", str(pdf), str(destino)], check=True)
        return Image.open(next(Path(carpeta).glob(f"{pdf.stem}-*.png"))).convert("RGB")
    import pdfplumber
    with pdfplumber.open(pdf) as documento:
        return documento.pages[0].to_image(resolution=DPI).original.convert("RGB")


def componer(salida=RAIZ / "docs" / "muestras-collage.png"):
    with tempfile.TemporaryDirectory() as carpeta:
        paginas = [primera_pagina(RAIZ / "docs" / f"muestra-{nombre}.pdf", carpeta) for nombre in MUESTRAS]
    alto = round(paginas[0].height * ANCHO / paginas[0].width)
    paginas = [pagina.resize((ANCHO, alto), Image.LANCZOS) for pagina in paginas]
    filas = -(-len(paginas) // COLUMNAS)
    lienzo = Image.new("RGB", (COLUMNAS * ANCHO + (COLUMNAS + 1) * ESPACIO, filas * alto + (filas + 1) * ESPACIO),
                       (243, 245, 248))
    sombra = Image.new("RGBA", lienzo.size, (0, 0, 0, 0))
    trazo = ImageDraw.Draw(sombra)
    posiciones = []
    for i in range(len(paginas)):
        fila, columna = divmod(i, COLUMNAS)
        x, y = ESPACIO + columna * (ANCHO + ESPACIO), ESPACIO + fila * (alto + ESPACIO)
        posiciones.append((x, y))
        trazo.rectangle((x + 6, y + 10, x + ANCHO + 6, y + alto + 10), fill=(20, 30, 50, 70))
    lienzo.paste(sombra.filter(ImageFilter.GaussianBlur(14)), (0, 0), sombra.filter(ImageFilter.GaussianBlur(14)))
    borde = ImageDraw.Draw(lienzo)
    for pagina, (x, y) in zip(paginas, posiciones):
        lienzo.paste(pagina, (x, y))
        borde.rectangle((x, y, x + ANCHO - 1, y + alto - 1), outline=(205, 210, 218))
    lienzo.save(salida, optimize=True)
    return salida


if __name__ == "__main__":
    print(componer())
