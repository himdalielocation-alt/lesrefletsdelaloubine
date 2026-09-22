# lesrefletsdelaloubine

Site vitrine de la location saisonnière « Les Reflets de la Loubine », hébergé sur GitHub Pages avec le domaine personnalisé `lesrefletsdelaloubine.fr` (voir `CNAME`).

## Pages du site

- `index.html` — page d'accueil (présentation, équipements, tarifs & disponibilités, localisation, réservation).
- `activites-sables-d-olonne.html` — article SEO « Que faire aux Sables-d'Olonne ? », accessible depuis le menu (« Que faire ? ») et depuis la section Localisation de la page d'accueil.
- `guide.html` — guide du séjour protégé par mot de passe (voir ci-dessous).
- `build-guide.html` — outil local pour régénérer `guide.html`.

Le domaine réel `https://lesrefletsdelaloubine.fr` est déjà utilisé partout (balises canoniques, Open Graph, JSON-LD, `sitemap.xml`, `robots.txt`) : ce n'est pas un espace réservé à remplacer.

## Photos à ajouter

La page `activites-sables-d-olonne.html` contient des blocs « Photo à ajouter » en attendant de vraies photos. Chaque bloc précise, en commentaire HTML juste au-dessus, le nom de fichier suggéré et le texte alternatif à utiliser. Liste des photos à fournir (à déposer dans `images/`) :

- `images/plages-sables-olonne.jpg` — Plage de La Pironnière aux Sables-d'Olonne, sable fin et rochers à marée basse
- `images/puits-enfer-sables-olonne.jpg` — Le Puits d'Enfer, faille rocheuse sur la corniche des Sables-d'Olonne
- `images/remblai-sables-olonne.jpg` — Le Remblai des Sables-d'Olonne, promenade bordant la Grande Plage
- `images/la-chaume-sables-olonne.jpg` — Le quartier de La Chaume aux Sables-d'Olonne, maisons basses et ruelles colorées
- `images/port-olona-sables-olonne.jpg` — Les pontons de Port Olona aux Sables-d'Olonne, port de départ du Vendée Globe
- `images/velodyssee-sables-olonne.jpg` — Piste cyclable de la Vélodyssée près de la résidence Lagrange L'Estran, Sables-d'Olonne
- `images/zoo-lac-tanchet-sables-olonne.jpg` — Le lac de Tanchet aux Sables-d'Olonne, à proximité du zoo
- `images/ironman-vendee-globe-sables-olonne.jpg` — Évènements sportifs et nautiques aux Sables-d'Olonne (IRONMAN, Vendée Globe)

Une fois une photo ajoutée dans `images/`, remplacez le bloc placeholder correspondant par une balise `<img>` classique dans `activites-sables-d-olonne.html`.

## Guide du séjour (page protégée par mot de passe)

`guide.html` est chiffré (AES-GCM + PBKDF2, côté client, aucun serveur) : le mot de passe n'apparaît jamais dans le code source. Pour le modifier ou changer le mot de passe : ouvrez `build-guide.html` directement dans votre navigateur (double-clic, pas de serveur nécessaire), éditez le contenu et/ou le mot de passe dans le formulaire, cliquez sur « Générer guide.html », puis remplacez le fichier `guide.html` du dépôt par celui téléchargé. Changer le mot de passe suppose toujours de régénérer `guide.html` de cette façon — il n'y a pas d'autre endroit où le modifier.

⚠️ Le contenu chiffré dans `guide.html` contient encore les `{{PLACEHOLDERS}}` par défaut (pas le vrai contenu) : à régénérer via `build-guide.html` une fois les informations réelles renseignées, avant de communiquer le lien aux voyageurs. Le mot de passe n'est volontairement noté nulle part dans ce dépôt.