# lesrefletsdelaloubine

## Guide du séjour (page protégée par mot de passe)

`guide.html` est chiffré (AES-GCM + PBKDF2, côté client, aucun serveur) : le mot de passe n'apparaît jamais dans le code source. Pour le modifier ou changer le mot de passe : ouvrez `build-guide.html` directement dans votre navigateur (double-clic, pas de serveur nécessaire), éditez le contenu et/ou le mot de passe dans le formulaire, cliquez sur « Générer guide.html », puis remplacez le fichier `guide.html` du dépôt par celui téléchargé. Changer le mot de passe suppose toujours de régénérer `guide.html` de cette façon — il n'y a pas d'autre endroit où le modifier.

Mot de passe de démonstration actuellement en place : `motdepasse-a-changer` (à remplacer avant de communiquer le lien aux voyageurs).