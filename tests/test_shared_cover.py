"""Check that a partner is represented only on the report cover."""
import copy
import hashlib
import json

import pdfplumber
from PIL import Image, ImageDraw


def demo_logos(root):
    primary = Image.new("RGBA", (280, 110))
    mark = ImageDraw.Draw(primary)
    mark.rounded_rectangle((5, 5, 275, 105), radius=25, fill="#155D86")
    mark.rectangle((52, 32, 228, 78), fill="#FFFFFF")
    mark.rectangle((75, 43, 205, 67), fill="#155D86")
    primary.save(root/"demo-primary.png")
    partner = Image.new("RGBA", (95, 130))
    mark = ImageDraw.Draw(partner)
    mark.polygon([(47, 5), (92, 58), (47, 125), (3, 58)], fill="#82623A")
    mark.ellipse((32, 44, 62, 74), fill="#FFFFFF")
    partner.save(root/"demo-partner.png")


def run_checks(example, root, checks, build, rejected_with):
    source = json.loads(example.read_text())
    partner_name = "Entidad asociada de demostración"
    source["brand"]["partner"] = {"entity": partner_name}
    demo_logos(root)

    for logo_fields in ((), ("partner",), ("primary", "partner")):
        custom = copy.deepcopy(source)
        if "primary" in logo_fields:
            custom["brand"]["logo"] = "demo-primary.png"
        if "partner" in logo_fields:
            custom["brand"]["partner"]["logo"] = "demo-partner.png"
        name = "portada-compartida-" + ("-".join(logo_fields) or "sin-logos")
        manifest, pdf = build(name, custom)
        assets = {asset["path"]: asset["sha256"] for asset in manifest["assets"]}
        for field in ("primary", "partner"):
            filename = f"demo-{field}.png"
            if field in logo_fields:
                assert assets[filename] == hashlib.sha256((root/filename).read_bytes()).hexdigest()
            else:
                assert filename not in assets

        with pdfplumber.open(pdf) as printed:
            cover = printed.pages[0]
            partner_words = cover.crop((cover.width/2, 47*72/25.4, cover.width, cover.height)).extract_text()
            primary_words = cover.crop((0, 47*72/25.4, cover.width/2, cover.height)).extract_text()
            assert partner_name in partner_words
            assert source["brand"]["entity"] in primary_words
            assert "Histórico de revisiones" in printed.pages[1].extract_text()
            assert all(partner_name not in page.extract_text() for page in printed.pages[1:])
            logos = [image for image in cover.images if image["top"] > 47*72/25.4]
            assert len(logos) == len(logo_fields)
            assert all((image["x0"] < cover.width/2) == (image["srcsize"] == (280, 110))
                       for image in logos)
        checks.append({"case": name, "pages": manifest["pages"]})

    (root/"demo-damaged.png").write_text("Contenido ficticio que no es una imagen.")
    for label, partner, expected in (
        ("nulo", None, "brand.partner debe ser un objeto"),
        ("nombre-vacio", {"entity": " "}, "brand.partner.entity"),
        ("campo-desconocido", {"entity": partner_name, "unit": "Unidad"}, "brand.partner debe ser un objeto"),
        ("logo-vacio", {"entity": partner_name, "logo": ""}, "brand.partner.logo"),
        ("logo-ausente", {"entity": partner_name, "logo": "demo-missing.png"}, "no existe el archivo del logo"),
        ("logo-danado", {"entity": partner_name, "logo": "demo-damaged.png"}, "imagen raster"),
    ):
        invalid = copy.deepcopy(source)
        invalid["brand"]["partner"] = partner
        rejected_with(f"portada-compartida-{label}", invalid, expected)

    form = json.loads((example.parent/"ejemplo-acta-reunion.json").read_text())
    form["brand"]["partner"] = source["brand"]["partner"]
    rejected_with("portada-compartida-acta", form, "brand.partner requiere un documento de tipo informe")
