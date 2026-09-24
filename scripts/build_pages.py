#!/usr/bin/env python3
"""Régénère les pages HTML à la racine du dépôt depuis templates/pages/,
en remplaçant {{HEADER}} et {{FOOTER}} par les includes partagés de
templates/includes/.

Usage : python3 scripts/build_pages.py
(depuis n'importe quel répertoire ; les chemins sont relatifs à la racine
du dépôt, calculée depuis l'emplacement de ce script)
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES_DIR = ROOT / "templates" / "pages"
INCLUDES_DIR = ROOT / "templates" / "includes"

TOKENS = {
    "{{HEADER}}": INCLUDES_DIR / "header.html",
    "{{FOOTER}}": INCLUDES_DIR / "footer.html",
}


def build() -> list[pathlib.Path]:
    if not PAGES_DIR.is_dir():
        sys.exit(f"Dossier introuvable : {PAGES_DIR}")

    includes = {}
    for token, path in TOKENS.items():
        if not path.is_file():
            sys.exit(f"Include manquant : {path}")
        includes[token] = path.read_text(encoding="utf-8")

    written = []
    for page_path in sorted(PAGES_DIR.glob("*.html")):
        content = page_path.read_text(encoding="utf-8")

        for token, replacement in includes.items():
            content = content.replace(token, replacement)

        remaining = [t for t in TOKENS if t in content]
        if remaining:
            sys.exit(
                f"{page_path.name} : jeton(s) non résolu(s) après substitution : "
                f"{', '.join(remaining)}"
            )

        output_path = ROOT / page_path.name
        output_path.write_text(content, encoding="utf-8")
        written.append(output_path)

    return written


if __name__ == "__main__":
    for path in build():
        print(f"Généré : {path.relative_to(ROOT)}")
