# Audit SEO — Les Reflets de la Loubine

Document de travail (non publié, voir `.nojekyll` et la section « Fichiers de travail non publiés » de `CLAUDE.md`). Mis à jour au fil de la mission SEO, branche `seo`.

## Constats de la Phase 0 (audit initial)

### 🔴 Conformité règle 0 — corrigé

| Constat | Statut |
|---|---|
| JSON-LD accueil : `starRating: 3` non confirmé, présenté comme un fait | ✅ Retiré (commit `456f132`) |
| JSON-LD : `checkinTime`/`checkoutTime` non confirmés | ✅ Retirés |
| JSON-LD : `paymentAccepted: "Virement bancaire"` absent des faits de référence | ✅ Retiré |
| JSON-LD : `postalCode: "85100"` incorrect | ✅ Corrigé en 85180, adresse complète |
| JSON-LD : `priceRange` jusqu'à 130€ alors que le tarif max affiché est 110€ | ✅ Corrigé |
| 3 photos Unsplash hotlinkées ne représentant pas le logement réel | ⬜ En attente de vos photos (voir `TODO-PROPRIETAIRE.md`) |

### 🟠 Technique — fondations SEO

| Constat | Statut |
|---|---|
| `.nojekyll` absent (risque de publication des .md par Jekyll) | ✅ Ajouté |
| Hiérarchie de titres cassée (accueil : H3 sans H2 parent, H2→H4) | ✅ Corrigée |
| Liens internes `activites-sables-d-olonne.html` → `index.html` au lieu de `/` | ✅ Corrigés (12 liens) |
| Lien du logo sans nom accessible, `href="#"` | ✅ Corrigé (`aria-label`, `href="/"`) |
| `<main>` absent sur l'accueil | ✅ Ajouté |
| Aucun lien d'évitement | ✅ Ajouté sur les 2 pages |
| Pas de `404.html` | ✅ Créée, cohérente avec l'identité visuelle |
| Pas d'`apple-touch-icon` | ✅ Généré (180×180, depuis le SVG existant) |
| Pas d'élément `<address>` pour le contact | ✅ Ajouté |
| Header/footer dupliqués sur 3 pages (risque d'oubli) | ✅ Système de templates + build automatique (commit `ca30ac6`) |
| Titre accueil 68 caractères (tronqué) | ⬜ Phase 4 |
| Meta description accueil 210 caractères (tronquée) | ⬜ Phase 4 |
| H1 accueil sans le lieu | ⬜ Phase 4 |

### 🟡 Performance (Core Web Vitals)

| Constat | Statut |
|---|---|
| `cdn.tailwindcss.com` en production | ⬜ À traiter (build CLI, à documenter avant d'introduire) |
| Leaflet chargé de façon bloquante dans le `<head>` | ⬜ À traiter (chargement à la demande) |
| Aucun `<img>` avec `width`/`height`/`loading`/`fetchpriority` | ⬜ À traiter |
| Pas de `preload` sur les polices critiques | ⬜ À traiter |
| SVG du logotype (29,5 Ko) dupliqué sur chaque page | Info — accepté tel quel pour l'instant (le gain de mutualisation nécessiterait un changement de format, hors périmètre immédiat) |

### 🟢 Déjà conforme

`robots.txt`, `sitemap.xml` (structure), canonical + Open Graph, `lang="fr"`, JSON-LD syntaxiquement valide, polices auto-hébergées avec `font-display: swap`, `guide.html`/`build-guide.html` déjà `noindex, nofollow`, hiérarchie de titres propre sur la page activités, titre/meta description de la page activités déjà dans les clous (63/150 caractères).

### Contenus provisoires visibles (restants)

- « Photo à ajouter » : 16 occurrences (page activités)
- Téléphone factice « 06 XX XX XX XX »
- « Lien disponible prochainement » (Airbnb)

## Scores Lighthouse

**Non mesurés** : `npx lighthouse` indisponible dans le bac à sable (registre npm bloqué), et `cdn.tailwindcss.com`/`unpkg.com`/`images.unsplash.com` bloqués par la politique réseau du bac à sable — un test local y serait de toute façon faussé. Scores PageSpeed Insights (mobile) sur `/` : à fournir par vous, ou je les redemande à la fin de la mission une fois le CDN Tailwind remplacé.

## Journal des commits (branche `seo`)

Voir `git log seo` pour l'historique complet, un sujet par commit, messages en français.
