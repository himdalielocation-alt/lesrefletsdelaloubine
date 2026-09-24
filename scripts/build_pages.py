#!/usr/bin/env python3
"""Régénère les pages HTML depuis templates/pages/, en remplaçant
{{HEADER}}/{{FOOTER}} par les includes partagés de templates/includes/ et
{{HREFLANG}} par les balises <link rel="alternate" hreflang="..."> reliant
les 3 langues du site.

Le français reste à la racine (ex. index.html). L'anglais et l'allemand
sont générés dans des sous-dossiers /en/ et /de/, chacun avec son propre
header/footer traduits (templates/includes/header.en.html, header.de.html,
etc.) et ses propres pages sources (templates/pages/en/, templates/pages/de/).
404.html reste unique (GitHub Pages ne sert qu'un seul fichier 404 pour tout
le site, quel que soit le préfixe de langue de l'URL demandée).

Usage : python3 scripts/build_pages.py
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES_DIR = ROOT / "templates" / "pages"
INCLUDES_DIR = ROOT / "templates" / "includes"

BASE_URL = "https://lesrefletsdelaloubine.fr"

LANGUAGES = {
    "fr": {"prefix": "", "header": "header.html", "footer": "footer.html"},
    "en": {"prefix": "/en", "header": "header.en.html", "footer": "footer.en.html"},
    "de": {"prefix": "/de", "header": "header.de.html", "footer": "footer.de.html"},
}

TRANSLATED_PAGES = [
    "index.html",
    "activites-sables-d-olonne.html",
    "mentions-legales.html",
    "politique-de-confidentialite.html",
]

LANG_SWITCH_NAMES = {"fr": "Français", "en": "English", "de": "Deutsch"}
# Drapeaux en SVG plat (pas d'emoji, rendu différent selon les appareils) :
# mêmes proportions pour les 3, recadrés en rond (preserveAspectRatio="slice",
# comme un object-fit:cover) dans un badge circulaire avec bordure — même
# traitement que les avatars/pastilles ronds déjà utilisés ailleurs sur le site.
LANG_SWITCH_FLAG_SVG = {
    "fr": (
        '<svg viewBox="0 0 24 16" preserveAspectRatio="xMidYMid slice" '
        'class="absolute inset-0 w-full h-full" aria-hidden="true" focusable="false">'
        '<rect width="8" height="16" fill="#0055A4"/>'
        '<rect x="8" width="8" height="16" fill="#fff"/>'
        '<rect x="16" width="8" height="16" fill="#EF4135"/>'
        '</svg>'
    ),
    "en": (
        '<svg viewBox="0 0 24 16" preserveAspectRatio="xMidYMid slice" '
        'class="absolute inset-0 w-full h-full" aria-hidden="true" focusable="false">'
        '<rect width="24" height="16" fill="#00247D"/>'
        '<path d="M0,0 L24,16 M24,0 L0,16" stroke="#fff" stroke-width="2.4"/>'
        '<path d="M0,0 L24,16 M24,0 L0,16" stroke="#CF142B" stroke-width="0.8"/>'
        '<path d="M12,0 V16 M0,8 H24" stroke="#fff" stroke-width="4"/>'
        '<path d="M12,0 V16 M0,8 H24" stroke="#CF142B" stroke-width="2.4"/>'
        '</svg>'
    ),
    "de": (
        '<svg viewBox="0 0 24 16" preserveAspectRatio="xMidYMid slice" '
        'class="absolute inset-0 w-full h-full" aria-hidden="true" focusable="false">'
        '<rect width="24" height="5.34" fill="#000"/>'
        '<rect y="5.33" width="24" height="5.34" fill="#DD0000"/>'
        '<rect y="10.66" width="24" height="5.34" fill="#FFCE00"/>'
        '</svg>'
    ),
}
LANG_SWITCH_ARIA = {
    "fr": "Changer de langue",
    "en": "Change language",
    "de": "Sprache wechseln",
}


def page_url(lang: str, slug: str) -> str:
    prefix = LANGUAGES[lang]["prefix"]
    if slug == "index.html":
        return f"{BASE_URL}{prefix}/"
    return f"{BASE_URL}{prefix}/{slug}"


def page_path_for_link(lang: str, slug: str) -> str:
    prefix = LANGUAGES[lang]["prefix"]
    if slug == "index.html":
        return f"{prefix}/" if prefix else "/"
    return f"{prefix}/{slug}"


def hreflang_block(slug: str) -> str:
    lines = [
        f'    <link rel="alternate" hreflang="{lang}" href="{page_url(lang, slug)}">'
        for lang in LANGUAGES
    ]
    lines.append(f'    <link rel="alternate" hreflang="x-default" href="{page_url("fr", slug)}">')
    return "\n".join(lines)


def lang_switch_block(current_lang: str, slug: str) -> str:
    items = []
    for lang in LANGUAGES:
        flag = (
            f'<span class="relative block w-8 h-8 rounded-rayon-pilule overflow-hidden border border-dune shrink-0">'
            f'{LANG_SWITCH_FLAG_SVG[lang]}</span>'
        )
        if lang == current_lang:
            items.append(
                f'<span aria-current="true" lang="{lang}" class="btn-focus p-1.5 rounded-rayon-pilule bg-sable">'
                f'{flag}<span class="sr-only">{LANG_SWITCH_NAMES[lang]}</span></span>'
            )
        else:
            items.append(
                f'<a href="{page_path_for_link(lang, slug)}" lang="{lang}" hreflang="{lang}" '
                f'class="btn-focus p-1.5 rounded-rayon-pilule hover:bg-sable transition" '
                f'aria-label="{LANG_SWITCH_NAMES[lang]}">{flag}</a>'
            )
    aria = LANG_SWITCH_ARIA[current_lang]
    return (
        f'<nav aria-label="{aria}" class="fixed bottom-4 right-4 z-30 flex items-center gap-1 '
        f'bg-blanc-coquille border border-dune rounded-rayon-pilule shadow-relief p-1.5">'
        + "".join(items)
        + "</nav>"
    )


def read_include(name: str) -> str:
    path = INCLUDES_DIR / name
    if not path.is_file():
        sys.exit(f"Include manquant : {path}")
    return path.read_text(encoding="utf-8")


def build() -> list[pathlib.Path]:
    if not PAGES_DIR.is_dir():
        sys.exit(f"Dossier introuvable : {PAGES_DIR}")

    written = []

    for slug in TRANSLATED_PAGES:
        hreflang = hreflang_block(slug)
        for lang, cfg in LANGUAGES.items():
            lang_pages_dir = PAGES_DIR if lang == "fr" else PAGES_DIR / lang
            page_path = lang_pages_dir / slug
            if not page_path.is_file():
                sys.exit(f"Page manquante : {page_path}")
            content = page_path.read_text(encoding="utf-8")

            content = content.replace("{{HEADER}}", read_include(cfg["header"]))
            content = content.replace("{{FOOTER}}", read_include(cfg["footer"]))
            content = content.replace("{{HREFLANG}}", hreflang)
            content = content.replace("{{LANGSWITCH}}", lang_switch_block(lang, slug))

            remaining = [
                t for t in ("{{HEADER}}", "{{FOOTER}}", "{{HREFLANG}}", "{{LANGSWITCH}}")
                if t in content
            ]
            if remaining:
                sys.exit(
                    f"{page_path} : jeton(s) non résolu(s) après substitution : "
                    f"{', '.join(remaining)}"
                )

            output_dir = ROOT if lang == "fr" else ROOT / lang
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / slug
            output_path.write_text(content, encoding="utf-8")
            written.append(output_path)

    # 404.html : une seule version pour tout le site (contrainte GitHub Pages).
    content = (PAGES_DIR / "404.html").read_text(encoding="utf-8")
    content = content.replace("{{HEADER}}", read_include("header.html"))
    content = content.replace("{{FOOTER}}", read_include("footer.html"))
    remaining = [t for t in ("{{HEADER}}", "{{FOOTER}}") if t in content]
    if remaining:
        sys.exit(f"404.html : jeton(s) non résolu(s) : {', '.join(remaining)}")
    output_path = ROOT / "404.html"
    output_path.write_text(content, encoding="utf-8")
    written.append(output_path)

    return written


if __name__ == "__main__":
    for path in build():
        print(f"Généré : {path.relative_to(ROOT)}")
