# À faire / à fournir — propriétaire

Document de travail (non publié). Tout ce qui suit reste en commentaire `<!-- TODO(proprio) : ... -->` dans le code tant que non fourni — rien n'est affiché sur le site avant validation.

## Informations à me donner

### Le logement
- [ ] Pièce où se trouve chaque couchage (2 lits simples + lit armoire)
- [ ] Formulation unique pour les dates des piscines — à choisir entre : « 15 mai – 15 octobre » (accueil actuel) / « mai à octobre » (page activités actuelle) / « avril à fin septembre selon météo » (fiches résidence)
- [ ] Nombre d'étoiles du classement meublé de tourisme
- [ ] Surface du logement
- [ ] Étage et ascenseur (oui/non)
- [ ] Wi-Fi (disponible ? gratuit ?)
- [ ] Lave-vaisselle / lave-linge
- [ ] Linge fourni ou non
- [ ] Animaux acceptés ou non
- [ ] Horaires d'arrivée et de départ (utilisés dans le JSON-LD `checkinTime`/`checkoutTime`, actuellement retirés faute de confirmation)
- [ ] Caution
- [ ] Conditions d'annulation
- [ ] Numéro d'enregistrement du meublé de tourisme
- [ ] Numéro de téléphone (actuellement « 06 XX XX XX XX » factice)
- [ ] Lien de l'annonce Airbnb (actuellement « Lien disponible prochainement »)
- [ ] Quelques lignes « Votre hôte »

### L'emplacement
- [x] Adresse résidence utilisée : 65 rue du Puits d'Enfer, Château-d'Olonne, 85180 Les Sables-d'Olonne — **à valider définitivement** (déjà utilisée dans le JSON-LD suite à votre validation du plan Phase 0, mais vous pouvez encore corriger)
- [ ] Coordonnées GPS précises : je proposerai un géocodage Nominatim/OpenStreetMap de l'adresse ci-dessus pour comparaison avec les valeurs actuelles (46.4741, -1.7483) — à valider avant remplacement

### Évènements
- [ ] Dates exactes du village de course Vendée Globe (le départ du 12 novembre 2028 est donné, le village « environ trois semaines avant » reste à préciser)
- [ ] Confirmation officielle de la date IRONMAN Les Sables-d'Olonne–Vendée (27 juin 2027 annoncé, à vérifier sur le site officiel)
- [ ] Dates 2027 : ponts de mai, Vendée Va'a, Journées européennes du patrimoine

### Mentions légales (Phase 5, à venir)
- [ ] Identité de l'éditeur du site (nom, adresse) pour la page Mentions légales

## Photos à prendre (remplacent les placeholders actuels)

Remplacent les 3 photos Unsplash de la section « Le Logement » (ne représentent pas le vrai logement) et les 8 blocs « Photo à ajouter » de la page activités :

- [ ] Vue depuis le salon
- [ ] Vue depuis la terrasse
- [ ] Séjour
- [ ] Chambre
- [ ] Lit armoire ouvert
- [ ] Lit armoire fermé
- [ ] Cuisine
- [ ] Salle de bain
- [ ] Les 2 piscines de la résidence
- [ ] Extérieurs / espaces verts de la résidence
- [ ] Le Puits d'Enfer

## Actions techniques à faire vous-même (une fois le site en ligne)

- [ ] Soumettre `sitemap.xml` dans Google Search Console
- [ ] Soumettre les nouvelles pages (activités, Vendée Globe le cas échéant) dans Search Console
- [ ] Vérifier que HTTPS fonctionne et que `www.lesrefletsdelaloubine.fr` redirige bien vers `lesrefletsdelaloubine.fr` (ou l'inverse selon votre config CNAME)
- [ ] Tester le JSON-LD sur [validator.schema.org](https://validator.schema.org) et sur le [test des résultats enrichis de Google](https://search.google.com/test/rich-results)
- [ ] Ajouter le site dans Bing Webmaster Tools

## Décisions déjà prises avec votre accord

- Header/footer désormais générés depuis `templates/` (voir `CLAUDE.md`) — éditez `templates/pages/` et `templates/includes/`, pas les fichiers à la racine
- JSON-LD nettoyé des faits non confirmés (voir `AUDIT-SEO.md`)
