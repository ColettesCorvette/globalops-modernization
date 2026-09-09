# Configurations validées

À copier dans la racine de l'installation (`F:\Games\GO116\`).

## `dxvk.conf`
Plafond de framerate et compteur FPS. **Jamais réécrit par le jeu** — c'est le verrou fiable.

## `autoexec.cfg`
Cvars du moteur et profil actif. **Réécrit par le jeu à chaque sortie propre** ; les valeurs y survivent
(vérifié pour `MaxFPS`), mais l'ordre des lignes change et le fichier peut être réordonné.

`"profilename"` désigne le profil chargé. Absent ou vide → le jeu retombe sur `Player` et recrée
`Player.cfg` avec les défauts **640×480 en 16 bits**, qui empêchent le démarrage.

## `display-profile.cfg`
Extrait de référence des clés d'affichage à appliquer dans `Globalops/profile/<nom>.cfg`.
Ce n'est pas un fichier complet : à reporter clé par clé dans le profil existant, **jeu fermé**.
