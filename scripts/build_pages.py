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

Le <lastmod> de sitemap.xml est aussi mis à jour automatiquement (date du
jour, UTC) pour chaque page dont le HTML généré a réellement changé : Google
s'en sert pour savoir quand repasser sur une page.

Les jetons photo ({{PHOTOBOX:id|classes}}, {{PHOTO:id}}, {{GALLERY}}) sont
remplacés par les photos présentes dans images/photos/<id>.jpg, décrites
dans data/photos.json (texte alternatif par langue). Ces photos sont envoyées
par le propriétaire depuis /admin.html ; une photo absente donne un
emplacement « Photo à ajouter » ({{PHOTOBOX}}) ou rien du tout ({{PHOTO}},
{{GALLERY}}).

Usage : python3 scripts/build_pages.py
"""
import datetime
import hashlib
import html
import json
import pathlib
import re
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
    "vendee-globe-2028.html",
]

SITEMAP_PATH = ROOT / "sitemap.xml"
PHOTOS_JSON = ROOT / "data" / "photos.json"
PHOTOS_DIR = ROOT / "images" / "photos"

# Groupe de data/photos.json affiché par {{GALLERY}} (galerie du logement).
GALLERY_GROUP_PREFIX = "Accueil : galerie"

PLACEHOLDER_SVG = (
    '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" '
    'focusable="false"><rect x="3" y="4" width="18" height="16" rx="2"></rect>'
    '<circle cx="8.5" cy="9.5" r="1.5"></circle><path d="M21 15l-5-5-4 4-3-3-6 6"></path></svg>'
)


def load_photo_slots() -> list[dict]:
    if not PHOTOS_JSON.is_file():
        sys.exit(f"Fichier manquant : {PHOTOS_JSON}")
    return json.loads(PHOTOS_JSON.read_text(encoding="utf-8"))["slots"]


def jpeg_size(data: bytes) -> tuple[int, int]:
    """Largeur et hauteur d'un JPEG, lues dans son en-tête (marqueur SOF)."""
    if data[:2] != b"\xff\xd8":
        raise ValueError("pas un fichier JPEG")
    i = 2
    while i + 9 < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7 or marker == 0xFF:
            i += 1 if marker == 0xFF else 2
            continue
        length = int.from_bytes(data[i + 2:i + 4], "big")
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            height = int.from_bytes(data[i + 5:i + 7], "big")
            width = int.from_bytes(data[i + 7:i + 9], "big")
            return width, height
        i += 2 + length
    raise ValueError("dimensions introuvables")


def photo_img(slot: dict, lang: str, css: str) -> str | None:
    """Balise <img> de l'emplacement, ou None si aucune photo n'a été envoyée."""
    path = PHOTOS_DIR / f"{slot['id']}.jpg"
    if not path.is_file():
        return None
    data = path.read_bytes()
    try:
        width, height = jpeg_size(data)
    except ValueError as exc:
        sys.exit(f"{path} : {exc}")
    version = hashlib.sha1(data).hexdigest()[:8]
    alt = html.escape(slot["alt"][lang], quote=True)
    return (
        f'<img src="/images/photos/{slot["id"]}.jpg?v={version}" alt="{alt}" '
        f'width="{width}" height="{height}" loading="lazy" decoding="async" class="{css}">'
    )


def render_photos(content: str, lang: str, slots: list[dict], page: pathlib.Path) -> str:
    by_id = {slot["id"]: slot for slot in slots}

    def get(slot_id: str) -> dict:
        if slot_id not in by_id:
            sys.exit(f"{page} : emplacement photo inconnu « {slot_id} » (absent de data/photos.json)")
        return by_id[slot_id]

    def box(match: re.Match) -> str:
        slot, css = get(match[1]), match[2]
        img = photo_img(slot, lang, "w-full h-full object-cover")
        if img:
            return f'<div class="{css} rounded-rayon-lg overflow-hidden">{img}</div>'
        label = html.escape(slot["placeholder"][lang])
        return (
            f'<div class="{css} rounded-rayon-lg border-2 border-dashed border-dune bg-sable flex '
            f'flex-col items-center justify-center gap-2 text-encre-douce p-6 text-center">'
            f'{PLACEHOLDER_SVG}<p class="legende">{label}</p></div>'
        )

    def inline(match: re.Match) -> str:
        return photo_img(get(match[1]), lang, "block w-full rounded-rayon-lg mb-6") or ""

    content = re.sub(r"\{\{PHOTOBOX:([\w-]+)\|([^}]*)\}\}", box, content)
    content = re.sub(r"\{\{PHOTO:([\w-]+)\}\}", inline, content)

    if "{{GALLERY}}" in content:
        items = [
            photo_img(slot, lang, "w-full h-full object-cover")
            for slot in slots
            if slot["group"].startswith(GALLERY_GROUP_PREFIX)
        ]
        items = [f'<div class="aspect-[4/3] rounded-rayon-lg overflow-hidden">{img}</div>' for img in items if img]
        gallery = (
            '<div class="grid grid-cols-2 md:grid-cols-3 gap-4 mb-12">' + "".join(items) + "</div>"
            if items else ""
        )
        content = content.replace("{{GALLERY}}", gallery)
    return content

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


def update_sitemap_lastmod(changed_urls: list[str]) -> None:
    """Met la date du jour dans le <lastmod> des URLs dont la page a changé."""
    if not changed_urls or not SITEMAP_PATH.is_file():
        return
    today = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    sitemap = SITEMAP_PATH.read_text(encoding="utf-8")
    for url in changed_urls:
        pattern = re.compile(
            r"(<loc>" + re.escape(url) + r"</loc>\s*<lastmod>)[^<]*(</lastmod>)"
        )
        sitemap, count = pattern.subn(r"\g<1>" + today + r"\g<2>", sitemap)
        if count == 0:
            print(f"Attention : {url} absente de sitemap.xml (ou sans <lastmod>)")
    SITEMAP_PATH.write_text(sitemap, encoding="utf-8")


def build() -> list[pathlib.Path]:
    if not PAGES_DIR.is_dir():
        sys.exit(f"Dossier introuvable : {PAGES_DIR}")

    written = []
    changed_urls = []
    photo_slots = load_photo_slots()

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
            content = render_photos(content, lang, photo_slots, page_path)

            remaining = [
                t for t in ("{{HEADER}}", "{{FOOTER}}", "{{HREFLANG}}", "{{LANGSWITCH}}",
                            "{{PHOTO", "{{GALLERY}}")
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
            previous = output_path.read_text(encoding="utf-8") if output_path.is_file() else None
            if content != previous:
                changed_urls.append(page_url(lang, slug))
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

    update_sitemap_lastmod(changed_urls)
    return written


if __name__ == "__main__":
    for path in build():
        print(f"Généré : {path.relative_to(ROOT)}")
