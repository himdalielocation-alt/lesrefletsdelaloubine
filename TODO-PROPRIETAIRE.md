# À faire / à fournir — propriétaire

Document de travail (non publié). Tout ce qui suit reste en commentaire `<!-- TODO(proprio) : ... -->` dans le code tant que non fourni — rien n'est affiché sur le site avant validation.

## Informations à me donner

### Le logement
- [x] Pièce de chaque couchage : 2 lits simples dans la chambre, lit armoire dans la pièce principale — **intégré** (accueil, FAQ, JSON-LD, 3 langues)
- [x] Dates des piscines : formulation des fiches résidence retenue, « d'avril à fin septembre, selon météo » — **intégré partout** (accueil, FAQ, page activités, JSON-LD, 3 langues). Conséquence : la carte « Moyenne saison » (mai, juin, septembre, octobre) précise désormais « Accès aux 2 piscines chauffées (jusqu'à fin septembre) »
- [x] Classement : meublé de tourisme classé 2 étoiles (classement officiel, pas le label Clévacances) — **intégré** (liste « À propos », JSON-LD `starRating: 2`)
- [x] Surface : 25 m² — **intégré** (« Capacité : 4 personnes · 25 m² », JSON-LD `floorSize`)
- [x] Étage : rez-de-chaussée — **intégré** (liste « À propos », FAQ « À quel étage se trouve l'appartement ? »). Rien n'est affiché sur l'accessibilité PMR (marches, largeur des portes…) faute d'information
- [x] Wi-Fi : non — **intégré** en FAQ (« Non, l'appartement n'a pas de connexion Wi-Fi »)
- [x] Lave-vaisselle dans l'appartement, lave-linge dans la résidence — **intégré** (carte « Cuisine équipée », FAQ, JSON-LD)
- [x] Linge de lit : en option, 12 € par lit pour le séjour — **intégré** (FAQ, mention sous les tarifs)
- [x] Animaux : non acceptés — **intégré** (FAQ, JSON-LD `petsAllowed: false`)
- [x] Horaires : arrivée à partir de 17h, départ avant 10h — **intégré** (FAQ, JSON-LD `checkinTime`/`checkoutTime` rétablis)
- [x] Caution : 300 € par empreinte bancaire (ex. Swikly, compte à créer de votre côté) — **intégré** (FAQ, sans nommer le service)
- [x] Annulation : 25 % d'arrhes à la réservation, solde 30 jours avant l'arrivée ; annulation > 30 jours : arrhes conservées ; < 30 jours : séjour dû sauf relocation ; assurance annulation conseillée — **intégré** (FAQ). À reprendre à l'identique dans votre contrat de location
- [x] Paiement : virement bancaire uniquement — **intégré** (FAQ « Comment se passe la réservation ? », JSON-LD `paymentAccepted`)
- [x] Délai de réponse : sous 24h — **intégré** (étape 3 de la section réservation, 3 langues)
- [x] Numéro d'enregistrement : 8519400689700 — **intégré** (mentions légales et pied de page de toutes les pages, 3 langues). La mention « Immatriculation en cours » du calendrier a été retirée
- [x] Numéro de téléphone : pas de téléphone affiché, choix définitif — seul l'e-mail reste comme contact (le TODO correspondant a été retiré du code)
- [x] Annonce Airbnb : https://www.airbnb.fr/h/lesrefletsdelaloubine — **intégré** (encart Airbnb de la section réservation, JSON-LD `sameAs`, 3 langues)
- [x] « Votre hôte » : « Maryse et ses enfants sont heureux de vous accueillir aux Sables-d'Olonne » — **intégré** dans la carte « Contact direct avec vos hôtes » (anciennement « … avec le propriétaire »), 3 langues

### L'emplacement
- [x] Adresse résidence utilisée : 65 rue du Puits d'Enfer, Château-d'Olonne, 85180 Les Sables-d'Olonne — **à valider définitivement** (déjà utilisée dans le JSON-LD suite à votre validation du plan Phase 0, mais vous pouvez encore corriger)
- [x] Coordonnées GPS : 46.473392, -1.745570, relevées par vous sur Google Maps — **intégré** (carte, liens itinéraire, JSON-LD, 3 langues)

### Évènements
- [x] Village Vendée Globe 2028 : du 20 octobre au 12 novembre 2028 — **intégré** (page `vendee-globe-2028.html`, 3 langues ; horaires 2028 non précisés)
- [ ] Photo du départ ou du village du Vendée Globe dont vous détenez les droits (pour la page Vendée Globe)
- [x] IRONMAN Les Sables-d'Olonne–Vendée : 27 juin 2027, confirmé — **intégré** (page activités, 3 langues)
- [ ] Dates 2027 : ponts de mai, Vendée Va'a, Journées européennes du patrimoine

### Mentions légales et confidentialité
- [x] Éditeur du site : Maryse Courant, Résidence L'Estran, 65 rue du Puits d'Enfer, Château-d'Olonne, 85180 Les Sables-d'Olonne — **intégré** (3 langues)
- [x] Directeur de la publication : Maryse Courant — **intégré** (3 langues)
- [x] Durée de conservation : demande sans suite 3 ans après le dernier échange ; séjour réservé : durée de la relation + 5 ans ; factures : 10 ans — **intégré** (3 langues)

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
- [ ] Plage (Tanchet ou à proximité) — remplace la 3e photo « galerie » de l'accueil, actuellement en placeholder
- [ ] Le Puits d'Enfer

## Actions techniques à faire vous-même (une fois le site en ligne)

- [ ] Soumettre `sitemap.xml` dans Google Search Console
- [ ] Soumettre les nouvelles pages (activités, Vendée Globe le cas échéant) dans Search Console
- [x] HTTPS et redirection `www.lesrefletsdelaloubine.fr` → site : vérifié par vous
- [ ] Tester le JSON-LD sur [validator.schema.org](https://validator.schema.org) et sur le [test des résultats enrichis de Google](https://search.google.com/test/rich-results)
- [ ] Ajouter le site dans Bing Webmaster Tools
- [ ] Obtenir l'autorisation de changement d'usage — tant qu'elle n'est pas obtenue, le site garde « Réservation bientôt disponible » (badge du calendrier) et « Bientôt disponible » (cartes de tarifs) ; me prévenir pour les remplacer par « Demander mes dates »
- [ ] Créer le compte Swikly pour la caution (plus tard)
- [ ] Reprendre les conditions de caution et d'annulation dans le contrat de location (clauses proposées dans la conversation)

## Décisions déjà prises avec votre accord

- Header/footer désormais générés depuis `templates/` (voir `CLAUDE.md`) — éditez `templates/pages/` et `templates/includes/`, pas les fichiers à la racine
- JSON-LD nettoyé des faits non confirmés puis restructuré en `WebSite` + `VacationRental` (voir `AUDIT-SEO.md`)
- Title, meta description et H1 de l'accueil choisis parmi 3 propositions chacun
- CSS compilé via Tailwind CLI à la place du CDN — **à vérifier après le premier push** (voir la mise en garde dans `CLAUDE.md`)
- Pages Mentions légales et Politique de confidentialité créées et liées depuis le footer
- Verbe unique pour l'action de réservation partout sur le site : « Demander mes dates » (mission UX/accessibilité, Phase 1) — remplace les 4 formulations différentes qui coexistaient (« Réserver en direct », « Demander une réservation », « Envoyer une demande par e-mail », « Réserver »)
- Pas de bouton ni de widget d'accessibilité : conformément à la règle du brief UX/accessibilité (les overlays d'accessibilité ne rendent pas un site réellement accessible), confirmé explicitement par vous
- Pas de refonte visuelle (pistes A/B refusées) : la mission UX/accessibilité continue uniquement sur les corrections fonctionnelles et d'accessibilité (structure, contenu, parcours), sans changement d'apparence proposé de votre propre initiative
- Site traduit en anglais et en allemand (`/en/`, `/de/`), avec un bouton de langue flottant (drapeaux) en bas à droite de chaque page — architecture documentée dans `CLAUDE.md`

## À vérifier : traductions

- [ ] **Mentions légales et Politique de confidentialité en anglais et en allemand** : traduites par mes soins, mais un texte juridique traduit comporte toujours un risque de nuance incorrecte — à faire relire par vous ou un professionnel avant de les considérer définitives, notamment si vous visez particulièrement une clientèle DE/UK.
- [ ] Le reste du contenu (accueil, page activités) a été traduit avec le même soin que le français d'origine, mais une relecture par un locuteur natif reste toujours une bonne pratique avant mise en ligne définitive.
