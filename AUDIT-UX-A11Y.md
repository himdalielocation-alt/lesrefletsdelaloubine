# Audit UX, design et accessibilité — lesrefletsdelaloubine.fr

Document de travail (non publié — voir `.nojekyll`, non listé dans la navigation ni dans `sitemap.xml`). Réalisé en Phase 0 de la mission UX/accessibilité, sur la base du site tel qu'il existait après la mission SEO précédente (branche `seo` déjà fusionnée dans `main`).

## Préalable : écart entre le brief et l'état réel du site

Le brief de mission décrit une palette « cyan/pierre » et un duo de polices « Playfair Display + Inter ». Ce n'est plus l'état réel du site : une refonte de marque antérieure a introduit des jetons de couleur propres (« Reflets de la Loubine ») et les polices maison **Fraunces Reflets** / **Karla Reflets**. Cet audit et toutes les corrections qui suivent travaillent sur l'état réel du site (jetons CSS de `templates/tailwind-input.css`), pas sur la description du brief.

## Limite d'outillage de cet environnement

`axe-core`, Lighthouse et le CLI Tailwind ne sont pas accessibles ici (le registre npm et les CDN externes renvoient une erreur réseau dans ce bac à sable). Cet audit s'appuie donc sur des vérifications automatisées maison construites avec Playwright/Chromium :
- un calculateur de contraste WCAG (luminance relative + formule de contraste standard), avec calcul du **fond effectif** de chaque élément en compositing les couleurs des ancêtres (gère les fonds transparents/semi-transparents correctement, contrairement à une lecture superficielle de `background-color`) ;
- un parcours DOM listant tous les éléments porteurs de texte direct, sur les 5 pages, aux 3 largeurs (360/768/1280px) et dans les 2 thèmes (clair/sombre) ;
- un test clavier réel (`page.keyboard.press('Tab')` en boucle, avec capture de la position et du nom accessible à chaque étape) ;
- des émulations `forced-colors: active`, `prefers-reduced-motion: reduce`, `color-scheme: dark`.

Recommandation complémentaire : faire tourner l'extension navigateur axe DevTools (ou WAVE) et PageSpeed Insights une fois le site en ligne, pour une deuxième opinion indépendante de cette méthode maison.

---

## Constats — 🔴 Bloquant

| # | Constat | Critère WCAG | Correctif | État |
|---|---|---|---|---|
| 1 | `.surtitre` (bleu-loubine) sur fond `--nuit` : contraste 1.85:1 en mode clair (bandes réservation/CTA activités/footer) | 1.4.3 Contraste minimum | Nouvelle classe `.bande-sombre` fixant `--bleu-loubine` à sa valeur claire, indépendamment du thème | ✅ Corrigé (commit `abda0a5`) |
| 2 | `.legende`/`.chapo` (encre-douce) sur fond `--nuit` : contraste 2.53:1 en mode clair, mêmes bandes | 1.4.3 Contraste minimum | Même classe `.bande-sombre`, fixe aussi `--encre-douce` et `--dune` (bordures) | ✅ Corrigé (commit `abda0a5`) |
| 3 | Cases du calendrier : `<div>` sans nom accessible (numéro seul annoncé), statut porté uniquement par la couleur de fond, changement de mois non annoncé | 4.1.2 Nom/rôle/valeur, 1.4.1 Utilisation de la couleur, 4.1.3 Messages de statut | `aria-label` complet par case (« samedi 12 juillet 2026, disponible »), `aria-live="polite"` sur le mois affiché, indicateur non-couleur (contour pointillé) pour l'état « information non disponible », en plus du texte barré déjà existant pour « occupé » | ✅ Corrigé (commit `172f2f3`) |

## Constats — 🟠 Majeur

