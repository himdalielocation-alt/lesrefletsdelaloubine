# Les Reflets de la Loubine — notes techniques

Site statique (aucun framework), hébergé sur GitHub Pages, domaine `lesrefletsdelaloubine.fr` (voir `CNAME`). `.nojekyll` désactive le traitement Jekyll par défaut de GitHub Pages.

## Header et footer partagés (templates)

Le header et le footer sont identiques sur toutes les pages. Pour éviter de les dupliquer et de devoir répéter chaque correctif sur chaque fichier :

- **Vous éditez le contenu propre à chaque page dans `templates/pages/`** (`index.html`, `activites-sables-d-olonne.html`, `404.html`), avec les jetons `{{HEADER}}` et `{{FOOTER}}` aux emplacements du header/footer.
- **Le header et le footer eux-mêmes se modifient une seule fois**, dans `templates/includes/header.html` et `templates/includes/footer.html`. Toutes les URLs y sont en absolu (`/`, `/#presentation`, `/activites-sables-d-olonne.html`...) car ce même include est réutilisé sur toutes les pages, y compris `404.html`.
- **Le JS du menu burger est un fichier partagé** : `assets/js/menu.js`, référencé par `<script src="/assets/js/menu.js" defer></script>` sur chaque page — rien à dupliquer là non plus.

### Régénérer les pages

```
python3 scripts/build_pages.py
```

Ce script lit `templates/pages/*.html`, remplace `{{HEADER}}`/`{{FOOTER}}` par le contenu des includes, et écrit le résultat à la racine du dépôt (`index.html`, `activites-sables-d-olonne.html`, `404.html`) — ce sont ces fichiers à la racine que GitHub Pages sert réellement. Aucune dépendance à installer (Python standard uniquement).

**En pratique** : un workflow GitHub Actions (`.github/workflows/build-pages.yml`) régénère et commit automatiquement ces fichiers dès qu'un push sur `main` touche `templates/**`. Vous n'avez normalement pas besoin de lancer la commande vous-même — mais vous pouvez si vous voulez vérifier le résultat avant de pousser.

### Ajouter une nouvelle page

1. Créer `templates/pages/ma-nouvelle-page.html` avec `{{HEADER}}` et `{{FOOTER}}` aux bons endroits (voir un fichier existant comme modèle pour le `<head>` : Tailwind CDN, polices, tokens de couleur).
2. Ajouter le lien vers cette page dans `templates/includes/header.html` (nav desktop + menu mobile) si elle doit apparaître dans la navigation.
3. Lancer `python3 scripts/build_pages.py` pour vérifier localement (ou laisser le workflow le faire au push).
4. Penser à l'ajouter dans `sitemap.xml`.

## Calendrier de disponibilités (ne pas modifier sans comprendre le mécanisme)

- `.github/workflows/sync-calendar.yml` : tourne tous les jours à minuit UTC (+ déclenchement manuel), lit un Google Sheet via un compte de service (secret `GOOGLE_SERVICE_ACCOUNT_JSON`), écrit `data/calendar.json`, commit et push sur `main`.
- `index.html` charge ce fichier côté client via `fetch('data/calendar.json')` (même origine, aucune dépendance tierce) pour construire le calendrier visuel.
- Ce mécanisme est indépendant du système de templates ci-dessus : `data/calendar.json` n'est pas un template, il est généré par `scripts/sync-calendar.py`, pas par `scripts/build_pages.py`.

## Fichiers de travail non publiés

`CLAUDE.md`, `AUDIT-SEO.md`, `TODO-PROPRIETAIRE.md` sont des notes de travail, pas du contenu du site. `.nojekyll` évite que GitHub Pages les transforme en pages HTML publiées ; ils ne sont listés dans aucune navigation ni dans `sitemap.xml`.
