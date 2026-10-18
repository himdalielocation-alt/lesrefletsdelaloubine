#!/usr/bin/env python3
"""Signale à IndexNow (Bing, Yahoo, DuckDuckGo, Ecosia, Yandex…) les pages du
sitemap modifiées récemment, pour qu'elles soient explorées sans attendre.

La clé est le nom du fichier <clé>.txt à la racine du site (son contenu est la
clé elle-même) : c'est ce qui prouve à IndexNow que le site nous appartient.
Google n'utilise pas IndexNow (pour Google : Search Console).

Usage : python3 scripts/indexnow.py [nombre_de_jours]   (défaut : 2)
Lancé chaque jour par .github/workflows/indexnow.yml. Python standard uniquement.
"""
import datetime
import json
import pathlib
import re
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
HOST = "lesrefletsdelaloubine.fr"


def main() -> None:
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    keys = [p.stem for p in ROOT.glob("*.txt") if re.fullmatch(r"[0-9a-f]{32}", p.stem)
            and p.read_text().strip() == p.stem]
    if not keys:
        sys.exit("Aucun fichier de clé IndexNow (<clé>.txt) à la racine du dépôt.")
    key = keys[0]

    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    since = datetime.date.today() - datetime.timedelta(days=days)
    urls = [
        loc for loc, lastmod in re.findall(r"<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>", sitemap)
        if datetime.date.fromisoformat(lastmod[:10]) >= since
    ]
    if not urls:
        print(f"Aucune page modifiée depuis le {since} : rien à signaler.")
        return

    body = json.dumps({
        "host": HOST,
        "key": key,
        "keyLocation": f"https://{HOST}/{key}.txt",
        "urlList": urls,
    }).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        print(f"IndexNow : {len(urls)} URL(s) signalée(s), réponse HTTP {resp.status}")
        for url in urls:
            print(" -", url)


if __name__ == "__main__":
    main()