| # | Constat | Critère WCAG | Correctif | État |
|---|---|---|---|---|
| 4 | 4 formulations différentes pour la même action de réservation selon la page (« Réserver en direct », « Demander une réservation », « Envoyer une demande par e-mail », « Réserver ») | 3.2.4 Identification cohérente | Verbe unique validé avec le propriétaire : « Demander mes dates », appliqué partout | ✅ Corrigé (commit `07ce655`) |
| 5 | Le clic sur le bouton mailto n'explique pas ce qu'il se passe ensuite (aucune réservation en ligne, juste un e-mail) | Heuristique Nielsen « visibilité de l'état du système » | Parcours en 3 étapes numérotées sous le bouton, + bouton « Copier l'adresse » en repli avec confirmation `aria-live` | ✅ Corrigé (commit `07ce655`) |
| 6 | `<html class="scroll-smooth">` inconditionnel : le défilement fluide ne respecte pas `prefers-reduced-motion` | 2.3.3 Animation en réponse aux interactions | `scroll-smooth` → `motion-safe:scroll-smooth` (variante Tailwind native) | ✅ Corrigé (commit `26ad63c`) |
| 7 | Menu mobile : aucun moyen clavier rapide de le refermer (pas d'Échap), focus non rendu au bouton | 2.1.1 Clavier | Échap ferme le menu et rend le focus au bouton burger (`assets/js/menu.js`) | ✅ Corrigé (commit `26ad63c`) |
| 8 | Carte Leaflet initialisée sans options : molette capture le défilement de la page, glisser à un doigt capture le défilement sur mobile, contrôles de zoom en anglais | 2.5.7 Mouvements de glissement (alternative), cohérence linguistique | `scrollWheelZoom: false`, `dragging`/`tap` désactivés sur tactile uniquement, `L.control.zoom` avec titres en français | ✅ Corrigé (commit `23bc08f`) — non testable en direct ici (Leaflet chargé depuis unpkg.com, bloqué dans ce bac à sable) ; à vérifier sur le site déployé |
| 9 | Adresse e-mail absente du footer sur 4 des 5 pages (seule `index.html` l'affichait, dans la section réservation) | 3.2.6 Aide cohérente | Ajout dans le footer partagé, donc sur les 5 pages en un seul changement | ✅ Corrigé (commit `26ad63c`) |
| 10 | Boutons pleins (fond coloré uni) invisibles en mode contrastes forcés (Windows High Contrast) : le fond disparaît sans laisser de contour | 1.4.11 Contraste du contenu non textuel (esprit du critère) | `border border-transparent` sur tous les boutons pleins ; vérifié par émulation `forced-colors: active` | ✅ Corrigé (commit `26ad63c`) |

## Constats — 🟡 Mineur

| # | Constat | Critère WCAG | Correctif | État |
|---|---|---|---|---|
| 11 | Liens légaux et contact du footer : cible tactile ~20px de hauteur, sous le minimum | 2.5.8 Taille de cible (minimum) | Padding vertical porté à 28px de hauteur | ✅ Corrigé (commit `26ad63c`) |
| 12 | 3 SVG du logo avec `role="img"`/`aria-label` individuels, redondants avec l'`aria-label` du lien parent qui porte déjà le nom accessible complet | 4.1.2 Nom/rôle/valeur (annonces cohérentes) | `aria-hidden="true" focusable="false"` sur les 3 SVG ; 2 icônes du bouton burger et 2 icônes de navigation du calendrier traitées de la même façon | ✅ Corrigé (commit `26ad63c`) |
| 13 | 3 icônes « photo » décoratives dans les blocs placeholder de la galerie, déjà doublées d'une légende textuelle explicite | 1.1.1 Contenu non textuel (redondance à éviter) | `aria-hidden="true" focusable="false"` sur les 3 icônes | ✅ Corrigé (commit `26ad63c`) |
| 14 | Jours de la semaine du calendrier affichés seulement en abrégé (Lun, Mar…) | 1.3.1 Information et relations | Ligne d'en-tête passée en `aria-hidden` (redondante : le nom complet du jour est déjà dans l'`aria-label` de chaque case) plutôt que dupliquée en texte cachée | ✅ Corrigé (commit `172f2f3`) |
| 15 | Skip-link « Aller au contenu principal » : même problème de bordure que le constat 10 une fois visible au focus | 1.4.11 (esprit) | `border border-transparent` ajouté sur les 5 pages | ✅ Corrigé (commit `26ad63c`) |
| 16 | Cartes de saison (« Bientôt disponible ») : contraste testé isolément avec un script maison simplifié qui ignorait le canal alpha d'un fond transparent — fausse alerte | — | Aucun correctif nécessaire ; confirmé par le scan complet (compositing correct) que cet élément passe déjà | ✔️ Faux positif, pas un vrai constat |
| 17 | Boutons de navigation du calendrier (mois précédent/suivant) : script de test maison confondant `textContent` vide (espaces de mise en forme) et absence de nom accessible — fausse alerte, l'`aria-label` réel était déjà correct en source | 4.1.2 | Aucun correctif nécessaire | ✔️ Faux positif, pas un vrai constat |

## 🟢 Déjà bon (confirmé, pas de régression)

- Hiérarchie de titres (H1→H2→H3) correcte sur toutes les pages — les sauts de niveau mentionnés dans le brief comme « à confirmer » avaient déjà été corrigés lors de la mission SEO précédente.
- Menu mobile : bouton burger présent avec `aria-expanded`/`aria-controls`/`aria-label`, bascule d'icône correcte.
- Header fixe (80px) : le léger chevauchement mesuré au clic sur un ancre (~1.5px) est négligeable, pas un vrai constat de focus masqué (2.4.11) — vérifié par clic réel + attente du défilement fluide, pas par un `scrollIntoView()` synchrone qui aurait donné un résultat trompeur.
- Logo : nom accessible correct sur le lien parent (`aria-label="Les Reflets de la Loubine — Accueil"`).
- Boutons de navigation du calendrier : `aria-label="Mois précédent"` / `"Mois suivant"` déjà présents en source (voir constat 17, faux positif de test).
- Calendrier : mécanisme de synchronisation quotidienne (`sync-calendar.yml` → `data/calendar.json`) non touché, fonctionne toujours.
- Carte : chargement à la demande (IntersectionObserver) non touché, fonctionne toujours.
- SEO : title/meta/H1/canonical/JSON-LD/sitemap/`google-site-verification` non touchés.

---

## Table de contraste — paires en échec avant correctif

| Élément | Avant | Après | Seuil AA | Pages concernées |
|---|---|---|---|---|
| `.surtitre` (bleu-loubine) sur `--nuit` | 1.85:1 ❌ | 9.36:1 ✅ | 4.5:1 | Accueil (réservation), Activités (CTA) |
| `.chapo`/`.legende` (encre-douce) sur `--nuit` | 2.53:1 ❌ | 10.27:1 ✅ | 4.5:1 | Accueil, Activités, Footer (5 pages) |
| Liens du footer (encre-douce) sur `--nuit` | 2.53:1 ❌ | 10.27:1 ✅ | 4.5:1 | Les 5 pages (footer partagé) |
| Texte principal du footer (`corps-fort`, ecume-nuit) sur `--nuit` | déjà correct (fix antérieur `--ecume-nuit`) | 17.19:1 ✅ | 4.5:1 | Les 5 pages |

---

## Parcours clavier (carte des arrêts de tabulation, accueil, avant correctifs Phase 1)

17 éléments focusables en ordre, du haut de la page à la section réservation : skip-link → logo → 5 liens de navigation desktop → « Espace locataire » → « Réserver en direct » (devenu « Demander mes dates ») → bouton burger → (liens du menu mobile si ouvert) → CTA hero primaire → CTA hero secondaire → boutons de saison (désactivés, non focusables, normal) → boutons prev/next du calendrier → bouton mailto → liens Mentions légales/Politique de confidentialité (footer).

**Trou principal identifié** : les cases du calendrier n'étaient pas dans ce parcours du tout (ni focusables, ni annoncées) — corrigé par l'ajout des `aria-label`, sans ajouter de nouveaux arrêts de tabulation (voir constat 3 : volontairement non focusables, puisque non interactives, pour ne pas alourdir le parcours de ~30 arrêts par mois).

---

## Ce qui fonctionne déjà bien (à préserver dans la suite de la mission)

- Structure sémantique globale (landmarks `header`/`main`/`footer`/`nav`, un seul H1 par page).
- Chargement différé de la carte (perf + n'impose pas Leaflet à qui ne fait pas défiler jusque-là).
- TODO(proprio) déjà en place pour les faits non confirmés (téléphone, Airbnb, adresse) — bon réflexe à poursuivre, repris pour le délai de réponse et les conditions de réservation (voir `TODO-PROPRIETAIRE.md`).
- Design tokens CSS centralisés (`:root` + variante `prefers-color-scheme: dark`), qui permettent des correctifs ciblés comme `.bande-sombre` sans dupliquer de styles page par page.
- Site 100% statique, aucune dépendance qui casserait la navigation/le contenu si JS est désactivé (à reconfirmer explicitement en Phase 5).

---

## Plan priorisé (validé avec le propriétaire)

1. ✅ Contrastes des bandes sombres (constats 1-2) — un seul token CSS à étendre, corrige 4 pages d'un coup, faible effort/fort impact.
2. ✅ Calendrier accessible (constat 3) — le plus gros morceau technique de la phase 1.
3. ✅ Corrections structurelles diverses (constats 6, 7, 9-13, 15) — menu clavier, footer, cibles tactiles, SVG décoratifs, mode contrastes forcés, mouvement réduit.
4. ✅ Carte Leaflet (constat 8) — molette/glisser tactile, contrôles en français.
5. ✅ Cohérence du parcours de réservation (constats 4-5) — verbe unique validé avec le propriétaire, étapes numérotées, bouton copier l'adresse.
6. ⏳ Choix de la piste visuelle (A ou B, voir ci-dessous) puis mise en œuvre — volontairement en dernier pour ne pas mélanger accessibilité et esthétique dans les mêmes commits.

Tout ce qui précède (1 à 5) est commité sur la branche `ux-accessibilite` (pull request [#2](https://github.com/himdalielocation-alt/lesrefletsdelaloubine/pull/2)).

---

## Pistes visuelles (Phase 3 — proposées en Phase 0, choix encore à faire)

Deux mockups temporaires (`_mockup-piste-a.html` / `_mockup-piste-b.html`) ont été créés puis supprimés après capture d'écran, pour respecter la contrainte « aucune modification de fichier » de la Phase 0. Captures envoyées en pièces jointes dans la conversation.

- **Piste A — évolution discrète** : mêmes couleurs et polices, hero en deux colonnes (texte/photo), liste factuelle à puces à la place du badge arrondi actuel, un seul CTA primaire clair (« Demander mes dates ») + un CTA secondaire.
- **Piste B — évolution plus affirmée** : la vue mer comme élément visuel fort (photo plein cadre en fond de hero avec dégradé de lisibilité), typographie plus marquée, toujours avec les mêmes polices (Fraunces Reflets / Karla Reflets) et le même vocabulaire de couleur — un seul élément mémorable plutôt que plusieurs cartes.

Ce choix reste à faire par le propriétaire avant la mise en œuvre de la Phase 3.
