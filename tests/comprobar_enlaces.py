#!/usr/bin/env python3
"""Comprueba que cada enlace relativo de README.md y de los markdown de skills/ apunta a un archivo."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\]\(([^)\s]+)\)")


def targets():
    yield ROOT / "README.md"
    yield from (ROOT / "skills").rglob("*.md")


def main():
    broken = []
    checked = 0
    for path in targets():
        for match in LINK.finditer(path.read_text()):
            url = match.group(1)
            destination = url.split("#", 1)[0]
            if not destination or destination.startswith(("http://", "https://", "mailto:")):
                continue
            checked += 1
            if not (path.parent / destination).resolve().exists():
                broken.append(f"{path.relative_to(ROOT)} -> {url}")
    if broken:
        sys.stderr.write("\n".join(broken) + "\n")
        return 1
    print(f"enlaces ok: {checked}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
