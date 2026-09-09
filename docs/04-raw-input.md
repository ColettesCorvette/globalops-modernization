# Chantier 2 — Souris en raw input

**Objectif :** supprimer l'accélération et le lissage de DirectInput 8, obtenir une visée 1:1.
**Dépend de :** Ultimate ASI Loader (socle partagé avec le [chantier 3](05-fps-physics.md)).

## Ce qui est établi

`globalops.exe` importe `DINPUT8.dll` **statiquement** — vérifié dans la table d'imports :

```
ADVAPI32.dll, d3d8.dll, DDRAW.dll, DINPUT8.dll, GDI32.dll,
KERNEL32.dll, mss32.dll, ole32.dll, USER32.dll, VERSION.dll,
WINMM.dll, WSOCK32.dll
```

La souris passe donc par DirectInput 8, avec les défauts classiques de l'époque : accélération dépendante
du système, lissage interne, échantillonnage lié au framerate.

Le profil expose `MouseSensitivity`, `mouselook`, `inputrate` (valeur observée : `12.000000`) — des
réglages de confort, pas une correction du fond.

**Il n'existe aucun correctif tout prêt** pour ce jeu : trop confidentiel pour avoir attiré un
Widescreen Fixes Pack ou équivalent. Le plugin est à écrire.

## Socle : Ultimate ASI Loader

[github.com/ThirteenAG/Ultimate-ASI-Loader](https://github.com/ThirteenAG/Ultimate-ASI-Loader) (v9.7.x) —
DLL proxy qui se substitue à une DLL système et charge des plugins `.asi` depuis `scripts/` ou `plugins/`.

### Choix du nom de la DLL proxy — attention au conflit

**DXVK occupe déjà `d3d8.dll` et `d3d9.dll`.** Ne pas les utiliser.

| Candidat | Verdict |
|---|---|
| `dinput8.dll` | choix par défaut de l'ASI Loader, importé par le jeu — **recommandé** |
| `winmm.dll` | importé aussi ; repli si `dinput8` pose problème |
| `version.dll` | repli neutre |

Nuance : si le plugin doit lui-même intercepter DirectInput, se substituer à `dinput8.dll` demande de
relayer proprement les appels vers la vraie DLL système. L'ASI Loader gère ce relais, mais il faut le
vérifier avant de bâtir dessus. `winmm.dll` évite la question.

## Méthode

1. **Valider le socle.** Déposer l'ASI Loader, écrire un plugin vide qui ouvre un fichier de log au
   chargement. Vérifier qu'il se charge et que le jeu démarre normalement. Ne pas aller plus loin
   tant que ce point n'est pas acquis.
2. **Localiser la consommation d'entrées.** Dans Ghidra, sur `globalops.exe` (non protégé, donc
   entièrement analysable), repérer les appels à `IDirectInputDevice8::GetDeviceData` et
   `GetDeviceState`, puis remonter à l'endroit où les deltas alimentent la rotation de la vue.
3. **Enregistrer le raw input.** `RegisterRawInputDevices` sur la souris, collecte des `WM_INPUT`
   dans la boucle de messages.
4. **Substituer.** Remplacer les deltas DirectInput par les deltas bruts, en conservant l'échelle de
   `MouseSensitivity` pour ne pas casser les réglages existants.
5. **Configurer.** Fichier `.ini` : activation, multiplicateur, inversion Y.

## Critères de succès

- [ ] Le plugin se charge, le jeu démarre normalement
- [ ] Déplacement souris identique quel que soit le framerate
- [ ] Aucune accélération : deux mouvements identiques produisent la même rotation
- [ ] Rotation cohérente sur un test au tapis (distance physique → angle constant)
- [ ] Menus toujours utilisables (le curseur ne doit pas être affecté)

## Risques

- **Double entrée** : si DirectInput continue d'alimenter le jeu en parallèle, la visée double de vitesse.
  Il faut neutraliser la source d'origine, pas seulement en ajouter une.
- **Curseur des menus** : le HUD et les menus utilisent probablement le même chemin d'entrée.
  Cantonner la substitution au mode jeu.
- **Interaction avec le plafond FPS** : à traiter après le [chantier 3](05-fps-physics.md) si celui-ci
  modifie la boucle principale, pour ne pas déboguer deux changements à la fois.
