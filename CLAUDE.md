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
5. Si la page utilise des classes Tailwind qui n'apparaissent sur aucune autre page, vérifier qu'elle est bien scannée par `tailwind.config.js` (`content: [...]`) — sinon ses classes ne seront pas générées dans le CSS compilé.

## Site multilingue (FR/EN/DE)

Le site existe en français (racine), anglais (`/en/`) et allemand (`/de/`), avec les mêmes noms de fichiers dans chaque langue (ex. `activites-sables-d-olonne.html`, `/en/activites-sables-d-olonne.html`, `/de/activites-sables-d-olonne.html`) — c'est ce qui permet au bouton de langue de toujours pointer vers l'équivalent exact de la page courante dans l'autre langue, sans table de correspondance.

- **Pages traduites** : `templates/pages/en/*.html` et `templates/pages/de/*.html`, mêmes noms de fichiers et même structure que leurs équivalents français dans `templates/pages/`. Les chemins vers les ressources (images, icônes `brand/`, `data/calendar.json`) doivent y être en **absolu** (`/images/...`, pas `images/...`) puisque ces pages sont servies depuis un sous-dossier.
- **Header/footer traduits** : `templates/includes/header.en.html`, `header.de.html`, `footer.en.html`, `footer.de.html` — mêmes principes que les versions françaises (URLs absolues, `data-label-open`/`data-label-close` sur le bouton burger pour que `assets/js/menu.js`, partagé entre les 3 langues, annonce le bon texte).
- **`404.html` reste unique** (une seule version, en français) : GitHub Pages ne sert qu'un seul fichier 404 pour tout le site, quel que soit le préfixe de langue de l'URL demandée — impossible d'en avoir un par langue avec ce hébergement.
- **`{{HREFLANG}}`** : jeton présent dans le `<head>` des 4 pages traduisibles (`index.html`, `activites-sables-d-olonne.html`, `mentions-legales.html`, `politique-de-confidentialite.html`, dans chacune des 3 langues). `scripts/build_pages.py` le remplace automatiquement par les 4 balises `<link rel="alternate" hreflang="...">` (fr/en/de/x-default) — rien à taper à la main.
- **`{{LANGSWITCH}}`** : jeton placé une seule fois par page (juste après `{{HEADER}}`), remplacé par le bouton flottant (drapeaux 🇫🇷🇬🇧🇩🇪, coin bas-droit, `position: fixed`) qui bascule vers l'équivalent de la page courante dans les 2 autres langues. Généré par `scripts/build_pages.py`, pas à écrire à la main.
- **`sitemap.xml`** : chaque URL liste ses 3 variantes de langue via `<xhtml:link rel="alternate" hreflang="...">`, en plus de son entrée `<loc>` propre — 12 entrées au total (3 langues × 4 pages traduisibles).
- **Pour ajouter une 4ᵉ page traduisible** : créer le fichier français dans `templates/pages/`, ses 2 traductions dans `templates/pages/en/` et `templates/pages/de/` (mêmes classes/structure, texte traduit, chemins de ressources absolus), ajouter son nom de fichier à `TRANSLATED_PAGES` dans `scripts/build_pages.py`, ajouter `{{HREFLANG}}` dans son `<head>` et `{{LANGSWITCH}}` juste après `{{HEADER}}`, puis l'ajouter à `sitemap.xml` (3 entrées, avec les 4 `hreflang` sur chacune).

## CSS (Tailwind CLI, plus de CDN)

Le site chargeait `cdn.tailwindcss.com` en production (script de prototypage, déconseillé par Tailwind lui-même hors développement). Remplacé par un CSS compilé et minifié :

- **Source** : `templates/tailwind-input.css` (directives `@tailwind` + tous les styles custom : polices, tokens de couleur clair/sombre, classes typographiques `.affiche`/`.titre-1`/etc., `.icono`, `.pastille`...). C'est là qu'on modifie les styles custom désormais, plus dans un `<style>` par page.
- **Config** : `tailwind.config.js` à la racine (couleurs, polices, rayons, ombres — reprend exactement ce qui était avant dans chaque `<script>tailwind.config = {...}</script>`).
- **Sortie** : `assets/css/styles.css`, référencé par `<link rel="stylesheet" href="/assets/css/styles.css">` sur chaque page.

### Compiler

```
npm install
npm run build:css
```

**En pratique**, comme pour les pages : le workflow `.github/workflows/build-css.yml` recompile et commit `assets/css/styles.css` automatiquement au push sur `main`, dès que `templates/tailwind-input.css`, `tailwind.config.js` ou le contenu de `templates/pages/`/`templates/includes/` changent.

⚠️ **Cette étape n'a pas pu être testée dans l'environnement où elle a été écrite** (le registre npm y était bloqué, donc impossible d'installer le CLI Tailwind ni de vérifier le rendu avant de committer). Après le premier push touchant le CSS : vérifiez que `.github/workflows/build-css.yml` se termine en vert dans l'onglet Actions de GitHub, que `assets/css/styles.css` a bien été généré (non vide), et ouvrez le site pour comparer visuellement avec ce que vous connaissiez avant. Si quelque chose cloche, le plus simple est de me dire ce qui a changé visuellement, ou de rouvrir `assets/css/styles.css` généré et regarder si une classe utilisée dans le HTML semble absente du CSS (signe que `tailwind.config.js` ne scanne pas le bon fichier).

## Calendrier de disponibilités (ne pas modifier sans comprendre le mécanisme)

- `.github/workflows/sync-calendar.yml` : tourne tous les jours à minuit UTC (+ déclenchement manuel), lit un Google Sheet via un compte de service (secret `GOOGLE_SERVICE_ACCOUNT_JSON`), écrit `data/calendar.json`, commit et push sur `main`.
- `index.html` charge ce fichier côté client via `fetch('data/calendar.json')` (même origine, aucune dépendance tierce) pour construire le calendrier visuel.
- Ce mécanisme est indépendant du système de templates ci-dessus : `data/calendar.json` n'est pas un template, il est généré par `scripts/sync-calendar.py`, pas par `scripts/build_pages.py`.

## Fichiers de travail non publiés

`CLAUDE.md`, `AUDIT-SEO.md`, `TODO-PROPRIETAIRE.md` sont des notes de travail, pas du contenu du site. `.nojekyll` évite que GitHub Pages les transforme en pages HTML publiées ; ils ne sont listés dans aucune navigation ni dans `sitemap.xml`.
