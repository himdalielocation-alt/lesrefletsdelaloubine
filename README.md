# lesrefletsdelaloubine

Site vitrine de la location saisonnière « Les Reflets de la Loubine », hébergé sur GitHub Pages avec le domaine personnalisé `lesrefletsdelaloubine.fr` (voir `CNAME`).

## Pages du site

- `index.html` — page d'accueil (présentation, équipements, tarifs & disponibilités, localisation, réservation).
- `activites-sables-d-olonne.html` — article SEO « Que faire aux Sables-d'Olonne ? », accessible depuis le menu (« Que faire ? ») et depuis la section Localisation de la page d'accueil.
- `livret.html` — livret d'accueil des voyageurs, chiffré, ouvert uniquement par l'URL complète / le QR code remis dans l'appartement (voir ci-dessous).

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

## Livret d'accueil (page privée)

`livret.html` n'est lié nulle part sur le site, n'est pas dans le sitemap et n'est pas indexé. Son contenu est chiffré (AES-GCM 256) : le dépôt étant public, seul le texte chiffré y figure. La clé est uniquement dans l'URL remise aux voyageurs (`https://lesrefletsdelaloubine.fr/livret.html#k=…`, la partie après `#` n'est jamais envoyée au serveur) : le QR code de l'appartement ouvre donc le livret directement, sans mot de passe. Sans cette URL complète, la page affiche seulement un message d'accueil.

Modifier le livret : `LIVRET_KEY='<URL complète>' node scripts/livret.mjs decrypt > contenu.html`, éditer `contenu.html`, puis `LIVRET_KEY='<URL complète>' node scripts/livret.mjs encrypt contenu.html` (ne pas committer `contenu.html`). Changer la clé (`node scripts/livret.mjs newkey`) oblige à réimprimer le QR code. L'URL complète n'est notée nulle part dans ce dépôt.
