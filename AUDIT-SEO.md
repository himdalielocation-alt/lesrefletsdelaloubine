# Audit SEO — Les Reflets de la Loubine

Document de travail (non publié, voir `.nojekyll` et la section « Fichiers de travail non publiés » de `CLAUDE.md`). Mis à jour au fil de la mission SEO, branche `seo`.

## Constats de la Phase 0 (audit initial) — état actuel

### 🔴 Conformité règle 0

| Constat | Statut |
|---|---|
| JSON-LD accueil : `starRating: 3` non confirmé, présenté comme un fait | ✅ Retiré |
| JSON-LD : `checkinTime`/`checkoutTime` non confirmés | ✅ Retirés |
| JSON-LD : `paymentAccepted: "Virement bancaire"` absent des faits de référence | ✅ Retiré |
| JSON-LD : `postalCode: "85100"` incorrect | ✅ Corrigé en 85180, adresse complète |
| JSON-LD : `priceRange` jusqu'à 130€ alors que le tarif max affiché est 110€ | ✅ Corrigé |
| 3 photos Unsplash hotlinkées ne représentant pas le logement réel | ✅ Remplacées par des placeholders honnêtes ; en attente de vos vraies photos |
| Téléphone factice « 06 XX XX XX XX » | ✅ Retiré |
| « Lien disponible prochainement » (Airbnb, bouton trompeur) | ✅ Reformulé honnêtement |
| 16 blocs « Photo à ajouter » visibles (page activités) | ✅ Masqués, commentaires HTML conservés pour l'ajout futur |

### 🟠 Technique — fondations SEO

| Constat | Statut |
|---|---|
| `.nojekyll` absent (risque de publication des .md par Jekyll) | ✅ Ajouté |
| Hiérarchie de titres cassée (accueil : H3 sans H2 parent, H2→H4) | ✅ Corrigée |
| Liens internes `activites-sables-d-olonne.html` → `index.html` au lieu de `/` | ✅ Corrigés (12 liens) |
| Lien du logo sans nom accessible, `href="#"` | ✅ Corrigé (`aria-label`, `href="/"`) |
| `<main>` absent sur l'accueil | ✅ Ajouté |
| Aucun lien d'évitement | ✅ Ajouté sur toutes les pages |
| Pas de `404.html` | ✅ Créée, cohérente avec l'identité visuelle |
| Pas d'`apple-touch-icon` | ✅ Généré (180×180, depuis le SVG existant) |
| Pas d'élément `<address>` pour le contact | ✅ Ajouté |
| Header/footer dupliqués sur 3 pages (risque d'oubli) | ✅ Système de templates + build automatique |
| Titre accueil 68 caractères (tronqué) | ✅ 56 caractères |
| Meta description accueil 210 caractères (tronquée) | ✅ 155 caractères |
| H1 accueil sans le lieu | ✅ Réécrit avec le lieu |
| Pas de mentions légales / politique de confidentialité | ✅ Créées, liées depuis le footer partagé |

### 🟡 Performance (Core Web Vitals)

| Constat | Statut |
|---|---|
| `cdn.tailwindcss.com` en production | ✅ Remplacé par un CSS compilé (Tailwind CLI) — **non testé localement, à vérifier après le premier push** (voir `CLAUDE.md`) |
| Leaflet chargé de façon bloquante dans le `<head>` | ✅ Chargement à la demande (IntersectionObserver), attribution OpenStreetMap avec lien corrigée |
| Aucun `<img>` avec `width`/`height`/`loading`/`fetchpriority` | ✅ Fait sur l'unique image réelle restante (hero) ; les autres sont des placeholders sans `<img>` |
| Pas de `preload` sur les polices critiques | ✅ Ajouté (Fraunces Reflets + Karla Reflets, sur toutes les pages) |
| SVG du logotype (29,5 Ko) dupliqué sur chaque page | Info — accepté tel quel (le gain de mutualisation nécessiterait un changement de format, hors périmètre immédiat) |

### JSON-LD (Phase 3)

`LodgingBusiness` → restructuré en `WebSite` (nom du site) + `VacationRental` avec `containsPlace → Accommodation` (occupation, pièces, équipements, literie). Pas de `sameAs` (pas de lien Airbnb confirmé), pas d'`AggregateRating`/`Review` (aucun avis fourni). `BreadcrumbList` déjà présent sur la page activités.

### 🟢 Déjà conforme (état initial, non touché)

`robots.txt`, `sitemap.xml` (structure), canonical + Open Graph, `lang="fr"`, `guide.html`/`build-guide.html` déjà `noindex, nofollow`, hiérarchie de titres propre sur la page activités, titre/meta description de la page activités déjà dans les clous (63/150 caractères).

## Scores Lighthouse

**Non mesurés** : `npx lighthouse` indisponible dans le bac à sable (registre npm bloqué), et `cdn.tailwindcss.com`/`unpkg.com`/`images.unsplash.com` bloqués par la politique réseau du bac à sable — un test local y serait de toute façon faussé, et de toute façon désormais obsolète puisque le CDN Tailwind a été remplacé. **Scores PageSpeed Insights (mobile) sur `/` à fournir par vous**, une fois le site poussé et le workflow de build CSS vérifié vert.

## Ce qui reste (hors périmètre de cette session ou en attente de vos infos)

- Photos réelles (voir `TODO-PROPRIETAIRE.md`)
- Pages évènements (Vendée Globe, IRONMAN) — en attente de dates confirmées
- FAQ, section « Votre hôte », contenu détaillé du logement — Phase 4, nécessite vos infos manquantes
- Version anglaise, formulaire de contact, mesure d'audience, blog — explicitement hors périmètre (section 10 du brief)

## Journal des commits (branche `seo`)

Voir `git log seo` pour l'historique complet, un sujet par commit, messages en français. Rien n'a été poussé sur `origin` sans votre accord explicite.
